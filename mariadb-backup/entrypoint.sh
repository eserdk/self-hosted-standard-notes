#!/bin/sh

echo "$BACKUP_CRON_JOB" >> /etc/crontabs/root
printenv | grep -E "DATABASE|DB|USER|PASSWORD" >> /etc/environment
crond -f -d 8
