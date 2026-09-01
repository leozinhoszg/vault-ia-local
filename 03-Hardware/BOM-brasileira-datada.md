# BOM brasileira datada

> **Regra:** esta é uma ficha de aquisição, não uma lista genérica. Preencha preço observado, vendedor, data, garantia e URL. Sem esses campos, a linha não é aprovada para compra.

| Campo | Valor a preencher |
|---|---|
| Data da cotação | AAAA-MM-DD |
| Região/UF | A preencher |
| Objetivo | Modelo, quantização, contexto, usuários e SLO |
| CAPEX aprovado | R$ |
| Câmbio de referência | R$/US$ e fonte |
| Tarifa de energia | R$/kWh e distribuidora |

## Componentes

| Item | Marca/modelo exato | Quantidade | Preço unit. | Total | URL | Garantia |
|---|---|---:|---:|---:|---|---|
| CPU | A preencher | 1 | R$ | R$ | URL | meses |
| Placa-mãe | A preencher | 1 | R$ | R$ | URL | meses |
| RAM | capacidade/tipo/kit | 1 | R$ | R$ | URL | meses |
| GPU | SKU, VRAM, espessura | 1 | R$ | R$ | URL | meses |
| PSU | watts, padrão, conectores | 1 | R$ | R$ | URL | meses |
| Cooler | modelo | 1 | R$ | R$ | URL | meses |
| Gabinete | espaço e airflow | 1 | R$ | R$ | URL | meses |
| SSD | capacidade/endurance | 1 | R$ | R$ | URL | meses |
| UPS | VA/W, autonomia | 1 | R$ | R$ | URL | meses |
| Rede | NIC/switch/cabos | 1 | R$ | R$ | URL | meses |

## Verificações técnicas

Registre socket e BIOS, canais de memória, lanes PCIe reais e bifurcação, distância entre slots, conectores, pico da PSU, fluxo de ar, tomada/circuito, ruído, temperatura, CUDA/ROCm/Metal e modelo quantizado testado. Para duas GPUs, indique se há P2P e se o runtime suporta sharding.

## Aprovação

A build só passa quando o modelo cabe com pesos + KV cache + margem, o benchmark atende o SLO, a PSU e refrigeração suportam a carga, a garantia está documentada e o TCO foi comparado à API em [[09-Servicos-e-Custos/Guia-financeiro-TCO-local-vs-OpenAI]].
