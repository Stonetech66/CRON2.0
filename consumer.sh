#!/usr/bin/env bash 
cd /app/

echo "starting consumer >>>"

python -m CRON2.core.consumer
