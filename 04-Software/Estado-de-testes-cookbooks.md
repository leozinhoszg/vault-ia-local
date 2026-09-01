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
| RAG local | `--selftest` executado em 2026-09-01: Windows 11 Pro, Python 3.11.9, chromadb 1.0.20, pypdf 6.0.0, numpy 2.4.6 (venv isolado); resultado `SELFTEST OK`, exit 0. Cobre chunking, Chroma, recuperação e formato `[Fonte N]` com embedding determinístico; **não** cobre embedding real nem Ollama. Durante o teste foi corrigido um `PermissionError` de limpeza de diretório temporário específico do Windows. | Executar ingestão com `sentence-transformers`, geração via Ollama, citação real e avaliação (recall@k, groundedness) em máquina com GPU/Ollama; registrar em [[99-Templates/Registro-de-benchmark]]. |

## Registro obrigatório

Preencha hardware, OS, kernel, driver, runtime, modelo, hash, quantização, contexto, prompt, temperatura, seed, tokens/s, TTFT, P50/P95, VRAM/RAM, consumo e logs. O resultado deve ser anexado à ficha do modelo e ao registro de benchmark.

## Por que não inventar números

Desempenho depende de implementação e ambiente. O vault pode oferecer comandos reproduzíveis e uma matriz de aceitação, mas não deve atribuir tokens/s a uma máquina que não foi medida. Resultados editoriais permanecem marcados como externos.
