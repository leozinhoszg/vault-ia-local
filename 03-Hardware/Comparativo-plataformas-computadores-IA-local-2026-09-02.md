# Plataformas de computadores para IA local — comparação 2026

**Data-base:** 2026-09-02. Esta nota complementa as fichas de [[03-Hardware/Workstations/Dell-Pro-Max-GB10]] e o comparativo financeiro de [[09-Servicos-e-Custos/Comparativo-Dell-Pro-Max-vs-PC-128-256GB-2026-09-02]].

## 1. Quais computadores são mais usados

Não existe um único “computador de IA local”. Na prática, os usuários se concentram em quatro famílias. A primeira é o **desktop x86 com uma GPU NVIDIA GeForce**, normalmente RTX 4090, RTX 5090 ou modelos menores. É a opção mais comum para coding, RAG, agentes e geração porque combina VRAM dedicada, CUDA, TensorRT-LLM, vLLM, llama.cpp, Ollama e ampla documentação.

A segunda é a **workstation multi-GPU ou profissional**, usada quando throughput, simultaneidade, VRAM e confiabilidade são mais importantes que tamanho e preço. Ela pode usar duas RTX 5090, uma RTX PRO 6000 Blackwell de 96 GB ou GPUs datacenter. A terceira é o **Apple Silicon**, especialmente Mac mini e Mac Studio, que usa memória unificada e oferece excelente eficiência, baixo ruído e MLX/Metal. A quarta é o grupo de **appliances e mini-PCs de memória alta**, como NVIDIA DGX Spark/Dell Pro Max GB10 e mini-PCs AMD Strix Halo, que priorizam capacidade de memória e formato compacto.

## 2. Comparação de alto nível

| Plataforma | Memória utilizável para o acelerador | Banda aproximada | Melhor uso | Limitação principal |
|---|---:|---:|---|---|
| Desktop RTX 5090 | 32 GB VRAM | 1.792 GB/s | Modelos até 27B–32B, coding, RAG, geração | Modelos 70B precisam de quantização/offload |
| Desktop 2× RTX 5090 | 64 GB VRAM agregada via paralelismo | até 3.584 GB/s agregados, com overhead | Throughput e modelos maiores | Preço, energia, fonte, lanes e sincronização |
| RTX PRO 6000 Blackwell | 96 GB VRAM | cerca de 1,6 TB/s conforme a edição | Workstation profissional e modelos grandes numa GPU | Preço elevado e disponibilidade brasileira |
| Dell Pro Max/DGX Spark GB10 | 128 GB unificados | 273 GB/s | Modelos grandes, MoE e appliance compacto | Banda baixa e software ARM64 mais específico |
| Mac mini M4 | 16–32 GB unificados nas configurações mais comuns | depende da configuração | Modelos pequenos, RAG, STT/TTS e automação | Memória máxima baixa e ausência de CUDA |
| Mac mini M5 Pro | 24–64 GB unificados | 307 GB/s | Modelos médios, coding e RAG silencioso | 64 GB é o limite; sem GPU discreta |
| Mac Studio M4 Max | 36–128 GB unificados, conforme a configuração | dependente do chip | Coding, RAG, mídia e modelos médios/grandes quantizados | Preço e dependência de MLX/Metal |
| Mac Studio M5 Max | 36–128 GB unificados | 460 GB/s | Modelos médios e desenvolvimento profissional | Não é CUDA; 128 GB é configuração cara |
| Mac Studio M5 Ultra | 96–512 GB unificados | 1,2 TB/s | LLMs enormes, múltiplos usuários e experimentação local | Preço inicial brasileiro de R$ 69.999 e ecossistema não-CUDA |
| Mini-PC AMD Ryzen AI/Strix Halo | até 128 GB em alguns modelos | inferior a GPU discreta | Assistentes, embeddings, STT/TTS, modelos pequenos | iGPU compartilha memória e tem menor throughput |
| Servidor H100/H200/B200/RTX PRO Server | 80–192 GB por GPU ou mais | muito alta | Fine-tuning, serving multiusuário e produção | CAPEX, energia, refrigeração e operação |

