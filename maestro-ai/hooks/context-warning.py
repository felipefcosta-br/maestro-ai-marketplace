#!/usr/bin/env python3
"""UserPromptSubmit: warns when the conversation has become long.

Plan A: if the hook receives `transcript_path`, it measures the transcript size and
warns once per session when it passes MAESTRO_AI_LIMIT_KB (default 600).

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
                "new reply. At the end of your current reply, suggest to the user, in one or two lines, "
                "running /maestro-ai:save-context and continuing in a clean session with /maestro-ai:resume. "
                "Suggest it only once and do not interrupt the work in progress." % detail
            ),
        }
    }))


transcript = data.get("transcript_path")

if isinstance(transcript, str) and os.path.isfile(transcript):
    # Plan A: transcript size, one warning per session
    size_kb = os.path.getsize(transcript) / 1024
    if size_kb >= LIMIT_KB:
        marker = os.path.join(tmp, "maestro-ai-warned-" + key)
        if not os.path.exists(marker):
            try:
                open(marker, "w").close()
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
