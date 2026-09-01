# Referências de desempenho de GPU para IA local

**Data de verificação:** 1º de setembro de 2026. Este arquivo não transforma números de um benchmark em promessa universal. Desempenho depende de modelo, quantização, contexto, batch, runtime, driver, CUDA, temperatura, potência e se a medição é prompt processing ou decode.

## Hierarquia de evidência

| Nível | Fonte | Uso correto |
|---|---|---|
| 1 | Medição própria com `llama-bench`, vLLM ou MLPerf | Decisão final para a máquina e o modelo específicos. |
| 2 | Benchmark reproduzível de terceiros com configuração completa | Comparação inicial, sempre registrando as condições. |
| 3 | Especificação oficial, TFLOPS, Tensor TOPS e largura de banda | Explicar capacidade física e formar hipóteses; não estimar tokens/s sozinho. |
| 4 | Relato sem modelo, quantização, contexto e runtime | Não usar para compra ou TCO. |

## Referências externas localizadas

O resultado OpenBenchmarking de llama.cpp para RTX 5090 é uma fonte de medições que deve ser lida junto com a configuração do sistema e do modelo [1]. O tópico de benchmark do llama.cpp para RTX 5090 e outras GPUs discute a escolha do modelo e o risco de comparar apenas números agregados [2]. O benchmark CloudRift compara RTX 4090, RTX 5090 e RTX PRO 6000 com vLLM e modelos quantizados de 24, 48 e 96 GB [3]. Esses resultados são referências externas, não medições deste vault.

## Como gerar uma medição válida

Use um arquivo de modelo fixo, por exemplo GGUF Q4_K_M, e registre hash. Rode cinco repetições após aquecimento, separe `pp` de `tg`, teste contextos de 4K, 16K e 32K, e registre tokens/s, TTFT, P50, P95, VRAM, RAM, potência na tomada, temperatura, driver, CUDA e versão do runtime. Em vLLM, registre concorrência, batch, throughput agregado e latência por requisição.

Para comparar GPUs, a pergunta correta é “qual GPU entrega menor custo por token para este modelo, contexto e SLO?”, e não “qual GPU tem mais TFLOPS?”. Uma RTX 4060 Ti 16 GB pode vencer uma RTX 4070 12 GB em capacidade de modelo, embora perca em banda; uma RTX 6000 Ada pode vencer uma RTX 4090 em viabilidade de 70B por caber em 48 GB, ainda que custe muito mais.

## Referências

[1]: https://openbenchmarking.org/result/2501264-PTS-LLAMACPP76 "OpenBenchmarking — llama.cpp NVIDIA GeForce RTX 5090"
[2]: https://news.ycombinator.com/item?id=43317406 "Discussão de benchmark llama.cpp e RTX 5090"
[3]: https://www.cloudrift.ai/blog "CloudRift — benchmarks de inferência em RTX 4090, RTX 5090 e RTX PRO 6000"
[4]: https://github.com/ggml-org/llama.cpp "llama.cpp — llama-bench"
[5]: https://docs.vllm.ai/ "vLLM — serving e throughput"
[6]: https://mlcommons.org/benchmarks/client/ "MLPerf Client"
