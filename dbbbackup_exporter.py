#! /usr/bin/env python3
from os import listdir
from os.path import isfile, join, getsize, getmtime
from datetime import datetime
import sys
import re

### Configure this
BACKUP_DIR = "./testdir"
###


NAME_REGEX = r"(.*)-\d{4}-\d{2}-\d{2}\..*"
METRIC_FORMAT = 'database_backup_file_{metric_type}{{database="{name}"}} {value}'
DB_SIZES = {}
DB_TIMESTAMP = {}

files = [f for f in listdir(BACKUP_DIR) if isfile(join(BACKUP_DIR, f))]

for f in files:
    match = re.match(NAME_REGEX, f)
    if match:
        name = match.groups()[0]
    else:
        print(f"'{f}' didn't matched the name format", file=sys.stderr)
        continue
    size = getsize(join(BACKUP_DIR, f))
    timestamp = getmtime(join(BACKUP_DIR, f))

    # new value or newer value
    if DB_TIMESTAMP.get(name) is None or DB_TIMESTAMP[name] < timestamp:
        DB_SIZES[name] = size
        DB_TIMESTAMP[name] = timestamp


print("# HELP database_backup_file_size Size of latest backup file in bytes")
print("# TYPE database_backup_file_size gauge")
for name, size in DB_SIZES.items():
    print(METRIC_FORMAT.format(metric_type="size", name=name, value=size))

print("# HELP database_backup_file_timestamp Timestamp of latest backup file")
print("# TYPE database_backup_file_timestamp gauge")
for name, timestamp in DB_TIMESTAMP.items():
    print(METRIC_FORMAT.format(metric_type="timestamp", name=name, value=int(timestamp)))
