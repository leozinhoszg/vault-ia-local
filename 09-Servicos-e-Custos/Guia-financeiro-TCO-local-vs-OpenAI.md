# Guia financeiro — TCO de IA local versus API da OpenAI

> **Escopo.** Este capítulo compara o custo total de propriedade de uma infraestrutura local de inferência com o custo variável da API da OpenAI. Ele é um modelo de decisão, não uma cotação, promessa de economia ou recomendação financeira personalizada. Todas as premissas devem ser substituídas por dados da empresa.

## 1. A unidade correta de comparação

Não compare apenas preço por token com preço da GPU. Compare **a mesma tarefa concluída com a mesma qualidade, contexto, disponibilidade, latência, segurança e operação**. Uma API cobra principalmente por tokens e serviços; uma máquina local exige capital, energia, espaço, manutenção, atualização, equipe, indisponibilidade e risco de obsolescência.

A unidade operacional recomendada é o **custo por milhão de tokens efetivamente processados**, separado em entrada, entrada em cache e saída, mais custo de disponibilidade e operação. Para coding e agentes, registre também tarefas concluídas, chamadas de ferramenta, testes passantes e intervenção humana.

## 2. Preços de referência da API

A página oficial consultada em 1º de setembro de 2026 apresenta, para processamento padrão abaixo de 270K de contexto, os seguintes preços: GPT-5.6 Sol a US$4/M tokens de entrada, US$0,40/M cached input e US$20/M output; GPT-5.6 Terra a US$2/M, US$0,20/M e US$12/M; GPT-5.6 Luna a US$0,20/M, US$0,02/M e US$1,20/M [1]. A planilha registra essa data, aplica fator editável para contexto longo e deixa `cache writes` como entrada editável, inicialmente zero porque o preço aplicável deve ser confirmado no endpoint/contrato. O preço promocional de Sol e qualquer condição de Batch precisam ser validados novamente na data do uso. A Batch API anuncia redução de 50% para tarefas assíncronas [1]. Preços, modelos promocionais e limites podem mudar; registre a data e consulte novamente antes da decisão.

| Modelo de referência | Entrada US$/M | Cached US$/M | Saída US$/M | Entrada BRL/M | Cached BRL/M | Saída BRL/M |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5.6 Sol | 4,00 | 0,40 | 20,00 | `4×câmbio` | `0,40×câmbio` | `20×câmbio` |
| GPT-5.6 Terra | 2,00 | 0,20 | 12,00 | `2×câmbio` | `0,20×câmbio` | `12×câmbio` |
| GPT-5.6 Luna | 0,20 | 0,02 | 1,20 | `0,20×câmbio` | `0,02×câmbio` | `1,20×câmbio` |

O preço API não inclui automaticamente todo o custo da aplicação. Acrescente armazenamento, logs, observabilidade, busca web, containers, egress, suporte, impostos, gerenciamento de chaves e desenvolvimento. A página oficial também informa preços para web search, containers, transcrição e realtime; esses itens podem dominar um agente multimodal [1].

## 3. TCO local

Use custo anualizado, não somente CAPEX. Para uma máquina:

`TCO_local_anual = CAPEX_amortizado + energia + refrigeração + manutenção + garantia + software + operação + espaço + backup + conectividade + risco_de_indisponibilidade`

`CAPEX_amortizado = CAPEX_total × fator_de_recuperação / vida_útil_anos`

Para uma aproximação linear simples, `CAPEX_total / vida_útil_anos`. Para análise financeira mais rigorosa, use taxa de desconto e valor residual:

`anuidade_CAPEX = (CAPEX - valor_residual/(1+r)^n) × r/(1-(1+r)^-n)`

onde `r` é a taxa mensal ou anual compatível com `n`, e `n` é a vida útil. Não misture taxa anual com número de meses.

## 4. Energia brasileira

Meça potência média na tomada. Não use TDP como consumo do sistema. A fórmula mensal é:

`kWh_mês = potência_média_kW × horas_ligadas_por_dia × dias_mês`

