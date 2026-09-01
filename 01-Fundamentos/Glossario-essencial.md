# Glossário essencial

> **Como usar.** Cada termo tem uma definição de uma frase, uma analogia para quem nunca usou IA local, o motivo pelo qual ele importa na prática e a nota do vault que aprofunda. As analogias são recursos didáticos, não definições técnicas; em caso de conflito, vale a nota de destino.

## Modelo e números

| Termo | Em uma frase | Analogia | Por que importa | Aprofundar |
|---|---|---|---|---|
| **Parâmetro** | Um número aprendido no treinamento; o modelo é o conjunto de todos eles. | Cada "botão" de um painel com bilhões de botões, já ajustados de fábrica. | Define quanta memória o modelo ocupa e quanto custa cada token gerado. | [[01-Fundamentos/Parametros-e-tokens]] |
| **Peso** | Sinônimo prático de parâmetro; "os pesos" = o arquivo do modelo. | O painel inteiro, empacotado em um arquivo. | "Carregar os pesos" é o primeiro passo de qualquer uso. | [[01-Fundamentos/Carregar-um-peso]] |
| **B / M (7B, 200M)** | Bilhões / milhões de parâmetros. | 7B = 7.000.000.000 botões. | Primeira triagem de "cabe na minha máquina?". | [[03-Hardware/Calculadora-de-memoria]] |
| **Dense (denso)** | Modelo em que todos os parâmetros trabalham em cada token. | Todos os funcionários atendem cada cliente. | Memória e velocidade escalam juntas com o tamanho. | [[01-Fundamentos/Arquiteturas]] |
| **MoE (Mixture of Experts)** | Modelo em que só uma parte dos parâmetros ("experts") trabalha em cada token, mas todos precisam estar na memória. | Um hospital com muitos especialistas: cada paciente vê poucos, mas todos precisam estar no prédio. | Dimensione memória pelos parâmetros **totais** e velocidade pelos **ativos**. | [[01-Fundamentos/Parametros-e-tokens]] |
| **Quantização** | Guardar cada parâmetro com menos bits (4 em vez de 16) para caber em menos memória. | Salvar a foto em JPEG em vez de RAW: menor, quase igual. | É o que permite rodar um 27B em uma GPU de 24 GB. | [[05-Memoria-e-Performance/Quantizacao-livro]] |
| **Q4_K_M, Q8, FP16** | Nomes de formatos de quantização (4, 8 e 16 bits por parâmetro, com variações). | Níveis de compressão do JPEG. | Q4 é o padrão doméstico; Q8 e FP16 são maiores e mais fiéis. | [[05-Memoria-e-Performance/Quantizacoes-praticas]] |
| **GGUF** | Formato de arquivo do ecossistema llama.cpp/Ollama: metadados e tensores em um único arquivo, com suporte a mmap [2]. | O ".zip" padronizado do modelo. | É o arquivo que você baixa e carrega em casa. | [[04-Software/Runtimes]] |
| **Model card** | A "etiqueta" oficial do modelo: parâmetros, contexto, licença, formato. | Bula do remédio. | Única fonte confiável dos números; blogs são contexto. | [[02-Modelos/Como-ler-um-model-card]] |

## Texto, entrada e saída

| Termo | Em uma frase | Analogia | Por que importa | Aprofundar |
|---|---|---|---|---|
| **Token** | A unidade em que o modelo lê e escreve; normalmente um pedaço de palavra [3]. | Sílabas de um idioma que só o modelo fala. | Contexto, velocidade e custo são medidos em tokens, não em palavras. | [[01-Fundamentos/Parametros-e-tokens]] |
| **Tokenizer** | O programa que converte texto em tokens e de volta. | Tradutor entre seu texto e o idioma do modelo. | Cada modelo tem o seu; o mesmo texto vira contagens diferentes. | [[01-Fundamentos/Entrada-e-saida]] |
| **Entrada (prompt)** | Tudo o que o modelo recebe antes de responder: sua pergunta, instruções de sistema, histórico e documentos anexados. | A pasta que você entrega a um consultor antes da reunião. | Quanto maior, mais tempo até a primeira palavra e mais memória de contexto. | [[01-Fundamentos/Entrada-e-saida]] |
| **Saída (geração)** | O texto que o modelo produz, um token por vez. | O consultor ditando a resposta palavra por palavra. | É a parte lenta; a velocidade é limitada pela memória, não só pelo processador. | [[01-Fundamentos/Entrada-e-saida]] |
| **Contexto (janela de contexto)** | O máximo de tokens que cabem em uma conversa, somando entrada e saída. | A mesa do consultor: só cabe certo número de páginas. | Estourou, o modelo esquece o começo ou devolve resposta vazia/cortada. | [[01-Fundamentos/Entrada-e-saida]] |
| **num_ctx** | O parâmetro do Ollama que define o tamanho da janela pedida ao runtime (padrão 4096) [1]. | O tamanho da mesa que você escolhe. | Mais contexto = mais VRAM para o KV cache. | [[07-Implementacao-Casa/03-RAG-deploy]] |
| **System prompt** | Instruções fixas que entram antes da conversa. | O briefing que o consultor recebe antes de você chegar. | Consome tokens de contexto em toda mensagem. | [[07-Implementacao-Casa/Agentes-e-tool-calling]] |
| **Thinking / raciocínio** | Modo em que o modelo escreve um rascunho interno antes da resposta final. | O consultor pensando em voz alta. | Consome tokens de saída e de contexto; foi a causa de respostas vazias no RAG do vault. | [[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]] |

## Execução

