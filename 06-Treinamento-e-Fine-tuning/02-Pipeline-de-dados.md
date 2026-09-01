# Pipeline de dados

Dados são o principal ativo do fine-tuning. Defina origem, titularidade, licença, finalidade, retenção, PII, direitos autorais e trilha de auditoria. Use validações automáticas para schema, duplicatas, toxicidade, instruções escondidas e respostas inconsistentes.

| Estágio | Controle |
|---|---|
| Coleta | Consentimento, licença e proveniência. |
| Limpeza | PII, duplicatas e conteúdo corrompido. |
| Curadoria | Critérios de qualidade e exemplos difíceis. |
| Split | Separação por entidade/documento para evitar vazamento. |
| Treino | Registro de seed, versão, hiperparâmetros e hardware. |
| Avaliação | Casos normais, borda, segurança e regressão. |
| Publicação | Model card, dataset card, licença e rollback. |
