# Changelog

## [0.6.0] - 2026-11-19
### Changed
- **The `maestro-ai-clear` mod is now part of `maestro-ai`.** One plugin, one install, one version: the "Save context and clear" band, the `clear_conversation` tool and the automatic `/maestro-ai:resume` after the clear ship inside `maestro-ai` (`hooks/register.tsx`, `types/`). The tool is now `mcp__maestro-ai__clear_conversation`.
- New option `saveAndClear` (default on) in the plugin's configuration. Turn it off to keep only the hooks, agents and commands; the mod then registers nothing.
- **Migration:** uninstall the separate plugin (`claude plugin uninstall maestro-ai-clear@maestro-ai-marketplace`), then update `maestro-ai`. Keeping both would show the band twice. `maestro-ai-clear` 0.1.0 is removed from the marketplace.
- The mod's code runs only where the host loads hooks modules (Claude Code). Elsewhere (chat, claude.ai) the plugin's skills and commands work as before.

## [0.5.1] - 2026-11-19
### Changed
- Saved contexts keep the user's intent. New section `Intent and success criteria (user's words)`: short verbatim quotes of what the user asked for and why, plus a `Done when` line. `/maestro-ai:save-context` re-reads the user's requests across the whole conversation (not only the last task), copies the section unchanged when updating, and checks that Goal, Decisions and Next steps still lead to `Done when`.
- `/maestro-ai:resume` quotes that intent in its opening summary, warns if the next step would not reach `Done when` or contradicts a quote, and asks the user to confirm the goal when an older context has no such section.
- The rule against pasting code into a context now gives way to an explicit request from the user. Size guide raised to ~80 lines.

## [0.5.0] - 2026-11-19
### Changed
- **Save and clear now continues by itself.** After `/clear`, the start-of-session hook resumes the context the user just saved, without asking, instead of only offering it. `/maestro-ai:resume` has an automatic mode (step 0) that uses the file the hook names and skips the search; its own checks still apply, and it asks before editing only when files or Git state diverge.
- `/maestro-ai:save-context` writes a marker, `~/.maestro-ai/pending-resume.json` (name and full path), after saving. The hook uses it to find the context from any working folder. It is deleted when used and ignored after 15 minutes (`MAESTRO_AI_FRESH_MIN`).
- Without a marker, after a clear the hook falls back to the newest context saved in the last 15 minutes, searched in the working folder, one folder down, `~/.maestro-ai/` and the common folder. This fixes the case where the context was saved in a repository folder and the new session opened in its parent, so nothing was found.
- `/maestro-ai:save-context` never pastes the source of a tool, mod or script into a context; it lists the file path instead, so the context stays short and cheap to resume.
### Added
- `maestro-ai-clear` 0.1.0 (optional companion mod, in this repository): button "Save context and clear" and the `clear_conversation` tool, now with automatic `/maestro-ai:resume <name>` after the clear. It confirms the save by looking at every assistant message of the turn, not only the last one.

## [0.4.11] - 2026-11-15
### Changed
- After saving the context, the long-conversation warning tells Claude to call a `clear_conversation` tool when one is available (provided by an optional companion mod), so the conversation is cleared with no extra step; without it, the user types `/clear` as before.

## [0.4.10] - 2026-11-15
### Changed
- The long-conversation warning no longer fires only once per session: after the first warning at `MAESTRO_AI_LIMIT_KB` (default 600 KB) it fires again each time the transcript grows by another `MAESTRO_AI_LIMIT_KB`, so choosing "Not now" does not silence a very long session for good.

## [0.4.9] - 2026-11-15
### Changed
- The long-conversation warning asks once with buttons (AskUserQuestion: Save context and clear / Not now) instead of a text suggestion. On accept it saves the context; the user then types `/clear`, which a plugin cannot run. Falls back to a text suggestion when the tool is not available.

## [0.4.8] - 2026-11-15
### Changed
- Long-conversation warning now suggests `/maestro-ai:save-context <name>` followed by `/clear` in the same session (the start-of-session hook then offers `/maestro-ai:resume`), instead of opening a new conversation.

## [0.4.7] - 2026-10-21
### Changed
- Single destination: `/maestro-ai:save-context` always writes to the common folder (`~/Documents/maestro-ai/<subject>/`), whatever the working folder is, so `resume` finds it from any session. A project's `.maestro-ai/` is only the fallback when access to the common folder is refused, and it is still read for older contexts.
- `/maestro-ai:resume` offers to move a context found in a project's `.maestro-ai/` to the common folder (only after the user agrees) and corrects a stale `Path:` line.

## [0.4.6] - 2026-10-21
### Changed
- `/maestro-ai:save-context` keeps `.maestro-ai/` out of Git by writing `.maestro-ai/.gitignore` (a single `*`) inside the folder, without asking and without touching the project's `.gitignore` or any global Git setting. It no longer asks about `.gitignore`.
- An old `.maestro-ai/context.md` that the new file replaces is renamed to `context.md.bak` instead of being deleted or asked about.

## [0.4.5] - 2026-10-21
### Added
- Common folder organized by subject: `~/Documents/maestro-ai/<subject>/context-<name>.md` (subject = the `Project:` value). Several contexts of one subject share a folder.
- `/maestro-ai:save-context` copies the working files the next step needs to `<subject>/files/` when the common folder is accessible and the files are small and not sensitive (never overwriting; it lists them otherwise, and records how to recreate regenerable ones).
### Changed
- `/maestro-ai:resume` also searches the subject folders (one level down) and lists contexts grouped by subject.
- `session-start.py` looks in the subject folders too and offers at most the latest context of each subject.

## [0.4.4] - 2026-10-21
### Added
- Context file sections `Verified vs assumed` (each claim marked verified, with how it was checked, or assumed) and `Files to keep` (files the next step needs that would not survive in a session folder).
### Changed
- `/maestro-ai:resume` treats the context as notes, not facts: it checks that the listed files exist and asks for the missing ones up front, tests the assumptions that block the next step, asks when a pasted result contradicts the context or looks incomplete, and separates what it confirmed now from what it inherited.

## [0.4.3] - 2026-10-20
### Changed
- `/maestro-ai:save-context` and `/maestro-ai:resume` ask the user to grant access to `~/Documents/maestro-ai` when the session cannot reach it, then retry; they fall back to the session folder and a downloadable file only if access is refused.
- `/maestro-ai:save-context` closing line is always a single non-empty code block with the resume command.

## [0.4.2] - 2026-10-20
### Added
- Common folder `~/Documents/maestro-ai/`: `/maestro-ai:save-context` uses it when the working folder is a session folder (for example a Desktop agent-mode session), so a new session can find the context by name.
- `Project:` and `Path:` lines in the context file. A later `save-context` with the same name updates the file at its `Path:`, so there is never a second copy.
- The `session-start.py` hook also looks in the common folder (only contexts from the last 7 days, `MAESTRO_AI_RECENT_DAYS`).
### Changed
- `/maestro-ai:resume` searches `.maestro-ai/`, then the common folder, and works on the file where it is. It no longer offers to copy it.

## [0.4.2] - 2026-10-20
### Fixed
- Desktop agent sessions: each session has its own temporary folder (`local-agent-mode-sessions/.../outputs`), so a context saved there was invisible to the next session. `/maestro-ai:save-context` now detects a session folder, gives the file to the user to download and says to keep it; the closing shows the full path.
- `/maestro-ai:resume` now explains why a context was not found (temporary session folder or no file access) and asks the user to attach the file, paste it or give its full path.

## [0.4.1] - 2026-10-20
### Added
- `LICENSE` (MIT) and `license` field in `plugin.json`; README security note says the protection hook is a safety net, not a guarantee.
- `session-start.py` hook: on a fresh session, if the folder has `.maestro-ai/context-*.md`, offers to resume the latest (no cost when there is none).
- `/maestro-ai:resume` falls back to searching `context-*.md` by name in the current folder and `~/Downloads`, asks which to use and offers to copy it into `.maestro-ai/`.
### Changed
- `/maestro-ai:save-context` ends with a single ready-to-paste `/maestro-ai:resume <name>` line.

## [0.4.0] - 2026-10-19
### Changed
- Named contexts: `/maestro-ai:save-context <name>` writes `.maestro-ai/context-<name>.md`, one file per conversation or topic, so contexts never mix. An existing file is updated only when it is the same topic; otherwise the command asks for another name.
- `/maestro-ai:resume <name>` reads that file; without a name it lists the saved contexts and asks which one (or uses the only one). The old `.maestro-ai/context.md` is still accepted.

## [0.3.0] - 2026-10-16
### Added
- Works beyond Claude Code: skills and commands run in Claude Desktop chat, claude.ai and Cowork; subagents and hooks stay Claude Code/Cowork only.
- `/maestro-ai:research` (current sources, checkable answer) and `/maestro-ai:plan` (steps, risks, open questions, no execution).
### Changed
- `/maestro-ai:save-context` and `/maestro-ai:resume` work without a shell or Git (chat): the file is created for download or attached/pasted back; the format covers non-code work too.

## [0.2.1] - 2026-10-16
### Added
- Language rule in the `orchestration` skill: use the recorded language; if the user writes in English, use English; otherwise ask once which language to use. `Language:` line in the `AGENTS.md` template and in `.maestro-ai/context.md`.

## [0.2.0] - 2026-10-16
### Changed (breaking)
- All identifiers renamed to English. Agents: `researcher`, `analyst`, `implementer`, `tester`, `specialist`, `architect`, `reviewer`. Skill: `orchestration`. Commands: `/maestro-ai:implement-test-review`, `/maestro-ai:pre-commit-review`, `/maestro-ai:save-context`, `/maestro-ai:resume`. The old Portuguese command names no longer exist.
- Hook scripts renamed: `confirm-fable.py`, `protection.py`, `context-warning.py`.
- Context file is now `.maestro-ai/context.md`.
- Environment variables renamed to `MAESTRO_AI_LIMIT_KB` and `MAESTRO_AI_LIMIT_MSGS`.
- Agent output modes are now `summary` and `didactic`.
### Added
- Prompts, skill and docs translated to English; bilingual READMEs (en + pt-BR).
- `author` metadata in `plugin.json` and `marketplace.json`.

## [0.1.1] - 2026-10-15
### Added
- `marketplace.json` so the plugin can be installed from a Git repository.
- Repository tooling: `.gitignore`, tests, CI and README.
### Changed
- Plugin renamed from `maestro` to `maestro-ai`.

## [0.1.0] - 2026-10-15
### Added
- Initial agents, orchestration skill, workflow commands, security hooks and templates.
