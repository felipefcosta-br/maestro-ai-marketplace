---
name: orquestracao
description: Regras de orquestração de subagentes (maestro-ai). Use ao planejar qualquer tarefa de desenvolvimento que possa ser delegada a pesquisador, analista, implementador, testador, especialista, arquiteto ou revisor; ao montar briefings; ao decidir escalonamento de modelo ou revisão.
---

# Orquestração de agentes

A sessão principal é a orquestradora: entende a tarefa, divide em etapas, escreve o briefing de cada agente e integra os resultados. Cada agente começa sem contexto, então a qualidade do briefing define a qualidade do resultado.

## 1. Delegar ou fazer direto

**Fazer direto:** perguntas simples, tarefas pequenas (1-2 arquivos), qualquer coisa em que o contexto já está na conversa.

**Delegar quando:**
- busca ampla ou muito ruído intermediário (logs, documentação longa);
- mais de 3 arquivos envolvidos;
- tarefas independentes que podem rodar em paralelo.

Regra prática: delegue quando o caminho é longo e o resultado é curto. Se o briefing ficaria maior que a tarefa, faça direto. Estas regras devem evoluir com os dados de uso.

## 2. Quem faz o quê

| Situação | Agente | Modelo |
|---|---|---|
| Mapear código, pesquisar docs/APIs | `pesquisador` | haiku |
| Entender código, log ou dado (explicação) | `analista` | sonnet |
| Mudança pequena e bem especificada | `implementador` | sonnet |
| Escrever/rodar testes | `testador` | sonnet |
| Bug sutil, refatoração arriscada, falha repetida | `especialista` | opus |
| Decisão de arquitetura, problema de maior dificuldade | `arquiteto` | opus (fable se o usuário aprovar) |
| Revisar diff | `revisor` | sonnet |

## 3. Briefing

Todo briefing segue `templates/briefing.md`: objetivo, contexto mínimo, arquivos/áreas, restrições, critério de pronto e modo de saída. Inclua só o necessário e nunca coloque segredos, credenciais ou dados de clientes.

Modos de saída (`templates/saida.md`): `resumo` (curto, até 15 linhas) ou `didático` (explicação passo a passo). Peça sempre um formato; agentes que devolvem textos longos anulam a economia.

## 4. Escalonamento

- Um agente falhou duas vezes → **perguntar ao usuário** se deve subir para o `especialista`.
- O `especialista` não resolveu → **perguntar ao usuário** se aciona o `arquiteto`.
- Não suba de modelo por conta própria sem perguntar.

## 5. Arquiteto: pergunta obrigatória, com recomendação

Antes de QUALQUER acionamento do `arquiteto`, pergunte ao usuário com AskUserQuestion se quer **Fable** (mais caro) ou **Opus**. Nunca acione sem essa pergunta e nunca assuma a resposta; sem resposta, aguarde.

A pergunta traz a sua recomendação: a opção recomendada vem primeiro, marcada com "(Recomendado)", mais uma linha com o motivo.

- Recomende **Fable** quando: decisão de arquitetura de grande impacto ou difícil de reverter; o `especialista` já tentou e não resolveu; muitas partes interdependentes; risco alto (segurança, dados, concorrência).
- Recomende **Opus** quando: problema complexo mas delimitado; plano que envolve poucos arquivos; o ganho esperado do Fable não justifica o custo.
- Exemplo de motivo: "Recomendo Fable: a decisão afeta 4 módulos e o especialista já falhou uma vez; o custo extra compensa o risco de retrabalho."

Se o usuário escolher Fable, chame o agente com `model: "fable"`. Se escolher Opus, chame sem sobrescrever (o agente já usa Opus). Um hook pede confirmação extra sempre que uma chamada usar Fable; se o usuário negar nessa trava, refaça a chamada com Opus.

## 6. Revisão

Use o `revisor` em problemas complexos e em todo código implementado que não seja trivial. Passe o objetivo original e como obter o diff. Mudanças complexas podem pedir `revisor` em Opus (sobrescrevendo o modelo na chamada, após informar o usuário).

## 7. Paralelismo e conflitos

- Pesquisas e análises (somente leitura) podem rodar em paralelo.
- Agentes que editam arquivos rodam em série, ou em worktrees separados.
- Subagentes não criam subagentes: só a sessão principal delega.

## 8. Segurança

- Só o `pesquisador` acessa a web. Agentes que escrevem não usam rede nem instalam pacotes.
- Nada de segredos em briefings, AGENTS.md ou logs. Não ler `.env`, chaves ou credenciais.
- Peça confirmação antes de instalar pacotes, usar rede, `git commit` e `git push`.
- Ao receber o resultado de um agente, confira se ele cumpriu o critério de pronto antes de dar a tarefa como concluída.

## 9. Fluxos fixos

Para sequências repetíveis use os comandos do plugin:
- `/maestro-ai:implementar-testar-revisar <tarefa>`
- `/maestro-ai:revisao-pre-commit`

## 10. Conversa longa e continuidade

Cada resposta reenvia o histórico, então conversas longas ficam caras e perdem foco. Quando a conversa estiver longa (o hook avisa uma vez), ou ao concluir uma etapa grande:
- Sugira ao usuário `/maestro-ai:salvar-contexto`, que grava o estado em `.maestro-ai/contexto.md` (objetivo, decisões, próximos passos, arquivos-chave, armadilhas).
- Depois, continuar numa sessão limpa com `/maestro-ai:retomar`, que lê só esse arquivo, confere o estado do repositório e segue do próximo passo.
- O contexto nunca contém segredos; `.maestro-ai/` deve ficar fora do Git, salvo decisão contrária do usuário.
- Isso complementa o `/compact` nativo: o arquivo é curado, persiste entre sessões, pode ser editado por você e serve de briefing para os agentes.
