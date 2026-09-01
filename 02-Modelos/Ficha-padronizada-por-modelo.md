# Ficha padronizada por modelo

## Template obrigatório

| Campo | Valor |
|---|---|
| Nome exato / versão | A preencher |
| Organização / URL | A preencher |
| Data de verificação | AAAA-MM-DD |
| Arquitetura | Dense, MoE, multimodal, etc. |
| Parâmetros totais | A preencher |
| Parâmetros ativos | A preencher ou N/A |
| Camadas / atenção | A preencher |
| Contexto nativo / máximo | A preencher |
| Modalidades | Texto, visão, áudio, código |
| Licença | URL e resumo; validação jurídica separada |
| Formatos | Safetensors, GGUF, AWQ, GPTQ, EXL2 |
| Memória FP16 / Q8 / Q6 / Q5 / Q4 | Peso + overhead medidos |
| KV cache | Fórmula e hiperparâmetros |
| Runtimes | Ollama, llama.cpp, vLLM, SGLang, MLX, etc. |
| Hardware testado | GPU/CPU/APU, VRAM/RAM e SO |
| Velocidade medida | Prefill, decode, TTFT, concorrência |
| Dataset de avaliação | Link/hash e tamanho |
| Tool calling / JSON | Passa, falha ou não testado |
| Segurança | Prompt injection, dados sensíveis e limites |
| Fonte primária | Model card/repositório oficial |
| Fonte editorial | Opcional, claramente rotulada |
| Estado | Não avaliado, piloto, aprovado ou obsoleto |
| Dono da ficha | Pessoa/equipe |
| Próxima revisão | Data |

## Regras

Não preencher parâmetros ativos de um modelo denso como se fossem MoE. Não chamar o tamanho do arquivo de requisito de VRAM. Registrar o arquivo exato, contexto e runtime da medição. Resultados editoriais não substituem benchmark próprio.

## Exemplo — Qwen3.6-27B

O model card oficial registra 27B, arquitetura causal com vision encoder, contexto nativo de 262.144 tokens extensível conforme método, licença Apache-2.0 e compatibilidade com Transformers, vLLM, SGLang e outros runtimes [1]. A ficha de velocidade deve ser preenchida pela equipe com hardware e quantização exatos.

## Exemplo — Kimi K2.6

O model card oficial registra MoE com 1T total, 32B ativos, 61 camadas, 384 experts, 8 routed experts por token, 1 shared expert, contexto de 256K e licença modified-MIT [2]. Não dimensione pelo número ativo: os pesos totais e a implementação de atenção precisam ser considerados.

## Referências

[1]: https://huggingface.co/Qwen/Qwen3.6-27B "Qwen3.6-27B model card"
[2]: https://huggingface.co/moonshotai/Kimi-K2.6 "Kimi K2.6 model card"
