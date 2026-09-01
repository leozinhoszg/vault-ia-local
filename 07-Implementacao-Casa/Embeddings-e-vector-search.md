# Embeddings e vector search — capítulo completo

## 1. Representação semântica

Um embedding transforma texto, código, imagem ou áudio em um vetor. A proximidade entre vetores é usada como sinal de relevância semântica. O embedding não é verdade, não é uma citação e não substitui autorização de acesso.

Para vetores normalizados, similaridade cosseno é `cos(a,b) = (a·b)/(||a|| ||b||)`. Distância L2 e produto interno podem produzir rankings equivalentes sob condições específicas, mas o índice e a normalização precisam combinar.

## 2. Pipeline

O pipeline robusto é: coletar documento; preservar origem e ACL; extrair texto; limpar sem destruir estrutura; dividir em chunks; gerar embeddings; inserir no índice; recuperar candidatos; opcionalmente reranquear; montar contexto; gerar resposta; validar citações.

Chunk fixo é um baseline, não uma verdade. Para código, prefira unidade semântica: arquivo, classe, função e janela de linhas. Para contratos, preserve seção, cláusula e página. Overlap reduz cortes, mas aumenta custo e duplicação.

## 3. Índices

| Índice | Característica | Quando usar |
|---|---|---|
| Flat/exato | Compara todos os vetores | Corpus pequeno e baseline. |
| HNSW | Grafo navegável, baixa latência | Busca online geral; exige memória. |
| IVF | Clusters e sondas | Corpus grande e tuning de recall. |
| PQ | Comprime vetores | Escala muito grande; pode perder recall. |
| BM25 | Termos lexicais | Erros, IDs, nomes de função e exatidão. |
| Híbrido | Combina lexical+denso | Documentação técnica e código. |

## 4. Avaliação

Crie perguntas reais com documentos gold. Meça recall@k, precision@k, MRR, nDCG, taxa de citação correta, contexto inútil, latência p95 e custo. Avalie consultas curtas, sinônimos, nomes exatos, versões conflitantes, português/inglês, código e prompt injection.

## 5. Segurança

Filtre por tenant antes ou durante a busca. Não permita que um documento recuperado altere as políticas do sistema. Marque conteúdo como dado não confiável. O retriever deve carregar metadados de fonte, versão, permissão, timestamp e hash.

## 6. Escolha de embedding

Teste modelos multilíngues se o corpus for português/inglês. Meça dimensão, memória, throughput, licença e qualidade no seu domínio. O melhor benchmark público pode não representar nomes de APIs, legislação, código ou documentos internos.

## Exercício

Monte dois índices, um BM25 e um HNSW, para 100 documentos. Compare top-5, combine rankings e avalie dez perguntas. Depois altere o chunking e documente o efeito no recall e na precisão de citação.

*Última atualização: 2026-09-01. Próxima revisão: 2026-10-01.*

## Referências

[1]: https://sbert.net/ "Sentence Transformers"
[2]: https://github.com/facebookresearch/faiss "FAISS"
[3]: https://qdrant.tech/documentation/ "Qdrant"
[4]: https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html "Elasticsearch vector search"
