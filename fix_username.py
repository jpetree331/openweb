#!/usr/bin/env python3
"""
OpenWebUI Username Fix Script (run-once on startup)
Renames 'Jessica Petree' to 'Jess Petree' or removes the duplicate account.
Uses a sentinel file so it only runs once; remove the sentinel to re-run.
"""

import os
import shutil
import sqlite3
import sys

# Names to fix (full name as stored in DB)
NAME_WRONG = "Jessica Petree"
NAME_CORRECT = "Jess Petree"
BACKUP_SUFFIX = ".pre_username_fix_backup"

# Set to "1" in Railway Variables to run the fix again (ignores sentinel)
FORCE_RERUN = os.environ.get("FORCE_USERNAME_FIX", "").strip().lower() in ("1", "true", "yes")


def get_sentinel_path(db_path: str) -> str:
    return os.path.join(os.path.dirname(db_path), ".username_fix_applied")


def _backup_db(db_path: str) -> None:
    """Copy database to a backup file before any write. Idempotent: skips if backup already exists."""
    backup_path = db_path + BACKUP_SUFFIX
    if os.path.exists(backup_path):
        return
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✓ Backup created: {backup_path}")
    except Exception as e:
        print(f"⚠ Could not create backup: {e} (continuing anyway)")


# Your Railway volume mount path (from OpenWebUI data volume settings)
DEFAULT_DATA_MOUNT_PATH = "/opt/render/project/src/data"


def get_db_path() -> str | None:
    """Resolve OpenWebUI database path: DATA_DIR or volume mount path, then fallbacks."""
    data_dir = os.environ.get("DATA_DIR", "").strip()
    if data_dir:
        path = os.path.join(data_dir, "webui.db")
        if os.path.exists(path):
            print(f"✓ Found database at: {path} (from DATA_DIR)")
            return path
    # Check actual volume mount path first, then common locations
    candidates = [
        os.path.join(DEFAULT_DATA_MOUNT_PATH, "webui.db"),
        "/app/data/webui.db",
        "/app/backend/data/webui.db",
        "/data/webui.db",
        os.path.join(os.getcwd(), "data", "webui.db"),
    ]
    for path in candidates:
        if os.path.exists(path):
            print(f"✓ Found database at: {path}")
            return path
    print("✗ Database not found. Tried:")
    if data_dir:
        print(f"  - {os.path.join(data_dir, 'webui.db')} (DATA_DIR)")
    for path in candidates:
        print(f"  - {path}")
    return None


def get_user_columns(cursor) -> list:
    """Return list of column names for the user table."""
    cursor.execute("PRAGMA table_info(user)")
    return [row[1] for row in cursor.fetchall()]


def show_users(cursor) -> list:
    """Display all users and return rows (id, email, name, username?, role, created_at)."""
    cols = get_user_columns(cursor)
    select = ["id", "email", "name", "role", "created_at"]
    if "username" in cols:
        select.insert(3, "username")
    col_list = ", ".join(select)
    cursor.execute(f"SELECT {col_list} FROM user")
    rows = cursor.fetchall()
    print("\n" + "=" * 60)
    print("CURRENT USERS IN DATABASE:")
    print("=" * 60)
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"  Email: {row[1]}")
        print(f"  Name: {row[2]}")
        if "username" in cols:
            idx = select.index("username")
            print(f"  Username: {row[idx]}")
        print(f"  Role: {row[select.index('role')]}")
        print(f"  Created: {row[select.index('created_at')]}")
        print("-" * 60)
    return rows


def fix_username(db_path: str) -> bool:
    """Apply the username fix once; create sentinel on success."""
    sentinel = get_sentinel_path(db_path)
    if os.path.exists(sentinel) and not FORCE_RERUN:
        print("✓ Username fix already applied (sentinel exists). Skipping.")
        return True
    if FORCE_RERUN:
        print("→ FORCE_USERNAME_FIX=1: running fix even if sentinel exists.")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        tables = [r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        if "user" not in tables:
            print("✓ No user table yet (fresh DB). Nothing to fix.")
            conn.close()
            with open(sentinel, "w") as f:
                f.write("username fix applied\n")
            return True
        cols = get_user_columns(cursor)
        users = show_users(cursor)

        # Build a simple (id, name, username?) view for matching
        name_idx = 2
        username_idx = cols.index("username") if "username" in cols else None
        has_jessica = any(
            (row[name_idx] == NAME_WRONG) or (username_idx is not None and row[username_idx] == NAME_WRONG)
            for row in (cursor.execute("SELECT id, email, name, role, created_at" + (", username" if "username" in cols else "") + " FROM user").fetchall())
        )
        cursor.execute("SELECT id, name" + (", username" if "username" in cols else "") + " FROM user")
        all_rows = cursor.fetchall()
        jessica_row = None
        jess_row = None
        for row in all_rows:
            n = row[1]
            un = row[2] if len(row) > 2 else None
            if n == NAME_WRONG or un == NAME_WRONG:
                jessica_row = row
            if n == NAME_CORRECT or un == NAME_CORRECT:
                jess_row = row

        if jessica_row and not jess_row:
            print(f"\n✓ Found '{NAME_WRONG}' account; no '{NAME_CORRECT}' account.")
            print(f"→ Renaming to '{NAME_CORRECT}'...")
            jessica_id = jessica_row[0]
            _backup_db(db_path)
            cursor.execute("UPDATE user SET name = ? WHERE id = ?", (NAME_CORRECT, jessica_id))
            if "username" in cols:
                cursor.execute("UPDATE user SET username = ? WHERE id = ?", (NAME_CORRECT, jessica_id))
            conn.commit()
            print("✓ Successfully renamed to Jess Petree.")

        elif jessica_row and jess_row:
            print(f"\n⚠ Both '{NAME_WRONG}' and '{NAME_CORRECT}' exist.")
            jessica_id = jessica_row[0]
            jess_id = jess_row[0]
            _backup_db(db_path)
            # Merge: give Jess account the same login (email + password) as Jessica, then remove Jessica.
            # That way you log in with your current email/password and get Jess's chats.
            print("→ Merging: copying Jessica's login (email+password) to Jess, then removing Jessica...")
            cursor.execute(
                "UPDATE auth SET email = (SELECT email FROM auth WHERE id = ?), password = (SELECT password FROM auth WHERE id = ?) WHERE id = ?",
                (jessica_id, jessica_id, jess_id),
            )
            cursor.execute("DELETE FROM auth WHERE id = ?", (jessica_id,))
            cursor.execute("DELETE FROM user WHERE id = ?", (jessica_id,))
            conn.commit()
            print("✓ Merged. Log in with your current email and password — you'll see Jess Petree with all chats.")

        else:
            print(f"\n✓ No change needed (no '{NAME_WRONG}' account found).")

        print("\n" + "=" * 60)
        print("FINAL USER STATE:")
        print("=" * 60)
        show_users(cursor)
        conn.close()

        with open(sentinel, "w") as f:
            f.write("username fix applied\n")
        print(f"\n✓ Sentinel created: {sentinel} (script will skip on next startup)")
        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def main() -> int:
    print("OpenWebUI Username Fix Script (Jess / Jessica Petree)")
    print("=" * 60)
    db_path = get_db_path()
    if not db_path:
        return 1
    ok = fix_username(db_path)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
