# LM Studio e Ollama como runtimes internos na empresa

- **Data de verificação:** 2026-09-01 (docs oficiais LM Studio e Ollama capturadas nesta data).
- **Escopo:** como usar LM Studio e Ollama num cenário empresarial com segurança, auditoria e RBAC. Complementa [[08-Implementacao-Empresa/01-Arquitetura-de-referencia]] e [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]]; não substitui a recomendação de [[04-Software/Runtimes]] de usar vLLM para serving multiusuário de alto throughput.
- **Status:** especificação de fabricante + destilação de práticas de segurança; **nenhum teste próprio executado** (ver "O que esta nota não afirma").

## Princípio arquitetural

Nem o LM Studio nem o Ollama oferecem RBAC, multi-tenancy ou trilha de auditoria corporativa nativos. A autenticação nativa do LM Studio (0.4+) é uma **segunda barreira entre gateway e runtime**, não o RBAC principal. Identidade, autorização, quotas e auditoria ficam no IdP + gateway/policy engine, exatamente como na [[08-Implementacao-Empresa/01-Arquitetura-de-referencia]].

```
Usuários / aplicações
        │
IdP — Entra ID, Okta ou Keycloak (OIDC/SAML + MFA + SCIM)
        │
API Gateway / Policy Engine
  ├── TLS na borda
  ├── RBAC por função + ABAC por tenant/projeto/dado/ambiente
  ├── quotas e allowlist de modelos
  ├── validação do corpo da requisição (modelo, contexto, options)
  ├── auditoria de decisões
  └── controle de ferramentas e egress
        │
Rede privada / mTLS
        │
  ├── LM Studio — 127.0.0.1:1234 (porta padrão do servidor)
  └── Ollama ──── 127.0.0.1:11434
```

Regras herdadas de [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]]: validar issuer, audience, assinatura, expiração, nonce e rotação de chaves no OIDC/SAML; service accounts com escopo mínimo e segredo fora do código; ACL aplicada na ingestão, índice, retriever, prompt e resposta quando houver RAG.

## LM Studio (requer 0.4.0 ou superior para autenticação)

Configurações verificadas na documentação oficial [1][2], com os nomes exatos da UI (Developer Page → Server Settings):

| Setting | Recomendação empresarial | Observação |
|---|---|---|
| `Require Authentication` | **Ligar** | Só aceita requisições com API Token válido no header `Authorization: Bearer …`; "Requires LM Studio 0.4.0 or newer" [1] |
| `Manage Tokens` (API Tokens) | Um token por aplicação; escopo mínimo | Permissões por token são editáveis na UI [1]; a doc não enumera os escopos disponíveis — conferir na versão instalada antes de prometer "somente inferência" |
| `Serve on Local Network` | **Desligado** | Mantém o bind local; exposição é papel do gateway [2] |
| `Enable CORS` | **Desligado** | API não deve ser chamada de browsers de outras origens [2] |
| `Allow per-request MCPs` | **Desligado** | Impede cliente de apontar MCP arbitrário fora do `mcp.json` [2] |
| `Allow calling servers from mcp.json` | Desligado, salvo integração formalmente aprovada | Exige `Require Authentication` ligado [1][2] |
| `Just in Time Model Loading` | Desligar em produção, ou allowlist rígida de modelos | JIT carrega qualquer modelo pedido na requisição [2]; com `Auto Unload Unused JIT Models` e `Only Keep Last JIT Loaded Model` como mitigação parcial |
| Gestão de modelos (download/load/unload) | Bloquear para consumidores comuns | Consumidores falam só com o gateway; gestão é operação |

Pontos que não são settings, mas contrato da API:

