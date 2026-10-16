---
description: Fixed workflow - pre-commit review of the current changes (diff, tests and verdict), without editing code
argument-hint: [optional focus, e.g. security, concurrency]
---
Do the **pre-commit review** of the repository's current changes, following the `orchestration` skill. Optional focus from the user: $ARGUMENTS

Steps:

1. **Check the state.** Run `git status` and `git diff` (including `git diff --staged`) to see what changed. If there are no changes, say so and stop.
2. **Tests.** Delegate to the `tester` the run of the tests relevant to the changed areas (test command from AGENTS.md), in `summary` mode. For small, low-risk changes you may run the command directly.
3. **Review.** Delegate to the `reviewer` with the goal of the changes (inferred from the diff and recent messages, or asked from the user if unclear) and how to get the diff. If the diff is large or complex, tell the user and ask whether they want the `reviewer` on Opus.
4. **Quick security check.** Confirm the diff contains no secrets (keys, tokens, passwords, `.env`), build artifacts or customer data.
5. **Report.** Deliver in at most 15 lines: test results, the reviewer's findings by severity (critical, important, suggestion), risks and a verdict: **ready to commit**, **ready with reservations** or **do not commit yet**.

Rules: this workflow **does not edit code** and **does not commit or push**. If something needs fixing, describe it and ask whether the user wants it applied.
