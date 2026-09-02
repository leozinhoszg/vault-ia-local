---
control_id: OLL-NET-001
status: tested
applicability:
  - ollama
environment:
  - home
  - enterprise
risk: critical
owner: platform-security
verified_on: 2026-09-01
review_due: 2026-10-01
evidence_type: own-test
---

# OLL-NET-001 — Bind do Ollama restrito a loopback

## Risco

Abuso da API sem autenticação (fronteira 2 do [[10-Operacao-e-Seguranca/Threat-model-LLM-local]]): a API local não tem auth nativa; qualquer bind além de loopback expõe inferência, listagem e gestão de modelos à rede.

## Requisito

[[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]] (autenticação forte em toda fronteira de usuário) e [[08-Implementacao-Empresa/04-LM-Studio-e-Ollama-como-runtimes-internos]].

## Configuração recomendada

`OLLAMA_HOST=127.0.0.1:11434` (default do fabricante). Em Docker, publicar somente `-p 127.0.0.1:11434:11434`. Exposição além do host é papel exclusivo do gateway.

## Configuração insegura conhecida

`OLLAMA_HOST=0.0.0.0` (ou publicação Docker sem IP) para "facilitar o acesso do time" — entrega a API inteira, sem credencial, à rede local.

## Teste positivo

`netstat -ano | findstr 11434` deve listar somente `127.0.0.1:11434 … LISTENING`. Executado em 2026-09-01: **PASS**.

## Teste negativo

De outra máquina da rede, `curl http://<ip-do-host>:11434/api/version` deve falhar por recusa de conexão. Não executado (exige segunda máquina); pendente.

## Evidência

[[10-Operacao-e-Seguranca/Evidencias/Ollama-testes-negativos-2026-09-01]], teste 2.

## Rollback

O controle é o default; rollback só existe no sentido inverso (expor de novo exige mudança explícita de `OLLAMA_HOST` e reinício do serviço).

## Limitações por versão

Verificado no Ollama 0.33.2/Windows. Loopback não protege contra processos locais no mesmo host — em host multiusuário, o controle compensatório é conta de serviço + firewall local.

## Referências

[1]: https://docs.ollama.com/faq "Ollama — FAQ (OLLAMA_HOST, default 127.0.0.1:11434)"