- **`/api/v1/chat` persiste a conversa por padrão.** A doc do parâmetro `store` diz: "Whether to store the chat. If set, response will return a `response_id` field. **Default true**" [3]. Para dados sensíveis, enviar `"store": false` — e, em produção, o gateway deve **impor** isso na requisição, não confiar no cliente. Isso concretiza a regra de [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]] de não registrar prompt/resposta sensível por padrão.
- **`llmster`** é o serviço/daemon do LM Studio; a doc traz "Setup llmster as a Startup Task on Linux" via systemctl [1]. Executar com conta de serviço dedicada, sem privilégios administrativos.

## Ollama

**A API local não tem autenticação nativa** — a FAQ oficial não documenta nenhum mecanismo de auth ou API key para `localhost:11434` [4]. As API keys do Ollama Cloud autenticam o serviço remoto, não a API local (inferência coerente com [[02-Modelos/Local-real-vs-cloud]]; a doc não descreve proteção local). Portanto o gateway não é opcional: é a única camada de autenticação.

Variáveis de ambiente verificadas na FAQ [4]:

| Variável | Default documentado | Uso empresarial |
|---|---|---|
| `OLLAMA_HOST` | `127.0.0.1:11434` | Manter em loopback; nunca `0.0.0.0` sem gateway na frente |
| `OLLAMA_MODELS` | Depende do SO (Windows: `%USERPROFILE%\.ollama\models`) | Mover para volume dedicado e controlado (ex.: `/srv/ollama/models`) com permissões restritas |
| `OLLAMA_NUM_PARALLEL` | `1` | Dimensionar conforme VRAM; é o teto de requisições simultâneas por modelo |
| `OLLAMA_MAX_LOADED_MODELS` | 3× nº de GPUs (ou 3 em CPU) | Reduzir ao conjunto aprovado; evita evicção imprevisível |
| `OLLAMA_MAX_QUEUE` | `512` | Reduzir a um limite operacional; fila longa esconde saturação |
| `OLLAMA_NO_CLOUD` | — | `1` em toda máquina corporativa: desativa modelos `:cloud` e busca web, fechando dois canais de exfiltração (ver [[02-Modelos/Local-real-vs-cloud]]) |
| `OLLAMA_ORIGINS` | Permite `127.0.0.1` e `0.0.0.0` | Restringir explicitamente; o parecer externo que originou esta nota não cobria o CORS do Ollama |

Complementos:

- **Docker:** publicar a porta somente em loopback ou rede interna (`-p 127.0.0.1:11434:11434`), como no padrão de [[08-Implementacao-Empresa/02-Deploy-com-vLLM]].
- **Gateway valida o corpo, não só a rota:** como o runtime aceita qualquer coisa autenticada, o gateway deve validar modelo solicitado (allowlist), `num_ctx`/opções de execução e tamanho da requisição.
- O script [[07-Implementacao-Casa/RAG-local-executavel.py]] já pratica o princípio: rejeita URLs remotas de Ollama por padrão (`allow_remote=False`).

## Endurecimento comum (destilado do cofre de coding)

Práticas confirmadas nas notas do cofre de coding deste host (261 — AuthN e AuthZ; 293 — Cloud e Network Security; 294 — DevSecOps e Supply Chain; 297 — Segurança de IA e LLMs; 299 — Production Readiness), citadas por nome porque vivem fora deste vault:

