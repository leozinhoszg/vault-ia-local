# Kimi K2.7 Code

| Campo | Registro |
|---|---|
| Data de verificação | 2026-09-01 (leitura do model card oficial, guia de deploy, licença, repositório GGUF da Unsloth e biblioteca Ollama nesta data) |
| Checkpoint | `moonshotai/Kimi-K2.7-Code` no Hugging Face; 64 arquivos safetensors, repositório de **595 GB** [1][2] |
| Lançamento | Data não consta no card; posterior ao Kimi K2.6, do qual deriva [1] |
| Arquitetura | Mesma do Kimi K2.5/K2.6: MoE com 61 camadas (1 densa), 384 experts, 8 selecionados por token + 1 shared, atenção MLA com 64 heads e dimensão 7168; encoder de visão MoonViT de 400M; entrada de imagem e vídeo [1] |
| Parâmetros totais/ativos | 1T totais / 32B ativados por token [1] |
| Contexto | 256K tokens [1] |
| Modalidades | Texto, código, imagem e vídeo (Image-Text-to-Text) [1] |
| Licença | Modified MIT: além do MIT, produtos ou serviços que ultrapassem 100 milhões de usuários ativos mensais **ou** US$ 20 milhões de receita mensal devem exibir "Kimi K2.7 Code" na interface. Validação jurídica separada [3] |
| Formato dos pesos | **INT4 nativo** (mesmo método QAT do Kimi-K2-Thinking); é a precisão de referência do modelo, não uma conversão comunitária. Por isso o GGUF Q8 da Unsloth (595 GB) é só ~10 GB maior que o Q4 (584 GB) [1][4] |
| Modo de execução | **Infraestrutura de alta memória** ou **serviço remoto**. No Ollama existe apenas `kimi-k2.7-code:cloud` (US$ 0,95/M tokens de entrada e US$ 4,00/M de saída na leitura); o comando não executa nada localmente. Ver [[02-Modelos/Local-real-vs-cloud]] [5] |
| Arquivo quantizado real | GGUF Unsloth (dynamic): UD-IQ1_M 304 GB; UD-IQ2_XXS/IQ2_M 318 GB; UD-Q2_K_XL 339 GB; UD-IQ3_S 419 GB; UD-Q3_K_M/Q3_K_XL 464 GB; UD-IQ4_XS 495 GB; UD-Q4_K_XL 584 GB; UD-Q8_K_XL 595 GB [4] |
| Memória estimada | Piso teórico dos pesos em 4 bits: 1T × 0,5 B ≈ 500 GB decimal, confirmado pelo repositório oficial de 595 GB. A quantização mais agressiva disponível (IQ1_M) ainda pede ~304 GB só de pesos; **nenhuma configuração doméstica de 22–24 GB executa este modelo**. Os 32B ativos reduzem computação por token, não o armazenamento [1][4] |
| Runtimes e versões mínimas | vLLM 0.19.1 (verificado pela Moonshot), SGLang v0.5.10+, KTransformers; llama.cpp/Ollama/LM Studio/Jan via GGUF de terceiros [1][2] |
| Hardware documentado pela Moonshot | vLLM/SGLang: nó H200 com TP8. KTransformers+SGLang: 8× NVIDIA L20 + 2× Intel Xeon 6454S (640 tok/s de prefill no guia). KTransformers+LLaMA-Factory: 2× RTX 4090 + Xeon 8488C com 1,97 TB de RAM e 200 GB de swap — este é o cenário de **offload CPU/RAM**, viável só com RAM de servidor [2] |
| Hardware medido | Não medido neste vault |
| Velocidade | Não publicar sem benchmark próprio; o número de prefill do guia é do ambiente da Moonshot |
| Tool calling/JSON | Card avaliado com Kimi Code CLI e benchmarks de MCP (MCP-Atlas, MCPMark Verified); validar no runtime escolhido [1] |
| Fonte primária | Model card [1]; guia de deploy [2]; licença [3] |
| Fonte editorial | [[02-Modelos/Verificacao-PromptQuorum]] (o artigo indica `ollama run kimi-k2.7-code`; a biblioteca oficial só tem a tag `:cloud`) |
| Ficha padrão | [[02-Modelos/Ficha-padronizada-por-modelo]] |
| Estado | Candidato para infraestrutura de alta memória ou consumo remoto; **não candidato** para workstation doméstica |
| Dono | Luiz Guimarães |
| Próxima revisão | 2026-10-01 |

