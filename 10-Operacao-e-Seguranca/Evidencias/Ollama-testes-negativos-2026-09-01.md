# Evidência — testes de segurança do Ollama local (2026-09-01)

- **Data de execução:** 2026-09-01.
- **Ambiente:** Windows 11 Pro, Ollama 0.33.2 (winget), servidor já em execução; sondas somente-leitura via `curl`, `netstat` e leitura do `server.log`. Nenhuma configuração foi alterada.
- **Tipo de evidência:** teste próprio (`own-test`). Primeira evidência de laboratório da camada de controles de [[10-Operacao-e-Seguranca/Threat-model-LLM-local]].

## Resultados

| # | Teste | Comando | Resultado | Veredito |
|---|---|---|---|---|
| 1 | Versão do runtime | `curl http://127.0.0.1:11434/api/version` | `{"version":"0.33.2"}` | Ambiente identificado |
| 2 | Bind restrito a loopback | `netstat -ano` filtrando `11434` | `TCP 127.0.0.1:11434 … LISTENING` — somente loopback, sem `0.0.0.0` | **PASS** ([[10-Operacao-e-Seguranca/Controles/OLL-NET-001-Bind-loopback]]) |
| 3 | API responde sem credencial | `curl -o /dev/null -w "%{http_code}" http://127.0.0.1:11434/api/tags` | `200` | Confirma ausência de auth nativa |
| 4 | Header de autorização é ignorado | mesmo request com `Authorization: Bearer x` (token inválido curto) | `200` — aceito igual | Confirma que não há validação alguma ([[10-Operacao-e-Seguranca/Controles/OLL-AUTH-002-Camada-externa-de-autenticacao]]) |
| 5 | Modo somente local | `server.log`, linha `msg="Ollama cloud disabled: false"` | Cloud **habilitado** nesta máquina | **FAIL** ([[10-Operacao-e-Seguranca/Controles/OLL-CLD-003-Modo-somente-local]]) |

## Configuração observada no `server.log` (linha `server config`)

Valores relevantes, corroborando os defaults documentados na FAQ [1] (caminho do usuário redigido):

```text
OLLAMA_HOST:http://127.0.0.1:11434
OLLAMA_MODELS:%USERPROFILE%\.ollama\models
OLLAMA_NUM_PARALLEL:1
OLLAMA_MAX_QUEUE:512
OLLAMA_MAX_LOADED_MODELS:0        (0 = automático; FAQ: 3x GPUs)
OLLAMA_NO_CLOUD:false             ← divergência da recomendação do vault
OLLAMA_KEEP_ALIVE:5m0s
OLLAMA_ORIGINS:[http://localhost … http://0.0.0.0 … app://* file://* tauri://* vscode-webview://* …]
OLLAMA_REMOTES:[ollama.com]
```

Observações:

- O default real de `OLLAMA_ORIGINS` inclui `0.0.0.0`, esquemas `app://*`, `file://*` e webviews de IDE — mais amplo do que a FAQ sugere; reforça a recomendação de restringir explicitamente em ambiente empresarial.
- `OLLAMA_REMOTES:[ollama.com]` lista o hub permitido para pull; candidato a controle de supply chain ([[10-Operacao-e-Seguranca/Supply-chain-de-modelos]]).

## Limitações

- Testes executados no cenário doméstico (host único); nenhum gateway presente para testar RBAC de ponta a ponta.
- O teste 4 usa a API de listagem; não foi testado endpoint de geração com header inválido (esperado o mesmo comportamento, mas não medido).
- LM Studio não está instalado nesta máquina; seus testes seguem pendentes.

## Referências

[1]: https://docs.ollama.com/faq "Ollama — FAQ (defaults de OLLAMA_HOST, NUM_PARALLEL, MAX_QUEUE, MAX_LOADED_MODELS, ORIGINS)"
