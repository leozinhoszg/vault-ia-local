# Verificação factual — PromptQuorum

> **Fonte analisada:** [PromptQuorum — Melhores LLMs locais para programação 2026](https://www.promptquorum.com/pt/local-llms/best-local-llms-for-coding), atualizado em 28 de agosto de 2026. Verificação realizada em 1º de setembro de 2026.

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
| Kimi K2.6 pode ser executado localmente via Ollama com o comando indicado | **Não confirmado como caminho oficial** | O model card oficial mostra Transformers, vLLM, SGLang, Docker Model Runner e quantizações compatíveis com Ollama/llama.cpp, mas a tag exata e a viabilidade dependem do checkpoint convertido. Verifique o repositório da quantização antes de usar um comando `ollama run`. |
| Devstral Small 24B é indicado para coding agentic | **Plausível, requer fonte primária específica** | A característica é coerente com a família Devstral, mas o artigo deve ser complementado pelo model card e pela documentação da versão exata. Não use “16 GB RAM” como requisito universal. |
| Codestral 22B é otimizado para FIM/autocomplete | **Plausível e compatível com o posicionamento do modelo** | O uso em IDE depende de suporte FIM, template, endpoint e integração; confirme a licença da variante exata. |
| Qwen3 8B é adequado para máquinas com 8 GB | **Condicional** | Pode ser viável em quantização baixa, mas “8 GB de RAM” não garante boa experiência: o sistema operacional, runtime, KV cache e contexto também consomem memória. |
| SWE-bench é mais representativo de coding real que HumanEval | **Interpretação válida, não fato absoluto** | SWE-bench cobre issues reais e tarefas multi-arquivo; HumanEval continua útil para funções isoladas. Use ambos e inclua testes próprios. |

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
