# Dell Pro Max com GB10 (FCM1253 Micro)

Ficha preenchida segundo [[99-Templates/Modelo-de-ficha-de-workstation]]. A máquina é a versão Dell do NVIDIA DGX Spark: mesmo superchip GB10, mesma memória e mesma banda; a NVIDIA publica as especificações completas e a Dell a página comercial brasileira [1][2][3][4].

| Campo | Registro |
|---|---|
| Nome exato / SKU | Dell Pro Max com GB10, modelo FCM1253 Micro |
| Fabricante / URL | Dell Brasil — landing page e página de produto [1][2] |
| Data de verificação | 2026-09-01 |
| Classe no vault | **128 GB unificados** — a linha mais próxima em [[03-Hardware/Sizing-9B-14B-27B-70B]] é a de Apple Silicon 128 GB, não a de "80 GB VRAM": a capacidade é de servidor pequeno, a banda não |
| CPU | NVIDIA Grace: 20 núcleos ARM (10× Cortex-X925 + 10× Cortex-A725), 16 MB L2 [2][3] |
| Acelerador | GPU Blackwell integrada ao superchip GB10; Tensor Cores de 5ª geração; até 1 PFLOP FP4 [3][4] |
| Memória do acelerador | 128 GB LPDDR5x unificada e coerente entre CPU e GPU [2][3] |
| Largura de banda | **273 GB/s**, interface de 256 bits [2][3] |
| RAM do sistema | A mesma memória unificada; descontar DGX OS, serviços e RAG antes de alocar ao LLM |
| Armazenamento | SSD M.2 2230 de 2 TB QLC ou M.2 2242 de 4 TB com criptografia Opal 2.0 [2] |
| Rede / expansão | 1× 10 GbE; ConnectX-7 com 2× 200G QSFP (uma porta para unir duas unidades); a NVIDIA declara até quatro DGX Spark em conjunto [2][4]. Sem slot PCIe para GPU discreta |
| Energia | Adaptador USB-C de 280 W (Dell); a NVIDIA declara 240 W para o DGX Spark [2][3]. Ordem de grandeza de um notebook gamer, não de uma workstation com GPU |
| Sistema operacional / stack | NVIDIA DGX OS (Linux **aarch64**) com NVIDIA AI Enterprise; CUDA nativo, NIM. Imagens Docker, wheels Python e bibliotecas precisam ser da variante ARM64/SBSA — ver [[03-Hardware/ARM-e-memoria-unificada]] e [[04-Software/Compatibilidade-por-stack]] |
| Preço datado | Dell: "este produto não pode ser adquirido on-line", sem preço publicado [2]. Referência do DGX Spark 4 TB (mesmo chip) em revendedor brasileiro: **R$ 54.552,17 à vista (Pix)**, R$ 64.179,02 parcelado, prazo de 20 dias úteis, consultado em 2026-09-01 [5]. Cotar a Dell diretamente antes de qualquer decisão |
| Alegações do fabricante | "Suporta modelos de até 200 bilhões de parâmetros" (inferência) e "fine-tuning de até 70 bilhões", ambos pressupondo FP4/quantização; "até 405B com duas unidades" na página em português e "até 700B com quatro" na página em inglês [3][4]. Nenhuma das alegações informa tokens/s |
| Modelos viáveis em modo 1 | Laguna XS 2.1 (GGUF Q4_K_M 20,3 GB; variante NVFP4 oficial); Qwen3-Coder-30B-A3B (~22 GB); Gemma 4 26B A4B (~12–18 GB); Qwen3.6-27B (~17–18 GB); **Qwen3-Coder-Next 80B/3B (~45 GB)**; **Laguna S 2.1 (~67 GB NVFP4; ~96 GB Q4, justo)**; Llama 3.1 70B Q4 (38–48 GB, inteiro, lento); Llama 4 Scout Int4 (~55–60 GB); Qwen3.8-Flash-Next (~65–75 GB estimados). Tamanhos conforme [[02-Modelos/Catalogo-de-modelos]] e [[02-Modelos/LLMs-locais-para-coding-Atomic]] |
| Modelos em modo 2 | Nada relevante do catálogo fica em modo 2: ou cabe inteiro ou não cabe nem com duas unidades |
| Fora de alcance | Kimi K2.7 Code: menor GGUF tem 304 GB; nem duas unidades (256 GB) executam — continua modo 3/4 ([[02-Modelos/Fichas/Kimi-K2.7-Code]]) |
| Teto de decode por banda | 273 ÷ GB lidos por token: Qwen3.6-27B Q4 (~17 GB) ≈ 16 tok/s; Llama 70B Q4 (~42 GB) ≈ 6,5 tok/s; MoE com 3B ativos (~2–2,5 GB por token) ≈ 100+ tok/s, provavelmente limitado por computação antes disso. **Triagem, não benchmark**; o medido costuma ficar em 50–70% do teto |
| Velocidade medida | Não medido neste vault |
| Incógnitas | Preço Dell BR; disponibilidade de vLLM/TensorRT-LLM, bitsandbytes e Unsloth em aarch64 nas versões atuais; tokens/s reais nos modelos-alvo; comportamento térmico em 10–20 min de carga; comportamento de `ollama` e `llama.cpp` com NVFP4 nesta GPU |
| Estado | Candidata — aguardando cotação e benchmark |
| Dono da ficha | Luiz Guimarães |
| Próxima revisão | 2026-10-01 |

