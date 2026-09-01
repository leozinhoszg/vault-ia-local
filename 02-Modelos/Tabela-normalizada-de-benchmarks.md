# Tabela normalizada de benchmarks publicados

> **Data de verificação:** 2026-09-01 (todas as linhas capturadas nesta data). **Estado:** ativo. **Dono:** Luiz Guimarães. **Próxima revisão:** 2026-10-01.

Esta tabela existe para impedir o erro mais comum das comparações editoriais: colocar lado a lado um SWE-bench **Pro** e um SWE-bench **Verified**, ou uma única tentativa e uma média de dez. Cada linha registra a variante exata, o harness, a métrica, o número de tentativas, as ferramentas, o contexto e a data de captura, conforme declarado pela fonte primária. Quando um campo não consta na fonte, fica "não consta"; nunca é inferido.

Regras: só entram números de model card ou blog oficial do fabricante; resultados de terceiros (PromptQuorum, Atomic) ficam nas notas editoriais correspondentes. Duas linhas só são comparáveis se coincidirem em variante **e** harness **e** métrica; caso contrário, a comparação é indicativa. Benchmarks próprios seguem [[99-Templates/Registro-de-benchmark]].

## SWE-bench, Terminal-Bench e afins

| Modelo | Benchmark (variante exata) | Resultado | Harness / scaffold | Métrica | Tentativas | Ferramentas | Contexto | Amostragem | Captura | Fonte |
|---|---|---:|---|---|---|---|---|---|---|---|
| Laguna XS 2.1 (33B/3B) | SWE-bench Verified | 70,9 | Harbor + harness poolside, máx. 500 passos, thinking on | média de pass@1 | 4 por tarefa | harness próprio (não detalhado) | 256K | T=1,0, top_k=20, top_p=1 | 2026-09-01 | [1] |
| Laguna XS 2.1 | SWE-bench Multilingual | 63,1 | idem | média de pass@1 | 4 por tarefa | idem | 256K | idem | 2026-09-01 | [1] |
| Laguna XS 2.1 | SWE-Bench Pro (Public) | 47,6 | idem | média de pass@1 | 2 por tarefa | idem | 256K | idem | 2026-09-01 | [1] |
| Laguna XS 2.1 | Terminal-Bench 2.0 | 37,5 | idem; sandbox 48 GB RAM/32 CPUs | média de pass@1 | 5 por tarefa | idem | 256K | idem | 2026-09-01 | [1] |
| Laguna S 2.1 (118B/8B) | SWE-bench Multilingual | 78,5 | não capturado nesta leitura | não consta | não consta | não consta | não consta | não consta | 2026-09-01 | [2] |
| Laguna S 2.1 | SWE-Bench Pro (Public) | 59,4 | não capturado nesta leitura | não consta | não consta | não consta | não consta | não consta | 2026-09-01 | [2] |
| Laguna S 2.1 | Terminal-Bench **2.1** | 70,2 | não capturado nesta leitura | não consta | não consta | não consta | não consta | não consta | 2026-09-01 | [2] |
| Kimi K2.6 (1T/32B) | SWE-bench Verified | 80,2 | framework adaptado do SWE-agent, thinking | média | 10 execuções independentes | bash, createfile, insert, view, strreplace, submit | geração máx. 98.304 tokens | T=1,0, top_p=1,0 | 2026-09-01 | [3] |
| Kimi K2.6 | SWE-Bench Pro | 58,6 | idem, ferramentas mínimas | média | 10 execuções | idem | idem | idem | 2026-09-01 | [3] |
| Kimi K2.6 | SWE-bench Multilingual | 76,7 | idem | média | 10 execuções | idem | idem | idem | 2026-09-01 | [3] |
| Kimi K2.6 | Terminal-Bench 2.0 | 66,7 | Terminus-2 (framework padrão), preserve thinking | não consta | não consta | Terminus-2 | idem | idem | 2026-09-01 | [3] |
| Kimi K2.6 | LiveCodeBench v6 | 89,6 | metodologia oficial do benchmark | não consta | não consta | — | idem | idem | 2026-09-01 | [3] |
| Kimi K2.7 Code (1T/32B) | SWE-bench (qualquer variante) | **não publicado** | — | — | — | — | — | — | 2026-09-01 | [4] |
| Kimi K2.7 Code | MCP-Atlas | 76,0 | Kimi Code CLI, thinking | média | 3 execuções | orçamento de 100 tool calls, 32K tokens/passo | 262.144 | T=1,0, top_p=0,95 | 2026-09-01 | [4] |
| Kimi K2.7 Code | MCPMark Verified | 81,1 | idem | média | 3 execuções | idem | 262.144 | idem | 2026-09-01 | [4] |
| Qwen3.6-27B (27B dense) | SWE-bench Verified | 77,2 | scaffold interno (bash + edição de arquivos) | não consta | não consta | bash, file-edit | 200K | T=1,0, top_p=0,95 | 2026-09-01 | [5] |
| Qwen3.6-27B | SWE-bench Pro | 53,5 | idem | não consta | não consta | idem | 200K | idem | 2026-09-01 | [5] |
| Qwen3.6-27B | SWE-bench Multilingual | 71,3 | idem | não consta | não consta | idem | 200K | idem | 2026-09-01 | [5] |
| Qwen3.6-27B | Terminal-Bench 2.0 | 59,3 | Harbor/Terminus-2; timeout 3 h; 32 CPU/48 GB RAM | média | 5 execuções | Terminus-2 | 256K; max_tokens 80K | T=1,0, top_p=0,95, top_k=20 | 2026-09-01 | [5] |
| Qwen3.6-27B | LiveCodeBench v6 | 83,9 | não consta | não consta | não consta | — | não consta | não consta | 2026-09-01 | [5] |
| Qwen3-Coder-Next (80B/3B) | SWE-bench Verified | 70,6 | não consta no card | não consta | não consta | não consta | não consta | não consta | 2026-09-01 | [6] |
| Qwen3-Coder-Next | SWE-bench Pro | 44,3 | não consta no card | não consta | não consta | não consta | não consta | não consta | 2026-09-01 | [6] |
| Qwen3-Coder-Next | Terminal-Bench 2.0 | 36,2 | não consta no card | não consta | não consta | não consta | não consta | não consta | 2026-09-01 | [6] |

