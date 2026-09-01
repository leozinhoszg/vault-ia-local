# LLM e inferência

Um LLM é uma rede neural que estima a distribuição do próximo token. O texto é dividido em tokens; o modelo produz logits; uma estratégia de amostragem escolhe o próximo token; o processo se repete. **Prefill** processa a entrada inicial e é dominado por operações matriciais. **Decode** gera um token por vez e tende a ser limitado por leitura de pesos e KV cache.

A latência percebida é separada em TTFT (time to first token) e velocidade de geração. Throughput pode ser tokens/segundo por usuário ou tokens/segundo agregado. Em aplicações interativas, TTFT, estabilidade e qualidade importam tanto quanto o pico de tokens/s.

## Vocabulário

| Termo | Significado operacional |
|---|---|
| Dense | Cada token usa praticamente todos os parâmetros do bloco. |
| MoE | Mixture of Experts; somente alguns experts são ativados por token, mas todos os pesos precisam estar disponíveis. |
| Context window | Número máximo de tokens de entrada mais saída suportado pelo modelo/runtime. |
| KV cache | Chaves e valores de atenção armazenados para não recalcular o histórico. |
| Quantização | Representação com menos bits, geralmente com escalas por tensor, canal ou bloco. |
| GGUF | Formato usado pelo ecossistema llama.cpp, com metadados e tensores quantizados. |
| Adapter/LoRA | Pequeno conjunto de pesos treinado sobre um modelo congelado. |

## Regra prática

Não compare apenas parâmetros totais. Para MoE, registre **parâmetros totais, parâmetros ativos, número de experts, contexto nativo e formato do checkpoint**. Veja [[02-Modelos/Como-ler-um-model-card]].

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://ai.meta.com/blog/llama-4-multimodal-intelligence/ "Meta: The Llama 4 herd"
[2]: https://github.com/ggml-org/llama.cpp "llama.cpp: LLM inference in C/C++"
