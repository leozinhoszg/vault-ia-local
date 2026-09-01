# Kimi K2.6

| Campo | Registro |
|---|---|
| Data de verificação | 2026-09-01 |
| Arquitetura | MoE causal |
| Parâmetros totais/ativos | 1T / 32B ativos |
| Experts | 384 routed, 8 routed por token, 1 shared, conforme model card |
| Contexto | 256K tokens |
| Licença | modified-MIT; revisar restrições da versão |
| Memória estimada | Dimensionar pelos pesos totais do checkpoint e runtime, não pelos 32B ativos |
| Hardware medido | Não medido neste sandbox |
| Velocidade | Não publicar sem benchmark próprio |
| Tool calling/JSON | Validar com harness de agente |
| Fonte primária | [[02-Modelos/Ficha-padronizada-por-modelo]] e [model card](https://huggingface.co/moonshotai/Kimi-K2.6) |
| Estado | Candidato para infraestrutura de alta memória |
| Dono | Luiz Guimarães |
| Próxima revisão | 2026-10-01 |

O número de parâmetros ativos informa computação por token, mas não elimina o armazenamento dos experts. O modelo é inadequado para uma workstation comum sem quantização e memória suficiente.
