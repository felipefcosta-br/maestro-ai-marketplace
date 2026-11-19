# maestro-ai-clear

Mod opcional do plugin `maestro-ai`. Transforma "salvar o contexto e começar limpo" em um único passo:

1. Uma faixa acima do prompt (depois de 15 turnos) oferece **Save context and clear**. A ferramenta `clear_conversation` faz o mesmo quando o Claude a chama depois do aviso de conversa longa.
2. Ele roda `/maestro-ai:save-context` e confere se o salvamento terminou (a linha final `/maestro-ai:resume <nome>`).
3. Roda `/clear` e depois `/maestro-ai:resume <nome>`, e o trabalho continua do contexto salvo sem você digitar nada.

Exige o `maestro-ai` 0.5.0 ou superior. Sem o mod tudo continua funcionando: você digita `/clear` e o hook de início de sessão do `maestro-ai` retoma o contexto salvo na sua primeira mensagem.

Se o salvamento não for confirmado, a conversa não é limpa. Se o `/clear` ou a retomada não puderem rodar, uma mensagem diz o comando para digitar.
