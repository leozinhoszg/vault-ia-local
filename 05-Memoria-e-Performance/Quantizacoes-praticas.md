# Quantizações práticas

## K-quants em GGUF

GGUF é um contêiner usado pelo llama.cpp. Os K-quants, como Q4_K_M, Q5_K_M e Q6_K, usam quantização em blocos com escalas e diferentes compromissos entre tamanho, qualidade e velocidade. Q4_K_M costuma ser o primeiro teste; Q5/Q6 preserva mais qualidade se houver memória.

## AWQ e GPTQ

AWQ e GPTQ são métodos de quantização de pesos populares no ecossistema Transformers/serving. O checkpoint e o kernel precisam ser compatíveis. AWQ pode funcionar bem em serving GPU; GPTQ aparece em muitos repositórios e versões. Não converta entre formatos apenas renomeando arquivo.

## NF4 e QLoRA

NF4 é uma representação de 4 bits usada principalmente para carregar pesos quantizados durante fine-tuning eficiente, especialmente com bitsandbytes/QLoRA. O modelo treinado normalmente produz um adapter LoRA; não confunda NF4 de treino com GGUF Q4 de inferência.

## EXL2

EXL2 é um formato orientado a inferência em GPU no ecossistema ExLlamaV2, permitindo granularidade de bits por camada. É uma boa opção quando o runtime ExLlama é o alvo, mas menos portátil que GGUF.

## KV-cache quantizado

Quantizar o KV cache para INT8, Q8, Q4 ou FP8 reduz memória de contexto e concorrência, mas pode alterar qualidade e depende do runtime/modelo. Faça avaliação de recuperação, tool calling e long-context; não presuma que a mesma qualidade de FP16 será mantida.

| Objetivo | Primeiro formato a testar |
|---|---|
| PC/CPU/GPU híbrida e portabilidade | GGUF Q4_K_M; depois Q5_K_M. |
| Serving NVIDIA com throughput | AWQ/GPTQ/FP8 conforme vLLM/TensorRT-LLM e modelo. |
| Fine-tuning com pouca VRAM | NF4 + LoRA/QLoRA. |
| GPU NVIDIA com ExLlama | EXL2, se houver checkpoint e kernel compatíveis. |
| Blackwell com suporte nativo | FP4/NVFP4, quando o checkpoint e runtime suportarem. |

## Critérios de escolha

Escolha pela combinação de qualidade no seu conjunto de testes, memória máxima, velocidade, suporte ao hardware, licença, facilidade de rollback e possibilidade de exportação. Compare sempre o mesmo modelo base e a mesma janela de contexto.

*Última atualização: 2026-09-01. Próxima revisão: 2026-10-01.*

## Referências

[1]: https://github.com/ggml-org/llama.cpp "GGUF e quantização no llama.cpp"
[2]: https://huggingface.co/docs/transformers/en/quantization/bitsandbytes "bitsandbytes, 8-bit e 4-bit"
[3]: https://github.com/turboderp-org/exllamav2 "ExLlamaV2 e EXL2"
[4]: https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/ "NVIDIA NVFP4"
