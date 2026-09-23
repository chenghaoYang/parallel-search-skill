#!/usr/bin/env python3
"""Progress plot and summary for the self-evolution loop.

Adapted from upstream/analysis.ipynb (karpathy/autoresearch). Differences: the metric is a pairwise
score vs the incumbent of the moment (higher is better) rather than an absolute val_bpb, so the
"running best" line uses anchor.tsv (each kept version judged against the fixed baseline) when present.

usage: uv run --with pandas --with matplotlib python evolve/analysis.py
"""

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent

df = pd.read_csv(ROOT / "results.tsv", sep="\t")
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["status"] = df["status"].str.strip().str.upper()
print(f"Total experiments: {len(df)}")
counts = df["status"].value_counts()
print("Experiment outcomes:")
print(counts.to_string())
n_keep, n_discard = counts.get("KEEP", 0), counts.get("DISCARD", 0)
if n_keep + n_discard:
    print(f"\nKeep rate: {n_keep}/{n_keep + n_discard} = {n_keep / (n_keep + n_discard):.1%}")

kept = df[df["status"] == "KEEP"]
print(f"\nKEPT experiments ({len(kept)} total):")
for _, row in kept.iterrows():
    print(f"  {row['exp']:>6}  score={row['score']:+.3f}  golden={row['golden']}  {row['description']}")

fig, axes = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={"height_ratios": [3, 2]})
ax = axes[0]
trial = df[df["status"].isin(["KEEP", "DISCARD", "CRASH"])].reset_index(drop=True)
colors = {"KEEP": "#2ecc71", "DISCARD": "#cccccc", "CRASH": "#e74c3c"}
for status, group in trial.groupby("status"):
    ax.scatter(group.index, group["score"].fillna(-2), c=colors[status], s=50 if status == "KEEP" else 16,
               edgecolors="black" if status == "KEEP" else "none", linewidths=0.5, zorder=3, label=status.title())
for idx, row in trial[trial["status"] == "KEEP"].iterrows():
    desc = str(row["description"]).strip()
    ax.annotate(desc[:42] + ("..." if len(desc) > 42 else ""), (idx, row["score"]), textcoords="offset points",
                xytext=(6, 6), fontsize=8, color="#1a7a3a", rotation=30, ha="left", va="bottom")
ax.axhline(0, color="#888", linewidth=0.8)
ax.set_xlabel("Experiment #")
ax.set_ylabel("Pairwise score vs incumbent (higher is better)")
ax.set_title(f"deep-search autoresearch: {len(trial)} experiments, {n_keep} kept")
ax.legend(loc="upper right", fontsize=9)
ax.grid(True, alpha=0.2)

ax = axes[1]
anchor = ROOT / "anchor.tsv"
if anchor.exists():
    an = pd.read_csv(anchor, sep="\t")
    ax.step(range(len(an)), an["score_vs_base"], where="post", color="#27ae60", linewidth=2)
    ax.scatter(range(len(an)), an["score_vs_base"], c="#27ae60", s=40, zorder=3)
    for i, row in an.iterrows():
        ax.annotate(row["exp"], (i, row["score_vs_base"]), textcoords="offset points", xytext=(4, 4), fontsize=8)
    ax.set_ylabel("Kept version vs baseline v1.1")
else:
    ax.text(0.5, 0.5, "anchor.tsv not written yet", ha="center", va="center", transform=ax.transAxes)
ax.axhline(0, color="#888", linewidth=0.8)
ax.set_xlabel("Kept version #")
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig(ROOT / "progress.png", dpi=150, bbox_inches="tight")
print(f"\nSaved to {ROOT / 'progress.png'}")
