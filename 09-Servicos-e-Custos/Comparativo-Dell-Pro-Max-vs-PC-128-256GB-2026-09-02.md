# Dell Pro Max GB10 versus PC local com 128 GB/256 GB — análise de preço

**Data-base:** 2026-09-02. **Moeda:** BRL. **Condição padrão:** preço à vista no Pix quando publicado. **Objetivo:** comparar o Dell Pro Max com GB10 contra uma workstation/PC de alto desempenho com Ryzen 9 9950X ou Intel Core Ultra 9 285K e uma RTX 5090.

> **Nota financeira:** esta é uma análise de preços e capacidade, não uma garantia de preço, disponibilidade ou retorno econômico. Ofertas podem mudar, e a decisão de compra deve considerar frete, garantia, montagem, impostos, ruído, energia e suporte.

## Conclusão executiva

A Dell Brasil não publica o preço do Dell Pro Max FCM1253 Micro na página consultada; informa que a compra exige contato comercial [1]. Para manter uma referência comparável, uso a cotação anterior registrada no vault para um DGX Spark de 4 TB com o mesmo GB10: **R$ 54.552,17 à vista**, de revendedor brasileiro, consultada em 2026-09-01 [2]. Essa referência não é preço oficial Dell e precisa ser reconfirmada.

Com os preços observados, é possível montar um PC com **Ryzen 9 9950X, 128 GB DDR5, RTX 5090 e 4 TB NVMe por aproximadamente R$ 58,1 mil**, antes de frete e montagem. Ele fica cerca de **R$ 3,5 mil acima** da referência de R$ 54,6 mil do Dell/DGX Spark, mas é muito mais rápido nos modelos que cabem na VRAM da RTX 5090. Em contrapartida, os **128 GB da máquina x86 não são VRAM**: modelos acima de aproximadamente 32 GB quantizados exigem divisão entre GPU e RAM, com queda importante de desempenho.

Para **256 GB de RAM**, usando dois kits de 128 GB, o custo estimado sobe para aproximadamente **R$ 77,8 mil**. Essa máquina tem grande capacidade de offload, mas continua com apenas 32 GB de VRAM; portanto, não substitui uma plataforma com 128 GB de memória unificada para carregar modelos grandes inteiramente no acelerador. Com o orçamento de um Dell Pro Max de aproximadamente R$ 54,6 mil, a resposta é: **sim, uma build com RTX 5090 entrega mais velocidade; não, ela não entrega a mesma capacidade de memória utilizável para modelos grandes sem offload**.

## Preços de componentes observados

| Componente | Loja e SKU | Preço observado | Status |
|---|---|---:|---|
| RTX 5090 32 GB | KaBuM — Gigabyte Aorus Master GV-N5090AORUSM-32GD | R$ 27.659,00 | Oferta observada [3] |
| RTX 5090 32 GB | Pichau — Asus TUF TUF-RTX5090-32G-GAMING | R$ 28.999,99 | Oferta observada [4] |
| RTX 5090 32 GB | Terabyte — Asus TUF TUF-RTX5090-O32G-GAMING | R$ 27.999,99 | Oferta observada [5] |
| Ryzen 9 9950X | Pichau — 100-100001277WOF | R$ 2.999,99 | Oferta observada [6] |
| Ryzen 9 9950X | Terabyte — 100-100001277WOF | R$ 3.299,99 | Oferta observada [7] |
| Core Ultra 9 285K | Pichau — BX80768285K | R$ 3.199,99 | Oferta observada [8] |
| Core Ultra 9 285K | Terabyte — BX80768285K | R$ 3.099,99 | Oferta observada [9] |
| DDR5 128 GB | Pichau Kingston Fury Beast 2×64 GB 5600 CL36, KF556C36BBEAK2-128 | R$ 19.699,99 | Oferta observada [10] |
| PC completo 128 GB | Pichau Highflyer, Ryzen 9 9950X, RTX 5090 32 GB, 128 GB DDR5, SSD 16 TB | R$ 74.999,89 | Referência de sistema montado [10] |

A Pichau mostrou 256 GB como capacidade disponível no catálogo, mas a busca não apresentou um kit UDIMM de 256 GB claramente identificável e validado para AM5/LGA1851. Por isso, o cenário de 256 GB abaixo trata a memória como **dois kits de 128 GB**, não como uma cotação fechada de kit único.

## Configurações comparáveis

