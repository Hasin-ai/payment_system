#!/bin/bash

# Exit on error
set -e

echo "Starting payment gateway system..."

# Start PostgreSQL
echo "Starting PostgreSQL..."
sudo service postgresql start

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h localhost -p 5432 -U postgres; do
    echo "PostgreSQL is not ready yet. Retrying in 2 seconds..."
    sleep 2
done

# Create database if it doesn't exist
echo "Ensuring database exists..."
createdb -h localhost -U postgres -p 5432 payment_db 2> /dev/null || true

# Run database migrations
echo "Running database migrations..."
cd /app
PYTHONPATH=/app alembic upgrade head

# Initialize database with default data
echo "Initializing database with default data..."
python init_db.py

# Start the FastAPI application
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo "Payment gateway system is running!"

# Keep the container running
tail -f /dev/null
