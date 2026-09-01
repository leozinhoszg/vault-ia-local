# Runbook operacional

## Diário

Verifique disponibilidade, erro por requisição, latência, tokens/s, fila, memória, temperatura e espaço em disco. Investigue picos de OOM e aumento de rejeições.

## Mudança de modelo

Registre versão, licença, hash, quantização, tokenizer e benchmark. Rode suíte de regressão; faça canary; compare custo e qualidade; mantenha rollback.

## Incidente

1. Congele mudanças.
2. Reduza tráfego ou desative ferramentas.
3. Preserve logs mínimos e seguros.
4. Verifique modelo, prompt, índice, GPU/driver e dependências.
5. Reverta para a última versão aprovada.
6. Documente causa, impacto e ação preventiva.

## Backup

Backupeie configurações, prompts, adapters, índices reconstruíveis, avaliações e manifests. Pesos grandes podem ser reobtidos, mas o hash e a origem devem ser preservados.
