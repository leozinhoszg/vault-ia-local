# Estado de testes dos cookbooks

## Critério de honestidade

Um cookbook só recebe o estado **testado** quando o comando foi executado no sistema operacional, backend, hardware, modelo e versão declarados, com saída preservada. “Compatível segundo documentação” e “sintaxe validada” não são equivalentes a teste de performance.

| Cookbook | Validação atual | Teste pendente |
|---|---|---|
| Windows + NVIDIA | Receita e comandos revisados | Executar no Windows com driver e GPU declarados. |
| WSL2 + NVIDIA | Receita e comandos revisados | Validar passthrough, filesystem e performance. |
| Linux + CUDA | Receita e comandos revisados | Validar driver, CUDA, PyTorch, vLLM e benchmark. |
| Linux + ROCm | Receita alinhada à matriz ROCm | Validar GPU/SO/kernel/firmware e kernels reais. |
| macOS + Metal/MLX | Receita e ferramentas identificadas | Validar cada Mac, macOS, modelo e quantização. |
| RAG local | **Patch endurecido parcialmente validado em 2026-09-01**: em container Linux/Python 3.11 sem mount do host, `--selftest` passou; retrieval real recuperou a fonte correta com `all-MiniLM-L6-v2` na revisão fixada `1110a243...`; PDF opt-in foi extraído em subprocesso e `--max-pdf-pages` falhou fechado; lock Windows teve checksum conferido e 43 pins auditados sem vulnerabilidade conhecida. Evidência atual: [[07-Implementacao-Casa/Evidencias/RAG-hardening-2026-09-01]]. A reprodução Windows/Ollama anterior é histórica e está preservada em [[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]], mas não valida este patch. | Instalar o lock novo em Windows limpo; repetir geração Ollama e recusa sem evidência na versão atual; corpus real/maior, PDF hostil isolado, recall@k/groundedness, concorrência e embeddings em GPU. Registrar em [[99-Templates/Registro-de-benchmark]]. |

## Registro obrigatório

Preencha hardware, OS, kernel, driver, runtime, modelo, hash, quantização, contexto, prompt, temperatura, seed, tokens/s, TTFT, P50/P95, VRAM/RAM, consumo e logs. O resultado deve ser anexado à ficha do modelo e ao registro de benchmark.

## Por que não inventar números

Desempenho depende de implementação e ambiente. O vault pode oferecer comandos reproduzíveis e uma matriz de aceitação, mas não deve atribuir tokens/s a uma máquina que não foi medida. Resultados editoriais permanecem marcados como externos.
