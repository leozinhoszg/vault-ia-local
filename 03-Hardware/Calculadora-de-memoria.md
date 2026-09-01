# Calculadora de memória

## Fórmulas

Memória aproximada dos pesos em **GB decimal**:

`peso_GB ≈ parâmetros × bits_por_peso / 8 / 1e9 × fator_de_escala`

Memória aproximada dos pesos em **GiB binário**:

`peso_GiB ≈ parâmetros × bits_por_peso / 8 / 2^30 × fator_de_escala`

Não misture unidades. Fabricantes de SSD e memória normalmente anunciam GB decimal; sistemas operacionais e ferramentas frequentemente exibem GiB. Um modelo denso de 27B em 4 bits tem piso de 13,5 GB decimal ou aproximadamente 12,57 GiB binário, antes de overhead.

Use `fator_de_escala` entre 1,05 e 1,20 para metadados, escalas, alinhamento e buffers. Depois some KV cache, ativação, workspace e margem. Para uma primeira estimativa conservadora, use 20–30% de folga.

| Precisão | Bytes por parâmetro | Exemplo 7B, pesos crus |
|---|---:|---:|
| FP32 | 4 | 28 GB decimal / 26,08 GiB |
| BF16/FP16 | 2 | 14 GB decimal / 13,04 GiB |
| INT8/FP8 | 1 | 7 GB decimal / 6,52 GiB |
| INT4/FP4 | 0,5 | 3,5 GB decimal / 3,26 GiB |

Quantização real tem escalas e formatos de bloco; por isso o arquivo não é exatamente `N × bits`. KV cache pode ser FP16, BF16, FP8 ou quantizado conforme runtime e modelo. Em contexto longo, ele pode ultrapassar os pesos.

## Exemplo de planejamento

Um modelo denso de 27B em 4 bits tem piso teórico de 13,5 GB decimal ou 12,57 GiB antes de overhead. Planeje algo como 15–18 GB decimal para pesos e buffers e acrescente KV cache conforme contexto e concorrência. Em MoE, calcule com parâmetros **totais** para armazenamento, não somente ativos.

## Comando útil

```bash
nvidia-smi
free -h
ls -lh models/
```

Meça a memória máxima no seu runtime; a fórmula é triagem, não benchmark.
