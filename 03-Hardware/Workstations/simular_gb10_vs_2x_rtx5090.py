#!/usr/bin/env python3
"""Simulação de teto de decode por tráfego de pesos: Dell GB10 vs 2x RTX 5090.

Isto não é benchmark. O modelo calcula um envelope bandwidth-bound e aplica
fatores de eficiência editáveis para representar overhead de kernels, cópia,
KV cache, sincronização tensor-parallel e utilização realista.
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent

SYSTEMS = {
    "Dell Pro Max GB10": {
        "bandwidth_gbs": 273.0,
        "bandwidth_efficiency": 0.70,
        "power_w": 280.0,
        "memory_gb": 128.0,
        "notes": "sistema completo/adaptador; memória unificada",
    },
    "2x RTX 5090": {
        "bandwidth_gbs": 2 * 1792.0,
        "bandwidth_efficiency": 0.62,
        "power_w": 2 * 575.0 + 250.0,
        "memory_gb": 64.0,
        "notes": "GPU TGP agregado + 250 W estimados para CPU/placa/SSD/ventoinhas",
    },
}

MODELS = [
    {
        "model": "Qwen3.6-27B Q4",
        "weight_gb": 17.5,
        "bytes_streamed_gb": 17.5,
        "context": "denso; pesos atravessados por token",
    },
    {
        "model": "Llama 3.1 70B Q4",
        "weight_gb": 42.0,
        "bytes_streamed_gb": 42.0,
        "context": "denso; pesos atravessados por token",
    },
    {
        "model": "Qwen3-Coder-Next 80B/3B Q4",
        "weight_gb": 45.0,
        "bytes_streamed_gb": 6.0,
        "context": "MoE; aproximação de pesos compartilhados + experts ativos",
    },
]


def simulate() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for model in MODELS:
        for name, system in SYSTEMS.items():
            fits = model["weight_gb"] <= system["memory_gb"]
            roofline = system["bandwidth_gbs"] / model["bytes_streamed_gb"]
            estimated = roofline * system["bandwidth_efficiency"] if fits else 0.0
            rows.append(
                {
                    "system": name,
                    "model": model["model"],
                    "weight_gb": model["weight_gb"],
                    "bytes_streamed_gb_per_token": model["bytes_streamed_gb"],
                    "memory_gb": system["memory_gb"],
                    "fits": fits,
                    "bandwidth_gbs": system["bandwidth_gbs"],
                    "efficiency": system["bandwidth_efficiency"],
                    "roofline_tok_s": roofline if fits else 0.0,
                    "estimated_tok_s": estimated,
                    "power_w": system["power_w"],
                    "estimated_tok_s_per_w": estimated / system["power_w"] if fits else 0.0,
                    "context": model["context"],
                    "notes": system["notes"],
                }
            )
    return rows


def main() -> None:
    rows = simulate()
    csv_path = OUT / "simulacao-gb10-vs-2x-rtx5090.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    labels = [m["model"] for m in MODELS]
    fig, ax = plt.subplots(figsize=(10, 5.8))
    x = list(range(len(labels)))
    width = 0.36
    for i, name in enumerate(SYSTEMS):
        values = [r["estimated_tok_s"] for r in rows if r["system"] == name]
        offset = (i - 0.5) * width
        bars = ax.bar([v + offset for v in x], values, width, label=name)
        ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=8)
    ax.set_xticks(x, labels, rotation=12, ha="right")
    ax.set_ylabel("tokens/s estimados — envelope bandwidth-bound")
    ax.set_title("Simulação de decode: Dell Pro Max GB10 vs 2× RTX 5090")
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "grafico-simulacao-gb10-vs-2x-rtx5090.png", dpi=180)
    plt.close(fig)

    print(csv_path)
    print(OUT / "grafico-simulacao-gb10-vs-2x-rtx5090.png")
    for row in rows:
        print(f"{row['system']} | {row['model']} | {row['estimated_tok_s']:.2f} tok/s | {row['estimated_tok_s_per_w']:.4f} tok/s/W | fits={row['fits']}")


if __name__ == "__main__":
    main()
