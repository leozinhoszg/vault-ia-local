# Regressão em machine learning — capítulo completo

## 1. Conceito

Regressão estima uma variável contínua a partir de atributos. Exemplos são consumo elétrico, demanda de tokens, preço, temperatura de GPU e risco de falha. Embora LLMs sejam modelos generativos, regressão continua importante para planejar capacidade, prever custo e avaliar sistemas locais.

Uma regressão linear escreve `y_hat = b0 + b1x1 + ... + bpxp`. O treinamento minimiza uma função de perda, frequentemente erro quadrático médio. Modelos robustos podem usar MAE, Huber, quantile loss ou árvores para lidar com outliers e relações não lineares.

## 2. Regressão versus classificação e geração

Classificação escolhe classes; regressão prevê números; geração produz sequências. Um sistema local pode usar os três: regressão para prever custo/latência, classificação para roteamento de prompts e LLM para resposta. Não use LLM como substituto automático de um modelo tabular simples.

## 3. Pipeline correto

Separe treino, validação e teste por tempo ou entidade quando houver vazamento. Faça baseline ingênuo, inspeção de missing, escalonamento quando necessário, seleção de atributos, validação cruzada e intervalo de incerteza. Compare com uma regra de negócio.

| Métrica | Uso | Limitação |
|---|---|---|
| MAE | Erro médio em unidade original | Pesa todos os erros igualmente. |
| RMSE | Penaliza erros grandes | Sensível a outliers. |
| MAPE | Erro percentual | Instável perto de zero. |
| R² | Variância explicada | Pode ser enganoso fora do domínio. |
| Pinball/quantílica | Previsão de percentis | Exige interpretação de quantis. |

## 4. Exemplo local

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

df=pd.read_csv('telemetria.csv')
X=df.loc[:, ['prompt_tokens','output_tokens','context_tokens','concurrency','gpu_watts']]
y=df['latency_ms']
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42)
m=HistGradientBoostingRegressor(max_iter=300,random_state=42).fit(Xtr,ytr)
p=m.predict(Xte)
print({'MAE_ms':mean_absolute_error(yte,p),'RMSE_ms':root_mean_squared_error(yte,p)})
```

Use este modelo para estimar latência ou energia somente dentro do domínio observado. Reavalie após trocar modelo, quantização, driver, contexto ou GPU. Monitoramento deve detectar drift.

## 5. Regressão para operação de LLM

Colete timestamp, modelo, quantização, tokens de entrada/saída, contexto, concorrência, TTFT, decode tokens/s, VRAM, RAM, potência e erro. Não inclua prompt sensível por padrão. Regressão ajuda a responder “quantas GPUs preciso?”, mas a decisão final deve ser confirmada por teste de carga.

## 6. Armadilhas

Correlação não prova causalidade. Latência tem caudas e filas; média pode esconder p95 ruim. Custo por token depende da utilização. Dados de uma GPU não generalizam para outra. Um modelo pode ajustar bem o histórico e falhar após atualização. Registre versão e mantenha um conjunto de aceitação congelado.

## Referências

[1]: https://scikit-learn.org/stable/modules/linear_model.html "scikit-learn linear models"
[2]: https://scikit-learn.org/stable/modules/model_evaluation.html "scikit-learn model evaluation"
