# Matriz RBAC e ABAC para inferência local

- **Data:** 2026-09-01.
- **Natureza:** baseline **editorial** — ponto de partida para adaptar à organização, estruturado nos princípios do cofre de coding (261 — AuthN e AuthZ; 265 — Multi-tenancy, citados por nome por estarem fora deste vault). Não é especificação de fabricante: LM Studio e Ollama não implementam nada disto nativamente; a matriz vive no IdP + gateway/policy engine ([[08-Implementacao-Empresa/04-LM-Studio-e-Ollama-como-runtimes-internos]]).

## Papéis

| Papel | Descrição |
|---|---|
| **Consumidor** | Pessoa ou aplicação que usa inferência via gateway; nunca fala com o runtime |
| **Desenvolvedor** | Constrói aplicações; acessa ambientes de dev/staging com dados não sensíveis |
| **Curador de modelos** | Avalia, aprova e promove modelos no registry ([[10-Operacao-e-Seguranca/Supply-chain-de-modelos]]) |
| **Operador da plataforma** | Opera runtime, gateway e capacidade; segue o [[10-Operacao-e-Seguranca/Runbook]] |
| **Auditor** | Lê trilha de auditoria e configuração; não altera nada |
| **Administrador de emergência** | Acesso break-glass, MFA forte, aprovação registrada, duração limitada |

## Matriz papel × permissão (default deny — célula vazia = negado)

| Permissão | Consumidor | Desenvolvedor | Curador | Operador | Auditor | Admin emergência |
|---|---|---|---|---|---|---|
| Inferir (via gateway) | ✔ | ✔ dev/staging | ✔ p/ avaliação | ✔ p/ smoke test | | ✔ |
| Consultar catálogo de modelos | ✔ aprovados | ✔ | ✔ | ✔ | ✔ | ✔ |
| Carregar/descarregar modelo | | | ✔ staging | ✔ | | ✔ |
| Alterar configuração do runtime | | | | ✔ com mudança registrada | | ✔ |
| Baixar/importar modelo | | ✔ dev isolado | ✔ via pipeline | | | ✔ |
| Excluir modelo | | | ✔ com registro | | | ✔ |
| Acessar RAG | ✔ só seus tenants/docs | ✔ corpus de teste | | | | ✔ |
| Executar ferramentas/MCP | ✔ allowlist, identidade delegada | ✔ sandbox | | | | ✔ |
| Consultar auditoria | | | | ✔ operacional | ✔ trilha completa | ✔ |
| Administrar políticas (RBAC/ABAC) | | | | | | ✔ + aprovação de segurança |

## Regras transversais

1. **Default deny** nos dois níveis: rota e recurso. A permissão da célula ainda passa pelo ABAC abaixo.
2. **ABAC** por atributos: `tenant`, `projeto`, `classificação do dado`, `ambiente` (dev/staging/prod), `modelo` (só aprovados para o ambiente). Exemplo: consumidor com papel de inferir só alcança modelos aprovados para o seu tenant e dados do seu escopo — a ACL vai **na query** do retrieval, nunca depois.
3. **Revalidação no servidor:** papéis em JWT de longa duração não bastam para ação crítica (excluir modelo, mudar política); o policy engine reconsulta o estado atual.
4. **Identidade delegada:** RAG, MCP e ferramentas executam com as permissões do usuário corrente, nunca com service account global — injection no tenant A não pode alcançar o tenant B por construção.
5. **Provisionamento via SCIM** a partir do IdP; papel órfão (pessoa desligada) é incidente de acesso.
6. **Break-glass:** o administrador de emergência só existe ativado — MFA forte, aprovação nominal, expiração automática e revisão da trilha após o uso.
7. **Separação de funções:** quem aprova modelo (curador) não é quem opera (operador) nem quem audita (auditor).

## Testes que a matriz exige

- Cross-tenant automatizado: usuário do tenant A tenta recuperar documento do tenant B → negado na query (teste obrigatório de [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]]).
- Escalada horizontal: consumidor tenta rota de gestão de modelos → 403 + evento de auditoria.
- Break-glass expira: acesso de emergência após o prazo → negado.

Nenhum destes testes foi executado ainda; exigem o laboratório com gateway (pendência registrada em [[00-Inicio/Auditoria-P0]]).

## Ver também

- [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]] — o contrato que esta matriz operacionaliza.
- [[10-Operacao-e-Seguranca/Esquema-de-auditoria-LLM]] — todo `authorization_decision` desta matriz vira evento lá.
- [[10-Operacao-e-Seguranca/Threat-model-LLM-local]] — excessive agency e cross-tenant como riscos.

## Referências

[1]: https://openid.net/specs/openid-connect-core-1_0.html "OpenID Connect Core"
[2]: https://datatracker.ietf.org/doc/html/rfc7644 "SCIM 2.0 — provisionamento de identidades"
[3]: https://csrc.nist.gov/pubs/sp/800/162/upd2/final "NIST SP 800-162 — guia de ABAC"
