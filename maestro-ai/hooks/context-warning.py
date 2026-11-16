#!/usr/bin/env python3
"""UserPromptSubmit: warns when the conversation has become long.

Plan A: if the hook receives `transcript_path`, it measures the transcript size and
warns when it passes MAESTRO_AI_LIMIT_KB (default 600), and again each time it grows
by another MAESTRO_AI_LIMIT_KB since the last warning (so declining once does not
silence the session for good).

Plan B: if there is no readable transcript, it counts messages and warns every
MAESTRO_AI_LIMIT_MSGS messages (default 30). The counter key is the `session_id`;
without it, the working directory is used (the counter is then shared between
sessions of the same project, which is imprecise but stable).
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


LIMIT_KB = integer("MAESTRO_AI_LIMIT_KB", 600)
LIMIT_MSGS = integer("MAESTRO_AI_LIMIT_MSGS", 30)

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
                "cannot run it for them. After the clear the session offers /maestro-ai:resume <name>. If /clear is "
                "not available, a new conversation works too. "
                "Ask only once and do not interrupt the work in progress." % detail
            ),
        }
    }))


transcript = data.get("transcript_path")

if isinstance(transcript, str) and os.path.isfile(transcript):
    # Plan A: transcript size, one warning per LIMIT_KB of growth
    size_kb = os.path.getsize(transcript) / 1024
    marker = os.path.join(tmp, "maestro-ai-warned-" + key)
    last = 0
    if os.path.exists(marker):
        try:
            with open(marker) as f:
                last = int(float(f.read().strip() or LIMIT_KB))
        except (OSError, ValueError):
            last = LIMIT_KB
    threshold = LIMIT_KB if last == 0 else last + LIMIT_KB
    if size_kb >= threshold:
        try:
            with open(marker, "w") as f:
                f.write(str(int(size_kb)))
        except OSError:
            pass
        warn("transcript of ~%d KB" % int(size_kb))
else:
    # Plan B: message counter, warn every LIMIT_MSGS messages
    counter_file = os.path.join(tmp, "maestro-ai-counter-" + key)
    try:
        with open(counter_file) as f:
            n = int(f.read().strip() or "0")
    except (OSError, ValueError):
        n = 0
    n += 1
    try:
        with open(counter_file, "w") as f:
            f.write(str(n))
    except OSError:
        pass
    if n % LIMIT_MSGS == 0:
        warn("about %d messages" % n)

sys.exit(0)
