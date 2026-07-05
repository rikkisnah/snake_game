<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Snake Game

## Purpose

This is a local desktop implementation of the classic Snake game built with Python and Pygame. It includes player-name entry, persistent top-ten scores, fullscreen support, and a small easter egg.

The repository also includes local-first agentic engineering governance, clean-code guidance, scorecard gates, durable non-secret memory, and explicit workflow docs.

## Features

- Four-direction keyboard movement and wall/self collision detection.
- Persistent high scores in the ignored local file `high_scores.json`.
- Start, high-score, name-entry, gameplay, and game-over screens.
- Fullscreen switching with `F` and an occasional `@rekharoy` easter egg.

## Quick Start

```bash
make setup
make run
```

Run the full local validation gate separately:

```bash
make validate
```

## Common Commands

```bash
make setup
make install
make run
make format
make test
make lint
make score
make score-gate
make check
make validate
make clean
make clean-env
```

`make setup` creates `.venv` with `uv` and installs `pygame==2.6.1` from `requirements.txt`. `make install` is a compatibility alias.

## Controls

- Main menu: `SPACE` starts, `H` shows high scores, and `F` toggles fullscreen.
- Name entry: type up to 15 letters, numbers, spaces, underscores, or hyphens; press `ENTER` to continue.
- Gameplay: use the arrow keys to move and `F` to toggle fullscreen.
- Fullscreen: `ESC` returns to windowed mode.
- Game over: `C` starts again and `Q` quits.

## Validation

`make validate` is the full local gate. It compiles the Python sources, runs the gameplay tests with dummy video/audio drivers for headless environments, runs governance regression tests, and enforces the architecture score gate.

`make score` prints the governance scorecard. `make score-gate` fails unless every enabled scorecard dimension is 10/10.

## Agentic Development Workflow

- Read `AGENTS.md` before changing code.
- Use `MEMORY.md` only for durable non-secret project context.
- Use `CONTEXT.md` only as a short-lived branch-local placeholder.
- Keep changes small, reviewable, tested, and documented.
- Treat documentation drift as a bug.

## Documentation Map

- `AGENTS.md`: authoritative agent operating contract.
- `MEMORY.md`: durable non-secret project context.
- `CONTEXT.md`: temporary branch handoff placeholder.
- `docs/agent/`: clean-code, review, subagent, testing, and language guidance.
- `docs/adr/template.md`: architecture decision record template.
- `INSTALL.md`: setup workflow, when generated for this runtime.
- `DEVELOP.md`: daily development loop.
- `CREATE-PR.md`: local PR handoff workflow.
- `DEPLOY.md`: deployment workflow, when generated for this runtime.

## Security And Secrets

Never commit secrets, credentials, private keys, bearer tokens, raw auth files, customer data, huge logs, or local-only environment files. Use safe placeholders such as `<token>`, `<secret>`, `REPLACE_ME`, or committed `.env.example` files.
