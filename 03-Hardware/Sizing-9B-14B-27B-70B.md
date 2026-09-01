# Sizing prático: 9B, 14B, 27B e 70B

## A distinção mais importante

**Carregar** significa alocar pesos, tokenizer e estruturas iniciais. **Rodar** significa carregar o modelo e ainda ter memória para KV cache, ativações, workspace, runtime, sistema operacional e margem. Uma máquina pode carregar um arquivo e falhar na primeira geração, no aumento do contexto ou quando chega o segundo usuário.

As estimativas desta nota assumem modelos densos, quantização típica de 4 bits e uma sessão curta. Modelos MoE devem ser dimensionados pelos **parâmetros totais armazenados**, não apenas pelos parâmetros ativos. Modelos multimodais precisam de memória adicional para encoder, projetor e tokens visuais.

## Memória dos pesos e memória operacional

| Tamanho | FP16/BF16 — pesos crus | Q8/INT8 — estimativa de arquivo | Q4/INT4 — estimativa de arquivo | Memória recomendada para rodar Q4 com folga |
|---:|---:|---:|---:|---:|
| 9B | ~18 GB | ~9–11 GB | ~5–7 GB | 8–12 GB |
| 14B | ~28 GB | ~14–17 GB | ~8–10 GB | 12–16 GB |
| 27B | ~54 GB | ~27–32 GB | ~15–19 GB | 20–24 GB |
| 70B | ~140 GB | ~70–82 GB | ~38–48 GB | 48–64 GB |

Os valores Q4 incluem uma faixa para escalas, metadados, alinhamento e variações de quantizador; não são uma promessa de tamanho exato. O cálculo teórico de 0,5 byte por parâmetro é apenas o piso. A folga recomendada pressupõe contexto moderado, normalmente 4K–8K, uma sessão e backend eficiente.

## O que cada classe de máquina consegue fazer

| Classe de máquina | 9B | 14B | 27B | 70B |
|---|---|---|---|---|
| CPU moderna, 16 GB RAM, sem GPU | Roda Q4, lento a moderado | Carrega Q4; roda lento | Geralmente não recomendada | Não recomendada |
| CPU moderna, 32 GB RAM, sem GPU | Roda bem para uso pessoal | Roda Q4 com paciência | Roda Q4, mas geralmente lento | Pode carregar Q4 em alguns casos, porém lento e sem folga |
| GPU 8 GB VRAM + 32 GB RAM | Roda Q4 com offload parcial | Roda com offload parcial | Roda com offload parcial, baixa velocidade | Não é uma boa configuração |
| GPU 12 GB VRAM + 32 GB RAM | Roda bem Q4 | Roda Q4 com offload parcial | Roda com offload parcial | Não recomendada |
| GPU 16 GB VRAM + 32–64 GB RAM | Roda bem Q4/Q5 | Roda bem Q4 | Roda Q4 com offload parcial | Não cabe integralmente |
| GPU 24 GB VRAM + 64 GB RAM | Roda muito bem | Roda muito bem | Roda Q4/Q5 com pequena folga | Roda com offload para RAM, mas não com boa performance |
| GPU 32 GB VRAM + 64 GB RAM | Roda muito bem | Roda muito bem | Roda bem Q4/Q5 | Roda Q4 com offload para RAM; performance depende da banda |
| 2×24 GB VRAM + 96–128 GB RAM | Excelente | Excelente | Excelente | Roda Q4 com divisão entre GPUs e/ou RAM |
| 48–64 GB VRAM + 128 GB RAM | Excelente | Excelente | Excelente | Configuração indicada para 70B Q4 |
| 80 GB VRAM + 128–256 GB RAM | Excelente | Excelente | Excelente | Muito boa para 70B Q4/Q5 e contexto maior |
| Apple Silicon 64 GB unificados | Excelente | Excelente | Boa | Q4 pode rodar, mas a banda e o contexto definem a experiência |
| Apple Silicon 128 GB unificados | Excelente | Excelente | Excelente | Boa opção silenciosa para 70B Q4, respeitando banda e temperatura |

“Roda” nesta tabela significa geração funcional, não necessariamente velocidade de produção. Para uso multiusuário, acrescente memória e prefira serving com batching contínuo, como vLLM em GPUs suportadas.

## Recomendações por tamanho

### Modelos 9B

Para uma experiência pessoal confortável, a configuração indicada é **16–32 GB de RAM e GPU com 8–12 GB de VRAM**. Uma GPU de 12 GB permite manter mais camadas no acelerador e normalmente é preferível a uma GPU muito rápida com apenas 8 GB. Sem GPU, um CPU moderno com 32 GB de RAM roda Q4 para chat, automação e RAG de baixa concorrência.

Use Q4 ou Q5 para começar. Q8 e FP16 fazem sentido quando a qualidade adicional foi medida e há memória disponível. Para 32K ou mais de contexto, não dimensione apenas pelo arquivo: o KV cache pode consumir vários gigabytes.

### Modelos 14B

A configuração equilibrada é **32 GB de RAM e 12–16 GB de VRAM**. Uma GPU de 16 GB costuma permitir uma experiência mais consistente em Q4, enquanto 12 GB pode exigir offload para RAM, redução de contexto ou quantização mais agressiva. Uma máquina somente CPU com 32–64 GB de RAM consegue executar, mas a velocidade pode ser insuficiente para uso conversacional intenso.

