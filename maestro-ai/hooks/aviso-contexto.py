#!/usr/bin/env python3
"""UserPromptSubmit: avisa quando a conversa ficou longa.

Plano A: se o hook recebe `transcript_path`, mede o tamanho da transcrição e avisa
uma vez por sessão ao passar de MAESTRO_AI_LIMITE_KB (padrão 600).

Plano B: se não houver transcrição legível, conta as mensagens e avisa a cada
MAESTRO_AI_LIMITE_MSGS mensagens (padrão 30). A chave do contador é o `session_id`;
sem ele, usa o diretório de trabalho (o contador então é compartilhado entre
sessões do mesmo projeto, o que é impreciso, mas estável).
"""
import hashlib
import json
import os
import sys
import tempfile


def inteiro(nome, padrao):
    try:
        valor = int(os.environ.get(nome, padrao))
        return valor if valor > 0 else padrao
    except ValueError:
        return padrao


LIMITE_KB = inteiro("MAESTRO_AI_LIMITE_KB", 600)
LIMITE_MSGS = inteiro("MAESTRO_AI_LIMITE_MSGS", 30)

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
if not isinstance(data, dict):
    data = {}

tmp = tempfile.gettempdir()
session = "".join(c for c in str(data.get("session_id") or "") if c.isalnum() or c in "-_")
if session:
    chave = session
else:
    cwd = str(data.get("cwd") or os.getcwd())
    chave = "cwd" + hashlib.md5(cwd.encode("utf-8")).hexdigest()[:12]


def avisar(detalhe):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "Aviso do maestro-ai: a conversa já está longa (%s), o que aumenta o custo de cada nova "
                "resposta. Ao final da sua resposta atual, sugira ao usuário, em uma ou duas linhas, rodar "
                "/maestro-ai:salvar-contexto e continuar numa sessão limpa com /maestro-ai:retomar. Sugira apenas "
                "uma vez e não interrompa o trabalho em andamento." % detalhe
            ),
        }
    }))


transcript = data.get("transcript_path")

if isinstance(transcript, str) and os.path.isfile(transcript):
    # Plano A: tamanho da transcrição, um aviso por sessão
    tamanho_kb = os.path.getsize(transcript) / 1024
    if tamanho_kb >= LIMITE_KB:
        marcador = os.path.join(tmp, "maestro-ai-aviso-" + chave)
        if not os.path.exists(marcador):
            try:
                open(marcador, "w").close()
            except OSError:
                pass
            avisar("transcrição de ~%d KB" % int(tamanho_kb))
else:
    # Plano B: contador de mensagens, aviso a cada LIMITE_MSGS
    arquivo = os.path.join(tmp, "maestro-ai-contador-" + chave)
    try:
        with open(arquivo) as f:
            n = int(f.read().strip() or "0")
    except (OSError, ValueError):
        n = 0
    n += 1
    try:
        with open(arquivo, "w") as f:
            f.write(str(n))
    except OSError:
        pass
    if n % LIMITE_MSGS == 0:
        avisar("cerca de %d mensagens" % n)

sys.exit(0)
