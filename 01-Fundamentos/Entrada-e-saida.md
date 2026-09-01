# Entrada, saída e contexto

> **Pergunta que esta nota responde.** O que exatamente entra no modelo, o que sai, o que é a "janela de contexto" que limita os dois, e por que entrada e saída custam de forma tão diferente.

## 1. O que é a entrada

A entrada (**prompt**, no sentido amplo) é **tudo** o que o modelo recebe antes de começar a responder. Em uma conversa comum, ela é montada pelo runtime a partir de várias partes:

| Parte | Quem coloca | Exemplo | Custo em tokens |
|---|---|---|---|
| **System prompt** | A aplicação ou o Modelfile | "Você é um assistente que responde em português e cita fontes." | Dezenas a centenas, em **toda** mensagem |
| **Histórico** | O runtime, automaticamente | Suas perguntas e as respostas anteriores | Cresce a cada turno |
| **Documentos / trechos de RAG** | O pipeline de busca | Os chunks recuperados dos seus PDFs | Centenas a milhares |
| **Sua mensagem** | Você | "Qual a antecedência para pedir férias?" | Dezenas |

Exemplo real do vault: no RAG testado em [[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]], a pergunta sobre backup gerou **358 tokens de entrada** (instrução + trechos recuperados + pergunta) para **48 tokens de saída**. A pergunta em si tinha poucas palavras; o resto era o "material de apoio" que o pipeline anexou.

O modelo não distingue essas partes por mágica: tudo vira uma única sequência de tokens ([[01-Fundamentos/Parametros-e-tokens]]). Formatos de chat usam marcadores especiais para indicar quem falou; é o runtime que os insere.

## 2. O que é a saída

A saída é o texto gerado, **um token por vez**. A cada passo o modelo produz uma distribuição de probabilidade sobre o próximo token; uma estratégia de amostragem (temperatura, top-p, etc.) escolhe um; ele é acrescentado à sequência e o ciclo repete até um token de parada ou um limite ([[01-Fundamentos/LLM-e-inferencia]]).

Consequências práticas:

- **A saída é a parte lenta.** Cada token exige ler os pesos inteiros da memória; por isso a velocidade se mede em tokens por segundo e é limitada pela banda de memória ([[03-Hardware/Por-que-VRAM-RAM-e-CPU-importam]]).
- **A saída também ocupa contexto.** Os tokens gerados entram na mesma janela que a entrada.
- **Modo thinking gera tokens que você não vê.** O rascunho interno conta como saída e consome contexto. No RAG do vault, thinking ligado com janela de 4096 devolvia resposta vazia; a correção foi desligar thinking por padrão e pedir 8192 de contexto ([[07-Implementacao-Casa/03-RAG-deploy]]).
- **Há um limite de saída configurável** (no Ollama, `num_predict`), separado do contexto. Estourou, a resposta é cortada no meio.

## 3. A janela de contexto: entrada + saída

A janela de contexto é o número máximo de tokens que o modelo consegue ter "em vista" ao mesmo tempo — **entrada e saída somadas**. Duas grandezas diferentes se escondem sob o mesmo nome:

| Grandeza | Quem define | Onde ver | Exemplo |
|---|---|---|---|
| **Contexto nativo do modelo** | O treino; é uma propriedade do modelo | Model card ([[02-Modelos/Como-ler-um-model-card]]) | 262.144 tokens no Laguna XS 2.1 |
| **Contexto pedido ao runtime** | Você, na configuração | `num_ctx` / `OLLAMA_CONTEXT_LENGTH` no Ollama, padrão **4096** [1]; `-c` no llama.cpp | O script RAG do vault pede 8192 |

O runtime nunca dá mais que o nativo, e por padrão dá bem menos, porque contexto custa memória: o KV cache cresce linearmente com os tokens ([[05-Memoria-e-Performance/KV-cache-formula-e-exemplos]]). Um modelo de 8B típico gasta ~128 KiB por token de KV em FP16; 8K de contexto são ~1 GiB, 32K são ~4 GiB — além dos pesos.

**O que acontece quando estoura?** Depende do runtime: alguns descartam o início da conversa silenciosamente (o modelo "esquece" o system prompt ou as primeiras instruções), outros truncam a entrada, outros devolvem erro ou resposta vazia. Nenhum desses comportamentos é bom; a defesa é medir tokens de entrada e dimensionar `num_ctx` com folga para a saída esperada.

## 4. Por que entrada e saída custam diferente

| | Entrada (prefill) | Saída (decode) |
|---|---|---|
| Como é processada | Todos os tokens de uma vez, em paralelo | Um token por vez, em sequência |
| Gargalo | Computação (FLOPs) | Banda de memória (ler os pesos a cada token) |
| Métrica | TTFT — tempo até a primeira palavra | tokens/s |
| O que piora | Prompts longos, muitos documentos de RAG | Modelos grandes, banda baixa, offload para RAM |
| Custo relativo | Barato por token | Caro por token |

É por isso que uma API cobra tokens de saída mais caro que tokens de entrada, e por isso um prompt de 2.000 tokens com resposta de 100 costuma ser mais rápido que um prompt de 100 com resposta de 2.000 ([[05-Memoria-e-Performance/Inferencia-livro]]).

## 5. Como contar e controlar

- **Conte antes de mandar.** O Ollama devolve `prompt_eval_count` e `eval_count` em cada resposta da API [1]; o script RAG do vault imprime esses valores no rodapé ([[07-Implementacao-Casa/RAG-local-executavel.py]]).
- **Dimensione `num_ctx` = maior entrada esperada + maior saída esperada + folga.** Para RAG, some system prompt, k chunks × tamanho do chunk e a pergunta.
- **Controle a saída** com `num_predict` (Ollama) ou equivalente, e prefira instruções claras de tamanho no prompt.
- **Cuidado com o histórico.** Em conversas longas, o histórico é a parte que mais cresce; aplicações sérias resumem ou cortam turnos antigos de forma explícita.
- **Para documentos, use RAG, não contexto gigante.** Colar um PDF inteiro no prompt gasta KV cache, TTFT e memória; recuperar só os trechos certos é mais barato e mais preciso ([[07-Implementacao-Casa/RAG-livro]]).

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://docs.ollama.com/faq "Ollama — FAQ: contexto padrão de 4096 tokens, num_ctx e OLLAMA_CONTEXT_LENGTH"
[2]: https://github.com/ollama/ollama/blob/main/docs/api.md "Ollama — API REST: campos prompt_eval_count, eval_count, num_predict e options"
[3]: https://huggingface.co/learn/llm-course/chapter2/4 "Hugging Face LLM Course — tokenizers"
[4]: https://github.com/ggml-org/llama.cpp "llama.cpp — parâmetro de contexto (-c) e KV cache"
