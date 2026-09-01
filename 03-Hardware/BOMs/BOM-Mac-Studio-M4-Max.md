# BOM — Apple Mac Studio M4 Max

**Estado:** `draft` — transformar em `quoted` somente após cotação brasileira datada.
**Data do registro:** 2026-09-01
**Objetivo:** IA local; modelo-alvo: 8B–70B conforme MLX/Metal e contexto.

| Campo | Valor |
|---|---|
| GPU/plataforma | Apple Mac Studio M4 Max |
| SKU/MPN exato | Mac Studio M4 Max, 16-core CPU, 40-core GPU, 64 GB unified memory, 2 TB SSD (part number Apple Brasil a confirmar no carrinho) |
| Memória | 64 ou 128 GB unified |
| Potência de referência | TDP de chip não publicado na fonte |
| Preço à vista (R$) | PENDENTE — cotar |
| Preço parcelado (R$) | PENDENTE — cotar |
| Frete/impostos | PENDENTE — registrar |
| Vendedor/CNPJ | PENDENTE — registrar |
| URL da oferta | PENDENTE — registrar |
| Data/hora da cotação | PENDENTE — registrar |
| Garantia | PENDENTE — registrar |

## Componentes obrigatórios

| Componente | SKU exato | Preço R$ | URL/data | Verificação técnica |
|---|---|---:|---|---|
| CPU | Apple M4 Max, 16-core CPU | consultar | https://www.apple.com/br/mac-studio/ | SoC integrado; sem PCIe/upgrade |
| Placa-mãe | Apple Mac Studio logic board integrada | incluída | https://www.apple.com/br/mac-studio/ | plataforma fechada; sem bifurcação PCIe |
| RAM | 64 GB unified memory (opção Apple) | consultar | https://www.apple.com/br/shop/buy-mac/mac-studio | memória integrada; não expansível |
| GPU/plataforma | Mac Studio M4 Max, 16-core CPU, 40-core GPU, 64 GB unified memory, 2 TB SSD (part number Apple Brasil a confirmar no carrinho) | PENDENTE | PENDENTE | memória, conectores, espessura e backend |
| PSU | Fonte interna Apple Mac Studio | incluída | https://www.apple.com/br/mac-studio/ | consumo deve ser medido na tomada |
| Cooler/gabinete | Chassi e refrigeração Apple Mac Studio | incluído | https://www.apple.com/br/mac-studio/ | validar ruído e sustentação térmica em benchmark |
| SSD | Apple 2 TB integrado | consultar | https://www.apple.com/br/shop/buy-mac/mac-studio | não substituível pelo usuário |
| UPS/rede | APC Smart-UPS 1500 VA + Ethernet 2,5 GbE | cotar | https://www.apc.com/br/ | validar autonomia e throughput |

## Aprovação

A BOM não está aprovada para compra. Falta cotar SKU, vendedor, preço, frete, garantia e confirmar a combinação de hardware/software. Após preencher, calcular TCO em [[09-Servicos-e-Custos/Guia-financeiro-TCO-local-vs-OpenAI]] e executar benchmark em [[05-Memoria-e-Performance/Benchmarks/README]].

## Referências

[1]: https://www.nvidia.com/ "NVIDIA — especificações oficiais"
[2]: https://www.amd.com/ "AMD — especificações oficiais"
[3]: https://www.apple.com/br/shop/buy-mac/mac-studio "Apple Brasil — compra do Mac Studio"
