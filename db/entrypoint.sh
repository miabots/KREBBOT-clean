#!/bin/bash

# Function to handle shutdown signal
dump_database() {
    pg_dump -U postgres -d KREBBOTDB > data.sql
    # Assuming a mounted volume to the host (modify accordingly)
    cp data.sql /backups/data_$(date +"%Y-%m-%d_%H-%M-%S").sql
}

# Trap SIGTERM and execute the dump_database function
trap 'dump_database' SIGTERM

# Start the Postgres server with correct permissions
#chmod 0700 /var/lib/postgresql/data
#su -c "postgres -D /var/lib/postgresql/data" -s /bin/bash postgres

# Start the Postgres server
echo "Starting Postgres server..."
/docker-entrypoint.sh postgres