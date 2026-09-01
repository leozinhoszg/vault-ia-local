# FP8 versus FP4 na IA local

**Data de verificação:** 1º de setembro de 2026. **Escopo:** inferência e treinamento de modelos de IA local. FP8 e FP4 são formatos numéricos de baixa precisão; eles podem ser usados em quantização, mas não são sinônimos de todos os métodos de quantização. Um checkpoint FP8 ou FP4 inclui representação dos valores e, frequentemente, escalas, grupos, calibração e metadados.

## Resumo técnico

FP8 usa 8 bits por elemento e oferece margem numérica significativamente maior que FP4. O FP8 E4M3 tem 1 bit de sinal, 4 de expoente e 3 de mantissa, com valor máximo aproximado de ±448. O FP8 E5M2 troca mantissa por alcance, chegando aproximadamente a ±57.344. A NVIDIA documenta E4M3 como mais apropriado para forward/ativação e E5M2 para gradientes/backward em receitas de treinamento FP8 [1].

FP4 usa 4 bits por elemento. A forma E2M1 tem 1 bit de sinal, 2 de expoente e 1 de mantissa, com poucos valores representáveis e magnitude aproximada até ±6. Por isso, FP4 depende mais de escalas granulares, calibração, tratamento de outliers e preservação de camadas sensíveis. Em Blackwell, NVFP4 associa valores E2M1 a escala FP8 E4M3 por blocos de 16 e uma escala FP32 por tensor; MXFP4 usa uma escala E8M0 por bloco de 32 [1] [2].

> **Regra prática:** FP8 costuma ser a escolha conservadora quando a qualidade, o treinamento ou a estabilidade numérica têm prioridade. FP4 é a escolha agressiva para reduzir memória e aumentar throughput em hardware com aceleração nativa, especialmente NVIDIA Blackwell, desde que o modelo, o runtime e a avaliação suportem o formato.

## Comparação de representação

| Característica | FP8 E4M3 | FP8 E5M2 | FP4 E2M1 / NVFP4 | Consequência |
|---|---:|---:|---:|---|
| Bits por valor | 8 | 8 | 4 | FP4 reduz aproximadamente pela metade o armazenamento elementar de FP8 e para um quarto do FP16, antes de escalas/metadados. |
| Bits de expoente | 4 | 5 | 2 | FP8 E5M2 tem maior alcance; FP4 tem alcance muito menor. |
| Bits de mantissa | 3 | 2 | 1 | FP8 E4M3 preserva mais detalhe relativo; FP4 exige escalas e calibração. |
| Uso típico | forward, pesos/ativações | gradientes/backward | pesos/ativações quantizados | O papel depende do algoritmo e do runtime. |
| Escalas | por tensor ou blocos, conforme variante | por tensor ou blocos | granulares; NVFP4 usa FP8 por bloco e FP32 por tensor | Escalas ocupam memória e reduzem o ganho teórico. |
| Risco de degradação | baixo a moderado | dependente da distribuição | maior sem calibração; menor com NVFP4/microscaling | Medir no dataset dourado. |
| Hardware | Hopper e posteriores, conforme operação | Hopper e posteriores, conforme operação | Blackwell nativo; AMD CDNA4 para HIP FP4; RDNA4 sem aceleração FP4 nativa na documentação consultada | Suporte do formato não garante suporte do modelo. |

## FP4 é quantização?

FP4 é uma representação de 4 bits e pode ser o tipo numérico escolhido durante uma quantização. Entretanto, dizer apenas “o modelo está em FP4” é incompleto. É necessário informar se é FP4 simples, MXFP4, NVFP4, uma variante com escalas por bloco, um checkpoint PTQ, uma receita QAT ou um formato empacotado por um runtime específico.

A quantização é o processo de mapear valores de maior precisão para uma representação menor, definir escalas/zero-points ou escalas flutuantes, calibrar com dados e validar a perda. FP4 é uma família de destino possível dentro desse processo; GGUF Q4_K_M, GPTQ 4-bit, AWQ 4-bit e NF4 também são quantizações de baixa largura, mas não são equivalentes a FP4 E2M1.

## Memória dos pesos

A aproximação inicial é:

```text
memória_elementos = parâmetros × bits / 8
memória_real = memória_elementos + escalas + metadados + padding + buffers do runtime
```

Para um modelo denso de 8B, os pisos elementares são aproximadamente 8 GB em FP8 e 4 GB em FP4. Para 27B, são 27 GB em FP8 e 13,5 GB em FP4. Para 70B, são 70 GB em FP8 e 35 GB em FP4. Esses números não incluem KV cache, que depende de camadas, dimensão de atenção, tipo KV, contexto e concorrência.

| Modelo | FP16 | FP8 elementar | FP4 elementar | Interpretação |
|---|---:|---:|---:|---|
| 8B | 16 GB | 8 GB | 4 GB | 12–16 GB de VRAM costuma dar margem melhor que o piso. |
| 27B | 54 GB | 27 GB | 13,5 GB | 16 GB pode ser apertado em FP4; 24 GB oferece melhor folga. |
| 70B | 140 GB | 70 GB | 35 GB | 48 GB é uma referência prática para FP4; FP8 normalmente exige 80 GB ou multi-GPU. |

## Variantes que não devem ser confundidas

