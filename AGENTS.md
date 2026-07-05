<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Agent Operating Contract

Maturity: standard
Runtime: cli (local Pygame desktop application; closest supported profile)
Language profile: python

`AGENTS.md` is the source of truth for agent instructions. CLAUDE.md must be a symlink to AGENTS.md in any directory that carries agent instructions.

Detailed guidance lives in:

- `docs/agent/clean-code-guide.md`
- `docs/agent/review-guide.md`
- `docs/agent/subagents-guide.md`
- `docs/agent/testing-guide.md`
- `docs/agent/python-style-guide.md`

## Project Context

Before editing, read local instructions, inspect nearby code and tests, and check `README.md`, `Makefile`, `MEMORY.md`, and `CONTEXT.md` when present.

## Operating Principles

- Readability over cleverness.
- Explicit behavior over implicit defaults.
- Small focused changes over broad rewrites.
- Existing project conventions over personal style.
- Tests and documentation are part of the change.
- Work with existing user changes; do not revert unrelated edits.

## Hard Requirements

- Keep `AGENTS.md` under 200 lines.
- Keep `CLAUDE.md` as a symlink to `AGENTS.md`.
- Run relevant tests for code changes.
- Run `make validate` before handoff when code, packaging, config, Makefile, validation, or workflow behavior changes.
- Run `make score` for docs-only governance changes.
- Use subagents where applicable for parallelizable, specialized, or independently reviewable work.
- Every enabled scorecard dimension should remain 10/10 unless the handoff documents a user-approved exception.
- Generated source, scripts, tests, automation, and substantial docs must include `#ai-assisted with OCA/OpenAI Model with human supervision`.

## Clean Code Requirements

Agentic code must be easy for humans and future agents to understand, modify, test, and verify.

Follow `docs/agent/clean-code-guide.md` for detailed rules. These rules are mandatory for source, scripts, tests, and automation changes.

- Use intention-revealing names based on domain language.
- Keep functions small, focused, and independently testable.
- Separate intent from implementation so high-level code reads clearly.
- Avoid clever code when straightforward code is possible.
- Make side effects explicit in names and structure.
- Prefer pure functions where practical.
- Keep boundaries clear between business logic, I/O, APIs, persistence, validation, logging, and presentation.
- Use tests as executable documentation for behavior, edge cases, failures, and regressions.
- Remove duplication by extracting repeated business logic into named concepts.
- Handle errors explicitly; never swallow exceptions silently.
- Make dependencies visible instead of hiding global state.
- Use formatters, linters, and consistent file organization.
- Prefer simple data structures and justify every abstraction.
- Protect important invariants with validation, types, tests, assertions, schemas, or constraints.
- Keep modules cohesive; avoid dumping unrelated code into `utils`, `helpers`, `common`, or `misc`.
- Design for likely change without inventing speculative architecture.
- Keep agent-generated diffs small and reviewable.

## Language Standards

Use the `python` profile in `docs/agent/python-style-guide.md`. Prefer configured project tooling over generic defaults.

## Modes Of Operation

- Inspect mode: reproduce, trace, explain root cause, and propose the smallest fix.
- Builder mode: make focused changes, update tests/docs, and validate.
- Reviewer mode: lead with bugs, risks, regressions, missing tests, stale docs, and security issues.

## Subagents

Follow `docs/agent/subagents-guide.md`. Use Claude or Codex delegation capabilities where work can be split safely, including independent exploration, focused review, test investigation, or implementation with disjoint write scopes.

Use a subagent when the task can be done independently and its result can be summarized compactly.

Do not use a subagent when the task needs constant shared context, sequential reasoning, or produces mostly overlapping work.

Apply this rule during skill-driven work as well as ordinary repo work. Before following a skill for non-trivial work, decide whether any steps can run in parallel or benefit from specialized review.

Delegate only when the task has clear ownership, expected output, constraints, and validation expectations. The primary agent remains responsible for integrating results, preserving user changes, and validating the final outcome.

Keep tiny, urgent blocking, tightly coupled, or duplicate work local.

## Testing And Tooling

- `make format`: apply safe formatting.
- `make test`: run tests.
- `make lint`: run lint/type/static checks.
- `make score`: print architecture scorecard.
- `make score-gate`: fail unless enabled dimensions meet the threshold.
- `make validate`: run full local validation.

## Documentation Update Rules

Documentation drift is a bug. A change that alters behavior, commands, configuration, dependencies, setup, validation, deployment, or user workflows is incomplete unless affected docs are updated in the same change set.

Check `README.md`, `AGENTS.md`, `MEMORY.md`, `CONTEXT.md`, workflow docs, `docs/agent/`, `docs/adr/`, and Makefile help text when behavior changes.

## Security And Secrets

Never write secrets, tokens, credentials, private keys, wallet files, bearer headers, auth files, customer data, huge logs, or raw sensitive material into repo docs, memory files, logs, prompts, tests, generated artifacts, or examples.

## Definition Of Done

- Code works and remains readable.
- Relevant tests pass.
- `make validate` passes or blockers are documented.
- Scorecard dimensions remain at the required threshold.
- Docs and workflow files match behavior.
- No secrets or local-only artifacts are committed.