## Leitura crítica

- **Capacidade de servidor pequeno, banda de notebook.** 128 GB colocam em modo 1 modelos que o catálogo marcava como "servidor ou workstation com muita RAM" (Qwen3-Coder-Next, Laguna S 2.1, Qwen3.8-Flash-Next). Mas 273 GB/s são ~3,7× menos que uma RTX 4090 e ~6,6× menos que uma RTX 5090; em modelo denso, o decode por sessão será sensivelmente mais lento que em qualquer PC com GPU discreta ([[03-Hardware/Comparativo-workstations-vs-GPU]]).
- **O ponto ideal é MoE com poucos parâmetros ativos.** Com 3B–8B ativos, os bytes lidos por token são pequenos e a banda deixa de ser o gargalo; é exatamente a classe de modelo que o guia da Atomic recomenda para coding ([[02-Modelos/LLMs-locais-para-coding-Atomic]]).
- **CUDA, mas em ARM.** É a vantagem sobre o Mac de 128 GB (vLLM, TensorRT-LLM, bitsandbytes, NVFP4 nativo) e a desvantagem sobre um PC x86 (parte do ecossistema chega depois ou não chega em aarch64). Validar cada ferramenta antes de comprar.
- **Fine-tuning.** A alegação de "até 70B" é QLoRA/adapters com pesos quantizados; o vault continua recomendando esse caminho ([[06-Treinamento-e-Fine-tuning/01-QLoRA-pratico]]) e não treino completo.
- **Preço.** Uma cotação brasileira de ~R$ 54,5 mil compra, na faixa de [[03-Hardware/Builds-brasileiros-por-orcamento]], uma Build C completa com RTX 5090 e sobra, ou se aproxima de uma Build D com duas 5090. A decisão depende da classe de modelo alvo, não da máquina isolada.

## Referências

[1]: https://www.dell.com/pt-br/lp/dell-pro-max-nvidia-ai-dev-premier "Dell Brasil — Dell Pro Max com GB10 (landing page: 128 GB unificados, 1 PFLOP FP4, até 200B parâmetros)"
[2]: https://www.dell.com/pt-br/shop/cty/pdp/spd/dell-pro-max-fcm1253-micro "Dell Brasil — Dell Pro Max FCM1253 Micro (especificações: 20 núcleos ARM, 128 GB LPDDR5x a 273 GB/s, SSD 2/4 TB, ConnectX-7, 280 W, sem preço on-line)"
[3]: https://www.nvidia.com/pt-br/products/workstations/dgx-spark/ "NVIDIA Brasil — DGX Spark (GB10: 10× X925 + 10× A725, 128 GB a 273 GB/s, 1 PFLOP FP4, 200B inferência, 70B fine-tuning, 405B com duas unidades, 240 W)"
[4]: https://www.nvidia.com/en-us/products/workstations/dgx-spark/ "NVIDIA — DGX Spark (273 GB/s, up to four systems for models up to 700B)"
[5]: https://www.worldwidebrasil.com.br/nvidia-dgx-spark-4tb-ia-supercomputador-pessoal-lacrado "Worldwide Brasil — NVIDIA DGX Spark 4 TB (R$ 54.552,17 à vista, consultado em 2026-09-01)"
