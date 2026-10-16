# marketplace maestro-ai

[English](README.md)

Um marketplace do Claude Code que distribui o **maestro-ai**: um time de subagentes especializados para desenvolvimento de software. A sessão principal orquestra e delega a agentes com modelos e ferramentas fixos, para reduzir custo e aumentar a qualidade.

## Instalação

```
claude plugin marketplace add felipefcosta-br/maestro-ai-marketplace
claude plugin install maestro-ai@maestro-ai-marketplace
```

O repositório é privado: o Git precisa estar autenticado com uma conta que consiga lê-lo (com o GitHub CLI: `gh auth switch -u felipefcosta-br`). O plugin é instalado por usuário do sistema (`~/.claude`), então uma instalação atende todas as contas Claude da máquina.

## Atualização

```
claude plugin marketplace update maestro-ai-marketplace
claude plugin update maestro-ai@maestro-ai-marketplace
```

Depois reinicie o Claude Code.

## Fluxo de release

1. Altere o plugin.
2. Aumente `version` em `maestro-ai/.claude-plugin/plugin.json` e em `.claude-plugin/marketplace.json`.
3. Adicione uma entrada no `CHANGELOG.md`.
4. Rode `python3 -m unittest discover -s tests -v` e `claude plugin validate .`.
5. Commit, `git tag vX.Y.Z`, `git push --follow-tags`.

## Nota de segurança

O plugin inclui hooks que executam scripts Python locais (bloqueiam segredos e comandos destrutivos, pedem confirmação antes de usar o Fable e avisam sobre conversas longas). Revise-os em `maestro-ai/hooks/` antes de usar em ambiente corporativo.

## Estrutura

```
.claude-plugin/marketplace.json
maestro-ai/        o plugin (agentes, skill, comandos, hooks, templates)
tests/             testes unitários (também rodam no CI)
```

Veja [maestro-ai/README.pt-BR.md](maestro-ai/README.pt-BR.md) para o plugin em si.

## Licença

A definir.
