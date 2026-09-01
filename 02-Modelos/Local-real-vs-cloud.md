# Local real versus cloud — modos de execução

> **Data de verificação:** 2026-09-01. **Estado:** ativo. **Dono:** Luiz Guimarães. **Próxima revisão:** 2026-10-01.

"Rodar localmente" virou uma expressão ambígua. Um artigo pode listar um modelo de 1T parâmetros como "LLM local" porque existe um comando `ollama run` para ele, quando na verdade o comando envia o prompt para a nuvem do Ollama. Esta nota fixa quatro modos de execução e exige que toda ficha, catálogo e recomendação declare qual deles está em jogo.

## Os quatro modos

| Modo | O que acontece com os pesos | O que acontece com o prompt | Como reconhecer | Quando faz sentido |
|---|---|---|---|---|
| **1. Local real** | Arquivo baixado e carregado inteiramente no acelerador (GPU/NPU/memória unificada) | Nunca sai da máquina | `ollama ls` mostra tamanho em GB; `ollama ps` mostra 100% GPU; llama.cpp com `-ngl` cobrindo todas as camadas; nenhuma conta ou token externo | Dados sensíveis, latência estável, custo marginal zero por token |
| **2. Offload CPU/RAM (híbrido)** | Parte dos pesos fica na VRAM, o restante na RAM do sistema (ou até em disco/swap) | Nunca sai da máquina | `ollama ps` mostra divisão CPU/GPU; llama.cpp com `-ngl` parcial; velocidade cai fortemente — a RAM tem banda muito menor que VRAM/HBM ([[03-Hardware/Sizing-9B-14B-27B-70B]]) | Rodar um modelo que não cabe na VRAM, aceitando tokens/s baixos; o guia de deploy do Kimi K2.7 Code documenta 2× RTX 4090 + 1,97 TB de RAM como caso extremo [4] |
| **3. Serviço remoto por ferramenta local** | Ficam no provedor (OpenRouter, API do fabricante, poolside API etc.) | Sai da máquina pelo cliente (Continue, Aider, Claude Code, curl) | URL do endpoint não é `localhost`; exige API key; fatura por token | Modelos grandes demais para o hardware; avaliação rápida antes de comprar hardware; sempre com revisão de contrato e LGPD ([[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]]) |
| **4. Ollama Cloud** | Ficam nos servidores do Ollama | Sai da máquina — o cliente é local (`localhost:11434`), mas o modelo `:cloud` é "automaticamente offloaded para o serviço cloud do Ollama" [1] | Tag `:cloud` (ou sufixo `-cloud`); exige `ollama signin`; a página do modelo lista preço por milhão de tokens; nenhum arquivo de vários GB é baixado | Testar um modelo de 1T sem hardware; não confundir com o modo 1 em nenhum documento de arquitetura ou compra |

O modo 4 é o mais traiçoeiro porque a experiência de linha de comando é idêntica à do modo 1. Na leitura de 2026-09-01, `ollama run kimi-k2.6:cloud` e `ollama run kimi-k2.7-code:cloud` são as únicas tags disponíveis para esses modelos na biblioteca oficial, enquanto `ollama run laguna-xs-2.1` baixa um Q4_K_M de 20 GB e executa no modo 1 ou 2 [2][3].

## O que o Ollama documenta sobre a nuvem

- Infraestrutura "primarily in the United States", com possibilidade de roteamento para Europa e Singapura para capacidade adicional [5].
- Política declarada: "Prompt or response data is never logged or trained on"; para provedores parceiros, exigência de no logging, no training e zero data retention [5]. Isso é uma declaração do fornecedor, não uma evidência auditada; para dados pessoais ou segredo industrial, trate como serviço externo e aplique o mesmo checklist de qualquer API.
- Concorrência por plano na leitura: Free 1 requisição simultânea, Pro 3, Max e Team 10 [5].
- **Modo somente local**: `{"disable_ollama_cloud": true}` em `~/.ollama/server.json` ou variável `OLLAMA_NO_CLOUD=1`; o log passa a mostrar `Ollama cloud disabled: true`. Desativar remove o acesso a modelos cloud e à busca web [6].

Em ambiente empresarial, ative o modo somente local por padrão nas estações e nos servidores de inferência, e registre a decisão no runbook ([[10-Operacao-e-Seguranca/Runbook]]).

## Regra editorial do vault

1. Toda ficha em `02-Modelos/Fichas/` declara **Modo de execução** (1 a 4) e **Arquivo quantizado real** com nome, tamanho em GB, runtime e versão mínima. "Cabe em 22 GB" sem arquivo, runtime e contexto não é registro válido.
2. Um comando `ollama run` só prova modo 1 ou 2 se a tag correspondente existir sem `:cloud` e o tamanho do download for compatível com os parâmetros totais.
3. Modelos com centenas de bilhões de parâmetros totais entram no catálogo como modo 2 (offload extremo), 3 ou 4 — nunca como modo 1 doméstico — até que alguém publique arquivo, hardware e tokens/s medidos.
4. Para comparar custo, o modo 3 e o modo 4 entram na planilha como API ([[09-Servicos-e-Custos/Guia-financeiro-TCO-local-vs-OpenAI]]); só os modos 1 e 2 entram como TCO local.

## Comandos de conferência

```bash
# Tamanho em disco: modelo cloud não ocupa GB
ollama ls
# Divisão de processamento: 100% GPU = modo 1; CPU/GPU = modo 2
ollama ps
# Modo somente local
OLLAMA_NO_CLOUD=1 ollama serve
# llama.cpp: todas as camadas no acelerador (modo 1) ou parcial (modo 2)
llama-server -m modelo.gguf -ngl 99 -c 32768
```

## Referências

[1]: https://docs.ollama.com/cloud "Ollama — Cloud models (offload automático para o serviço cloud, ollama signin)"
[2]: https://ollama.com/library/kimi-k2.6 "Ollama — kimi-k2.6 (única tag: :cloud)"
[3]: https://ollama.com/library/laguna-xs-2.1 "Ollama — laguna-xs-2.1 (tags locais com tamanho em GB)"
[4]: https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/docs/deploy_guidance.md "Moonshot AI — deploy do Kimi K2.7 Code, incluindo cenário KTransformers com RAM de servidor"
[5]: https://ollama.com/cloud "Ollama — Cloud (região, política de dados, limites por plano, preços)"
[6]: https://docs.ollama.com/faq "Ollama — FAQ (disable_ollama_cloud, OLLAMA_NO_CLOUD)"
