#!/usr/bin/env python3
"""SessionStart: tells the main session when to use the maestro-ai agents.

The mode comes from, in this order:
  1. the override file ~/.maestro-ai/preferences.json (written by /maestro-ai:mode),
  2. the plugin option `maestro_mode` (asked when the plugin is enabled, editable in /config;
     Claude Code exports it to hooks as CLAUDE_PLUGIN_OPTION_MAESTRO_MODE),
  3. the default, "complex".

Modes:
  complex  use the agents only for complex tasks (default)
  always   use the agents for every development task
  ask      on a new session, ask once with buttons whether to use them
  manual   do not use them unless the user asks

Command line (used by /maestro-ai:mode):
  maestro-ai-mode.py --show | --set <mode> | --reset
"""
import json
import os
import sys
import tempfile
import time

MODES = ("complex", "always", "ask", "manual")
DEFAULT = "complex"
ENV_NAME = "CLAUDE_PLUGIN_OPTION_MAESTRO_MODE"
FOLDER = os.path.join(os.path.expanduser("~"), ".maestro-ai")
PREFS = os.path.join(FOLDER, "preferences.json")
LAST = os.path.join(FOLDER, "mode-last.json")

TEXT = {
    "complex": (
        "maestro-ai mode: complex. Use the maestro-ai orchestration skill and delegate to the maestro-ai "
        "agents only for complex tasks (changes across more than two files, research that needs sources, "
        "or review of non-trivial code). For simple questions and small edits, work directly without delegating."
    ),
    "always": (
        "maestro-ai mode: always. Use the maestro-ai orchestration skill and its agents for every "
        "development task, following its delegation rules."
    ),
    "ask": (
        "maestro-ai mode: ask. Once the user's first task in this conversation is clear and is not trivial, "
        "ask once with the AskUserQuestion tool (one question, options: 'Use maestro-ai', 'Work directly') "
        "whether to use the maestro-ai orchestration skill and agents here, then follow the answer until the "
        "user says otherwise. For simple questions and small edits, skip the question and work directly."
    ),
    "manual": (
        "maestro-ai mode: manual. Do not use the maestro-ai orchestration skill or delegate to the maestro-ai "
        "agents unless the user asks (a /maestro-ai: command, or words like 'use maestro-ai')."
    ),
}


def read_json(path):
    try:
        if os.path.islink(path) or not os.path.isfile(path) or os.path.getsize(path) > 4096:
            return None
        with open(path) as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def write_json(path, data):
    os.makedirs(FOLDER, mode=0o700, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=FOLDER, prefix=".tmp-")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        os.replace(tmp, path)
    except OSError:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def override():
    prefs = read_json(PREFS)
    mode = prefs.get("mode") if prefs else None
    return mode if mode in MODES else None


def effective():
    mode = override()
    if mode:
        return mode, "override"
    value = os.environ.get(ENV_NAME, "").strip().lower()
    if value in MODES:
        return value, "config"
    return DEFAULT, "default"


def notice(mode, event):
    # In "ask" mode the question belongs to a brand-new conversation. After /clear (auto-resume),
    # compact or resume it stays silent: the user already answered, or is mid-task.
    if mode == "ask" and event != "startup":
        return None
    return TEXT[mode]


def cli(args):
    if args[0] == "--show":
        last = read_json(LAST) or {}
        print("override: %s" % (override() or "none"))
        print("mode at last session start: %s (%s)" % (last.get("mode", "unknown"), last.get("source", "unknown")))
        print("valid modes: %s" % ", ".join(MODES))
        return 0
    if args[0] == "--set":
        mode = args[1].strip().lower() if len(args) > 1 else ""
        if mode not in MODES:
            print("invalid mode: use one of %s" % ", ".join(MODES))
            return 2
        try:
            write_json(PREFS, {"mode": mode})
        except OSError as error:
            print("could not save the preference: %s" % error)
            return 1
        print("mode set to %s (override)" % mode)
        return 0
    if args[0] == "--reset":
        try:
            if os.path.exists(PREFS):
                os.remove(PREFS)
        except OSError as error:
            print("could not remove the override: %s" % error)
            return 1
        print("override removed; the plugin option (or the default, %s) applies again" % DEFAULT)
        return 0
    print("usage: maestro-ai-mode.py --show | --set <mode> | --reset")
    return 2


def hook():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    event = str(data.get("source") or "startup")
    mode, source = effective()
    try:
        write_json(LAST, {"mode": mode, "source": source, "at": int(time.time())})
    except OSError:
        pass
    text = notice(mode, event)
    if text:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}))
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].startswith("--"):
        sys.exit(cli(sys.argv[1:]))
    sys.exit(hook())
