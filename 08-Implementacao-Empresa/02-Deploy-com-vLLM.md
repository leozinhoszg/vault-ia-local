# Deploy com vLLM

vLLM é adequado quando a prioridade é servir uma API compatível com OpenAI em GPU, com batching contínuo e concorrência. Fixe versões de CUDA, driver, container e modelo. Não exponha a porta diretamente.

```bash
# Exemplo de laboratório; em produção use secrets manager e imagem fixada
docker run --gpus all --ipc=host --shm-size=16g \
  -p 127.0.0.1:8000:8000 \
  -v $HOME/.cache/huggingface:/root/.cache/huggingface \
  vllm/vllm-openai:latest \
  --model Qwen/Qwen3.8-27B --served-model-name local-qwen
```

Em produção, substitua `latest` por digest, configure autenticação no gateway, health checks, timeouts, max model length, limites de concorrência, métricas e estratégia de rollout. Faça benchmark com o mesmo hardware e contexto do piloto.

**Referências**

[1]: https://docs.vllm.ai/ "vLLM documentation"
[2]: https://huggingface.co/Qwen/Qwen3.8-27B "Qwen3.8 model card com exemplo vLLM"
