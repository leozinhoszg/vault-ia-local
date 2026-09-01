# Matriz de hardware

A escolha deve começar por memória disponível, largura de banda, suporte de kernel, energia e manutenção. TOPS de NPU geralmente mede operações de baixa precisão em condições específicas; não é equivalente a tokens/s de LLM.

| Plataforma | Quando escolher | Limitação típica |
|---|---|---|
| NVIDIA RTX com 12–24 GB VRAM | Melhor ecossistema CUDA, prototipagem e inferência pessoal | VRAM limita modelo/contexto; consumo e preço. |
| NVIDIA workstation/data center | Multiusuário, throughput, vLLM/TensorRT-LLM | Custo de aquisição, refrigeração e energia. |
| AMD Radeon/Instinct | Boa capacidade de memória e alternativa ao CUDA | Compatibilidade ROCm varia por GPU, SO e kernel. |
| Apple Silicon | Silêncio, memória unificada, ARM/Metal, boa experiência pessoal | Memória não é VRAM dedicada; upgrade impossível após compra. |
| Intel GPU/NPU | Integração com OpenVINO e edge corporativo | Cobertura de modelos e desempenho devem ser testados. |
| CPU x86 com muita RAM | Modelo pequeno, batch baixo, servidor barato | Banda e paralelismo geralmente inferiores à GPU. |
| ARM SBC/mini-PC | Edge, automação e consumo baixo | RAM, térmica e suporte de kernels limitados. |
| NPU de notebook/SoC | Voz, visão e tarefas quantizadas eficientes | Runtimes, operadores e modelos compatíveis são restritos. |

**Regra de sizing:** para inferência interativa, reserve memória para pesos + KV cache + buffers + SO. A capacidade nominal nunca deve ser usada a 100%. Veja [[03-Hardware/Calculadora-de-memoria]].

**Referências**

[1]: https://github.com/ggml-org/llama.cpp "Backends do llama.cpp"
[2]: https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/ "NVIDIA: NVFP4"
