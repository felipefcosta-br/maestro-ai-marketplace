# maestro-ai

[English](README.md)

Um time de subagentes para desenvolvimento de software. A sessão principal orquestra; os agentes executam com modelos e ferramentas fixos.

## Conteúdo

- **agents/**: sete subagentes (tabela abaixo)
- **skills/orchestration/**: regras de quando delegar, briefing, escalonamento e revisão (carregada sob demanda)
- **commands/**: `/maestro-ai:research`, `/maestro-ai:plan`, `/maestro-ai:save-context`, `/maestro-ai:resume` (em todo lugar); `/maestro-ai:implement-test-review`, `/maestro-ai:pre-commit-review` (código)
- **hooks/**: proteção contra segredos e comandos destrutivos, confirmação do Fable, aviso de conversa longa
- **templates/**: `AGENTS.md`, `settings.json`, formatos de briefing e saída

## Onde funciona

| Parte | Claude Code | Cowork | Chat (Desktop / claude.ai) |
|---|---|---|---|
| Skills e comandos | sim | sim | sim |
| Subagentes | sim | sim | não |
| Hooks | sim | sim | não |

No chat, as regras da skill ainda orientam a conversa (briefing, perguntar antes de decisões grandes, autorrevisão), mas nada troca de modelo nem bloqueia comandos. Plugins exigem plano pago.

## Agentes

| Agente | Modelo | Ferramentas | Papel |
|---|---|---|---|
| researcher | haiku | leitura, web | Buscar informação e ler documentação |
| analyst | sonnet | leitura, bash | Investigar código e logs (somente leitura) |
| implementer | sonnet | leitura, edição, bash | Implementar mudanças bem definidas |
| tester | sonnet | leitura, edição, bash | Escrever e rodar testes |
| specialist | opus | leitura, edição, bash | Tarefas complexas ou delicadas |
| architect | opus (fable sob pedido) | leitura, bash | Design e trade-offs; você sempre é perguntado Fable vs Opus, com recomendação |
| reviewer | sonnet | leitura, bash | Revisar código complexo ou implementado (somente leitura) |

Os agentes escrevem relatórios no idioma do briefing, no modo `summary` ou `didactic`.

## Instalação

```
claude plugin marketplace add felipefcosta-br/maestro-ai-marketplace
claude plugin install maestro-ai@maestro-ai-marketplace
```

Pelo marketplace (veja o README da raiz) ou por projeto, copiando `agents/`, `skills/` e `commands/` para `.claude/`.

## Permissões

`templates/settings.json` é um ponto de partida restrito (permite comandos de leitura, pergunta antes de editar, commitar ou usar rede, nega segredos e comandos destrutivos). Para uso corporativo, coloque no `.claude/settings.json` do repositório.

## AGENTS.md por projeto

Copie `templates/AGENTS.md` para cada repositório e preencha a seção "Project" (comando de teste, convenções, armadilhas).

## Idioma

Se o usuário escreve em inglês, tudo é em inglês. Se escreve em outro idioma e nenhum está registrado, a sessão principal pergunta uma vez qual idioma usar e registra (`Language:` no `AGENTS.md` / `.maestro-ai/context.md`).

## Conversas longas

- `/maestro-ai:save-context` grava um resumo em `.maestro-ai/context.md` (mantenha fora do Git).
- `/maestro-ai:resume` continua a partir dele numa sessão limpa.
- Um hook avisa quando a conversa fica longa: pelo tamanho do transcript, se disponível (`MAESTRO_AI_LIMIT_KB`, padrão 600), ou a cada N mensagens (`MAESTRO_AI_LIMIT_MSGS`, padrão 30).

## Validação

```
claude plugin validate .
python3 -m unittest discover -s tests -v
```
