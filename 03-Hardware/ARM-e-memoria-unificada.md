# ARM e memória unificada

ARM aparece em Apple Silicon, Snapdragon, servidores e edge. O conjunto de instruções, o runtime e a topologia de memória são mais importantes que o rótulo ARM. Apple Silicon combina CPU, GPU e aceleradores com memória unificada; isso permite carregar modelos maiores que caberiam em uma VRAM dedicada equivalente, mas CPU e GPU competem pela mesma banda e capacidade.

A arquitetura ARM é atraente para uso pessoal silencioso, aplicações sempre ligadas e edge. Para empresa, verifique disponibilidade, virtualização, imagens Docker multi-arquitetura, bibliotecas nativas, observabilidade e suporte do fornecedor.

O llama.cpp declara suporte de primeira classe a Apple Silicon via NEON, Accelerate e Metal e também mantém backends para CUDA, HIP, SYCL, OpenVINO, Vulkan e outros [1].

**Referência**

[1]: https://github.com/ggml-org/llama.cpp "llama.cpp: descrição e backends"
