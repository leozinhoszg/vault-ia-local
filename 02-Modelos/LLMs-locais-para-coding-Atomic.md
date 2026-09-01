# LLMs locais para coding — guia Atomic

> Esta nota registra e contextualiza as informações do guia **Best Local LLM for Coding in 2026**, da Atomic Chat, consultado em 1º de setembro de 2026 [1]. Os números de VRAM e velocidade são resultados publicados pela Atomic em seu próprio teste, com seu hardware e sua configuração; não devem ser tratados como garantia universal.

## Recomendação resumida

O guia recomenda escolher o melhor modelo que **a sua máquina consegue executar com velocidade aceitável**, e não o maior modelo existente. A conclusão central é que modelos locais de aproximadamente 24–30B oferecem um equilíbrio especialmente favorável entre qualidade, velocidade e facilidade de implantação em uma GPU de 24 GB. O artigo aponta o **Qwen3-Coder 30B** como melhor opção geral para coding local no momento do teste, o **Qwen3-Coder-Next 80B** para máquinas muito fortes e a **Laguna S 2.1** para workstations ou servidores com grande capacidade de memória.

O guia também afirma que modelos de 200B–300B ou mais podem ter qualidade superior, mas não são realistas em hardware doméstico comum. Sua regra prática é aproximadamente 1 GB de VRAM por bilhão de parâmetros para modelos não comprimidos ou cenários conservadores; isso é uma heurística, não uma fórmula exata, pois quantização, arquitetura, contexto e KV cache alteram o resultado.

## Modelos comparados pela Atomic

| Modelo | Arquitetura | Parâmetros | Contexto | VRAM Q4 publicada | Velocidade no teste Atomic | Perfil |
|---|---|---:|---:|---:|---:|---|
| Qwen3-Coder 30B | MoE, 128 experts, 8 roteados ativos | 30,5B total / 3,3B ativos | 256K; até 1M com YaRN | ~22 GB | 220 tok/s | Melhor equilíbrio geral para coding local. |
| Qwen3-Coder-Next 80B | MoE, 512 experts, 10 roteados + 1 compartilhado | 80B total / ~3B ativos | 256K | ~45 GB | 5,5 tok/s | Melhor raciocínio em máquina grande; lento em hardware de consumo. |
| Laguna S 2.1 | MoE, padrão e thinking | 118B total / ~8B ativos | Até 1M | ~96 GB Q4; ~67 GB NVFP4 | Não publicado | Coding agentic em workstation/servidor. |
| Gemma 4 26B A4B | MoE | 26B total / ~4B ativos | 256K | ~12–18 GB | 136 tok/s | Opção compacta e rápida. |
| Qwen3.6 27B | Dense | 27B | 256K; até 1M com extensão | ~17–18 GB | 47 tok/s | Alternativa densa com bom equilíbrio. |

## Benchmarks mencionados

| Modelo ou referência | SWE-bench Verified | SWE-bench Pro | Terminal-Bench |
|---|---:|---:|---:|
| Qwen3.6 27B | 77,2% | — | — |
| Qwen3-Coder-Next 80B | 70,6% | 44,3% | 36,2% |
| Laguna S 2.1 | — | 59,4% | 70,2% com thinking |
| Modelos open-weight grandes citados | ~80% | — | — |

Benchmarks de coding medem dimensões diferentes. SWE-bench verifica correções em issues reais; LiveCodeBench reduz o risco de contaminação usando problemas posteriores ao cutoff; Terminal-Bench mede tarefas agentic de linha de comando. Nenhum benchmark substitui uma suíte com os repositórios, linguagens, ferramentas e padrões de erro da sua equipe.

## Tradução para decisões de hardware

| Memória de acelerador disponível | Recomendação de coding local |
|---:|---|
| 8–12 GB | Modelos menores; não perseguir 27–30B se a prioridade for velocidade. |
| 16 GB | Gemma 4 26B A4B ou Qwen3.6 27B podem exigir ajustes de quantização/offload; prefira contexto moderado. |
| 24 GB | Ponto ideal para Qwen3-Coder 30B Q4 (~22 GB publicado) ou Qwen3.6 27B Q4 (~17–18 GB). Reserve memória para KV cache. |
| 32 GB | Boa margem para 27–30B, contexto maior e buffers; Qwen3-Coder-Next 80B ainda precisará de memória adicional. |
| 48 GB | Qwen3-Coder-Next 80B Q4 começa a ser viável, mas o teste Atomic reportou somente 5,5 tok/s em sua configuração; avalie se o custo compensa. |
| 64–96 GB | Qwen3-Coder-Next 80B com mais conforto; Laguna S 2.1 em quantização agressiva pode ser possível no limite inferior. |
| 96–128 GB | Laguna S 2.1 Q4/NVFP4 ou Mac/servidor de alta memória, sujeito a runtime e largura de banda. |

A recomendação de “24 GB para 27–30B” não significa que toda GPU de 24 GB terá a mesma velocidade. O resultado depende de largura de banda, kernel, versão do runtime, número de camadas no acelerador, contexto e temperatura. Para verificar a sua máquina, use [[03-Hardware/Sizing-9B-14B-27B-70B]].

## Critérios para coding agentic

Para coding assistido por agente, avalie mais que a resposta de um prompt isolado. O modelo precisa seguir instruções de ferramentas, editar arquivos, interpretar testes, recuperar de erros, produzir JSON válido e evitar ações perigosas. O guia relata que Qwen3-Coder 30B foi eficiente em tarefas de simulação e Snake, com cerca de 1.840 tokens em uma tarefa de física durante o teste Atomic; esse dado é específico do experimento.

No seu benchmark, registre: taxa de testes aprovados, número de iterações, tokens consumidos, chamadas de ferramenta malformadas, tempo até o primeiro patch, tempo até a solução, alterações fora do escopo e necessidade de intervenção humana.

## Atomic Chat como opção de cliente

O artigo também apresenta o Atomic Chat como aplicativo open source para baixar modelos de pesos abertos do Hugging Face e executá-los localmente, com API compatível com OpenAI para integração com IDEs e ferramentas como Claude Code. Antes de usar em empresa, confirme versão, licença do aplicativo, origem dos binários, telemetria, política de atualização e controles de rede.

## Limitações e cuidados de interpretação

As recomendações são editoriais e baseadas em testes da Atomic, não em uma avaliação independente. A nota deve ser atualizada quando houver nova versão do guia, mudança nos modelos, novos quantizadores ou resultados reproduzidos em hardware brasileiro. A velocidade de 220 tok/s, por exemplo, é uma observação de teste, não uma especificação do Qwen3-Coder 30B.

## Referências

[1]: https://atomic.chat/blog/guides/best-local-llms-for-coding "Atomic Chat — Best Local LLM for Coding in 2026: A Comprehensive Guide"
[2]: https://huggingface.co/Qwen/Qwen3-Coder-Next "Qwen3-Coder-Next — model card"
[3]: https://huggingface.co/Qwen/Qwen3.6-35B-A3B "Qwen3.6-35B-A3B — model card relacionado"
[4]: https://github.com/ggml-org/llama.cpp "llama.cpp — backends e inferência local"
[5]: https://docs.vllm.ai/ "vLLM — serving e batching"
