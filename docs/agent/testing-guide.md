<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Testing Guide

Tests are executable documentation.

## Required Guidance

- Every behavior change needs tests unless purely cosmetic.
- Prefer testing public behavior over private implementation details.
- Cover happy path, edge cases, invalid input, permissions, dependency failures, and regressions.
- Avoid live cloud/backend calls in the normal offline test suite.
- Use targeted tests during development and full validation before handoff.
- Do not weaken tests just to make a change pass.
- Add regression tests for bugs.

## Commands

```bash
make test
make test-<name>
make lint
make score
make validate
```

## Test Design

Good tests describe the behavior users or callers rely on. Avoid tests that only mirror private implementation details or make refactoring expensive without protecting behavior.
