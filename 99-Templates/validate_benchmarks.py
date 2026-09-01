#!/usr/bin/env python3
import csv, datetime, hashlib, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/'05-Memoria-e-Performance/Benchmarks/results.csv'
required=['run_id','measured_at','model_id','quantization','hardware_id','runtime','context_tokens','concurrency','decode_tok_s','status']
errors=[]
with CSV.open(newline='',encoding='utf-8') as f:
    reader=csv.DictReader(f)
    rows=list(reader)
    missing=[x for x in required if x not in (rows[0].keys() if rows else reader.fieldnames or [])]
    errors += [f'coluna ausente: {x}' for x in missing]
    for i,r in enumerate(rows,2):
        if r.get('status') not in {'measured','failed','not_run'}: errors.append(f'linha {i}: status inválido')
        if r.get('measured_at'):
            try: datetime.datetime.fromisoformat(r['measured_at'].replace('Z','+00:00'))
            except ValueError: errors.append(f'linha {i}: measured_at inválido')
        for k in ['context_tokens','concurrency']:
            try:
                if int(r[k])<1: errors.append(f'linha {i}: {k} deve ser >=1')
            except (ValueError,TypeError): errors.append(f'linha {i}: {k} não numérico')
        if r.get('status')=='measured':
            try:
                if float(r['decode_tok_s'])<=0: errors.append(f'linha {i}: decode_tok_s deve ser >0')
            except (ValueError,TypeError): errors.append(f'linha {i}: decode_tok_s ausente/não numérico')
        if r.get('status')=='measured' and not re.fullmatch(r'[0-9a-fA-F]{64}',r.get('model_file_sha256','')): errors.append(f'linha {i}: SHA-256 do modelo ausente/inválido')
print(json.dumps({'rows':len(rows),'errors':errors},ensure_ascii=False))
sys.exit(1 if errors else 0)
