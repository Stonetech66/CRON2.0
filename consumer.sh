#!bin/bash

cd /app/

echo "starting worker >>>"

python -m CRON2.core.consumer
