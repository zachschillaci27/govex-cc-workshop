# service-metrics

## Project overview

Small CLI that reads a CSV of city 311 service requests and prints per-department
count, percent closed, and median days to close. Python 3.11+, standard library only.
Code lives in `src/service_metrics/`: `load.py` (CSV parsing), `metrics.py` (pure
functions), `cli.py` (output). Tests in `tests/`. Sample data in `data/sample_311.csv`.

## Commands

- `make test`: run pytest
- `make lint`: ruff check and format check
- `make run`: run the CLI on the sample data
- `make install`: editable install with dev deps

## Team norms

Commits:
- Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`).
- Subject at most 72 characters. Body only if it explains why. Never restate the diff.
- No emoji. No marketing language ("comprehensive", "robust", "enhance").

PRs:
- Use `.github/pull_request_template.md`. Under 150 words.
- No "summary of changes" section that duplicates the diff.

Architecture:
- Simplest thing that works.
- No new abstraction, class hierarchy, or dependency without a stated reason in the PR.
- Prefer editing existing code over adding new modules.

## Code style

- Every module starts with a 1 to 3 line docstring saying what it is for.
- Comments explain why, not what.
- Prefer boring, readable code over clever code.
- A teammate must be able to explain any function in this repo without Claude.
- Run `ruff format` on anything you touch (the PostToolUse hook does this for you).

## Verification

- Never claim a task is done without running `make test` and showing the result.
- For bug fixes: write a failing test first, show it failing, then fix it.
- Never edit a test to make it pass without saying so explicitly.
- The Stop hook runs the test suite; if it fails, keep working until it passes.

## Model and tool choice

- Haiku: quick lookups, codebase search, simple edits. Sonnet: default for implementation.
  Opus: planning, hard debugging, reviews.
- Use plan mode for anything touching more than 2 files.
- Deterministic logic (parsing, metrics, validation) stays in plain code. Never call an
  LLM for something a function or a query can do.
- Use a subagent when you need an isolated, read-only investigation that returns a
  short answer. `pr-reviewer` is the example in this repo.
