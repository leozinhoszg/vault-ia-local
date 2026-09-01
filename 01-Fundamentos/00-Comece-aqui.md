# Comece aqui — IA local para quem nunca usou

> **Para quem é esta nota.** Para quem nunca rodou um modelo de linguagem no próprio computador e quer entender, sem jargão, o que acontece quando digita uma pergunta e aperta Enter. As notas técnicas do vault continuam sendo a fonte de detalhe; esta é a porta de entrada.

## O que você tem nas mãos

Uma "IA local" é composta por três coisas:

| Peça | O que é | Exemplo |
|---|---|---|
| **Modelo** | Um arquivo grande cheio de números (os **pesos**). Não é um programa; sozinho não faz nada. | `qwen3.5:4b`, um arquivo de 3,4 GB |
| **Runtime** | O programa que lê o arquivo, recebe seu texto e produz a resposta. | Ollama, llama.cpp, LM Studio |
| **Máquina** | Onde os números ficam guardados enquanto trabalham (VRAM da GPU, RAM) e quem faz as contas (GPU, CPU). | Notebook com RTX 4060 de 8 GB |

Você escreve um texto (a **entrada**), o runtime devolve outro texto (a **saída**), pedacinho por pedacinho. Cada pedacinho é um **token**. É só isso — o resto desta nota explica o que acontece entre a entrada e a saída, e por que a máquina importa.

## O que acontece quando você aperta Enter

Exemplo real do vault: `ollama run qwen3.5:4b` em um notebook com GPU de 8 GB ([[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]]).

| Passo | O que acontece | Quem trabalha | Ordem de grandeza |
|---:|---|---|---|
| 0 | **Baixar** o modelo (uma vez só). O arquivo vai para o SSD. | Rede e SSD | Minutos, depende da conexão |
| 1 | **Carregar**: o runtime lê o arquivo do SSD, passa pela RAM e copia para a VRAM da GPU o que couber. Reserva espaço para a "memória de conversa" (KV cache). | SSD → RAM → VRAM | Segundos; na evidência, a primeira resposta levou 9,3 s **incluindo** a carga |
| 2 | **Tokenizar**: seu texto vira uma lista de números (tokens). | CPU | Milissegundos |
| 3 | **Prefill**: o modelo lê a entrada inteira de uma vez e monta o KV cache. | GPU (ou CPU, se o modelo não coube na VRAM) | Fração de segundo a alguns segundos; é o "tempo até a primeira palavra" (TTFT) |
| 4 | **Decode**: gera **um token por vez**; a cada token, lê os pesos inteiros da memória. | GPU e a **banda** da memória dela | Dezenas de tokens por segundo em GPU; poucos em CPU |
| 5 | **Detokenizar** e mostrar na tela. | CPU | Milissegundos |
| 6 | **Descarregar**: por padrão o Ollama mantém o modelo na memória por 5 minutos após o último uso e depois libera [1]. | — | A próxima pergunta dentro desse tempo pula o passo 1 (0,9 s na evidência, contra 9,3 s) |

Detalhe de cada passo: [[01-Fundamentos/Carregar-um-peso]] (passos 1 e 6, e em que momento se usa GPU ou RAM), [[01-Fundamentos/Entrada-e-saida]] (passos 2 a 5) e [[01-Fundamentos/LLM-e-inferencia]] (a mecânica).

## Cinco palavras que resolvem a maior parte da confusão

1. **Parâmetro** — cada número dentro do modelo. "4B" significa 4 bilhões deles. Mais parâmetros = mais memória e, em geral, mais capacidade. → [[01-Fundamentos/Parametros-e-tokens]]
2. **Token** — a unidade em que o modelo lê e escreve; um pedaço de palavra. Tudo se mede em tokens: contexto, velocidade, custo. → [[01-Fundamentos/Parametros-e-tokens]]
3. **Contexto** — quantos tokens (entrada + saída) o modelo consegue "segurar" em uma conversa. Estourou, ele esquece o começo ou falha. → [[01-Fundamentos/Entrada-e-saida]]
4. **VRAM** — a memória da GPU. É o recurso que decide **qual** modelo você consegue rodar bem. → [[03-Hardware/Por-que-VRAM-RAM-e-CPU-importam]]
5. **Quantização** — guardar cada parâmetro com menos bits para o modelo caber em menos memória, com pequena perda de qualidade. "Q4" é o formato mais comum em casa. → [[05-Memoria-e-Performance/Quantizacao-livro]]

