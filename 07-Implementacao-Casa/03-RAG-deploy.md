# RAG executável — deploy local e limites

O protótipo [[07-Implementacao-Casa/RAG-local-executavel.py]] faz retrieval
cosine exato em memória com NumPy e chama o Ollama. Ele não usa banco vetorial
persistente: cada execução reconstrói o índice, evitando documentos stale e
removendo ChromaDB do caminho de dependências.

Instale os pins de [[07-Implementacao-Casa/requirements-rag.txt]]. Para uma
instalação reproduzível, prefira o lock com hashes em
[[07-Implementacao-Casa/requirements-rag.lock.txt]]. Ele é resolvido para
Windows x86_64/CPython 3.11; regenere para outra plataforma ou para uma build
específica de torch com CUDA/ROCm.

## Instalação

### Linux, macOS e WSL2

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# Selecione antes o build CPU/CUDA/ROCm do torch conforme a documentação oficial.
python -m pip install -r requirements-rag.txt
mkdir -p docs
python RAG-local-executavel.py --docs docs --query "Qual é a política de backup?" --model qwen3.5:4b
```

O lock versionado **não é portável para esse bloco**: ele foi resolvido para
Windows x86_64. O comando acima valida os pins diretos, mas não fixa as
transitivas. Para reprodução real em Linux/macOS/WSL, gere e versione um lock
específico do sistema e do backend torch escolhido, com hashes, e valide-o em
ambiente limpo antes do uso.

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-rag.lock.txt
New-Item -ItemType Directory -Force docs | Out-Null
.\.venv\Scripts\python.exe RAG-local-executavel.py --docs docs --query "Qual é a política de backup?" --model qwen3.5:4b
```

O embedding padrão é `sentence-transformers/all-MiniLM-L6-v2` na revisão
`1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, com
`trust_remote_code=False` e safetensors. Um modelo remoto diferente exige
`--embed-revision`; `--local-files-only` impede download durante a execução.
Registre também tag e digest do modelo Ollama: tag mutável não é identidade
reproduzível.

## Defaults de contenção

| Controle | Default | Efeito |
|---|---:|---|
| Entradas percorridas | `--max-entries 10000` | Limita diretórios e arquivos, inclusive formatos ignorados. |
| Arquivos | `--max-files 1000` | Limita arquivos percorridos, antes do filtro de extensão. |
| Bytes por arquivo | `--max-file-bytes 10485760` | Recusa arquivo maior que 10 MiB antes da extração. |
| Texto total | `--max-text-chars 20000000` | Limita memória e trabalho de chunking. |
| Chunks | `--max-chunks 20000` | Limita embeddings e matriz cosine. |
| PDF | recusado | Exige `--allow-pdf`, até 200 páginas e 30 s por subprocesso. |
| Ollama | loopback | Endpoint remoto exige `--allow-remote-ollama`; proxy e redirects são recusados. |
| Resposta Ollama | 10 MiB | Corpo HTTP e timeout são limitados. |

Symlinks, junctions/reparse points, arquivos não regulares, mudanças detectadas
durante a leitura e texto não UTF-8 são recusados. As fontes exibem somente o
caminho relativo a `--docs`; o caminho absoluto da máquina não entra no prompt.
O corpus é percorrido em ordem determinística.

Esses defaults são limites de um protótipo, não valores universais. Reduza-os
para corpus pequeno. Aumente-os apenas depois de medir memória, tempo e volume de
contexto. Busca exata em memória é apropriada para laboratório; produção maior
precisa de um índice escolhido e operado com threat model, ACL e lifecycle.

## PDF é opt-in, não “seguro por flag”

```bash
python RAG-local-executavel.py --docs docs --allow-pdf --pdf-timeout 20 \
  --max-pdf-pages 100 --query "Qual é o prazo contratual?" --retrieve-only
