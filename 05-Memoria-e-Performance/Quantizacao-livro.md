# Quantização — capítulo completo

## 1. Definição

Quantização é a transformação de valores numéricos de uma representação para outra com menos bits, normalmente com escalas, zeros, grupos ou codebooks. O objetivo é reduzir memória, largura de banda e, quando há kernels apropriados, custo computacional. Quantização **não é simplesmente “converter para 4 bits”**: é uma cadeia de escolhas sobre pesos, ativações, KV cache, granularidade, calibração e hardware.

Para um valor real `x`, uma quantização uniforme típica usa `q = round(x/s) + z`, onde `s` é a escala e `z` o zero-point. A reconstrução é `x_hat = s(q-z)`. O erro depende da distribuição, do intervalo e da granularidade. Em LLMs, outliers podem tornar uma escala global ruim; por isso aparecem escalas por tensor, canal, grupo ou bloco.

## 2. FP4 é quantização?

**Sim, em sentido amplo.** FP4 é uma representação de ponto flutuante de 4 bits, portanto uma forma de quantização de baixa precisão. Diferencia-se de INT4 porque reserva bits para sinal, expoente e mantissa; INT4 representa inteiros e normalmente usa escala/zero-point externos. Há várias codificações FP4, como E2M1, e variantes de implementação não são automaticamente intercambiáveis.

FP4 pode ser usado para pesos, ativações ou ambos. “Suporte a FP4” também pode significar: armazenamento FP4, conversão no kernel, multiplicação Tensor Core em FP4, ou apenas um caminho experimental de runtime. Confirme o hardware, o kernel, o checkpoint e o acumulador.

## 3. Tipos e quando usar

| Tipo | O que reduz | Quando usar | Principal risco |
|---|---|---|---|
| FP16/BF16 | Precisão sem quantização agressiva | Qualidade máxima, treino e baseline | Footprint e custo altos. |
| INT8 | Pesos/ativações para 8 bits | Serving com boa qualidade e suporte amplo | Ganho menor de memória que 4 bits. |
| INT4 | Pesos para 4 bits | Inferência doméstica e modelos grandes | Perda de qualidade, outliers e kernels. |
| FP4/NVFP4 | Pesos/ativações em ponto flutuante de 4 bits | Hardware/runtime com suporte explícito | Não confundir formato do arquivo com execução nativa. |
| NF4 | Pesos quantizados por distribuição normal | QLoRA e fine-tuning de adapters | Não é um formato universal de serving. |
| AWQ | Pesos, calibrados por importância de ativações | Serving GPU com kernels AWQ | Exige checkpoint/runtime compatíveis. |
| GPTQ | Pesos pós-treinados por reconstrução | Inferência GPU em ecossistema GPTQ | Qualidade depende da calibração e versão. |
| GGUF Q4/Q5/Q6 | Pesos em contêiner portátil llama.cpp | CPU, GPU híbrida, Mac e desktop | Nem todo modelo/quantização tem kernels equivalentes. |
| EXL2 | Pesos GPU com bits por camada | ExLlama e máxima utilização de VRAM | Portabilidade menor. |
| KV INT8/FP8/Q4 | Cache de atenção | Contexto longo e alta concorrência | Pode afetar recuperação e raciocínio longo. |

## 4. GGUF e K-quants

GGUF é um contêiner com metadados, tokenizer e tensores para o ecossistema llama.cpp. Q4_K_M, Q5_K_M e Q6_K são escolhas de compromisso: quanto maior a quantidade efetiva de bits, maior o arquivo e normalmente melhor a fidelidade. O sufixo não deve ser comparado apenas pelo número “4”: overhead de escalas, mistura de tipos e implementação importam.

Comece com Q4_K_M quando a memória for a restrição. Suba para Q5_K_M ou Q6_K se a qualidade em código, chamadas de ferramenta e instruções longas estiver insuficiente. Para avaliação, use o mesmo seed, temperatura, contexto e conjunto.

## 5. AWQ, GPTQ, NF4 e EXL2

AWQ tenta proteger pesos importantes observando ativações; GPTQ usa uma reconstrução pós-treinamento para minimizar erro; NF4 foi desenhado para representar pesos durante QLoRA; EXL2 distribui bits de modo mais flexível por camada no ExLlama. Eles são **algoritmos e ecossistemas**, não apenas extensões de arquivo.

Uma quantização de inferência pode ser excelente para geração e inadequada para continuar treinamento. Uma quantização de treino pode economizar VRAM, mas não ser aceita pelo servidor escolhido. A pergunta correta é: “qual representação, em qual runtime, em qual hardware, para qual tarefa?”.

## 6. Calibração e avaliação

Quantização pós-treinamento pode usar dados de calibração representativos. Para coding, inclua funções, arquivos longos, diffs, testes, JSON, tool calls e idiomas utilizados. Meça perplexidade apenas como sinal auxiliar; uma queda pequena pode esconder falha grande em tool calling ou sintaxe.

Use uma matriz de aceitação: qualidade geral, compilação do código gerado, testes passantes, precisão de citações, JSON válido, taxa de chamadas corretas, TTFT, decode tokens/s, VRAM, RAM e energia.

## 7. Regra de decisão

Escolha FP16/BF16 para baseline e treino; NF4 para QLoRA; GGUF para portabilidade; AWQ/GPTQ/FP8/FP4 para serving GPU quando o runtime os suportar; EXL2 para ExLlama; KV quantizado quando contexto/concor­rência forem o gargalo. Sempre mantenha o checkpoint original e uma quantização de rollback.

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://github.com/ggml-org/llama.cpp "llama.cpp e GGUF"
[2]: https://huggingface.co/docs/transformers/en/quantization/bitsandbytes "bitsandbytes e NF4"
[3]: https://huggingface.co/docs/transformers/en/quantization/awq "AWQ"
[4]: https://huggingface.co/docs/transformers/en/quantization/gptq "GPTQ"
[5]: https://github.com/turboderp-org/exllamav2 "ExLlamaV2 e EXL2"
[6]: https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/ "NVIDIA NVFP4"
