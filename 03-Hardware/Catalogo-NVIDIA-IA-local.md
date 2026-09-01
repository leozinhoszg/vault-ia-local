# Catálogo NVIDIA para IA local — especificações e sizing

<!-- validador: sem-formulas: a planilha homônima é um snapshot tabular estático do catálogo; não contém modelo de cálculo -->

**Data de verificação:** 1º de setembro de 2026. **Objetivo:** comparar capacidade de memória e características de GPU com modelos locais.

## Como interpretar

A primeira restrição para LLM local é a memória disponível, não o número bruto de CUDA cores. O modelo precisa armazenar pesos, escalas, buffers, ativações e KV cache; em MoE, os parâmetros ativos reduzem a computação por token, mas os parâmetros totais continuam relevantes para armazenar os experts.

Os valores de tokens/s não devem ser deduzidos de TFLOPS ou da largura de banda isoladamente. A referência de desempenho deste catálogo usa três níveis: especificação oficial, teto teórico de leitura de pesos e benchmark reproduzível com `llama-bench`/vLLM. Números de benchmark externo só são comparáveis quando modelo, quantização, contexto, batch, runtime, driver e potência estão registrados.

## Matriz principal

| GPU | Arquitetura | VRAM | Banda | Potência máx. (W) | CUDA cores | Modelos viáveis em uma GPU | Classe | Fonte |
|---|---|---:|---:|---:|---:|---|---|---|
| RTX 3060 12GB | Ampere | 12 GB GDDR6 | 360 GB/s | 170 | 3584 | GeForce; consumo moderado | 8B Q4/Q5; 14B Q4 com contexto moderado | TPU/TechPowerUp |
| RTX 3060 Ti | Ampere | 8 GB GDDR6 | 448 GB/s | 200 | 4864 | GeForce; pouca VRAM | 8B Q4/Q5; 14B apenas muito ajustado | TechPowerUp |
| RTX 4060 Ti 16GB | Ada | 16 GB GDDR6 | 288 GB/s | 165 | 4352 | GeForce; eficiente, banda baixa | 8B/14B; 27B Q4 com contexto curto/offload | NVIDIA/TechPowerUp |
| RTX 4070 Super | Ada | 12 GB GDDR6X | 504 GB/s | 220 | 7168 | GeForce; bom equilíbrio | 8B/14B; 27B Q4 apertado | TechPowerUp |
| RTX 4070 Ti Super | Ada | 16 GB GDDR6X | 672 GB/s | 285 | 8448 | GeForce; 16 GB | 8B/14B; 27B Q4 com margem limitada | NVIDIA/TechPowerUp |
| RTX 4080 Super | Ada | 16 GB GDDR6X | 736 GB/s | 320 | 10240 | GeForce; alta velocidade | 8B/14B; 27B Q4 com contexto moderado | TechPowerUp |
| RTX 4090 | Ada | 24 GB GDDR6X | 1,008 GB/s | 450 | 16384 | GeForce; referência de throughput | 8B/14B; 27B/30B Q4; 70B com multi-GPU/offload | NVIDIA/TechPowerUp |
| RTX 3090 | Ampere | 24 GB GDDR6X | 936 GB/s | 350 | 10496 | GeForce usada; boa capacidade/preço | 8B/14B; 27B/30B Q4; 70B com 2+ GPUs | NVIDIA/TechPowerUp |
| RTX 3090 Ti | Ampere | 24 GB GDDR6X | 1,008 GB/s | 450 | 10752 | GeForce usada; consumo alto | 8B/14B; 27B/30B Q4; multi-GPU para 70B | TechPowerUp |
| RTX 5080 | Blackwell | 16 GB GDDR7 | 960 GB/s | 360 | 10752 | GeForce; FP4/Tensor 5ª geração | 8B/14B; 27B Q4 com margem limitada | TechPowerUp/NVIDIA |
| RTX 5090 | Blackwell | 32 GB GDDR7 | 1,792 GB/s | 575 | 21760 | GeForce; FP4/Tensor 5ª geração | 8B/14B; 27B/30B; 70B Q4 com offload/multi-GPU | NVIDIA/TechPowerUp |
| RTX 5000 Ada | Ada | 32 GB GDDR6 ECC | 576 GB/s | 250 | 12800 | Workstation; ECC, dual-slot | 8B/14B; 27B/30B; 70B Q4 apertado | NVIDIA |
| RTX 6000 Ada | Ada | 48 GB GDDR6 ECC | 960 GB/s | 300 | 18176 | Workstation; ECC, 48 GB | 8B–70B Q4 com contexto dimensionado | NVIDIA |
| RTX A6000 | Ampere | 48 GB GDDR6 ECC | 768 GB/s | 300 | 10752 | Workstation usada; ECC | 8B–70B Q4 com contexto dimensionado | TechPowerUp/NVIDIA |
| RTX PRO 6000 Blackwell | Blackwell | 96 GB GDDR7 ECC | Não confirmado na página consultada | 600 | 24064 | Workstation; 96 GB; confirmar ficha regional | 8B–70B Q4/Q8; modelos maiores conforme quantização | NVIDIA |
| A100 80GB | Ampere datacenter | 80 GB HBM2e | 1,935 GB/s | 300 | 6912 | Datacenter; não é placa doméstica | 70B Q4/Q8 e serving; custo/appliance | NVIDIA |
| H100 80GB | Hopper datacenter | 80 GB HBM3 | 3,350 GB/s | 700 | 16896 | Datacenter; SXM/PCIe | 70B e treinamento; infraestrutura especializada | NVIDIA |
| H200 141GB | Hopper datacenter | 141 GB HBM3e | 4,800 GB/s | 700 | N/A | Datacenter; capacidade alta | 70B/405B conforme quantização; não workstation comum | NVIDIA |

