---
description: Salva um resumo de contexto da implementação em .maestro-ai/contexto.md para continuar numa sessão nova sem reler a conversa
argument-hint: [observação opcional, ex.: o que priorizar na retomada]
---
Crie (ou atualize) o arquivo de contexto `.maestro-ai/contexto.md` na raiz do repositório, para que a implementação possa continuar numa sessão nova sem reler esta conversa. Observação do usuário: $ARGUMENTS

Passos:

1. **Verifique o estado real**, em vez de confiar só na memória da conversa: rode `git status --short`, `git branch --show-current` e `git log --oneline -5`, e `git diff --stat` se houver mudanças.
2. **Escreva o arquivo** (crie a pasta `.maestro-ai/` se necessário; se o arquivo já existir, atualize-o em vez de duplicar). Use exatamente esta estrutura, com no máximo ~60 linhas:

```
# Contexto da implementação

Atualizado em: <data e hora>
Branch: <branch> | Último commit: <hash curto e mensagem> | Mudanças não commitadas: <sim/não, resumo>

## Objetivo
<1-3 linhas: o que está sendo construído e por quê>

## Estado atual
<o que já está feito e funcionando; o que está em andamento>

## Decisões tomadas
- <decisão> — <motivo em uma linha>

## Próximos passos (em ordem)
1. <passo concreto>
2. ...

## Arquivos-chave
- <caminho> — <papel/o que mudou>

## Como validar
- <comando de teste e o que esperar>

## Armadilhas e pontos de atenção
- <o que já deu errado, o que evitar, dependências entre mudanças>

## Agentes e escalonamento
- <agentes já usados, falhas relevantes, se o arquiteto/especialista foi acionado e a decisão sobre Fable/Opus>

## Perguntas em aberto
- <decisões que dependem do usuário>
```

Regras:
- **Nunca inclua segredos**, credenciais, tokens ou dados de clientes.
- Seja denso e específico: caminhos, comandos e decisões, sem narrar a conversa.
- Registre só o que importa para continuar; não copie trechos grandes de código.
- Marque como "não verificado" o que não pôde ser conferido no repositório.

3. **Feche** com até 5 linhas: o caminho do arquivo, o resumo do estado, e a sugestão de continuar numa sessão limpa (`/clear` ou nova sessão) com `/maestro-ai:retomar`. Se `.maestro-ai/` não estiver no `.gitignore`, avise e pergunte se deve ser adicionado; não altere o `.gitignore` sem confirmação.
