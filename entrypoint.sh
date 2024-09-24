#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Reset the database
echo "Resetting the database..."
rm -f core/store.sqlite3
flask db upgrade -d core/migrations/

# Start the application
exec "$@"