Para coding e RAG, 14B costuma ser uma classe interessante: ainda cabe em uma workstation pessoal, mas oferece mais capacidade que 7–9B. Valide latência com o seu tokenizer e contexto reais.

### Modelos 27B

Para boa performance, indique **24 GB de VRAM, 64 GB de RAM e SSD NVMe**. Uma GPU de 16 GB pode rodar Q4 com offload para RAM, porém a troca entre VRAM e RAM reduz a velocidade. Duas GPUs totalizando 32–48 GB ou uma GPU com 32 GB são opções mais confortáveis.

Em Apple Silicon, 64 GB unificados é um ponto de entrada prático e 96–128 GB oferece mais margem. A memória unificada não transforma automaticamente o sistema em uma GPU dedicada: CPU, GPU e sistema compartilham capacidade e banda.

### Modelos 70B

Para **boa performance**, a recomendação principal é **48–64 GB de memória de acelerador efetivamente utilizável**, mais **128 GB de RAM**, SSD NVMe e fonte/refrigeração apropriadas. Isso pode ser uma GPU de 48–64 GB, duas GPUs de 24–32 GB ou um servidor com múltiplas GPUs.

Com Q4, o arquivo costuma ficar próximo de 40–48 GB, mas ainda são necessários KV cache, workspace e folga. Por isso, uma única GPU de 24 GB não é uma configuração de boa performance para 70B: ela dependerá fortemente de RAM e/ou ficará sem memória ao aumentar o contexto. Uma workstation com 64–128 GB de RAM pode executar 70B Q4 em CPU ou híbrido, mas a experiência será limitada pela largura de banda da RAM.

Apple Silicon com **128 GB de memória unificada** é uma opção doméstica silenciosa para 70B Q4, desde que o usuário aceite velocidade inferior a uma solução multi-GPU dedicada em vários cenários. Para contexto grande ou múltiplos usuários, prefira servidor com HBM/VRAM suficiente.

## “Minha máquina consegue?” — procedimento objetivo

Preencha este inventário antes de baixar um modelo:

| Item | Seu valor |
|---|---|
| Sistema operacional | |
| CPU e número de threads | |
| RAM total e RAM livre | |
| GPU / NPU | |
| VRAM dedicada ou memória unificada | |
| Largura de banda da memória, se conhecida | |
| Espaço livre no SSD | |
| Fonte de alimentação e refrigeração | |
| Runtime e versão | |
| Modelo, quantização e contexto desejados | |

No Linux, execute:

```bash
lscpu
free -h
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
nvidia-smi                         # se houver NVIDIA
rocminfo | head -80                # se houver AMD/ROCm
lspci | grep -Ei 'vga|3d|display'
```

No Windows, consulte o Gerenciador de Tarefas em **Desempenho** e registre CPU, memória, GPU e memória dedicada/compartilhada. No macOS, use **Sobre Este Mac** e registre o chip e a memória; em Apple Silicon, a memória é compartilhada.

Depois compare:

1. **Espaço em disco:** mantenha pelo menos duas vezes o tamanho do arquivo durante download, conversão e atualização.
2. **Memória:** pesos quantizados + KV cache + buffers + sistema devem ficar abaixo da memória disponível, com 20–30% de margem.
3. **Acelerador:** confirme se o runtime usa CUDA, Metal, HIP, Vulkan, SYCL ou OpenVINO em vez de cair silenciosamente para CPU.
4. **Contexto:** repita o teste no contexto real. Dobrar ou quadruplicar contexto pode alterar significativamente o KV cache.
5. **Velocidade:** meça TTFT e tokens/s de decode. “Carregou” sem medir geração não é aprovação.
6. **Estabilidade:** faça um teste de 10–20 minutos e observe OOM, temperatura, throttling e consumo.

## Teste mínimo de aceitação

```bash
# Ollama: substitua pelo modelo escolhido
ollama run NOME_DO_MODELO

# llama.cpp: ajuste o caminho e o número de camadas offload
./llama-cli -m ./models/model.gguf -ngl 999 -c 4096 -n 256 \
  -p "Responda em português e explique o resultado em cinco linhas."
```

Se ocorrer OOM, reduza nesta ordem: contexto, batch, número de sequências, precisão do KV cache, quantização dos pesos e número de camadas no acelerador. Se a execução ficar lenta depois do offload parcial, isso é esperado: a memória do sistema tem banda muito menor que VRAM/HBM em muitos equipamentos.

*Última atualização: 2026-09-01. Próxima revisão: 2026-10-01.*

## Referências

[1]: https://github.com/ggml-org/llama.cpp "llama.cpp: backends, quantização e CPU+GPU híbrida"
[2]: https://huggingface.co/docs/transformers/en/quantization/bitsandbytes "Hugging Face: quantização em 8 e 4 bits"
[3]: https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/ "NVIDIA: formatos FP4 e memória"
[4]: https://docs.vllm.ai/ "vLLM: serving e batching"
[5]: https://ai.meta.com/blog/llama-4-multimodal-intelligence/ "Meta: parâmetros ativos e totais em Llama 4"
