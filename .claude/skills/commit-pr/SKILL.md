---
name: commit-pr
description: Write a commit message and PR description to the team standard. Use when asked to commit, open a PR, or draft either.
---

Write the commit message and PR text for the current staged or branch changes.

Commit message:
- Conventional Commits: `type(scope): subject`. Types: feat, fix, refactor, test, docs, chore.
- Subject at most 72 characters, imperative mood, no trailing period.
- Body only if it explains why. Never restate the diff. No emoji, no marketing words.

PR description:
- Fill in the four headings from `.github/pull_request_template.md`: What, Why, How verified, Risk.
- Under 150 words total. Do not list files changed; the diff already shows that.
- "How verified" names the command you ran and its result.

Before writing, run `git diff --cached` (or `git diff main...HEAD` for a branch) and read it.
Output the commit message in one fenced block and the PR description in another. Do not run `git commit` or `gh pr create` unless asked.

## Bad example (do not produce this)

```
✨ Enhance metrics calculation with comprehensive improvements

This comprehensive change enhances the metrics module by:
- Updated metrics.py to improve median calculation
- Updated tests/test_metrics.py to add new test
- Updated cli.py formatting
These improvements ensure robust, production-ready behavior. 🚀
```

## Good rewrite

```
fix: exclude open requests from median days to close

Open requests have no closed_at, so they were measured to today and
inflated the median for any department with a backlog.
```
