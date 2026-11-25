# marketplace maestro-ai

[English](README.md)

Um marketplace do Claude Code que distribui o **maestro-ai**: um time de subagentes especializados para desenvolvimento de software. A sessão principal orquestra e delega a agentes com modelos e ferramentas fixos, para reduzir custo e aumentar a qualidade.

## Instalação

```
claude plugin marketplace add felipefcosta-br/maestro-ai-marketplace
claude plugin install maestro-ai@maestro-ai-marketplace
```

O repositório é público, então não é preciso entrar em nenhuma conta para instalar. O plugin é instalado por usuário do sistema (`~/.claude`), então uma instalação atende todas as contas Claude da máquina.

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

O plugin inclui hooks que executam scripts Python locais (bloqueiam segredos e comandos destrutivos, pedem confirmação antes de usar o Fable, avisam sobre conversas longas e oferecem retomar um contexto salvo). Revise-os em `maestro-ai/hooks/` antes de usar em ambiente corporativo. O hook de proteção compara padrões de texto: é uma rede de segurança, não uma garantia, e pode ser contornado. Mantenha suas próprias regras de permissão e revise o que os agentes fazem.

- O marcador e os arquivos de contexto são dados no disco: depois de um clear, o plugin só retoma um arquivo chamado `context-<nome>.md` dentro de uma pasta `.maestro-ai` ou da pasta comum (arquivo comum, sem link simbólico, menor que 512 KB), e `/maestro-ai:resume` trata o texto dele como anotações, não como instruções.
- `analyst`, `architect` e `reviewer` são somente leitura por instrução: têm Bash e nada técnico os impede. Use `templates/settings.json` para regras de permissão de verdade.
- Cadeia de suprimento: quem consegue publicar neste repositório muda o que suas máquinas executam. Use 2FA ou passkey na conta do GitHub, proteja a `main`, assine commits e, em máquina corporativa, fixe a versão ou desligue a atualização automática do marketplace e atualize de propósito depois de ler o CHANGELOG.
- Coloque `.maestro-ai/` no `.gitignore` de todo projeto: os contextos podem conter detalhes do projeto.

## Estrutura

```
.claude-plugin/marketplace.json
maestro-ai/        o plugin (agentes, skill, comandos, hooks, templates)
tests/             testes unitários (também rodam no CI)
```

Veja [maestro-ai/README.pt-BR.md](maestro-ai/README.pt-BR.md) para o plugin em si.

## Licença

[MIT](LICENSE).
