# BOMs brasileiras reais

Esta pasta separa BOM de planejamento de BOM cotada. Uma BOM só pode ser marcada como `quoted` quando cada componente possui SKU exato, vendedor, URL, data/hora, UF, preço à vista, frete, impostos incluídos, garantia e condição de estoque.

## Campos mínimos de cotação

| Campo | Regra |
|---|---|
| SKU/MPN | Copiar da página do fabricante ou nota fiscal; não usar apenas o nome comercial. |
| Vendedor | Razão social/CNPJ ou marketplace e vendedor efetivo. |
| Preço | Informar à vista e parcelado separadamente; registrar frete e impostos. |
| Data/hora | Usar ISO 8601 e considerar cotação vencida após alteração de preço/estoque. |
| Evidência | URL e captura/arquivo da cotação, quando permitidos. |
| Compatibilidade | Socket, BIOS, lanes, dimensões, conectores, PSU, refrigeração e SO/runtime. |
| Estado | `draft`, `quoted`, `validated`, `purchased`, `retired`. |

Não preencher preços fictícios. Quando a busca não confirmar preço e SKU, usar `PENDENTE — cotar` e manter a BOM fora da aprovação de compra.
