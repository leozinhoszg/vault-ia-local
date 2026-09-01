# Auditoria P0 — verificação das correções

<!-- validador: sem-referencias: relatório interno; as evidências (células, comandos, versões) estão citadas inline e as fontes externas ficam nas notas auditadas -->

**Data da auditoria:** 1º de setembro de 2026. **Revisão:** 4 (as revisões 1–3 cobrem a reconciliação da planilha e o pipeline RAG anterior; a revisão 4 substitui o exemplo Chroma vulnerável por retrieval efêmero e reabre explicitamente os gates Windows/Ollama). **Resultado:** aprovado no escopo estático, editorial e dos smokes isolados descritos abaixo; validação ponta a ponta da implementação atual permanece aberta.

| Item | Verificação | Resultado |
|---|---|---|
| Rastros de prompt | Varredura textual e revisão dos finais das três notas indicadas. | Corrigido; blocos após referências removidos. O validador não encontrou trace ou segredo nesta execução. |
| RAG executável | Commit `ffec088e2c2af03ff85d318673b6bcc7ab555539`: Chroma/requests removidos; retrieval cosine exato em memória; enumeração, bytes, texto, chunks, PDF e HTTP limitados; fontes relativas; embedding default fixado por SHA; PDF default-deny; Ollama loopback sem proxy/redirect. Smokes em container Linux/Python 3.11 sem bind mount do host. | **Parcialmente validado na implementação atual**: selftest exit 0; embedding real recuperou a fonte correta; PDF opt-in funcionou e limite de páginas falhou fechado; gate negativo requirements↔lock funcionou. Evidência: [[07-Implementacao-Casa/Evidencias/RAG-hardening-2026-09-01]]. O teste Windows/Ollama anterior está preservado em [[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]], mas é histórico e não valida este patch. |
| GB/GiB | Fórmula revisada para `/1e9` em GB decimal e `/2^30` em GiB binário. | Corrigido; exemplos recalculados, incluindo 27B Q4. |
| TCO API | Texto e planilha usam 100M input, 20M cached e 25M output, câmbio R$5,50. | Reconciliado: Sol R$4.994, Terra R$2.772, Luna R$277,20. |
| TCO local | Componentes separados entre CAPEX, energia, refrigeração, manutenção e operação. | Reconciliado em R$1.768,50/mês para as premissas atuais. |
| Break-even | Revisão 1: `Break_even!E2:E4` dividia o TCO em BRL por um custo blended em USD, o que produziria 282,41M, 508,79M e 5.087,93M. Revisão 2: fórmula reescrita como `TCO local ÷ (custo API BRL ÷ tokens totais)`, com o blended em BRL exposto em `Break_even!H2:H4`. | Reconciliado após correção: 51,35M, 92,51M e 925,08M tokens/mês para Sol, Terra e Luna, verificados por recomputação independente em Python. |
| Valor residual | `Local!C2` usava apenas `CAPEX / vida útil`. | Corrigido: `(CAPEX − valor residual) / vida útil`. Com residual zero o resultado não muda. |
| Batch API | O fator existia em `Premissas!B20` mas não participava de nenhum cálculo. | Corrigido: `API_OpenAI!G` e `Break_even!G` mostram custo e break-even com Batch (fator aplicado ao custo inteiro; ver limitação). |
| Contexto longo | Um único fator era aplicado a entrada, cache e saída. | Corrigido: fatores separados em `Premissas!B21`, `B23` e `B24`, todos com valor 1 até confirmação do preço aplicável. |
| Sensibilidade | Somente câmbio, e sem os fatores de contexto longo e cache writes. | Corrigido: o bloco de câmbio agora deriva de `API_OpenAI!E` (inclui todos os fatores) e foram adicionados blocos de vida útil, utilização e tarifa de energia. |
| Preços | Data de consulta, Batch, contexto longo e cache writes são premissas editáveis. | Mantido com ressalva: revalidar preços e contrato antes de uso. |
| Estrutura da planilha | Verificado com `openpyxl`: na revisão 2 não havia tabelas estruturadas (a alegação de tabelas em `A1:H1`/`A1:H19` não procedia), apenas autofiltros herdados curtos. | Revisão 3: `99-Templates/recalcular_tco.ps1` cria tabelas estruturadas reais (`tBreakEven` A1:H4, quatro tabelas em `Sensibilidade` até A19:F24, `tPremissas`, `tAPI`, `tLocal`, `tChecks`), recalcula no Excel e salva com valores em cache. |
| Aba `Checks` e conferência | `Checks` reconcilia TCO, três break-evens, custo API, mix e premissas por fórmulas independentes; `99-Templates/check_tco.py` recalcula tudo em Python e compara com os valores em cache. | `STATUS GERAL = PASS`; `check_tco.py` exit 0 (TCO 1.768,50; 51,35 / 92,51 / 925,08). Anuidade com taxa de desconto implementada como opção (`Método de CAPEX = 1`). |
| Lockfile e gate | Lock Windows/Python 3.11 regenerado com uv 0.12.8 e hashes: 43 pins, sha256 `f5256db8…`; requirements diretos reconciliados contra o lock; pypdf mínimo 6.15.0; SCA fail-closed; Actions por SHA; Dependabot semanal. | Gate local do commit `ffec088`: validador `--strict` exit 0 (0 erros/avisos), índice `--check` exit 0, `check_tco.py` PASS, checksum OK, selftest OK e pip-audit 2.10.1 sem vulnerabilidades conhecidas. A execução `33524666554` continua evidência histórica do pipeline anterior; o CI remoto no SHA atual ainda precisa ser observado no PR. |

