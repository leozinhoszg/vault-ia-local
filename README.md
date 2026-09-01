# Vault: IA Local

Este vault é uma base de conhecimento em português brasileiro para **entender, escolher, instalar, operar e governar IA local** em casa ou em uma empresa. Ele cobre LLMs e VLMs, hardware x86/ARM, GPU/CPU/NPU, memória e banda, quantização incluindo FP4, runtimes, RAG, agentes, treinamento e fine-tuning, custos e operação segura.

> **Data de referência:** 1º de setembro de 2026. Modelos, preços, drivers e compatibilidades mudam rapidamente. Trate números de custo como faixas de planejamento, não como cotação.

## Como usar

Comece em [[00-Inicio/MAPA]] e siga o roteiro adequado. Use a nota [[03-Hardware/Calculadora-de-memoria]] antes de escolher um modelo. Para uma primeira instalação, consulte [[07-Implementacao-Casa/01-LLM-local-com-Ollama]]; para uma API multiusuário, consulte [[08-Implementacao-Empresa/01-Arquitetura-de-referencia]] e [[08-Implementacao-Empresa/02-Deploy-com-vLLM]].

Cada nota possui links internos com o caminho da pasta e da nota, referências externas numeradas e uma seção **Referências**. Os valores aproximados são separados dos fatos publicados. A licença de cada modelo deve ser checada antes de uso comercial.

## Índice por objetivo

| Objetivo | Notas principais |
|---|---|
| Escolher hardware | [[03-Hardware/Matriz-de-hardware]], [[03-Hardware/GPU-vs-CPU-vs-NPU]], [[03-Hardware/ARM-e-memoria-unificada]] |
| Entender memória | [[05-Memoria-e-Performance/Modelo-de-memoria]], [[03-Hardware/Calculadora-de-memoria]] |
| Rodar um modelo | [[07-Implementacao-Casa/01-LLM-local-com-Ollama]], [[04-Software/Runtimes]] |
| Criar busca sobre documentos | [[07-Implementacao-Casa/02-RAG-local]] |
| Fazer fine-tuning | [[06-Treinamento-e-Fine-tuning/01-QLoRA-pratico]], [[06-Treinamento-e-Fine-tuning/02-Pipeline-de-dados]] |
| Produção empresarial | [[08-Implementacao-Empresa/01-Arquitetura-de-referencia]], [[08-Implementacao-Empresa/03-Seguranca-e-governanca]] |
| Custear o projeto | [[09-Servicos-e-Custos/Modelo-de-custo]], [[09-Servicos-e-Custos/Cenarios-de-infraestrutura]] |
