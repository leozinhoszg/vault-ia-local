# Modelo de custo

O custo total de propriedade inclui aquisição, energia, refrigeração, espaço, rede, armazenamento, suporte, engenharia, observabilidade, backup e risco de indisponibilidade. Compare com custo de API por tokens, mas inclua utilização: uma GPU ociosa é um custo fixo.

`TCO = CAPEX amortizado + energia + refrigeração + software/suporte + operação + armazenamento + risco`

| Variável | Medição |
|---|---|
| CAPEX | GPU, workstation/servidor, RAM, SSD, PSU, rede e UPS. |
| Energia | kWh medidos × tarifa local × horas ligadas. |
| Utilização | % de tempo em inferência útil. |
| Trabalho | Horas de instalação, MLOps, segurança e suporte. |
| Escala | Usuários simultâneos, tokens/dia e pico. |

Nunca use um preço de varejo global como verdade brasileira. Faça três cotações locais, registre data, impostos, garantia e disponibilidade; atualize esta nota quando a decisão for tomada.
