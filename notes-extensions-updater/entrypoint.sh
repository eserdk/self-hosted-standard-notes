#!/bin/bash

printenv | grep -E "GH|HOST|DELETE_OLD" >> /etc/environment

if ! [ "$(ls -A /app/public)" ]; then
  echo "Extensions directory is empty. Fetching extensions..."
  /venv/bin/python /app/update.py
  echo "Completed."
fi

cron -f
