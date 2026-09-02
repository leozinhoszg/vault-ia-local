# Supply chain de modelos

- **Data:** 2026-09-01.
- **Escopo:** ciclo de vida do modelo como artefato controlado — da aquisição à aposentadoria. Formaliza o que o [[PROTOCOLO-DE-ATUALIZACAO]] já exige em prosa e o que [[08-Implementacao-Empresa/03-Seguranca-e-governanca]] pede (SBOM, hashes, inventário). Princípios destilados do cofre de coding (294 — DevSecOps e Supply Chain, citada por nome). Baseline editorial; nenhum registry foi implantado.

## Por que modelo é supply chain

Um GGUF é um artefato executável baixado de hub aberto, muitas vezes quantizado por terceiros que não são o autor do modelo. O risco OWASP LLM05 do [[10-Operacao-e-Seguranca/Threat-model-LLM-local]] cobre modelo adulterado, dataset envenenado e MCP server malicioso — todos entram pela mesma porta: dependência sem verificação. A evidência de 2026-09-01 mostrou que o Ollama desta máquina confia em `OLLAMA_REMOTES:[ollama.com]` por default ([[10-Operacao-e-Seguranca/Evidencias/Ollama-testes-negativos-2026-09-01]]).

## Regras

1. **Nada de `latest`, auto-pull ou atualização automática** em ambiente com dado sensível: versão fixada por digest/hash, promoção manual.
2. **Todo artefato tem manifesto** (abaixo) antes de servir; artefato sem manifesto não sobe.
3. **Quantização de terceiro é artefato próprio:** hash e manifesto da quantização, não só do modelo original — a regra do vault de separar "arquivo quantizado real" de spec ([[02-Modelos/Ficha-padronizada-por-modelo]]).
4. **Re-scan após publicação:** aprovação tem validade (`review_due`); modelo aprovado ontem não é modelo aprovado para sempre.
5. **MCPs e datasets seguem o mesmo fluxo** — dependência é dependência.
6. **Promoção por ambiente:** dev → staging → prod, com avaliação registrada em cada porta ([[10-Operacao-e-Seguranca/Runbook]]: canary, regressão, rollback).

## Manifesto de modelo (por artefato)

```yaml
model_id: laguna-xs-2.1-q4km          # ID interno estável
origem_url: https://exemplo/hub/...    # onde foi obtido
publicador: <organização>
licenca: OpenMDW-1.1                   # verificada no card, com data
revisao: <commit/versão do repositório>
hash_sha256: <digest do arquivo servido>
formato: GGUF
quantizacao: Q4_K_M
tokenizer: <identificação e versão>
ferramenta_quantizacao: <quem/o que produziu o quantizado>
data_aquisicao: 2026-09-01
scanner: <ferramenta e versão usadas no scan>
avaliacoes:                            # funcionais e de segurança, com data
  - <suite>: <resultado, data>
aprovacao: <quem, quando>
ambientes_autorizados: [dev, staging]
review_due: 2026-12-01                 # expiração da aprovação
```

Campos espelham o [[PROTOCOLO-DE-ATUALIZACAO]] (nome exato, versão/commit, licença, formato, quantizações, data, referências) e alimentam `model_id`/`model_hash` do [[10-Operacao-e-Seguranca/Esquema-de-auditoria-LLM]] — a trilha só fecha o ciclo se o hash servido bater com o manifesto aprovado.

## Verificação prática de hash

```powershell
Get-FileHash -Algorithm SHA256 .\modelo.gguf   # Windows
```

```bash
sha256sum modelo.gguf                          # Linux/macOS
```

Comparar com o hash publicado pela fonte **e** registrar o observado no manifesto (fontes nem sempre publicam digest do quantizado; nesse caso o manifesto registra o primeiro hash confiável e a origem exata).

## Papéis

Aquisição e avaliação: **curador de modelos**; aprovação: curador + segurança; operação do registry: **operador**; tudo conforme [[08-Implementacao-Empresa/Matriz-RBAC-e-ABAC]] (separação de funções: quem aprova não opera).

## Estado e pendências

- Nenhum registry interno implantado; modelos locais atuais (ex.: `qwen3.5:4b` da evidência RAG) não têm manifesto retroativo — candidato a primeiro exercício prático.
- Assinatura de artefatos (cosign/sigstore para modelos) documentada como direção, não testada.

## Ver também

- [[10-Operacao-e-Seguranca/Threat-model-LLM-local]] — LLM05 e poisoning.
- [[02-Modelos/Verificacao-PromptQuorum]] — caso real de claims de modelo que não sobreviveram à verificação.
- [[07-Implementacao-Casa/Evidencias/RAG-reproducao-2026-09-01]] — digest de modelo já registrado em evidência (`2a654d98e6fb`).

## Referências

[1]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP LLM05 — Supply chain"
[2]: https://slsa.dev/ "SLSA — níveis de integridade de cadeia de fornecimento"
[3]: https://docs.ollama.com/faq "Ollama — FAQ (OLLAMA_REMOTES e origem dos pulls)"
