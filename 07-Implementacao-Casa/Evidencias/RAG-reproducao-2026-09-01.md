# Evidência — reprodução do RAG em ambiente limpo (2026-09-01)

<!-- validador: sem-referencias: nota de evidência; as fontes são o log e os artefatos abaixo -->

> [!warning] Evidência histórica do pipeline anterior
> Esta reprodução valida somente a versão que usava ChromaDB 1.0.20,
> pypdf 6.0.0 e caminhos absolutos nas citações. Esses pins foram substituídos
> após a identificação de advisories e de lacunas de contenção. O log abaixo é
> preservado como registro append-only e **não valida** o RAG endurecido atual.
> Para o gate vigente, use [[07-Implementacao-Casa/03-RAG-deploy]] e a revisão
> corrente de [[00-Inicio/Auditoria-P0]].

| Campo | Valor |
|---|---|
| Status | **Histórico/superado** — não usar como aceite da implementação atual |
| Data | 2026-09-01 |
| Máquina | Windows 11 Pro (build 10.0.26200), x86_64; GPU NVIDIA GeForce RTX 4060 Laptop 8 GB, driver 566.24 (usada só pelo Ollama; embeddings em torch CPU) |
| Python | 3.11.9 |
| Procedimento | `python -m venv` novo → `pip install --require-hashes -r requirements-rag.lock.txt` (exit 0) → `--selftest` → `--retrieve-only` com embedding real → pipeline completo com geração via Ollama |
| Lockfile | [[07-Implementacao-Casa/requirements-rag.lock.txt]] — sha256 `43a5d853cc7330c1440d757e4b7d423e754bf90708ceea80022625bec28e3f3f` |
| Versões efetivas | chromadb 1.0.20, pypdf 6.0.0, numpy **2.3.2**, requests 2.32.5, sentence-transformers 5.1.0, huggingface-hub 0.34.4, torch 2.13.0 (CPU), transformers 4.57.6, tokenizers 0.22.2 |
| Modelo de embedding | `sentence-transformers/all-MiniLM-L6-v2` (padrão do script; `EMBED_MODEL` sobrescreve) |
| Ollama | 0.33.2 (winget `Ollama.Ollama`), servidor em `127.0.0.1:11434`; modelo `qwen3.5:4b`, Q4_K_M, 4,7B parâmetros, digest `2a654d98e6fb`, 3,4 GB, 100% GPU, `num_ctx` 8192 |
| Corpus de teste | 2 documentos: `politica-backup.md` (snapshots diários às 02h, retenção 30 dias) e `politica-ferias.txt` (30 dias de antecedência, gestor aprova) |

## Resultados

| Etapa | Resultado | Latência |
|---|---|---|
| `--selftest` (embedding por hashing, Chroma, citação) | `SELFTEST OK`, exit 0 | 5,03 s |
| `--retrieve-only` "política de backup e retenção dos snapshots" | `[Fonte 1]` = `politica-backup.md#chunk-0` (correto); exit 0 | 26,05 s (1ª execução) |
| `--retrieve-only` "antecedência para pedir férias" | `[Fonte 1]` = `politica-ferias.txt#chunk-0` (correto); exit 0 | 23,03 s |
| Pipeline completo, pergunta 1 (backup) | Resposta correta com `[Fonte 1]`; 358 tokens de prompt, 48 de resposta; geração 9,3 s (inclui carga do modelo) | 34,7 s ponta a ponta |
| Pipeline completo, pergunta 2 (férias) | Resposta correta com `[Fonte 1]` em duas afirmações; geração 0,9 s | 24,9 s |
| Pipeline completo, pergunta 3 (reembolso de viagens — **sem evidência no corpus**) | "Não foi encontrado…", citando `[Fonte 1]` e `[Fonte 2]` como examinadas; geração 1,1 s | 24,1 s |

A latência ponta a ponta é dominada pelo import do torch CPU e pela carga do modelo de embedding a cada processo (≈ 23 s); a geração em GPU fica em ~1 s após o modelo carregado. O script é um protótipo sem servidor residente.

## Defeito encontrado e corrigido durante o teste

Na primeira execução completa, a pergunta 3 devolveu `response` vazia com exit 0. Diagnóstico por chamada direta à API: `qwen3.5:4b` é um modelo com *thinking*; com o modo ligado (padrão) ele gastou 3.138 tokens de raciocínio (47 s) e, como o servidor usava o `num_ctx` padrão de 4096, o orçamento acabou antes da resposta. Com `think=false` a mesma pergunta foi respondida corretamente em 0,9 s. Correção no script: `think` desligado por padrão (`--think` para habilitar), `--num-ctx` explícito (padrão 8192), resposta vazia vira exit 3 com `done_reason` no stderr, e o rodapé imprime tokens e duração reportados pelo Ollama.

## O que este teste provou para a versão histórica

Na revisão então testada, o lockfile instalou em ambiente limpo com verificação
de hashes; ingestão, embedding real, índice Chroma, recuperação e geração com
citação `[Fonte N]` funcionaram no corpus descrito; o modelo recusou responder
sem evidência. Isso não prova a implementação atual, segurança das dependências,
qualidade em corpus real e maior, PDFs escaneados, recall@k/groundedness,
concorrência nem desempenho de embeddings em GPU. Esses itens seguem o roteiro
de [[07-Implementacao-Casa/03-RAG-deploy]] e devem ser registrados em
[[99-Templates/Registro-de-benchmark]].

