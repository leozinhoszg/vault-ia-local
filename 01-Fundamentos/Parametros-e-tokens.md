# Parâmetros e tokens — o que os números do modelo significam

> **Pergunta que esta nota responde.** Quando um modelo diz "200 milhões de parâmetros" ou "24 bilhões de parâmetros", o que isso significa para quem quer rodar em casa? E o que parâmetro tem a ver com token?

## 1. O que é um parâmetro

Um parâmetro é **um número** dentro do modelo, ajustado durante o treinamento. O modelo inteiro é o conjunto desses números, organizados em matrizes; o arquivo que você baixa é esse conjunto gravado em disco (os "pesos"). "Rodar o modelo" é multiplicar seu texto, convertido em números, por essas matrizes, camada por camada, até sair a previsão do próximo token ([[01-Fundamentos/LLM-e-inferencia]]).

Nada é "consultado" em um banco de dados: o conhecimento está distribuído nos valores dos parâmetros. Por isso o modelo não sabe o que aconteceu depois do treino e por isso RAG existe ([[07-Implementacao-Casa/RAG-livro]]).

## 2. O que o número de parâmetros te diz antes de qualquer teste

Três coisas, nesta ordem de confiabilidade:

1. **Quanta memória os pesos ocupam.** É aritmética: `parâmetros × bytes por parâmetro` ([[03-Hardware/Calculadora-de-memoria]]).
2. **Quanto custa gerar cada token.** No decode, a cada token o runtime lê os pesos ativos inteiros; mais parâmetros = mais bytes lidos por token = menos tokens por segundo na mesma máquina ([[05-Memoria-e-Performance/Modelo-de-memoria]]).
3. **A classe de capacidade.** Grosseiramente, modelos maiores raciocinam melhor e sabem mais. É a menos confiável das três: treino, dados e arquitetura mudam muito o resultado, e só benchmark decide ([[02-Modelos/Tabela-normalizada-de-benchmarks]]).

## 3. Exemplo: 200 milhões versus 24 bilhões

Pisos teóricos pela tabela de bytes por parâmetro da [[03-Hardware/Calculadora-de-memoria]]; o arquivo real fica 5–20% acima por causa de escalas e metadados.

| | 200 milhões (200M, 0,2B) | 24 bilhões (24B) |
|---|---:|---:|
| FP16/BF16 (2 bytes) | ~0,4 GB | ~48 GB |
| INT8/Q8 (1 byte) | ~0,2 GB | ~24 GB |
| INT4/Q4 (0,5 byte, piso) | ~0,1 GB | ~12 GB (arquivo real ~13–15 GB) |
| Onde roda | Em qualquer CPU, quase sem custo | GPU de 16 GB em Q4 com contexto curto; em GPU de 8 GB só com parte na RAM, lento ([[03-Hardware/Sizing-9B-14B-27B-70B]]) |
| Classe típica | Embeddings, rerankers, classificadores — as peças auxiliares de um pipeline RAG (o `all-MiniLM-L6-v2` usado no RAG do vault é ainda menor) | LLM gerador de porte médio para chat e código |
| Diferença | 120× em parâmetros → ~120× em memória de pesos e, no decode, algo próximo disso em bytes lidos por token | |

Um modelo de 200M responde em milissegundos porque cabe em qualquer lugar e lê pouca memória por token; um de 24B "mede tokens por segundo" porque cada token exige ler 12 GB ou mais.

## 4. Totais versus ativos: a distinção que mais engana

| Tipo | O que "24B" significa | Memória | Velocidade |
|---|---|---|---|
| **Denso** | Todos os 24B trabalham em cada token. | Pelos 24B. | Pelos 24B. |
| **MoE** (ex.: "33B totais / 3B ativos") | Só ~3B trabalham em cada token, escolhidos por um roteador; os outros ficam esperando — **na memória**. | Pelos **33B totais**. | Pelos **3B ativos**. |

