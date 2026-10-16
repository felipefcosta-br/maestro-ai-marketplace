# maestro-ai

Time de subagentes para desenvolvimento no Claude Code. A sessão principal orquestra: delega pesquisa, implementação, testes e revisão a agentes com modelo e ferramentas adequados a cada papel, e escala para modelos mais fortes só quando necessário (o modelo mais caro sempre com aprovação do usuário).

Este repositório é um **marketplace** do Claude Code que contém o plugin `maestro-ai`. Documentação do plugin: [`maestro-ai/README.md`](maestro-ai/README.md).

## Instalar

Substitua `DONO` pelo usuário ou organização dona do repositório.

```
claude plugin marketplace add DONO/maestro-ai-marketplace
claude plugin install maestro-ai@maestro-ai-marketplace
```

Para repositório privado, a máquina precisa de acesso Git ao repositório (por exemplo, `gh auth login` ou chave SSH). A partir de uma cópia local, use o caminho da pasta no lugar de `DONO/...`.

Depois de instalar:
1. Copie `maestro-ai/templates/settings.json` para as suas permissões (o plugin não as define).
2. Use `maestro-ai/templates/AGENTS.md` como modelo em cada projeto.

> **Segurança:** o plugin inclui hooks, que são scripts executados na sua máquina. Leia `maestro-ai/hooks/*.py` antes de instalar, principalmente em máquina de trabalho, e confirme com TI/segurança quando houver política.

## Atualizar

Em cada máquina ou usuário onde estiver instalado:

```
claude plugin marketplace update maestro-ai-marketplace
claude plugin update maestro-ai@maestro-ai-marketplace
```

Reinicie o Claude Code para aplicar. O Claude Code usa o número da versão para saber se há novidade, então **toda mudança no plugin precisa de uma versão nova** (veja abaixo).

## Publicar uma melhoria (fluxo de release)

1. Faça a mudança dentro de `maestro-ai/`.
2. Suba a versão **nos dois lugares**: `maestro-ai/.claude-plugin/plugin.json` e `.claude-plugin/marketplace.json`.
3. Registre no `CHANGELOG.md`.
4. Rode os testes e a validação:
   ```
   python -m unittest discover -s tests -v
   claude plugin validate .
   ```
5. Faça commit, crie a tag (`git tag v0.1.2`) e dê push (`git push --follow-tags`).
6. Atualize as contas (seção anterior).

Os testes falham se as versões estiverem fora de sincronia, se faltar a entrada no changelog ou se uma regra de segurança do desenho for quebrada (por exemplo, agentes de leitura com permissão de escrita).

## Testes

```
python -m unittest discover -s tests -v
```

Cobrem os hooks (proteção de segredos e comandos destrutivos, confirmação do Fable, aviso de conversa longa) e a estrutura do plugin. O CI do GitHub Actions roda os mesmos testes a cada push.

Ainda não coberto: o comportamento dos agentes, comandos e hooks dentro de uma sessão real com um modelo.

## Estrutura

```
.claude-plugin/marketplace.json   catálogo do marketplace
maestro-ai/                       o plugin (agents, skills, commands, hooks, templates)
tests/                            testes dos hooks e da estrutura
CHANGELOG.md
```

## Licença

A definir. Enquanto não houver um arquivo `LICENSE`, todos os direitos ficam reservados ao autor.
