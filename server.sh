#!/bin/sh
set -e
cd /app/
echo "starting server 🚀"

uvicorn CRON2.main:app --host 0.0.0.0 --port $PORT
