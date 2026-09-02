# Dell Pro Max com GB10 (FCM1253 Micro)

Ficha preenchida segundo [[99-Templates/Modelo-de-ficha-de-workstation]]. A máquina é a versão Dell do NVIDIA DGX Spark: mesmo superchip GB10, mesma memória e mesma banda; a NVIDIA publica as especificações completas e a Dell a página comercial brasileira [1][2][3][4].

| Campo | Registro |
|---|---|
| Nome exato / SKU | Dell Pro Max com GB10, modelo FCM1253 Micro |
| Fabricante / URL | Dell Brasil — landing page e página de produto [1][2] |
| Data de verificação | 2026-09-02 |
| Classe no vault | **128 GB unificados** — a linha mais próxima em [[03-Hardware/Sizing-9B-14B-27B-70B]] é a de Apple Silicon 128 GB, não a de "80 GB VRAM": a capacidade é de servidor pequeno, a banda não |
| CPU | NVIDIA Grace: 20 núcleos ARM (10× Cortex-X925 + 10× Cortex-A725), 16 MB L2 [2][3] |
| Acelerador | GPU Blackwell integrada ao superchip GB10; Tensor Cores de 5ª geração; até 1 PFLOP FP4 [3][4] |
| Memória do acelerador | 128 GB LPDDR5x unificada e coerente entre CPU e GPU [2][3] |
| Largura de banda | **273 GB/s**, interface de 256 bits [2][3] |
| RAM do sistema | A mesma memória unificada; descontar DGX OS, serviços e RAG antes de alocar ao LLM |
| Armazenamento | SSD M.2 2230 de 2 TB QLC ou M.2 2242 de 4 TB com criptografia Opal 2.0 [2] |
| Rede / expansão | 1× RJ-45 10 GbE; ConnectX-7 com 2× QSFP de 200G (uma porta necessária para conectar outra unidade); sem slot de expansão e sem slot PCIe para GPU discreta [2] |
| Energia | Adaptador CA USB Type-C de 280 W [2]. A referência NVIDIA do DGX Spark declara 240 W [3]; não tratar os valores como TDP diretamente comparáveis |
| Sistema operacional / stack | NVIDIA DGX OS (Linux **aarch64**) com CUDA nativo. Imagens Docker, wheels Python e bibliotecas precisam ser da variante ARM64/SBSA — ver [[03-Hardware/ARM-e-memoria-unificada]] e [[04-Software/Compatibilidade-por-stack]] |
| Preço datado | Dell: "este produto não pode ser adquirido on-line", sem preço publicado [2]. Referência do DGX Spark 4 TB (mesmo chip) em revendedor brasileiro: **R$ 54.552,17 à vista (Pix)**, R$ 64.179,02 parcelado, prazo de 20 dias úteis, consultado em 2026-09-01 [5]. Cotar a Dell diretamente antes de qualquer decisão |
| Alegações do fabricante | "Suporta modelos de até 200 bilhões de parâmetros" (inferência) e "fine-tuning de até 70 bilhões", ambos pressupondo FP4/quantização; "até 405B com duas unidades" na página em português e "até 700B com quatro" na página em inglês [3][4]. Nenhuma das alegações informa tokens/s |
| Modelos viáveis em modo 1 | Laguna XS 2.1 (GGUF Q4_K_M 20,3 GB; variante NVFP4 oficial); Qwen3-Coder-30B-A3B (~22 GB); Gemma 4 26B A4B (~12–18 GB); Qwen3.6-27B (~17–18 GB); **Qwen3-Coder-Next 80B/3B (~45 GB)**; **Laguna S 2.1 (~67 GB NVFP4; ~96 GB Q4, justo)**; Llama 3.1 70B Q4 (38–48 GB, inteiro, lento); Llama 4 Scout Int4 (~55–60 GB); Qwen3.8-Flash-Next (~65–75 GB estimados). Tamanhos conforme [[02-Modelos/Catalogo-de-modelos]] e [[02-Modelos/LLMs-locais-para-coding-Atomic]] |
| Modelos em modo 2 | Nada relevante do catálogo fica em modo 2: ou cabe inteiro ou não cabe nem com duas unidades |
| Fora de alcance | Kimi K2.7 Code: menor GGUF tem 304 GB; nem duas unidades (256 GB) executam — continua modo 3/4 ([[02-Modelos/Fichas/Kimi-K2.7-Code]]) |
| Teto de decode por banda | 273 ÷ GB lidos por token: Qwen3.6-27B Q4 (~17 GB) ≈ 16 tok/s; Llama 70B Q4 (~42 GB) ≈ 6,5 tok/s; MoE com 3B ativos (~2–2,5 GB por token) ≈ 100+ tok/s, provavelmente limitado por computação antes disso. **Triagem, não benchmark**; o medido costuma ficar em 50–70% do teto |
| Velocidade medida | Não medido neste vault |
| Incógnitas | Preço Dell BR; tokens/s reais nos modelos-alvo; comportamento térmico em 10–20 min de carga; comportamento de `ollama` e `llama.cpp` com NVFP4 nesta GPU; suporte modelo-a-modelo em vLLM e TensorRT-LLM |
| Estado | Candidata — aguardando cotação e benchmark |
| Dono da ficha | Luiz Guimarães |
| Próxima revisão | 2026-10-01 |