## Log (caminhos locais anonimizados)

```text
== 2026-09-01T15:10:47Z ambiente limpo (venv novo, pip install --require-hashes -r requirements-rag.lock.txt)
python 3.11.9 Windows 10 AMD64
lock sha256: 43a5d853cc7330c1440d757e4b7d423e754bf90708ceea80022625bec28e3f3f
chromadb==1.0.20
huggingface-hub==0.34.4
numpy==2.3.2
pypdf==6.0.0
requests==2.32.5
sentence-transformers==5.1.0
tokenizers==0.22.2
torch==2.13.0
transformers==4.57.6
== --selftest
SELFTEST OK: chunking, Chroma, recupera��o e formato de cita��o funcionam. N�o testa embedding real nem gera��o via Ollama.

exit=0 latencia=5.03s
== --retrieve-only com sentence-transformers/all-MiniLM-L6-v2
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<caminho-local> line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '/ufffd' in position 195: character maps to <undefined>
== --retrieve-only com sentence-transformers/all-MiniLM-L6-v2 (1ª execução, inclui download do modelo se ausente)
[Fonte 1: <scratch>/ragtest/docs/politica-backup.md#chunk-0] # Política de backup Os snapshots do servidor de arquivos são feitos diariamente às 02h e retidos por 30 dias. Backups mensais completos ficam guardados por 12 meses em cofre externo. A restauração deve ser testada trimestralmente.

[Fonte 2: <scratch>/ragtest/docs/politica-ferias.txt#chunk-0] Política de férias: o colaborador deve solicitar férias com pelo menos 30 dias de antecedência e o gestor aprova em até 5 dias úteis. Férias podem ser divididas em até três períodos.
STDERR(tail): 
exit=0 latencia_total=26.05s
== --retrieve-only (2ª execução, modelo em cache)
[Fonte 1: <scratch>/ragtest/docs/politica-ferias.txt#chunk-0] Política de férias: o colaborador deve solicitar férias com pelo menos 30 dias de antecedência e o gestor aprova em até 5 dias úteis. Férias podem ser divididas em até três períodos.

[Fonte 2: <scratch>/ragtest/docs/politica-backup.md#chunk-0] # Política de backup Os snapshots d
exit=0 latencia_total=23.03s
== 2026-09-01T15:34:04Z geração via Ollama {"version":"0.33.2"} modelo qwen3.5:4b (Q4_K_M, digest 2a654d98e6fb, 3,4 GB) GPU: NVIDIA GeForce RTX 4060 Laptop GPU, 566.24
== pipeline completo | pergunta: Qual é a política de backup e a retenção dos snapshots?
Os snapshots do servidor de arquivos são feitos diariamente às 02h e retidos por 30 dias [Fonte 1].
Backups mensais completos ficam guardados por 12 meses em cofre externo [Fonte 1].
A restauração deve ser testada trimestralmente [Fonte 1].
STDERR(tail): 
exit=0 latencia_total=55.67s cita_fonte=True
== pipeline completo | pergunta: Com quanta antecedência devo pedir férias e quem aprova?
De acordo com a política de férias, o colaborador deve solicitar férias com pelo menos 30 dias de antecedência [Fonte 1]. A aprovação da solicitação é realizada pelo gestor [Fonte 1].
STDERR(tail): 
exit=0 latencia_total=39.71s cita_fonte=True
== pipeline completo | pergunta: Qual é o limite de reembolso de viagens?

STDERR(tail): 
exit=0 latencia_total=69.90s cita_fonte=False
== ollama ps (após execução)
NAME          ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
qwen3.5:4b    2a654d98e6fb    3.1 GB    100% GPU     4096       4 minutes from now    
== 2026-09-01T15:38:36Z reexecução após correção do script (think=false, num_ctx=8192); causa da resposta vazia: thinking + num_ctx 4096 padrão do servidor
== pipeline completo | pergunta: Qual é a política de backup e a retenção dos snapshots?
Os snapshots do servidor de arquivos são feitos diariamente às 02h e retidos por 30 dias, enquanto os backups mensais completos ficam guardados por 12 meses em um cofre externo [Fonte 1].
STDERR(tail): [modelo=qwen3.5:4b done_reason=stop prompt_tokens=358 tokens_resposta=48 duracao_total=9.3s]
exit=0 latencia_total=34.73s cita_fonte=True
== pipeline completo | pergunta: Com quanta antecedência devo pedir férias e quem aprova?
Você deve solicitar as férias com pelo menos 30 dias de antecedência [Fonte 1] e a aprovação é feita pelo gestor [Fonte 1].
STDERR(tail): [modelo=qwen3.5:4b done_reason=stop prompt_tokens=358 tokens_resposta=33 duracao_total=0.9s]
exit=0 latencia_total=24.86s cita_fonte=True
== pipeline completo | pergunta: Qual é o limite de reembolso de viagens?
Não foi encontrado nenhum evidências sobre o limite de reembolso de viagens nas fontes fornecidas. As informações disponíveis referem-se exclusivamente à política de férias ([Fonte 1]) e à política de backup ([Fonte 2]).
STDERR(tail): [modelo=qwen3.5:4b done_reason=stop prompt_tokens=354 tokens_resposta=46 duracao_total=1.1s]
exit=0 latencia_total=24.13s cita_fonte=True
== ollama ps
NAME          ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
qwen3.5:4b    2a654d98e6fb    3.3 GB    100% GPU     8192       4 minutes from now
```
