# Comparativo: workstations de IA versus PC com RTX 4090/5090

> **Data de verificação:** 2026-09-01. **Estado:** ativo. **Dono:** Luiz Guimarães. **Próxima revisão:** 2026-10-01.

Esta nota responde a duas perguntas para cada máquina candidata: **quais modelos do catálogo rodam nela em modo local real** e **se compensa, em vez dela, montar um PC com RTX 4090 ou 5090**. Cada máquina entra por uma ficha em `03-Hardware/Workstations/` preenchida com [[99-Templates/Modelo-de-ficha-de-workstation]]; os modelos vêm de [[02-Modelos/Catalogo-de-modelos]]; os modos de execução (1 local real, 2 offload, 3 remoto, 4 Ollama Cloud) são os de [[02-Modelos/Local-real-vs-cloud]].

## 1. Os cinco eixos de comparação

| Eixo | O que mede | Por que importa |
|---|---|---|
| Memória do acelerador | GB efetivamente utilizáveis pelo modelo (VRAM dedicada ou memória unificada menos SO/RAG) | Decide **o que cabe** em modo 1: pesos + KV cache + folga ([[03-Hardware/Calculadora-de-memoria]]) |
| Largura de banda | GB/s entre memória e acelerador | Decide **quantos tokens/s** em modelo denso: cada token lê os pesos ativos inteiros ([[05-Memoria-e-Performance/Inferencia-livro]]) |
| Ecossistema | CUDA x86, CUDA aarch64, Metal/MLX, ROCm | Decide quais runtimes, formatos (NVFP4, AWQ, GGUF) e ferramentas de fine-tuning existem ([[04-Software/Compatibilidade-por-stack]]) |
| Consumo | W em carga e em idle | Entra no TCO e define fonte, circuito, ruído e refrigeração |
| Preço datado | R$ à vista, vendedor, URL e data | Sem isso, a comparação é opinião ([[03-Hardware/BOM-brasileira-datada]]) |

Regra de leitura: **capacidade e velocidade são eixos independentes.** Uma máquina com 128 GB e 273 GB/s carrega um 70B que uma RTX 5090 não carrega, e a 5090 gera um 27B seis vezes mais rápido. Nenhuma das duas "ganha" sem antes fixar a classe de modelo alvo.

## 2. Máquinas comparadas

| Máquina | Memória do acelerador | Banda | RAM do sistema | Consumo em carga | Preço datado (2026-09-01) | Stack |
|---|---:|---:|---:|---:|---|---|
| PC com RTX 4090 (Build B) | 24 GB GDDR6X | ~1.008 GB/s [1] | 64 GB DDR5 | ~450–800 W; TGP 450 W [1] | R$ 9.000–15.000 a build, faixa de [[03-Hardware/Builds-brasileiros-por-orcamento]]; GPU nova ou usada | CUDA x86 |
| PC com RTX 5090 (Build C) | 32 GB GDDR7 | ~1.792 GB/s (28 Gbps × 512 bits) [2] | 128 GB DDR5 | ~700–1.300 W; TGP 575 W, fonte ≥ 850 W [2] | R$ 17.000–30.000 a build, mesma faixa | CUDA x86 |
| PC com 2× RTX 5090 (Build D reduzida) | 64 GB agregados por sharding, não como VRAM única | 2× 1.792 GB/s, limitados por PCIe entre GPUs | 128–256 GB | ~1,2–1,6 kW | R$ 35.000+; Build D em [[03-Hardware/Builds-brasileiros-por-orcamento]] | CUDA x86; TP/PP em [[08-Implementacao-Empresa/03-Paralelismo-e-multi-GPU]] |
| Dell Pro Max com GB10 / DGX Spark | 128 GB LPDDR5x unificados | 273 GB/s [3][4] | A mesma memória | 240–280 W [3][4] | Dell sem preço on-line; DGX Spark 4 TB a R$ 54.552 à vista em revendedor [5] | CUDA **aarch64**, DGX OS, NVFP4 nativo |
| Mac Studio M5 Max 128 GB | 128 GB unificados | até 614 GB/s [6] | A mesma memória | Baixo; não publicado por carga | "Confira em breve a disponibilidade" na Apple Brasil em 2026-09-01 [6] | Metal/MLX, sem CUDA |
| Mac Studio M5 Ultra 256 GB | 256 GB unificados | até 1,2 TB/s [6] | A mesma memória | Baixo; não publicado por carga | Idem | Metal/MLX, sem CUDA |

Fichas individuais: [[03-Hardware/Workstations/Dell-Pro-Max-GB10]]; Macs em [[03-Hardware/Mac-Studio-e-IA-local]]; builds x86 em [[03-Hardware/Builds-brasileiros-por-orcamento]]. As faixas de preço das builds são planejamento; a cotação do DGX Spark é uma única loja em um único dia.

## 3. Matriz modelo × máquina (modo de execução)

Tamanhos de arquivo conforme [[02-Modelos/Catalogo-de-modelos]], [[02-Modelos/LLMs-locais-para-coding-Atomic]] e fichas. "1" exige pesos + KV cache de contexto moderado + folga dentro da memória do acelerador; "1 justo" cabe com contexto ≤ 32K e pouca margem; "2" é offload para RAM com queda forte de velocidade; "3/4" é remoto.

