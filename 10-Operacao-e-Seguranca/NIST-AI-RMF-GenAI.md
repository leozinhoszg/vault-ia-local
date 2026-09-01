# Governança com NIST AI RMF para IA generativa

O NIST AI 600-1 é um perfil transversal do AI Risk Management Framework para riscos de IA generativa, destinado ao uso voluntário e à melhoria da capacidade de organizações incorporarem confiabilidade no desenho, desenvolvimento, uso e avaliação [1].

## Tradução operacional

| Função | Controle verificável no projeto local |
|---|---|
| Govern | Dono do caso de uso, inventário, licença, risco, aprovação e política de mudança. |
| Map | Fluxo de dados, usuários afetados, ameaças, dependências, ferramentas e impactos. |
| Measure | Suíte de qualidade, segurança, viés, robustez, latência, custo e regressão. |
| Manage | Mitigações, revisão humana, incident response, rollback e monitoramento contínuo. |

Mantenha evidências: model card, dataset card, hashes, prompts de sistema, logs de avaliação, decisões de aprovação, testes de prompt injection, limites de ferramenta, registros de incidentes e revisão de fornecedor.

## Controles mínimos

ACL por tenant e documento, criptografia, secrets manager, retenção definida, redaction de PII, sandbox de ferramentas, aprovação para efeitos externos, rate limiting, monitoramento de OOM e custo, atualização de dependências, backup e plano de desligamento.

**Referência**

[1]: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence "NIST AI 600-1 — Generative AI Profile"
