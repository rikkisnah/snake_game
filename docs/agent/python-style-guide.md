<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Python Style Guide

## Defaults

- Use Python 3.11 or newer unless the project specifies otherwise.
- Prefer `uv` for dependency sync and command execution.
- Use type hints for public functions and explicit return types.
- Keep imports grouped: standard library, third-party, local.
- Prefer dataclasses, `TypedDict`, or Pydantic models for structured data crossing boundaries.
- Keep modules cohesive and functions small.

## Error Handling

- Use specific exceptions.
- Never use bare `except:`.
- Catch exceptions only when adding context, recovering, or converting to a clearer domain error.
- Do not swallow exceptions silently.

## Tooling

- Format with configured `ruff format` or `black`.
- Lint with configured project tools and `python -m compileall`.
- Test with `uv run pytest` when pytest is configured, otherwise `python3 -m unittest`.
