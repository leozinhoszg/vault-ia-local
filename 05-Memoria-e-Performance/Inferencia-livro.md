# Inferência local — capítulo completo

## 1. O que acontece durante uma geração

Inferência é executar um modelo treinado para produzir uma saída. No prompt inicial ocorre o **prefill**: todos os tokens de entrada são processados e o KV cache é criado. Depois ocorre o **decode**: em geral, um token por passo, reutilizando o cache. Prefill costuma ser limitado por computação e paralelismo; decode frequentemente é limitado por largura de banda e movimentação de pesos.

O tempo até o primeiro token é TTFT. A velocidade durante a resposta é decode tokens/s. Throughput do servidor mede tokens/s agregados entre usuários; não substitui latência de uma sessão. Sempre reporte p50/p95 e o contexto usado.

## 2. Carregar não é executar bem

Carregar significa alocar pesos, tokenizer, buffers e parte do cache. Executar bem requer memória livre para o contexto, largura de banda, kernels, threads, afinidade, temperatura e ausência de swapping. Um modelo pode iniciar com 8 GB livres e falhar quando o contexto cresce.

Uma aproximação é `memória_total = pesos_quantizados + KV_cache + workspace + overhead + margem`. Use margem de 10–30%; para servidor multiusuário, reserve pelo pior número de sequências e contexto.

## 3. CPU, GPU e híbrido

CPU é flexível e pode usar RAM grande, mas decode costuma ser mais lento. GPU acelera por paralelismo e banda de memória, desde que os pesos e cache caibam. Offload CPU/GPU permite executar modelos maiores, porém transfere dados pelo PCIe e pode reduzir drasticamente tokens/s. Apple Silicon usa memória unificada e exige atenção a pressão de memória do sistema.

## 4. Configuração e benchmark

Fixe modelo, quantização, contexto, temperatura, seed, prompt e runtime. Registre CPU, GPU, VRAM, RAM, driver, backend e número de threads. Execute três classes: prompt curto/saída curta, contexto longo e concorrência.

```bash
# Ollama
ollama run qwen3.6:27b
ollama ps
nvidia-smi

# llama.cpp, exemplo conceitual
./llama-bench -m model-Q4_K_M.gguf -p 512 -n 128
./llama-cli -m model-Q4_K_M.gguf -ngl 99 -c 8192 -p "Explique este repositório."
```

Não compare números de fontes diferentes sem verificar versão, prompt, contexto, quantização e hardware. Um benchmark de uma única sequência não representa um endpoint de agentes.

## 5. Falhas comuns

OOM de GPU exige reduzir contexto, quantizar pesos/KV, reduzir concorrência ou fazer offload. OOM de RAM exige mais RAM, menor modelo ou menos workers. Baixa utilização de GPU pode indicar offload excessivo, tokenização, sincronização, kernel ausente ou CPU lenta. Tokens/s instáveis podem indicar throttling térmico, swap ou disputa com outros processos.

## 6. Servidor

Para uma máquina pessoal, Ollama/LM Studio/llama.cpp reduzem complexidade. Para API multiusuário, vLLM, SGLang ou outro servidor com batching e paged attention tendem a ser mais apropriados quando o modelo e o hardware são suportados. Exponha autenticação, limites, logs mínimos, timeouts e health checks.

## 7. Inferência reprodutível

Versione o model ID, hash/commit, arquivo de quantização, prompt de sistema, parâmetros de amostragem, ferramentas e corpus RAG. Armazene apenas os logs necessários e remova segredos. Um resultado local só é auditável se outra pessoa consegue reconstruir o ambiente.

## Referências

[1]: https://github.com/ggml-org/llama.cpp "llama.cpp"
[2]: https://docs.vllm.ai/ "vLLM"
[3]: https://docs.sglang.ai/ "SGLang"
[4]: https://github.com/ollama/ollama "Ollama"
