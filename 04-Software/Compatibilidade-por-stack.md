# Compatibilidade por stack

Compatibilidade significa mais que “o driver instalou”. Confirme GPU, arquitetura, SO, kernel, versão do toolkit, versão do runtime, formato do modelo, operadores e caminho de fallback.

| Stack | Melhor cenário | Windows | WSL2 | Linux | Cuidados |
|---|---|---|---|---|---|
| CUDA | NVIDIA; maior cobertura de LLM e kernels | Excelente | Excelente para workloads suportados | Excelente | Driver, CUDA, PyTorch e container devem ser compatíveis. |
| ROCm/HIP | AMD Radeon/Instinct | Suporte seletivo e versão-dependente | Verifique matriz e suporte específico | Melhor cobertura, mas não universal | GPU, SO, kernel, firmware e ROCm precisam formar combinação suportada. |
| Metal | Apple Silicon | Não aplicável | Não aplicável | Não aplicável | Memória unificada; use llama.cpp/MLX e confira conversão. |
| Vulkan | GPU multiplataforma | Bom para apps compatíveis | Possível, depende do passthrough | Bom | Pode ser fallback; desempenho e operadores variam. |
| OpenVINO | Intel CPU/GPU/NPU | Suportado conforme matriz | Depende da integração | Suportado conforme matriz | Converta e valide operadores; fallback pode ir para CPU. |
| CPU/BLAS/NEON/AVX | Universal | Bom | Bom | Bom | Mais portátil, porém geralmente mais lento no decode. |

## AMD: procedimento obrigatório

A matriz oficial do ROCm 10.0.0 relaciona GPU, distribuição Linux, Windows/WSL2, driver de kernel e firmware. Não presuma que toda Radeon funciona com todo ROCm. Registre o modelo exato, `gfx` target, versão do kernel, versão do ROCm e método de instalação [1].

```bash
rocminfo | head -100
clinfo | head -80
uname -a
python -c "import torch; print(torch.__version__, torch.version.hip, torch.cuda.is_available())"
```

No Windows, valide primeiro a matriz AMD e o caminho oficial para a versão do ROCm. No WSL2, valide também versão do Windows, kernel WSL, driver do host e acesso ao dispositivo. Se o runtime usar fallback CPU sem avisar, a aplicação pode parecer funcional e ficar inviável.

## Checklist de produção

Fixe imagem Docker, driver, toolkit, runtime, modelo, quantização e commit. Rode smoke test de geração, multimodalidade, tool calling e structured output. Meça memória e velocidade no mesmo SO que será usado em produção.

*Última atualização: 2026-09-01. Próxima revisão: 2026-12-01.*

## Referências

[1]: https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html "AMD ROCm 10.0.0 compatibility matrix"
[2]: https://docs.nvidia.com/cuda/ "NVIDIA CUDA documentation"
[3]: https://github.com/ggml-org/llama.cpp "llama.cpp backends"
[4]: https://www.intel.com/content/www/us/en/developer/tools/openvino-toolkit/overview.html "Intel OpenVINO"