Exemplo do vault: o [[02-Modelos/Fichas/Laguna-XS-2.1]] tem 33B/3B; é rápido como um modelo de 3B, mas exige ~20 GB de arquivo em Q4 porque os 33B precisam residir em memória. Dimensionar um MoE pelos ativos é o erro mais comum de planejamento ([[03-Hardware/Sizing-9B-14B-27B-70B]], [[02-Modelos/Verificacao-PromptQuorum]]).

## 5. O que é um token

Um token é a unidade em que o modelo lê e escreve. O **tokenizer** quebra o texto em pedaços de um vocabulário fixo (dezenas ou centenas de milhares de pedaços) e cada pedaço vira um número; na saída, o processo inverso remonta o texto [1]. Um token costuma ser uma palavra curta, um pedaço de palavra, um sinal de pontuação ou um espaço com a palavra seguinte.

Regras de bolso (estimativa editorial; a contagem real depende do tokenizer de cada modelo):

- Em inglês, ~4 caracteres ou ~0,75 palavra por token.
- Em português, a contagem tende a ser um pouco pior, porque palavras acentuadas e terminações longas se dividem em mais pedaços. Conte com **1,3–2 tokens por palavra** e confira com o tokenizer real.
- Código e JSON gastam mais tokens por caractere que prosa.

Tudo no mundo dos LLMs é medido em tokens: janela de contexto, velocidade (tokens/s), custo de API, tamanho do KV cache. Nunca em palavras ou caracteres.

## 6. O que parâmetro tem a ver com token — e o que não tem

| Relação | Vale? | Onde está no vault |
|---|---|---|
| Parâmetros **ativos** são contados "por token": é a quantidade de pesos que trabalha para produzir cada token. | Sim | [[01-Fundamentos/LLM-e-inferencia]], fichas de MoE |
| Mais parâmetros ativos → mais bytes lidos por token → menos tokens/s. | Sim | [[03-Hardware/Comparativo-workstations-vs-GPU]] (`tok/s_teto ≈ banda ÷ GB por token`) |
| Parâmetros de **runtime** como `num_ctx` são medidos em tokens. | Sim, mas é outro sentido da palavra "parâmetro": é uma opção de configuração, não um peso do modelo. | [[01-Fundamentos/Entrada-e-saida]] |
| O KV cache cresce com o número de parâmetros. | **Não.** Cresce com o número de tokens no contexto, camadas, cabeças KV e dimensão da atenção. Dois modelos com o mesmo número de parâmetros podem ter KV cache muito diferente. | [[05-Memoria-e-Performance/KV-cache-formula-e-exemplos]] |
| Modelo maior aceita contexto maior. | **Não** por si só. O contexto é uma propriedade do treino e da arquitetura, informada no model card. | [[02-Modelos/Como-ler-um-model-card]] |

## 7. Quatro ressalvas antes de confiar no número

1. **Parâmetros não são o tamanho do arquivo.** Depende dos bits por parâmetro; a quantização acrescenta escalas e metadados, então `N × bits` é só o piso.
2. **Pesos não são a memória total.** Some o KV cache (que cresce com tokens), ativações e o runtime. Um 24B em Q4 "carrega" em 16 GB e pode falhar ao rodar com contexto grande ([[01-Fundamentos/Carregar-um-peso]]).
3. **A contagem publicada pode estar inflada.** O Hugging Face conta tensores automaticamente e pode incluir escalas de quantização — caso do "41B" exibido para a variante INT4 do Laguna, cujo card diz 33B ([[02-Modelos/Fichas/Laguna-XS-2.1]]). Use o model card.
4. **Denso ou MoE muda tudo.** Sem essa informação, "24B" não permite dimensionar nem memória nem velocidade.

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://huggingface.co/learn/llm-course/chapter2/4 "Hugging Face LLM Course — tokenizers: tokenização por palavra, caractere e subpalavra"
[2]: https://github.com/ggml-org/llama.cpp "llama.cpp — formatos GGUF e tamanhos de quantização"
[3]: https://ai.meta.com/blog/llama-4-multimodal-intelligence/ "Meta — Llama 4: exemplo de família MoE com parâmetros totais e ativos"
[4]: https://arxiv.org/abs/1706.03762 "Attention Is All You Need — arquitetura Transformer"