O restante do vocabulário está em [[01-Fundamentos/Glossario-essencial]].

## Regra de bolso para a primeira instalação

Estimativas de planejamento, consolidadas de [[03-Hardware/Sizing-9B-14B-27B-70B]]; meça na sua máquina antes de decidir qualquer compra.

| Sua máquina | O que costuma rodar bem | Comece com |
|---|---|---|
| Sem GPU, 16 GB de RAM | Modelos de 1–8B em Q4, lentos a moderados | Um modelo de 4B |
| Sem GPU, 32 GB de RAM | 8–9B em Q4 com boa experiência; 14B com paciência | Um modelo de 8B |
| GPU de 8 GB + 32 GB de RAM | 4–9B em Q4 inteiramente na GPU (o vault testou `qwen3.5:4b`); 14B com parte na RAM, mais lento | Um modelo de 4–8B |
| GPU de 16 GB | 9–14B em Q4 com folga; 27B parcialmente na RAM | Um modelo de 14B |
| GPU de 24 GB | 27B em Q4 com pequena folga | Um modelo de 27B |

Passo a passo de instalação: [[07-Implementacao-Casa/01-LLM-local-com-Ollama]].

## Erros comuns de quem está começando

- **Escolher GPU pela velocidade, não pela memória.** Se o modelo não cabe na VRAM, a velocidade da GPU quase não importa. O vault registra o princípio como "memória limita antes da computação" ([[00-Inicio/MAPA]]).
- **Confundir "carregou" com "roda bem".** Um modelo pode abrir e travar na primeira resposta longa, quando o contexto cresce ([[03-Hardware/Sizing-9B-14B-27B-70B]]).
- **Acreditar que qualquer modelo do catálogo roda local.** Alguns nomes no Ollama existem apenas como `:cloud`, ou seja, rodam em servidor remoto ([[02-Modelos/Local-real-vs-cloud]]).
- **Comparar modelos só pelo número de parâmetros.** Um MoE de 33B com 3B ativos se comporta diferente de um denso de 33B ([[01-Fundamentos/Parametros-e-tokens]]).
- **Não medir.** Anote tempo até a primeira palavra, tokens por segundo e memória usada. Sem isso, toda troca de modelo ou hardware é chute ([[05-Memoria-e-Performance/Benchmarking]]).

## Trilha de leitura sugerida

1. Esta nota.
2. [[01-Fundamentos/Glossario-essencial]] — vocabulário mínimo.
3. [[01-Fundamentos/Parametros-e-tokens]] — o que os números do modelo significam.
4. [[01-Fundamentos/Entrada-e-saida]] — prompt, contexto e geração.
5. [[01-Fundamentos/Carregar-um-peso]] — o que acontece na memória e quando GPU, RAM e CPU trabalham.
6. [[03-Hardware/Por-que-VRAM-RAM-e-CPU-importam]] — o que cada peça compra e o que não compra.
7. [[07-Implementacao-Casa/01-LLM-local-com-Ollama]] — instale e rode.
8. Depois disso, siga a sequência do [[00-Inicio/MAPA]] e o [[00-Inicio/Livro-IA-Local]].

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://docs.ollama.com/faq "Ollama — FAQ: modelo permanece carregado 5 minutos por padrão (keep_alive), contexto padrão de 4096 tokens (num_ctx / OLLAMA_CONTEXT_LENGTH), `ollama ps` mostra GPU/CPU"
[2]: https://github.com/ggml-org/llama.cpp "llama.cpp — inferência em C/C++, GGUF, offload de camadas para GPU"
[3]: https://huggingface.co/learn/llm-course/chapter2/4 "Hugging Face LLM Course — tokenizers (palavra, caractere, subpalavra)"
