# BOM — NVIDIA RTX 4090

**Estado:** `draft` — transformar em `quoted` somente após cotação brasileira datada.
**Data do registro:** 2026-09-01
**Objetivo:** IA local; modelo-alvo: 8B/14B/27B Q4; 70B com multi-GPU/offload.

| Campo | Valor |
|---|---|
| GPU/plataforma | NVIDIA RTX 4090 |
| SKU/MPN exato | ASUS TUF-RTX4090-O24G-GAMING (24 GB; confirmar disponibilidade e revisão) |
| Memória | 24 GB GDDR6X |
| Potência de referência | 450 W de referência da placa |
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
| CPU | AMD Ryzen 9 9950X (100-100000277WOF) | PENDENTE | PENDENTE | lanes, consumo e suporte |
| Placa-mãe | ASUS ProArt X870E-CREATOR WIFI | cotar | https://www.asus.com/motherboards-components/motherboards/proart/proart-x870e-creator-wifi/ | AM5, PCIe x16, bifurcação e rede |
| RAM | Kingston Fury Beast KF560C36BBEK2-64 (64 GB DDR5-6000) | cotar | https://www.kingston.com/en/memory/gaming/kingston-fury-beast-ddr5-memory | 2 DIMMs; validar QVL |
| GPU/plataforma | ASUS TUF-RTX4090-O24G-GAMING (24 GB; confirmar disponibilidade e revisão) | PENDENTE | PENDENTE | memória, conectores, espessura e backend |
| PSU | Corsair HX1500i (CP-9020259) | cotar | https://www.corsair.com/ | ATX 3.x; margem para 450 W e picos |
| Cooler/gabinete | Arctic Liquid Freezer III 360 + Fractal Meshify 2 XL | cotar | https://www.arctic.de/ / https://www.fractal-design.com/ | compatibilidade AM5, radiador e espessura da GPU |
| SSD | Samsung 990 PRO 2 TB (MZ-V9P2T0BW) | cotar | https://semiconductor.samsung.com/consumer-storage/internal-ssd/990-pro/ | NVMe PCIe 4.0; modelos e datasets |
| UPS/rede | APC Smart-UPS SRT 2200 VA + Ethernet 2,5 GbE | cotar | https://www.apc.com/br/ | validar autonomia sob carga e throughput |

## Aprovação

A BOM não está aprovada para compra. Falta cotar SKU, vendedor, preço, frete, garantia e confirmar a combinação de hardware/software. Após preencher, calcular TCO em [[09-Servicos-e-Custos/Guia-financeiro-TCO-local-vs-OpenAI]] e executar benchmark em [[05-Memoria-e-Performance/Benchmarks/README]].

## Referências

[1]: https://www.nvidia.com/ "NVIDIA — especificações oficiais"
[2]: https://www.amd.com/ "AMD — especificações oficiais"
[3]: https://www.apple.com/br/shop/buy-mac/mac-studio "Apple Brasil — compra do Mac Studio"
