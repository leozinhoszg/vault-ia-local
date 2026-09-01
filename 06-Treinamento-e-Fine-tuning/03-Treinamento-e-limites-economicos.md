# Treinamento, continued pretraining e distillation

## Níveis de adaptação

| Técnica | Quando usar | Custo relativo |
|---|---|---:|
| Prompt/RAG | Conhecimento mutável e comportamento simples | Baixo |
| LoRA/QLoRA/SFT | Formato, estilo, tarefa ou ferramentas | Baixo–médio |
| Preference tuning DPO/ORPO | Preferências e ranking de respostas | Médio |
| Distillation | Transferir comportamento de professor para modelo menor | Médio–alto |
| Continued pretraining | Domínio/idioma com grande corpus não rotulado | Alto |
| Pré-treinamento do zero | Criar modelo base próprio | Extremamente alto |

Continued pretraining exige corpus grande, limpo e licenciado; pode causar esquecimento catastrófico. Distillation exige política de qualidade e cuidado para não copiar erros ou dados protegidos do professor. Preference tuning precisa de pares ou rankings consistentes e avaliação de segurança.

## Limite econômico

Estime tokens, FLOPs, GPU-hours, energia, armazenamento, engenharia e avaliação. Pare se o ganho marginal for menor que o custo de RAG, prompt, ferramenta ou modelo maior. Para muitas empresas, comprar capacidade de inferência e curar dados gera mais retorno que treinar um modelo base.

## Portão de decisão

1. O problema é conhecimento mutável? Use RAG.
2. O problema é formato/comportamento repetitivo? Teste SFT/LoRA.
3. Há preferências mensuráveis? Teste DPO/ORPO.
4. Há corpus de domínio em escala? Avalie continued pretraining.
5. Há orçamento, dados e equipe para um ciclo completo? Só então considere distillation ou pré-treino.

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://arxiv.org/abs/2305.14314 "QLoRA: Efficient Finetuning of Quantized LLMs"
[2]: https://arxiv.org/abs/2305.18290 "Direct Preference Optimization"
[3]: https://huggingface.co/docs/peft/index "Hugging Face PEFT — adaptadores LoRA"
[4]: https://huggingface.co/docs/trl/index "Hugging Face TRL — SFT, DPO e ORPO"

Nota canônica: [[06-Treinamento-e-Fine-tuning/Fine-tuning-livro]].
