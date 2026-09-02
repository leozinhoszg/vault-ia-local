# Esquema de auditoria para inferência local

- **Data:** 2026-09-01.
- **Natureza:** implementação concreta do contrato de auditoria de [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]] (baseline editorial; campos a adaptar ao SIEM da organização). Nem LM Studio nem Ollama emitem esta trilha — ela nasce no gateway/policy engine e no orquestrador.

## Princípios

1. **Trilha de auditoria ≠ log operacional.** O log operacional (latência, GPU, fila — [[10-Operacao-e-Seguranca/Runbook]]) serve à operação e pode ter retenção curta; a trilha de auditoria registra decisões, é protegida contra alteração (append-only/WORM) e vai ao SIEM.
2. **Prompt e resposta completos ficam FORA do esquema padrão.** São dados sensíveis (PII, segredo de negócio) e entram no escopo LGPD de retenção e direitos do titular. Captura integral só como exceção justificada, com aprovação, redaction, proteção e retenção curta.
3. **Todo evento é correlacionável:** um `correlation_id` atravessa gateway → policy engine → runtime → RAG → ferramenta, permitindo reconstruir a cadeia de uma resposta sem guardar o conteúdo.

## Campos por evento

| Campo | Conteúdo | Observação |
|---|---|---|
| `timestamp` | ISO 8601 com timezone | Relógio sincronizado (NTP) |
| `correlation_id` | ID único da requisição ponta a ponta | Chave de investigação |
| `subject_id` | Usuário ou aplicação autenticada | Pseudonimizável para relatórios |
| `service_identity` | Workload que emitiu (gateway, orquestrador) | Identidade por workload |
| `tenant_id` | Tenant/projeto | Base do isolamento |
| `source_ip` | Origem da chamada | Dado pessoal — retenção definida |
| `authorization_decision` | allow/deny + papel e política aplicada | O coração da trilha ([[08-Implementacao-Empresa/Matriz-RBAC-e-ABAC]]) |
| `policy_version` | Versão da política vigente | Permite reproduzir a decisão |
| `runtime` | ollama/lm-studio/vllm + versão | |
| `model_id` / `model_hash` | Modelo servido e digest do artefato | Liga ao manifesto de [[10-Operacao-e-Seguranca/Supply-chain-de-modelos]] |
| `tool` | Ferramenta/MCP invocada, se houver | Argumentos só com redaction |
| `knowledge_base` | Índice RAG consultado | Sem o conteúdo dos documentos |
| `latency` | Total e TTFT | |
| `input_tokens` / `output_tokens` | Contagem | Base de custo e detecção de abuso |
| `status` | success/denied/error/timeout | |
| `error_class` | Classe do erro, sem payload | |

## Eventos mínimos

- Autenticação (sucesso/falha) e emissão/uso de token.
- Decisão de autorização (allow e **deny** — negados são o sinal de ataque).
- Inferência (metadados acima, sem conteúdo).
- Recuperação RAG (índice, nº de documentos, tenant — sem texto).
- Chamada de ferramenta/MCP e sua aprovação humana, quando exigida.
- Mudança administrativa: modelo carregado/removido, configuração alterada, política mudada — com autor.
- Uso de break-glass, do início ao fim.

## Retenção e proteção

Retenção definida por classe (decisões administrativas e break-glass mais longa; `source_ip` conforme política de dados pessoais). Redaction antes de qualquer campo livre. Acesso à trilha segue a coluna "Consultar auditoria" da [[08-Implementacao-Empresa/Matriz-RBAC-e-ABAC]]; alteração é incidente.

## Estado

Esquema não implantado em nenhum ambiente ainda; nenhum evento real coletado. Primeiro teste de aceitação: emitir os eventos de uma requisição sintética via gateway de laboratório e conferir a chegada íntegra ao SIEM.

## Ver também

- [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]] — contrato e base LGPD.
- [[10-Operacao-e-Seguranca/Threat-model-LLM-local]] — adulteração da trilha como ameaça.

## Referências

[1]: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence "NIST AI 600-1 — governança e transparência"
[2]: https://www.gov.br/esporte/pt-br/acesso-a-informacao/lgpd "LGPD — retenção e direitos do titular sobre logs com dados pessoais"
