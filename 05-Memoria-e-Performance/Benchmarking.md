# Benchmarking

Faça benchmark em três níveis: microbenchmark do runtime, benchmark do modelo e teste de aceitação do produto. Fixe modelo, quantização, contexto, temperatura, top-p, número de threads, offload, batch, concorrência e versão do driver.

```bash
# Exemplo conceitual; adapte ao runtime e ao modelo
llama-bench -m models/model.gguf -p 512 -n 128
curl http://localhost:8000/metrics
```

Registre resultados em CSV ou Markdown, incluindo data, commit, hardware, temperatura e consumo. Um benchmark útil também mede falhas: OOM, timeouts, respostas malformadas, alucinação, recusas incorretas e degradação em contexto longo.
