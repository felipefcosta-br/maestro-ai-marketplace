#!/usr/bin/env python3
"""PreToolUse: blocks access to secrets and destructive commands."""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if not isinstance(data, dict):
    sys.exit(0)

tool = data.get("tool_name", "")
ti = data.get("tool_input") or {}


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


# Sensitive files (.env.example and similar are allowed)
SENSITIVE_PATH = re.compile(
    r"(^|/)(\.env(\.(?!example|sample|template)[\w.-]+)?"
    r"|id_(rsa|dsa|ecdsa|ed25519)"
    r"|credentials(\.\w+)?"
    r"|secrets?\.(json|ya?ml|properties|toml)"
    r"|[\w.-]+\.(pem|key|p12|pfx|jks|keystore)"
    r"|\.netrc|\.pgpass"
    r"|\.aws/(credentials|config)"
    r"|\.ssh/[^/]+)$",
    re.IGNORECASE,
)

# Destructive commands
DESTRUCTIVE = [
    (r"\brm\s+(-[a-zA-Z]*\s+)*-[a-zA-Z]*[rR][a-zA-Z]*[fF]|\brm\s+(-[a-zA-Z]*\s+)*-[a-zA-Z]*[fF][a-zA-Z]*[rR]|\brm\s+.*--recursive.*--force|\brm\s+.*--force.*--recursive",
     "rm -rf is blocked"),
    (r"\bgit\s+push\b.*(--force\b|--force-with-lease\b|\s-f\b)", "git push --force is blocked"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard is blocked"),
    (r"\bgit\s+clean\b.*-[a-zA-Z]*[fdx]", "destructive git clean is blocked"),
    (r"\bdrop\s+(database|table|schema)\b", "DROP on a database is blocked"),
    (r"\bmkfs(\.\w+)?\b|\bdd\s+if=", "destructive disk command is blocked"),
    (r"\bchmod\s+-R\s+777\b", "chmod -R 777 is blocked"),
    (r"(curl|wget)\b[^|]*\|\s*(sudo\s+)?(ba)?sh\b", "download-and-run (curl | sh) is blocked"),
]

if tool in ("Read", "Edit", "Write", "NotebookEdit", "Grep", "Glob"):
    for key in ("file_path", "path", "notebook_path"):
        p = ti.get(key)
        if isinstance(p, str) and SENSITIVE_PATH.search(p.replace("\\", "/")):
            deny("Access to a secrets file is blocked: " + p)

elif tool == "Bash":
    cmd = ti.get("command") or ""
    for pattern, reason in DESTRUCTIVE:
        if re.search(pattern, cmd, re.IGNORECASE):
            deny("Command blocked by maestro-ai: " + reason)
    # reading secrets through the shell
    for token in re.split(r"[\s;|&<>()]+", cmd):
        token = token.strip("'\"")
        if token and SENSITIVE_PATH.search(token.replace("\\", "/")):
            deny("Access to a secrets file through the shell is blocked: " + token)

sys.exit(0)
