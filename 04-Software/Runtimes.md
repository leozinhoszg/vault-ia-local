# Runtimes e ferramentas

| Ferramenta | Melhor uso | Interface / backend |
|---|---|---|
| llama.cpp | Uma máquina, GGUF, CPU+GPU híbrido, edge | CLI e servidor compatível com OpenAI; CUDA, Metal, HIP, Vulkan, SYCL, OpenVINO e outros. |
| Ollama | Primeiro contato e API local simples | Gerência de modelos e serviço local; ideal para desenvolvimento. |
| LM Studio | Desktop com UI e experimentação | GGUF e backends conforme plataforma. |
| Transformers | Pesquisa, avaliação, treinamento e máxima flexibilidade | PyTorch; checkpoints HF. |
| vLLM | API multiusuário e alto throughput em GPU | PagedAttention, batching contínuo e API compatível com OpenAI. |
| SGLang | Serving e workflows estruturados/agentic | GPU, otimizações específicas. |
| TensorRT-LLM | NVIDIA e produção otimizada | CUDA/TensorRT; exige validação e build por modelo. |
| OpenVINO | Intel CPU/GPU/NPU e edge | Conversão e execução com plugins Intel. |
| MLX | Apple Silicon | Treinamento e inferência nativos em memória unificada. |
| LiteRT/ONNX Runtime | Edge e modelos convertidos | Depende do operador e provedor de execução. |

Comece com o runtime que reduz risco operacional. Trocar para vLLM ou TensorRT-LLM faz sentido quando métricas mostram que throughput, concorrência ou latência justificam a complexidade.

**Referências**

[1]: https://github.com/ggml-org/llama.cpp "llama.cpp"
[2]: https://docs.vllm.ai/ "vLLM documentation"
[3]: https://huggingface.co/docs/transformers/index "Hugging Face Transformers"
[4]: https://github.com/openvinotoolkit/openvino "OpenVINO"
[5]: https://github.com/ml-explore/mlx "Apple MLX"