| Modelo (arquivo Q4/NVFP4) | RTX 4090 24 GB | RTX 5090 32 GB | 2× RTX 5090 64 GB | GB10 128 GB | M5 Max 128 GB | M5 Ultra 256 GB |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Gemma 4 26B A4B (~12–18 GB) | 1 | 1 | 1 | 1 | 1 | 1 |
| Qwen3.6-27B dense (~17–18 GB) | 1 justo em contexto longo | 1 | 1 | 1 | 1 | 1 |
| Laguna XS 2.1 33B/3B (20,3 GB) | 1 justo | 1 | 1 | 1 | 1 com aviso Metal | 1 com aviso Metal |
| Qwen3-Coder 30B-A3B (~22 GB) | 1 justo | 1 | 1 | 1 | 1 | 1 |
| Qwen3-Coder-Next 80B/3B (~45 GB) | 2 | 2 | 1 (TP=2) | 1 | 1 | 1 |
| Llama 3.1 70B dense (38–48 GB) | 2 | 2 | 1 justo | 1 | 1 | 1 |
| Llama 4 Scout 109B/17B (~55–60 GB Int4) | 2 | 2 | 1 justo | 1 | 1 | 1 |
| Laguna S 2.1 118B/8B (67 GB NVFP4; 96 GB Q4) | 2 | 2 | 2 (67 > 64) | 1 | 1 justo (Q4) | 1 |
| Qwen3.8-Flash-Next 125B/6B (~65–75 GB est.) | 2 | 2 | 2 | 1 | 1 | 1 |
| Kimi K2.7 Code 1T/32B (≥ 304 GB) | 3/4 | 3/4 | 3/4 | 3/4 | 3/4 | 3/4 |

Leituras diretas da matriz:

- Até a classe **27–30B**, todas as máquinas estão em modo 1; a diferença é só velocidade e preço.
- A classe **70B denso e MoE de 80–125B totais** é o que separa as máquinas: PC de uma GPU cai para modo 2; duas 5090 resolvem parte; 128 GB unificados resolvem tudo.
- **Nenhuma** das seis executa Kimi K2.7 Code; a ficha [[02-Modelos/Fichas/Kimi-K2.7-Code]] continua válida.

## 4. Teto de decode por banda

Em modelo denso, cada token gerado lê todos os pesos; em MoE, lê os experts ativos mais embeddings e camadas compartilhadas. O teto por sessão é:

`tok/s_teto ≈ banda_GB/s ÷ GB_lidos_por_token`

Os valores abaixo são **triagem, não benchmark**: o medido costuma ficar em 50–70% do teto por overhead de kernel, KV cache e atenção, e MoE pequeno bate primeiro no limite de computação. O vault só publica tokens/s medidos com modelo, contexto, runtime e versão ([[05-Memoria-e-Performance/Benchmarking]]).

| Máquina (banda) | Qwen3.6-27B Q4 (~17 GB/token) | Llama 70B Q4 (~42 GB/token) | MoE 3B ativos (~2,5 GB/token) | Laguna S 2.1, 8B ativos (~5 GB/token) |
|---|---:|---:|---:|---:|
| RTX 4090 (1.008 GB/s) | ~59 | modo 2 | > 400 (limite de computação antes) | modo 2 |
| RTX 5090 (1.792 GB/s) | ~105 | modo 2 | > 700 (idem) | modo 2 |
| 2× RTX 5090 | ~105 por GPU | ~40, menos a comunicação PCIe | > 700 | modo 2 |
| GB10 (273 GB/s) | ~16 | ~6,5 | ~110 | ~55 |
| M5 Max 128 GB (614 GB/s) | ~36 | ~15 | ~245 | ~120 |
| M5 Ultra 256 GB (1.200 GB/s) | ~70 | ~29 | ~480 | ~240 |

Sanidade: a Atomic mediu 220 tok/s no Qwen3-Coder 30B em uma GPU de 24 GB [7] — abaixo do teto de banda, como esperado para MoE pequeno, e coerente com a tabela.

## 5. Compensa comprar um PC com 4090/5090?

A resposta depende só da **classe de modelo alvo**. Regras de decisão, na ordem em que devem ser aplicadas:

