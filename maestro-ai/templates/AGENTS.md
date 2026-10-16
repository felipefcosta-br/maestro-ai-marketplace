# AGENTS.md

> Modelo curto. Preencha a seção "Projeto" em cada repositório e apague o que não se aplicar.
> Mantenha este arquivo enxuto: detalhes longos vão em `docs/` e as regras de orquestração ficam na skill `orquestracao` do plugin maestro-ai.

## Projeto
- **Linguagem/stack:** Kotlin (ajuste por projeto)
- **Build/gerenciador:** Gradle (`./gradlew`)
- **Hospedagem/CI:** GitHub (Actions)
- **Comando de teste (suíte completa):** `./gradlew test`
- **Teste de uma classe/método:** `./gradlew test --tests "pacote.NomeDaClasse"`
- **Lint/formatação:** `./gradlew ktlintCheck` (ou `detekt`; ajuste ao projeto)
- **Build:** `./gradlew build`

> Outras linguagens: troque os comandos acima (ex.: `npm test`, `pytest`, `mvn test`, `cargo test`).

## Convenções
- (Preencher: padrão de nomes, estrutura de pastas, estilo de commits, regras de PR)

## Armadilhas conhecidas
- (Preencher: módulos gerados que não se editam, flags obrigatórias, testes lentos, etc.)

## Documentação sob demanda
- Arquitetura: `docs/architecture.md` (ler ao mexer em módulos centrais)
- Decisões: `docs/decisions/` (ler antes de propor mudanças de desenho)

## Orquestração (resumo)
- Perguntas simples e tarefas pequenas (1-2 arquivos): resolver direto, sem delegar.
- Tarefas amplas, com mais de 3 arquivos ou muito ruído: delegar aos agentes do maestro-ai, seguindo a skill `orquestracao` (quem faz o quê, briefing, escalonamento, revisão).
- **Arquiteto:** antes de acioná-lo, perguntar ao usuário se quer Fable ou Opus, sempre incluindo a recomendação.
- Fluxos fixos: `/maestro-ai:implementar-testar-revisar` e `/maestro-ai:revisao-pre-commit`.
- Conversa longa: `/maestro-ai:salvar-contexto` grava `.maestro-ai/contexto.md` e `/maestro-ai:retomar` continua numa sessão limpa. Manter `.maestro-ai/` fora do Git.

## Segurança
- Nunca colocar neste arquivo, em briefings ou em logs: credenciais, tokens, chaves, dados de clientes ou informação confidencial.
- Não ler `.env`, arquivos de chaves ou segredos (o plugin também bloqueia por hook).
- Somente o `pesquisador` acessa a web. Agentes que escrevem não usam rede nem instalam pacotes.
- Pedir confirmação antes de: instalar pacotes, comandos com rede, `git commit` e `git push`.
- Proibido: `rm -rf` e comandos destrutivos sem pedido explícito.
