# Username Fix (Jess / Jessica Petree) — One-time migration

This document describes the one-time username fix for OpenWebUI on Railway and how to remove it after use.

---

## How to implement (deploy the fix)

1. **Commit and push**  
   Make sure these files are in your repo and pushed to GitHub:
   - `fix_username.py`
   - `entrypoint.sh`
   - `Dockerfile` (with the entrypoint and COPY lines for the fix)

2. **Set Railway variable**  
   In Railway: open your project → **Variables** → add:
   - **Name:** `DATA_DIR`
   - **Value:** `/opt/render/project/src/data`  
   (This matches your volume mount path so OpenWebUI and the fix script use the same DB.)

3. **Redeploy**  
   Push to GitHub (or use Railway’s “Redeploy” on the latest deployment). Railway will rebuild the image and start the container.

4. **Check logs**  
   In Railway: open the service → **Deployments** → select the latest → **View logs**. You should see:
   - `Running username fix script (no-op if already applied)...`
   - `✓ Found database at: /opt/render/project/src/data/webui.db`
   - `CURRENT USERS IN DATABASE:` (and your users)
   - Either `✓ Successfully renamed to Jess Petree.` or `✓ Deleted Jessica Petree account.` or `✓ No change needed...`
   - `Starting OpenWebUI...`

5. **Log in**  
   Open your app URL and sign in as **Jess Petree** (same password you used for the Jess or Jessica account). Your chats should be there.

6. **Remove the fix later**  
   After you’ve confirmed everything works, revert the Dockerfile and delete the fix files as described in **“After the fix: remove the one-time logic”** below.

---

## Safety (will it destroy data?)

- **No accidental wipe**: The script only updates or deletes the single user with name/username **"Jessica Petree"**. All writes use parameterized queries and that exact string; it never deletes by a broad condition or touches other users/tables.
- **Commit only on success**: If anything throws (e.g. DB locked, disk error), the script exits without calling `commit()`, so the transaction is rolled back and **nothing is written**.
- **Backup before changes**: Right before any rename or delete, the script copies the database to **`webui.db.pre_username_fix_backup`** in the same directory (once per run). If something goes wrong, you can stop OpenWebUI, replace `webui.db` with that file, and restart.
- **Sentinel only after success**: The "already applied" sentinel is written only after a successful run, so a crash won’t leave the DB half-fixed and the script thinking it’s done.

## What it does

- **Finds the DB** using `DATA_DIR` (e.g. `/app/data`) or fallback paths, so the database path is correct for your deployment.
- **Lists all users** so you can confirm "Jess Petree" and "Jessica Petree" in the logs.
- **Rename**  
  If only "Jessica Petree" exists: renames that account to **"Jess Petree"** (both `name` and `username`).
- **Delete duplicate**  
  If both "Jessica Petree" and "Jess Petree" exist: deletes the "Jessica Petree" user (and her `auth` row) so you keep one account and all chats stay with "Jess Petree".

## Database path

- **Your volume mount path**: The OpenWebUI data volume is mounted at **`/opt/render/project/src/data`** (Railway Settings). The database is **`/opt/render/project/src/data/webui.db`**.
- **Script behavior**: The fix script checks `DATA_DIR` first (if set), then **`/opt/render/project/src/data/webui.db`** (your mount path), then other common paths.
- **OpenWebUI**: Set **`DATA_DIR=/opt/render/project/src/data`** in Railway Variables so OpenWebUI reads/writes the DB on the volume. If you don’t set this, the app may use `/app/data` and the script will still find the DB on the volume.

## How it’s integrated

1. **`fix_username.py`**  
   - Connects to the SQLite DB, shows users, then either renames "Jessica Petree" → "Jess Petree" or deletes the "Jessica Petree" account.  
   - Writes a **sentinel file** next to the DB: `{data_dir}/.username_fix_applied`.  
   - On later starts it sees the sentinel and **skips** (run-once).

2. **`entrypoint.sh`**  
   - Runs `python3 /app/fix_username.py` (failure is ignored so a missing DB doesn’t block startup).  
   - Then starts OpenWebUI (or runs Railway’s start command if provided).

3. **Dockerfile**  
   - Copies `fix_username.py` and `entrypoint.sh` into the image and sets `ENTRYPOINT ["/app/entrypoint.sh"]`.

So on **every** startup the entrypoint runs; the Python script does real work only the **first** time (until the sentinel exists).

## Railway: volume and variables

- **Volume**: Your data volume is mounted at **`/opt/render/project/src/data`**. The DB path is **`/opt/render/project/src/data/webui.db`**. The fix script checks this path first (after `DATA_DIR`).
- **Env**: Set **`DATA_DIR=/opt/render/project/src/data`** in Railway Variables so OpenWebUI uses the volume for all data (recommended).

## After the fix: remove the one-time logic

When you’ve confirmed the fix (e.g. logged in as "Jess Petree" and see your chats):

1. **Revert deployment to normal** (no script, no entrypoint):
   - Remove the entrypoint and fix script from the Dockerfile (see below).
   - Commit and push so Railway redeploys.

2. **Optional**: Delete the sentinel file from the volume so the script would run again if you ever re-add it:
   - In the same directory as `webui.db`, delete `.username_fix_applied`.  
   - You don’t have to do this unless you plan to run the fix again.

### Dockerfile revert (after fix)

Remove the fix from the Dockerfile so it looks like this again:

```dockerfile
# Create data directory
RUN mkdir -p /app/data

# Run OpenWebUI (use PORT env var if provided, otherwise default to 8080)
CMD sh -c "open-webui serve --host 0.0.0.0 --port ${PORT:-8080}"
```

Delete these lines (or the block you added):

- `COPY fix_username.py ...`
- `COPY entrypoint.sh ...`
- `RUN chmod +x /app/entrypoint.sh`
- `ENTRYPOINT ["/app/entrypoint.sh"]`
- And change `CMD` back to a single line:  
  `CMD sh -c "open-webui serve --host 0.0.0.0 --port ${PORT:-8080}"`

You can also delete the files `fix_username.py`, `entrypoint.sh`, and this `USERNAME_FIX.md` from the repo if you no longer need them.

## Re-running the fix

If you need to run the fix again (e.g. after restoring a backup):

1. Remove the sentinel file in the data directory (e.g. `/app/data/.username_fix_applied` on the volume).
2. Redeploy with the entrypoint and script still in the image, or temporarily add them back and redeploy.
