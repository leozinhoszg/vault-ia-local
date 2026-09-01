# Auditoria P0 — verificação das correções

**Data da auditoria:** 1º de setembro de 2026. **Resultado:** aprovado com ressalvas editoriais não bloqueantes.

| Item | Verificação | Resultado |
|---|---|---|
| Rastros de prompt | Varredura textual e revisão dos finais das três notas indicadas. | Corrigido; blocos após referências removidos. Validador não detecta trace ou segredo. |
| RAG executável | `ast.parse` do script, revisão das strings e documentação de dependências/comando. | Corrigido; o script compila. O smoke test funcional ainda depende de instalar `pypdf`, `chromadb`, `sentence-transformers` e executar Ollama. |
| GB/GiB | Fórmula revisada para `/1e9` em GB decimal e `/2^30` em GiB binário. | Corrigido; exemplos recalculados, incluindo 27B Q4. |
| TCO API | Texto e planilha usam 100M input, 20M cached e 25M output, câmbio R$5,50. | Reconciliado: Sol R$4.994, Terra R$2.772, Luna R$277,20. |
| TCO local | Componentes separados entre CAPEX, energia, refrigeração, manutenção e operação. | Reconciliado em R$1.768,50/mês para as premissas atuais. |
| Break-even | Fórmula usa custo efetivo por token considerando a proporção do mix, não apenas preço de entrada. | Reconciliado: aproximadamente 51,4M, 92,5M e 925M tokens/mês para Sol, Terra e Luna. |
| Preços | Data de consulta, Batch, contexto longo e cache writes foram adicionados como premissas editáveis. | Corrigido com ressalva: revalidar preços e contrato antes de uso. |

## Limites da aprovação

A aprovação significa que a consistência editorial, matemática e estrutural foi corrigida. Não significa que o RAG foi executado neste sandbox, que a API foi faturada em produção ou que os preços permanecerão vigentes. O próximo teste de aceitação deve executar o cookbook em cada plataforma-alvo e comparar a fatura real com a planilha.