1. **Alvo até 30B (a faixa que o guia de coding recomenda para uma GPU de 24 GB [7]).** O PC com RTX 5090 é a melhor compra: 4–6× a banda do GB10, 3× a do M5 Max, metade ou um terço do preço cotado do DGX Spark, ecossistema CUDA x86 completo. Uma 4090 usada e testada faz o mesmo com 24 GB e margem menor para contexto longo. Workstation de 128 GB aqui é dinheiro em capacidade que não será usada.
2. **Alvo é 70B denso em modo 1, numa caixa só.** O PC de uma GPU sai da disputa (modo 2, lento). Restam 2× 5090 (R$ 35 mil+, ~1,5 kW, ~40 tok/s de teto), GB10 (~R$ 54,5 mil na cotação, 280 W, ~6,5 tok/s) e Mac 128/256 GB (silencioso, ~15–29 tok/s). Se velocidade importa, duas 5090; se energia, silêncio e simplicidade importam, Mac ou GB10 — sabendo que 70B denso nessas duas é "roda", não "boa performance", na terminologia de [[03-Hardware/Sizing-9B-14B-27B-70B]].
3. **Alvo é MoE grande com poucos ativos (Qwen3-Coder-Next 80B, Laguna S 2.1, Qwen3.8-Flash-Next).** É o nicho onde 128 GB unificados vencem: modo 1 com decode aceitável (banda deixa de limitar quando só 3–8B são lidos por token), enquanto o PC precisa de duas 5090 e ainda assim não carrega Laguna S NVFP4 (67 GB > 64 GB). Entre GB10 e Mac, o GB10 tem CUDA e NVFP4 nativo; o Mac tem 2,2–4,4× a banda e a página do Laguna XS no Ollama ainda adverte sobre saída vazia em Metal ([[02-Modelos/Fichas/Laguna-XS-2.1]]).
4. **Fine-tuning.** QLoRA até ~14B: PC CUDA, com bitsandbytes e Unsloth maduros em x86. QLoRA de 27B–70B: só o GB10 combina CUDA com 128 GB nesta lista, sujeito à disponibilidade das bibliotecas em aarch64; Mac exige o caminho MLX ([[06-Treinamento-e-Fine-tuning/01-QLoRA-pratico]]).
5. **Serving multiusuário.** Nenhuma das seis é um servidor; 273 GB/s limitam o throughput agregado do GB10 e a VRAM limita a concorrência da 5090. Para SLA, o vault continua apontando HBM ([[09-Servicos-e-Custos/Cenarios-de-infraestrutura]]).
6. **Se a dúvida persiste, o padrão é o PC com 5090 mais API para os modelos grandes** (modo 3), e a comparação vai para a planilha de [[09-Servicos-e-Custos/Guia-financeiro-TCO-local-vs-OpenAI]] com o preço datado e o consumo medido na tomada. Comprar capacidade de 128 GB "para o futuro" é a hipótese que mais precisa de prova.

## 6. Como incluir uma nova máquina

1. Preencher [[99-Templates/Modelo-de-ficha-de-workstation]] em `03-Hardware/Workstations/`, com banda e preço datados.
2. Classificar na linha correspondente de [[03-Hardware/Sizing-9B-14B-27B-70B]]; se não houver linha, criar.
3. Adicionar à tabela da seção 2 e à matriz da seção 3, aplicando a regra pesos + KV + folga para cada modelo do catálogo.
4. Calcular o teto de decode da seção 4 com a banda publicada.
5. Só depois de um benchmark próprio, registrar tokens/s medidos na ficha e em [[99-Templates/Registro-de-benchmark]].
6. Registrar a mudança em [[MEMORY]] e regenerar o índice de URLs.

## Referências

[1]: https://www.nvidia.com/pt-br/geforce/graphics-cards/40-series/rtx-4090/ "NVIDIA Brasil — GeForce RTX 4090 (24 GB GDDR6X, 384 bits, TGP 450 W, fonte 850 W); banda de ~1.008 GB/s conforme especificação de referência"
[2]: https://www.nvidia.com/pt-br/geforce/graphics-cards/50-series/rtx-5090/ "NVIDIA Brasil — GeForce RTX 5090 (32 GB GDDR7 a 28 Gbps, 512 bits, 21.760 CUDA cores, TGP 575 W, fonte 850 W); 28 Gbps × 512 bits ≈ 1.792 GB/s"
[3]: https://www.dell.com/pt-br/shop/cty/pdp/spd/dell-pro-max-fcm1253-micro "Dell Brasil — Dell Pro Max FCM1253 Micro (GB10, 128 GB LPDDR5x a 273 GB/s, 280 W, sem preço on-line)"
[4]: https://www.nvidia.com/pt-br/products/workstations/dgx-spark/ "NVIDIA Brasil — DGX Spark (273 GB/s, 1 PFLOP FP4, 240 W, 200B inferência, 70B fine-tuning)"
[5]: https://www.worldwidebrasil.com.br/nvidia-dgx-spark-4tb-ia-supercomputador-pessoal-lacrado "Worldwide Brasil — NVIDIA DGX Spark 4 TB (R$ 54.552,17 à vista em 2026-09-01)"
[6]: https://www.apple.com/br/mac-studio/ "Apple Brasil — Mac Studio (M5 Max até 128 GB e 614 GB/s; M5 Ultra até 512 GB e 1,2 TB/s)"
[7]: https://atomic.chat/blog/guides/best-local-llms-for-coding "Atomic Chat — Best Local LLM for Coding in 2026 (220 tok/s no Qwen3-Coder 30B em GPU de 24 GB; recomendação de 24 GB para 27–30B)"
[8]: https://github.com/ggml-org/llama.cpp "llama.cpp — offload parcial (modo 2), backends CUDA/Metal e GGUF"