`energia_R$/mês = kWh_mês × tarifa_efetiva_R$/kWh`

Inclua UPS, perdas da fonte, ar-condicionado e consumo em idle. A tarifa efetiva deve incluir impostos, encargos e bandeira da distribuidora. Para uma estação de 0,65 kW ligada 12 horas/dia, 26 dias/mês e tarifa de R$1,05/kWh, a energia da máquina é `0,65×12×26×1,05 = R$212,94/mês`, antes de refrigeração.

## 5. Custo API

`custo_API = (tokens_in/M × preço_in) + (cached_in/M × preço_cached) + (tokens_out/M × preço_out) + ferramentas + armazenamento + egress + impostos`

Se os preços estão em dólar:

`custo_API_BRL = custo_API_USD × câmbio_efetivo`

Use câmbio efetivo, não somente PTAX: inclua spread, IOF, retenções e impostos aplicáveis ao contrato. O Banco Central publica a série de boletins e a PTAX; a cotação de planejamento deve ser datada [2].

## 6. Break-even

Defina `C_local_mês` como TCO local mensal e `c_api` como custo API por milhão de tokens equivalentes. O volume de break-even é:

`tokens_break_even_M/mês = C_local_mês / c_api_por_M_tokens`

Se separar entrada e saída:

`c_api_por_M = mix_in × p_in + mix_cached × p_cached + mix_out × p_out`

com `mix_in`, `mix_cached` e `mix_out` em milhões de tokens no mês. Para uma mistura real, não trate todos os tokens como entrada barata: coding e agentes frequentemente geram muita saída e repetem contexto.

O break-even de tempo, se o CAPEX for pago à vista e a API economizada mensalmente for positiva, é:

`meses_break_even = CAPEX_incremental / (custo_API_mês - custo_operacional_local_mês)`

Se o denominador for zero ou negativo, a máquina não amortiza por uso de API nessa carga. Se a máquina também atender outros workloads, aloque custo por GPU-hour ou por token, evitando atribuir 100% do CAPEX a um único projeto.

## 7. Exemplo numérico editável

Premissas ilustrativas: câmbio efetivo R$5,50/US$; local com CAPEX de R$20.000; vida útil de 36 meses; valor residual zero; energia medida de R$212,94/mês; refrigeração de R$150/mês; manutenção/garantia de R$250/mês; operação e espaço de R$600/mês. O CAPEX linearizado é R$555,56/mês e o TCO local reconciliado é R$1.768,50/mês.

Para a mistura mensal de 100M tokens de entrada, 20M cached input e 25M tokens de saída:

| API | Custo mensal aproximado |
|---|---:|
| GPT-5.6 Sol | `(100×4 + 20×0,4 + 25×20)×5,5 = R$4.994,00` |
| GPT-5.6 Terra | `(100×2 + 20×0,2 + 25×12)×5,5 = R$2.772,00` |
| GPT-5.6 Luna | `(100×0,2 + 20×0,02 + 25×1,2)×5,5 = R$277,20` |
| Local | R$1.768,50/mês, independentemente dos tokens dentro da capacidade |

Com o mix de 145M tokens/mês, os break-evens aproximados são **51,4M tokens/mês para Sol**, **92,5M para Terra** e **925M para Luna**, mantendo a mesma proporção de entrada, cache e saída. Neste exemplo, o local vence Sol e Terra em custo direto acima desses volumes, mas perde para Luna até aproximadamente 925M tokens/mês. Isso não prova equivalência de qualidade. Se a máquina local não entregar a mesma taxa de conclusão, a comparação deve incluir custo de intervenção, retrabalho e capacidade ociosa.

## 8. Capacidade e custo por token local

Meça tokens/s de prefill e decode e o número de horas úteis. Uma aproximação de capacidade é:

`tokens_mês = tokens_s × 3600 × horas_uso_mês × fator_utilização`

`custo_local_por_M = TCO_local_mês / (tokens_mês/M)`

