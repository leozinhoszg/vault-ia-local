> **Nota canônica:** a explicação aprofundada e os critérios de escolha estão em [[05-Memoria-e-Performance/Quantizacao-livro]]. Esta nota é um resumo de referência rápida.

# Quantização e FP4

Quantização representa pesos e/ou ativações com menos bits. INT4 usa valores inteiros com escalas; FP4 usa uma mini representação de ponto flutuante. A qualidade depende de granulação, escalas, outliers, calibração e compatibilidade do kernel.

A NVIDIA descreve NVFP4 como E2M1 com escala FP8 compartilhada por blocos de 16 valores e um fator FP32 por tensor. O objetivo é reduzir erro em relação a formatos mais grosseiros. Blackwell oferece aceleração nativa para FP4, FP6, FP8 e outros formatos [1].

| Formato | Ideia | Onde usar |
|---|---|---|
| FP16/BF16 | Alta qualidade e treino estável | Fine-tuning, baseline e modelos menores. |
| INT8/FP8 | Compromisso de qualidade e memória | Serving e treino/inferência modernos. |
| INT4/GGUF Q4 | Grande economia e ampla compatibilidade | PCs, workstations e CPU+GPU. |
| FP4/NVFP4/MXFP4 | Ultra-baixa precisão com escalas especializadas | Hardware e kernels compatíveis, sobretudo Blackwell. |

**Não confunda:** um arquivo Q4 de GGUF e um checkpoint NVFP4 não são automaticamente intercambiáveis. Use o formato esperado pelo runtime e valide qualidade no seu conjunto de testes.

## Referência

[1]: https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/ "NVIDIA: Introducing NVFP4"
