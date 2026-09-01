# Fine-tuning completo

## Ambiente

Use Linux ou WSL2 quando o stack CUDA/ROCm exigir. Fixe Python, PyTorch, Transformers, PEFT, TRL, bitsandbytes/Unsloth e o driver. Comece com 8–14B QLoRA; fine-tuning completo de 27B/70B é um projeto multi-GPU.

```bash
python -m venv .venv && source .venv/bin/activate
pip install torch transformers datasets peft trl accelerate bitsandbytes
accelerate config
```

## Dataset

Formato JSONL recomendado:

```json
{"messages":[{"role":"user","content":"Corrija a função."},{"role":"assistant","content":"Aqui está a correção..."}]}
```

Faça deduplicação, remoção de segredos/PII, validação de licença, split por projeto e conjunto de teste congelado. Não treine sobre a validação.

## Script mínimo

```python
# treino_qlora.py
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig
from trl import SFTTrainer
import torch
base='Qwen/Qwen3.6-27B'
tok=AutoTokenizer.from_pretrained(base)
q=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=torch.bfloat16)
model=AutoModelForCausalLM.from_pretrained(base,quantization_config=q,device_map='auto')
ds=load_dataset('json',data_files={'train':'train.jsonl','validation':'valid.jsonl'})
args=TrainingArguments(output_dir='out',num_train_epochs=2,per_device_train_batch_size=1,gradient_accumulation_steps=16,learning_rate=2e-4,logging_steps=10,eval_strategy='steps',eval_steps=100,save_steps=100,bf16=True,gradient_checkpointing=True)
trainer=SFTTrainer(model=model,tokenizer=tok,train_dataset=ds['train'],eval_dataset=ds['validation'],peft_config=LoraConfig(r=16,lora_alpha=32,lora_dropout=0.05,target_modules='all-linear',task_type='CAUSAL_LM'),args=args)
trainer.train(); trainer.save_model('out/adapter'); tok.save_pretrained('out/adapter')
```

Confirme a assinatura da versão instalada de TRL, pois APIs mudam. Para GPUs sem BF16, use FP16 e valide estabilidade. Ajuste batch efetivo, gradient accumulation, sequence length e checkpointing conforme memória.

## Estimativa de memória

QLoRA economiza memória dos pesos, mas ainda precisa de ativações, gradientes dos adapters, estados do otimizador e sequência. Sequence length é frequentemente o maior multiplicador. Use batch 1, gradient accumulation, packing controlado e checkpointing no início. Monitore pico, não média.

## Checkpoint, merge e exportação

Mantenha o modelo base imutável, adapter, tokenizer, configuração, logs, dataset card e hash. Avalie adapter separado antes do merge. Para merge em FP16/BF16, reserve espaço para uma cópia adicional do modelo. Depois converta para GGUF com a ferramenta oficial do llama.cpp e quantize em uma cópia; não destrua o checkpoint mestre.

```bash
# Exemplos conceituais; confira a versão do llama.cpp
python convert_hf_to_gguf.py out/merged --outfile out/model-f16.gguf --outtype f16
./llama-quantize out/model-f16.gguf out/model-Q4_K_M.gguf Q4_K_M
```

## Avaliação

Compare base, adapter, merged e GGUF quantizado em prompts de coding, regressão geral, segurança, formato e conjunto não visto. Publique a diferença de qualidade, memória e latência; se houver regressão, faça rollback.

**Referências**

[1]: https://arxiv.org/abs/2305.14314 "QLoRA"
[2]: https://huggingface.co/docs/peft/index "PEFT"
[3]: https://huggingface.co/docs/trl/index "TRL"
[4]: https://github.com/unslothai/unsloth "Unsloth"
[5]: https://github.com/ggml-org/llama.cpp "Conversão e quantização GGUF"
