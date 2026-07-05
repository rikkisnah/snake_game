#ai-assisted with OCA/OpenAI Model with human supervision

SHELL := /bin/bash
PYTHON ?= python3
UV ?= uv
UV_CACHE_DIR ?= .uv-cache
VENV_DIR ?= .venv
APP_PYTHON := $(VENV_DIR)/bin/python
TEST_ENV := SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy

.DEFAULT_GOAL := help

.PHONY: help setup install run format test test-% lint score score-gate check validate clean clean-env

help:
	@printf '%s\n' 'Targets:'
	@printf '  %-14s %s\n' 'setup' 'Install or sync dependencies.'
	@printf '  %-14s %s\n' 'install' 'Compatibility alias for setup.'
	@printf '  %-14s %s\n' 'run' 'Start the Snake game.'
	@printf '  %-14s %s\n' 'format' 'Apply safe formatting when configured.'
	@printf '  %-14s %s\n' 'test' 'Run the test suite.'
	@printf '  %-14s %s\n' 'test-NAME' 'Run a focused test file or unittest target.'
	@printf '  %-14s %s\n' 'lint' 'Run syntax/lint checks.'
	@printf '  %-14s %s\n' 'score' 'Print governance scorecard.'
	@printf '  %-14s %s\n' 'score-gate' 'Require all scorecard dimensions to be 10/10.'
	@printf '  %-14s %s\n' 'check' 'Run lint and tests.'
	@printf '  %-14s %s\n' 'validate' 'Run check and score-gate.'
	@printf '  %-14s %s\n' 'clean' 'Remove local caches.'
	@printf '  %-14s %s\n' 'clean-env' 'Remove local env/cache.'

setup:
	@command -v $(UV) >/dev/null 2>&1 || { echo 'uv is required; install it before running make setup.'; exit 1; }
	@if [ ! -x "$(APP_PYTHON)" ]; then UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) venv --python "$(PYTHON)" "$(VENV_DIR)"; fi
	UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) pip install --python "$(APP_PYTHON)" -r requirements.txt

install: setup

run: setup
	"$(APP_PYTHON)" snake_game.py

format:
	@if [ -f pyproject.toml ] && command -v $(UV) >/dev/null 2>&1 && UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) run ruff --version >/dev/null 2>&1; then UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) run ruff format .; \
	elif [ -f pyproject.toml ] && command -v $(UV) >/dev/null 2>&1 && UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) run black --version >/dev/null 2>&1; then UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) run black .; \
	else echo 'No configured Python formatter found; format skipped.'; fi

test: setup
	$(TEST_ENV) "$(APP_PYTHON)" -m unittest discover -s . -p 'test_*.py' -v

test-%: setup
	@if [ -f "test_$*.py" ]; then $(TEST_ENV) "$(APP_PYTHON)" -m unittest "test_$*"; \
	elif [ -f "tests/test_$*.py" ]; then $(TEST_ENV) "$(APP_PYTHON)" -m unittest "tests.test_$*"; \
	elif [ -f "tests/$*.py" ]; then module=$$(printf '%s' "$*" | sed 's#/#.#g; s#\.py$$##'); $(TEST_ENV) "$(APP_PYTHON)" -m unittest "tests.$$module"; \
	else echo "No test target found for '$*'."; exit 2; fi

lint:
	$(PYTHON) -m compileall -q snake_game.py test_snake_game.py scripts tests

score:
	$(PYTHON) scripts/score_architecture.py

score-gate:
	$(PYTHON) scripts/score_architecture.py --min-score 10

check: lint test

validate: check score-gate

clean:
	rm -rf .coverage .pytest_cache .mypy_cache .ruff_cache htmlcov build dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

clean-env:
	rm -rf .venv .uv-cache
