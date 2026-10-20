#!/usr/bin/env python3
"""SessionStart: offers to resume the latest saved context.

Looks in the working folder (.maestro-ai/) and in the common folder
(~/Documents/maestro-ai/). Contexts in the common folder are offered only when
recent, so old ones from other projects do not add noise.
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

try:
    recent_days = int(os.environ.get("MAESTRO_AI_RECENT_DAYS", "7"))
except ValueError:
    recent_days = 7

now = time.time()
cwd = str(data.get("cwd") or os.getcwd())
local = glob.glob(os.path.join(cwd, ".maestro-ai", "context-*.md"))
common = glob.glob(os.path.join(os.path.expanduser("~"), "Documents", "maestro-ai", "context-*.md"))
common = [f for f in common if now - os.path.getmtime(f) <= recent_days * 86400]

files = [f for f in local + common if os.path.isfile(f)]
if not files:
    sys.exit(0)

files.sort(key=os.path.getmtime, reverse=True)
seen = set()
items = []
for f in files:
    name = os.path.basename(f)[len("context-"):-len(".md")]
    if name in seen:
        continue
    seen.add(name)
    days = int((now - os.path.getmtime(f)) // 86400)
    items.append("%s (%s)" % (name, "today" if days <= 0 else "%dd ago" % days))
    if len(items) == 3:
        break

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": (
            "maestro-ai notice: saved contexts found: %s. In your first reply, mention it in one "
            "line and offer `/maestro-ai:resume %s`. Do not read any context file unless the user agrees."
            % (", ".join(items), items[0].split(" ")[0])
        ),
    }
}))
sys.exit(0)
