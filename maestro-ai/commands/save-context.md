---
description: Saves a named context summary (code or any other work) to context-<name>.md in .maestro-ai/ or the common folder so work can continue in a new session without rereading the conversation
argument-hint: [name] [optional note, e.g. what to prioritize when resuming]
---
Create (or update) a named context file, `context-<name>.md`, so the work can continue in a new session without rereading this conversation. Each conversation or topic has its own file, so contexts never mix. Arguments: $ARGUMENTS

This works in Claude Code and in chat.

**Where to save (one file per name, in one place only)**
1. If `context-<name>.md` already exists, in `.maestro-ai/` or in `~/Documents/maestro-ai/`, update it where it is (see its `Path:` line). Never create a second copy.
2. Otherwise, if the working folder is lasting (a Git repository, or a folder the user connected or chose), use `.maestro-ai/` in the repository root (or the current folder outside a repository).
3. Otherwise (a session folder: its path contains `local-agent-mode-sessions` or ends in `/outputs`, or you cannot tell), use the common folder `~/Documents/maestro-ai/` (create it if needed). A session folder belongs to this session only, and a new session will not see it.
4. If you have no shell or cannot write there (chat), create `context-<name>.md` with the file tool and give it to the user to download, or, if you cannot create files, show it in one code block.

**Choosing the name**
- If the first word of the arguments is a short slug (lowercase letters, digits and hyphens, at most 30 characters), it is the name and the rest is the user's note. Otherwise, the whole text is the note.
- With no name, propose one from the topic (2-4 words, e.g. `qa-skill`, `login-refactor`) and use it.
- With a shell, list `.maestro-ai/` and `~/Documents/maestro-ai/` first. If `context-<name>.md` already exists, update it only when this conversation is the one that wrote or resumed it (same topic, you can tell from its content). Otherwise do not overwrite: ask the user for a different name.
- Always state the final name in your closing lines, so the user can resume it later.

Steps:

1. **Check the real state** instead of relying only on the conversation. With a shell in a Git repository: run `git status --short`, `git branch --show-current` and `git log --oneline -5`, and `git diff --stat` if there are changes. Without a shell, or outside a repository, skip this and write `Branch: n/a`.
2. **Write the file** in the working language defined in the `orchestration` skill (section 0) (create the `.maestro-ai/` folder if needed; if the file already exists and is the same topic, update it instead of duplicating). Use exactly this structure, at most ~60 lines:

```
# Context: <name>

Name: <name>
Project: <repository or folder name this work belongs to, or n/a>
Path: <full path where this file is saved, or n/a if it was only given for download>
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

3. **Close** with at most 6 lines: the full path of the file (or where to download it), a summary of the state, and, as the last line, only the ready-to-paste command in a code block: `/maestro-ai:resume <name>` (in chat, add "attach the file"). If the file went to the common folder, add one line before the command: "Saved in the common folder, so a new session can find it by name." The user continues in a clean session (`/clear` or a new conversation). In a repository, if `.maestro-ai/` is not in `.gitignore`, warn and ask whether it should be added; do not change `.gitignore` without confirmation.
