---
description: Saves an implementation context summary to .maestro-ai/context.md so work can continue in a new session without rereading the conversation
argument-hint: [optional note, e.g. what to prioritize when resuming]
---
Create (or update) the context file `.maestro-ai/context.md` at the repository root, so the implementation can continue in a new session without rereading this conversation. User note: $ARGUMENTS

Steps:

1. **Check the real state** instead of relying only on the conversation: run `git status --short`, `git branch --show-current` and `git log --oneline -5`, and `git diff --stat` if there are changes.
2. **Write the file** in the working language defined in the `orchestration` skill (section 0) (create the `.maestro-ai/` folder if needed; if the file already exists, update it instead of duplicating). Use exactly this structure, at most ~60 lines:

```
# Implementation context

Updated at: <date and time>
Language: <working language agreed with the user>
Branch: <branch> | Last commit: <short hash and message> | Uncommitted changes: <yes/no, summary>

## Goal
<1-3 lines: what is being built and why>

## Current state
<what is done and working; what is in progress>

## Decisions made
- <decision> — <reason in one line>

## Next steps (in order)
1. <concrete step>
2. ...

## Key files
- <path> — <role / what changed>

## How to validate
- <test command and what to expect>

## Pitfalls and points of attention
- <what already went wrong, what to avoid, dependencies between changes>

## Agents and escalation
- <agents already used, relevant failures, whether the architect/specialist was called and the Fable/Opus decision>

## Open questions
- <decisions that depend on the user>
```

Rules:
- **Never include secrets**, credentials, tokens or customer data.
- Be dense and specific: paths, commands and decisions, without narrating the conversation.
- Record only what matters to continue; do not copy large code excerpts.
- Mark as "not verified" anything that could not be checked in the repository.

3. **Close** with at most 5 lines: the file path, a summary of the state, and the suggestion to continue in a clean session (`/clear` or a new session) with `/maestro-ai:resume`. If `.maestro-ai/` is not in `.gitignore`, warn and ask whether it should be added; do not change `.gitignore` without confirmation.
