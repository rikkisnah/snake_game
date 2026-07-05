<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Develop

Use this workflow for every code or governance change.

## Loop

Understand -> Plan -> Implement -> Test -> Refactor -> Review.

## Steps

1. Start from a feature branch.
2. Decide whether subagents apply before implementation.
3. Make one logical edit at a time.
4. Run targeted tests for fast feedback.
5. Run `make validate` before handoff.
6. Update docs in the same change set when behavior changes.

## Subagents

Use available Claude or Codex subagent/delegation capabilities for parallelizable, specialized, or independently reviewable work. Keep tiny, blocking, tightly coupled, or duplicate work local.

## Commands

```bash
make format
make test
make test-<name>
make lint
make score
make validate
```

## Documentation Drift

Documentation drift is a bug. A change that alters behavior, commands, configuration, dependencies, setup, validation, deployment, or user workflows is incomplete unless affected docs are updated in the same change set.

Check `README.md`, `AGENTS.md`, `MEMORY.md`, `CONTEXT.md`, workflow docs, `docs/agent/`, `docs/adr/`, and Makefile help text.

## Scorecard Updates

When introducing new stable architecture boundaries or runtime invariants, update `scripts/score_architecture.py` and `tests/test_score_architecture.py`.

## Clean-Code Loop

Before finalizing, review your own diff for naming, function size, duplication, hidden side effects, error handling, tests, unnecessary abstractions, and convention drift.
