# AI-Assisted Coding Tools — capítulo completo

## 1. Categorias

| Categoria | Exemplos de uso | Risco principal |
|---|---|---|
| Autocomplete/FIM | Completar linha e função | Sugestão plausível porém errada. |
| Chat no IDE | Explicar, refatorar e gerar testes | Contexto incompleto e vazamento. |
| CLI agent | Navegar no repositório, editar e testar | Execução de comandos perigosos. |
| Code review | Encontrar bugs, segurança e regressões | Falsos negativos e excesso de confiança. |
| RAG de código | Responder sobre APIs e arquitetura internas | ACL, versões e citações erradas. |
| Agente de issue | Implementar tarefa ponta a ponta | Loop, patch amplo e mudança não revisada. |

## 2. Context engineering

Forneça instruções de build, convenções, arquitetura, comandos de teste, limites de diretório e definição de pronto. Prefira contexto selecionado a despejar o repositório inteiro. Use árvore de arquivos, arquivos relevantes, símbolos, diffs e resultados de testes.

## 3. Fluxo seguro

O ciclo recomendado é: entender issue; localizar arquivos; propor plano; pedir aprovação para mudança ampla; aplicar patch pequeno; rodar formatter/lint/testes; revisar diff; gerar resumo e riscos. O agente não deve commitar, fazer push, publicar ou alterar produção sem autorização explícita.

## 4. Ferramentas locais

Aider, Continue e clientes compatíveis com OpenAI podem apontar para Ollama, llama.cpp server ou vLLM. Coding agents com contexto longo precisam de RAM/VRAM e avaliação de tool calling. Modelos FIM podem ser melhores para autocomplete; modelos agentic podem ser melhores para tarefas multi-arquivo, mas custam mais latência.

## 5. Avaliação

Crie tarefas internas anonimizadas e meça: patch aplicável, testes passantes, regressões, tempo até solução, tokens, custo, taxa de intervenção humana, precisão de explicação e vulnerabilidades introduzidas. Inclua tarefas fáceis, médias, legadas, multi-linguagem e com requisitos conflitantes.

## 6. Privacidade e propriedade

Verifique se prompts, código, telemetria e logs permanecem locais. Defina retenção, exclusão, classificação de repositório e política para código proprietário. Licença do modelo, licença do código gerado e política do fornecedor são questões distintas.

## 7. Prompt base

```text
Você trabalha apenas no diretório permitido. Antes de editar, explique o plano.
Não invente APIs: procure no repositório e na documentação disponível.
Depois do patch, rode os testes indicados. Nunca execute comandos fora da allowlist.
Mostre o diff, testes executados, falhas restantes e arquivos alterados.
```

## Referências

[1]: https://aider.chat/ "Aider"
[2]: https://docs.continue.dev/ "Continue"
[3]: https://github.com/ollama/ollama "Ollama"
[4]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP LLM risks"