Os valores de placa-mãe, SSD, fonte, cooler e gabinete são **provisões de montagem**, não cotações individuais fechadas nesta coleta. Eles foram definidos para não subestimar uma workstation com RTX 5090: placa-mãe X870/Z890 com dois slots PCIe x16 físicos, SSD NVMe de 4 TB, fonte ATX 3.1 de 1.200 W, water cooler de 360 mm e gabinete grande com fluxo de ar.

| Item | Ryzen 9 — 128 GB | Core Ultra 9 — 128 GB | Ryzen 9 — 256 GB | Core Ultra 9 — 256 GB |
|---|---:|---:|---:|---:|
| CPU | R$ 2.999,99 | R$ 3.099,99 | R$ 2.999,99 | R$ 3.099,99 |
| Placa-mãe X870/Z890 | R$ 2.599,99* | R$ 2.599,99* | R$ 2.599,99* | R$ 2.599,99* |
| Memória DDR5 | R$ 19.699,99 | R$ 19.699,99 | R$ 39.399,98* | R$ 39.399,98* |
| RTX 5090 32 GB | R$ 27.659,00 | R$ 27.659,00 | R$ 27.659,00 | R$ 27.659,00 |
| SSD NVMe 4 TB | R$ 1.999,99* | R$ 1.999,99* | R$ 1.999,99* | R$ 1.999,99* |
| Fonte ATX 3.1 1.200 W | R$ 1.699,99* | R$ 1.699,99* | R$ 1.699,99* | R$ 1.699,99* |
| Refrigeração | R$ 699,99* | R$ 699,99* | R$ 699,99* | R$ 699,99* |
| Gabinete e ventoinhas | R$ 699,99* | R$ 699,99* | R$ 699,99* | R$ 699,99* |
| **Total estimado** | **R$ 58.058,93** | **R$ 58.158,93** | **R$ 77.758,92** | **R$ 77.858,92** |

\* Estimativa de provisão para montagem, a confirmar por SKU, vendedor, frete e garantia. O total não inclui sistema operacional pago, montagem profissional, monitor, nobreak, frete, acessórios ou custo de oportunidade.

## Comparação com o valor de referência do Dell Pro Max

| Cenário | Total | Diferença contra R$ 54.552,17 | Capacidade principal |
|---|---:|---:|---|
| Dell/DGX Spark GB10, referência de revendedor | R$ 54.552,17 | — | 128 GB unificados; GB10; 273 GB/s |
| PC Ryzen 9 + RTX 5090 + 128 GB | R$ 58.058,93 | +R$ 3.506,76 | 32 GB VRAM + 128 GB RAM; alta velocidade GPU |
| PC Core Ultra 9 + RTX 5090 + 128 GB | R$ 58.158,93 | +R$ 3.606,76 | 32 GB VRAM + 128 GB RAM; alta velocidade GPU |
| PC Ryzen 9 + RTX 5090 + 256 GB | R$ 77.758,92 | +R$ 23.206,75 | 32 GB VRAM + 256 GB RAM; offload amplo |
| PC Core Ultra 9 + RTX 5090 + 256 GB | R$ 77.858,92 | +R$ 23.306,75 | 32 GB VRAM + 256 GB RAM; offload amplo |

O preço do processador altera pouco o total: nesta classe, a RTX 5090 e principalmente a memória de alta capacidade dominam o orçamento. O Ryzen 9 9950X é a opção mais barata nas ofertas observadas da Pichau; o Core Ultra 9 285K aparece ligeiramente mais barato na Terabyte, mas a diferença final é pequena.

## O que roda melhor

A RTX 5090 tem 32 GB de VRAM. Modelos Q4 na faixa de 7B–27B cabem confortavelmente, e modelos de aproximadamente 30B podem caber dependendo do formato, contexto e KV cache. Um Llama 3.1 70B Q4, com cerca de 38–48 GB de pesos, não cabe integralmente na RTX 5090; parte deve ser colocada na RAM do sistema, usando CPU offload, ou o modelo deve ser particionado entre GPUs.

O Dell Pro Max GB10 possui 128 GB de memória LPDDR5x unificada a 273 GB/s, permitindo manter modelos de 70B quantizados e vários MoE grandes na mesma memória compartilhada. Isso não significa que seja rápido: a própria ficha do vault estima aproximadamente 4,6–6,5 tok/s para um 70B Q4 como teto/estimativa de banda. A vantagem é a capacidade de manter os pesos próximos ao acelerador, sem depender de PCIe para cada acesso.

