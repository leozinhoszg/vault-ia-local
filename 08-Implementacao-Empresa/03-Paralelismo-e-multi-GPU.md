# Paralelismo e multi-GPU

## Tensor parallelism (TP)

TP divide tensores de uma camada entre GPUs. É apropriado quando uma camada ou o modelo não cabe em uma GPU e quando a interconexão entre GPUs é rápida. Cada token exige comunicação coletiva, então latência de PCIe pode limitar muito o ganho.

## Pipeline parallelism (PP)

PP divide camadas inteiras em estágios. Reduz a memória por GPU e pode usar GPUs com menos comunicação por camada, mas introduz bolhas de pipeline e pode elevar latência de uma única sequência. Batch maior amortiza melhor o custo.

## PCIe, NVLink e rede

| Interconexão | Uso | Efeito prático |
|---|---|---|
| PCIe 4/5 | GPU-host e GPU-GPU via P2P | Adequado para algumas divisões, mas pode ser gargalo. |
| NVLink/NVSwitch | GPUs NVIDIA suportadas | Reduz custo de comunicação; confirme suporte no SKU/runtime. |
| NUMA | CPU/socket/memória local | Prenda processos e memória ao nó correto; evite tráfego remoto. |
| InfiniBand | Cluster com baixa latência e RDMA | Preferível para treinamento e serving distribuído exigente. |
| RoCE | Ethernet com RDMA | Mais acessível, mas exige configuração lossless, PFC/ECN e operação madura. |

Não some VRAM como se fosse uma única memória automaticamente. O runtime precisa implementar sharding. Em GPUs heterogêneas, a partição tende a ser limitada pela GPU mais lenta ou menor.

## Diagnóstico

```bash
nvidia-smi topo -m
nvidia-smi p2p -p 0,1
numactl --hardware
ibstat
rdma link
```

Meça modelo inteiro em uma GPU, TP=2, PP=2 e offload para CPU. Compare tokens/s, TTFT, memória, largura de banda, uso de PCIe e estabilidade. Escolha a topologia pelo benchmark, não pelo número de GPUs.

**Referências**

[1]: https://docs.vllm.ai/en/latest/serving/parallelism_scaling.html "vLLM — distributed inference"
[2]: https://docs.nvidia.com/nvidia-hpc-benchmarks/NVLink_Benchmarks.html "NVIDIA — NVLink benchmarks"
[3]: https://docs.nvidia.com/networking/display/ibta "InfiniBand Trade Association"
