#!/bin/bash

# Exit on error
set -e

echo "Running tests..."

# Run tests with coverage
pytest --cov=app --cov-report=term-missing tests/

echo "Tests completed!"
