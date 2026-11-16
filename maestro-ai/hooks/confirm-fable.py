#!/usr/bin/env python3
"""PreToolUse: asks the user to confirm whenever a subagent is called with the Fable model."""
import json
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if not isinstance(data, dict):
    sys.exit(0)

tool_input = data.get("tool_input") or {}
model = str(tool_input.get("model") or "").lower()

if "fable" in model:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                "This call uses the Fable model (more expensive). "
                "Approve to continue; if you deny, the agent should run on Opus."
            ),
        }
    }))
sys.exit(0)
