# GPU vs CPU vs NPU

## GPU

GPU é normalmente a opção mais simples para LLM local porque oferece paralelismo massivo, kernels maduros e memória dedicada de alta banda. NVIDIA tende a ter a cobertura mais ampla; AMD, Apple Metal, Intel SYCL/OpenVINO e Vulkan podem ser excelentes quando o modelo e o runtime suportam o caminho escolhido.

## CPU

CPU é adequada para modelos pequenos, baixa concorrência, fallback e máquinas sem GPU. AVX2/AVX-512/AMX em x86 e NEON/Accelerate em ARM podem acelerar operações. O gargalo frequente é a largura de banda da RAM, não apenas o número de núcleos.

## NPU

NPU é um acelerador especializado com eficiência energética atraente para modelos e operadores suportados. Use-o para tarefas de borda, voz e visão quando o compilador/runtime tiver suporte real. Valide conversão, precisão, operadores ausentes, memória compartilhada e fallback para CPU/GPU.

| Pergunta | GPU | CPU | NPU |
|---|---|---|---|
| Flexibilidade de modelos | Alta | Alta | Média/baixa |
| Ecossistema LLM | Alto, depende do fornecedor | Muito alto | Em evolução |
| Eficiência em workload compatível | Alta | Média | Muito alta |
| Facilidade de depuração | Alta | Alta | Menor |

Para entender o que cada peça faz em cada momento da geração e o que mais VRAM, RAM ou CPU compram (ou não), veja [[03-Hardware/Por-que-VRAM-RAM-e-CPU-importam]] e [[01-Fundamentos/Carregar-um-peso]].