## Método de verificação do break-even

As fórmulas foram lidas com `openpyxl`, todas as referências de célula foram checadas contra células não vazias e os valores esperados foram recomputados fora da planilha com as mesmas premissas. A planilha é salva sem valores em cache, portanto o recálculo no Excel/LibreOffice na abertura é o teste final de aceitação.

## Pendências abertas

- RAG atual: instalar o lock novo em Windows limpo e repetir retrieval/geração com Ollama, inclusive ausência de evidência, timeout e limite de resposta.
- RAG: avaliação quantitativa (recall@k, groundedness) em corpus real e maior ainda não medida; o smoke atual usou 2 documentos pequenos.
- Bloco de vida útil da `Sensibilidade` usa amortização linear mesmo com `Método de CAPEX = 1`; o fator Batch é aplicado a 100% do custo.
- Preços da API são premissas datadas e devem ser reconsultados na data da decisão.
- O job de release só roda em tags `v*`; nenhuma release foi publicada ainda.

## Fora do alcance desta auditoria (exigem hardware ou ambiente real)

Os itens abaixo, pedidos na revisão externa, não podem ser fechados por edição documental e permanecem **não iniciados**: benchmarks próprios em NVIDIA/AMD/Apple com múltiplos SOs, modelos, quantizações e contextos ([[05-Memoria-e-Performance/Benchmarking]]); fichas completas dos modelos prioritários com memória medida e benchmark próprio ([[02-Modelos/Fichas/Registro-de-modelos-prioritarios]]); cotações brasileiras reais na BOM ([[03-Hardware/BOM-brasileira-datada]]); aceitação empresarial executada — SSO/OIDC, RBAC, isolamento, prompt injection, backup/restore, failover, carga, SLO, incidente e checklist LGPD ([[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]]). Nenhum número desses domínios foi adicionado sem medição.

## Limites da aprovação

A aprovação significa que a consistência editorial, matemática e estrutural foi corrigida e verificada pelos métodos acima. Não significa que a API foi faturada em produção, que os preços permanecerão vigentes ou que o modelo local entrega a mesma qualidade. O próximo teste de aceitação deve executar o cookbook em cada plataforma-alvo e comparar a fatura real com a planilha.

Para o RAG da revisão 4, aprovação também não significa sandbox de PDF, eliminação atômica de toda janela TOCTOU, instalação do lock Windows nem geração Ollama atual. Esses gates só fecham com as evidências pendentes listadas acima.
