# Avaliação e regressão de modelos

## Dataset dourado

Crie um conjunto versionado de perguntas reais, respostas esperadas, fontes gold, critérios e severidade. Inclua casos de sucesso, “não sei”, conflito documental, prompt injection, tool call, JSON, código, português/inglês, contexto curto/longo e dados sensíveis sintéticos. O dataset deve ter hash, licença e dono.

## Métricas

| Dimensão | Métricas |
|---|---|
| Qualidade geral | Judge rubric, pairwise win rate, factualidade e completude. |
| RAG | Recall@k, MRR, nDCG, groundedness, precisão/cobertura de citação. |
| Código | Compilação, testes passantes, lint, regressões e segurança. |
| Agente | Conclusão, passos, tool-call correto, loops e intervenção. |
| Performance | TTFT P50/P95, decode P50/P95, tokens/s, throughput e fila. |
| Recursos | Pico de VRAM/RAM, energia, custo/tarefa e taxa de OOM. |

## Harness mínimo

Execute base e candidato com os mesmos prompts, seed, temperatura, tools, contexto, retriever, timeout e número de tentativas. Grave resultado estruturado, não raciocínio privado. Para P50/P95, use amostras suficientes e informe warm-up. Compare também erro e disponibilidade.

```json
{"id":"rag-001","question":"Qual é a política de backup?","gold_sources":["politica.md#backup"],"criteria":["cita a fonte","não inventa prazo"]}
```

## RAGAS ou equivalente

RAGAS pode ser usado como referência de avaliação de faithfulness, context precision e context recall, mas métricas baseadas em LLM podem introduzir viés. Combine avaliação automática, regras determinísticas de citação e revisão humana amostrada. Se RAGAS não for adequado ao idioma/domínio, implemente rubrica equivalente.

## Regressão

Defina limiares: queda de mais de 3 pontos percentuais em tarefas críticas, aumento de P95 acima de 20%, aumento de OOM, citação inválida ou tool-call perigoso bloqueiam rollout. Execute canary, compare e permita rollback para modelo, prompt, índice ou runtime anterior.

## Relatório

O relatório deve conter versão do modelo, hash, quantização, hardware, runtime, dataset, métricas, intervalos, falhas, decisão, aprovador e data da próxima revisão. Nunca publique um score isolado sem condições do teste.

## Referências

[1]: https://docs.ragas.io/ "Ragas documentation"
[2]: https://scikit-learn.org/stable/modules/model_evaluation.html "Model evaluation"
[3]: https://docs.vllm.ai/ "vLLM metrics and serving"
