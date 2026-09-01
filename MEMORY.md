# MEMORY — estado do vault

- **Última atualização:** 1º de setembro de 2026.
- **Escopo:** IA local para casa e empresa; hardware, software, modelos, RAG, treinamento, operação e governança.
- **Dono editorial:** Luiz Guimarães; substituto e dono técnico ainda precisam ser designados.
- **Fonte de verdade de hardware:** `03-Hardware/` e documentação oficial do fabricante.
- **Fonte de verdade de modelos:** model card/repositório oficial; blogs editoriais são contexto, não autoridade única.
- **Fonte de verdade de governança:** NIST AI 600-1 e políticas internas aprovadas.
- **Estado de revisão:** builds e preços são planejamento e precisam de cotação brasileira na data de compra; compatibilidade AMD exige consulta à matriz ROCm vigente.
- **Pendências:** designar substituto, revisor de segurança e operador de benchmarks; preencher região/tarifa de energia, orçamento real, máquina atual e conjunto de benchmarks do usuário.

## Changelog

- **2026-09-01 (rev. 2, re-auditoria P0):** corrigido `Break_even!E2:E4` da planilha TCO (faltava multiplicar o custo blended pelo câmbio; o resultado era ~5,5× maior que o texto); `Local!C2` passou a descontar o valor residual; fator Batch e fatores de contexto longo por categoria agora entram no cálculo; aba `Sensibilidade` ampliada para câmbio, vida útil, utilização e tarifa. Ficha do Qwen3-Coder 30B passou a citar o model card oficial (`Qwen3-Coder-30B-A3B-Instruct`). Script RAG ganhou `--selftest` e `--retrieve-only`; selftest executado em Windows/Python 3.11 com chromadb 1.0.20. Lockfile com hashes adicionado. Cabeçalhos `## Referências` e datas normalizados em 21 notas; validador passou a distinguir "Markdown no pacote" de "analisados" e a aceitar justificativas. Impacto: [[00-Inicio/Auditoria-P0]] reescrita; nenhuma recomendação de hardware ou modelo mudou. Fonte: re-auditoria externa + verificação com `openpyxl` e recomputação em Python.

