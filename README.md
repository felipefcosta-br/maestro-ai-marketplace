# maestro-ai marketplace

[Português](README.pt-BR.md)

A Claude Code marketplace that distributes **maestro-ai**: a team of specialized subagents for software development. The main session orchestrates and delegates to agents with fixed models and tools, to reduce cost and increase quality.

## Install

```
claude plugin marketplace add felipefcosta-br/maestro-ai-marketplace
claude plugin install maestro-ai@maestro-ai-marketplace
```

The repository is private: Git must be authenticated with an account that can read it (with the GitHub CLI: `gh auth switch -u felipefcosta-br`). The plugin is installed per OS user (`~/.claude`), so one install serves every Claude account on the machine.

## Update

```
claude plugin marketplace update maestro-ai-marketplace
claude plugin update maestro-ai@maestro-ai-marketplace
```

Then restart Claude Code.

## Release flow

1. Change the plugin.
2. Bump `version` in both `maestro-ai/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
3. Add an entry to `CHANGELOG.md`.
4. Run `python3 -m unittest discover -s tests -v` and `claude plugin validate .`.
5. Commit, `git tag vX.Y.Z`, `git push --follow-tags`.

## Security note

The plugin ships hooks that run local Python scripts (they block secrets and destructive commands, ask before using the Fable model, and warn about long conversations). Review them in `maestro-ai/hooks/` before using them in a corporate environment.

## Structure

```
.claude-plugin/marketplace.json
maestro-ai/        the plugin (agents, skill, commands, hooks, templates)
tests/             unit tests (also run by CI)
```

See [maestro-ai/README.md](maestro-ai/README.md) for the plugin itself.

## License

To be defined.
