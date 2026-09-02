from pathlib import Path
import csv
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
models = [
    ("LFM2", 1.2, "Texto", 0),
    ("Granite 4.1", 8, "Texto/RAG", 0),
    ("Qwen3.5", 9, "Texto", 0),
    ("Qwen3-Coder", 30, "Coding", 0),
    ("Gemma 4", 31, "Texto/RAG", 0),
    ("Qwen3-Coder-Next", 80, "Coding MoE", 3),
    ("Laguna S 2.1", 118, "Coding MoE", 8),
    ("qwen2.5-vl", 72, "Visão", 72),
]
# Q4 é uma aproximação de planejamento; inclui overhead de runtime e KV cache curto.
def memory_gib(total_b):
    return total_b * 0.55 + 3.5

platforms = {
    "RTX 5090 32 GB": {"bandwidth": 1792, "eff": 0.55, "capacity": 32, "offload_factor": 0.18},
    "GB10 128 GB": {"bandwidth": 273, "eff": 0.70, "capacity": 128, "offload_factor": 0.75},
    "Mac Studio M5 Max 128 GB": {"bandwidth": 460, "eff": 0.60, "capacity": 128, "offload_factor": 0.65},
    "Mac mini M5 Pro 64 GB": {"bandwidth": 307, "eff": 0.50, "capacity": 64, "offload_factor": 0.45},
}

def tok_s(memory, p):
    raw = p["bandwidth"] * p["eff"] / memory
    if memory > p["capacity"]:
        raw *= p["offload_factor"]
    return raw

rows = []
for name, total, task, active in models:
    mem = memory_gib(total)
    for platform, p in platforms.items():
        rows.append({
            "modelo": name,
            "tarefa": task,
            "parametros_totais_B": total,
            "parametros_ativos_B": active or total,
            "memoria_pesos_q4_GiB": round(mem, 2),
            "plataforma": platform,
            "memoria_acelerador_GiB": p["capacity"],
            "tokens_s_estimados": round(tok_s(mem, p), 1),
            "modo": "offload" if mem > p["capacity"] else "acelerador/memoria_unificada",
        })

csv_path = OUT / "modelos-tarefa-memoria-desempenho-estimado.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

# Plot 1: memória requerida versus capacidade das plataformas.
labels = [m[0] for m in models]
mem = [memory_gib(m[1]) for m in models]
fig, axes = plt.subplots(2, 1, figsize=(14, 10), constrained_layout=True)
colors = ["#4C78A8" if x <= 32 else "#F58518" if x <= 64 else "#E45756" for x in mem]
axes[0].bar(labels, mem, color=colors)
axes[0].axhline(32, color="#222222", linestyle="--", linewidth=1, label="32 GiB VRAM — RTX 5090")
axes[0].axhline(64, color="#666666", linestyle=":", linewidth=1, label="64 GiB — Mac mini M5 Pro")
axes[0].axhline(128, color="#000000", linestyle="-.", linewidth=1, label="128 GiB — GB10/Mac Studio")
axes[0].set_ylabel("Memória estimada dos pesos + overhead (GiB)")
axes[0].set_title("Modelos do guia: memória necessária em Q4")
axes[0].tick_params(axis="x", rotation=25)
axes[0].legend(loc="upper left", fontsize=8)
for i, value in enumerate(mem):
    axes[0].text(i, value + 1, f"{value:.1f}", ha="center", fontsize=8)

for platform, p in platforms.items():
    vals = [tok_s(memory_gib(m[1]), p) for m in models]
    axes[1].plot(labels, vals, marker="o", linewidth=2, label=platform)
axes[1].set_ylabel("Tokens/s estimados (decode)")
axes[1].set_title("Desempenho estimado por banda de memória; offload indicado quando necessário")
axes[1].tick_params(axis="x", rotation=25)
axes[1].grid(axis="y", alpha=0.25)
axes[1].legend(fontsize=8, ncol=2)
fig.text(0.01, 0.01, "Estimativa de planejamento, não benchmark medido. Q4 ≈ 0,55 bytes/parâmetro + 3,5 GiB; contexto curto e uma sessão. MoE usa parâmetros totais para memória.", fontsize=8)
fig.savefig(OUT / "grafico-modelos-tarefa-memoria-desempenho.png", dpi=180)
plt.close(fig)
print(csv_path)
print(OUT / "grafico-modelos-tarefa-memoria-desempenho.png")
