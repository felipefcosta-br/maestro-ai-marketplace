#!/usr/bin/env python3
"""SessionStart: resumes (after a clear) or offers to resume a saved context.

After `/clear` (source "clear") the session continues the context the user just
saved, without asking: the user chose "Save context and clear". The context is
found by, in order:
  1. the marker `~/.maestro-ai/pending-resume.json` written by `save-context`
     (name + full path, fresh for MAESTRO_AI_FRESH_MIN minutes, default 15);
  2. the newest context file modified in the last MAESTRO_AI_FRESH_MIN minutes in
     the working folder (`.maestro-ai/`, also one folder down), `~/.maestro-ai/`
     or the common folder (`~/Documents/maestro-ai/`, also its subject folders).
The marker is consumed (deleted) when used, so it runs once.

On a fresh start (source "startup") or when nothing fresh exists, it only offers
the latest contexts (at most one per subject, up to three), as before. Common
folder contexts are offered only when recent (MAESTRO_AI_RECENT_DAYS, default 7).

Costs no tokens when there is nothing to offer. Does not fire when a conversation
is resumed or compacted.
"""
import glob
import json
import os
import sys
import time


def integer(name, default):
    try:
        value = int(os.environ.get(name, default))
        return value if value > 0 else default
    except ValueError:
        return default


try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
if not isinstance(data, dict):
    data = {}

source = str(data.get("source") or "startup")
if source not in ("startup", "clear"):
    sys.exit(0)

recent_days = integer("MAESTRO_AI_RECENT_DAYS", 7)
fresh_seconds = integer("MAESTRO_AI_FRESH_MIN", 15) * 60

now = time.time()
home = os.path.expanduser("~")
cwd = str(data.get("cwd") or os.getcwd())
base = os.path.join(home, "Documents", "maestro-ai")
marker_path = os.path.join(home, ".maestro-ai", "pending-resume.json")


def name_of(path):
    return os.path.basename(path)[len("context-"):-len(".md")]


def context_files():
    patterns = [
        os.path.join(cwd, ".maestro-ai", "context-*.md"),
        os.path.join(cwd, "*", ".maestro-ai", "context-*.md"),
        os.path.join(home, ".maestro-ai", "context-*.md"),
        os.path.join(base, "context-*.md"),
        os.path.join(base, "*", "context-*.md"),
    ]
    found = []
    for pattern in patterns:
        found.extend(glob.glob(pattern))
    return [f for f in dict.fromkeys(found) if os.path.isfile(f)]


def read_marker():
    """Returns (name, path) of a fresh marker, or None. Removes stale markers."""
    if not os.path.isfile(marker_path):
        return None
    try:
        age = now - os.path.getmtime(marker_path)
        with open(marker_path, encoding="utf-8") as f:
            marker = json.load(f)
    except (OSError, ValueError):
        return None
    if age > fresh_seconds:
        if age > 86400:
            try:
                os.remove(marker_path)
            except OSError:
                pass
        return None
    if not isinstance(marker, dict):
        return None
    path = os.path.expanduser(str(marker.get("path") or ""))
    name = str(marker.get("name") or "")
    if path and os.path.isfile(path):
        return (name or name_of(path), path)
    return None


def consume_marker():
    try:
        os.remove(marker_path)
    except OSError:
        pass


def emit(text):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}))
    sys.exit(0)


files = context_files()

if source == "clear":
    target = read_marker()
    if target is None:
        fresh = [f for f in files if now - os.path.getmtime(f) <= fresh_seconds]
        if fresh:
            newest = max(fresh, key=os.path.getmtime)
            target = (name_of(newest), newest)
    if target is not None:
        consume_marker()
        name, path = target
        emit(
            "maestro-ai notice: this session was just cleared on purpose after the user chose 'Save context and "
            "clear', so the work continues from the saved context `%s` (file: %s). Continue it now, in your next "
            "reply, without asking for confirmation and without asking what is being worked on: follow "
            "/maestro-ai:resume for that file (use that exact path, do not search or list other contexts). Skip this "
            "if the user's message already is /maestro-ai:resume. Resume's own checks still apply: only ask before "
            "editing if the files or Git state diverge from the context." % (name, path)
        )

# Offer only: fresh start, or nothing fresh to resume.
common = [f for f in files if not (f.startswith(base + os.sep) and now - os.path.getmtime(f) > recent_days * 86400)]
if not common:
    sys.exit(0)

common.sort(key=os.path.getmtime, reverse=True)
seen_names = set()
seen_folders = set()
items = []
for f in common:
    name = name_of(f)
    folder = os.path.dirname(f)
    is_subject = os.path.dirname(folder) == base
    if name in seen_names or (is_subject and folder in seen_folders):
        continue
    seen_names.add(name)
    if is_subject:
        seen_folders.add(folder)
    days = int((now - os.path.getmtime(f)) // 86400)
    items.append("%s (%s)" % (name, "today" if days <= 0 else "%dd ago" % days))
    if len(items) == 3:
        break

emit(
    "maestro-ai notice: saved contexts found: %s. In your first reply, mention it in one "
    "line and offer `/maestro-ai:resume %s`. Do not read any context file unless the user agrees."
    % (", ".join(items), items[0].split(" ")[0])
)
