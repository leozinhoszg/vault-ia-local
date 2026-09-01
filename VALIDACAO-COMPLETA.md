# Validação automatizada do vault

- Markdown no pacote: 81
- Markdown analisados: 79 (excluídos os relatórios VALIDACAO-COMPLETA.md, VALIDACAO.md)
- Arquivos na triagem textual heurística: 90 (.cfg, .ini, .json, .md, .ps1, .py, .sh, .toml, .txt, .yaml, .yml)
- Limite da triagem: regexes indicam padrões suspeitos; não substituem secret scanning dedicado, histórico Git ou revisão humana.
- Erros: 0
- Avisos: 1
- Avisos justificados: 7

## Erros
- Nenhum erro.

## Avisos
- NO_FORMULAS 03-Hardware/Catalogo-NVIDIA-IA-local.xlsx

## Avisos justificados
- NO_REFERENCES_SECTION README.md — nota de apresentação e navegação; fontes ficam nas notas e em 11-Referencias
- NO_REFERENCES_SECTION 00-Inicio/Auditoria-P0.md — relatório interno; as evidências (células, comandos, versões) estão citadas inline e as fontes externas ficam nas notas auditadas
- NO_REFERENCES_SECTION 00-Inicio/MAPA.md — nota de navegação; as fontes ficam nas notas de destino e em 11-Referencias
- NO_REFERENCES_SECTION 00-Inicio/Sessoes/2026-09-01-sessao-re-auditoria-P0.md — ata de sessão; as evidências estão nas notas e commits citados
- NO_REFERENCES_SECTION 11-Referencias/Fontes-principais.md — lista de fontes primárias; as URLs são o próprio conteúdo
- NO_REFERENCES_SECTION 11-Referencias/Indice-de-fontes-urls.md — nota gerada automaticamente por 99-Templates/gerar_indice_urls.py; as fontes são o próprio conteúdo
- NO_REFERENCES_SECTION 07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01.md — nota de evidência; as fontes são o log e os artefatos abaixo
