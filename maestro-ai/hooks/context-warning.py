#!/usr/bin/env python3
"""UserPromptSubmit: warns when the conversation has become long, and keeps reminding.

The hook counts the user's prompts in each session and, when it can read the transcript
(`transcript_path`), also measures its size. It warns when either limit is reached:
  - the transcript is at least MAESTRO_AI_LIMIT_KB (default 1500), or
  - the session has MAESTRO_AI_LIMIT_MSGS prompts (default 40).

After a warning it reminds again, even if the user answered "Not now", when either:
  - MAESTRO_AI_REMIND_MSGS more prompts have passed (default 30), or
  - the transcript has grown by another MAESTRO_AI_LIMIT_KB since the last warning.

The state key is the `session_id`; without it, the working directory is used (the state is
then shared between sessions of the same project, which is imprecise but stable).
"""
import hashlib
import json
import os
import sys
import tempfile


def integer(name, default):
    try:
        value = int(os.environ.get(name, default))
        return value if value > 0 else default
    except ValueError:
        return default


LIMIT_KB = integer("MAESTRO_AI_LIMIT_KB", 1500)
LIMIT_MSGS = integer("MAESTRO_AI_LIMIT_MSGS", 40)
REMIND_MSGS = integer("MAESTRO_AI_REMIND_MSGS", 30)

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
if not isinstance(data, dict):
    data = {}

tmp = tempfile.gettempdir()
session = "".join(c for c in str(data.get("session_id") or "") if c.isalnum() or c in "-_")
if session:
    key = session
else:
    cwd = str(data.get("cwd") or os.getcwd())
    key = "cwd" + hashlib.md5(cwd.encode("utf-8")).hexdigest()[:12]


def warn(detail):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "maestro-ai notice: the conversation is already long (%s), which raises the cost of every "
                "new reply. At the end of your current reply, ask the user once with the AskUserQuestion tool "
                "(one question, options: 'Save context and clear', 'Not now'); if that tool is not available, "
                "suggest it in one or two lines instead. If the user chooses 'Save context and clear', run the "
                "/maestro-ai:save-context command with a name you propose (use the Skill tool). Then, if a tool named "
                "clear_conversation is available (it may appear as mcp__<plugin>__clear_conversation), call it so the "
                "conversation is cleared when your reply ends; otherwise tell the user to type /clear, since you "
                "cannot run it for them. After the clear the session resumes the saved context by itself (the "
                "start-of-session hook finds it); if the user typed /clear, any first message continues it, or "
                "/maestro-ai:resume <name> does. If /clear is not available, a new conversation works too. "
                "This notice is new: ask once for it, even if you asked before in this session and the user said "
                "'Not now'. Do not interrupt the work in progress." % detail
            ),
        }
    }))


def read_state(path):
    try:
        with open(path) as f:
            state = json.load(f)
        if isinstance(state, dict):
            return {
                "n": int(state.get("n", 0)),
                "warned_n": int(state.get("warned_n", 0)),
                "warned_kb": float(state.get("warned_kb", 0)),
            }
    except (OSError, ValueError, TypeError):
        pass
    return {"n": 0, "warned_n": 0, "warned_kb": 0.0}


state_file = os.path.join(tmp, "maestro-ai-state-" + key)
state = read_state(state_file)
state["n"] += 1

size_kb = None
transcript = data.get("transcript_path")
if isinstance(transcript, str) and os.path.isfile(transcript):
    try:
        size_kb = os.path.getsize(transcript) / 1024
    except OSError:
        size_kb = None

if state["warned_n"] == 0:
    due = state["n"] >= LIMIT_MSGS or (size_kb is not None and size_kb >= LIMIT_KB)
else:
    due = (
        state["n"] - state["warned_n"] >= REMIND_MSGS
        or (size_kb is not None and size_kb - state["warned_kb"] >= LIMIT_KB)
    )

if due:
    state["warned_n"] = state["n"]
    state["warned_kb"] = size_kb if size_kb is not None else 0.0

try:
    with open(state_file, "w") as f:
        json.dump(state, f)
except OSError:
    pass

if due:
    detail = "%d message%s" % (state["n"], "" if state["n"] == 1 else "s")
    if size_kb is not None:
        detail += ", transcript of ~%d KB" % int(size_kb)
    warn(detail)

sys.exit(0)
