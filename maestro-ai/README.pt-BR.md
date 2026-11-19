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

Se o usuário escreve em inglês, tudo é em inglês. Se escreve em outro idioma e nenhum está registrado, a sessão principal pergunta uma vez qual idioma usar e registra (`Language:` no `AGENTS.md` / no arquivo de contexto salvo).

## Conversas longas

- `/maestro-ai:save-context <nome>` grava um resumo em `.maestro-ai/context-<nome>.md` (o Git ignora a pasta sozinho: o comando grava dentro dela um `.gitignore` com `*`). Use um nome por conversa ou assunto, para os contextos não se misturarem; um arquivo existente só é atualizado quando é o mesmo assunto.
- `/maestro-ai:resume <nome>` continua a partir dele numa sessão limpa, tratando-o como anotações a conferir (verifica os arquivos listados e as suposições que bloqueiam o próximo passo), não como fatos. Sem nome, lista os contextos salvos e pergunta qual usar (ou usa o único que existir).
- Onde é salvo: sempre a pasta comum, organizada por assunto, qualquer que seja a pasta de trabalho (o `.maestro-ai/` do projeto é só reserva quando o acesso é recusado, e ainda é lido para contextos antigos): `~/Documents/maestro-ai/<assunto>/context-<nome>.md`, para uma sessão nova achar pelo nome. Várias conversas do mesmo assunto dividem a pasta, e os arquivos de trabalho de que o próximo passo precisa são copiados para `<assunto>/files/` quando são pequenos e seguros de copiar (sem sobrescrever); senão, são listados para você guardar. O arquivo tem as linhas `Project:` e `Path:`, e salvar de novo com o mesmo nome atualiza o mesmo arquivo, sem criar segunda cópia.
- Um hook oferece retomar o último contexto salvo ao abrir uma sessão numa pasta que tenha um, ou quando a pasta comum tem um dos últimos 7 dias (`MAESTRO_AI_RECENT_DAYS`); sem custo quando não há. Se o `resume` não achar nada em nenhuma das pastas, procura `context-*.md` pelo nome na pasta atual e em `~/Downloads` e pergunta qual usar. No chat sem acesso a arquivos, anexe o arquivo.
- No modo agente do Claude Desktop cada sessão tem a sua pasta temporária, então um contexto salvo ali não aparece na sessão seguinte. O `save-context` detecta isso, entrega o arquivo e avisa para você guardá-lo; na conversa nova, anexe o arquivo (ou informe o caminho completo) e rode `/maestro-ai:resume`.
- Quando a conversa ficar longa, o aviso pergunta com botões (Salvar contexto e limpar / Agora não). Se você aceitar, ele salva o contexto, grava o marcador `~/.maestro-ai/pending-resume.json` e limpa a conversa sozinho no Claude Code (a faixa `Save context and clear` e a ferramenta `clear_conversation` já vêm no plugin); onde isso não existe, você digita `/clear`. A opção `saveAndClear` na configuração do plugin desliga a faixa e a ferramenta. Depois da limpeza, o hook de início de sessão retoma o contexto salvo sem perguntar (depois de um `/clear` manual, qualquer primeira mensagem basta; com a faixa, não há nada a digitar). O marcador é achado de qualquer pasta de trabalho, usado uma vez e ignorado depois de 15 minutos (`MAESTRO_AI_FRESH_MIN`). À mão: `/maestro-ai:save-context <nome>` e depois `/clear`. No chat, que não tem `/clear`, abra uma conversa nova.
- Um hook avisa quando a conversa fica longa: pelo tamanho do transcript, se disponível (`MAESTRO_AI_LIMIT_KB`, padrão 600; pergunta de novo a cada vez que o transcript cresce esse tanto a mais, então "Agora não" não silencia para sempre), ou a cada N mensagens (`MAESTRO_AI_LIMIT_MSGS`, padrão 30).

## Validação

```
claude plugin validate .
python3 -m unittest discover -s tests -v
```
