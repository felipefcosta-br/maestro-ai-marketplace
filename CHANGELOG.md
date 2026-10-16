# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versões seguem [SemVer](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Adicionado
- Repositório Git: `.gitignore`, testes dos hooks e da estrutura (`tests/`), CI no GitHub Actions e README de raiz.

## [0.1.1] - 2026-10-16

### Adicionado
- `marketplace.json`: o repositório passa a ser um marketplace instalável (`maestro-ai@maestro-ai-marketplace`).

### Alterado
- Plugin renomeado de `maestro` para `maestro-ai`: prefixo dos comandos (`/maestro-ai:…`), pasta de contexto (`.maestro-ai/`) e variáveis de ambiente (`MAESTRO_AI_LIMITE_KB`, `MAESTRO_AI_LIMITE_MSGS`).

## [0.1.0] - 2026-10-15

### Adicionado
- Sete agentes: pesquisador (haiku), analista, implementador, testador, revisor (sonnet), especialista e arquiteto (opus; Fable só com aprovação do usuário).
- Skill `orquestracao`: delegação, escalonamento, pergunta obrigatória do arquiteto com recomendação, revisão, templates de briefing e de saída.
- Comandos: `implementar-testar-revisar`, `revisao-pre-commit`, `salvar-contexto` e `retomar`.
- Hooks: `protecao` (segredos e comandos destrutivos), `confirmar-fable` e `aviso-contexto` (conversa longa, com plano B por contagem de mensagens).
- Modelos em `templates/`: `AGENTS.md` e `settings.json` (permissões allow/ask/deny).
