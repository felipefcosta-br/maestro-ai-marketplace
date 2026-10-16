#!/usr/bin/env python3
"""PreToolUse: bloqueia acesso a segredos e comandos destrutivos."""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
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


# Arquivos sensíveis (.env.example e similares são permitidos)
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

# Comandos destrutivos
DESTRUCTIVE = [
    (r"\brm\s+(-[a-zA-Z]*\s+)*-[a-zA-Z]*[rR][a-zA-Z]*[fF]|\brm\s+(-[a-zA-Z]*\s+)*-[a-zA-Z]*[fF][a-zA-Z]*[rR]|\brm\s+.*--recursive.*--force|\brm\s+.*--force.*--recursive",
     "rm -rf é bloqueado"),
    (r"\bgit\s+push\b.*(--force\b|--force-with-lease\b|\s-f\b)", "git push --force é bloqueado"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard é bloqueado"),
    (r"\bgit\s+clean\b.*-[a-zA-Z]*[fdx]", "git clean destrutivo é bloqueado"),
    (r"\bdrop\s+(database|table|schema)\b", "DROP em banco de dados é bloqueado"),
    (r"\bmkfs(\.\w+)?\b|\bdd\s+if=", "comando de disco destrutivo é bloqueado"),
    (r"\bchmod\s+-R\s+777\b", "chmod -R 777 é bloqueado"),
    (r"(curl|wget)\b[^|]*\|\s*(sudo\s+)?(ba)?sh\b", "baixar e executar script (curl | sh) é bloqueado"),
]

if tool in ("Read", "Edit", "Write", "NotebookEdit", "Grep", "Glob"):
    for key in ("file_path", "path", "notebook_path"):
        p = ti.get(key)
        if isinstance(p, str) and SENSITIVE_PATH.search(p.replace("\\", "/")):
            deny("Acesso a arquivo de segredos bloqueado: " + p)

elif tool == "Bash":
    cmd = ti.get("command") or ""
    for pattern, reason in DESTRUCTIVE:
        if re.search(pattern, cmd, re.IGNORECASE):
            deny("Comando bloqueado pelo maestro-ai: " + reason)
    # leitura de segredos via shell
    for token in re.split(r"[\s;|&<>()]+", cmd):
        token = token.strip("'\"")
        if token and SENSITIVE_PATH.search(token.replace("\\", "/")):
            deny("Acesso a arquivo de segredos via shell bloqueado: " + token)

sys.exit(0)