## Dados mecânicos e conectividade confirmados pela Dell

A página comercial brasileira confirma que o chassi mede **15,10 × 15,10 cm**, com altura entre 4,55 cm e 5,10 cm, e pesa no mínimo 1,31 kg. A conectividade inclui três USB-C Gen 2x2 com DisplayPort Alt Mode, uma HDMI 2.1b, uma entrada de energia USB-C, RJ-45 de 10 GbE e duas portas QSFP de 200G no ConnectX-7. Não há unidade óptica nem slots de expansão. A máquina também oferece Wi-Fi 802.11be e Bluetooth 5.4 [2].

## Estado dos frameworks ARM64 e NVFP4

| Framework | ARM64/CUDA no GB10 | NVFP4 no GB10 | Classificação para produção |
|---|---|---|---|
| vLLM | Wheels CUDA 13 aarch64 aparecem a partir da linha 0.13.0; requer ambiente Linux/ARM64 compatível e wheel correta [6][7] | Suporte é condicional por modelo, kernel e combinação SM121; a documentação geral não equivale a uma validação universal de NVFP4 no GB10 | **Disponível, mas não declarar universalmente estável**; testar o modelo-alvo |
| TensorRT-LLM | Suporte NVIDIA/Blackwell e caminhos ARM64/SBSA na plataforma DGX Spark | Release 1.2 declara **DGX Spark beta**, single-node e uma lista limitada de modelos/formatos validados, incluindo vários NVFP4 [8] | **Melhor caminho NVIDIA para NVFP4 no GB10, porém beta e restrito à matriz validada** |
| Ollama / llama.cpp | Caminhos práticos para uso local, mas dependem da build/driver e não substituem a validação CUDA específica | Não tratar NVFP4 como garantido nesta ficha sem benchmark no GB10 | **Fallback operacional; validar formato e backend** |

A conclusão é deliberadamente conservadora: o TensorRT-LLM tem o suporte oficial mais explícito para DGX Spark/NVFP4, mas ainda em beta e somente para combinações validadas. O vLLM já tem caminho ARM64/CUDA 13 em releases recentes, porém o suporte genérico a CUDA não prova estabilidade de todos os kernels NVFP4 no SM121.

## Simulação de inferência versus 2× RTX 5090

Foi adicionada uma simulação reproduzível em [[03-Hardware/Workstations/simular_gb10_vs_2x_rtx5090.py]], com dados em [[03-Hardware/Workstations/simulacao-gb10-vs-2x-rtx5090.csv]] e gráfico em [[03-Hardware/Workstations/grafico-simulacao-gb10-vs-2x-rtx5090.png]]. O cálculo é um envelope bandwidth-bound, não um benchmark: usa 273 GB/s e 70% de eficiência para o GB10; 2 × 1.792 GB/s e 62% de eficiência para as RTX 5090, com 1.400 W estimados para o sistema de duas GPUs completo.

| Modelo | Dell GB10 | 2× RTX 5090 | Ganho estimado das 5090 |
|---|---:|---:|---:|
| Qwen3.6-27B Q4 | 10,9 tok/s | 127,0 tok/s | 11,6× |
| Llama 3.1 70B Q4 | 4,6 tok/s | 52,9 tok/s | 11,6× |
| Qwen3-Coder-Next 80B/3B Q4 | 31,9 tok/s | 370,4 tok/s | 11,6× |

