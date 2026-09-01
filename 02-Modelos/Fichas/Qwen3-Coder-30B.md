# Qwen3-Coder-30B-A3B-Instruct

| Campo | Registro |
|---|---|
| Data de verificação | 2026-09-01 |
| Checkpoint | `Qwen/Qwen3-Coder-30B-A3B-Instruct` no Hugging Face; o guia Atomic chama o modelo de "Qwen3-Coder 30B" e este vault assume que se refere a esse checkpoint |
| Arquitetura | Causal MoE para código; 48 camadas; 128 experts, 8 ativados por token; GQA com 32 heads Q e 4 heads KV; modo somente non-thinking (não emite blocos `<think>`) [1] |
| Parâmetros totais/ativos | 30,5B totais / 3,3B ativados, conforme model card oficial [1] |
| Contexto | 262.144 tokens nativos; o card informa extensão até 1M com YaRN, o que depende do runtime e degrada qualidade sem validação [1] |
| Licença | Apache-2.0 declarada no model card; confirmar no arquivo LICENSE do commit baixado antes de uso comercial [1] |
| Quantizações | Verificar GGUF/AWQ/GPTQ por arquivo; o tamanho real do Q4 depende do quantizador e do formato de bloco |
| Memória estimada | Q4 editorial ~22 GB medido pela Atomic [2]; piso teórico dos pesos em 4 bits é 30,5B × 0,5 B ≈ 15,25 GB decimal antes de escalas, embeddings e KV cache; em MoE, o armazenamento usa os parâmetros **totais** |
| Hardware medido | Atomic Chat: configuração do artigo; benchmark próprio pendente |
| Velocidade | 220 tok/s no teste Atomic [2]; observação de teste, não especificação; não generalizar |
| Tool calling/JSON | O card descreve suporte a function calling com formato próprio de parser; validar com harness local antes de uso agentic [1] |
| Fonte primária | [Model card oficial](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) [1] |
| Fonte editorial | [[02-Modelos/LLMs-locais-para-coding-Atomic]]; [Atomic Chat](https://atomic.chat/blog/guides/best-local-llms-for-coding) [2] |
| Ficha padrão | [[02-Modelos/Ficha-padronizada-por-modelo]] |
| Estado | Candidato para GPU de 24 GB, sujeito a teste |
| Dono | Luiz Guimarães |
| Próxima revisão | 2026-10-01 |

Com 3,3B parâmetros ativos, o modelo tende a decodificar rápido em relação ao seu tamanho total, mas os 30,5B precisam caber em memória. Em uma GPU de 24 GB, o Q4 deixa margem limitada para KV cache em contexto longo; para 128K ou mais, planeje offload, KV quantizado ou GPU maior, conforme [[05-Memoria-e-Performance/KV-cache-formula-e-exemplos]].

## Referências

[1]: https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct "Qwen3-Coder-30B-A3B-Instruct — model card oficial (parâmetros, contexto, licença)"
[2]: https://atomic.chat/blog/guides/best-local-llms-for-coding "Atomic Chat — Best Local LLM for Coding (medições editoriais)"
