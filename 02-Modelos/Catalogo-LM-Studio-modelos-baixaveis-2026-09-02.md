# Catálogo LM Studio — famílias observadas

URL: https://lmstudio.ai/models
Data da consulta: 2026-09-02.

O catálogo oferece filtros GGUF e MLX, ordenação por atualização/data/downloads/estrelas/tamanho e capacidades. A página distingue “Available to download” de “Available in LM Studio Cloud”; nem todo item do catálogo é um download local.

## Famílias e tamanhos observados na página

| Família | Tamanhos/arquitetura observados | Capacidades ou uso destacado |
|---|---|---|
| Qwen3.8 | 27B denso | Visão-linguagem, coding, trabalho profissional e agentes; 262K de contexto |
| Muse Glimmer | 30B | Agentes locais, multimodalidade, tool use e recuperação de falhas |
| DeepSeek V4 Flash | 284B MoE, 13B ativos | Coding, tool use e agentes; download local e Cloud |
| Laguna S 2.1 | 118B MoE, 8B ativos | Coding agentic e tool use; até 1M de contexto |
| Bonsai 27B | 27B, variantes 1-bit/ternárias baseadas em Qwen3.6 | Visão, raciocínio e tools |
| Granite 4.1 | 3B, 8B e 30B | Tool calling, instruction following e chat |
| Nemotron 3 Omni | 30B | Multimodalidade, visão, áudio e linguagem |
| Qwen3.6 | 27B e 35B | Coding |
| Gemma 4 | 5.1B, 7.9B, 12B, 26B e 31B | Visão e implantação local |
| Nemotron 3 Super | 120B MoE, 12B ativos | Raciocínio; até 1M de contexto |
| Qwen3.5 | 2B, 4B, 9B, 27B e 35B | Multimodalidade, raciocínio e acessibilidade |
| LFM2-24B-A2B | 24B, arquitetura híbrida | Inferência eficiente |
| Qwen3-Coder-Next | 80B MoE, 3B ativos | Coding agentic e tool use |
| GLM-4.7 | 30B | Coding e tool calling |
| FunctionGemma | 270M | Function calling especializado |
| Nemotron 3 | 30B MoE, 3,5B ativos | Chat e raciocínio |
| GLM-4.6V-Flash | 9B | Visão-linguagem de baixa latência |
| Devstral 2 | 24B e 123B | Coding agentic e visão |
| Rnj-1 | 8B denso | Uso geral |
| Ministral 3 | 3B, 8B e 14B | Boa relação custo/desempenho |
| Qwen3 Next | 80B MoE, 3B ativos | Arquitetura híbrida e alta esparsidade |
| Olmo 3 | 7B e 32B | Modelos abertos para pesquisa |
| olmOCR 2 | 7B | VLM/OCR |
| minimax-m2 | 230B MoE, 10B ativos | Coding e agentes |
| gpt-oss-safeguard | 20B e 120B | Classificação de segurança; conferir licença no card |
| Qwen3-VL | 2B, 4B, 8B, 30B e 32B | Visão-linguagem |
| Granite 4.0 | 3B, 7B e 32B | Multilíngue, coding, RAG, tool use e JSON |
| seed-oss | 36B | Raciocínio com orçamento configurável |
| Qwen3 | 4B, 30B e 235B | Variantes dense/MoE e thinking/non-thinking |
| gpt-oss | 20B e 120B | Tool use, raciocínio configurável e Apache 2.0 conforme catálogo |
| Qwen3-Coder | 30B e 480B, 3B e 35B ativos respectivamente | Coding e 256K de contexto |
| Ernie-4.5 | 21B MoE | Uso geral |
| LFM2 | 350M, 700M e 1.2B | Edge/on-device |
| Devstral | 23,6B e 24B | Coding agentic |
| gemma-3n | 4,5B e 6,9B | Dispositivos cotidianos |
| Mistral Small | 24B multimodal | Modelo local multimodal; conferir contexto no card |
| Magistral | 23,6B e 24B | Raciocínio; até 128K |
| mistral-nemo | 12B | Uso multilíngue |
| qwen2.5-vl | 3B, 7B, 32B e 72B | Visão-linguagem; até 128K |
| gemma-3 | 270M, 1B, 4B, 12B e 27B | Imagem + texto |
| phi-4-reasoning | 3,8B e 14,7B | Raciocínio leve |

