#!/usr/bin/env python3
"""PreToolUse: blocks access to secrets and destructive commands.

This is a speed bump against mistakes and obvious prompt-injection attempts, not
a security boundary: a shell can always find another way. For real isolation use
the permission rules in `templates/settings.json` and a sandbox.
"""
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
if not isinstance(ti, dict):
    ti = {}


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
    r"|\.netrc|\.pgpass|\.npmrc|\.pypirc|\.git-credentials"
    r"|\.aws/(credentials|config)"
    r"|\.ssh/[^/]+"
    r"|\.kube/config"
    r"|\.docker/config\.json"
    r"|\.config/gh/hosts\.yml"
    r"|\.claude/\.credentials\.json"
    r"|\.claude\.json)$",
    re.IGNORECASE,
)

# Destructive commands (matched on the command with quotes and backslashes removed)
DESTRUCTIVE = [
    (r"\bgit\s+push\b.*(--force\b|--force-with-lease\b|\s-f\b|\s\+[\w./-]+)", "git push --force is blocked"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard is blocked"),
    (r"\bgit\s+clean\b.*-[a-zA-Z]*[fdx]", "destructive git clean is blocked"),
    (r"\bgit\s+checkout\b.*\s--\s+\.(\s|$)|\bgit\s+checkout\s+\.(\s|$)", "git checkout . discards all changes and is blocked"),
    (r"\bgit\s+restore\b.*\s\.(\s|$)", "git restore . discards all changes and is blocked"),
    (r"\bgit\s+branch\b.*\s(?-i:-D)\b", "git branch -D is blocked"),
    (r"\bdrop\s+(database|table|schema)\b", "DROP on a database is blocked"),
    (r"\bmkfs(\.\w+)?\b|\bdd\s+if=", "destructive disk command is blocked"),
    (r"\bchmod\s+(-\w+\s+)*-R\s+777\b|\bchmod\s+-R\s+777\b", "chmod -R 777 is blocked"),
    (r"\bfind\b.*\s-delete\b|\bfind\b.*-exec\s+rm\b", "find ... -delete / -exec rm is blocked"),
    (r"\b(rmtree|shutil\.rmtree)\b", "recursive delete through a script (rmtree) is blocked"),
    # download-and-run
    (r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(env\s+)?(ba|z|da|k)?sh\b", "download-and-run (curl | sh) is blocked"),
    (r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(python[\d.]*|perl|ruby|node)\b", "download-and-run (curl | interpreter) is blocked"),
    (r"\b(ba|z|da|k)?sh\s+<\(\s*(curl|wget)\b|\.\s+<\(\s*(curl|wget)\b|\bsource\s+<\(\s*(curl|wget)\b", "run of a downloaded script is blocked"),
    (r"\beval\b.*\b(curl|wget)\b|\b(curl|wget)\b.*\beval\b", "eval of downloaded content is blocked"),
    # dumping the environment (tokens and keys live there)
    (r"(^|[;&|(]\s*)(sudo\s+)?printenv\b|(^|[;&|(]\s*)(sudo\s+)?env\s*($|[;&|)])|(^|[;&|(]\s*)(sudo\s+)?env\s*\|", "dumping the environment is blocked"),
    (r"/proc/[\w$]+/environ", "reading process environment is blocked"),
]

SHELL_SPLIT = re.compile(r"[;&|\n()`]+")


def rm_is_recursive_force(cmd):
    """True when some `rm` has both a recursive and a force flag, in any spelling."""
    for segment in SHELL_SPLIT.split(cmd):
        words = segment.split()
        for i, word in enumerate(words):
            if word.rsplit("/", 1)[-1] != "rm":
                continue
            recursive = force = False
            for arg in words[i + 1:]:
                if arg == "--":
                    break
                if arg.startswith("--"):
                    recursive = recursive or arg == "--recursive"
                    force = force or arg == "--force"
                elif arg.startswith("-") and len(arg) > 1:
                    recursive = recursive or any(c in "rR" for c in arg[1:])
                    force = force or "f" in arg[1:]
            if recursive and force:
                return True
    return False


if tool in ("Read", "Edit", "Write", "NotebookEdit", "Grep", "Glob"):
    for key in ("file_path", "path", "notebook_path"):
        p = ti.get(key)
        if isinstance(p, str) and SENSITIVE_PATH.search(p.replace("\\", "/")):
            deny("Access to a secrets file is blocked: " + p)

elif tool == "Bash":
    raw = ti.get("command") or ""
    if not isinstance(raw, str):
        sys.exit(0)
    # quotes and backslashes are removed so `.e""nv` or `r\m` cannot hide a match
    cmd = raw.replace('"', "").replace("'", "").replace("\\", "")
    if rm_is_recursive_force(cmd):
        deny("Command blocked by maestro-ai: rm -rf is blocked")
    for pattern, reason in DESTRUCTIVE:
        if re.search(pattern, cmd, re.IGNORECASE):
            deny("Command blocked by maestro-ai: " + reason)
    # reading secrets through the shell
    for token in re.split(r"[\s;|&<>()=]+", cmd):
        if token and SENSITIVE_PATH.search(token):
            deny("Access to a secrets file through the shell is blocked: " + token)

sys.exit(0)
