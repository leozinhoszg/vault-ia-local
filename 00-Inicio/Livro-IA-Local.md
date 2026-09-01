# IA Local — livro de implementação

> **Propósito.** Este vault é tratado como um livro técnico vivo: cada capítulo explica conceitos, decisões, limitações, implementação, medição, segurança e manutenção. Resumos servem apenas como mapas; as notas de capítulo são a fonte didática principal.

## Como estudar

Leia os capítulos na ordem quando estiver começando. Se você já conhece LLMs, vá diretamente para o capítulo do seu problema, mas leia as seções de memória, avaliação e segurança antes de comprar hardware ou expor um endpoint.

| Capítulo | Pergunta respondida |
|---|---|
| [[01-Fundamentos/LLM-e-inferencia]] | O que é um LLM e como uma geração acontece? |
| [[01-Fundamentos/Regressao-ML]] | Como regressão se relaciona a previsão, avaliação e sistemas de IA local? |
| [[05-Memoria-e-Performance/Quantizacao-livro]] | O que é quantização, o que é FP4 e qual formato escolher? |
| [[05-Memoria-e-Performance/Inferencia-livro]] | Como carregar, executar, medir e otimizar um modelo? |
| [[05-Memoria-e-Performance/KV-cache-formula-e-exemplos]] | Como calcular pesos, KV cache, contexto e concorrência? |
| [[07-Implementacao-Casa/Embeddings-e-vector-search]] | Como transformar documentos em busca semântica? |
| [[07-Implementacao-Casa/RAG-livro]] | Como construir RAG com fontes e avaliação? |
| [[07-Implementacao-Casa/Agentes-e-tool-calling]] | Como permitir que o modelo use ferramentas com segurança? |
| [[06-Treinamento-e-Fine-tuning/Fine-tuning-livro]] | Como adaptar o modelo com dados próprios? |
| [[07-Implementacao-Casa/AI-assisted-coding-tools]] | Como escolher e operar assistentes de programação? |
| [[08-Implementacao-Empresa/01-Arquitetura-de-referencia]] | Como transformar um experimento em serviço empresarial? |
| [[10-Operacao-e-Seguranca/NIST-AI-RMF-GenAI]] | Como governar riscos, avaliações e mudanças? |

## Projeto-guia

Ao longo do livro, implemente um assistente local que responde sobre um repositório de código, cita arquivos e linhas, executa testes em sandbox e pede confirmação antes de alterar o sistema. O projeto deve ter uma versão CPU, uma versão GPU, uma suíte de avaliação e um relatório de custo.

## Critério de conclusão

Um capítulo está concluído quando o leitor consegue explicar o conceito, reproduzir o exemplo, medir o resultado, identificar a falha mais provável, escolher uma alternativa e registrar a decisão no vault. Uma instalação que apenas “responde” não é considerada produção.

## Convenções editoriais

Fatos externos recebem referências numeradas. Números de benchmark sempre incluem variante, dataset, harness, temperatura, contexto e número de tentativas quando disponíveis. Preços são faixas com data. Afirmações não confirmadas permanecem marcadas como hipótese.

## Exercícios integradores

1. Carregue um modelo 8B em CPU e GPU, registre TTFT, tokens/s, RAM, VRAM e qualidade.
2. Compare Q4_K_M, Q5_K_M e uma quantização AWQ no mesmo conjunto de prompts.
3. Calcule o KV cache para quatro sessões de 8K e confirme o pico observado.
4. Construa RAG com dez documentos, exija citações e introduza um documento conflitante.
5. Adicione uma ferramenta de testes com allowlist e tente induzir o agente a executar um comando proibido.
6. Treine um adapter pequeno, compare base/adapter/merged/GGUF e faça rollback.
7. Calcule o break-even de uma workstation versus API para a carga mensal real.

## Referências centrais

[1]: https://github.com/ggml-org/llama.cpp "llama.cpp"
[2]: https://huggingface.co/docs/transformers/index "Hugging Face Transformers"
[3]: https://docs.vllm.ai/ "vLLM"
[4]: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence "NIST AI 600-1"
[5]: https://arxiv.org/abs/2305.14314 "QLoRA"