> **Cuidado com “potência”.** TBP/TGP é limite ou referência da placa, não consumo médio do sistema. Para TCO, meça tomada, idle, prefill, decode e pico.

## Memória necessária por modelo

| Modelo | Pesos FP16 | Piso Q8 | Piso Q4 | GPU única recomendada | Resultado prático |
|---|---:|---:|---:|---|---|
| 8B dense | 16 GB | 8 GB | 4 GB | 12–16 GB | 8 GB pode funcionar em Q4, mas contexto e sistema reduzem a margem. |
| 14B dense | 28 GB | 14 GB | 7 GB | 16 GB | 12 GB é possível em Q4 com contexto moderado; 16 GB é preferível. |
| 27B dense | 54 GB | 27 GB | 13,5 GB | 24 GB | 16 GB pode funcionar em Q4 apertado; 24 GB é o alvo doméstico. |
| 70B dense | 140 GB | 70 GB | 35 GB | 48–96 GB | 24/32 GB exigem offload ou multi-GPU; 48 GB é o mínimo confortável para Q4 moderado. |
| MoE 80B total/3B ativos | 160 GB | 80 GB | 40 GB | 48–96 GB | Dimensione armazenamento pelos 80B totais; ativos só explicam computação. |
| MoE 1T total/32B ativos | 2 TB | 1 TB | 500 GB | Servidor/appliance | Não trate 32B ativos como requisito de memória; experts totais dominam. |

Os pisos são `parâmetros × bits / 8` e não incluem escalas, metadados, runtime, KV cache ou margem. Use [[03-Hardware/Calculadora-de-memoria]] e [[05-Memoria-e-Performance/KV-cache-formula-e-exemplos]].

## Teto teórico de banda para decode

Uma aproximação otimista para um decode memory-bound é `tokens/s_teórico ≈ banda_bytes_s / bytes_de_pesos`. Em Q4, um modelo de 8B exige aproximadamente 4 GB de pesos; uma RTX 4090 teria teto de cerca de 252 tokens/s e uma RTX 5090 cerca de 448 tokens/s, antes de eficiência do kernel, KV cache, sincronização e outros custos. Esses números são **tetos didáticos**, não medições. O benchmark real deve registrar tokens/s e utilização.

## Classes de escolha

| Objetivo | Escolha NVIDIA | Por que | Fica a desejar quando |
|---|---|---|---|
| Entrada econômica | RTX 3060 12GB ou 4060 Ti 16GB | Roda 8B/14B Q4 e tem consumo controlável | Contexto longo, 27B rápido ou treinamento maior |
| Melhor usada | RTX 3090 24GB | VRAM suficiente para 27–30B Q4 e boa banda | Garantia, calor, fonte e disponibilidade |
| Melhor consumo/velocidade | RTX 4090 24GB | Banda alta e ecossistema CUDA maduro | 70B em uma placa não cabe confortavelmente |
| Maior capacidade consumer | RTX 5090 32GB | 32 GB e banda muito alta, FP4 nativo Blackwell | 70B ainda exige offload/multi-GPU; 575 W |
| Workstation profissional | RTX 6000 Ada 48GB | ECC, 300 W e 48 GB em uma placa | Preço alto e menor disponibilidade |
| Alta capacidade local | RTX PRO 6000 Blackwell 96GB | Grande VRAM e workstation | Custo alto; confirmar banda/potência da SKU regional |
| Datacenter | A100/H100/H200 | HBM, serving e treinamento | Não são compra doméstica; exigem chassis, refrigeração e rede |

## Protocolo de benchmark reproduzível

Para cada GPU, rode o mesmo modelo e arquivo quantizado, por exemplo `llama-bench -m modelo.gguf -p 512,2048,4096 -n 128 -r 5`, e registre prompt processing, generation, TTFT, P50/P95, temperatura, potência na tomada, VRAM, driver, CUDA, runtime e contexto. Para vLLM, registre concorrência, input/output tokens, batch, throughput agregado e latência por requisição.

O resultado deve ser anexado à [[02-Modelos/Ficha-padronizada-por-modelo]] e à [[05-Memoria-e-Performance/Evaliacao-e-regressao-de-modelos]]. Nunca misture benchmark de 7B Q4 com 27B Q4 para concluir que uma GPU é “mais rápida” em geral.

## Referências

[1]: https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/ "NVIDIA GeForce RTX 5090"
[2]: https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/ "NVIDIA GeForce RTX 4090"
[3]: https://www.nvidia.com/en-us/products/workstations/rtx-5000/ "NVIDIA RTX 5000 Ada"
[4]: https://www.nvidia.com/en-us/products/workstations/rtx-6000/ "NVIDIA RTX 6000 Ada"
[5]: https://www.techpowerup.com/gpu-specs/ "TechPowerUp GPU Database — referência secundária de especificações"
[6]: https://github.com/ggerganov/llama.cpp "llama.cpp — llama-bench e backends"
[7]: https://docs.vllm.ai/ "vLLM — serving e benchmarks"
[8]: https://mlcommons.org/benchmarks/client/ "MLPerf Client — benchmark para PCs"
