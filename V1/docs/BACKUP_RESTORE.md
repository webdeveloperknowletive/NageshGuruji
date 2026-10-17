# Database Backup & Disaster Recovery Guide

This document defines the backup schedules, snapshot procedures, and restoration runbooks for PostgreSQL and user-uploaded media.

---

## 1. Backup Schedule & Retention Policy

| Target | Frequency | Retention Period | Storage Location |
| :--- | :--- | :--- | :--- |
| **PostgreSQL Database** | Every 6 hours | 30 days | S3-compatible remote storage (Wasabi/AWS/Backblaze) or offsite VPS |
| **Uploaded Media Files** | Daily (incremental) | 90 days | Offsite block storage / encrypted rsync mirror |
| **System Configurations** | On every modification | Git Version Control | Private Git repository (`.env` files stored in encrypted vault) |

---

## 2. Automated PostgreSQL Backup (Cron on Host VPS)

Create `/usr/local/bin/backup-japam-db.sh` on the Hostinger VPS:

```bash
#!/bin/bash
set -eo pipefail

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/var/backups/japam"
DB_CONTAINER="japam-postgres"
DB_NAME="japam_db"
DB_USER="japam_user"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting PostgreSQL backup..."
docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" -Fc "$DB_NAME" > "$BACKUP_DIR/db_${DB_NAME}_${TIMESTAMP}.dump"

# Keep last 14 days locally
find "$BACKUP_DIR" -type f -name "db_${DB_NAME}_*.dump" -mtime +14 -delete

echo "[$(date)] PostgreSQL backup completed successfully: db_${DB_NAME}_${TIMESTAMP}.dump"
```

Make executable and add to crontab (`crontab -e`):
```cron
0 */6 * * * /usr/local/bin/backup-japam-db.sh >> /var/log/japam_backup.log 2>&1
```

---

## 3. Database Restoration Runbook

In the event of data corruption or disaster recovery:

### Step 1: Transfer Dump to Target Host
```bash
scp user@backup-server:/var/backups/japam/db_japam_db_YYYYMMDD_HHMMSS.dump /tmp/
```

### Step 2: Restore into PostgreSQL Container
```bash
# Terminate existing connections to database
docker exec -i japam-postgres psql -U japam_user -d postgres -c \
  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'japam_db' AND pid <> pg_backend_pid();"

# Re-create clean database
docker exec -i japam-postgres psql -U japam_user -d postgres -c "DROP DATABASE IF EXISTS japam_db;"
docker exec -i japam-postgres psql -U japam_user -d postgres -c "CREATE DATABASE japam_db OWNER japam_user;"

# Restore from custom-format dump
cat /tmp/db_japam_db_YYYYMMDD_HHMMSS.dump | docker exec -i japam-postgres pg_restore -U japam_user -d japam_db --clean --if-exists --no-owner
```

### Step 3: Run Validation Queries
```bash
docker exec -i japam-postgres psql -U japam_user -d japam_db -c "SELECT count(*) AS total_orders FROM orders;"
docker exec -i japam-postgres psql -U japam_user -d japam_db -c "SELECT count(*) AS total_products FROM products;"
```

---

## 4. Media & Uploads Restoration

The upload directory (`/app/uploads`) is mounted as a persistent volume. To archive and restore media:

### Backup Uploads
```bash
tar -czvf /var/backups/japam/uploads_$(date +"%Y%m%d").tar.gz /var/coolify/volumes/japam-uploads
```

### Restore Uploads
```bash
tar -xzvf /var/backups/japam/uploads_YYYYMMDD.tar.gz -C /
```