| Nome | Estrutura | Quando usar | Limite |
|---|---|---|---|
| FP8 E4M3 | FP8 com maior mantissa e menor alcance | Pesos/ativações e forward quando a faixa é controlada | Pode saturar valores fora do alcance. |
| FP8 E5M2 | FP8 com maior alcance e menor mantissa | Gradientes/backward em treinamento misto | Menor precisão relativa. |
| MXFP8 | FP8 E4M3 com escala E8M0 por bloco de 32 | Blackwell e receitas de microscaling | Exige suporte do kernel e do formato do checkpoint. |
| FP4 E2M1 | Tipo de 4 bits simples | Armazenamento/experimentos com forte compressão | Grande erro sem escalas adequadas. |
| MXFP4 | E2M1 com escala E8M0 por bloco de 32 | Blackwell com hardware de microscaling | E8M0 é mais grosseiro que escala FP8 fracionária. |
| NVFP4 | E2M1, escala FP8 E4M3 por 16 e FP32 por tensor | Inferência e treinamento em Blackwell | Não é portável para qualquer GPU/runtime. |
| NF4 | Código normalizado de 4 bits, não FP4 | QLoRA e fine-tuning com bitsandbytes | Não deve ser rotulado como NVFP4/MXFP4. |
| Q4_K_M/GGUF | Quantização empacotada com grupos/escalas | llama.cpp/Ollama/CPU/GPU ampla | O “Q4” não significa FP4 E2M1. |

## Hardware e runtimes

A NVIDIA documenta FP8 nativo no H100 e NVFP4/MXFP8 no Blackwell; Blackwell oferece Tensor Cores com FP4, FP6, FP8 e outros formatos [1] [2]. Na prática, o ganho máximo depende de TensorRT-LLM, vLLM, Transformer Engine, TensorRT Model Optimizer ou outro runtime que implemente o caminho específico.

A documentação HIP consultada descreve FP4 E2M1 e informa aceleração nativa para CDNA4, mas não para CDNA1–3, RDNA2, RDNA3 ou RDNA4 na tabela consultada [3]. Isso significa que uma Radeon de consumo pode armazenar uma quantização de 4 bits e ainda assim executar os kernels em outro caminho, sem obter aceleração FP4 nativa.

No Apple Silicon, Metal/MLX possui seus próprios formatos e kernels. Não se deve inferir suporte a NVFP4 ou MXFP4 a partir do fato de a máquina ter memória unificada. Para Apple, registrar o formato realmente aceito pelo MLX/llama.cpp e a medição com o backend Metal.

## Inferência: quando escolher

Escolha FP8 quando a GPU tem suporte nativo, o modelo tem checkpoint FP8 confiável, a avaliação de qualidade mostra perda aceitável e você precisa de mais margem numérica que FP4. FP8 é particularmente atraente para serving em H100/H200/Blackwell e para pipelines em que o mesmo modelo será usado em múltiplos contextos.

Escolha FP4 quando a limitação dominante é memória ou quando o hardware tem aceleração nativa e o runtime está otimizado para ela. Em Blackwell, NVFP4 pode reduzir a memória e aumentar throughput, mas o ganho deve ser validado no modelo específico. Para GPUs sem aceleração FP4, GGUF Q4, AWQ, GPTQ ou outra quantização suportada pelo runtime pode ser uma escolha mais portátil.

Não escolha pelo nome “4-bit” ou “8-bit” sozinho. Verifique a qualidade no dataset dourado, o contexto máximo, a compatibilidade de tool calling, a taxa de falhas JSON, o uso de KV cache, o throughput sob concorrência e o custo de desquantização/requantização.

## Treinamento e fine-tuning

FP8 é mais maduro para treinamento misto porque o formato pode ser usado no forward e backward com receitas de escala, histórico de amax e loss scaling apropriados. FP4 exige uma receita mais especializada. A documentação do Transformer Engine descreve NVFP4 com stochastic rounding, escala 2D para pesos, transformações de Hadamard e preservação de camadas sensíveis em maior precisão [2].

Para QLoRA, NF4 continua sendo uma escolha distinta: ele reduz os pesos congelados enquanto adaptadores LoRA permanecem treináveis, normalmente com computação em BF16/FP16. Não substitua NF4 por FP4 NVFP4 sem confirmar a biblioteca e a receita de treinamento.

## Protocolo de avaliação

Para cada par modelo/formato, fixe o mesmo prompt set, contexto, temperatura, seed quando suportado, runtime, driver e número de repetições. Registre perplexidade quando houver corpus apropriado, exatidão, pass@k para código, groundedness e citation correctness para RAG, taxa de JSON válido para tool calling, TTFT, P50/P95, tokens/s, VRAM, RAM, energia e temperatura.

O comparativo deve conter duas colunas de evidência: `suporte_de_hardware` e `tokens_s_medido`. “FP4 suportado” é um fato de compatibilidade; “FP4 é 1,8× mais rápido” só é válido para o modelo, kernel, batch e configuração medidos.

## Referências

[1]: https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/ "NVIDIA — Introducing NVFP4"
[2]: https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html "NVIDIA Transformer Engine — Using FP8 and FP4"
[3]: https://rocm.docs.amd.com/projects/HIP/en/latest/reference/low_fp_types.html "AMD ROCm HIP — Low precision floating point types"
[4]: https://arxiv.org/abs/2209.05433 "FP8 Formats for Deep Learning"
[5]: https://github.com/ml-explore/mlx "MLX — Apple machine learning framework"
[6]: https://github.com/ggml-org/llama.cpp "llama.cpp — quantização e inferência"
