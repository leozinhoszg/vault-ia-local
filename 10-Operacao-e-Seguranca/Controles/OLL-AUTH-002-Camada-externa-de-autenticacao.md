---
control_id: OLL-AUTH-002
status: tested
applicability:
  - ollama
environment:
  - enterprise
risk: critical
owner: platform-security
verified_on: 2026-09-01
review_due: 2026-10-01
evidence_type: own-test
---

# OLL-AUTH-002 — Autenticação e autorização em camada externa

## Risco

A API local do Ollama aceita qualquer requisição; header `Authorization` é ignorado. Fora do host local, qualquer uso exige gateway com IdP (RBAC/ABAC) na frente — [[10-Operacao-e-Seguranca/Threat-model-LLM-local]], ameaça "abuso da API sem autenticação".

## Requisito

[[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]] (SSO via OIDC/SAML, RBAC por função, ABAC por tenant) aplicado conforme [[08-Implementacao-Empresa/04-LM-Studio-e-Ollama-como-runtimes-internos]].

## Configuração recomendada

Gateway/policy engine como único caminho de rede até `:11434`: autentica, aplica RBAC/ABAC, quotas, allowlist de modelos e valida o corpo (modelo, `num_ctx`, options). O runtime nunca é alcançável diretamente por consumidores.

## Configuração insegura conhecida

Tratar API key do Ollama Cloud, token de aplicação ou "está atrás do VPN" como autenticação da API local — nenhum deles é validado pelo runtime (teste 4 da evidência).

## Teste positivo

Via gateway: requisição sem token válido do IdP deve receber 401/403; com token válido e papel autorizado, 200. Não executado (nenhum gateway neste host); pendente de laboratório empresarial.

## Teste negativo

Direto no runtime: `curl -H "Authorization: Bearer x" http://127.0.0.1:11434/api/tags` retorna `200` mesmo com token inválido — executado em 2026-09-01, confirmando que **não há validação nativa** e que o controle externo é obrigatório.

## Evidência

[[10-Operacao-e-Seguranca/Evidencias/Ollama-testes-negativos-2026-09-01]], testes 3 e 4.

## Rollback

Remover o gateway devolve a API aberta; qualquer mudança nesse caminho é mudança de superfície e exige nova rodada destes testes.

## Limitações por versão

Verificado no Ollama 0.33.2. Se o fabricante introduzir auth nativa, ela vira segunda barreira (como no LM Studio 0.4+), não substituto do RBAC no gateway.

## Referências

[1]: https://docs.ollama.com/faq "Ollama — FAQ (sem mecanismo de autenticação local documentado)"
