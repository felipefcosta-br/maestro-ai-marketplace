---
description: Fluxo fixo - revisão pré-commit das mudanças atuais (diff, testes e veredito), sem editar código
argument-hint: [foco opcional, ex.: segurança, concorrência]
---
Faça a **revisão pré-commit** das mudanças atuais do repositório, seguindo a skill `orquestracao`. Foco opcional do usuário: $ARGUMENTS

Etapas:

1. **Levantar o estado.** Rode `git status` e `git diff` (incluindo `git diff --staged`) para saber o que mudou. Se não houver mudanças, avise e encerre.
2. **Testes.** Delegue ao `testador` a execução dos testes relevantes às áreas alteradas (comando de teste do AGENTS.md), em modo `resumo`. Em mudanças pequenas e de baixo risco, você pode rodar o comando direto.
3. **Revisão.** Delegue ao `revisor` com o objetivo das mudanças (inferido do diff e das mensagens recentes, ou perguntado ao usuário se não estiver claro) e como obter o diff. Se o diff for grande ou complexo, informe ao usuário e pergunte se quer o `revisor` em Opus.
4. **Segurança rápida.** Confirme que o diff não contém segredos (chaves, tokens, senhas, `.env`), arquivos de build ou dados de clientes.
5. **Relatório.** Entregue em até 15 linhas: resultado dos testes, achados do revisor por severidade (crítico, importante, sugestão), riscos e um veredito: **pronto para commit**, **pronto com ressalvas** ou **não commitar ainda**.

Regras: este fluxo **não edita código** e **não faz commit nem push**. Se algo precisar de correção, descreva-a e pergunte se o usuário quer que seja aplicada.
