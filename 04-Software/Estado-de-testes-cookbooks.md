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
| RAG local | Reproduzido em ambiente limpo em 2026-09-01 (Windows 11, Python 3.11.9, venv novo, `pip install --require-hashes` do lockfile): `--selftest` OK em 5,0 s e `--retrieve-only` com `all-MiniLM-L6-v2` recuperou o documento correto em duas consultas (26 s / 23 s, torch CPU). Versões efetivas iguais ao lockfile (numpy 2.3.2). Evidência: [[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]]. | Geração via Ollama com resposta `[Fonte N]`, corpus real, PDFs escaneados e avaliação (recall@k, groundedness) em máquina com Ollama/GPU; registrar em [[99-Templates/Registro-de-benchmark]]. |

## Registro obrigatório

Preencha hardware, OS, kernel, driver, runtime, modelo, hash, quantização, contexto, prompt, temperatura, seed, tokens/s, TTFT, P50/P95, VRAM/RAM, consumo e logs. O resultado deve ser anexado à ficha do modelo e ao registro de benchmark.

## Por que não inventar números

Desempenho depende de implementação e ambiente. O vault pode oferecer comandos reproduzíveis e uma matriz de aceitação, mas não deve atribuir tokens/s a uma máquina que não foi medida. Resultados editoriais permanecem marcados como externos.
