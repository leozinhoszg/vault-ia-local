# Mapa do vault

<!-- validador: sem-referencias: nota de navegação; as fontes ficam nas notas de destino e em 11-Referencias -->

## Sequência recomendada

0. Nunca rodou IA local? Comece em [[01-Fundamentos/00-Comece-aqui]] e no [[01-Fundamentos/Glossario-essencial]].
1. Defina o caso de uso, a sensibilidade dos dados, a latência e o número de usuários em [[08-Implementacao-Empresa/00-Definicao-de-requisitos]].
2. Escolha a classe de modelo em [[02-Modelos/Catalogo-de-modelos]] e valide a licença.
3. Estime pesos, KV cache e folga em [[03-Hardware/Calculadora-de-memoria]].
4. Selecione o runtime em [[04-Software/Runtimes]].
5. Instale e faça benchmark seguindo [[05-Memoria-e-Performance/Benchmarking]].
6. Adicione RAG, ferramentas e observabilidade apenas depois de validar a resposta básica.
7. Para treinamento, prefira primeiro prompt engineering, RAG e fine-tuning de adaptador; pré-treinamento do zero é outro projeto.

## Princípios

> **Local não é sinônimo de seguro.** Uma implantação local reduz dependência de terceiros e pode manter dados dentro do perímetro, mas ainda exige controle de acesso, logs, atualizações, proteção contra prompt injection e governança.

> **Memória limita antes da computação.** Em inferência autoregressiva, os pesos precisam caber e o KV cache cresce com contexto e concorrência. Mais TOPS, isoladamente, não garante melhor experiência.

## Notas essenciais

| Área | Nota |
|---|---|
| Fundamentos | [[01-Fundamentos/00-Comece-aqui]], [[01-Fundamentos/Glossario-essencial]], [[01-Fundamentos/Parametros-e-tokens]], [[01-Fundamentos/Entrada-e-saida]], [[01-Fundamentos/Carregar-um-peso]], [[00-Inicio/Livro-IA-Local]], [[01-Fundamentos/LLM-e-inferencia]], [[01-Fundamentos/Regressao-ML]], [[01-Fundamentos/Arquiteturas]] |
| Modelos | [[02-Modelos/Catalogo-de-modelos]], [[02-Modelos/Ficha-padronizada-por-modelo]], [[02-Modelos/Fichas/Qwen3.6-27B]], [[02-Modelos/Fichas/Kimi-K2.6]], [[02-Modelos/Fichas/Kimi-K2.7-Code]], [[02-Modelos/Fichas/Laguna-XS-2.1]], [[02-Modelos/Fichas/Qwen3-Coder-30B]], [[02-Modelos/Local-real-vs-cloud]], [[02-Modelos/Tabela-normalizada-de-benchmarks]], [[02-Modelos/LLMs-locais-para-coding-Atomic]], [[02-Modelos/Verificacao-PromptQuorum]], [[02-Modelos/Como-ler-um-model-card]] |
| Hardware | [[03-Hardware/Por-que-VRAM-RAM-e-CPU-importam]], [[03-Hardware/Matriz-de-hardware]], [[03-Hardware/Catalogo-NVIDIA-IA-local]], [[03-Hardware/Referencias-de-desempenho-GPU]], [[03-Hardware/Builds-brasileiros-por-orcamento]], [[03-Hardware/BOM-brasileira-datada]], [[03-Hardware/Sizing-9B-14B-27B-70B]], [[03-Hardware/GPU-vs-CPU-vs-NPU]], [[03-Hardware/APU-e-TPU]], [[03-Hardware/Mac-Studio-e-IA-local]], [[03-Hardware/Comparativo-workstations-vs-GPU]], [[03-Hardware/Workstations/Dell-Pro-Max-GB10]], [[99-Templates/Modelo-de-ficha-de-workstation]] |
| Precisão | [[05-Memoria-e-Performance/Quantizacao-e-FP4]], [[05-Memoria-e-Performance/Quantizacao-livro]], [[05-Memoria-e-Performance/Quantizacoes-praticas]], [[05-Memoria-e-Performance/Inferencia-livro]], [[05-Memoria-e-Performance/KV-cache-formula-e-exemplos]], [[05-Memoria-e-Performance/Evaliacao-e-regressao-de-modelos]] |
| Compatibilidade | [[04-Software/Compatibilidade-por-stack]], [[04-Software/Cookbooks-multiplataforma]], [[04-Software/Estado-de-testes-cookbooks]], [[08-Implementacao-Empresa/03-Paralelismo-e-multi-GPU]] |
| Financeiro | [[09-Servicos-e-Custos/Guia-financeiro-TCO-local-vs-OpenAI]], [[09-Servicos-e-Custos/Modelo-de-custo]], [[03-Hardware/BOM-brasileira-datada]], [Planilha TCO](../09-Servicos-e-Custos/TCO-local-vs-OpenAI.xlsx) |
| Implementação | [[07-Implementacao-Casa/01-LLM-local-com-Ollama]], [[07-Implementacao-Casa/Embeddings-e-vector-search]], [[07-Implementacao-Casa/RAG-livro]], [[07-Implementacao-Casa/Agentes-e-tool-calling]], [[07-Implementacao-Casa/AI-assisted-coding-tools]], [[06-Treinamento-e-Fine-tuning/Fine-tuning-livro]], [[06-Treinamento-e-Fine-tuning/02-Fine-tuning-completo]], [[08-Implementacao-Empresa/01-Arquitetura-de-referencia]], [[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]] |

## Auditoria e operação

- [[00-Inicio/Auditoria-P0]]
- [[00-Inicio/Sessoes/2026-09-01-sessao-re-auditoria-P0]]

## Operação e manutenção

- [[00-Inicio/Governanca-editorial-do-vault]]
- [[10-Operacao-e-Seguranca/NIST-AI-RMF-GenAI]]
- [[10-Operacao-e-Seguranca/Runbook]]
- [[04-Software/Estado-de-testes-cookbooks]]
- [[99-Templates/validate_vault_completo.py]]
- [[99-Templates/gerar_indice_urls.py]]
- [[99-Templates/check_tco.py]]
- [[99-Templates/recalcular_tco.ps1]]
- [[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]]

## Fontes e reprodução

- [[11-Referencias/Fontes-principais]]
- [[11-Referencias/Indice-de-fontes-urls]]
- [[07-Implementacao-Casa/requirements-rag.txt]]
- [[07-Implementacao-Casa/requirements-rag.lock.txt]]
