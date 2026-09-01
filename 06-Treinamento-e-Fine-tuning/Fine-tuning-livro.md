# Fine-tuning — capítulo completo

## 1. Escolha antes do treino

Use prompting quando o comportamento já existe; RAG quando o problema é conhecimento atual; fine-tuning quando há padrão repetitivo de saída, estilo, formato, ferramenta ou tarefa. Fine-tuning não é mecanismo confiável para inserir fatos que mudam diariamente.

## 2. SFT e adapters

Supervised fine-tuning treina o modelo em exemplos de entrada e resposta. LoRA congela o modelo base e aprende matrizes de baixa dimensão; QLoRA carrega o base quantizado, calcula em maior precisão e treina adapters. O adapter é pequeno e facilita experimentos, mas depende do modelo base e do tokenizer.

## 3. Dataset de qualidade

Defina contrato de dados, licença, consentimento, remoção de PII, deduplicação, balanceamento, dificuldade e critérios de aceitação. Divida por usuário, projeto ou documento para evitar vazamento. Para coding, inclua problema, contexto mínimo, patch, testes e explicação; não treine apenas em respostas perfeitas sem casos negativos.

## 4. Hiperparâmetros iniciais

Comece com batch 1, gradient accumulation para batch efetivo 8–32, learning rate LoRA entre 1e-4 e 3e-4, rank 8–32, alpha 16–64, dropout 0–0,1, 1–3 épocas, sequence length compatível e gradient checkpointing. São pontos de partida, não valores universais. Pare por overfitting e avalie a cada checkpoint.

## 5. Memória

Na QLoRA, os pesos ocupam menos memória, mas ativações crescem com sequência e batch; adapters e estados do otimizador também custam. Reserve memória para tokenização, dataloader, avaliação e checkpoints. OOM deve ser tratado reduzindo sequência/batch, ativando checkpointing, usando accumulation ou escolhendo modelo menor.

## 6. DPO e preference tuning

DPO aprende a preferência entre resposta escolhida e rejeitada sem treinar explicitamente um reward model. A qualidade e consistência dos pares são críticas. Use-o depois de um SFT funcional e mantenha testes contra degradação de segurança, factualidade e tool calling.

## 7. Checkpoint e merge

Salve adapter, base model ID, tokenizer, config, hashes, dataset manifest, hiperparâmetros, logs e ambiente. Faça avaliação do adapter antes do merge. Merge exige espaço adicional e pode ser irreversível na prática; mantenha base e adapter separados. Só depois exporte para formato de inferência e quantize uma cópia.

## 8. Avaliação

Compare base, adapter, merged e quantizado em teste não visto, prompts adversariais, formato estruturado, coding, RAG e ferramentas. Para código, execute lint, compilação e testes em sandbox. Relate intervalo de confiança quando possível e não use somente loss de treinamento.

## 9. Exemplo operacional

O roteiro executável em [[06-Treinamento-e-Fine-tuning/02-Fine-tuning-completo]] é o ponto de partida. Para um experimento sério, crie um registro de decisão, faça um pequeno piloto, valide consumo e qualidade, então escale.

## Referências

[1]: https://arxiv.org/abs/2106.09685 "LoRA"
[2]: https://arxiv.org/abs/2305.14314 "QLoRA"
[3]: https://arxiv.org/abs/2305.18290 "Direct Preference Optimization"
[4]: https://huggingface.co/docs/peft/index "PEFT"
[5]: https://huggingface.co/docs/trl/index "TRL"
