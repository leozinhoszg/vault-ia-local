# Fórmula real do KV cache

## Fórmula para atenção MHA/GQA/MQA

Para uma camada de atenção convencional:

`KV_bytes = tokens × sessões × camadas × 2(K,V) × n_kv_heads × head_dim × bytes_por_elemento`

Se houver paginação, fragmentação, alinhamento, prefix cache e estruturas do runtime, o pico real será maior. Use uma margem de 10–30% e some pesos, ativações e workspace.

A fórmula usa **número de cabeças KV**, não número total de cabeças de query. GQA/MQA reduz o KV cache. O número de parâmetros do modelo não entra diretamente na fórmula; em MoE, o KV cache depende da arquitetura de atenção e contexto, não do total de experts.

## Exemplos em FP16/BF16

| Modelo de referência | Camadas | KV heads | Head dim | KV por token | 4K / sessão | 8K / sessão | 32K / sessão |
|---|---:|---:|---:|---:|---:|---:|---:|
| 8B GQA típico | 32 | 8 | 128 | 128 KiB | 0,50 GiB | 1,00 GiB | 4,00 GiB |
| Qwen3.6-27B | 64 | 4 | 256 | 256 KiB | 1,00 GiB | 2,00 GiB | 8,00 GiB |
| 70B GQA típico | 80 | 8 | 128 | 320 KiB | 1,25 GiB | 2,50 GiB | 10,00 GiB |
| MoE com 61 camadas, 8 KV heads e 128 dim | 61 | 8 | 128 | 244 KiB | 0,95 GiB | 1,91 GiB | 7,63 GiB |

Os exemplos são aproximações pedagógicas. Confirme os hiperparâmetros no `config.json` ou model card da versão exata. Para modelos com Multi-head Latent Attention, como alguns Kimi, a implementação pode armazenar um estado latente diferente; use a fórmula do runtime/modelo, não a tabela convencional.

## Concorrência

Com 10 sessões de Qwen3.6-27B em 8K, a aproximação é 20 GiB somente de KV FP16, antes de pesos e buffers. Quantizar KV para 8 bits pode reduzir aproximadamente pela metade a parte correspondente, mas a economia e a qualidade dependem da implementação. Um servidor deve reservar memória para o pior pico, não para uma única conversa média.

## Checklist de cálculo

1. Obtenha camadas, KV heads, head dimension e tipo de KV.
2. Multiplique pelo contexto máximo real, não pelo contexto anunciado sem teste.
3. Multiplique pelo número máximo de sequências simultâneas.
4. Some pesos quantizados, workspace, prefix cache e overhead.
5. Reserve folga e teste OOM em canary.

*Última atualização: 2026-09-01. Próxima revisão: 2026-10-01.*

## Referências

[1]: https://huggingface.co/Qwen/Qwen3.6-27B "Qwen3.6-27B — arquitetura e hiperparâmetros"
[2]: https://github.com/ggml-org/llama.cpp "llama.cpp — KV cache e backends"
[3]: https://docs.vllm.ai/ "vLLM — paged attention e serving"
