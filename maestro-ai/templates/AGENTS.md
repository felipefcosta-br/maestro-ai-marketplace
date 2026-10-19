# AGENTS.md

> Short template. Fill in the "Project" section in each repository and delete what does not apply.
> Keep this file lean: long details go in `docs/`, and the orchestration rules live in the `orchestration` skill of the maestro-ai plugin.

## Project
- **Language:** English (language for replies, briefings and saved context; change to e.g. Portuguese if preferred)
- **Language/stack:** Kotlin (adjust per project)
- **Build tool:** Gradle (`./gradlew`)
- **Hosting/CI:** GitHub (Actions)
- **Test command (full suite):** `./gradlew test`
- **Test a single class/method:** `./gradlew test --tests "package.ClassName"`
- **Lint/format:** `./gradlew ktlintCheck` (or `detekt`; adjust to the project)
- **Build:** `./gradlew build`

> Other languages: replace the commands above (e.g. `npm test`, `pytest`, `mvn test`, `cargo test`).

## Conventions
- (Fill in: naming, folder structure, commit style, PR rules)

## Known pitfalls
- (Fill in: generated modules that must not be edited, required flags, slow tests, etc.)

## On-demand documentation
- Architecture: `docs/architecture.md` (read when touching core modules)
- Decisions: `docs/decisions/` (read before proposing design changes)

## Orchestration (summary)
- Simple questions and small tasks (1-2 files): handle directly, without delegating.
- Broad tasks, more than 3 files or a lot of noise: delegate to the maestro-ai agents, following the `orchestration` skill (who does what, briefing, escalation, review).
- **Architect:** before calling it, ask the user whether they want Fable or Opus, always including your recommendation.
- Fixed workflows: `/maestro-ai:implement-test-review` and `/maestro-ai:pre-commit-review`.
- Long conversation: `/maestro-ai:save-context <name>` writes `.maestro-ai/context-<name>.md` (one per conversation) and `/maestro-ai:resume <name>` continues in a clean session. Keep `.maestro-ai/` out of Git.

## Security
- Never put credentials, tokens, keys, customer data or confidential information in this file, in briefings or in logs.
- Do not read `.env`, key files or secrets (the plugin also blocks this with a hook).
- Only the `researcher` uses the web. Agents that write files do not use the network or install packages.
- Ask for confirmation before: installing packages, commands that use the network, `git commit` and `git push`.
- Forbidden: `rm -rf` and destructive commands without an explicit request.
