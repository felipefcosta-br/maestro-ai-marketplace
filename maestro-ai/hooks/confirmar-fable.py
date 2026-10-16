#!/usr/bin/env python3
"""PreToolUse: exige confirmação do usuário sempre que um subagente for chamado com o modelo Fable."""
import json
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_input = data.get("tool_input") or {}
model = str(tool_input.get("model") or "").lower()

if "fable" in model:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                "Esta chamada usa o modelo Fable (mais caro). "
                "Aprove para continuar; se negar, o agente deve rodar em Opus."
            ),
        }
    }))
sys.exit(0)
