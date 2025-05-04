.PHONY: setup install lint format mypy test clean

# Variables
PYTHON = python3
PIP = $(PYTHON) -m pip
VENV = venv
VENV_BIN = $(VENV)/bin
PYTEST = $(VENV_BIN)/pytest
FLAKE8 = $(VENV_BIN)/flake8
BLACK = $(VENV_BIN)/black
MYPY = $(VENV_BIN)/mypy

# Default target
all: lint format mypy test

# Setup virtual environment and install dependencies
setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Install the package in development mode
install:
	$(PIP) install -e .

# Run linting
lint:
	$(FLAKE8) *.py

# Format code
format:
	$(BLACK) *.py

# Run type checking
mypy:
	$(MYPY) --ignore-missing-imports *.py

# Run tests
test:
	$(PYTEST) -v

# Clean up
clean:
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	find . -name "*.pyc" -delete