# Por que VRAM, RAM e CPU importam — e o que cada uma não compra

> **Pergunta que esta nota responde.** Por que ter mais VRAM? Por que mais RAM importa? Por que mais CPU importa? Para cada peça: o que ela faz na IA local, o que acontece quando falta, o que "mais" compra e o que "mais" **não** compra. Sem isso, é fácil gastar no lugar errado.

## 0. A regra que organiza tudo

Em inferência de LLM, **memória limita antes da computação** ([[00-Inicio/MAPA]]). O modelo precisa caber; depois, a cada token gerado, os pesos inteiros são lidos da memória. Logo:

- **Capacidade** (GB) decide **qual** modelo você roda.
- **Largura de banda** (GB/s) decide **quão rápido** ele gera.
- **Computação** (FLOPs, núcleos) decide pouco no decode e mais no prefill e nas tarefas auxiliares.

Os dois primeiros eixos são independentes: uma máquina de 128 GB a 273 GB/s carrega um 70B que uma RTX 5090 de 32 GB não carrega, e a 5090 gera um 27B várias vezes mais rápido ([[03-Hardware/Comparativo-workstations-vs-GPU]]).

## 1. Por que ter mais VRAM

**O que ela faz.** Guarda os pesos e o KV cache das camadas que rodam na GPU, e entrega esses bytes à GPU com banda muito alta (centenas de GB/s a mais de 1 TB/s nas placas de referência do vault).

**O que acontece quando falta.** O runtime deixa parte das camadas na RAM (offload) ou recusa carregar. Com offload, cada token passa a depender da CPU e da banda da RAM, e a velocidade despenca ([[01-Fundamentos/Carregar-um-peso]]). Com contexto grande, o KV cache estoura no meio de uma resposta.

**O que mais VRAM compra:**

| Ganho | Exemplo |
|---|---|
| Modelo maior inteiro na GPU | 8 GB: 4–9B em Q4; 16 GB: 14B; 24 GB: 27B ([[03-Hardware/Sizing-9B-14B-27B-70B]]) |
| Quantização mais fiel para o mesmo modelo | Q8 ou FP16 em vez de Q4 |
| Contexto maior | Cada 8K de contexto em um 8B típico custa ~1 GiB de KV FP16 ([[05-Memoria-e-Performance/KV-cache-formula-e-exemplos]]) |
| Mais sessões simultâneas | Cada usuário tem seu KV cache |
| Modelo de embedding ou reranker na GPU ao lado do gerador | RAG mais rápido |

**O que mais VRAM não compra:**

- **Velocidade, se o modelo já cabia.** Tokens/s dependem da banda, não da capacidade. Uma placa de 24 GB com a mesma banda de uma de 16 GB gera um 8B na mesma velocidade.
- **Qualidade além do modelo.** Rodar o mesmo Q4 em uma placa maior dá a mesma resposta.
- **Um 70B em uma placa só.** 70B em Q4 pede ~38–48 GB; não existe GPU doméstica com isso. Entra-se em multi-GPU, memória unificada ou offload ([[08-Implementacao-Empresa/03-Paralelismo-e-multi-GPU]]).

O vault registra a prioridade de compra assim: "16 GB é mais útil que uma GPU rápida com 8 GB" ([[03-Hardware/Builds-brasileiros-por-orcamento]]).

## 2. Por que mais RAM importa

**O que ela faz.** Recebe o arquivo do modelo durante a carga; hospeda as camadas que não couberam na VRAM; sustenta o resto do sistema (sistema operacional, navegador, o pipeline de RAG com modelo de embedding, banco vetorial e parser de PDF); e, sem GPU, é a única memória do modelo.

**O que acontece quando falta.** A carga fica lenta ou o sistema pagina para o SSD (swap), tornando tudo dezenas de vezes mais lento; o pipeline de RAG compete com o modelo; sem GPU, o modelo simplesmente não abre.

**O que mais RAM compra:**

| Ganho | Exemplo |
|---|---|
| Rodar sem GPU | 32 GB rodam 8–9B em Q4 com boa experiência; 14B com paciência ([[03-Hardware/Sizing-9B-14B-27B-70B]]) |
| Offload de modelos maiores que a VRAM | 27B em Q4 em uma GPU de 8–12 GB, aceitando baixa velocidade |
| Carga mais rápida e repetível | O sistema mantém o arquivo em cache; a segunda carga vem da RAM, não do SSD |
| RAG e ferramentas ao lado do modelo | Embeddings em CPU, Chroma/FAISS, parsers — no vault, o embedding roda em `torch` CPU ([[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]]) |
| Datasets e fine-tuning de adapter | Pré-processamento e checkpoints ([[06-Treinamento-e-Fine-tuning/Fine-tuning-livro]]) |

**O que mais RAM não compra:**

- **Velocidade de GPU.** Se o modelo já cabe na VRAM, a RAM quase não participa do decode.
- **Um offload rápido.** Camadas na RAM rodam na banda da RAM (dezenas de GB/s em DDR5 dual channel, contra centenas na VRAM). Mais RAM permite o offload; não o torna bom.
- **Contexto na GPU.** O KV cache das camadas na GPU vive na VRAM.

