---
description: Resumes the implementation from .maestro-ai/context.md, without rereading the previous conversation
argument-hint: [optional focus for this session]
---
Resume the work from the saved context. Optional focus from the user: $ARGUMENTS

Steps:

1. **Read `.maestro-ai/context.md`** and use the working language recorded in its `Language:` line (if it has none and the user is not writing in English, ask once, as in section 0 of the `orchestration` skill). If it does not exist, tell the user and suggest `/maestro-ai:save-context` in the previous session; do not try to rebuild the context by scanning the whole project.
2. **Check that the context is current**: run `git status --short`, `git branch --show-current` and `git log --oneline -5` and compare with the branch, last commit and changes recorded in the file. If something diverges (new commits, a different branch, changed files the context does not mention), list the differences and ask the user how to proceed before editing anything.
3. **Read only what is needed.** Open just the "Key files" related to the next step, and only the relevant parts. Do not reread the whole project or redo work the context marks as done.
4. **Summarize in at most 5 lines**: goal, state, next step and open questions.
5. **Continue** from the first item of "Next steps", following the `orchestration` skill (delegate only when worth it, complete briefings, escalation and review as usual). Respect the recorded decisions and pitfalls; if you need to contradict them, tell the user first.
6. After each relevant step, suggest updating the context with `/maestro-ai:save-context`.

If "Open questions" block the next step, ask the user those first.
