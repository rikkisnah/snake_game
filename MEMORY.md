<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Project Memory

Durable, non-secret project context for future agents and maintainers.

`MEMORY.md` is durable context, not the source of truth. `AGENTS.md`, `README.md`, Makefile targets, workflow docs, and code remain authoritative.

## Project Context

- Project: `snake_game`
- Runtime type: `cli` profile for a local graphical Pygame desktop application
- Language profile: `python`
- Maturity: `standard`

## Stable Facts

- This repository uses `AGENTS.md` as the authoritative agent contract.
- `CLAUDE.md` must remain a symlink to `AGENTS.md`.
- `make validate` is the full local validation gate.
- `scripts/score_architecture.py` is the local governance scorecard.
- `make setup` installs Pygame into the ignored local `.venv` with `uv`.

## Decisions

- Use local-first validation through Makefile targets.
- Treat documentation drift as incomplete work.
- Require OCA/OpenAI AI-assistance disclosure headers for generated artifacts.

## Assumptions

- Project-specific runtime behavior should be documented in `README.md` and workflow docs.
- Scorecard runtime-contract checks should be customized as the repo matures.

## Constraints

- Do not commit secrets or local-only environment files.
- Keep generated governance files consistent with `AGENTS.md`.

## Known Issues Or Follow-Ups

- Add project-specific runtime-contract scorecard checks when stable invariants are known.

## Proposals

Use this section for non-authoritative proposed updates. Move accepted rules into `AGENTS.md`, docs, Makefile, or code.

## Do Not Store Here

Do not store credentials, tokens, wallet files, private keys, customer data, bearer headers, auth files, private URLs with credentials, huge logs, or temporary scratch notes in `MEMORY.md`.
