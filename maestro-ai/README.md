# maestro-ai

[Português](README.pt-BR.md)

A team of subagents for software development. The main session orchestrates; agents do the work with fixed models and tools.

## Contents

- **agents/**: seven subagents (table below)
- **skills/orchestration/**: rules for when to delegate, briefing, escalation, review (loaded on demand)
- **commands/**: `/maestro-ai:research`, `/maestro-ai:plan`, `/maestro-ai:save-context`, `/maestro-ai:resume` (everywhere); `/maestro-ai:implement-test-review`, `/maestro-ai:pre-commit-review` (code)
- **hooks/**: secrets and destructive-command protection, Fable confirmation, long-conversation warning
- **templates/**: `AGENTS.md`, `settings.json`, briefing and output formats

## Where it works

| Part | Claude Code | Cowork | Chat (Desktop / claude.ai) |
|---|---|---|---|
| Skills and commands | yes | yes | yes |
| Subagents | yes | yes | no |
| Hooks | yes | yes | no |

In chat, the skill's rules still guide the conversation (briefing, asking before big decisions, self-review), but nothing switches models or blocks commands. Plugins need a paid plan.

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

If the user writes in English, everything is in English. If they write in another language and none is recorded, the main session asks once which language to use, then records it (`Language:` in `AGENTS.md` / the saved context file).

## Long conversations

- `/maestro-ai:save-context <name>` writes a summary to `.maestro-ai/context-<name>.md` (keep it out of Git). Use one name per conversation or topic so contexts never mix; an existing file is only updated when it is the same topic.
- `/maestro-ai:resume <name>` continues from it in a clean session. Without a name it lists the saved contexts and asks which one (or uses the only one).
- Where it is saved: `.maestro-ai/` in a lasting folder (a Git repository or a folder you connected); in a session folder (for example a Desktop agent-mode session) it goes to the common folder `~/Documents/maestro-ai/`, so a new session finds it by name. The file has `Project:` and `Path:` lines, and saving again with the same name updates it in place, so there is never a second copy.
- A hook offers to resume the latest saved context when you open a session in a folder that has one, or when the common folder has one from the last 7 days (`MAESTRO_AI_RECENT_DAYS`); no cost when there is none. If `resume` finds nothing in either folder, it looks for `context-*.md` by name in the current folder and `~/Downloads` and asks which to use. In plain chat without file access, attach the file.
- In Claude Desktop agent mode each session has its own temporary folder, so a context saved there is not visible to the next session. `save-context` detects this, hands you the file and tells you to keep it; in the new conversation attach it (or give its full path) and run `/maestro-ai:resume`.
- A hook warns when the conversation gets long: by transcript size if available (`MAESTRO_AI_LIMIT_KB`, default 600), otherwise every N messages (`MAESTRO_AI_LIMIT_MSGS`, default 30).

## Validate

```
claude plugin validate .
python3 -m unittest discover -s tests -v
```
