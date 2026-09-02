# Modelo de nota de controle

- **Data:** 2026-09-01.
- **Uso:** toda recomendação empresarial de segurança que quiser valer como *controle verificável* (cadeia `risco → requisito → configuração → teste → evidência → operação → revisão`) deve seguir este modelo. O frontmatter com `control_id` ativa o schema no `validate_vault_completo.py`; nota sem frontmatter continua sendo nota editorial comum.

## Frontmatter obrigatório

```yaml
---
control_id: IAM-LLM-001          # MAIÚSCULAS e dígitos, segmentos com hífen
status: documented               # documented | configured | tested | verified
applicability:
  - lm-studio
  - ollama
environment:
  - enterprise
risk: critical                   # critical | high | medium | low
owner: platform-security
verified_on: 2026-09-01          # data ISO da última verificação
review_due: 2026-10-01           # o validador avisa quando vencer
evidence_type: manufacturer-specification
---
```

Regras que o validador impõe:

- `status: tested` ou `verified` **exige** `evidence_type: own-test` — spec de fabricante, inferência, estimativa ou opinião editorial nunca sustentam "verificado". Escala honesta: `documented` (lido na doc) → `configured` (config escrita/aplicável) → `tested` (teste executado uma vez, evidência ligada) → `verified` (teste repetível, evidência atual).
- `evidence_type` usa a taxonomia do vault: `manufacturer-specification`, `own-test`, `inference`, `estimate`, `editorial`, `compensating-control`.
- `verified_on` e `review_due` em ISO; `review_due` no passado gera aviso `CONTROL_REVIEW_OVERDUE` (justificável com `<!-- validador: revisao-vencida: motivo -->`).
- Seções de corpo obrigatórias: `## Risco`, `## Configuração`, `## Teste positivo`, `## Teste negativo`, `## Evidência`, `## Rollback`.

## Corpo — as dez perguntas que a nota responde

1. **Risco mitigado** — qual linha do [[10-Operacao-e-Seguranca/Threat-model-LLM-local]] este controle ataca.
2. **Requisito normativo** — de onde vem a obrigação ([[08-Implementacao-Empresa/Seguranca-empresarial-e-LGPD]], NIST AI 600-1, política interna).
3. **Configuração recomendada** — comandos, settings, valores exatos.
4. **Configuração insegura conhecida** — o antipadrão que o teste negativo deve flagrar.
5. **Teste positivo** — como provar que o controle funciona quando aplicado.
6. **Teste negativo** — como provar que a ausência do controle é detectável.
7. **Evidência esperada** — saída, log ou nota em `Evidencias/` com data.
8. **Procedimento de rollback** — como desfazer sem quebrar o serviço.
9. **Limitações por versão** — a partir de qual versão vale; o que muda antes/depois.
10. **Referências e data de verificação** — fontes primárias, sempre.

## Esqueleto

```markdown
## Risco
## Requisito
## Configuração recomendada
## Configuração insegura conhecida
## Teste positivo
## Teste negativo
## Evidência
## Rollback
## Limitações por versão
## Referências
```

## Ver também

- [[10-Operacao-e-Seguranca/Threat-model-LLM-local]] — o catálogo de riscos que os controles citam.
- [[99-Templates/Modelo-de-ficha-de-workstation]] — o equivalente para hardware.

## Referências

[1]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 LLM — vocabulário de risco usado nos control_id"
