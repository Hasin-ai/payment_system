.PHONY: install test lint format check-style run build-docker run-docker stop-docker clean-docker

# Variables
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
ALEMBIC = $(VENV)/bin/alembic
PYTEST = $(VENV)/bin/pytest
BLACK = $(VENV)/bin/black
ISORT = $(VENV)/bin/isort
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy

# Install dependencies
install:
	echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run tests
test:
	$(PYTEST) tests/ -v --cov=app --cov-report=term-missing

# Run linters
lint:
	$(FLAKE8 app/

# Format code
format:
	$(BLACK) app/
	$(ISORT) app/

# Check code style
check-style:
	$(BLACK) --check app/
	$(ISORT) --check-only app/
	$(FLAKE8) app/

# Type checking
type-check:
	$(MYPY) app/

# Run the application
run:
	$(PYTHON) -m uvicorn app.main:app --reload

# Database migrations
migrate:
	$(ALEMBIC) revision --autogenerate -m "$(m)"
	$(ALEMBIC) upgrade head

# Build Docker image
build-docker:
	docker-compose build

# Start Docker containers
run-docker:
	docker-compose up -d

# Stop Docker containers
stop-docker:
	docker-compose down

# Clean Docker resources
clean-docker:
	docker-compose down -v
	docker system prune -f
	docker volume prune -f

# Clean up
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
