#!/usr/bin/env python3
"""RAG local mínimo: ingestão de TXT/MD/PDF, Chroma, embeddings e citações."""
from pathlib import Path
import argparse, os, requests
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

EXTS={'.txt','.md','.pdf'}
def read_file(p):
    if p.suffix.lower()=='.pdf':
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

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--docs',default='docs')
    ap.add_argument('--query',required=True)
    ap.add_argument('--model',default='qwen3.5:4b')
    ap.add_argument('--ollama',default='http://127.0.0.1:11434')
    args=ap.parse_args()
    embed=SentenceTransformer(os.getenv('EMBED_MODEL','sentence-transformers/all-MiniLM-L6-v2'))
    db=chromadb.PersistentClient(path='rag_db')
    col=db.get_or_create_collection('docs')
    ids=[]; texts=[]; metas=[]
    for p in Path(args.docs).rglob('*'):
        if p.is_file() and p.suffix.lower() in EXTS:
            for i,c in enumerate(chunks(read_file(p))):
                ids.append(f'{p}:{i}'); texts.append(c); metas.append({'source':str(p),'chunk':i})
    if texts:
        col.upsert(ids=ids,documents=texts,metadatas=metas,embeddings=embed.encode(texts).tolist())
    q=embed.encode([args.query]).tolist()
    res=col.query(query_embeddings=q,n_results=5)
    evidence='\n\n'.join(f"[Fonte {i+1}: {m['source']}#chunk-{m['chunk']}] {d}" for i,(d,m) in enumerate(zip(res['documents'][0],res['metadatas'][0])))
    prompt=f"""Responda em português usando somente as evidências abaixo. Cite [Fonte N] após cada afirmação. Se não houver evidência suficiente, diga que não foi encontrado.

EVIDÊNCIAS:
{evidence}

PERGUNTA:
{args.query}"""
    r=requests.post(f'{args.ollama}/api/generate',json={'model':args.model,'prompt':prompt,'stream':False},timeout=600)
    r.raise_for_status()
    print(r.json()['response'])

if __name__=='__main__':
    main()
