# RAG executável

Instale as dependências fixadas em [[07-Implementacao-Casa/requirements-rag.txt]] para o script [[07-Implementacao-Casa/RAG-local-executavel.py]].

## Linux, macOS e WSL2

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-rag.txt
mkdir -p docs
python RAG-local-executavel.py --docs docs --query "Qual é a política de backup?" --model qwen3.6:27b
```

## Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-rag.txt
New-Item -ItemType Directory -Force docs | Out-Null
.\.venv\Scripts\python.exe RAG-local-executavel.py --docs docs --query "Qual é a política de backup?" --model qwen3.6:27b
```

O Ollama deve estar instalado e acessível em `http://127.0.0.1:11434`. Antes do teste, execute `ollama pull qwen3.6:27b` ou substitua por uma tag existente. O script ingere TXT, Markdown e PDF, preserva fonte e chunk, cria embeddings locais com Sentence Transformers, armazena Chroma e chama uma API local do Ollama.

## Smoke test

Coloque um arquivo `docs/teste.md` contendo uma afirmação conhecida. Execute o comando de consulta e aceite somente uma resposta que contenha `[Fonte N]`, não apresente traceback e recupere o arquivo de teste. Registre SO, Python, versões, modelo, hash, latência e resultado em [[99-Templates/Registro-de-benchmark]]. O validador confirma sintaxe Python, mas não substitui esse teste funcional.

## Produção

Substitua o chunking simples por parser por página/seção, aplique ACLs no índice, use embedding multilíngue validado, reranker opcional, criptografia e avaliação. Mantenha um arquivo JSONL com perguntas, fontes esperadas e critérios. Meça recall@k, MRR, precisão de citação, groundedness, resposta “não sei”, latência de ingestão, latência de recuperação e latência de geração. Inclua documentos com tabelas, PDFs escaneados, versões conflitantes e prompt injection.