## Como ler

- **Verified ≠ Pro.** Na mesma fonte, o Pro fica 20 a 25 pontos abaixo do Verified (Laguna XS 2.1: 70,9 vs 47,6; Kimi K2.6: 80,2 vs 58,6; Qwen3.6-27B: 77,2 vs 53,5). Comparar o 58,6 Pro do Kimi com o 77,2 Verified do Qwen inverte o ranking real: no Verified, o Kimi K2.6 publica 80,2.
- **Tentativas mudam o número.** Média de 10 execuções (Kimi) e média de 4 (Laguna) suavizam variância; um resultado de execução única costuma ser mais baixo ou mais volátil. "pass@1" aqui é sempre média de pass@1, não pass@k.
- **Harness muda o número.** Scaffold interno (Qwen), SWE-agent adaptado (Kimi) e Harbor (Laguna) têm ferramentas e limites de passos diferentes; os Terminal-Bench 2.0 de Qwen e Kimi usam Terminus-2 e são os mais próximos de comparáveis desta tabela.
- **Terminal-Bench 2.0 ≠ 2.1.** O card da Laguna S 2.1 reporta a versão 2.1; a nota editorial da Atomic escreve apenas "Terminal-Bench". Registrar a versão.
- **Benchmarks internos não entram no ranking.** Kimi Code Bench v2, Program Bench etc. medem progresso K2.6 → K2.7 Code dentro da Moonshot; não comparam com outros fabricantes.
- **Tamanho de parâmetros não está nesta tabela por acaso.** A relação entre benchmark e viabilidade local passa por [[02-Modelos/Local-real-vs-cloud]] e [[03-Hardware/Calculadora-de-memoria]]: o Kimi K2.6 lidera o Verified e não roda em máquina doméstica; o Laguna XS 2.1 fica 9 pontos abaixo e cabe em 20,3 GB.

## Modelo de linha para novas entradas

```text
| <modelo (totais/ativos)> | <benchmark e variante exata> | <valor> | <harness/scaffold, limite de passos, thinking> | <média de pass@1 | pass@k | acurácia> | <N por tarefa ou N execuções> | <ferramentas> | <contexto> | <T, top_p, top_k> | <AAAA-MM-DD da captura> | [n] |
```

## Referências

[1]: https://huggingface.co/poolside/Laguna-XS-2.1 "poolside — Laguna XS 2.1 model card (benchmarks e metodologia Harbor)"
[2]: https://huggingface.co/poolside/Laguna-S-2.1 "poolside — Laguna S 2.1 model card (benchmarks datados de 2026-07-21)"
[3]: https://huggingface.co/moonshotai/Kimi-K2.6 "Moonshot AI — Kimi K2.6 model card (benchmarks, média de 10 execuções, ferramentas)"
[4]: https://huggingface.co/moonshotai/Kimi-K2.7-Code "Moonshot AI — Kimi K2.7 Code model card (benchmarks internos e MCP; sem SWE-bench)"
[5]: https://huggingface.co/Qwen/Qwen3.6-27B "Qwen — Qwen3.6-27B model card (benchmarks e notas de metodologia)"
[6]: https://huggingface.co/Qwen/Qwen3-Coder-Next "Qwen — Qwen3-Coder-Next model card (benchmarks sem metodologia detalhada)"