Os números de memória e banda não são diretamente comparáveis: VRAM dedicada entrega maior largura de banda, enquanto memória unificada aumenta a capacidade de carregar modelos. Para inferência, é necessário considerar o tamanho quantizado dos pesos, KV cache, contexto e concorrência.

## 3. Mac mini M4, M5 e M5 Pro

O Mac mini M4 continua sendo uma boa porta de entrada para IA local quando o objetivo é executar modelos pequenos, embeddings, RAG, transcrição, síntese de voz, Home Assistant e automações. Configurações de 16 GB ou 24/32 GB permitem modelos de 7B–14B com conforto; 32 GB é preferível para contexto maior e múltiplos serviços. O modelo base não deve ser escolhido para 70B.

A página oficial brasileira atualmente apresenta o **Mac mini M6 e o Mac mini M5 Pro**, indicando que o M4 é geração anterior e que a alternativa “M5” relevante na linha atual é o M5 Pro [1]. O M5 Pro tem 24 GB de memória unificada, configuração possível de 48 GB ou 64 GB e 307 GB/s de banda. A página exibe preços de R$ 10.799 a R$ 18.999 para as configurações atuais do Mac mini [1].

| Mac mini | Memória | Banda | Avaliação para IA local |
|---|---:|---:|---|
| M4 base | 16 GB, configurável em algumas variantes | menor que M5 Pro | Bom para 7B–14B, embeddings e automações |
| M4 com mais memória | até 32 GB nas configurações documentadas do vault | suficiente para modelos pequenos/médios | Melhor opção M4 quando encontrado com desconto |
| M5 Pro | 24/48/64 GB | 307 GB/s | Melhor Mac mini para 14B–27B quantizados; 64 GB permite alguns 30B, dependendo do contexto |
| M6 | 16/24/32 GB conforme a página atual | 153–170 GB/s | Sucessor compacto; ainda limitado por memória para LLMs grandes |

O Mac mini tem excelente relação entre silêncio, consumo e tamanho, mas não é uma máquina de treinamento pesado. Ele funciona bem como servidor doméstico de RAG, gateway de ferramentas, nó de embeddings ou assistente pessoal. Para modelos maiores que 27B, a configuração M5 Pro de 64 GB é o teto mais interessante, mas ainda ficará abaixo de Mac Studio e GB10 em capacidade.

## 4. Mac Studio M4 Max e M5 Max/Ultra

O Mac Studio M4 Max existente no vault deve continuar sendo tratado como uma plataforma de memória unificada, sem possibilidade de upgrade posterior. A BOM atual está em estado `draft` porque ainda faltam preço e cotação brasileira datada.

O Mac Studio M5 Max oferece configuração de 36 GB, 48 GB, 64 GB ou 128 GB; a ficha oficial informa 18 núcleos de CPU, 32 ou 40 núcleos de GPU e 460 GB/s de banda na configuração M5 Max [2]. O Mac Studio M5 Ultra começa em 96 GB e pode ser configurado para 256 GB ou 512 GB, com 1,2 TB/s de banda na configuração de 36 núcleos de CPU e 80 núcleos de GPU [2]. A página de especificações mostra preços de referência de R$ 30.999 para M5 Max e R$ 69.999 para M5 Ultra [2].

| Modelo | Preço de referência Apple BR | Memória | Modelos locais plausíveis |
|---|---:|---:|---|
| Mac Studio M4 Max | cotação pendente no vault | 64–128 GB | 27B–70B quantizados, dependendo de MLX/llama.cpp e contexto |
| Mac Studio M5 Max | R$ 30.999 na página de especificações | 36–128 GB | 14B–70B quantizados, com 128 GB sendo a configuração relevante |
| Mac Studio M5 Ultra | R$ 69.999 na página de especificações | 96–512 GB | Modelos muito grandes, MoE e múltiplos serviços; 256/512 GB são os alvos para LLMs enormes |

