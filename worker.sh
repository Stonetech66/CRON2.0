#!/usr/bin/env bash 
cd /app/

echo "starting worker >>>"

python -m CRON2.core.worker
