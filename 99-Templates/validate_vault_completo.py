from pathlib import Path
import re, ast, json, sys
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parent / 'vault-ia-local' if (Path(__file__).resolve().parent / 'vault-ia-local').exists() else Path(__file__).resolve().parent.parent
errors=[]; warnings=[]; justified=[]
def rel(p): return p.relative_to(ROOT).as_posix()
EXCLUDED_REPORTS={'VALIDACAO.md','VALIDACAO-COMPLETA.md'}
all_md=[p for p in ROOT.rglob('*.md') if '.obsidian' not in p.parts]
md=[p for p in all_md if p.name not in EXCLUDED_REPORTS]
JUST=re.compile(r'<!--\s*validador:\s*(sem-referencias|sem-data)\s*:\s*(.+?)\s*-->')

for p in md:
    text=p.read_text(encoding='utf-8', errors='replace')
    # Reference URL syntax, without network access.
    for url in re.findall(r'\]\:\s*(https?://\S+)', text):
        if any(ch in url for ch in ['<','>','"']):
            warnings.append(f'MALFORMED_REFERENCE_URL {rel(p)}')
    # Internal Obsidian links.
    for raw in re.findall(r'\[\[([^\]|#]+)', text):
        target=raw.strip()
        candidates=[ROOT/(target+'.md'), ROOT/target]
        if not any(c.exists() for c in candidates):
            errors.append(f'LINK {rel(p)} -> {target}')
    # Agent-trace phrases, escaped newlines and obvious secrets.
    if re.search(r'Need update|Use file edit|tool_result_received|compacted_history|functions\.(file|shell|plan|message)|<system_reminder>', text, re.I):
        errors.append(f'AGENT_TRACE {rel(p)}')
    if r'\\n\\n' in text or r'\\n' in text:
        errors.append(f'ESCAPED_NEWLINE {rel(p)}')
    # Absolute paths and obvious secrets.
    if re.search(r'[A-Za-z]:\\|/home/ubuntu/|/Users/|C:\\Users', text):
        errors.append(f'ABSOLUTE_PATH {rel(p)}')
    if re.search(r'(sk-[A-Za-z0-9]{20,}|OPENAI_API_KEY\s*=\s*[^$<\n]+|api[_-]?key\s*[:=]\s*[A-Za-z0-9_-]{20,})', text, re.I):
        errors.append(f'POSSIBLE_SECRET {rel(p)}')
    # Editorial completeness checks. A note may justify an absence with
    # <!-- validador: sem-referencias: motivo --> or <!-- validador: sem-data: motivo -->.
    just={k:v for k,v in JUST.findall(text)}
    if len(text.splitlines()) >= 25 and '## Referências' not in text and '## References' not in text:
        if 'sem-referencias' in just: justified.append(f'NO_REFERENCES_SECTION {rel(p)} — {just["sem-referencias"]}')
        else: warnings.append(f'NO_REFERENCES_SECTION {rel(p)}')
    if len(text.splitlines()) >= 25 and not re.search(r'20\d{2}|Última atualização|Data|Status', text, re.I):
        if 'sem-data' in just: justified.append(f'NO_DATE_OR_STATUS {rel(p)} — {just["sem-data"]}')
        else: warnings.append(f'NO_DATE_OR_STATUS {rel(p)}')

# Python syntax.
for p in ROOT.rglob('*.py'):
    try: ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    except SyntaxError as e: errors.append(f'PYTHON {rel(p)}:{e.lineno}:{e.msg}')

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
        # Catálogos de especificações podem ser deliberadamente sem fórmulas;
        # planilhas financeiras continuam sujeitas à checagem de fórmulas.
        if not formulas and p.name not in {'Catalogo-NVIDIA-IA-local.xlsx'}:
            warnings.append(f'NO_FORMULAS {rel(p)}')
    except Exception as e: errors.append(f'XLSX {rel(p)} {e}')

# 5) Prompt/secret trace audit; prompts are allowed in cookbooks, raw secrets are not.
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.py','.json','.txt'}:
        t=p.read_text(encoding='utf-8',errors='replace')
        if re.search(r'BEGIN (PRIVATE KEY|RSA PRIVATE KEY)|password\s*[:=]\s*[^<\n]{8,}|bearer\s+[A-Za-z0-9._-]{20,}',t,re.I):
            errors.append(f'PROMPT_OR_SECRET_TRACE {rel(p)}')

report=ROOT/'VALIDACAO-COMPLETA.md'
lines=['# Validação completa do vault','',
       f'- Markdown no pacote: {len(all_md)}',
       f'- Markdown analisados: {len(md)} (excluídos os relatórios {", ".join(sorted(EXCLUDED_REPORTS))})',
       f'- Erros: {len(errors)}',f'- Avisos: {len(warnings)}',f'- Avisos justificados: {len(justified)}','', '## Erros']
lines += [f'- {x}' for x in errors] or ['- Nenhum erro.']
lines += ['', '## Avisos'] + ([f'- {x}' for x in warnings] or ['- Nenhum aviso.'])
lines += ['', '## Avisos justificados'] + ([f'- {x}' for x in justified] or ['- Nenhum.'])
report.write_text(chr(10).join(lines)+chr(10),encoding='utf-8')
print(json.dumps({'markdown_pacote':len(all_md),'markdown_analisados':len(md),'errors':len(errors),'warnings':len(warnings),'justified':len(justified)},ensure_ascii=False))
if errors: sys.exit(1)
if '--strict' in sys.argv and warnings: print('STRICT: avisos não justificados'); sys.exit(1)
