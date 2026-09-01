> **Nota canônica:** o capítulo aprofundado está em [[06-Treinamento-e-Fine-tuning/Fine-tuning-livro]]. Esta nota é o roteiro operacional resumido.

# QLoRA prático

QLoRA congela o modelo base quantizado e treina adaptadores LoRA, reduzindo memória em comparação ao ajuste completo. É indicado para adaptar estilo, formato, vocabulário e comportamento em uma tarefa bem definida. Não é uma forma mágica de inserir uma base de conhecimento que muda diariamente; para isso, prefira RAG.

## Passos

1. Escolha modelo base e licença.
2. Defina o comportamento mensurável e um conjunto de validação separado.
3. Normalize exemplos no formato de conversa e remova segredos.
4. Faça split treino/validação por documento ou caso, evitando vazamento.
5. Carregue com bitsandbytes ou método suportado; aplique LoRA em módulos adequados.
6. Treine com learning rate baixo, poucos epochs e early stopping por avaliação.
7. Compare base, adapter e modelo mesclado no mesmo benchmark.
8. Publique adapter, configuração, dataset card, licença e hash.

## Riscos

Overfitting, esquecimento de capacidades gerais, vazamento de PII, contaminação da validação, instruções conflitantes e custo de inferência do adapter. Em produção, mantenha rollback para o modelo base.

## Referências

[1]: https://arxiv.org/abs/2305.14314 "QLoRA"
[2]: https://huggingface.co/docs/peft/index "Hugging Face PEFT"
[3]: https://github.com/unslothai/unsloth "Unsloth"
