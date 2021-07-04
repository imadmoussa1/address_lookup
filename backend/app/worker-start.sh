#! /usr/bin/env bash
set -e

python /app/app/celeryworker_pre_start.py

celery -A app.worker worker -Q main-queue -c 3 --loglevel=info -n worker1 &

if [ -f "celerybeat.pid" ]; then
  rm celerybeat.pid
fi
celery -A app.worker beat --loglevel=info