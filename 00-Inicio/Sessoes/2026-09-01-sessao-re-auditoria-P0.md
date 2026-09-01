# Ata de sessão — re-auditoria P0 e fechamento do gate (2026-09-01)

<!-- validador: sem-referencias: ata de sessão; as evidências estão nas notas e commits citados -->

| Campo | Valor |
|---|---|
| Data | 2026-09-01 |
| Participantes | Dono editorial (Luiz Guimarães); auditor externo (relatório em texto); Claude Code (verificação e execução) |
| Método | Cada achado externo foi verificado contra o pacote real antes de qualquer edição (`openpyxl`, recomputação em Python, execução em venv limpo, `gh`) |
| Commits | `73ddb8d` (rev. 2), `2cf7e2a` (rev. 3), `8421953` (CI observado) em `main` de `leozinhoszg/vault-ia-local` |

## Achados externos e veredito

| Achado | Veredito | Ação |
|---|---|---|
| `Break_even!E2:E4` divide BRL por USD | **Confirmado** (produziria 282M/509M/5.088M) | Fórmula reescrita; 51,35M / 92,51M / 925,08M verificados por modelo independente |
| Residual ignorado, Batch sem uso, fator único de contexto longo, sensibilidade só de câmbio | **Confirmados** | Corrigidos na planilha (rev. 2) |
| Contagens 72/71/70 sem rótulo | **Confirmado** | Validador e `VALIDACAO.md` declaram escopo |
| 35 avisos | **Confirmado**; maioria era `**Referências**` em negrito em vez de cabeçalho | 21 notas normalizadas; 6 notas sem fontes ganharam referências reais; 5 justificativas explícitas |
| 69 vs 66 URLs | **Confirmado**; diferença = 3 endpoints `localhost` | Índice gerado por script, endpoints separados |
| Qwen só via Atomic | **Confirmado**; card oficial verificado por fetch | Ficha reescrita com `Qwen3-Coder-30B-A3B-Instruct` |
| Lockfile inexistente / validador exit 1 (2ª rodada) | **Não procede** para o pacote commitado: o auditor avaliou snapshot anterior a `73ddb8d` | Nenhuma; registrado |
| NumPy 2.4.6 no selftest vs 2.3.2 no requirements | **Confirmado** | Reprodução em venv limpo a partir do lockfile (numpy 2.3.2) |
| Tabelas estruturadas em `A1:H1` e `A1:H19` | **Não procede**: não havia tabelas, só autofiltros curtos | Tabelas reais criadas via Excel COM em todas as abas |

## Ações executadas por revisão

- **Rev. 2:** correções da planilha; ficha do Qwen; `--selftest`/`--retrieve-only` no script RAG (2 bugs reais no Windows corrigidos: tokenização com pontuação e cleanup do diretório temporário); referências e datas; validador com escopo e justificativas; `gerar_indice_urls.py`; `.gitignore`.
- **Rev. 3:** lockfile com hashes (`uv`, após `pip-compile` travar em backtracking) e `.sha256`; reprodução do RAG em venv limpo ([[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]]); aba `Checks`, anuidade opcional, tabelas estruturadas e valores em cache (`99-Templates/recalcular_tco.ps1`, conferido por `99-Templates/check_tco.py`); validador `--strict`; índice `--check`; `.github/workflows/validate.yml` (run `33524666554` = success).

## Decisões em aberto (do dono editorial)

1. ~~Instalar Ollama e executar a geração com `[Fonte N]`~~ — **feito** na mesma sessão após autorização: Ollama 0.33.2 via winget, `qwen3.5:4b`, 3/3 respostas corretas com citação; evidência em [[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]].
2. Criar a tag `v1.0.0` para a primeira release versionada com checksum.
3. Itens que exigem hardware/ambiente real (benchmarks multi-stack, fichas medidas, BOM com cotações, aceitação empresarial) permanecem não iniciados; ver [[00-Inicio/Auditoria-P0]].

## Lições operacionais

- `pip-compile --generate-hashes` travou por 20 min nesta árvore; `uv pip compile` resolveu em 2,5 s com pins idênticos.
- Arquivos `.xlsx` salvos por `openpyxl` perdem valores em cache; `check_tco.py` retorna 2 nesse estado e o recálculo via Excel COM restaura.
- Modelos com *thinking* (Qwen3.5) podem consumir todo o `num_ctx` padrão do Ollama (4096) antes de responder; o script passou a desligar thinking e pedir 8192 explicitamente.
- Selftests com stub determinístico encontram bugs de encanamento (pontuação, locks de arquivo no Windows) que a análise estática não vê.
