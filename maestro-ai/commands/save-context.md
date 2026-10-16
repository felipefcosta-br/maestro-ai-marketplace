---
description: Saves a context summary (code or any other work) to .maestro-ai/context.md so work can continue in a new session without rereading the conversation
argument-hint: [optional note, e.g. what to prioritize when resuming]
---
Create (or update) the context file `.maestro-ai/context.md`, so the work can continue in a new session without rereading this conversation. User note: $ARGUMENTS

This works in Claude Code and in chat. If you have a shell, save the file in the repository root. If you do not (chat), create the file with the file tool and give it to the user to download, or, if you cannot create files, show it in one code block.

Steps:

1. **Check the real state** instead of relying only on the conversation. With a shell in a Git repository: run `git status --short`, `git branch --show-current` and `git log --oneline -5`, and `git diff --stat` if there are changes. Without a shell, or outside a repository, skip this and write `Branch: n/a`.
2. **Write the file** in the working language defined in the `orchestration` skill (section 0) (create the `.maestro-ai/` folder if needed; if the file already exists, update it instead of duplicating). Use exactly this structure, at most ~60 lines:

```
# Context

Updated at: <date and time>
Language: <working language agreed with the user>
Branch: <branch> | Last commit: <short hash and message> | Uncommitted changes: <yes/no, summary>

## Goal
<1-3 lines: what is being done and why (code, research, plan, analysis...)>

## Current state
<what is done and working; what is in progress>

## Decisions made
- <decision> — <reason in one line>

## Next steps (in order)
1. <concrete step>
2. ...

## Key files and sources
- <path, document or link> — <role / what changed or what it says>

## How to validate
- <test command and expected result; for non-code work, how to check the result>

## Pitfalls and points of attention
- <what already went wrong, what to avoid, dependencies between changes>

## Agents and escalation (code work only; omit otherwise)
- <agents already used, relevant failures, whether the architect/specialist was called and the Fable/Opus decision>

## Open questions
- <decisions that depend on the user>
```

Rules:
- **Never include secrets**, credentials, tokens or customer data.
- Be dense and specific: paths, commands and decisions, without narrating the conversation.
- Record only what matters to continue; do not copy large code excerpts.
- Mark as "not verified" anything that could not be checked in the repository.

3. **Close** with at most 5 lines: the file path (or where to download it), a summary of the state, and the suggestion to continue in a clean session (`/clear` or a new conversation) with `/maestro-ai:resume`, attaching the file in chat. In a repository, if `.maestro-ai/` is not in `.gitignore`, warn and ask whether it should be added; do not change `.gitignore` without confirmation.
