# Cenários de infraestrutura

As faixas abaixo são **ordens de grandeza para planejamento**, não cotação, e variam muito por país e data.

| Cenário | Hardware típico | Faixa indicativa de CAPEX | Uso |
|---|---|---:|---|
| Casa econômica | CPU/mini-PC, 16–32 GB RAM, SSD, sem GPU forte | US$ 300–900 | 1–8B quantizado, embeddings e automação. |
| Casa acelerada | GPU 12–24 GB ou Apple/ARM com 32–64 GB | US$ 900–3.500 | 7–32B quantizado, RAG pessoal, coding. |
| Workstation | 64–192 GB RAM, uma ou mais GPUs | US$ 3.500–15.000 | Modelos maiores, fine-tuning de adapters, poucos usuários. |
| Servidor empresarial | 1–8 GPUs data center, rede rápida, storage e UPS | US$ 20.000–250.000+ | Serving multiusuário, SLA e throughput. |
| Rack/cluster | Vários nós, fabric de rede, energia e refrigeração | US$ 250.000+ | Treino e inferência de escala. |

Uma alternativa é serviço gerenciado ou nuvem privada, pagando por uso e reduzindo manutenção. Porém, verifique residência de dados, retenção, treinamento sobre seus dados, SLA e saída de dados.

## Como usar estas faixas

As cinco faixas acima são apenas envelopes iniciais. Para uma composição concreta de CPU, placa-mãe, RAM, GPU, PSU, SSD, consumo e modelos viáveis, consulte [[03-Hardware/Builds-brasileiros-por-orcamento]]. Para calcular energia, câmbio, impostos, garantia, depreciação e break-even entre máquina própria e API, consulte [[09-Servicos-e-Custos/Servicos-comerciais-e-break-even]].

O orçamento final deve registrar a data, três cotações brasileiras, frete, impostos, garantia, consumo medido na tomada, disponibilidade de peças, risco de GPU usada e a classe de modelos que será executada. Uma build barata que não consiga manter os pesos e o KV cache na memória disponível pode ter custo efetivo maior devido à baixa produtividade.
