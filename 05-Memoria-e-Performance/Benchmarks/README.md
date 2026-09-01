# P0 — Benchmark real por hardware e modelo

**Objetivo:** substituir tetos teóricos por medições reproduzíveis de inferência local. Nenhum número deve ser registrado sem modelo, arquivo/hash, quantização, contexto, runtime, driver, hardware, temperatura e potência.

## Fluxo

1. Escolha uma ficha de modelo e um hardware.
2. Registre o arquivo exato e seu SHA-256.
3. Faça aquecimento e execute o harness cinco vezes.
4. Separe prompt processing de decode.
5. Registre TTFT, P50/P95, tokens/s, VRAM/RAM, temperatura e potência na tomada.
6. Execute o teste de qualidade correspondente.
7. Grave uma linha em `results.csv` e um relatório Markdown com stdout/stderr.

O arquivo `results.csv` começa vazio de propósito. Não há benchmarks sintéticos ou números inventados. A coluna `status` deve ser `measured`, `failed` ou `not_run`; `estimated` não pode ser usado como medição.

## Unidade mínima de comparação

| Campo | Obrigatório |
|---|---|
| Modelo e revisão | Nome, versão, repositório e hash do arquivo |
| Precisão | GGUF/GPTQ/AWQ/NF4/FP8/FP4 e variante exata |
| Hardware | GPU/CPU/APU, VRAM/RAM e número de dispositivos |
| Software | SO, kernel, driver, CUDA/ROCm/Metal, runtime e versão |
| Carga | prompt tokens, geração, contexto, batch e concorrência |
| Resultado | TTFT, P50/P95, prompt tok/s, decode tok/s, energia e temperatura |
| Qualidade | dataset, seed, pass@k/accuracy/groundedness e falhas |

## Referências

[1]: https://github.com/ggml-org/llama.cpp "llama.cpp e llama-bench"
[2]: https://docs.vllm.ai/ "vLLM"
[3]: https://www.mlperf.org/ "MLPerf"
