# Voz, visão e geração local

## Voz

STT converte áudio em texto; TTS converte texto em voz. Um pipeline local típico é Whisper ou modelo STT compatível, LLM local e Piper/Coqui ou outro TTS. Separe microfone, diarização, transcrição, inferência e reprodução para diagnosticar latência.

## Visão

VLMs adicionam encoder visual e projetor ao LLM. Imagens grandes, múltiplas imagens e vídeo aumentam tokens visuais e memória. Use OCR especializado para documentos quando isso for mais confiável e entregue trechos estruturados ao LLM.

## Geração de imagem

Stable Diffusion/Flux e similares têm requisitos diferentes de VRAM, atenção e quantização. Separe o ambiente de imagem do ambiente de LLM quando drivers ou versões de PyTorch entrarem em conflito. Para 8–12 GB, use resoluções e modelos compatíveis; para workflows maiores, 16–24 GB oferece mais margem.

## Home Assistant

Coloque o assistente local atrás de rede interna, autenticação e allowlist. Ações como abrir portas, comprar ou desligar alarmes exigem confirmação. Mantenha STT/TTS e LLM desacoplados e registre somente o necessário.

## Agentes e assistentes de código

Use sandbox, diretório de trabalho limitado, ferramentas permitidas, timeouts, revisão de diff e execução de testes. Um modelo bom em chat pode ser ruim em tool calling; avalie loops completos. Continue.dev, Aider e clientes compatíveis com API local podem consumir Ollama, llama.cpp ou vLLM conforme protocolo.
