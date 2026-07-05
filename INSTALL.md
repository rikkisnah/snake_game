<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Install

Use this runbook to set up `snake_game` locally.

## Required Inputs

```text
LOCAL_REPO="<absolute repo path>"
RUN_VALIDATION="<yes|no>"
```

Recommended defaults:

```text
LOCAL_REPO="$(pwd)"
RUN_VALIDATION="yes"
```

## Prerequisites

Confirm the standard command surface:

```bash
git --version
make --version
python3 --version
uv --version
```

Python 3.11 or newer, Make, and `uv` are required. The setup target installs Pygame from `requirements.txt` into the local `.venv`; it does not modify the system Python environment.

## Setup

```bash
cd "$LOCAL_REPO"
git status --short
make setup
```

Use Makefile targets for normal setup and validation. Start the graphical game from a desktop session with:

```bash
make run
```

The validation suite supplies dummy SDL video and audio drivers, so tests can run in a headless shell even though interactive gameplay requires a display.

## Validation

```bash
make validate
```

If validation is skipped, report why and list the exact command that should be run later.

## Expected Handoff

Report repo path, language/runtime version when known, dependency tool version when known, validation result, and skipped steps.
