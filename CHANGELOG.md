# Changelog

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
