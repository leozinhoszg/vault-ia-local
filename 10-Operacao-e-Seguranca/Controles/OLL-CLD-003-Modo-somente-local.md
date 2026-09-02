---
control_id: OLL-CLD-003
status: tested
applicability:
  - ollama
environment:
  - home
  - enterprise
risk: high
owner: platform-security
verified_on: 2026-09-01
review_due: 2026-10-01
evidence_type: own-test
---

# OLL-CLD-003 — Modo somente local (cloud desativado)

## Risco

Exfiltração via cloud do runtime ([[10-Operacao-e-Seguranca/Threat-model-LLM-local]]): tags `:cloud` e busca web enviam prompts para servidores do Ollama por um cliente que parece local ([[02-Modelos/Local-real-vs-cloud]]).

## Requisito

Política de dados de [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]]: dado sensível não sai da fronteira controlada.

## Configuração recomendada

`OLLAMA_NO_CLOUD=1` (ou `{"disable_ollama_cloud": true}` em `server.json`) em toda máquina que processa dado sensível; confirmar no log `Ollama cloud disabled: true`.

## Configuração insegura conhecida

Default de fábrica: cloud habilitado (`Ollama cloud disabled: false`), com `ollama.com` em `OLLAMA_REMOTES`.

## Teste positivo

Após aplicar a variável e reiniciar, o `server.log` mostra `Ollama cloud disabled: true` e `ollama run <modelo>:cloud` falha. Não executado ainda.

## Teste negativo

Ler o `server.log` atual: em 2026-09-01 esta máquina registrou `Ollama cloud disabled: false` — **controle ausente confirmado; divergência aberta com a recomendação do vault**. Ação corretiva: aplicar a configuração e reexecutar o teste positivo (decisão do dono editorial; este controle não autoriza mudar o serviço).

## Evidência

[[10-Operacao-e-Seguranca/Evidencias/Ollama-testes-negativos-2026-09-01]], teste 5.

## Rollback

Remover a variável/entrada do `server.json` e reiniciar restaura o comportamento de fábrica (cloud e busca web disponíveis).

## Limitações por versão

Verificado no Ollama 0.33.2; a FAQ documenta a chave desde a introdução dos modelos cloud. Desativar remove também a busca web — funcionalidade, não só risco.

## Referências

[1]: https://docs.ollama.com/faq "Ollama — FAQ (disable_ollama_cloud / OLLAMA_NO_CLOUD)"
