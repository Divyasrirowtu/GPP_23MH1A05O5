#!/bin/bash
set -euo pipefail

# Ensure directories exist
mkdir -p /data /cron

# Install cron job if cron file exists in repo (safe to run multiple times)
if [ -f /app/cron/2fa-cron ]; then
    crontab /app/cron/2fa-cron || true
fi

# Start cron (daemon)
service cron start || cron &

# Start the FastAPI server with Uvicorn on 0.0.0.0:8080
exec uvicorn api:app --host 0.0.0.0 --port 8080
