---
description: Fluxo fixo - implementar uma tarefa, testar e revisar, delegando a cada agente do maestro-ai
argument-hint: <descrição da tarefa>
---
Execute o fluxo fixo **implementar → testar → revisar** para a tarefa abaixo, seguindo a skill `orquestracao` (briefing com `templates/briefing.md`).

Tarefa: $ARGUMENTS

Etapas (siga a ordem, sem pular):

1. **Entender.** Se a tarefa for ampla ou envolver mais de 3 arquivos, delegue o mapeamento ao `pesquisador` (modo `resumo`). Se for pequena, leia você mesmo. Se a descrição for ambígua, pergunte ao usuário antes de continuar.
2. **Plano curto.** Liste em poucas linhas o que será mudado e o critério de pronto. Se a tarefa for complexa ou arriscada, use o `especialista` em vez do `implementador`.
3. **Implementar.** Delegue ao `implementador` (ou `especialista`) com briefing completo: objetivo, arquivos, restrições, critério de pronto e o comando de teste do AGENTS.md. Modo `resumo`.
4. **Testar.** Delegue ao `testador`: criar ou atualizar testes para a mudança e rodar os relevantes. Se falhar, devolva a falha ao implementador. Após **duas falhas seguidas**, pare e pergunte ao usuário se deve subir para o `especialista` (e depois, se necessário, ao `arquiteto`, com a pergunta obrigatória sobre Fable/Opus e a sua recomendação).
5. **Revisar.** Delegue ao `revisor` com o objetivo original e `git diff` como fonte do diff. Corrija itens críticos e importantes (volte ao passo 3 para eles) e repita a revisão uma vez.
6. **Fechar.** Reporte ao usuário, em até 10 linhas: o que mudou, arquivos tocados, resultado dos testes, veredito do revisor e pendências. Não faça commit nem push sem pedido explícito.

Regras: agentes que editam arquivos rodam em série; nunca coloque segredos em briefings; confira o resultado de cada agente contra o critério de pronto antes de avançar.
