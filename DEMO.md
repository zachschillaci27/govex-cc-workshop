# Workshop run-sheet

90 minutes, 7 people. Start in a Claude Code session at the repo root on branch `demo/simplify`.
Prep: `make install`, then `claude`. Run `/context` once so the audience sees CLAUDE.md
and the rules loaded.

## Planted problems (do not read aloud)

- `src/service_metrics/metrics.py`: `days_to_close` measures open requests to today, so
  `median_days_to_close` includes still-open requests. No test covers this. Parks and
  Sanitation have open rows in the sample data, so their medians drift upward every day.
- `src/service_metrics/legacy_report.py`: ~60 lines of ABC, registry, factory, and config
  dict that produce a table 10 lines could. Works, untested, no docstrings.

## 1. No shared standards

Pain: AI-padded commits and PRs, over-built architecture, every teammate has a different bar.

Files: `CLAUDE.md` (Team norms), `.claude/skills/commit-pr/SKILL.md`,
`.github/pull_request_template.md`.

Prompt: make a small edit first, for example change the CLI header from `closed%` to
`pct_closed` in `src/service_metrics/cli.py`, then `git add -A` and type:

    /commit-pr

Audience should see: a one-line Conventional Commit and a four-heading PR under 150 words.
Open the SKILL.md and show the bad example next to it. Point out that the norms live in the
repo, not in anyone's head.

## 2. Code nobody can explain

Pain: Claude writes it, nobody can explain it in review, so people ask Claude again.

Files: `CLAUDE.md` (Code style, Architecture), `.claude/skills/explain-change/SKILL.md`.

Prompts, in order:

    Explain src/service_metrics/legacy_report.py to me in plain language. What would I lose if it were 10 lines?

    Simplify legacy_report.py per our CLAUDE.md norms. Keep build_report's signature.

    /explain-change

Audience should see: Claude names the abstractions and admits none are needed; the
rewrite is a short function; the brief is under 200 words with two or three `file:line`
pointers, not a narration. Ask the room: could you review this from the brief alone?

## 3. Verification

Pain: wrong outputs shipped, AI-generated issues and CI noise nobody triages.

Files: `CLAUDE.md` (Verification), `.claude/hooks/run_tests.py` (Stop hook),
`.claude/hooks/format_py.py`, `.claude/rules/tests.md`.

Prompt:

    The median days to close for Parks looks too high. Investigate and fix it. Follow the Verification section of CLAUDE.md.

Audience should see:
1. Claude writes `test_median_excludes_open_requests` in `tests/test_metrics.py` and runs
   it. It fails because open requests are measured to today.
2. If Claude stops early with the test still red, the Stop hook blocks the stop and
   prints the pytest summary back to it. Say out loud: "That was the hook, not me."
3. Claude filters to closed requests in `median_days_to_close`, reruns `make test`, green.
4. The PostToolUse hook ran `ruff format` on every edited file with no prompt.

If Claude finds the bug and fixes it in one pass, trigger the hook manually: ask it to
"change the expected median in the new test to 99 and stop". The hook will refuse the stop.

## 4. Judgment calls

Pain: which model, when to use an agent, when AI is the wrong tool.

Files: `CLAUDE.md` (Model and tool choice), `.claude/agents/pr-reviewer.md` (`model: opus`,
read-only tools).

Prompt:

    Use the pr-reviewer agent to review this branch.

Audience should see: a separate agent runs on Opus with Read, Grep, Glob and limited Bash,
returns at most 5 ranked findings as `severity | file:line | problem | fix`, no praise.
Open the agent file and show that the model and tool limits are config, not a prompt
someone has to remember. Mention the illustrative `.github/workflows/claude-review.yml`.

## 5. Trust

Pain: what does the tool read, and who decided that.

Files: `.claude/settings.json` (permissions), `.env.example`, `data/private/.gitkeep`.

Prompts:

    cat .env

    Read whatever is in data/private and summarise it.

    Push this branch to origin.

Audience should see: the first two are denied by the `Read` deny rules (they also cover
`cat`, `head`, and `sed`). The push triggers an ask prompt. Open `settings.json` and show
the three lists. Note that `deny` rules apply even before a teammate trusts the folder.

## Adopt this on Monday

1. Copy `CLAUDE.md` into one real repo and cut it to what the team actually disagrees on.
2. Add the Stop hook and the `Read` deny rules to that repo's `.claude/settings.json`.
3. Pick one skill (`commit-pr`) and require it for a week; drop the PR template in.
4. Route reviews through `pr-reviewer` or the GitHub Action on one project, compare to manual.
5. Revisit CLAUDE.md after two weeks: delete anything nobody cited in a review.
