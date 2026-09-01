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
| RAG local | Script Python compilado estaticamente pelo validador; dependências não instaladas neste sandbox | Executar ingestão, recuperação, citação e avaliação. |

## Registro obrigatório

Preencha hardware, OS, kernel, driver, runtime, modelo, hash, quantização, contexto, prompt, temperatura, seed, tokens/s, TTFT, P50/P95, VRAM/RAM, consumo e logs. O resultado deve ser anexado à ficha do modelo e ao registro de benchmark.

## Por que não inventar números

Desempenho depende de implementação e ambiente. O vault pode oferecer comandos reproduzíveis e uma matriz de aceitação, mas não deve atribuir tokens/s a uma máquina que não foi medida. Resultados editoriais permanecem marcados como externos.
