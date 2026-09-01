# Implementação doméstica com Ollama

## Objetivo

Ter um assistente local acessível por CLI e API, sem expor a porta à internet.

## Passo a passo

1. Use Linux, macOS ou Windows atualizado, reserve espaço em SSD e confirme RAM/VRAM.
2. Instale o Ollama pelo instalador oficial; não use scripts de origem desconhecida.
3. Baixe um modelo compatível com o hardware e confira licença/model card.
4. Execute um teste local:

```bash
ollama run qwen3.5:4b
curl http://localhost:11434/api/generate -d '{"model":"qwen3.5:4b","prompt":"Explique memória de GPU em três frases","stream":false}'
```

5. Meça qualidade, latência, memória e temperatura.
6. Para documentos, siga [[07-Implementacao-Casa/02-RAG-local]].
7. Faça backup dos Modelfiles, prompts, avaliações e hashes; os pesos podem ser baixados novamente.
8. Não faça port-forward da API sem autenticação, TLS, rate limit e firewall.

## Alternativa explícita

Use llama.cpp quando precisar de GGUF, controle fino de offload, CPU+GPU híbrido ou suporte a arquiteturas específicas. Consulte [[04-Software/Runtimes]].

*Última atualização: 2026-09-01. Próxima revisão: 2026-10-01.*

## Referências

[1]: https://github.com/ollama/ollama "Ollama — instalação oficial e Modelfile"
[2]: https://github.com/ollama/ollama/blob/main/docs/api.md "Ollama — API REST (/api/generate, /api/chat)"
[3]: https://github.com/ggml-org/llama.cpp "llama.cpp — alternativa com GGUF e offload fino"
