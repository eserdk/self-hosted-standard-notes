#!/bin/sh

echo "Restoring $NOTES_DB..."
openssl enc -d -aes-256-cbc -k "$NOTES_DB_BACKUP_PASSWORD" -pbkdf2 -in /opt/mysql/backup/"$NOTES_DB".xb.enc | gzip -d | mysql -h mariadb -P 3306 -u root -p"$MYSQL_ROOT_PASSWORD"
echo "$NOTES_DB restored."