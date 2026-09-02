# Validação automatizada do vault

- Markdown no pacote: 112
- Markdown analisados: 110 (excluídos os relatórios VALIDACAO-COMPLETA.md, VALIDACAO.md)
- Arquivos na triagem textual heurística: 124 (.cfg, .ini, .json, .key, .md, .pem, .properties, .ps1, .py, .sh, .toml, .txt, .yaml, .yml; nomes especiais: .env*)
- Notas de controle (frontmatter control_id): 3
- Limite da triagem: regexes indicam padrões suspeitos; não substituem secret scanning dedicado, histórico Git ou revisão humana.
- Erros: 0
- Avisos: 0
- Avisos justificados: 9

## Erros
- Nenhum erro.

## Avisos
- Nenhum aviso.

## Avisos justificados
- NO_REFERENCES_SECTION README.md — nota de apresentação e navegação; fontes ficam nas notas e em 11-Referencias
- NO_REFERENCES_SECTION 00-Inicio/Auditoria-P0.md — relatório interno; as evidências (células, comandos, versões) estão citadas inline e as fontes externas ficam nas notas auditadas
- NO_REFERENCES_SECTION 00-Inicio/MAPA.md — índice de navegação; as fontes estão nas notas técnicas vinculadas e em 11-Referencias
- NO_REFERENCES_SECTION 00-Inicio/Sessoes/2026-09-01-sessao-re-auditoria-P0.md — ata de sessão; as evidências estão nas notas e commits citados
- NO_REFERENCES_SECTION 07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01.md — nota de evidência; as fontes são o log e os artefatos abaixo
- NO_REFERENCES_SECTION 11-Referencias/Fontes-principais.md — lista de fontes primárias; as URLs são o próprio conteúdo
- NO_REFERENCES_SECTION 11-Referencias/Indice-de-fontes-urls.md — nota gerada automaticamente por 99-Templates/gerar_indice_urls.py; as fontes são o próprio conteúdo
- NO_REFERENCES_SECTION 99-Templates/Modelo-de-ficha-de-workstation.md — template vazio; cada ficha preenchida carrega as próprias fontes
- NO_FORMULAS 03-Hardware/Catalogo-NVIDIA-IA-local.xlsx — a planilha homônima é um snapshot tabular estático do catálogo; não contém modelo de cálculo
