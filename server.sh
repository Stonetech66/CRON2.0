#!/usr/bin/env bash 
cd /app/
echo "starting server >>>>"

uvicorn CRON2.main:app --host 0.0.0.0 --port 80
