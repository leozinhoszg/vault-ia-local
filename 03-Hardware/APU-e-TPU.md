# APU e TPU — capítulo completo

## 1. Por que faltavam

CPU, GPU e NPU não cobrem toda a arquitetura de hardware para IA local. **APU** descreve uma integração de CPU e GPU no mesmo pacote/SoC, frequentemente com memória compartilhada; **TPU** é um acelerador especializado de Google para operações de machine learning, usado principalmente via Google Cloud. São categorias diferentes: APU é uma organização de sistema; TPU é um ASIC/acelerador e ecossistema de compilação.

## 2. APU

Uma APU combina núcleos de CPU e GPU integrada. Em uma APU tradicional, CPU e GPU compartilham RAM e a GPU não possui VRAM dedicada. Em APUs modernas de memória unificada, a capacidade total pode ser muito maior que a VRAM de uma GPU de desktop, mas CPU, GPU e sistema disputam o mesmo pool.

O AMD Ryzen AI Max+ 395 com Radeon 8060S é um exemplo relevante. A AMD descreve até 128 GB de memória unificada e até 112 GB alocáveis pela GPU em um artigo técnico; um guia ROCm reproduzível usa 128 GB LPDDR5X, 64 GB configuráveis para GPU, Ubuntu 24.04 e ROCm 7.2.1 [1] [2]. Isso torna possível executar modelos grandes em uma única máquina, mas **capacidade não é velocidade**: quando parte dos pesos fica em CPU ou a banda da memória é compartilhada, o decode pode cair significativamente.

| APU/UMA | Vantagem | Limitação |
|---|---|---|
| Ryzen AI Max/Strix Halo | Grande pool unificado e GPU integrada forte | ROCm/driver/SO, banda menor que HBM/GDDR e memória compartilhada. |
| Apple Silicon | Memória unificada, Metal/MLX, baixo atrito no macOS | Não usa CUDA; memória não é expansível; suporte varia por modelo. |
| Intel Core Ultra | CPU, GPU integrada e NPU no mesmo pacote | NPU/GPU dependem de OpenVINO/Windows/Linux e operadores suportados. |
| APU básica | Baixo consumo e custo | Pouca banda e capacidade; adequada a modelos pequenos. |

### Como dimensionar APU

A memória total não deve ser atribuída integralmente ao modelo. Reserve sistema operacional, desktop, embedding model, banco vetorial, cache e aplicações. Em uma APU de 128 GB, 64–96 GB utilizáveis pelo acelerador pode permitir Q4 de modelos de dezenas ou mais de 100B, mas contexto, runtime e offload determinam a execução. Use `rocm-smi`, `free -h`, `ollama ps` e benchmark real.

### Quando escolher APU

Escolha APU/UMA quando a prioridade for **capacidade de memória em uma caixa pequena**, eficiência, silêncio ou não comprar múltiplas GPUs. É interessante para 9B–35B com boa experiência e para modelos maiores com velocidade moderada. Não escolha esperando a mesma taxa de tokens de uma GPU discreta com grande banda.

## 3. TPU

TPU significa Tensor Processing Unit. A documentação do Google define Cloud TPU como ASIC específico para acelerar machine learning, com unidades de multiplicação matricial organizadas em systolic arrays e memória HBM [3]. O código é compilado pelo XLA; frameworks como JAX e PyTorch podem usar TPU quando o grafo e as operações são suportados [4].

TPU não é uma peça doméstica que se instala em PCIe como uma GPU de consumo. O caminho usual é Compute Engine, TPU VM, GKE ou Vertex AI. Há host Linux, topologias single-host/multi-host, inter-chip interconnect e slices. O custo deve incluir alocação, armazenamento, rede e tempo ocioso.

| Característica | GPU | TPU |
|---|---|---|
| Flexibilidade | Alta, muitos kernels e softwares | Menor, exige XLA e operações compatíveis. |
| Melhor uso | Inferência variada, visão, LLM local, operações customizadas | Treino/inferência matricial em escala, batch alto e grafos estáveis. |
| Memória | VRAM/HBM, formatos variados | HBM integrada ao sistema TPU. |
| Programação | CUDA/HIP/Metal/Vulkan/OpenVINO | XLA, JAX, PyTorch/XLA e APIs Google. |
| Acesso doméstico | Possível com GPU/APU | Geralmente não; serviço de nuvem. |
| Formas dinâmicas/branching | Geralmente mais tolerante | Podem causar recompilação, padding ou baixa utilização. |

### Quando escolher TPU

TPU é atraente para treinamento longo, modelos dominados por multiplicações matriciais, batches grandes e embeddings de escala. A documentação oficial recomenda GPU quando há muitas operações PyTorch/JAX customizadas ou operadores não suportados; recomenda TPU quando o workload é matricial, estável e grande [4]. Não é a primeira escolha para um agente local com muitas chamadas pequenas, comandos, branching e operações heterogêneas.

### Interconexão e escala

TPU chips formam slices conectados por ICI; multislice usa também a rede de data center. O paralelismo exige particionamento, shapes adequados, padding e compilação. O primeiro batch pode incluir custo de compilação. Use topologia, número de chips, HBM, batch e shape como parte do experimento.

## 4. APU, NPU e TPU não são sinônimos

A GPU integrada de uma APU pode executar kernels gerais; a NPU é otimizada para inferência eficiente e contínua em modelos compatíveis; a TPU é um acelerador especializado de data center/cloud. Um PC pode ter CPU+GPU+NPU em uma APU/SoC, mas isso não transforma o computador em TPU.

## 5. Checklist de compra ou nuvem

Para APU, verifique memória total, memória máxima alocável à GPU, largura de banda, suporte do runtime, ROCm/Metal/OpenVINO, resfriamento e possibilidade de upgrade. Para TPU, verifique versão, HBM, chips, topologia, XLA/PyTorch/JAX, operações suportadas, tempo de compilação, preço por hora, região e quota.

## Referências

[1]: https://www.amd.com/en/developer/resources/technical-articles/2025/amd-ryzen-ai-max-395--a-leap-forward-in-generative-ai-performanc.html "AMD Ryzen AI Max+ 395 — memória unificada e IA generativa"
[2]: https://rocm.blogs.amd.com/artificial-intelligence/ryzen-uma-llm/README.html "AMD ROCm — inferência em Ryzen AI Max com 128 GB UMA"
[3]: https://docs.cloud.google.com/tpu/docs/system-architecture-tpu-vm "Google Cloud — TPU architecture"
[4]: https://docs.cloud.google.com/tpu/docs/intro-to-tpu "Google Cloud — Introduction to Cloud TPU"
