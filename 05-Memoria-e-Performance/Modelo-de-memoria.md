# Modelo de memória e banda

O footprint de uma sessão é aproximadamente:

`memória_total = pesos + KV_cache + ativações + workspace + runtime + sistema + folga`.

O KV cache cresce com camadas, dimensão de atenção, bytes por elemento, número de tokens e sequências concorrentes. GQA/MQA reduz KV em relação à atenção multi-head tradicional. Quantizar pesos reduz leitura de memória; quantizar KV pode aumentar a capacidade de contexto, com possível impacto de qualidade.

A largura de banda efetiva é crítica no decode: a cada token, grandes partes dos pesos são lidas. Por isso uma GPU com menos FLOPs mas mais banda pode vencer uma com mais FLOPs em um caso memory-bound. Prefill e decode devem ser medidos separadamente.

## Checklist de benchmark

| Métrica | Como interpretar |
|---|---|
| TTFT | Experiência inicial e custo do prompt. |
| tokens/s decode | Fluidez da resposta. |
| tokens/s agregado | Capacidade multiusuário. |
| pico de VRAM/RAM | Sizing e risco de OOM. |
| energia e temperatura | Custo operacional e sustentabilidade. |
| qualidade | Não sacrificar a tarefa real por velocidade. |
