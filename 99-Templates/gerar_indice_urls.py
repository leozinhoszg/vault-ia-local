#!/usr/bin/env python3
"""Regenera 11-Referencias/Indice-de-fontes-urls.md a partir das URLs do vault.

Escopo: arquivos .md, .py e .txt fora de .obsidian, excluindo o próprio índice,
os relatórios de validação e o lockfile. Endpoints locais (localhost/127.0.0.1)
são listados à parte e não contam como fonte.

Uso: python gerar_indice_urls.py          # regenera se houver mudança de conteúdo
     python gerar_indice_urls.py --check  # sai com 1 se o índice estiver desatualizado
A linha "Gerado em" é ignorada na comparação, para não gerar ruído por data.
"""
import re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '11-Referencias/Indice-de-fontes-urls.md'
SKIP = {OUT.name, 'VALIDACAO.md', 'VALIDACAO-COMPLETA.md', 'requirements-rag.lock.txt'}
URL = re.compile(r'https?://[^\s<>"\'`)\]|]+')

def render():
    found = {}
    for p in ROOT.rglob('*'):
        if not p.is_file() or p.suffix not in {'.md', '.py', '.txt'} or '.obsidian' in p.parts or '.github' in p.parts or p.name in SKIP:
            continue
        for u in URL.findall(p.read_text(encoding='utf-8', errors='replace')):
            found.setdefault(u.rstrip('.,;:'), set()).add(p.relative_to(ROOT).as_posix())
    local = {u for u in found if re.match(r'https?://(localhost|127\.0\.0\.1)', u)}
    ext = sorted(set(found) - local)
    lines = ['# Índice central de fontes', '',
             '<!-- validador: sem-referencias: nota gerada automaticamente por 99-Templates/gerar_indice_urls.py; as fontes são o próprio conteúdo -->', '',
             f'Gerado em {date.today().isoformat()} por `99-Templates/gerar_indice_urls.py`. '
             f'URLs únicas no vault: {len(found)}, sendo {len(ext)} fontes externas e {len(local)} endpoints locais de exemplo '
             f'(listados ao final, não são fontes). Escopo: `.md`, `.py` e `.txt`, excluindo este índice, os relatórios de validação e o lockfile. '
             'O índice é auxiliar; a nota de origem continua sendo a autoridade contextual.', '',
             '| URL | Arquivos de origem |', '|---|---|']
    lines += [f'| {u} | {", ".join(sorted(found[u]))} |' for u in ext]
    lines += ['', '## Endpoints locais citados em exemplos', '', '| URL | Arquivos de origem |', '|---|---|']
    lines += [f'| {u} | {", ".join(sorted(found[u]))} |' for u in sorted(local)]
    return '\n'.join(lines) + '\n', {'total': len(found), 'externas': len(ext), 'locais': len(local)}

def sem_data(s):
    return '\n'.join(l for l in s.splitlines() if not l.startswith('Gerado em '))

def main():
    new, stats = render()
    old = OUT.read_text(encoding='utf-8') if OUT.exists() else ''
    atualizado = sem_data(old) == sem_data(new)
    if '--check' in sys.argv:
        if not atualizado:
            print('DESATUALIZADO: regenere com python 99-Templates/gerar_indice_urls.py', stats); return 1
        print('OK: índice de URLs atualizado', stats); return 0
    if atualizado:
        print('sem mudanças', stats); return 0
    OUT.write_text(new, encoding='utf-8'); print('regenerado', stats); return 0

if __name__ == '__main__':
    sys.exit(main())