O M5 Ultra é a alternativa Apple mais próxima de uma workstation de memória alta. Ele não deve ser comparado com uma RTX 5090 apenas por quantidade de memória: a Apple oferece memória unificada, enquanto a RTX oferece VRAM dedicada muito mais rápida e CUDA. O Mac Studio ganha em simplicidade, acústica, consumo e capacidade unificada; o PC NVIDIA ganha em compatibilidade e throughput para modelos que cabem na VRAM.

## 5. Appliances GB10 e sistemas OEM

O NVIDIA DGX Spark usa o GB10, 128 GB de memória coerente unificada e até 1 PFLOP FP4 segundo a NVIDIA [3]. O fabricante declara suporte a modelos de até 200 bilhões de parâmetros em um sistema e conexão de até quatro unidades para modelos de até 700 bilhões, mas esses números descrevem capacidade de memória/posicionamento e não tokens/s garantidos [3]. O Dell Pro Max FCM1253 Micro é uma implementação OEM da mesma classe, com 128 GB, 273 GB/s, ConnectX-7 e formato compacto.

A NVIDIA também posiciona sistemas Blackwell de IA de fabricantes como Acer, ASUS, Dell, HP, Lenovo, MSI e Supermicro [4]. Isso cria uma categoria importante para empresas: o cliente compra suporte, garantia, imagem de software e integração de fornecedor, não apenas componentes. No Brasil, a disponibilidade, o preço e o prazo precisam ser cotados caso a caso; não há motivo para assumir que um SKU internacional esteja disponível localmente.

## 6. Workstations com RTX PRO

A RTX PRO 6000 Blackwell Workstation Edition é o caminho de uma GPU profissional com aproximadamente 96 GB de VRAM e banda próxima de 1,6 TB/s, conforme a edição e a especificação do fabricante. Ela se torna interessante quando um modelo de 70B quantizado precisa caber inteiro em uma única placa, evitando tensor parallelism entre duas GPUs. Também pode ser preferível em ambiente profissional por drivers, suporte OEM e recursos de workstation.

Uma workstation Dell Precision, Lenovo ThinkStation, HP Z ou Supermicro com RTX PRO 6000 deve ser avaliada como appliance corporativo. O custo costuma ser dominado pela GPU, chassi, fonte, refrigeração, garantia e suporte. Sem cotação brasileira confirmada, o vault deve registrar esses sistemas como **opções de arquitetura**, não como BOM com preço.

## 7. PCs comuns com NVIDIA GeForce

O desktop com RTX 5090 é a plataforma de melhor desempenho para o usuário individual quando o modelo-alvo cabe nos 32 GB de VRAM. A comparação financeira do vault encontrou uma build Ryzen 9 9950X + RTX 5090 + 128 GB por cerca de R$ 58 mil, dependendo das ofertas e componentes [5]. Uma RTX 4090 usada ou em promoção pode reduzir o custo, mas seus 24 GB limitam mais cedo os modelos grandes.

Duas RTX 5090 aumentam muito o throughput e podem manter mais pesos em VRAM agregada, mas a memória não se torna automaticamente um pool único: o backend precisa fazer tensor parallelism ou pipeline parallelism. Também são necessários slots PCIe, fonte de pelo menos 1.600 W, gabinete grande, fluxo de ar e atenção a latência entre GPUs.

## 8. PCs AMD, mini-PCs e NPUs

Radeon RX 7900 XTX e RX 9070 XT são alternativas para quem aceita ROCm, Vulkan ou backends comunitários. A RX 7900 XTX com 24 GB pode ser interessante pelo custo, mas a compatibilidade varia com GPU, sistema operacional, kernel e versão ROCm. Para uma experiência previsível em LLM local, NVIDIA continua sendo a opção mais simples.