1. **Default deny nos dois níveis** (rota e recurso); autorização também no nível do dado/tenant, com revalidação no servidor ou policy engine — não confiar apenas em roles gravadas em JWT de longa duração.
2. **Zero Trust entre serviços:** identidade por workload e mTLS (service mesh ou SPIFFE/SPIRE) quando a escala justificar; controle de egress dos runtimes — um LLM server não precisa iniciar conexões de saída.
3. **Cadeia de fornecimento de modelos:** registry interno com origem, licença, hash, quantização, tokenizer, assinatura e resultado de avaliação; versões fixadas por digest; nada de `latest`, auto-pull ou atualização automática. Ecoa [[08-Implementacao-Empresa/03-Seguranca-e-governanca]] (SBOM, hashes) e o [[10-Operacao-e-Seguranca/Runbook]] (mudança de modelo com canary e rollback).
4. **Identidade delegada para RAG, MCP e ferramentas:** a chamada opera com as permissões do usuário/tenant corrente; uma service account global com acesso amplo quebra o isolamento mesmo com RBAC no endpoint.
5. **Auditoria:** os campos de [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]] (usuário/serviço, modelo, versão, política, decisão de autorização, timestamps, latência, custo, status) + correlation ID; separar log operacional de trilha de auditoria; conteúdo integral de prompt/resposta somente como exceção justificada, com proteção e retenção curta.
6. **Gate formal de produção:** threat model, pentest/DAST, teste de carga, restore testado, rollback e kill switch antes do go-live — PASS/FAIL explícito.

## Checklist mínimo antes de expor a qualquer usuário

- [ ] IdP integrado (OIDC/SAML + MFA); RBAC/ABAC no gateway; default deny.
- [ ] LM Studio: `Require Authentication` ligado, token por aplicação, `Serve on Local Network`/CORS/MCPs desligados, JIT desligado ou com allowlist.
- [ ] LM Studio: política de `store:false` imposta pelo gateway para dados sensíveis.
- [ ] Ollama: `OLLAMA_HOST` em loopback, `OLLAMA_NO_CLOUD=1`, `OLLAMA_ORIGINS` restrito, limites de paralelismo/fila definidos.
- [ ] Allowlist de modelos validada no gateway; modelos fixados por hash/digest no registry interno.
- [ ] Trilha de auditoria com correlation ID chegando ao SIEM; retenção definida.
- [ ] Runbook de incidente e rollback testados ([[10-Operacao-e-Seguranca/Runbook]]).

## O que esta nota não afirma

- Nenhuma configuração foi testada nesta máquina ou em ambiente corporativo; tudo acima é especificação de fabricante capturada em 2026-09-01 mais destilação editorial de práticas de segurança.
- Os escopos exatos de permissão por token do LM Studio não estão enumerados na doc pública; conferir na UI da versão instalada antes de prometer "token somente de inferência".
- "API keys do Ollama Cloud não protegem a API local" é inferência por ausência na doc, não afirmação testada; um smoke test local pode fechá-la.
- Defaults e nomes de settings mudam entre versões; revisar mensalmente junto com o ciclo de modelos/runtimes do [[AGENTS]].

## Ver também

- [[08-Implementacao-Empresa/01-Arquitetura-de-referencia]] — onde o gateway vive.
- [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]] — contrato de identidade, auditoria e LGPD.
- [[08-Implementacao-Empresa/03-Seguranca-e-governanca]] — supply chain, SBOM, allowlist de ferramentas.
- [[02-Modelos/Local-real-vs-cloud]] — por que `:cloud` e busca web importam para exfiltração.
- [[07-Implementacao-Casa/01-LLM-local-com-Ollama]] — o mesmo runtime no cenário doméstico.

## Referências

[1]: https://lmstudio.ai/docs/developer/core/authentication "LM Studio — Authentication (Require Authentication 0.4.0+, API Tokens, llmster startup task)"
[2]: https://lmstudio.ai/docs/developer/core/server/settings "LM Studio — Server Settings (Serve on Local Network, CORS, MCPs, JIT loading)"
[3]: https://lmstudio.ai/docs/developer/rest/chat "LM Studio — REST API /api/v1/chat (parâmetro store, default true)"
[4]: https://docs.ollama.com/faq "Ollama — FAQ (OLLAMA_HOST, OLLAMA_MODELS, OLLAMA_NUM_PARALLEL, OLLAMA_MAX_LOADED_MODELS, OLLAMA_MAX_QUEUE, OLLAMA_NO_CLOUD, OLLAMA_ORIGINS)"
[5]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 para aplicações LLM (excessive agency, supply chain)"
