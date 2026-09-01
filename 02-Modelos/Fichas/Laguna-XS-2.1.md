# Laguna XS 2.1

| Campo | Registro |
|---|---|
| Data de verificação | 2026-09-01 (leitura dos model cards oficiais e da biblioteca Ollama nesta data) |
| Checkpoint | `poolside/Laguna-XS-2.1` no Hugging Face; variantes oficiais `-FP8`, `-NVFP4`, `-INT4`, `-GGUF`, `-NVFP4-mlx`, `-DFlash` (draft para decodificação especulativa) [1][2][3][4] |
| Lançamento | 2026-07-02, conforme blog oficial; substitui a Laguna XS.2 (mesma arquitetura) [5] |
| Arquitetura | MoE causal para coding agentic; 40 camadas (10 com atenção global, 30 com sliding window de 512 tokens, razão 3:1); 256 experts roteados + 1 shared; sigmoid gating com escalas rotatórias por camada; KV cache quantizado em FP8 por projeto; raciocínio nativo com thinking intercalado entre tool calls, ligável por requisição [1] |
| Parâmetros totais/ativos | 33B totais / 3B ativados por token, conforme model card [1]. O Hugging Face exibe "41B params" na página da variante INT4; é contagem automática de tensores (escalas e metadados) e não deve ser usada como especificação |
| Contexto | 262.144 tokens; o blog cita até 32K tokens de saída [1][5] |
| Modalidades | Texto e código; tool calling com parser `poolside_v1` (vLLM/SGLang) [1] |
| Licença | OpenMDW-1.1, declarada como permissiva para uso comercial e não comercial; mudança em relação à licença da XS.2. Ler o texto integral antes de uso empresarial; validação jurídica separada [1][5] |
| Modo de execução | **Local real** em GPU/Mac com memória suficiente; ver [[02-Modelos/Local-real-vs-cloud]]. No Ollama, `laguna-xs-2.1` é um download local (não há tag `:cloud`) [6] |
| Arquivo quantizado real | GGUF oficial: `Laguna-XS-2.1-Q4_K_M.gguf` = **20,3 GB**; `Laguna-XS-2.1-BF16.gguf` = 66,9 GB [3]. Biblioteca Ollama: `latest` (Q4_K_M) 20 GB; `q8_0` 36 GB; `bf16` 67 GB; `nvfp4` (MLX) 20 GB; `mxfp8` (MLX) 40 GB; `mlx-bf16` 68 GB [6] |
| Memória estimada | Piso teórico dos pesos em 4 bits: 33B × 0,5 B ≈ 16,5 GB decimal; o arquivo Q4_K_M real (20,3 GB) fica ~23% acima do piso por escalas, blocos e tensores não quantizados. Some KV cache e buffers; para uma GPU de 24 GB, o Q4_K_M cabe com margem pequena e contexto moderado. O card afirma que o modelo é "compact enough to run on a Mac with 36 GB of RAM" [1][3] |
| Runtimes e versões mínimas | vLLM (KV cache FP8 exige `>= 0.22.0`); SGLang (suporte via PR #24204 no momento da leitura); Transformers (quantização detectada automaticamente); TensorRT-LLM `>= 1.3.0rc16`; llama.cpp somente BF16 e Q4_K_M — o PR #25165 "Add support for Laguna XS.2 & M.1" foi mesclado em 2026-07-22 (referência a build b10018, commit `54f214a`), embora a página GGUF ainda instrua a compilar a partir do PR; usar build igual ou posterior e confirmar no changelog [2][3][4][7]. Ollama: página oficial adverte que no macOS/Metal o modelo "pode retornar output vazio"; recomenda host Linux/CUDA ou endpoint `/api/generate` [6] |
| Parâmetros recomendados | `llama-server -m Laguna-XS-2.1-Q4_K_M.gguf --jinja -ngl 99 -c 32768`; `-c 32768` sugerido para máquinas locais, embora o modelo aceite 262.144; `-fa on` no macOS [3] |
| Hardware medido | Não medido neste vault; benchmark próprio pendente |
| Velocidade | Não publicar sem benchmark próprio; nenhum tokens/s oficial foi encontrado nos cards |
| Tool calling/JSON | Card documenta parser próprio e thinking intercalado entre chamadas; validar com harness local antes de uso agentic [1] |
| Fonte primária | Model card [1]; variantes [2][3][4]; blog de lançamento [5]; biblioteca Ollama [6] |
| Fonte editorial | [[02-Modelos/Verificacao-PromptQuorum]] (o artigo cita o modelo com 70,9% no SWE-bench Verified; confirmado no card) |
| Ficha padrão | [[02-Modelos/Ficha-padronizada-por-modelo]] |
| Estado | Candidato para GPU de 24 GB ou Mac de 36 GB+, sujeito a teste; melhor candidato local entre os modelos verificados nesta rodada |
| Dono | Luiz Guimarães |
| Próxima revisão | 2026-10-01 |

## Benchmarks publicados (metodologia do próprio card)

Os números abaixo são do model card oficial e valem sob a metodologia declarada pela poolside: Harbor Framework (Laude Institute) com o harness de agente da própria empresa, máximo de 500 passos, `temperature=1.0`, `top_k=20`, `top_p=1`, thinking ativado, contexto de 256K tokens; sandbox de 8 GB RAM/2 CPUs por tarefa, exceto Terminal-Bench 2.0 com 48 GB RAM/32 CPUs [1][5].

| Benchmark (variante exata) | Resultado | Tentativas | Observação |
|---|---:|---:|---|
| SWE-bench Verified | 70,9% | média de pass@1 em 4 tentativas por tarefa | Valor citado pelo PromptQuorum; confirmado |
| SWE-bench Multilingual | 63,1% | média de pass@1 em 4 tentativas por tarefa | Maior ganho sobre a XS.2 (+5,4 pontos) |
| SWE-Bench Pro (Public Dataset) | 47,6% | média de pass@1 em 2 tentativas por tarefa | Não comparar com SWE-bench Verified |
| Terminal-Bench 2.0 | 37,5% | média de pass@1 em 5 tentativas por tarefa | Sandbox maior (48 GB RAM/32 CPUs) |

Os cards das variantes quantizadas publicam comparações com a BF16 sob a mesma metodologia. Na leitura de 2026-09-01: FP8 — SWE-bench Verified 70,75 vs 70,85; SWE-Bench Pro 48,02 vs 47,61; Terminal-Bench 2.0 40,22 vs 37,53 [4]. INT4 — SWE-Bench Pro 48,70 vs 47,61 [2]. Diferenças dessa ordem estão dentro da variação esperada entre tentativas e não devem ser lidas como "a quantização melhora o modelo". A tabela cruzada com outros modelos está em [[02-Modelos/Tabela-normalizada-de-benchmarks]].

## Leitura crítica

- O par "33B totais / 3B ativos" é o motivo de o modelo ser rápido **e** exigir ~20 GB de arquivo: a computação por token usa 3B, mas os 33B precisam residir em memória. Não dimensionar por parâmetros ativos ([[03-Hardware/Calculadora-de-memoria]]).
- "Cabe em 24 GB" depende do arquivo (20,3 GB no Q4_K_M), do contexto e do KV cache (aqui FP8 por projeto, o que ajuda). Para 128K+ de contexto, medir antes de prometer.
- O 70,9% no SWE-bench Verified é média de 4 tentativas com harness próprio, thinking ligado e 500 passos. Outro harness ou uma única tentativa produzirá outro número.
- Suporte em llama.cpp/Ollama é recente e limitado a BF16/Q4_K_M; o aviso de output vazio no Metal é um risco concreto para usuários de Mac até nova versão.

## Referências

[1]: https://huggingface.co/poolside/Laguna-XS-2.1 "poolside — Laguna XS 2.1 model card (arquitetura, contexto, licença, benchmarks e metodologia)"
[2]: https://huggingface.co/poolside/Laguna-XS-2.1-INT4 "poolside — Laguna XS 2.1-INT4 (variante INT4, KV FP8, comparação com BF16)"
[3]: https://huggingface.co/poolside/Laguna-XS-2.1-GGUF "poolside — Laguna XS 2.1-GGUF (Q4_K_M 20,3 GB, BF16 66,9 GB, flags recomendadas)"
[4]: https://huggingface.co/poolside/Laguna-XS-2.1-FP8 "poolside — Laguna XS 2.1-FP8 (versões mínimas de runtime e comparação com BF16)"
[5]: https://poolside.ai/blog/introducing-laguna-xs-2-1 "poolside — Introducing Laguna XS 2.1 (2026-07-02; licença, metodologia, sunset da XS.2)"
[6]: https://ollama.com/library/laguna-xs-2.1 "Ollama — laguna-xs-2.1 (tags locais, tamanhos e aviso para macOS/Metal)"
[7]: https://github.com/ggml-org/llama.cpp/pull/25165 "llama.cpp — PR #25165 Add support for Laguna XS.2 & M.1 (merged 2026-07-22)"
