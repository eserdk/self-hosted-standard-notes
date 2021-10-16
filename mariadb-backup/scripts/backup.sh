#!/bin/sh

echo "Backing up $NOTES_DB..."
mysqldump -h mariadb -P 3306 -u root -p"$MYSQL_ROOT_PASSWORD" --databases "$NOTES_DB" --single-transaction --triggers --routines | gzip -9 | openssl enc -e -aes-256-cbc -k "$NOTES_DB_BACKUP_PASSWORD" -pbkdf2 -out /opt/mysql/backup/"$NOTES_DB".xb.enc
echo "$NOTES_DB backed up."
