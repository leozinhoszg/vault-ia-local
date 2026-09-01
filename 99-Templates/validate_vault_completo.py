from pathlib import Path
import re, ast, json, sys
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parent / 'vault-ia-local' if (Path(__file__).resolve().parent / 'vault-ia-local').exists() else Path(__file__).resolve().parent.parent
errors=[]; warnings=[]
md=[p for p in ROOT.rglob('*.md') if p.name not in {'VALIDACAO.md','VALIDACAO-COMPLETA.md'}]

for p in md:
    text=p.read_text(encoding='utf-8', errors='replace')
    # Reference URL syntax, without network access.
    for url in re.findall(r'\]\:\s*(https?://\S+)', text):
        if any(ch in url for ch in ['<','>','"']):
            warnings.append(f'MALFORMED_REFERENCE_URL {p.relative_to(ROOT)}')
    # Internal Obsidian links.
    for raw in re.findall(r'\[\[([^\]|#]+)', text):
        target=raw.strip()
        candidates=[ROOT/(target+'.md'), ROOT/target]
        if not any(c.exists() for c in candidates):
            errors.append(f'LINK {p.relative_to(ROOT)} -> {target}')
    # Agent-trace phrases, escaped newlines and obvious secrets.
    if re.search(r'Need update|Use file edit|tool_result_received|compacted_history|functions\.(file|shell|plan|message)|<system_reminder>', text, re.I):
        errors.append(f'AGENT_TRACE {p.relative_to(ROOT)}')
    if r'\\n\\n' in text or r'\\n' in text:
        errors.append(f'ESCAPED_NEWLINE {p.relative_to(ROOT)}')
    # Absolute paths and obvious secrets.
    if re.search(r'[A-Za-z]:\\|/home/ubuntu/|/Users/|C:\\Users', text):
        errors.append(f'ABSOLUTE_PATH {p.relative_to(ROOT)}')
    if re.search(r'(sk-[A-Za-z0-9]{20,}|OPENAI_API_KEY\s*=\s*[^$<\n]+|api[_-]?key\s*[:=]\s*[A-Za-z0-9_-]{20,})', text, re.I):
        errors.append(f'POSSIBLE_SECRET {p.relative_to(ROOT)}')
    # Editorial completeness checks.
    if len(text.splitlines()) >= 25 and '## Referências' not in text and '## References' not in text:
        warnings.append(f'NO_REFERENCES_SECTION {p.relative_to(ROOT)}')
    if len(text.splitlines()) >= 25 and not re.search(r'20\d{2}|Última atualização|Data|Status', text, re.I):
        warnings.append(f'NO_DATE_OR_STATUS {p.relative_to(ROOT)}')

# Python syntax.
for p in ROOT.rglob('*.py'):
    try: ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    except SyntaxError as e: errors.append(f'PYTHON {p.relative_to(ROOT)}:{e.lineno}:{e.msg}')

# 3) Dependency pinning.
req=ROOT/'07-Implementacao-Casa/requirements-rag.txt'
if not req.exists(): errors.append('MISSING_RAG_REQUIREMENTS')
else:
    for i,line in enumerate(req.read_text(encoding='utf-8').splitlines(),1):
        line=line.strip()
        if line and not line.startswith('#') and '==' not in line:
            errors.append(f'UNPINNED_DEPENDENCY requirements-rag.txt:{i}:{line}')

# 4) XLSX formulas and broken references.
for p in ROOT.rglob('*.xlsx'):
    try:
        wb=load_workbook(p, data_only=False)
        formulas=[]
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value,str) and c.value.startswith('='):
                        formulas.append((ws.title,c.coordinate,c.value))
                        if '#REF!' in c.value or '#DIV/0!' in c.value:
                            errors.append(f'FORMULA {p.name}!{ws.title}!{c.coordinate} {c.value}')
        if not formulas: warnings.append(f'NO_FORMULAS {p.relative_to(ROOT)}')
    except Exception as e: errors.append(f'XLSX {p.relative_to(ROOT)} {e}')

# 5) Prompt/secret trace audit; prompts are allowed in cookbooks, raw secrets are not.
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.py','.json','.txt'}:
        t=p.read_text(encoding='utf-8',errors='replace')
        if re.search(r'BEGIN (PRIVATE KEY|RSA PRIVATE KEY)|password\s*[:=]\s*[^<\n]{8,}|bearer\s+[A-Za-z0-9._-]{20,}',t,re.I):
            errors.append(f'PROMPT_OR_SECRET_TRACE {p.relative_to(ROOT)}')

report=ROOT/'VALIDACAO-COMPLETA.md'
lines=['# Validação completa do vault','',f'- Markdown analisados: {len(md)}',f'- Erros: {len(errors)}',f'- Avisos: {len(warnings)}','', '## Erros']
lines += [f'- {x}' for x in errors] or ['- Nenhum erro.']
lines += ['', '## Avisos'] + ([f'- {x}' for x in warnings] or ['- Nenhum aviso.'])
report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'markdown':len(md),'errors':len(errors),'warnings':len(warnings)},ensure_ascii=False))
if errors: sys.exit(1)