| Termo | Em uma frase | Analogia | Por que importa | Aprofundar |
|---|---|---|---|---|
| **Inferência** | Usar o modelo treinado para produzir uma saída (não é treinar). | Consultar o especialista, não formá-lo. | É o que uma IA local doméstica faz o tempo todo. | [[05-Memoria-e-Performance/Inferencia-livro]] |
| **Carregar** | Ler o arquivo do SSD e colocar os pesos na VRAM/RAM, prontos para uso. | Abrir o programa e esperar a tela inicial. | Leva segundos e define onde (GPU ou RAM) cada parte vai rodar. | [[01-Fundamentos/Carregar-um-peso]] |
| **Runtime** | O programa que carrega e executa o modelo (Ollama, llama.cpp, vLLM). | O tocador de música; o modelo é a música. | Escolhe o hardware, o formato e a API. | [[04-Software/Runtimes]] |
| **Prefill** | Fase em que o modelo lê a entrada inteira de uma vez. | Ler a pasta antes de responder. | Define o tempo até a primeira palavra (TTFT). | [[01-Fundamentos/LLM-e-inferencia]] |
| **Decode** | Fase em que o modelo gera um token por vez. | Ditar a resposta. | Define os tokens por segundo; limitada pela banda de memória. | [[01-Fundamentos/LLM-e-inferencia]] |
| **KV cache** | Memória de trabalho da conversa; cresce com o número de tokens no contexto. | Anotações que o consultor mantém para não reler a pasta a cada frase. | Em contexto longo pode ocupar mais memória que os próprios pesos. | [[05-Memoria-e-Performance/KV-cache-formula-e-exemplos]] |
| **TTFT** | Time to first token: tempo até a primeira palavra aparecer. | O silêncio antes da resposta. | Percepção de "travou". | [[05-Memoria-e-Performance/Benchmarking]] |
| **tokens/s** | Quantos tokens o modelo gera por segundo. | Velocidade de digitação. | Abaixo de ~10 tokens/s a leitura fica desconfortável (opinião editorial). | [[05-Memoria-e-Performance/Benchmarking]] |
| **Offload** | Deixar parte das camadas do modelo na RAM, processadas pela CPU, quando não cabe tudo na VRAM. | Guardar parte dos arquivos em outra sala e ir buscar. | Permite rodar modelos maiores, muito mais devagar. | [[01-Fundamentos/Carregar-um-peso]] |
| **Embedding** | Um vetor de números que representa o significado de um texto; usado para busca em documentos (RAG). | Coordenadas GPS do sentido de uma frase. | É o que permite "perguntar aos meus PDFs". | [[07-Implementacao-Casa/Embeddings-e-vector-search]] |
| **RAG** | Buscar trechos relevantes nos seus documentos e entregá-los ao modelo no prompt. | Entregar ao consultor só as páginas certas. | Forma segura de dar dados próprios ao modelo sem treiná-lo. | [[07-Implementacao-Casa/RAG-livro]] |

## Hardware

| Termo | Em uma frase | Analogia | Por que importa | Aprofundar |
|---|---|---|---|---|
| **VRAM** | Memória da placa de vídeo; rápida e dedicada. | A mesa de trabalho ao lado do especialista. | Decide qual modelo roda **bem**. | [[03-Hardware/Por-que-VRAM-RAM-e-CPU-importam]] |
| **RAM** | Memória do sistema; maior, mais lenta que a VRAM. | O armário na mesma sala. | Recebe o que não coube na VRAM e sustenta o resto (RAG, sistema). | [[03-Hardware/Por-que-VRAM-RAM-e-CPU-importam]] |
| **Largura de banda** | Quantos GB por segundo a memória entrega ao processador. | Largura do corredor entre a mesa e o especialista. | Em decode, é o teto dos tokens/s: cada token lê os pesos inteiros. | [[03-Hardware/Comparativo-workstations-vs-GPU]] |
| **GPU** | Processador paralelo com VRAM própria; o caminho mais simples para LLM local. | Uma equipe enorme fazendo contas simples ao mesmo tempo. | Velocidade, desde que o modelo caiba na VRAM. | [[03-Hardware/GPU-vs-CPU-vs-NPU]] |
| **CPU** | Processador geral; roda modelos pequenos, tokenização, embeddings e a parte que não coube na GPU. | Poucos funcionários muito versáteis. | Fallback e trabalho auxiliar; limitada pela banda da RAM. | [[03-Hardware/GPU-vs-CPU-vs-NPU]] |
| **Memória unificada** | Arquitetura (Apple Silicon, GB10, APUs) em que CPU e GPU usam a mesma memória. | Uma sala só, sem corredor. | Permite modelos grandes com uma banda menor que a de uma GPU discreta. | [[03-Hardware/ARM-e-memoria-unificada]] |
| **OOM (out of memory)** | Erro por falta de memória (VRAM ou RAM). | A mesa transbordou. | Sintoma clássico de contexto grande ou modelo grande demais. | [[05-Memoria-e-Performance/Inferencia-livro]] |

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://docs.ollama.com/faq "Ollama — FAQ: num_ctx / OLLAMA_CONTEXT_LENGTH (padrão 4096), keep_alive e `ollama ps`"
[2]: https://github.com/ggml-org/ggml/blob/master/docs/gguf.md "GGUF — especificação do formato (arquivo único, metadados chave-valor, tensores, mmap)"
[3]: https://huggingface.co/learn/llm-course/chapter2/4 "Hugging Face LLM Course — tokenizers"
[4]: https://arxiv.org/abs/1706.03762 "Attention Is All You Need — arquitetura Transformer"
