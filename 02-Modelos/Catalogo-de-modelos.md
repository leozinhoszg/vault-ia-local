# Catálogo de modelos atuais

Esta é uma shortlist para avaliação local em 2026. “Cabe” significa **estimativa dos pesos quantizados**, não garantia de velocidade ou qualidade. Baixe somente de repositórios oficiais ou mantenedores conhecidos e registre hash, licença e data.

| Família / exemplo | Parâmetros publicados | Modalidade | Perfil local sugerido | Observação |
|---|---:|---|---|---|
| Qwen3.8-27B | 27B dense | Texto + visão | 16–24 GB VRAM em quantização baixa; mais com contexto | Contexto nativo 262k, extensível conforme model card. |
| Qwen3.8-Flash-Next | 125B total / 6B ativos; + componentes publicados | Texto | Servidor multi-GPU ou memória unificada grande | MoE; ativos não eliminam a necessidade de armazenar pesos. |
| Qwen3.6-35B-A3B | 35B total / 3B ativos | Texto | 16–24 GB com quantização adequada | Bom candidato para experimentar MoE compacto. |
| Qwen3-Coder-Next | 80B total / 3B ativos | Código | Servidor ou workstation com muita RAM/VRAM | Prioriza agentes e coding; confirme licença e runtime. |
| Llama 4 Scout | 109B total / 17B ativos, 16 experts | Texto + visão | A Meta declara execução em um H100 com Int4 | Contexto anunciado de até 10M; contexto longo tem custo operacional. |
| Llama 4 Maverick | 400B total / 17B ativos, 128 experts | Texto + visão | Host H100/DGX ou distribuição | Grande footprint de pesos apesar de poucos ativos. |
| Llama 3.1 8B / 70B / 405B | 8B / 70B / 405B | Texto | 8B em máquina pessoal; maiores em servidor | 128K de contexto anunciado para a série. |
| Gemma 3 1B–27B | Varia por versão | Texto + visão em variantes | 8–24 GB conforme tamanho | Compactos e úteis para edge; confira licença. |
| DeepSeek-R1 e derivados | Varia; grandes versões MoE | Raciocínio | Quantizados ou multi-GPU | Raciocínio pode aumentar tokens gerados e custo. |
| Coding local — shortlist Atomic | Qwen3-Coder 30B, Qwen3-Coder-Next 80B, Laguna S 2.1 118B, Gemma 4 26B A4B, Qwen3.6 27B | Código / agentes | 24 GB para a classe 27–30B; 45–96 GB para modelos maiores | Ver análise de benchmarks, VRAM e velocidade em [[02-Modelos/LLMs-locais-para-coding-Atomic]]. |

Os números Qwen3.8 e Qwen3.6 acima são do model card oficial, enquanto os números de Llama 4 são da publicação da Meta. A shortlist de coding e os resultados de velocidade/VRAM foram adicionados a partir do guia da Atomic, com caráter editorial e dependência do hardware testado. A tabela deliberadamente não fixa preços: disponibilidade e câmbio mudam diariamente. Para escolher, faça uma matriz com qualidade no seu conjunto de testes, memória, latência, licença e custo total.

**Referências**

[1]: https://huggingface.co/Qwen/Qwen3.8-27B "Qwen3.8-27B model card"
[2]: https://huggingface.co/Qwen/Qwen3.8-Flash-Next "Qwen3.8-Flash-Next model card"
[3]: https://huggingface.co/Qwen/Qwen3.6-35B-A3B "Qwen3.6-35B-A3B model card"
[4]: https://huggingface.co/Qwen/Qwen3-Coder-Next "Qwen3-Coder-Next model card"
[5]: https://ai.meta.com/blog/llama-4-multimodal-intelligence/ "Meta: Llama 4"
[6]: https://ai.meta.com/blog/meta-llama-3-1/ "Meta: Llama 3.1"
[7]: https://atomic.chat/blog/guides/best-local-llms-for-coding "Atomic Chat — Best Local LLM for Coding in 2026"
