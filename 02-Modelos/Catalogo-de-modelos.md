# Catálogo de modelos atuais

Esta é uma shortlist para avaliação local em 2026. “Cabe” significa **estimativa dos pesos quantizados**, não garantia de velocidade ou qualidade. Baixe somente de repositórios oficiais ou mantenedores conhecidos e registre hash, licença e data. A coluna **Modo** usa a escala de [[02-Modelos/Local-real-vs-cloud]]: 1 local real, 2 offload CPU/RAM, 3 serviço remoto via ferramenta local, 4 Ollama Cloud. Quando houver arquivo quantizado oficial medido, ele aparece na coluna de perfil; "8/16/22 GB" sem arquivo é estimativa.

| Família / exemplo | Parâmetros publicados | Modalidade | Perfil local sugerido | Modo | Observação |
|---|---:|---|---|:---:|---|
| Laguna XS 2.1 | 33B total / 3B ativos, MoE | Código / agentes | GGUF oficial Q4_K_M = 20,3 GB; Ollama `latest` 20 GB, `q8_0` 36 GB; GPU de 24 GB ou Mac de 36 GB+ | 1 | OpenMDW-1.1; 262.144 de contexto; 70,9 SWE-bench Verified (média de 4 tentativas). Ficha: [[02-Modelos/Fichas/Laguna-XS-2.1]]. |
| Qwen3.8-27B | 27B dense | Texto + visão | 16–24 GB VRAM em quantização baixa; mais com contexto | 1 | Contexto nativo 262k, extensível conforme model card. |
| Qwen3.8-Flash-Next | 125B total / 6B ativos; + componentes publicados | Texto | Servidor multi-GPU ou memória unificada grande | 2–3 | MoE; ativos não eliminam a necessidade de armazenar pesos. |
| Qwen3.6-35B-A3B | 35B total / 3B ativos | Texto | 16–24 GB com quantização adequada | 1 | Bom candidato para experimentar MoE compacto. |
| Qwen3-Coder-Next | 80B total / 3B ativos | Código | Servidor ou workstation com muita RAM/VRAM | 2 | Prioriza agentes e coding; confirme licença e runtime. |
| Kimi K2.7 Code | 1T total / 32B ativos, MoE | Código + imagem/vídeo | Checkpoint INT4 nativo de 595 GB; GGUF 304–595 GB; H200 ×8 ou RAM de ~2 TB | 2 (servidor), 3 ou 4 | Modified MIT; 256K; Ollama só `kimi-k2.7-code:cloud`. Não é modelo doméstico. Ficha: [[02-Modelos/Fichas/Kimi-K2.7-Code]]. |
| Llama 4 Scout | 109B total / 17B ativos, 16 experts | Texto + visão | A Meta declara execução em um H100 com Int4 | 2–3 | Contexto anunciado de até 10M; contexto longo tem custo operacional. |
| Llama 4 Maverick | 400B total / 17B ativos, 128 experts | Texto + visão | Host H100/DGX ou distribuição | 3 | Grande footprint de pesos apesar de poucos ativos. |
| Llama 3.1 8B / 70B / 405B | 8B / 70B / 405B | Texto | 8B em máquina pessoal; maiores em servidor | 1 (8B) a 3 (405B) | 128K de contexto anunciado para a série. |
| Gemma 3 1B–27B | Varia por versão | Texto + visão em variantes | 8–24 GB conforme tamanho | 1 | Compactos e úteis para edge; confira licença. |
| DeepSeek-R1 e derivados | Varia; grandes versões MoE | Raciocínio | Quantizados ou multi-GPU | 2–3 | Raciocínio pode aumentar tokens gerados e custo. |
| Coding local — shortlist Atomic | Qwen3-Coder 30B, Qwen3-Coder-Next 80B, Laguna S 2.1 118B, Gemma 4 26B A4B, Qwen3.6 27B | Código / agentes | 24 GB para a classe 27–30B; 45–96 GB para modelos maiores | 1–2 | Ver análise de benchmarks, VRAM e velocidade em [[02-Modelos/LLMs-locais-para-coding-Atomic]]. |

Os números Qwen3.8 e Qwen3.6 acima são do model card oficial, enquanto os números de Llama 4 são da publicação da Meta. Laguna XS 2.1 e Kimi K2.7 Code vêm dos model cards oficiais e das páginas da biblioteca Ollama, capturados em 2026-09-01. Benchmarks com variante, harness e tentativas estão em [[02-Modelos/Tabela-normalizada-de-benchmarks]]. A shortlist de coding e os resultados de velocidade/VRAM foram adicionados a partir do guia da Atomic, com caráter editorial e dependência do hardware testado. A tabela deliberadamente não fixa preços: disponibilidade e câmbio mudam diariamente. Para escolher, faça uma matriz com qualidade no seu conjunto de testes, memória, latência, licença e custo total.

## Referências

[1]: https://huggingface.co/Qwen/Qwen3.8-27B "Qwen3.8-27B model card"
[2]: https://huggingface.co/Qwen/Qwen3.8-Flash-Next "Qwen3.8-Flash-Next model card"
[3]: https://huggingface.co/Qwen/Qwen3.6-35B-A3B "Qwen3.6-35B-A3B model card"
[4]: https://huggingface.co/Qwen/Qwen3-Coder-Next "Qwen3-Coder-Next model card"
[5]: https://ai.meta.com/blog/llama-4-multimodal-intelligence/ "Meta: Llama 4"
[6]: https://ai.meta.com/blog/meta-llama-3-1/ "Meta: Llama 3.1"
[7]: https://atomic.chat/blog/guides/best-local-llms-for-coding "Atomic Chat — Best Local LLM for Coding in 2026"
[8]: https://huggingface.co/poolside/Laguna-XS-2.1 "Laguna XS 2.1 model card"
[9]: https://huggingface.co/poolside/Laguna-XS-2.1-GGUF "Laguna XS 2.1 GGUF (Q4_K_M 20,3 GB)"
[10]: https://huggingface.co/moonshotai/Kimi-K2.7-Code "Kimi K2.7 Code model card"
[11]: https://ollama.com/library/laguna-xs-2.1 "Ollama — laguna-xs-2.1 (tags locais)"
[12]: https://ollama.com/library/kimi-k2.7-code "Ollama — kimi-k2.7-code (apenas :cloud)"
