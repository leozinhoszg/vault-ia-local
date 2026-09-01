# Qwen3-Coder 30B

| Campo | Registro |
|---|---|
| Data de verificação | 2026-09-01 |
| Arquitetura | MoE para código |
| Parâmetros totais/ativos | 30,5B / 3,3B ativos, conforme registro editorial; confirmar versão exata no card |
| Contexto | 256K; extensão depende do runtime |
| Licença | Confirmar no model card do checkpoint exato |
| Memória estimada | Q4 editorial ~22 GB; tratar como medição externa, não requisito universal |
| Hardware medido | Atomic Chat: configuração do artigo; benchmark próprio pendente |
| Velocidade | 220 tok/s no teste Atomic; não generalizar |
| Tool calling/JSON | Validar com harness local |
| Fonte | [[02-Modelos/Ficha-padronizada-por-modelo]]; [Atomic Chat](https://atomic.chat/blog/guides/best-local-llms-for-coding) |
| Estado | Candidato para GPU de 24 GB, sujeito a teste |
| Dono | Luiz Guimarães |
| Próxima revisão | 2026-10-01 |
