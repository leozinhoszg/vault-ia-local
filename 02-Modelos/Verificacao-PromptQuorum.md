# Verificação factual — PromptQuorum

> **Fonte analisada:** [PromptQuorum — Melhores LLMs locais para programação 2026](https://www.promptquorum.com/pt/local-llms/best-local-llms-for-coding). **Captura:** 1º de setembro de 2026 (rev. 2 desta nota, mesma data). A página exibe datas internas conflitantes — ver "Datas internas da página" abaixo; por isso toda extração daqui carrega a data de captura, não a data declarada pelo artigo.

Esta nota confronta o artigo indicado com model cards e páginas oficiais. O objetivo não é desqualificar o artigo, mas separar **fato primário**, **resultado editorial reproduzível somente no ambiente do autor** e **afirmação que precisa de correção ou confirmação adicional**.

## Resultado da verificação

| Afirmação do PromptQuorum | Resultado | Evidência / interpretação |
|---|---|---|
| Qwen3.6-27B tem 27B e é dense | **Confirmado** | O model card oficial informa 27B e arquitetura densa. |
| Qwen3.6-27B tem contexto nativo de 262.144 tokens, extensível a aproximadamente 1,01M | **Confirmado no model card** | A extensão depende do método, runtime e qualidade no contexto longo; não equivale a custo baixo. |
| Qwen3.6-27B alcança 77,2% no SWE-bench Verified | **Confirmado no relatório Qwen** | O artigo do Qwen também publica 53,5 no SWE-bench Pro e 59,3 no Terminal-Bench 2.0; “SWE-bench” sem variante é ambíguo. |
| Qwen3.6-27B exige exatamente 22 GB de VRAM em Q4 | **Não confirmado como requisito universal** | O valor é editorial. Arquivo, runtime, contexto, KV cache, multimodalidade e buffers alteram o pico. Para sizing, use a nota [[03-Hardware/Sizing-9B-14B-27B-70B]]. |
| Kimi K2.6 tem 1T total / 32B ativos | **Confirmado** | O model card oficial informa MoE de 1T total, 32B ativos, 384 experts, 8 selecionados e 1 compartilhado. |
| Kimi K2.6 tem licença MIT modificada | **Confirmado** | O model card informa `modified-mit`; leia o texto integral da licença antes de uso comercial. |
| Kimi K2.6 tem 256K de contexto | **Confirmado** | O model card oficial publica contexto de 256K. |
| Kimi K2.6 cabe em aproximadamente 22 GB em Q4 | **Rejeitado para planejamento** | A afirmação é incompatível com um MoE de 1T se os pesos totais forem armazenados em 4 bits: o piso teórico dos pesos é aproximadamente 500 GB, antes de escalas e overhead. Parâmetros ativos reduzem computação por token, não removem os pesos dos experts da memória. O próprio model card apresenta implantação com infraestrutura de serving e não deve ser interpretado como “GPU doméstica de 22 GB”. |
| Kimi K2.6 marcou 58,6 no SWE-bench Pro | **Confirmado no model card** | O card oficial publica 58,6 no SWE-Bench Pro e 80,2 no SWE-Bench Verified, sob as condições descritas pelo autor. |
| Kimi K2.6 pode ser executado localmente via Ollama com `ollama run kimi-k2.6` | **Rejeitado como prova de inferência local** | Na biblioteca oficial do Ollama, a única tag publicada para o modelo é `kimi-k2.6:cloud` (1,04T parâmetros, 256K, sem tamanho de download) [7]. O comando executa no serviço cloud do Ollama, com o prompt saindo da máquina; não demonstra execução local. O mesmo vale para `ollama run kimi-k2.7-code`, cuja única tag é `kimi-k2.7-code:cloud`, com preço por token na página [8]. Ver [[02-Modelos/Local-real-vs-cloud]]. |
| Laguna XS 2.1 (poolside, 2 de julho de 2026) é MoE de 33B total / 3B ativo com contexto de 256K e 70,9% no SWE-bench Verified | **Confirmado no model card e no blog oficial** | 33B/3B, 262.144 tokens, OpenMDW-1.1, lançado em 2026-07-02; 70,9% é média de pass@1 em 4 tentativas, harness próprio sobre Harbor, thinking ligado. O GGUF oficial Q4_K_M tem 20,3 GB e `ollama run laguna-xs-2.1` baixa 20 GB para execução local [9][10]. Ficha: [[02-Modelos/Fichas/Laguna-XS-2.1]]. |
| Kimi K2.7 Code é a evolução do K2.6 focada em código para sessões de longo horizonte | **Confirmado no model card, com ressalva de escala** | 1T total / 32B ativos, 256K, INT4 nativo, Modified MIT; repositório de 595 GB; hardware de referência H200 ×8 ou RAM de ~2 TB com KTransformers. O card não publica SWE-bench. Continua modelo de infraestrutura de alta memória, apesar dos parâmetros ativos reduzidos [11]. Ficha: [[02-Modelos/Fichas/Kimi-K2.7-Code]]. |
| Devstral Small 24B é indicado para coding agentic | **Plausível, requer fonte primária específica** | A característica é coerente com a família Devstral, mas o artigo deve ser complementado pelo model card e pela documentação da versão exata. Não use “16 GB RAM” como requisito universal. |
| Codestral 22B é otimizado para FIM/autocomplete | **Plausível e compatível com o posicionamento do modelo** | O uso em IDE depende de suporte FIM, template, endpoint e integração; confirme a licença da variante exata. |
| Qwen3 8B é adequado para máquinas com 8 GB | **Condicional** | Pode ser viável em quantização baixa, mas “8 GB de RAM” não garante boa experiência: o sistema operacional, runtime, KV cache e contexto também consomem memória. |
| SWE-bench é mais representativo de coding real que HumanEval | **Interpretação válida, não fato absoluto** | SWE-bench cobre issues reais e tarefas multi-arquivo; HumanEval continua útil para funções isoladas. Use ambos e inclua testes próprios. |

## Três correções que não devem ser importadas do artigo

1. **`ollama run kimi-k2.6` não prova inferência local.** O comando oficial vigente é `kimi-k2.6:cloud` [7]; a inferência acontece nos servidores do Ollama. Qualquer nota que use esse comando como evidência de "roda na minha máquina" está errada. Registre o modo de execução conforme [[02-Modelos/Local-real-vs-cloud]].
2. **Um modelo de 1T não cabe em 22 GB em Q4.** O piso teórico dos pesos em 4 bits é aproximadamente 500 GB; o checkpoint INT4 nativo do K2.7 Code tem 595 GB e o GGUF mais agressivo (IQ1_M) ainda tem 304 GB [11]. Parâmetros ativos reduzem computação, não armazenamento.
3. **58,6 (Kimi) e 77,2 (Qwen) são benchmarks diferentes.** O 58,6 do Kimi K2.6 é SWE-bench **Pro**; o 77,2 do Qwen3.6-27B é SWE-bench **Verified**. No Verified, o Kimi K2.6 publica 80,2; no Pro, o Qwen publica 53,5. Comparar os dois números originais inverte o ranking. A tabela com variante, harness, tentativas e data está em [[02-Modelos/Tabela-normalizada-de-benchmarks]].

## Datas internas da página

Na captura de 2026-09-01, a página exibia simultaneamente "Last updated: 28 de agosto de 2026", "Atualizado: 2026-05-04" no bloco de resposta rápida, "Em julho de 2026, os melhores modelos..." no corpo e "Laguna XS 2.1 (Poolside, 2 de julho de 2026)". Não há como saber qual trecho foi revisado em qual data. Regra adotada: cada afirmação extraída desta fonte carrega a data de captura e é confrontada com a fonte primária na mesma data; a data declarada pelo artigo é registrada apenas como metadado.

## Correção crítica para o hardware

A regra “1 GB de VRAM por bilhão de parâmetros” é uma heurística conservadora para modelos em precisões altas ou para planejamento sem quantização. Ela não deve ser combinada com a afirmação de que um MoE de 1T cabe em 22 GB Q4. Para modelos MoE, registre sempre:

| Dimensão | Por que importa |
|---|---|
| Parâmetros totais | Determinam aproximadamente os pesos que precisam ser armazenados. |
| Parâmetros ativos | Determinam parte do custo computacional por token, não o footprint completo. |
| Bits por peso | Determinam o piso de memória dos pesos. |
| KV cache | Cresce com contexto, camadas, precisão e número de sessões. |
| Runtime | Pode exigir buffers e formatos específicos. |
| Offload | Pode distribuir pesos entre VRAM, RAM e armazenamento, mas a velocidade pode cair muito. |

Para uma única GPU de 24 GB, a recomendação segura do artigo é reinterpretada assim: **Qwen3.6-27B ou outro modelo denso de aproximadamente 27–30B em Q4 pode ser uma classe plausível**, enquanto Kimi K2.6 de 1T total não deve ser tratado como modelo doméstico de 22 GB sem uma técnica explícita de compressão, offload extremo ou serviço remoto que altere o problema.

## Benchmarks: como registrar corretamente

O Qwen3.6-27B model card informa, sob seu próprio harness e configurações, 77,2 no SWE-bench Verified, 53,5 no SWE-bench Pro e 59,3 no Terminal-Bench 2.0. O Kimi K2.6 model card informa 80,2 no SWE-bench Verified e 58,6 no SWE-bench Pro. Esses resultados não são diretamente comparáveis sem verificar dataset, harness, temperatura, contexto, número de tentativas, ferramentas e correções do conjunto.

Registre a variante do benchmark no nome da métrica. Por exemplo, use `SWE-bench Verified`, `SWE-bench Pro` ou `Terminal-Bench 2.0`, e não somente `SWE-bench`. Para decisão de compra, reproduza uma amostra com os repositórios e linguagens da equipe.

## Recomendação final incorporada ao vault

Para uma máquina doméstica com 16–24 GB de VRAM, priorize modelos densos ou MoE cujo **arquivo quantizado e KV cache medido** caibam com margem. Para 27–30B, uma GPU de 24 GB é um alvo realista para Q4, sujeito a contexto moderado. Para modelos MoE com centenas de bilhões ou 1T de parâmetros totais, planeje multi-GPU, memória unificada muito grande, offload e velocidade reduzida; não dimensione pelo número de parâmetros ativos.

## Referências

[1]: https://www.promptquorum.com/pt/local-llms/best-local-llms-for-coding "PromptQuorum — Melhores LLMs locais para programação 2026"
[2]: https://huggingface.co/moonshotai/Kimi-K2.6 "Moonshot AI — Kimi K2.6 model card"
[3]: https://huggingface.co/Qwen/Qwen3.6-27B "Qwen — Qwen3.6-27B model card"
[4]: https://qwen.ai/blog?id=qwen3.6-27b "Qwen — Qwen3.6-27B technical blog"
[5]: https://github.com/ggml-org/llama.cpp "llama.cpp — quantização, backends e offload"
[6]: https://huggingface.co/docs/transformers/en/quantization/bitsandbytes "Hugging Face — quantização com bitsandbytes"
[7]: https://ollama.com/library/kimi-k2.6 "Ollama — kimi-k2.6 (única tag: :cloud)"
[8]: https://ollama.com/library/kimi-k2.7-code "Ollama — kimi-k2.7-code (única tag: :cloud; preço por token)"
[9]: https://ollama.com/library/laguna-xs-2.1 "Ollama — laguna-xs-2.1 (download local de 20 GB em Q4_K_M)"
[10]: https://huggingface.co/poolside/Laguna-XS-2.1 "poolside — Laguna XS 2.1 model card"
[11]: https://huggingface.co/moonshotai/Kimi-K2.7-Code "Moonshot AI — Kimi K2.7 Code model card"
