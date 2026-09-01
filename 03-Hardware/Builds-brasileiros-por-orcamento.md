# Builds brasileiros por orçamento

## Como interpretar os preços

As faixas abaixo são **orçamentos de planejamento em reais**, com referência de setembro de 2026. Não são cotação nem recomendação de compra irrevogável. No Brasil, preço, estoque, impostos, garantia e câmbio variam muito; registre três cotações e a data antes de fechar. GPU usada exige teste de VRAM, temperatura, ruído, artefatos e procedência.

A prioridade para LLM é: **VRAM/memória efetivamente disponível > largura de banda > suporte do runtime > consumo e refrigeração > FLOPS de pico**. Para uma build de coding, inclua SSD NVMe para modelos e RAM suficiente para offload, conversão e RAG.

## Build A — entrada eficiente: R$ 5.000–7.500

| Componente | Configuração indicativa | Observação |
|---|---|---|
| CPU | Ryzen 5 7600 ou Core i5 recente, 6–8 núcleos | CPU não deve ser o gargalo do RAG e da aplicação. |
| Placa-mãe | B650 ou B760 de fabricante conhecido | Um slot PCIe x16 físico; confira espaço da GPU. |
| RAM | 32 GB DDR5; 2×16 GB | 64 GB é melhor se houver orçamento. |
| GPU | RTX 4060 Ti 16 GB, Radeon equivalente suportada ou usada com 16 GB | 16 GB é mais útil que uma GPU rápida com 8 GB. |
| PSU | 650–750 W, 80 Plus Gold, ATX atual | Use cabo e conector recomendados pelo fabricante. |
| SSD | NVMe 1–2 TB | Reserve espaço para pesos, cache e datasets. |
| Consumo | ~250–450 W no uso de IA, conforme GPU | Meça na tomada; não estime só pelo TDP. |
| Banda | GPU GDDR; CPU depende da DDR5 | Adequada para 7–14B Q4 e RAG local. |
| Modelos viáveis | 8–14B Q4; 27B com offload e paciência | 27B não é “boa performance” nesta faixa. |

## Build B — ponto ideal doméstico: R$ 9.000–15.000

| Componente | Configuração indicativa | Observação |
|---|---|---|
| CPU | Ryzen 7 7700/9700X ou Core i7 equivalente | Mais linhas PCIe e folga para compilação/RAG. |
| Placa-mãe | B650E/X870 ou Z equivalente com bons VRMs | Confirme bifurcação PCIe se planejar duas GPUs. |
| RAM | 64 GB DDR5; 2×32 GB | 96–128 GB é preferível para 70B híbrido. |
| GPU | RTX 3090 24 GB usada em bom estado ou RTX 4090 24 GB | 24 GB atende bem Q4 de 27–30B. |
| PSU | 850–1.000 W Gold; 1.000–1.200 W para 4090 com margem | Dimensione picos e não apenas consumo médio. |
| SSD | NVMe 2 TB Gen4 + backup | Modelos e checkpoints ocupam dezenas de GB. |
| Consumo | ~450–800 W em carga de IA | 3090 pode consumir mais e aquecer; exija fluxo de ar. |
| Banda | RTX 3090 ~936 GB/s; RTX 4090 ~1.008 GB/s, conforme especificações de referência | A banda favorece decode, mas a VRAM continua limitante. |
| Modelos viáveis | 9B, 14B, 27–30B Q4/Q5; 70B com offload lento | Melhor relação doméstica entre custo e capacidade. |

## Build C — workstation avançada: R$ 17.000–30.000

| Componente | Configuração indicativa | Observação |
|---|---|---|
| CPU | Ryzen 9/Threadripper ou Xeon/EPYC conforme PCIe e RAM | Prefira plataforma com muitas linhas PCIe. |
| Placa-mãe | Workstation com 2–3 slots x16 físicos e boa distância | Duas GPUs grossas podem não caber em placas comuns. |
| RAM | 128 GB DDR5/DDR4 ECC quando a plataforma permitir | Fundamental para offload e datasets. |
| GPU | RTX 5090 32 GB; alternativa 2×RTX 3090 24 GB | 5090 possui 32 GB GDDR7; duas 3090 oferecem 48 GB agregados, mas não como uma VRAM única simples. |
| PSU | 1.200–1.600 W Gold/Platinum | Use PSU e cabos próprios para múltiplas GPUs. |
| SSD | 2–4 TB NVMe + storage de backup | Separe sistema, modelos e datasets. |
| Consumo | ~700–1.300 W em carga | Requer gabinete, exaustão, circuito e UPS adequados. |
| Banda | RTX 5090: 32 GB GDDR7 e alta banda; confirme especificação do SKU | O ganho de banda não elimina o limite de memória. |
| Modelos viáveis | 27–32B com folga; 70B Q4 híbrido ou distribuído | 70B integralmente em acelerador ainda exige mais memória. |

## Build D — 70B com boa experiência: R$ 35.000–90.000+

| Componente | Configuração indicativa | Observação |
|---|---|---|
| CPU | Threadripper Pro, EPYC ou Xeon workstation | Muitas linhas PCIe, RAM e estabilidade. |
| Placa-mãe | WRX/EPYC/Xeon com slots e espaçamento adequados | Verifique NUMA e topologia antes de comprar. |
| RAM | 128–256 GB ECC | Para pesos, KV cache, conversão, RAG e múltiplos processos. |
| GPU | 2×RTX 5090 32 GB, 2×RTX 6000/PRO de alta memória ou GPU data center de 48–80 GB | O caminho depende do runtime e do orçamento. |
| PSU | 1.600–2.400 W ou servidor dimensionado pelo fabricante | Circuito elétrico e refrigeração são parte da build. |
| Consumo | ~1–2,5 kW em carga | Calcule energia, ar-condicionado e ruído. |
| Banda | VRAM/HBM e interconexão determinam decode e comunicação | NVLink só ajuda quando GPU e software o suportam. |
| Modelos viáveis | 70B Q4/Q5; 80B quantizado; 118B/MoE com mais memória | Para 70B multiusuário, use serving e benchmark. |

## Compatibilidade física e elétrica

Antes de comprar, confira comprimento e espessura da GPU, conectores, linhas PCIe reais, slot de captura, altura do cooler, fluxo de ar, PSU, disjuntores e UPS. Duas GPUs de 450–600 W podem tornar uma workstation comum inadequada mesmo quando o software funcionaria.

**Referências**

[1]: https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/ "NVIDIA RTX 5090 — 32 GB GDDR7"
[2]: https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/ "NVIDIA RTX 4090 — 24 GB GDDR6X"
[3]: https://github.com/ggml-org/llama.cpp "llama.cpp — CPU+GPU híbrido e backends"
