# Evidência — hardening do RAG local (2026-09-01)

> **TL;DR:** o patch `c4ecf977a3ce8bbf53a23ca9ab0483fb761a3ce4`
> passou nos gates estático, editorial, de lock/SCA, selftest, embedding real e
> PDF opt-in descritos abaixo. A geração com Ollama e a instalação do lock em
> Windows limpo permanecem pendentes e não são implicitamente aprovadas.

## Escopo reproduzido

| Campo | Valor |
|---|---|
| Data | 2026-09-01 |
| Commit de código | `c4ecf977a3ce8bbf53a23ca9ab0483fb761a3ce4` |
| Base upstream | `6cc5209d607e09c8d63de2f44bac105f3d1abd32` |
| Ambiente | Container `python:3.11-slim-bookworm`, digest `sha256:528257d48c1da0dcecc2e725d1ae34498d60c965f1241e39cd6a85a8859bdf84`, sem bind mount do host |
| Python | 3.11.16 |
| Pins efetivos do smoke Linux | numpy 2.4.6; pypdf 6.16.2; sentence-transformers 6.0.1; huggingface-hub 1.29.0; torch 2.13.0+cu130; transformers 5.16.1 |
| Lock auditado | Windows x86_64/CPython 3.11; 43 pins; sha256 `f5256db8b01457745c1824f197232dcfe4086784a5945655aa4bcfa79b8b3ff4` |
| Embedding | `sentence-transformers/all-MiniLM-L6-v2`, snapshot `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, safetensors |
| Corpus funcional | 2 arquivos pequenos (`backup.md` e `ferias.txt`) com afirmações conhecidas; fixtures PDF em diretórios descartáveis |

O repositório foi copiado para o container; código ou dependências do parceiro
não foram executados diretamente no host. Downloads de modelo e dependências
ocorreram somente no container descartável.

## Resultados

| Gate | Comando/método | Resultado |
|---|---|---|
| Diff | `git diff --check` | Exit 0. |
| Validador | `python 99-Templates/validate_vault_completo.py --strict` | Exit 0; 0 erros e 0 avisos não justificados. |
| Índice de URLs | regeneração seguida de `--check` | Exit 0; índice sincronizado. |
| TCO | `python 99-Templates/check_tco.py` | Exit 0; valores em cache reconciliados e `Checks = PASS`. |
| Integridade do lock | `sha256sum -c requirements-rag.lock.sha256` | Exit 0, `OK`. |
| SCA | pip-audit 2.10.1, `--require-hashes --no-deps --disable-pip` | Exit 0; nenhuma vulnerabilidade conhecida encontrada no lock. Consulta OSV independente dos 43 pins também retornou zero findings nesta data. |
| Selftest | `python RAG-local-executavel.py --selftest` | Exit 0; limites, entrada ignorada, symlink/PDF default-deny, cosine, desempate, estado efêmero e citações passaram. |
| Embedding real | `--retrieve-only --top-k 1 --local-files-only` após cache do snapshot fixado | Exit 0; `backup.md#chunk-0` foi a Fonte 1 correta. O cache continha somente o snapshot `1110a243...`. |
| PDF opt-in | PDF válido em subprocesso com `--allow-pdf` | Exit 0; retrieval continuou correto e a fonte exposta permaneceu relativa. |
| Limite PDF | PDF de 2 páginas com `--max-pdf-pages 1` | Exit 2; falha fechada com `PDF excede max_pdf_pages=1`. |
| Reconciliação requirements/lock | numa cópia descartável, `numpy==2.4.6` foi trocado por `2.4.5` sem regenerar o lock | Exit 1; `RAG_DIRECT_PIN_LOCK_MISMATCH` detectado. |

## O que permanece pendente

- instalar `requirements-rag.lock.txt` em Windows x86_64/Python 3.11 limpo;
- repetir retrieval e geração com Ollama na revisão atual, incluindo ausência de
  evidência, resposta vazia, timeout e limite de corpo;
- testar PDF hostil dentro da sandbox operacional recomendada; subprocesso e
  timeout não são uma sandbox de memória, kernel ou filesystem;
- medir corpus real/maior, recall@k, groundedness, latência, concorrência e uso
  de memória;
- fechar atomicamente a janela TOCTOU residual de troca e restauração de
  diretório pai exigiria APIs específicas do sistema operacional;
- o CI usa Actions fixadas por SHA, mas instalações auxiliares de pip-audit,
  openpyxl e NumPy ainda não têm um lock próprio de ferramentas.

Esses itens continuam gates independentes. O resultado acima não reaproveita a
reprodução histórica do pipeline Chroma como prova do patch atual.

*Última atualização: 2026-09-01. Próxima revisão: após o smoke Windows/Ollama.*

## Referências

[1]: https://github.com/Noobru/vault-ia-local/commit/c4ecf977a3ce8bbf53a23ca9ab0483fb761a3ce4 "Commit do hardening validado"
[2]: https://hub.docker.com/_/python "Imagem oficial Python"
[3]: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/1110a243fdf4706b3f48f1d95db1a4f5529b4d41 "Snapshot fixado do embedding"
[4]: https://github.com/huggingface/sentence-transformers/blob/main/SECURITY.md "Sentence Transformers — segurança no carregamento de modelos"
[5]: https://github.com/pypa/pip-audit "pip-audit"
[6]: https://osv.dev/ "OSV"
