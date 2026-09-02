# Guia de escolha de modelos por tarefa, máquina e ambiente

**Data-base:** 2026-09-02. Esta nota usa o catálogo do LM Studio consultado na mesma data e deve ser atualizada quando o catálogo mudar. O catálogo distingue modelos disponíveis para download daqueles disponíveis somente no LM Studio Cloud [1].

## 1. Regra de dimensionamento

O modelo mais forte não é automaticamente o melhor modelo para cada atividade. Para uma tarefa curta e repetitiva, um 3B–9B pode entregar menor latência e menor custo energético que um 70B. Modelos maiores devem ser reservados para tarefas que realmente exigem raciocínio, contexto extenso, visão complexa, coding agentic ou maior qualidade de resposta.

A escolha deve cruzar cinco variáveis: tamanho e arquitetura do modelo, quantização e contexto, memória necessária para pesos e KV cache, backend disponível na máquina e requisitos de licença/privacidade. “Baixar” não significa “rodar bem”: um arquivo pode caber no SSD e não caber na VRAM/RAM operacional.

## 2. Matriz prática por atividade

| Atividade | Modelo inicial recomendado | Alternativa de maior qualidade | Máquina pessoal indicada | Máquina empresarial indicada |
|---|---|---|---|---|
| Texto, resumo e classificação | LFM2 1.2B, Ministral 3 3B ou Granite 4.1 3B | Qwen3.5 9B ou Gemma 4 12B | Mac mini M4/M5 Pro 16–32 GB; PC com 16 GB e iGPU/GPU | Mini-PC/desktop com 32 GB; serviço NVIDIA compartilhado |
| Texto em português e multilíngue | Qwen3.5 9B ou mistral-nemo 12B | Qwen3.5 27B ou Granite 4.1 30B | RTX 4090/5090; Mac mini 64 GB; Mac Studio | RTX 5090 ou RTX PRO; servidor vLLM |
| Chat geral e raciocínio | Qwen3 4B ou Gemma 4 5.1B | Qwen3 30B, Gemma 4 26B ou GLM-4.7 30B | RTX 4090/5090; Mac Studio 64–128 GB | RTX 5090/RTX PRO 6000; múltiplos usuários em vLLM |
| Coding assistido simples | Qwen3-Coder-Next 80B MoE/3B ativos ou Qwen3-Coder 30B | Devstral 2 123B, Qwen3-Coder 480B ou modelos 30B/35B | RTX 5090 para 30B; GB10/Mac Studio 128 GB para MoE grande | RTX PRO/multi-GPU ou GB10; validação com repositório privado |
| Coding agentic e tool calling | Qwen3-Coder-Next, Devstral ou GLM-4.7 30B | Devstral 2 ou Laguna S 2.1 118B/8B ativos | RTX 5090 32 GB; Mac Studio 128 GB; GB10 | vLLM/TensorRT-LLM em NVIDIA; isolamento e auditoria |
| RAG com documentos | Granite 4.0 7B/32B, Qwen3.5 9B/27B | Qwen3.6 27B ou Gemma 4 26B | 32–64 GB RAM; GPU opcional | 64–128 GB RAM; GPU NVIDIA para reranking/serving |
| Visão e imagens em documentos | Qwen3-VL 8B ou GLM-4.6V-Flash 9B | Qwen3-VL 30B/32B ou qwen2.5-vl 32B | RTX 4090/5090; Mac Studio com MLX se houver conversão | RTX PRO/servidor NVIDIA, com fila e controle de documentos |
| OCR e extração de PDF | olmOCR 2 7B ou Qwen3-VL 4B/8B | qwen2.5-vl 32B | RTX 3060/4090/5090 ou Mac com 32–64 GB | Serviço dedicado com sandbox, limites e revisão humana |
| Áudio, voz e multimodalidade | Nemotron 3 Omni 30B ou pipeline especializado STT/TTS | Modelo multimodal maior, validado no backend | GPU NVIDIA ou Mac Studio; separar STT/TTS do LLM | Serviços separados por função, com GPU e filas |
| Vídeo: entender, descrever ou consultar vídeo | Qwen3-VL 8B/32B ou Nemotron 3 Omni | pipeline multimodal com extração de frames e áudio | RTX 4090/5090 ou Mac Studio | GPU NVIDIA com processamento assíncrono e armazenamento de objetos |
| Vídeo: gerar vídeo | Wan2.1 1.3B/14B em ComfyUI, não LM Studio | Wan/fluxo mais pesado conforme VRAM | RTX 4090/5090; 24–32 GB VRAM preferível | RTX PRO/multi-GPU e fila de jobs |
| Function calling especializado | FunctionGemma 270M | Granite 4.1 ou Qwen3.5 9B | Qualquer PC moderno; CPU pode bastar | Serviço leve isolado, com schema e testes |
| Classificação de segurança | gpt-oss-safeguard 20B | gpt-oss-safeguard 120B | RTX 4090/5090 ou GB10 | Serviço de moderação separado e auditável |

