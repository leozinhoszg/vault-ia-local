# Como ler um model card

Antes do download, registre: organização, nome exato, versão, commit ou tag, licença, uso comercial permitido, parâmetros totais e ativos, contexto, idiomas, modalidade, tokenizer, formato, requisitos de VRAM, método de quantização, benchmarks e limitações.

Não trate benchmark do fabricante como decisão final. Crie um conjunto de 30 a 100 prompts representativos, com respostas esperadas ou critérios de avaliação. Meça factualidade, aderência ao formato, segurança, latência, TTFT, tokens/s, memória máxima e comportamento com contexto longo.

| Campo | Pergunta |
|---|---|
| Licença | Posso usar e redistribuir no meu caso? |
| Pesos | São oficiais, convertidos pela comunidade ou quantizados? |
| Reprodutibilidade | Há hash, commit e parâmetros de inferência? |
| Contexto | É nativo ou apenas extrapolado? Qual o custo? |
| Dados | Existem restrições, dados pessoais ou obrigações de aviso? |
| Ferramentas | Há suporte no runtime escolhido? |
