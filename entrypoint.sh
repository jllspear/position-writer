#!/bin/sh
set -e

# Run database migrations
alembic upgrade head

# Execute the command passed as arguments
exec "$@"