A página foi truncada depois de phi-4-reasoning na coleta desta versão. Portanto, esta é uma **lista de famílias prioritárias observadas**, não uma garantia de inventário exaustivo de todos os modelos do catálogo. A atualização deve ser reexecutada para capturar novas famílias, tamanhos e estados de disponibilidade.

## Ferramentas de obtenção e execução

| Ferramenta | Formatos/artefatos | Melhor uso |
|---|---|---|
| LM Studio | GGUF e MLX no catálogo; runtime baseado em llama.cpp/MLX | Desktop pessoal, descoberta, download, chat e servidor local |
| `lms get` | Modelos do catálogo LM Studio, com filtro MLX | Automação de pesquisa e download no desktop |
| Hugging Face Hub | Pesos originais, GGUF, MLX, GPTQ/AWQ e model cards | Fonte primária e reprodutibilidade |
| Ollama | Modelos empacotados, tags e Modelfile | API local simples, Home Assistant e scripts |
| llama.cpp | GGUF, CLI e servidor local | Controle de offload, contexto e benchmark |
| MLX/MLX-LM | Pesos no formato MLX | Inferência e fine-tuning em Apple Silicon |
| vLLM | Servidor de inferência | Produção, batching e API compatível com OpenAI |
| TensorRT-LLM | Engines otimizadas para NVIDIA | Baixa latência e serving NVIDIA validado |
| ComfyUI | Checkpoints e workflows de difusão | Imagem e vídeo local, inclusive Wan |
| ModelScope | Pesos de repositórios que publicam lá | Alternativa para modelos com distribuição asiática |
| Git LFS/curl/wget | Arquivos de repositórios oficiais | Ambientes sem GUI e pipelines reprodutíveis |
| Bionic | Interface/agente de coding conforme produto | Coding assistido; não é formato universal de pesos |

O download deve preservar model card, licença, revisão/commit e hash. Repositórios de quantização de terceiros podem alterar template, tokenizer ou parâmetros; para ambiente empresarial, preferir pesos originais ou um repositório interno de artefatos aprovado.

## Regras de verificação

“Disponível no catálogo” não significa “cabe na máquina”. Antes de baixar, cruzar tamanho dos pesos, formato, quantização, parâmetros totais/ativos, contexto, KV cache, backend e licença. Antes de executar, deixar margem para runtime, buffers e concorrência. Em MoE, os parâmetros ativos afetam o custo de computação, mas os parâmetros totais continuam afetando armazenamento e memória dos pesos.

Também é necessário distinguir um modelo de chat de um modelo de vídeo. LM Studio é principalmente um catálogo de LLM/VLM. Geração de vídeo normalmente usa ComfyUI e modelos de difusão, como Wan2.1, enquanto compreensão de vídeo usa VLMs, extração de frames e áudio em pipeline separado.

## Referências

[1]: https://lmstudio.ai/models "LM Studio — catálogo público de modelos, formatos GGUF/MLX e disponibilidade para download"
[2]: https://lmstudio.ai/docs/cli/local-models/get "LM Studio — comando lms get para pesquisar e baixar modelos"
[3]: https://huggingface.co/docs/hub/en/models-downloading "Hugging Face — documentação de download de modelos"
[4]: https://ollama.com/library "Ollama — biblioteca pública de modelos e tags"
[5]: https://github.com/ggml-org/llama.cpp "llama.cpp — execução de modelos GGUF"
[6]: https://github.com/ml-explore/mlx-lm "MLX-LM — inferência e fine-tuning para Apple Silicon"
[7]: https://docs.comfy.org/tutorials/video/wan/wan-video "ComfyUI — workflow Wan2.1 para geração local de vídeo"
