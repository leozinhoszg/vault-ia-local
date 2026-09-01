# Kimi K2.6

| Campo | Registro |
|---|---|
| Data de verificação | 2026-09-01 |
| Arquitetura | MoE causal |
| Parâmetros totais/ativos | 1T / 32B ativos |
| Experts | 384 routed, 8 routed por token, 1 shared, conforme model card |
| Contexto | 256K tokens |
| Licença | modified-MIT; revisar restrições da versão |
| Memória estimada | Dimensionar pelos pesos totais do checkpoint e runtime, não pelos 32B ativos; piso teórico em 4 bits ≈ 500 GB |
| Modo de execução | Infraestrutura de alta memória (modo 2 com RAM de servidor) ou serviço remoto. Na biblioteca Ollama a única tag é `kimi-k2.6:cloud` (modo 4, Ollama Cloud); `ollama run kimi-k2.6` não executa localmente. Ver [[02-Modelos/Local-real-vs-cloud]] e a [página do Ollama](https://ollama.com/library/kimi-k2.6) |
| Arquivo quantizado real | Não capturado para o K2.6; para a ordem de grandeza, o sucessor [[02-Modelos/Fichas/Kimi-K2.7-Code]] tem checkpoint INT4 nativo de 595 GB e GGUF de 304–595 GB |
| Hardware medido | Não medido neste sandbox |
| Velocidade | Não publicar sem benchmark próprio |
| Tool calling/JSON | Validar com harness de agente |
| Fonte primária | [[02-Modelos/Ficha-padronizada-por-modelo]] e [model card](https://huggingface.co/moonshotai/Kimi-K2.6) |
| Estado | Candidato para infraestrutura de alta memória |
| Dono | Luiz Guimarães |
| Próxima revisão | 2026-10-01 |

O número de parâmetros ativos informa computação por token, mas não elimina o armazenamento dos experts. O modelo é inadequado para uma workstation comum sem quantização e memória suficiente. Benchmarks publicados com metodologia (SWE-bench Verified 80,2 e Pro 58,6, média de 10 execuções) estão em [[02-Modelos/Tabela-normalizada-de-benchmarks]]; o sucessor focado em código é [[02-Modelos/Fichas/Kimi-K2.7-Code]].
