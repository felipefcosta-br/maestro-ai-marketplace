---
description: Resumes work from a named context file (.maestro-ai/context-<name>.md, or one the user attached), without rereading the previous conversation
argument-hint: [name] [optional focus for this session]
---
Resume the work from a saved context. Arguments: $ARGUMENTS (optionally a context name, then a focus for this session)

Steps:

1. **Find the context.** Use the first match:
   - a file the user attached or pasted in chat;
   - with a shell, `.maestro-ai/context-<name>.md` when the first argument is a name that exists (also accept an exact file path);
   - with a shell and no name, list `.maestro-ai/context-*.md` (and the old `.maestro-ai/context.md`): if there is exactly one, use it and say so; if there are several, show each name with its `Updated at` and goal line and ask which one. Do not guess.
   Use the working language recorded in its `Language:` line (if it has none and the user is not writing in English, ask once, as in section 0 of the `orchestration` skill). If there is none, tell the user and suggest `/maestro-ai:save-context <name>` in the previous session; do not try to rebuild the context by scanning the whole project.
2. **Check that the context is current** (only with a shell in a Git repository; otherwise skip): run `git status --short`, `git branch --show-current` and `git log --oneline -5` and compare with the branch, last commit and changes recorded in the file. If something diverges (new commits, a different branch, changed files the context does not mention), list the differences and ask the user how to proceed before editing anything.
3. **Read only what is needed.** Open just the "Key files and sources" related to the next step, and only the relevant parts. Do not reread the whole project or redo work the context marks as done.
4. **Summarize in at most 5 lines**: goal, state, next step and open questions.
5. **Continue** from the first item of "Next steps", following the `orchestration` skill (delegate only when worth it, complete briefings, escalation and review as usual). Respect the recorded decisions and pitfalls; if you need to contradict them, tell the user first.
6. After each relevant step, suggest updating the context with `/maestro-ai:save-context <same name>`.

If "Open questions" block the next step, ask the user those first.
