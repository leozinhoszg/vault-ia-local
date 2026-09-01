#!/usr/bin/env python3
"""Harness mínimo: coleta metadados e opcionalmente executa llama-bench."""
import argparse, hashlib, json, platform, shutil, subprocess, sys, time
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def cmd(s):
    p=subprocess.run(s, shell=True, text=True, capture_output=True)
    return {'command':s,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model', required=True, help='caminho do arquivo GGUF')
    ap.add_argument('--out', required=True, help='JSON de evidência')
    ap.add_argument('--llama-bench', default='llama-bench')
    ap.add_argument('--prompt', default='512')
    ap.add_argument('--generation', default='128')
    ap.add_argument('--repetitions', type=int, default=5)
    ap.add_argument('--execute', action='store_true')
    args=ap.parse_args()
    model=Path(args.model)
    if not model.exists(): raise SystemExit(f'modelo não encontrado: {model}')
    evidence={'captured_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'model_path':str(model.resolve()),'model_sha256':sha256(model),'host':{'os':platform.platform(),'python':platform.python_version(),'machine':platform.machine()},'runs':[]}
    for _ in range(args.repetitions):
        r=cmd(f'{shutil.which(args.llama_bench) or args.llama_bench} -m "{model}" -p {args.prompt} -n {args.generation}') if args.execute else {'command':'not executed','returncode':None,'stdout':'','stderr':''}
        evidence['runs'].append(r)
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
    print(out)
if __name__=='__main__': main()
