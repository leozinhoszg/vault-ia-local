> **Nota canônica:** conceitos, arquitetura e critérios aprofundados estão em [[07-Implementacao-Casa/RAG-livro]]. Esta nota mantém o roteiro resumido e aponta para o protótipo em [[07-Implementacao-Casa/RAG-local-executavel.py]].

# RAG local

RAG recupera trechos relevantes de uma coleção local e os entrega ao LLM no prompt. O pipeline é: ingestão, extração, chunking, embedding, índice vetorial, recuperação, reranking opcional, geração com citações e avaliação.

## Passos

1. Extraia texto preservando título, página, origem e data.
2. Divida por unidade semântica; teste chunk size e overlap.
3. Gere embeddings localmente. Para laboratório pequeno, uma matriz efêmera em memória reduz estado stale; para produção, escolha e opere explicitamente um índice persistente com lifecycle, ACL, backup e tombstone.
4. Recupere top-k, filtre por metadados e rerankeie quando necessário.
5. Instrua o modelo a responder somente com evidência recuperada e declarar ausência.
6. Mostre ao usuário as fontes e mantenha ACLs também no índice.
7. Avalie recall@k, precisão de citações, groundedness e latência.

RAG não torna o modelo automaticamente correto: documentos ruins, recuperação inadequada e prompt injection em arquivos continuam sendo riscos.

O protótipo deste vault usa retrieval cosine exato em memória, não banco vetorial. Ele recusa PDF por padrão e contém volume, endpoint Ollama e metadados de fonte; consulte [[07-Implementacao-Casa/03-RAG-deploy]] antes de executar. Essa implementação é uma referência educacional, não uma arquitetura empresarial pronta.

*Última atualização: 2026-09-01. Próxima revisão: 2026-10-01.*