O termo “vídeo” precisa ser separado. LM Studio é principalmente um catálogo de LLM/VLM; geração de vídeo normalmente usa ComfyUI e modelos de difusão, como Wan2.1, não um modelo GGUF de chat. Para compreensão de vídeo, extrair frames, áudio e metadados e enviar lotes ao VLM costuma ser mais controlável que tentar manter um vídeo inteiro no contexto [9].

## 3. Faixas de memória e modelos

| Memória disponível | Modelos locais razoáveis | Observação |
|---:|---|---|
| 8–16 GB de RAM | 270M–4B quantizados | Boa faixa para resumo, classificação, pequenas automações e edge |
| 16–32 GB | 7B–14B quantizados | Ponto de entrada para chat, RAG e coding básico |
| 32 GB + GPU 12–16 GB | 7B–14B rápidos; alguns 20B–27B com offload | A VRAM define a latência; RAM apoia embeddings e serviços |
| 24–32 GB de VRAM | 14B–27B/32B conforme quantização | Faixa ideal de RTX 4090/5090 para coding e RAG |
| 64–96 GB unificados/VRAM | 30B–70B quantizados; MoE grandes | Contexto e KV cache podem reduzir o tamanho prático |
| 128 GB unificados | 70B–120B e MoE maiores, dependendo do backend | GB10 e Mac Studio; capacidade não implica alto tokens/s |
| 256–512 GB unificados | 120B–480B e modelos enormes, condicionados a quantização | Mac Studio Ultra ou sistemas multi-appliance; validar formato |

Como regra inicial, reservar 1,2–1,5 vezes o tamanho dos pesos quantizados para acomodar runtime, buffers e KV cache. Para contexto extenso ou concorrência, a reserva precisa ser maior. O dimensionamento exato deve usar a fórmula canônica de [[03-Hardware/Calculadora-de-memoria]] e os benchmarks da máquina.

## 4. Ferramentas para baixar e executar

| Ferramenta | Baixa/usa | Melhor cenário | Comando ou fluxo recomendado |
|---|---|---|---|
| LM Studio | GGUF e MLX no catálogo; runtime llama.cpp/MLX | Desktop pessoal, teste, chat e servidor local | Pesquisar por família/quantização, baixar e carregar com contexto conservador |
| `lms get` | Modelos do catálogo LM Studio, com filtro MLX | Automação de download no desktop | `lms get <modelo>`; conferir a sintaxe na versão instalada [2] |
| Hugging Face Hub | Pesos originais, GGUF, MLX, GPTQ/AWQ e cards | Fonte primária e reprodutibilidade | Aceitar licença, baixar snapshot, verificar hash e model card [3] |
| Ollama | Modelos empacotados e tags/Modelfile | Uso simples, API local e Home Assistant | `ollama pull <modelo>`; confirmar tag, quantização e licença [4] |
| llama.cpp | GGUF, CLI e servidor local | Controle de GPU offload, contexto e benchmark | `llama-cli -m modelo.gguf`; usar `llama-server` para API [5] |
| MLX/MLX-LM | Pesos no formato MLX em Apple Silicon | Mac mini/Studio, inferência e fine-tuning Apple | `mlx_lm.generate --model <repo>`; conferir suporte do modelo [6] |
| vLLM | Servidor de inferência NVIDIA/AMD conforme suporte | Produção, batching, OpenAI-compatible API | Instalar versão compatível e apontar para Hugging Face; validar GPU/kernel [7] |
| TensorRT-LLM | Engine otimizada NVIDIA | Produção NVIDIA e baixa latência | Converter/buildar engine conforme GPU e modelo; validar suporte de quantização [8] |
| ComfyUI | Checkpoints e workflows de imagem/vídeo | Geração visual, Wan e difusão | Instalar workflow, baixar cada checkpoint oficial e conferir VRAM [9] |
| ModelScope | Pesos de repositórios que publicam lá | Modelos com distribuição asiática | Usar apenas repositório oficial ou fonte confiável |
| Git LFS/curl/wget | Arquivos publicados pelos autores | Reprodutibilidade e ambientes sem GUI | Baixar URL oficial, registrar commit/hash/licença |
| Bionic | Integração/agente e modelos conforme produto | Coding assistido e fluxo de desenvolvimento | Tratar Bionic como ferramenta/interface, não como formato de pesos; confirmar modelo/backend na documentação vigente |