```

O subprocesso e o timeout contêm hang simples, mas não formam uma sandbox de
memória, kernel ou filesystem. PDF de origem não confiável deve ser extraído em
container/VM sem secrets, sem rede, com CPU/RAM/PIDs/filesystem limitados; envie
ao RAG apenas o texto resultante após validação. O pin atual do pypdf corrige
advisories conhecidos do pin anterior, mas atualização não elimina a classe de
risco de parser complexo.

## Prompt injection documental

As evidências entram entre delimitadores explícitos e são rotuladas como dados
não confiáveis. O prompt manda ignorar instruções encontradas dentro dos
documentos, mas isso é mitigação, não garantia. O protótipo não possui tools nem
credenciais; mantenha-o assim no laboratório. Antes de permitir tool use,
adicione policy enforcement fora do modelo, allowlist, aprovação humana,
separação de tenants, eval adversarial e auditoria de cada ação.

## Selftest isolado

```bash
python -m pip install numpy==2.4.6
python RAG-local-executavel.py --selftest
```

O selftest não baixa modelo e não chama Ollama nem parser PDF. Ele cobre limites,
rejeição de PDF/symlink, desempate determinístico, ausência de estado stale,
retrieval cosine e citações relativas. Resultado esperado: `SELFTEST OK`. Para
inspecionar evidências com o embedding real, use `--retrieve-only`.

## Evidência e aceite

A reprodução de 2026-09-01 em
[[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]] permanece como
evidência histórica do pipeline anterior com ChromaDB. Ela não valida este
patch. O gate atual deve registrar separadamente:

1. checksum e instalação do novo lock;
2. `--selftest` em Linux e Windows;
3. embedding real fixado por revisão;
4. geração Ollama com tag, digest, contexto, latência e citações;
5. casos sem evidência, prompt injection, corpus no limite e PDF isolado.

O CI executa os itens que não exigem modelo/hardware e roda SCA no lockfile. A
validação ponta a ponta com Ollama continua sendo um gate distinto.

## Produção

Acrescente autenticação, ACL antes do retrieval, isolamento por tenant, fila de
ingestão, object storage, versionamento/tombstone, índice com filtros,
observabilidade, quotas e eval contínua. Meça recall@k, MRR, precisão e cobertura
de citação, groundedness, resposta “não sei”, latência e uso de recursos. Inclua
documentos conflitantes, poisoning, tabelas, OCR, prompt injection e revogação de
acesso. Nunca exponha o endpoint Ollama diretamente à internet.

*Última atualização: 2026-09-01. Próxima revisão: 2026-10-01.*

## Referências

[1]: https://github.com/advisories/GHSA-f4j7-r4q5-qw2c "GitHub Advisory — ChromaDB pre-auth code injection"
[2]: https://github.com/advisories/GHSA-36p7-vc44-83pf "GitHub Advisory — ChromaDB code injection"
[3]: https://pypdf.readthedocs.io/ "pypdf — extração de texto de PDF"
[4]: https://sbert.net/docs/package_reference/sentence_transformer/model.html "Sentence Transformers — model loading e revision"
[5]: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/1110a243fdf4706b3f48f1d95db1a4f5529b4d41 "Artefato de embedding fixado"
[6]: https://docs.ollama.com/api/generate "Ollama — Generate API"
[7]: https://pytorch.org/get-started/locally/ "PyTorch — seleção oficial de plataforma e backend"
[8]: https://github.com/advisories/GHSA-5xf7-4p34-54qr "GitHub Advisory — pypdf infinite loop"
[9]: https://github.com/advisories/GHSA-g867-7843-wf8q "GitHub Advisory — pypdf infinite loop"
[10]: https://github.com/advisories/GHSA-fwg2-594c-jp42 "GitHub Advisory — pypdf CID width resource exhaustion"
[11]: https://github.com/advisories/GHSA-fp3f-mc75-235c "GitHub Advisory — pypdf ToUnicode memory exhaustion"

Nota canônica: [[07-Implementacao-Casa/RAG-livro]].
