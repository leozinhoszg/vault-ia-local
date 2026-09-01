# Qwen3.6-27B

| Campo | Registro |
|---|---|
| Data de verificação | 2026-09-01 |
| Arquitetura | Causal multimodal, conforme model card |
| Parâmetros totais/ativos | 27B / N/A (dense) |
| Contexto | 262.144 tokens no model card |
| Licença | Apache-2.0, confirmar termos da versão baixada |
| Quantizações | Verificar GGUF/AWQ/GPTQ por arquivo |
| Memória estimada | Q4: piso de pesos ~13,5 GB + overhead/KV; medir o arquivo real |
| Hardware medido | Não medido neste sandbox |
| Velocidade | Não publicar sem benchmark próprio; PromptQuorum registra números editoriais separados |
| Tool calling/JSON | Validar no runtime escolhido |
| Fonte primária | [[02-Modelos/Ficha-padronizada-por-modelo]] e [model card](https://huggingface.co/Qwen/Qwen3.6-27B) |
| Estado | Candidato para piloto |
| Dono | Luiz Guimarães |
| Próxima revisão | 2026-10-01 |

O modelo é adequado para testes de coding, RAG e contexto longo em Macs e workstations com 32–64 GB ou mais, dependendo da quantização, KV cache e concorrência. Essa é uma recomendação de capacidade, não uma promessa de tokens/s.
