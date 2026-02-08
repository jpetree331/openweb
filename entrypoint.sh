#!/bin/sh
# Run username fix once, then start OpenWebUI
set -e
echo "Running username fix script (no-op if already applied)..."
python3 /app/fix_username.py || true
echo "Starting OpenWebUI..."
if [ $# -gt 0 ]; then
  exec "$@"
else
  exec sh -c "open-webui serve --host 0.0.0.0 --port ${PORT:-8080}"
fi
