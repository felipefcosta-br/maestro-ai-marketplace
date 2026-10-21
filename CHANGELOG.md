# Changelog

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