Para agentes, prefira `custo_por_tarefa_concluída = TCO_mês / tarefas_concluídas`, pois tokens/s maior pode vir acompanhado de mais tentativas ou erros.

Se houver fila, o fator de utilização não deve ser confundido com uptime. Uma GPU ligada 24/7 e usando 5% pode custar o mesmo em energia idle e ainda ter baixo throughput econômico.

## 9. Sensibilidade

Varie pelo menos: câmbio ±20%; tarifa de energia ±30%; utilização 10/25/50/80%; vida útil 24/36/48 meses; CAPEX ±20%; tokens de saída; cached input; downtime; custo da equipe; e qualidade. O resultado deve mostrar em quais condições a decisão muda.

| Variável | Favorece local quando | Favorece API quando |
|---|---|---|
| Utilização | Alta e previsível | Baixa ou muito variável |
| Contexto | Estável e moderado | Picos longos e imprevisíveis |
| Qualidade | Modelo local atende | Modelo frontier é necessário |
| Privacidade | Dados não podem sair | API contratada atende residência/controle |
| Latência | Rede externa é gargalo | Provedor está mais próximo/rápido |
| Capital | CAPEX disponível | Preservar caixa é prioridade |
| Operação | Equipe já existe | Não há equipe de MLOps/SRE |

## 10. O que a planilha calcula

A planilha `TCO-local-vs-OpenAI.xlsx` possui abas de premissas, API, local, cenários e break-even. Altere células amarelas, mantenha a unidade em milhões de tokens e verifique se o mix soma o volume total. O resultado é uma ferramenta de planejamento; valide contra fatura real, wattímetro, benchmark e disponibilidade.

## 11. Decisão empresarial

A decisão madura costuma ser híbrida: local para dados sensíveis, baixa latência e carga previsível; API para picos, modelos maiores, experimentação e capacidade de fallback. Formalize SLA, residência, retenção, incidentes, RTO/RPO, orçamento, limite de API, fallback e critérios de desligamento. O menor custo nominal não é necessariamente o menor custo por resultado confiável.

## Referências

[1]: https://openai.com/api/pricing/ "OpenAI API Pricing"
[2]: https://opendata.bcb.gov.br/dataset/exchange-rates-daily-bulletins "Banco Central — Exchange rates daily bulletins / PTAX"
[3]: https://www.aneel.gov.br/ "ANEEL — tarifas e regulação"
[4]: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence "NIST AI RMF Generative AI Profile"

## 12. Sensibilidade ampliada e custo de qualidade

Para uma decisão empresarial, crie pelo menos três cenários: conservador, base e agressivo. O cenário conservador usa menor utilização, maior custo de energia, vida útil curta, maior downtime e mais intervenção humana; o agressivo usa carga previsível, uptime alto e reaproveitamento do equipamento em múltiplas aplicações.

`custo_downtime_mês = horas_indisponíveis × custo_hora_negócio`

`custo_equipe_mês = horas_MLOps × custo_hora_carregado + horas_suporte × custo_hora_carregado`

`custo_qualidade_mês = tarefas_com_retrabalho × custo_médio_retrabalho + tarefas_falhas × custo_da_falha`

`TCO_ajustado = TCO_direto + downtime + equipe + qualidade + risco_residual`

| Cenário | Utilização | Downtime | Vida útil | Equipe/mês | Interpretação |
|---|---:|---:|---:|---:|---|
| Conservador | 10–25% | 8 h | 24 meses | Alta | API tende a vencer por elasticidade. |
| Base | 25–50% | 2 h | 36 meses | Média | Depende de qualidade, mix de tokens e preço API. |
| Agressivo | 60–80% | <1 h | 48 meses | Baixa incremental | Local pode vencer com carga previsível. |

Uma API pode parecer mais cara por token e ainda ser economicamente melhor quando evita compra antecipada, time operacional, indisponibilidade e retrabalho. Da mesma forma, local pode ser superior quando privacidade, latência, residência e volume estável têm valor econômico real. Registre cada valor em BRL, data e responsável pela premissa.
