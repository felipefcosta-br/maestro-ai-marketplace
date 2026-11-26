---
description: Shows or changes when the main session uses the maestro-ai agents (complex, always, ask, manual)
argument-hint: [complex|always|ask|manual|reset]
---
Show or change when the main session uses the maestro-ai agents. The four modes:

- `complex`: use the agents only for complex tasks (the default).
- `always`: use them for every development task.
- `ask`: in a new conversation, ask once with buttons whether to use them.
- `manual`: do not use them unless the user asks.

Argument: $ARGUMENTS

Steps:

1. If the argument is `complex`, `always`, `ask` or `manual`, run `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/maestro-ai-mode.py" --set <mode>`. If it is `reset`, run `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/maestro-ai-mode.py" --reset`. Report the result in one line.
2. If there is no argument, run `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/maestro-ai-mode.py" --show`, tell the user the current override and the mode at the last session start in one or two lines, then ask with the AskUserQuestion tool (one question, one option per mode, with the one-line meanings above). Run `--set` with the chosen mode. If the user types `reset` as their own answer, run `--reset`.
3. If the argument is anything else, list the valid modes and stop.
4. The new mode is stored as an override of the plugin option (`maestro_mode`, editable in `/config`) and is read at the start of each new session. For this conversation, follow the new mode from now on.