A RTX 5090, por outro lado, tem banda de memória muito maior e CUDA maduro em x86/Linux/Windows. Para modelos que cabem nos 32 GB de VRAM, a experiência interativa tende a ser muito superior ao GB10. Para modelos de 70B, a vantagem pode diminuir bastante com offload; o desempenho real dependerá da proporção GPU/RAM, do backend, do contexto e do KV cache.

## Recomendação

Para **coding, RAG e agentes com modelos de até aproximadamente 27B–32B**, eu escolheria a build com **Ryzen 9 9950X, 128 GB e uma RTX 5090**. Ela custa cerca de R$ 3,5 mil acima da referência do GB10, mas oferece uma plataforma CUDA x86 mais ampla e muito mais velocidade nos modelos que cabem na VRAM. A configuração de 128 GB é suficiente para RAG, embeddings, reranking, bancos vetoriais e offload ocasional.

Para **70B/80B ou modelos MoE grandes mantidos integralmente em memória**, eu escolheria o GB10 se a cotação oficial Dell ficar próxima de R$ 54–60 mil. Ele oferece capacidade de memória muito mais útil por real para modelos grandes, embora com menor tokens/s. O PC com 256 GB só se justifica quando a necessidade de RAM do sistema, múltiplos serviços ou offload é prioridade; ele não transforma uma RTX 5090 de 32 GB em uma GPU de 256 GB.

A melhor alternativa de desempenho absoluto seria uma configuração com **duas RTX 5090**, mas somente as GPUs já custariam aproximadamente R$ 55–58 mil nas ofertas observadas. Com CPU, 128 GB, placa-mãe, fonte de pelo menos 1.600 W, gabinete e refrigeração, o sistema ultrapassaria com folga o orçamento do Dell Pro Max. Ela é superior em throughput, mas não é uma substituta econômica de 128 GB unificados.

## Riscos e diligências antes da compra

A memória DDR5 de 128 GB em dois módulos é cara e deve ser validada na QVL da placa-mãe. Para 256 GB usando quatro módulos, é prudente esperar redução de frequência, treinamento de memória mais demorado e possível ajuste manual de BIOS; não tratar a capacidade nominal como garantia de estabilidade no clock anunciado.

Também é necessário confirmar o modelo exato da RTX 5090, dimensões, conector de alimentação, limite da fonte, espaço do gabinete e distância entre slots PCIe. O preço exibido nas lojas é dinâmico, pode ser condicionado ao Pix e não inclui necessariamente frete ou montagem. A cotação Dell oficial deve ser obtida pelo canal comercial antes de comparar definitivamente.

## Referências

[1]: https://www.dell.com/pt-br/shop/cty/pdp/spd/dell-pro-max-fcm1253-micro "Dell Brasil — Dell Pro Max FCM1253 Micro; preço somente via contato comercial"
[2]: https://www.worldwidebrasil.com.br/nvidia-dgx-spark-4tb-ia-supercomputador-pessoal-lacrado "Worldwide Brasil — referência anterior de preço do DGX Spark 4 TB"
[3]: https://www.kabum.com.br/busca/RTX-5090 "KaBuM — busca RTX 5090; Gigabyte Aorus Master observada a R$ 27.659,00 no Pix"
[4]: https://www.pichau.com.br/search?q=RTX%205090 "Pichau — busca RTX 5090; Asus TUF observada a R$ 28.999,99 no Pix"
[5]: https://www.terabyteshop.com.br/busca?str=RTX%205090 "Terabyte — busca RTX 5090; Asus TUF observada a R$ 27.999,99 no Pix"
[6]: https://www.pichau.com.br/search?q=Ryzen%209%209950X "Pichau — Ryzen 9 9950X 100-100001277WOF observado a R$ 2.999,99 no Pix"
[7]: https://www.terabyteshop.com.br/busca?str=Ryzen%209%209950X "Terabyte — Ryzen 9 9950X 100-100001277WOF observado a R$ 3.299,99 no Pix"
[8]: https://www.pichau.com.br/search?q=Core%20Ultra%209%20285K "Pichau — Core Ultra 9 285K BX80768285K observado a R$ 3.199,99 no Pix"
[9]: https://www.terabyteshop.com.br/busca?str=Core%20Ultra%209%20285K "Terabyte — Core Ultra 9 285K BX80768285K observado a R$ 3.099,99 no Pix"
[10]: https://www.pichau.com.br/search?q=DDR5%20128GB "Pichau — memória Kingston Fury Beast 128 GB e PC completo Highflyer com 128 GB/RTX 5090"