Detalhe que importa: a **banda** da RAM depende de canais e frequência. Dois pentes (dual channel) e DDR5 fazem diferença real em CPU-only e em offload ([[03-Hardware/GPU-vs-CPU-vs-NPU]]). Memória unificada (Apple, GB10, APUs) é o caso em que "RAM" e "VRAM" são a mesma coisa e a banda dessa memória vira o limite único ([[03-Hardware/ARM-e-memoria-unificada]]).

## 3. Por que mais CPU importa

**O que ela faz.** Tokeniza e destokeniza; orquestra a carga; executa as camadas que ficaram na RAM (offload) ou o modelo inteiro (CPU-only); roda embeddings, parsers, banco vetorial, reranker e a própria aplicação; e, no prefill em CPU, faz a computação pesada.

**O que acontece quando falta.** Com GPU e modelo inteiro na VRAM: quase nada — a CPU fica ociosa no decode. Sem GPU ou com offload: tokens/s baixos, prefill lento em prompts longos, e o pipeline de RAG (indexação de documentos) demora.

**O que mais CPU compra:**

| Ganho | Quando aparece |
|---|---|
| Prefill mais rápido em CPU-only | Prompts longos e RAG sem GPU |
| Mais tokens/s em CPU-only e offload — **até o teto da banda da RAM** | Depois de certo número de threads, a memória satura e núcleos extras não ajudam |
| Indexação de documentos e embeddings mais rápidos | RAG com muitos PDFs; embedding em `torch` CPU |
| Vários serviços ao lado do modelo | Aplicação, banco vetorial, reranker, testes em sandbox ([[07-Implementacao-Casa/Agentes-e-tool-calling]]) |
| Instruções vetoriais (AVX2/AVX-512/AMX em x86, NEON em ARM) | Kernels do llama.cpp usam essas extensões ([[03-Hardware/GPU-vs-CPU-vs-NPU]]) |

**O que mais CPU não compra:**

- **Velocidade quando a GPU faz o trabalho.** Trocar de CPU não muda tokens/s de um modelo 100% na VRAM.
- **Superar a banda da RAM.** Em CPU-only, dobrar núcleos raramente dobra tokens/s; o gargalo é a leitura dos pesos.
- **Substituir VRAM.** CPU forte com pouca RAM ou sem GPU continua limitada a modelos pequenos.

## 4. E o SSD?

Não gera tokens, mas define quanto tempo a carga leva (arquivos de 3 a 50 GB), quanto espaço você tem para vários modelos e onde ficam índices de RAG e datasets. NVMe é o padrão recomendado nas builds do vault; um HD mecânico transforma cada primeira carga em minutos.

## 5. Tabela de decisão

| Sintoma | Recurso em falta | O que fazer primeiro |
|---|---|---|
| Modelo não carrega ou `ollama ps` mostra parte em CPU | VRAM | Quantização menor, `num_ctx` menor, modelo menor; depois, GPU com mais memória |
| Carrega, mas trava em respostas longas ou contexto grande | VRAM (KV cache) | Reduzir `num_ctx`; quantizar KV se o runtime permitir |
| Muito lento, GPU quase ociosa, CPU a 100% | Offload em curso → VRAM | Ver acima; ou aceitar e trocar por modelo que caiba |
| Sistema inteiro fica lento durante o uso, SSD trabalhando sem parar | RAM (swap) | Fechar aplicações; mais RAM |
| Sem GPU: lento, mas funciona | Banda da RAM + CPU | Dual channel, DDR5, modelo menor; GPU é o próximo passo |
| Indexar PDFs para RAG demora horas | CPU (ou embedding na GPU) | Mais núcleos ou mover embedding para a GPU |
| Primeira carga leva minutos, depois é rápido | SSD | NVMe |

## 6. Ordem de prioridade para gastar (opinião editorial)

Para uso doméstico de LLM: **1º VRAM (capacidade), 2º banda da VRAM, 3º RAM (32 GB é o mínimo confortável; 64 GB se houver offload ou RAG pesado), 4º CPU, 5º SSD NVMe**. Para um pipeline de RAG e agentes com muitos documentos, RAM e CPU sobem uma posição. Para treinamento, veja [[06-Treinamento-e-Fine-tuning/Fine-tuning-livro]]: os requisitos mudam. Builds concretas com preços datados estão em [[03-Hardware/Builds-brasileiros-por-orcamento]] e [[03-Hardware/Matriz-de-hardware]].

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://docs.ollama.com/faq "Ollama — FAQ: `ollama ps` mostra a divisão GPU/CPU do modelo carregado; keep_alive; num_ctx"
[2]: https://docs.ollama.com/gpu "Ollama — suporte a GPU (NVIDIA, AMD ROCm, Apple Metal, Vulkan)"
[3]: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md "llama.cpp — backends de GPU e --n-gpu-layers (offload de camadas)"
[4]: https://www.nvidia.com/pt-br/geforce/graphics-cards/40-series/rtx-4090/ "NVIDIA Brasil — GeForce RTX 4090 (24 GB GDDR6X; banda de referência ~1.008 GB/s)"
[5]: https://www.nvidia.com/pt-br/products/workstations/dgx-spark/ "NVIDIA Brasil — DGX Spark (GB10: 128 GB unificados a 273 GB/s)"
