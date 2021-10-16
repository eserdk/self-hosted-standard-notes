#!/bin/bash
set -e

echo "Performing initial setup for $NOTES_DB..."
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "mysql" -e"CREATE DATABASE $NOTES_DB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER '$NOTES_USER' IDENTIFIED BY '$NOTES_PASSWORD'; GRANT ALL ON $NOTES_DB.* TO '$NOTES_USER'; FLUSH PRIVILEGES;"
echo "$NOTES_DB set up completed."
