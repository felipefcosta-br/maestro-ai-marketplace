---
description: Retoma a implementação a partir de .maestro-ai/contexto.md, sem reler a conversa anterior
argument-hint: [foco opcional para esta sessão]
---
Retome o trabalho a partir do contexto salvo. Foco opcional do usuário: $ARGUMENTS

Passos:

1. **Leia `.maestro-ai/contexto.md`.** Se não existir, avise o usuário e sugira `/maestro-ai:salvar-contexto` na sessão anterior; não tente reconstruir o contexto vasculhando o projeto inteiro.
2. **Confira se o contexto está atual**: rode `git status --short`, `git branch --show-current` e `git log --oneline -5` e compare com a branch, o último commit e as mudanças registradas no arquivo. Se houver divergência (commits novos, branch diferente, arquivos alterados que o contexto não menciona), liste-as e pergunte ao usuário como seguir antes de editar qualquer coisa.
3. **Leia só o necessário.** Abra apenas os "Arquivos-chave" relacionados ao próximo passo, e apenas os trechos relevantes. Não releia o projeto inteiro nem refaça trabalho que o contexto marca como concluído.
4. **Resuma em até 5 linhas**: objetivo, estado, próximo passo e perguntas em aberto.
5. **Continue** pelo primeiro item de "Próximos passos", seguindo a skill `orquestracao` (delegar só quando compensar, briefing completo, escalonamento e revisão como de costume). Respeite as decisões e armadilhas registradas; se precisar contrariá-las, avise o usuário antes.
6. Ao concluir cada passo relevante, sugira atualizar o contexto com `/maestro-ai:salvar-contexto`.

Se houver "Perguntas em aberto" que bloqueiam o próximo passo, faça-as ao usuário primeiro.
