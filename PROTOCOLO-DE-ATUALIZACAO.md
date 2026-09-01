# Protocolo de atualização

## Ao adicionar um modelo

Registrar nome exato, versão/commit, organização, parâmetros totais/ativos, contexto nativo, modalidade, licença, formato, quantizações, runtimes suportados, data e referências primárias. Atualizar catálogo, sizing e estado de revisão.

## Ao adicionar hardware

Registrar VRAM/RAM, tipo e banda de memória, consumo, conectores, linhas PCIe, compatibilidade de driver, preço em reais com data, garantia e modelos testados. Separar preço observado de faixa estimada.

## Ao atualizar software

Registrar SO, kernel, driver, toolkit, runtime, versão do modelo e resultado de smoke test. Para AMD, anexar a matriz ROCm consultada.

## Ao atualizar uma recomendação

Criar uma entrada em `MEMORY.md` ou nota de changelog com data, autor, motivo, fontes e impacto. Rodar o validador de links antes de compactar o vault.
