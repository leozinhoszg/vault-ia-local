#!/usr/bin/env python3
"""Regenera 11-Referencias/Indice-de-fontes-urls.md a partir das URLs do vault.

Escopo: arquivos .md, .py e .txt fora de .obsidian, excluindo o próprio índice,
os relatórios de validação e o lockfile. Endpoints locais (localhost/127.0.0.1)
são listados à parte e não contam como fonte.
"""
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '11-Referencias/Indice-de-fontes-urls.md'
SKIP = {OUT.name, 'VALIDACAO.md', 'VALIDACAO-COMPLETA.md', 'requirements-rag.lock.txt'}
URL = re.compile(r'https?://[^\s<>"\'`)\]|]+')

def main():
    found = {}
    for p in ROOT.rglob('*'):
        if not p.is_file() or p.suffix not in {'.md', '.py', '.txt'} or '.obsidian' in p.parts or p.name in SKIP:
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
    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print({'total': len(found), 'externas': len(ext), 'locais': len(local)})

if __name__ == '__main__':
    main()