O download deve ser feito de uma fonte que preserve o **model card**, a licença, a revisão/commit e o hash. Repositórios de quantização de terceiros podem alterar templates, tokenizer ou parâmetros; para ambiente empresarial, preferir os pesos originais ou um fornecedor interno de artefatos.

## 5. Procedimento pessoal

Para uma pessoa em casa, instalar uma única ferramenta principal reduz a fricção. LM Studio é indicado para explorar famílias e comparar quantizações; Ollama é indicado quando a prioridade é ter uma API simples e integrar Home Assistant ou scripts; llama.cpp é indicado quando o usuário precisa controlar offload, contexto e benchmark; MLX-LM é a escolha natural no Apple Silicon quando existe conversão MLX adequada.

Começar pelo modelo mais leve que atende à tarefa. Para texto e resumo, iniciar com 3B–9B. Para coding, iniciar com 9B–30B e só subir para um MoE ou 70B quando o contexto, tool use e qualidade realmente exigirem. Para visão, preferir um VLM 8B antes de um 32B. Para vídeo, separar compreensão de geração e não instalar um modelo de difusão apenas porque o computador executa LLMs.

## 6. Procedimento empresarial

Em empresa, o catálogo deve ser uma **allowlist de modelos aprovados**, com licença, origem, hash, versão, avaliação, classificação de dados, limites de retenção, logs e responsável pela atualização. Um modelo pode ser tecnicamente excelente e juridicamente inadequado para determinado dado ou uso.

A implantação deve separar o plano de download do plano de serving. O download acontece em um repositório controlado, com varredura de dependências e assinatura/hash; o serving ocorre em uma rede isolada, com RBAC, autenticação, limites por usuário, auditoria, backup da configuração, SLO de latência e procedimento de rollback.

Uma empresa deve medir qualidade e operação em vez de comparar apenas parâmetros. O conjunto mínimo inclui taxa de acerto em dataset dourado, groundedness/citações para RAG, taxa de chamadas de ferramenta corretas, latência P50/P95, tokens/s, memória máxima, falhas de contexto e custo de energia. Cada recomendação desta nota deve ser promovida de `candidate` para `approved` somente após esse processo.

## 7. Checklist de seleção

Antes de baixar, confirmar o repositório oficial, licença, tamanho dos arquivos, arquitetura, tokenizer, contexto, formato e compatibilidade do backend. Antes de carregar, verificar memória livre, margem para KV cache, número de camadas a descarregar na GPU e limite de contexto. Depois de carregar, executar um prompt de smoke test, um benchmark de tokens/s e uma avaliação curta de qualidade.

Nunca confundir parâmetros totais com parâmetros ativos em MoE. Um modelo de 120B com 12B ativos pode ter custo de computação menor que um modelo denso de 30B em alguns cenários, mas seus pesos ainda precisam estar armazenados e acessíveis. Também não confundir “modelo disponível em LM Studio Cloud” com “pesos disponíveis para download local”.

## Referências

[1]: https://lmstudio.ai/models "LM Studio — catálogo de modelos e distinção entre download e Cloud"
[2]: https://lmstudio.ai/docs/cli/local-models/get "LM Studio — comando lms get"
[3]: https://huggingface.co/docs/hub/en/models-downloading "Hugging Face — download de modelos"
[4]: https://ollama.com/library "Ollama — biblioteca de modelos"
[5]: https://github.com/ggml-org/llama.cpp "llama.cpp — execução e servidor de GGUF"
[6]: https://github.com/ml-explore/mlx-lm "MLX-LM — inferência e fine-tuning em Apple Silicon"
[7]: https://docs.vllm.ai/en/stable/ "vLLM — documentação oficial"
[8]: https://github.com/NVIDIA/TensorRT-LLM "NVIDIA TensorRT-LLM — engine de inferência"
[9]: https://docs.comfy.org/tutorials/video/wan/wan-video "ComfyUI — workflow Wan2.1 para geração de vídeo"
