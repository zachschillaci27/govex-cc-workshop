---
name: explain-change
description: Produce a short reviewer brief for the current diff or a branch. Use before asking a teammate to review.
argument-hint: "[branch or empty for working tree]"
---

Write a reviewer brief for $ARGUMENTS (default: the working tree diff against HEAD; for a branch, `git diff main...<branch>`).

Under 200 words, four short sections:

1. Intent: one or two sentences on what the change is for.
2. Look here: the two or three places a human reviewer should actually read, as `file:line`, each with one line on why it matters.
3. Assumptions: what the change takes for granted about data, callers, or environment.
4. Not tested: behavior the diff touches that no test covers.

This is not a line-by-line narration. Skip anything a reviewer can see by reading the diff. If the change is trivial, say so in one line and stop.
