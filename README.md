# maestro-ai marketplace

[Português](README.pt-BR.md)

A Claude Code marketplace that distributes **maestro-ai**: a team of specialized subagents for software development. The main session orchestrates and delegates to agents with fixed models and tools, to reduce cost and increase quality.

## Install

```
claude plugin marketplace add felipefcosta-br/maestro-ai-marketplace
claude plugin install maestro-ai@maestro-ai-marketplace
```

The repository is public, so no sign-in is needed to install. The plugin is installed per OS user (`~/.claude`), so one install serves every Claude account on the machine.

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

The plugin ships hooks that run local Python scripts (they block secrets and destructive commands, ask before using the Fable model, warn about long conversations, and offer to resume a saved context). Review them in `maestro-ai/hooks/` before using them in a corporate environment. The protection hook matches text patterns: it is a safety net, not a security guarantee, and can be bypassed. Keep your own permission rules and review what the agents do.

- The marker and the context files are data on disk: after a clear, the plugin only resumes a file named `context-<name>.md` inside a `.maestro-ai` folder or the common folder (regular file, not a symlink, under 512 KB), and `/maestro-ai:resume` treats its text as notes, not as instructions.
- `analyst`, `architect` and `reviewer` are read-only by instruction: they have Bash, and nothing technical stops them. Use `templates/settings.json` for real permission rules.
- Supply chain: whoever can push to this repository can change what your machines run. Use 2FA or a passkey on the GitHub account, protect `main`, sign commits, and on a corporate machine pin the version or turn off marketplace auto-update and update on purpose after reading the CHANGELOG.
- Add `.maestro-ai/` to the `.gitignore` of every project: contexts can hold project details.

## Structure

```
.claude-plugin/marketplace.json
maestro-ai/        the plugin (agents, skill, commands, hooks, templates)
tests/             unit tests (also run by CI)
```

See [maestro-ai/README.md](maestro-ai/README.md) for the plugin itself.

## License

[MIT](LICENSE).
