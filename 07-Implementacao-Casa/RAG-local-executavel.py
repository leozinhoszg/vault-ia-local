#!/usr/bin/env python3
"""RAG local mínimo: ingestão de TXT/MD/PDF, Chroma, embeddings e citações.

Modos:
  padrão      ingere --docs, recupera top-k e gera resposta via Ollama
              (thinking desligado e num_ctx=8192 por padrão; ver --think/--num-ctx).
  --retrieve-only  ingere e imprime somente as evidências (sem Ollama).
  --selftest  smoke test do pipeline (chunking, Chroma, recuperação e citação)
              com embedding determinístico local, sem baixar modelo nem chamar
              Ollama. Não valida qualidade de embedding nem de geração.
"""
from pathlib import Path
import argparse, hashlib, os, re, sys, tempfile

EXTS={'.txt','.md','.pdf'}

def read_file(p):
    if p.suffix.lower()=='.pdf':
        from pypdf import PdfReader
        return '\n'.join((page.extract_text() or '') for page in PdfReader(str(p)).pages)
    return p.read_text(encoding='utf-8', errors='ignore')

def chunks(text, size=900, overlap=120):
    text=' '.join(text.split())
    out=[]; start=0
    while start<len(text):
        end=min(len(text), start+size); out.append(text[start:end])
        if end==len(text): break
        start=end-overlap
    return out

class HashEmbedder:
    """Embedding bag-of-words por hashing (256 dims). Serve apenas para testar o encanamento."""
    dims=256
    def encode(self, texts):
        import numpy as np
        vecs=[]
        for t in texts:
            v=np.zeros(self.dims, dtype='float32')
            for tok in re.findall(r'\w+', t.lower()):
                if len(tok)<=2: continue  # reduz peso de artigos/preposições
                v[int(hashlib.md5(tok.encode()).hexdigest(),16)%self.dims]+=1.0
            n=np.linalg.norm(v); vecs.append(v/n if n else v)
        return np.stack(vecs)

def build_embedder(selftest):
    if selftest: return HashEmbedder()
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(os.getenv('EMBED_MODEL','sentence-transformers/all-MiniLM-L6-v2'))

def ingest_and_query(docs_dir, query, db_path, embed, k=5):
    import chromadb
    db=chromadb.PersistentClient(path=db_path)
    col=db.get_or_create_collection('docs')
    ids=[]; texts=[]; metas=[]
    for p in Path(docs_dir).rglob('*'):
        if p.is_file() and p.suffix.lower() in EXTS:
            for i,c in enumerate(chunks(read_file(p))):
                ids.append(f'{p}:{i}'); texts.append(c); metas.append({'source':str(p),'chunk':i})
    if texts:
        col.upsert(ids=ids,documents=texts,metadatas=metas,embeddings=embed.encode(texts).tolist())
    q=embed.encode([query]).tolist()
    res=col.query(query_embeddings=q,n_results=min(k, max(col.count(),1)))
    pairs=list(zip(res['documents'][0],res['metadatas'][0]))
    evidence='\n\n'.join(f"[Fonte {i+1}: {m['source']}#chunk-{m['chunk']}] {d}" for i,(d,m) in enumerate(pairs))
    return pairs, evidence

def build_prompt(evidence, query):
    return f"""Responda em português usando somente as evidências abaixo. Cite [Fonte N] após cada afirmação. Se não houver evidência suficiente, diga que não foi encontrado.

EVIDÊNCIAS:
{evidence}

PERGUNTA:
{query}"""

def selftest():
    # ignore_cleanup_errors: no Windows o Chroma mantém data_level0.bin aberto até o fim do processo.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        docs=Path(tmp)/'docs'; docs.mkdir()
        (docs/'backup.md').write_text('Política de backup: os snapshots são feitos diariamente às 02h e retidos por 30 dias. '*3, encoding='utf-8')
        (docs/'ferias.txt').write_text('Política de férias: o colaborador deve solicitar com 30 dias de antecedência. '*3, encoding='utf-8')
        pairs,evidence=ingest_and_query(docs,'Qual é a política de backup e a retenção dos snapshots?',str(Path(tmp)/'rag_db'),HashEmbedder(),k=2)
        assert pairs, 'nenhum chunk recuperado'
        assert pairs[0][1]['source'].endswith('backup.md'), f"fonte errada no topo: {pairs[0][1]['source']}"
        assert '[Fonte 1:' in evidence and '#chunk-0]' in evidence, 'citação ausente na evidência'
        prompt=build_prompt(evidence,'teste'); assert 'EVIDÊNCIAS:' in prompt
    print('SELFTEST OK: chunking, Chroma, recuperação e formato de citação funcionam. '
          'Não testa embedding real nem geração via Ollama.')

def main():
    ap=argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--docs',default='docs')
    ap.add_argument('--query')
    ap.add_argument('--model',default='qwen3.5:4b')
    ap.add_argument('--ollama',default='http://127.0.0.1:11434')
    ap.add_argument('--db',default='rag_db')
    ap.add_argument('--num-ctx',type=int,default=8192,help='janela de contexto pedida ao Ollama (padrão 8192; o padrão do servidor, 4096, pode truncar a resposta)')
    ap.add_argument('--think',action='store_true',help='habilita o modo thinking em modelos que o suportam (lento; pode consumir o contexto antes da resposta)')
    ap.add_argument('--retrieve-only',action='store_true')
    ap.add_argument('--selftest',action='store_true')
    args=ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.query:
        ap.error('--query é obrigatório fora do --selftest')
    embed=build_embedder(selftest=False)
    pairs,evidence=ingest_and_query(args.docs,args.query,args.db,embed)
    if args.retrieve_only:
        print(evidence); return
    import requests
    body={'model':args.model,'prompt':build_prompt(evidence,args.query),'stream':False,
          'think':args.think,'options':{'num_ctx':args.num_ctx}}
    r=requests.post(f'{args.ollama}/api/generate',json=body,timeout=600)
    r.raise_for_status(); data=r.json()
    resp=(data.get('response') or '').strip()
    if not resp:
        print(f"[sem resposta do modelo: done_reason={data.get('done_reason')}, eval_count={data.get('eval_count')}; "
              "verifique --num-ctx e se o modo thinking consumiu o contexto]", file=sys.stderr)
        return 3
    print(resp)
    print(f"[modelo={args.model} done_reason={data.get('done_reason')} prompt_tokens={data.get('prompt_eval_count')} "
          f"tokens_resposta={data.get('eval_count')} duracao_total={(data.get('total_duration') or 0)/1e9:.1f}s]", file=sys.stderr)

if __name__=='__main__':
    sys.exit(main())
