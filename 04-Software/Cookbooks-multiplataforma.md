# Cookbooks multiplataforma

## Contrato de teste

Cada cookbook deve registrar data, hardware, sistema operacional, kernel, driver, toolkit, runtime, modelo, quantização, contexto, prompt, tokens/s, TTFT, memória e resultado. Os comandos abaixo são **receitas reproduzíveis**; a execução depende do equipamento e da versão instalada. O status desta nota é: **comandos revisados estaticamente; smoke tests de hardware devem ser executados no host-alvo**.

## Windows nativo — NVIDIA

Instale driver Studio/Game Ready atual, Git, Python e Ollama ou LM Studio. Valide:

```powershell
nvidia-smi
ollama run qwen3.6:27b
ollama ps
```

Para PyTorch, instale o wheel CUDA recomendado pela página oficial da versão, confirme `torch.cuda.is_available()` e rode um prompt curto. Windows nativo é simples para desktop; Docker e alguns servidores Linux podem ser mais previsíveis em WSL2.

## WSL2 — NVIDIA

Atualize Windows e WSL, instale o driver NVIDIA no host e não instale um driver Linux conflitante dentro do WSL. Valide:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

Compare o mesmo modelo com Windows nativo. Registre acesso a filesystem: o código dentro do filesystem Linux costuma evitar parte da penalidade de `/mnt/c`.

## Linux — NVIDIA/CUDA

Fixe Ubuntu, kernel, driver, CUDA/PyTorch e container. Valide `nvidia-smi`, memória livre, persistência e P2P. Para serving, use vLLM/SGLang quando o modelo suportar. Rode benchmark com contexto curto, longo e concorrência.

## Linux — AMD/ROCm

Consulte a matriz oficial antes de instalar: GPU, `gfx` target, distribuição, kernel, firmware e versão ROCm precisam combinar. Valide:

```bash
rocminfo | head -100
rocm-smi
python -c "import torch; print(torch.version.hip, torch.cuda.is_available())"
```

Não trate “PyTorch instalou” como prova de aceleração. Confirme uso da GPU, VRAM, kernels e tokens/s. WSL2 e Windows possuem combinações mais restritas; Linux é geralmente o primeiro caminho a testar.

## macOS — Apple Silicon

Use Metal/MLX/llama.cpp/Ollama. Valide memória e backend:

```bash
system_profiler SPHardwareDataType
ollama run qwen3.6:27b
ollama ps
```

Não há CUDA/ROCm nativos. A memória é unificada; deixe margem para macOS, aplicações, embeddings e KV cache. Para treino, confirme suporte específico do MLX ou PyTorch MPS.

## Matriz de aceitação

| Teste | Passa quando |
|---|---|
| Modelo carrega | Processo inicia sem swap/OOM e memória fica abaixo do limite. |
| Aceleração ativa | Backend reporta GPU/Metal/ROCm, não apenas CPU. |
| Geração | Resposta termina e JSON/tool call é válido. |
| Performance | TTFT e tokens/s atingem o SLO definido. |
| Estabilidade | 30–60 minutos sem crash, throttling ou crescimento de memória. |
| Regressão | Resultado não piora no dataset dourado. |

## Referências

[1]: https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html "ROCm compatibility matrix"
[2]: https://docs.nvidia.com/cuda/ "CUDA documentation"
[3]: https://github.com/ml-explore/mlx "MLX"
[4]: https://github.com/ggml-org/llama.cpp "llama.cpp"
