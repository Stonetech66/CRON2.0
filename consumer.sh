#!/bin/sh
cd /app/

echo "starting consumer >>>"

python -m CRON2.core.consumer
