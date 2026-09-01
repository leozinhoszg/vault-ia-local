# Evidência — reprodução do RAG em ambiente limpo (2026-09-01)

<!-- validador: sem-referencias: nota de evidência; as fontes são o log e os artefatos abaixo -->

| Campo | Valor |
|---|---|
| Data | 2026-09-01 |
| Máquina | Windows 11 Pro (build 10.0.26200), x86_64, sem GPU usada no teste (torch CPU) |
| Python | 3.11.9 |
| Procedimento | `python -m venv` novo → `pip install --require-hashes -r requirements-rag.lock.txt` (exit 0) → `--selftest` → `--retrieve-only` com embedding real |
| Lockfile | [[07-Implementacao-Casa/requirements-rag.lock.txt]] — sha256 `43a5d853cc7330c1440d757e4b7d423e754bf90708ceea80022625bec28e3f3f` |
| Versões efetivas | chromadb 1.0.20, pypdf 6.0.0, numpy **2.3.2**, requests 2.32.5, sentence-transformers 5.1.0, huggingface-hub 0.34.4, torch 2.13.0 (CPU), transformers 4.57.6, tokenizers 0.22.2 |
| Modelo de embedding | `sentence-transformers/all-MiniLM-L6-v2` (padrão do script; `EMBED_MODEL` sobrescreve) |
| Corpus de teste | 2 documentos: `politica-backup.md` (snapshots diários às 02h, retenção 30 dias) e `politica-ferias.txt` (30 dias de antecedência) |

## Resultados

| Etapa | Resultado | Latência |
|---|---|---|
| `--selftest` (embedding por hashing, Chroma, citação) | `SELFTEST OK`, exit 0 | 5,03 s |
| `--retrieve-only` "Qual é a política de backup e a retenção dos snapshots?" | `[Fonte 1]` = `politica-backup.md#chunk-0` (correto); exit 0 | 26,05 s (1ª execução) |
| `--retrieve-only` "Com quanta antecedência devo pedir férias?" | `[Fonte 1]` = `politica-ferias.txt#chunk-0` (correto); exit 0 | 23,03 s (modelo em cache) |
| Geração via Ollama com resposta `[Fonte N]` | **Não executada**: Ollama não está instalado nesta máquina | — |

A latência é dominada pelo import do torch CPU e pela carga do modelo de embedding a cada processo; o script é um protótipo sem servidor residente. A divergência anterior (selftest com numpy 2.4.6) foi eliminada: este teste usou exclusivamente o lockfile.

## O que este teste prova e o que não prova

Prova: o lockfile instala em ambiente limpo com verificação de hashes; o pipeline de ingestão, embedding real, índice Chroma e recuperação com citação funciona no stack documentado; a recuperação escolheu o documento correto em duas consultas simples. Não prova: qualidade de recuperação em corpus real, geração com Ollama, comportamento com PDFs escaneados, nem desempenho com GPU. O teste de aceitação completo ([[07-Implementacao-Casa/03-RAG-deploy]], seção "Smoke test funcional") permanece pendente de uma máquina com Ollama.

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
```
