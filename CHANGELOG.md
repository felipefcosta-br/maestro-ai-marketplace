# Changelog

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
