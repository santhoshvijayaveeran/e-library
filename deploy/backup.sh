#!/usr/bin/env bash
# DB + media backup.  Cron: 0 2 * * * bash /home/ubuntu/E-library/deploy/backup.sh
set -euo pipefail
cd /home/ubuntu/E-library
set -a; source .env; set +a
mkdir -p ~/backups
TS=$(date +%F)
PGPASSWORD="$DB_PASSWORD" pg_dump -h localhost -U "$DB_USER" "$DB_NAME" | gzip > ~/backups/db-$TS.sql.gz
tar -czf ~/backups/media-$TS.tar.gz media 2>/dev/null || true
find ~/backups -type f -mtime +7 -delete
