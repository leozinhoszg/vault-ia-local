# AGENTS.md — regras do vault

## Objetivo

Manter este vault como base técnica verificável para IA local doméstica e empresarial.

## Regras de edição

Toda nota factual deve informar data de verificação e referências. Diferencie especificação do fabricante, resultado de benchmark próprio, estimativa e opinião editorial. Não transforme preço, compatibilidade ou desempenho em promessa. Use links internos portáveis do Obsidian, nunca caminhos absolutos do computador do autor.

Antes de substituir uma recomendação, preserve o histórico na nota de mudança e atualize o estado em [[MEMORY]]. Não apague uma fonte porque foi superada; marque-a como obsoleta e registre a substituta.

## Notas canônicas

A fonte canônica de quantização é [[05-Memoria-e-Performance/Quantizacao-livro]]; de RAG é [[07-Implementacao-Casa/RAG-livro]]; de fine-tuning é [[06-Treinamento-e-Fine-tuning/Fine-tuning-livro]]. Notas práticas, de deploy e resumos devem apontar para a nota canônica e não contradizê-la. Fichas de modelos seguem [[02-Modelos/Ficha-padronizada-por-modelo]].

## Validação obrigatória

Executar `python3 99-Templates/validate_vault_completo.py` antes de empacotar ou publicar. Erros de links, Python, fórmulas, caminhos absolutos, segredos ou rastros sensíveis bloqueiam a entrega. Avisos de data ou referências devem ser tratados ou justificados no relatório.

## Critérios de revisão

Revisar modelos e runtimes mensalmente; drivers, ROCm/CUDA e preços trimestralmente; governança e segurança a cada mudança relevante ou incidente. Toda nova build precisa de VRAM/RAM, PSU, consumo, banda, compatibilidade e modelos viáveis.
