#!/bin/bash
set -e

# Function to wait for PostgreSQL to be ready
wait_for_postgres() {
    echo "Waiting for PostgreSQL to be ready..."
    until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 2
    done
    echo "PostgreSQL is up and running!"
}

# Function to run database migrations
run_migrations() {
    echo "Running database migrations..."
    PYTHONPATH=/app alembic upgrade head
}

# Function to initialize the database
init_db() {
    echo "Initializing database with default data..."
    python /app/init_db.py
}

# Main execution
case "$1" in
    web)
        wait_for_postgres
        run_migrations
        init_db
        echo "Starting FastAPI application..."
        exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    worker)
        wait_for_postgres
        echo "Starting Celery worker..."
        exec celery -A app.worker.celery_app worker --loglevel=info
        ;;
    *)
        exec "$@"
        ;;
esac
