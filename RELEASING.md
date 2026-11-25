# Releasing

The GitHub repository is the only source of truth. Nothing is edited in an installed copy or in a zip.

## Each release

1. Change the code and the tests. Run `python3 -m unittest discover -s tests` (all OK).
2. Set the same version in `maestro-ai/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` and the top entry of `CHANGELOG.md`.
3. `claude plugin validate .` and `claude plugin validate maestro-ai`.
4. Commit (signed), tag `vX.Y.Z`, push the branch and the tag.

## Where each copy updates

| Where | How it follows GitHub | What you do |
| --- | --- | --- |
| Claude Code in the terminal | marketplace `maestro-ai-marketplace` | auto-update (`/plugin` > Marketplaces), or `claude plugin marketplace update maestro-ai-marketplace` then `claude plugin update maestro-ai@maestro-ai-marketplace` |
| Claude desktop and Cowork | the same marketplace, added under Customize > Plugins of each account | **Check for updates**, then turn on **Sync automatically** |
| Claude Code cloud sessions | the plugin synced to the account that owns the cloud session | in that account: Customize > Plugins > **Check for updates** and **Sync automatically** |

Each Claude account has its own plugin list, so repeat the desktop/Cowork step on every account you use (for example one corporate and one personal). Cloud sessions do not install plugins declared in a repository's `.claude/settings.json`.

## Check it worked

- Terminal and desktop: `claude plugin list` shows `maestro-ai@maestro-ai-marketplace` with the new version.
- Cloud: start a new session and check the plugin version.

## Keeping the repository safe

Whoever can push to `main` changes what every installed copy runs.

- Turn on 2FA or a passkey on the GitHub account.
- Protect `main` (no force pushes, no deletion) and sign commits and tags.
- On a corporate machine, pin the version or turn off marketplace auto-update, and update on purpose after reading the CHANGELOG.
- Put `.maestro-ai/` in the `.gitignore` of every project that uses the plugin.
