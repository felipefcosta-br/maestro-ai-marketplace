---
description: Fixed workflow - implement a task, test it and review it, delegating to each maestro-ai agent
argument-hint: <task description>
---
Run the fixed workflow **implement → test → review** for the task below, following the `orchestration` skill (briefings from `templates/briefing.md`). Settle the working language first (section 0 of the skill).

Task: $ARGUMENTS

Steps (in order, no skipping):

1. **Understand.** If the task is broad or involves more than 3 files, delegate the mapping to the `researcher` (`summary` mode). If it is small, read the files yourself. If the description is ambiguous, ask the user before continuing.
2. **Short plan.** List in a few lines what will change and the definition of done. If the task is complex or risky, use the `specialist` instead of the `implementer`.
3. **Implement.** Delegate to the `implementer` (or `specialist`) with a complete briefing: goal, files, constraints, definition of done and the test command from AGENTS.md. `summary` mode.
4. **Test.** Delegate to the `tester`: create or update tests for the change and run the relevant ones. If they fail, send the failure back to the implementer. After **two failures in a row**, stop and ask the user whether to move up to the `specialist` (and then, if needed, the `architect`, with the mandatory Fable/Opus question and your recommendation).
5. **Review.** Delegate to the `reviewer` with the original goal and `git diff` as the diff source. Fix critical and important items (go back to step 3 for them) and repeat the review once.
6. **Close.** Report to the user in at most 10 lines: what changed, files touched, test results, the reviewer's verdict and pending items. Do not commit or push unless explicitly asked.

Rules: agents that edit files run in series; never put secrets in briefings; check each agent's result against the definition of done before moving on.