Mini-PCs AMD Ryzen AI são diferentes de uma workstation com GPU. O Minisforum AI X1 Pro-470, por exemplo, usa Ryzen AI 9 HX 470, Radeon 890M, NPU de 86 TOPS, dois slots SO-DIMM DDR5 e capacidade máxima de 128 GB [6]. Ele é adequado para modelos pequenos, embeddings, agentes leves, STT/TTS e serviços auxiliares, mas a iGPU compartilha memória e não compete com RTX 5090 ou GB10 em modelos grandes.

NPUs Intel, AMD e Apple são úteis para cargas específicas e eficientes, mas TOPS de NPU não são equivalentes a tokens/s de LLM. O usuário deve exigir benchmark do backend, formato de quantização e modelo específico antes de concluir que uma NPU “roda” determinado LLM.

## 9. Recomendação por objetivo

| Objetivo | Plataforma recomendada | Motivo |
|---|---|---|
| Entrada barata e silenciosa | Mac mini M4 usado ou M5 Pro 32/64 GB | Baixo consumo, boa experiência e memória suficiente para modelos pequenos/médios |
| Coding e RAG com maior velocidade | Ryzen 9 9950X + RTX 5090 + 128 GB | CUDA, VRAM rápida e melhor throughput nos modelos até 27B–32B |
| Modelos grandes com 128 GB unificados | Dell Pro Max GB10/DGX Spark | Capacidade de memória em formato compacto; aceitar menor tokens/s |
| Apple profissional e silencioso | Mac Studio M5 Max 128 GB | 128 GB unificados, 460 GB/s e MLX/Core ML |
| LLMs enormes localmente | Mac Studio M5 Ultra 256/512 GB ou workstation RTX PRO 6000/multi-GPU | Capacidade ampla; escolher entre simplicidade Apple e ecossistema CUDA |
| Desenvolvimento corporativo | Dell/Lenovo/HP/Supermicro com RTX PRO ou GB10 | Garantia, suporte, gestão e ciclo de vida |
| Home Assistant, embeddings, voz e serviços auxiliares | Mini-PC AMD/Intel com 32–128 GB | Baixo consumo e suficiente capacidade de CPU/NPU/iGPU |

A conclusão prática é que **RTX 5090 é a escolha dominante em desempenho por real**, **GB10 é a escolha de capacidade compacta e memória unificada**, e **Mac Studio é a escolha de silêncio, integração e grande memória sem montar hardware**. O Mac mini é excelente como nó auxiliar e servidor pessoal, mas deixa de ser competitivo para LLMs grandes quando a configuração de memória se aproxima do preço de um desktop com GPU dedicada.

## Referências

[1]: https://www.apple.com/br/mac-mini/specs/ "Apple Brasil — especificações do Mac mini atual"
[2]: https://www.apple.com/br/mac-studio/specs/ "Apple Brasil — especificações do Mac Studio M5 Max e M5 Ultra"
[3]: https://www.nvidia.com/en-us/products/workstations/dgx-spark/ "NVIDIA — DGX Spark, GB10, 128 GB e capacidade declarada de modelos"
[4]: https://blogs.nvidia.com/blog/local-ai-open-source-models-agents-nemotron/ "NVIDIA — ecossistema de sistemas Blackwell e fabricantes parceiros"
[5]: https://github.com/leozinhoszg/vault-ia-local/blob/main/09-Servicos-e-Custos/Comparativo-Dell-Pro-Max-vs-PC-128-256GB-2026-09-02.md "Vault — comparação financeira Dell Pro Max versus PC local"
[6]: https://store.minisforum.com/products/minisforum-ai-x1-pro-470-mini-pc "Minisforum — AI X1 Pro-470, Ryzen AI 9 HX 470, NPU 86 TOPS e até 128 GB"
