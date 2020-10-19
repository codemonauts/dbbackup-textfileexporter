# dbbackup-textfileexporter

Export metrics about your local database backups to Prometheus.

# Requirements & Assumptions
 1) This scripts needs Python >= 3.6 without any additional librarys
 2) All backup files need to be written to one folder
 3) All filenames must match the pattern `<database name>-YYYY-MM-DD.<file extension>`


# Usage
Change the path where your backup files are create in the top part of the script (`BACKUP_DIR`).

The metrics get written to stdout so you can pipe the ouput into a file which gets then served by the node-exporter
```
dbbackup_exporter.py > /var/lib/prometheus/node-exporter/databases.prom
```


# Example metric

```
# HELP database_backup_file_size Size of latest backup file in bytes
# TYPE database_backup_file_size gauge
database_backup_file_size{database="my_database"} 160464896
# HELP database_backup_file_timestamp Timestamp of latest backup file
# TYPE database_backup_file_timestamp gauge
database_backup_file_timestamp{database="my_database"} 1603054802
```

# Example rules

```
  # Alert after 30h for daily backups to avoid false-positives due to timezone mismatch
  - alert: NoDatabaseBackup
    expr: (time() - database_backup_file_timestamp) / 3600 > 30
    for: 5m
    annotations:
      description: 'Es wurd kein tägliches Backup erzeugt'
      summary: 'Kein Backup für {{ $labels.database }} auf {{ $labels.instance }} angelegt'

  # Less than 1Kb is considered empty
  - alert: EmptyDatabaseBackup
    expr: database_backup_file_size < 1024
    for: 5m
    annotations:
      description: 'Die Backupdatei ist leer'
      summary: 'Leeres Backup für {{ $labels.database }} auf {{ $labels.instance }} angelegt'
```
