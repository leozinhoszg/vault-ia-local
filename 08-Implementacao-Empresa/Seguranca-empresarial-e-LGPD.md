# Segurança empresarial e LGPD

## Identidade e acesso

Integre SSO via OIDC ou SAML ao IdP corporativo. Valide issuer, audience, assinatura, expiração, nonce e rotação de chaves. Faça RBAC por função e ABAC por tenant, projeto, documento e ambiente. Service accounts devem ter escopo mínimo e segredo fora do código. Para aplicar este contrato a runtimes de desktop (LM Studio, Ollama), ver [[08-Implementacao-Empresa/04-LM-Studio-e-Ollama-como-runtimes-internos]].

## Isolamento multi-tenant

A ACL deve ser aplicada na ingestão, no índice, no retriever, no prompt e na resposta. Nunca confie somente no filtro da interface. Separe namespace, chave de criptografia, logs e quotas conforme o risco. Teste tentativa de recuperar documento de outro tenant.

## LGPD

Mapeie controlador/operador, finalidade, base legal, categorias de dados, retenção, eliminação, direitos do titular, transferência internacional e suboperadores. Classifique prompts, documentos, embeddings, logs e outputs. Embeddings podem carregar informação sensível; trate-os como dados protegidos.

## Auditoria

Registre usuário/serviço, modelo, versão, política, ferramenta, decisão de autorização, timestamps, latência, custo e status. Evite registrar prompt ou resposta sensível por padrão; aplique redaction e retenção definida. Logs de auditoria devem ser protegidos contra alteração.

## Backup, restauração e HA

Faça backup criptografado de configuração, model manifest, índices, metadados, adapters, prompts, políticas e avaliações. Teste restauração, não apenas existência do backup. Defina RPO/RTO. Para HA, use réplicas do serving, health checks, fila, circuit breaker, fallback API/local, storage durável e reindexação automatizada.

## SLO e incidentes

Defina SLO de disponibilidade, TTFT P95, tokens/s mínimo, taxa de erro, citação válida e conclusão de ferramenta. Incidentes incluem vazamento, tool call indevido, prompt injection bem-sucedido, modelo comprometido, degradação e custo anômalo. O runbook deve conter contenção, revogação, rollback, preservação de evidência, comunicação e pós-incidente.

## Referências

[1]: https://www.gov.br/esporte/pt-br/acesso-a-informacao/lgpd "Governo Federal — LGPD"
[2]: https://openid.net/specs/openid-connect-core-1_0.html "OpenID Connect Core"
[3]: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence "NIST AI 600-1"
[4]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP LLM risks"
