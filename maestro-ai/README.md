# maestro-ai

Time de subagentes para desenvolvimento no Claude Code. A sessão principal orquestra: delega pesquisa, implementação, testes e revisão a agentes com modelo e ferramentas adequados a cada papel, e escala para modelos mais fortes quando necessário.

## Conteúdo

| Pasta | O que tem |
|---|---|
| `agents/` | pesquisador (haiku), analista, implementador, testador, revisor (sonnet), especialista, arquiteto (opus; fable sob aprovação) |
| `skills/orquestracao/` | Regras de delegação, escalonamento, pergunta do arquiteto, revisão; templates de briefing e de saída |
| `commands/` | `/maestro-ai:implementar-testar-revisar`, `/maestro-ai:revisao-pre-commit`, `/maestro-ai:salvar-contexto` e `/maestro-ai:retomar` |
| `hooks/` | `protecao.py` (bloqueia segredos e comandos destrutivos), `confirmar-fable.py` (confirmação ao usar Fable) e `aviso-contexto.py` (avisa quando a conversa ficou longa) |
| `templates/` | `AGENTS.md` modelo e `settings.json` com permissões allow/ask/deny |

## Instalação (uso pessoal)

Opção A (recomendada): instalar pelo marketplace local. Extraia o zip numa pasta fixa e, no Claude Code:
```
/plugin marketplace add /caminho/para/maestro-ai-marketplace
/plugin install maestro-ai@maestro-ai-marketplace
```
O `marketplace.json` passou em `claude plugin validate` e a instalação por esse caminho funcionou numa configuração isolada de teste (v0.1.1). Ainda não foi exercitado de ponta a ponta com um modelo; se o Claude Code da sua versão recusar, use a Opção B.

Opção B: testar o plugin direto da pasta:
```
claude --plugin-dir /caminho/para/maestro-ai
```

Opção C: prototipar sem plugin, copiando os arquivos para `~/.claude/`:
```
cp agents/*.md ~/.claude/agents/
cp -r skills/orquestracao ~/.claude/skills/
```
Nesse caso os comandos e hooks precisam ser copiados/registrados à parte.

Confirme na documentação da sua versão do Claude Code os detalhes de instalação de plugins e o formato do `hooks.json`.

## Permissões

Plugins normalmente não definem permissões. Copie o conteúdo de `templates/settings.json` para o `settings.json` do usuário (`~/.claude/settings.json`) ou do projeto (`.claude/settings.json`) e ajuste. Comece conservador e afrouxe com o uso. Na conta do trabalho, use a lista de bloqueios mais rígida.

## Por projeto

Copie `templates/AGENTS.md` para a raiz do repositório e preencha a seção "Projeto" (stack, comando de teste, convenções). Se a ferramenta lê `CLAUDE.md`, referencie o AGENTS.md de dentro dele.

## Contexto para conversas longas

1. O hook `aviso-contexto.py` avisa quando a conversa fica longa:
   - **Plano A:** se recebe `transcript_path`, avisa uma vez por sessão quando a transcrição passa de 600 KB (variável `MAESTRO_AI_LIMITE_KB`).
   - **Plano B:** se não houver transcrição legível, conta as mensagens e avisa a cada 30 (variável `MAESTRO_AI_LIMITE_MSGS`). É menos preciso: sem `session_id`, o contador é compartilhado entre as sessões do mesmo diretório.
2. `/maestro-ai:salvar-contexto` grava o estado em `.maestro-ai/contexto.md`.
3. Numa sessão nova (`/clear` ou outra janela), `/maestro-ai:retomar` lê só esse arquivo, confere o repositório e continua do próximo passo.

Coloque `.maestro-ai/` no `.gitignore` do projeto e nunca registre segredos no contexto.

## Pontos a validar na sua versão
- O hook `UserPromptSubmit` recebe `transcript_path` e `session_id`? Sem `transcript_path`, o aviso cai no plano B (contador de mensagens). Se o hook nem rodar, o aviso não dispara, mas os comandos funcionam do mesmo jeito.
- Nome do matcher de subagentes nos hooks (`Agent` ou `Task`; ambos estão configurados) e se o hook recebe o campo `model`.
- Se o alias `fable` funciona no frontmatter ou na chamada; se não, use o ID completo do modelo.
- Antes de usar no código da empresa: checar com TI/segurança modelos permitidos, uso de web e shell, e retenção de dados.
