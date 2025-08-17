# Makefile for the Snake Game

# Variables
PYTHON = python3
VENV_DIR = venv

# Targets
.PHONY: all install run test clean

all: install

# Install dependencies
install: $(VENV_DIR)/bin/activate
	@echo "Installing dependencies..."
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt

# Create virtual environment
$(VENV_DIR)/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip

# Run the game
run: install
	@echo "Starting the game..."
	. $(VENV_DIR)/bin/activate && $(PYTHON) snake_game.py

# Run tests
test: install
	@echo "Running tests..."
	. $(VENV_DIR)/bin/activate && $(PYTHON) -m unittest discover

# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -f .coverage

