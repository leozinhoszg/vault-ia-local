# Governança editorial do vault

## Responsáveis formais

| Papel | Responsável | Substituto | Responsabilidade |
|---|---|---|---|
| Proprietário editorial | Luiz Guimarães | A designar | Aprova escopo, prioridades e publicação. |
| Editor técnico | Luiz Guimarães | A designar | Aprova fórmulas, benchmarks, arquitetura e compatibilidade. |
| Revisor de segurança/privacidade | A designar | A designar | Revisa LGPD, IAM, incidentes e dados sensíveis. |
| Operador de benchmarks | A designar | A designar | Executa testes em hardware e mantém evidências. |

Enquanto os substitutos não forem definidos, Luiz Guimarães é o owner padrão para decisões editoriais e técnicas. A responsabilidade por preços, licenças e produção deve ser delegada antes de uso empresarial.

## Estado e envelhecimento

Cada nota deve conter `estado`, `data_verificacao`, `dono` e `proxima_revisao`. Modelos/runtimes devem ser revisados mensalmente; drivers, compatibilidade e preços, trimestralmente; segurança e governança, a cada mudança relevante ou incidente. Notas vencidas ficam marcadas como `revisão necessária` e não podem sustentar uma compra ou rollout sem nova verificação.

## Fluxo de mudança

Uma mudança abre registro com motivo, fonte, impacto, autor e data. O validador completo roda antes do merge. Mudanças de modelo, quantização, runtime, índice RAG ou política exigem avaliação de regressão. Mudanças de hardware exigem BOM e benchmark. Mudanças de segurança exigem aprovação do revisor.

## Evidências mínimas

Model card, licença, hash, configuração, logs de benchmark, dataset dourado, fatura/cotação, consumo medido, ticket de incidente e decisão de aprovação devem ser armazenados com retenção definida e sem segredos.
