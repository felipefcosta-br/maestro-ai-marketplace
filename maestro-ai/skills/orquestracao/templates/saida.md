# Modos de saída

## `resumo` (padrão para execução)
Máximo de 15 linhas:
1. O que foi feito ou concluído
2. Arquivos tocados (caminhos)
3. Resultado dos testes (passou/falhou, contagem)
4. Riscos ou pendências

## `didático` (padrão para análise e quando o usuário quer entender)
Explicação passo a passo:
1. Contexto: o que está sendo analisado e por quê
2. Raciocínio em etapas curtas, com exemplos pequenos
3. Evidências (arquivo:linha), separando fatos de hipóteses
4. Conclusão e próximos passos sugeridos

## Regras comuns
- Sem colar trechos grandes de código: aponte caminho e linhas.
- Sem segredos na resposta, mesmo que apareçam em logs.
- Diga claramente o que não foi verificado.
