# maestro-ai

[Português](README.pt-BR.md)

A team of subagents for software development. The main session orchestrates; agents do the work with fixed models and tools.

## Contents

- **agents/**: seven subagents (table below)
- **skills/orchestration/**: rules for when to delegate, briefing, escalation, review (loaded on demand)
- **commands/**: `/maestro-ai:implement-test-review`, `/maestro-ai:pre-commit-review`, `/maestro-ai:save-context`, `/maestro-ai:resume`
- **hooks/**: secrets and destructive-command protection, Fable confirmation, long-conversation warning
- **templates/**: `AGENTS.md`, `settings.json`, briefing and output formats

## Agents

| Agent | Model | Tools | Role |
|---|---|---|---|
| researcher | haiku | read, web | Find information, read docs |
| analyst | sonnet | read, bash | Investigate code and logs (read-only) |
| implementer | sonnet | read, edit, bash | Implement well-defined changes |
| tester | sonnet | read, edit, bash | Write and run tests |
| specialist | opus | read, edit, bash | Complex or delicate tasks |
| architect | opus (fable on request) | read, bash | Design and trade-offs; the user is always asked Fable vs Opus, with a recommendation |
| reviewer | sonnet | read, bash | Review complex or implemented code (read-only) |

Agents write reports in the language of the briefing, in `summary` or `didactic` mode.

## Install

```
claude plugin marketplace add felipefcosta-br/maestro-ai-marketplace
claude plugin install maestro-ai@maestro-ai-marketplace
```

From the marketplace (see the root README), or per project by copying `agents/`, `skills/` and `commands/` into `.claude/`.

## Permissions

`templates/settings.json` is a strict starting point (allow read-only commands, ask for edits, commits, network, deny secrets and destructive commands). For corporate use, put it in the repository's `.claude/settings.json`.

## Per-project AGENTS.md

Copy `templates/AGENTS.md` into each repository and fill in the "Project" section (test command, conventions, pitfalls).

## Language

If the user writes in English, everything is in English. If they write in another language and none is recorded, the main session asks once which language to use, then records it (`Language:` in `AGENTS.md` / `.maestro-ai/context.md`).

## Long conversations

- `/maestro-ai:save-context` writes a summary to `.maestro-ai/context.md` (keep it out of Git).
- `/maestro-ai:resume` continues from it in a clean session.
- A hook warns when the conversation gets long: by transcript size if available (`MAESTRO_AI_LIMIT_KB`, default 600), otherwise every N messages (`MAESTRO_AI_LIMIT_MSGS`, default 30).

## Validate

```
claude plugin validate .
python3 -m unittest discover -s tests -v
```