O resultado favorece fortemente as duas RTX 5090 em velocidade porque a simulação assume acesso agregado à banda das duas GPUs. Em troca, o GB10 oferece 128 GB unificados contra 64 GB de VRAM agregada, menor consumo nominal e um chassi muito menor. Para 70B/80B, a comparação também depende do overhead de tensor parallelism, da capacidade de manter o KV cache e do fato de o modelo realmente caber sem offload.

## Leitura crítica

- **Capacidade de servidor pequeno, banda de notebook.** 128 GB colocam em modo 1 modelos que o catálogo marcava como "servidor ou workstation com muita RAM" (Qwen3-Coder-Next, Laguna S 2.1, Qwen3.8-Flash-Next). Mas 273 GB/s são ~3,7× menos que uma RTX 4090 e ~6,6× menos que uma RTX 5090; em modelo denso, o decode por sessão será sensivelmente mais lento que em qualquer PC com GPU discreta ([[03-Hardware/Comparativo-workstations-vs-GPU]]).
- **O ponto ideal é MoE com poucos parâmetros ativos.** Com 3B–8B ativos, os bytes lidos por token são pequenos e a banda deixa de ser o gargalo; é exatamente a classe de modelo que o guia da Atomic recomenda para coding ([[02-Modelos/LLMs-locais-para-coding-Atomic]]).
- **CUDA, mas em ARM.** É a vantagem sobre o Mac de 128 GB, com caminho oficial mais claro para TensorRT-LLM/NVFP4, e a desvantagem sobre um PC x86: parte do ecossistema chega depois ou depende de wheels ARM64/SBSA. O quadro acima deve ser revisado por modelo e versão.
- **Fine-tuning.** A alegação de "até 70B" é QLoRA/adapters com pesos quantizados; o vault continua recomendando esse caminho ([[06-Treinamento-e-Fine-tuning/01-QLoRA-pratico]]) e não treino completo.
- **Preço.** Uma cotação brasileira de ~R$ 54,5 mil compra, na faixa de [[03-Hardware/Builds-brasileiros-por-orcamento]], uma Build C completa com RTX 5090 e sobra, ou se aproxima de uma Build D com duas 5090. A decisão depende da classe de modelo alvo, não da máquina isolada.

## Referências

[1]: https://www.dell.com/pt-br/lp/dell-pro-max-nvidia-ai-dev-premier "Dell Brasil — Dell Pro Max com GB10 (landing page: 128 GB unificados, 1 PFLOP FP4, até 200B parâmetros)"
[2]: https://www.dell.com/pt-br/shop/cty/pdp/spd/dell-pro-max-fcm1253-micro "Dell Brasil — Dell Pro Max FCM1253 Micro (especificações: 20 núcleos ARM, 128 GB LPDDR5x a 273 GB/s, SSD 2/4 TB, ConnectX-7, 280 W, sem preço on-line)"
[3]: https://www.nvidia.com/pt-br/products/workstations/dgx-spark/ "NVIDIA Brasil — DGX Spark (GB10: 10× X925 + 10× A725, 128 GB a 273 GB/s, 1 PFLOP FP4, 200B inferência, 70B fine-tuning, 405B com duas unidades, 240 W)"
[4]: https://www.nvidia.com/en-us/products/workstations/dgx-spark/ "NVIDIA — DGX Spark (273 GB/s, up to four systems for models up to 700B)"
[5]: https://www.worldwidebrasil.com.br/nvidia-dgx-spark-4tb-ia-supercomputador-pessoal-lacrado "Worldwide Brasil — NVIDIA DGX Spark 4 TB (R$ 54.552,17 à vista, consultado em 2026-09-01)"

[6]: https://docs.vllm.ai/en/stable/getting_started/installation/gpu/ "vLLM — instalação GPU e requisitos gerais"

[7]: https://github.com/vllm-project/vllm/issues/31128 "vLLM — suporte a Blackwell SM121/DGX Spark e wheels CUDA 13 aarch64"

[8]: https://nvidia.github.io/TensorRT-LLM/release-notes.html "TensorRT-LLM — Release 1.2: suporte beta a DGX Spark e formatos validados"