## Benchmarks publicados (metodologia do próprio card)

Na leitura de 2026-09-01, o model card do K2.7 Code **não publica SWE-bench Verified, SWE-bench Pro nem Terminal-Bench**; publica benchmarks internos ou de agentes. Qualquer número de SWE-bench atribuído ao K2.7 Code precisa de outra fonte primária e data. Metodologia declarada: thinking ativado via Kimi Code CLI, `temperature=1.0`, `top-p=0.95`, contexto de 262.144 tokens; MCP-Atlas e MCPMark-Verified com orçamento de 100 tool calls, 32K tokens por passo e média de 3 execuções. GPT-5.5 rodou no Codex (xhigh) e Claude Opus 4.8 no Claude Code (xhigh) — harnesses diferentes, portanto comparação indicativa [1].

| Benchmark | Kimi K2.6 | Kimi K2.7 Code | Observação |
|---|---:|---:|---|
| Kimi Code Bench v2 | 50,9 | 62,0 | Benchmark interno da Moonshot; não reproduzível externamente |
| Program Bench | 48,3 | 53,6 | Idem |
| MLS Bench Lite | 26,7 | 35,1 | Idem |
| Kimi Claw 24/7 Bench | 42,9 | 46,9 | Idem |
| MCP-Atlas | 69,4 | 76,0 | Média de 3 execuções |
| MCPMark Verified | 72,8 | 81,1 | Média de 3 execuções |

O card também declara redução de aproximadamente 30% nos tokens de thinking em relação ao K2.6, o que afeta custo e latência mais do que qualidade. Para SWE-bench, a referência primária mais próxima continua sendo o card do K2.6 (80,2 Verified / 58,6 Pro, média de 10 execuções) em [[02-Modelos/Fichas/Kimi-K2.6]] e [[02-Modelos/Tabela-normalizada-de-benchmarks]].

## Leitura crítica

- O modelo é excelente candidato a **API remota** ou a **cluster próprio**; enquadrá-lo como "LLM local para programação" exige declarar o hardware (H200 ×8 ou RAM de ~2 TB), o que muda o problema de custo por completo ([[09-Servicos-e-Custos/Cenarios-de-infraestrutura]]).
- "INT4 nativo" significa que não há versão de maior precisão a perder; e também que a quantização comunitária abaixo de 4 bits parte de um modelo já em 4 bits, com degradação a medir.
- A licença é permissiva na prática, mas a obrigação de exibir a marca acima dos limiares deve entrar no checklist jurídico de qualquer produto.

## Referências

[1]: https://huggingface.co/moonshotai/Kimi-K2.7-Code "Moonshot AI — Kimi K2.7 Code model card (arquitetura, contexto, INT4 nativo, benchmarks e metodologia)"
[2]: https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/docs/deploy_guidance.md "Moonshot AI — guia de deploy do Kimi K2.7 Code (vLLM, SGLang, KTransformers, hardware)"
[3]: https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/LICENSE "Moonshot AI — Modified MIT License do Kimi K2.7 Code"
[4]: https://huggingface.co/unsloth/Kimi-K2.7-Code-GGUF "Unsloth — Kimi K2.7 Code GGUF (tamanhos reais por quantização)"
[5]: https://ollama.com/library/kimi-k2.7-code "Ollama — kimi-k2.7-code (apenas tag :cloud e preço por token)"
