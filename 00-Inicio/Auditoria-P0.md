# Auditoria P0 — verificação das correções

<!-- validador: sem-referencias: relatório interno; as evidências (células, comandos, versões) estão citadas inline e as fontes externas ficam nas notas auditadas -->

**Data da auditoria:** 1º de setembro de 2026. **Revisão:** 2 (a revisão 1 do mesmo dia declarou o break-even reconciliado; a re-auditoria encontrou um erro de câmbio na planilha, corrigido nesta revisão). **Resultado:** aprovado com ressalvas não bloqueantes, listadas em "Pendências abertas".

| Item | Verificação | Resultado |
|---|---|---|
| Rastros de prompt | Varredura textual e revisão dos finais das três notas indicadas. | Corrigido; blocos após referências removidos. O validador não encontrou trace ou segredo nesta execução. |
| RAG executável | `ast.parse` do script; execução de `--selftest` em Windows 11, Python 3.11.9, chromadb 1.0.20, pypdf 6.0.0. | Corrigido. O selftest cobre chunking, Chroma, recuperação e formato de citação com embedding determinístico; **não** cobre embedding real nem geração via Ollama. Detalhe em [[04-Software/Estado-de-testes-cookbooks]]. |
| GB/GiB | Fórmula revisada para `/1e9` em GB decimal e `/2^30` em GiB binário. | Corrigido; exemplos recalculados, incluindo 27B Q4. |
| TCO API | Texto e planilha usam 100M input, 20M cached e 25M output, câmbio R$5,50. | Reconciliado: Sol R$4.994, Terra R$2.772, Luna R$277,20. |
| TCO local | Componentes separados entre CAPEX, energia, refrigeração, manutenção e operação. | Reconciliado em R$1.768,50/mês para as premissas atuais. |
| Break-even | Revisão 1: `Break_even!E2:E4` dividia o TCO em BRL por um custo blended em USD, o que produziria 282,41M, 508,79M e 5.087,93M. Revisão 2: fórmula reescrita como `TCO local ÷ (custo API BRL ÷ tokens totais)`, com o blended em BRL exposto em `Break_even!H2:H4`. | Reconciliado após correção: 51,35M, 92,51M e 925,08M tokens/mês para Sol, Terra e Luna, verificados por recomputação independente em Python. |
| Valor residual | `Local!C2` usava apenas `CAPEX / vida útil`. | Corrigido: `(CAPEX − valor residual) / vida útil`. Com residual zero o resultado não muda. |
| Batch API | O fator existia em `Premissas!B20` mas não participava de nenhum cálculo. | Corrigido: `API_OpenAI!G` e `Break_even!G` mostram custo e break-even com Batch (fator aplicado ao custo inteiro; ver limitação). |
| Contexto longo | Um único fator era aplicado a entrada, cache e saída. | Corrigido: fatores separados em `Premissas!B21`, `B23` e `B24`, todos com valor 1 até confirmação do preço aplicável. |
| Sensibilidade | Somente câmbio, e sem os fatores de contexto longo e cache writes. | Corrigido: o bloco de câmbio agora deriva de `API_OpenAI!E` (inclui todos os fatores) e foram adicionados blocos de vida útil, utilização e tarifa de energia. |
| Preços | Data de consulta, Batch, contexto longo e cache writes são premissas editáveis. | Mantido com ressalva: revalidar preços e contrato antes de uso. |

## Método de verificação do break-even

As fórmulas foram lidas com `openpyxl`, todas as referências de célula foram checadas contra células não vazias e os valores esperados foram recomputados fora da planilha com as mesmas premissas. A planilha é salva sem valores em cache, portanto o recálculo no Excel/LibreOffice na abertura é o teste final de aceitação.

## Pendências abertas

- A planilha não implementa a anuidade com taxa de desconto descrita na seção 3 do [[09-Servicos-e-Custos/Guia-financeiro-TCO-local-vs-OpenAI]]; a amortização é linear.
- O fator Batch é aplicado a 100% do custo; cargas parcialmente elegíveis exigem uma premissa de percentual.
- O smoke test funcional completo do RAG (embedding real + Ollama + resposta com `[Fonte N]`) continua pendente de uma máquina com Ollama.
- Preços da API são premissas datadas e devem ser reconsultados na data da decisão.

## Limites da aprovação

A aprovação significa que a consistência editorial, matemática e estrutural foi corrigida e verificada pelos métodos acima. Não significa que a API foi faturada em produção, que os preços permanecerão vigentes ou que o modelo local entrega a mesma qualidade. O próximo teste de aceitação deve executar o cookbook em cada plataforma-alvo e comparar a fatura real com a planilha.
