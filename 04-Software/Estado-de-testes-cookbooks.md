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
| RAG local | **Testado ponta a ponta em 2026-09-01** (Windows 11, RTX 4060 Laptop 8 GB, Python 3.11.9, venv novo com `--require-hashes` do lockfile, Ollama 0.33.2 + `qwen3.5:4b` Q4_K_M): selftest OK; recuperação com `all-MiniLM-L6-v2` correta em 2/2; geração com `[Fonte N]` correta em 3/3, incluindo recusa sem evidência; geração 0,9–9,3 s em GPU, 24–35 s ponta a ponta. Evidência: [[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]]. | Corpus real e maior, PDFs escaneados, recall@k/groundedness, concorrência e embeddings em GPU; registrar em [[99-Templates/Registro-de-benchmark]]. |

## Registro obrigatório

Preencha hardware, OS, kernel, driver, runtime, modelo, hash, quantização, contexto, prompt, temperatura, seed, tokens/s, TTFT, P50/P95, VRAM/RAM, consumo e logs. O resultado deve ser anexado à ficha do modelo e ao registro de benchmark.

## Por que não inventar números

Desempenho depende de implementação e ambiente. O vault pode oferecer comandos reproduzíveis e uma matriz de aceitação, mas não deve atribuir tokens/s a uma máquina que não foi medida. Resultados editoriais permanecem marcados como externos.
