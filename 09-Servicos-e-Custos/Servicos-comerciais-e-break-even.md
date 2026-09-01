# Serviços comerciais, appliances e break-even

## Opções

| Opção | Vantagem | Risco/custo |
|---|---|---|
| GPU cloud por hora | Sem CAPEX e acesso a GPUs grandes | Egress, disponibilidade, privacidade e custo variável. |
| GPU cloud reservada | Previsibilidade e SLA melhor | Contrato e ociosidade. |
| Appliance on-prem | Integração, suporte e perímetro | CAPEX alto, lock-in e manutenção. |
| API gerenciada | Time-to-market e elasticidade | Dados saem do perímetro e cobrança por uso. |
| Workstation própria | Controle e custo marginal baixo | Operação, garantia, energia e escala limitada. |

Exemplos de fornecedores a comparar incluem AWS, Azure, Google Cloud, Oracle Cloud, CoreWeave, Lambda, RunPod, Vast.ai e provedores brasileiros. Confirme região, GPU, preço atual, armazenamento, rede, SLA, retenção, treinamento sobre dados e suporte antes de contratar.

## Fórmula de break-even

`custo_local_mensal = CAPEX_amortizado + energia + refrigeração + manutenção + operação`

`custo_api_mensal = (tokens_entrada × preço_entrada + tokens_cached × preço_cached + tokens_saída × preço_saída) × câmbio_efetivo + armazenamento + egress`

O exemplo numérico, a planilha e o break-even em tokens/mês estão em [[09-Servicos-e-Custos/Guia-financeiro-TCO-local-vs-OpenAI]]; esta nota resume o critério.

O break-even ocorre quando os dois custos são equivalentes **para a mesma qualidade, contexto, disponibilidade e carga**. Inclua utilização: uma GPU 24/7 com 10% de uso raramente compete com API pay-as-you-go apenas pelo preço por token.

## Energia brasileira

`kWh_mês = potência_média_kW × horas_ligadas`

`R$energia = kWh_mês × tarifa_total_R$/kWh`

Use a tarifa efetiva da sua distribuidora, incluindo impostos, bandeira e encargos. Meça a potência na tomada com wattímetro; TDP não é consumo de todo o sistema.

## Câmbio, imposto e garantia

Para equipamento importado, some preço convertido, frete, imposto, ICMS quando aplicável, despacho, garantia, manutenção e risco cambial. Para GPU usada, modele vida útil residual e ausência de garantia. Depreciação econômica é preferível a tratar hardware como gratuito após a compra.

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://openai.com/api/pricing/ "OpenAI API Pricing — preços por token, cached input e Batch"
[2]: https://opendata.bcb.gov.br/dataset/exchange-rates-daily-bulletins "Banco Central — PTAX e boletins de câmbio"
[3]: https://www.aneel.gov.br/ "ANEEL — tarifas e bandeiras de energia"
