#!/usr/bin/env python3
"""SessionStart: when the working folder has saved contexts, offers to resume the latest.

Costs no tokens when there is nothing to offer. Only fires on a fresh session
(startup or clear), not when a conversation is resumed or compacted.
"""
import glob
import json
import os
import sys
import time

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
if not isinstance(data, dict):
    data = {}

if str(data.get("source") or "startup") not in ("startup", "clear"):
    sys.exit(0)

cwd = str(data.get("cwd") or os.getcwd())
files = glob.glob(os.path.join(cwd, ".maestro-ai", "context-*.md"))
files = [f for f in files if os.path.isfile(f)]
if not files:
    sys.exit(0)

files.sort(key=os.path.getmtime, reverse=True)
items = []
for f in files[:3]:
    name = os.path.basename(f)[len("context-"):-len(".md")]
    days = int((time.time() - os.path.getmtime(f)) // 86400)
    items.append("%s (%s)" % (name, "today" if days <= 0 else "%dd ago" % days))

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": (
            "maestro-ai notice: this folder has saved contexts: %s. In your first reply, mention it in one "
            "line and offer `/maestro-ai:resume %s`. Do not read any context file unless the user agrees."
            % (", ".join(items), items[0].split(" ")[0])
        ),
    }
}))
sys.exit(0)
