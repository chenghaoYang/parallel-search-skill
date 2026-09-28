#!/usr/bin/env python3
"""Blind LLM judge over arm reports.

usage: judge.py ARM_ID [ARM_ID ...] [--passes 2] [--judge claude|grok] [--model MODEL] [--out NAME]

Each pass copies task.md + the reports, anonymized and shuffled with a per-pass seed, into a
fresh dir and runs a headless judge with file tools only (no web): `claude -p` (default model
opus) or Grok Build (default grok-4.7; a second model family to check self-preference bias).
Scores are mapped back to arms and averaged over passes into judge/<out or judge>/summary.json.
"""

import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from run_arm import GROK_ENV  # noqa: E402
KEYS = ["orientation", "taxonomy", "mainstream", "downstream", "pitfalls",
        "accuracy", "sourcing", "concision", "overall"]


def judge_cmd(judge, model, prompt):
    if judge == "grok":
        return [str(Path.home() / ".grok" / "bin" / "grok"), "-p", prompt, "-m", model,
                "--output-format", "json", "--permission-mode", "bypassPermissions", "--always-approve",
                "--disable-web-search", "--no-subagents"], dict(os.environ, **GROK_ENV)
    if judge == "claude-devin":
        return [str(Path.home() / ".local" / "bin" / "claude-devin"), "-p", prompt, "--model", model,
                "--output-format", "json", "--tools", "Read,Write", "--dangerously-skip-permissions",
                "--strict-mcp-config", "--no-session-persistence"], None
    return ["claude", "-p", prompt, "--model", model, "--output-format", "json",
            "--tools", "Read,Write", "--dangerously-skip-permissions", "--strict-mcp-config",
            "--no-session-persistence"], None


def one_pass(arms, seed, judge, model):
    order = list(arms)
    random.Random(seed).shuffle(order)
    work = Path(tempfile.mkdtemp(prefix=f"judge-p{seed}-"))
    spec = json.loads((ROOT / "arms.json").read_text(encoding="utf-8"))
    shutil.copy2(ROOT / spec["task"], work / "task.md")
    label = {}
    for i, arm in enumerate(order, start=1):
        shutil.copy2(ROOT / "runs" / arm / "report.md", work / f"D{i}.md")
        label[f"D{i}"] = arm
    prompt = (ROOT / "judge.md").read_text(encoding="utf-8")
    cmd, env = judge_cmd(judge, model, prompt)
    proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, env=env,
                          stdin=subprocess.DEVNULL)
    meta = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {}
    scores = json.loads((work / "scores.json").read_text(encoding="utf-8"))
    mapped = {label[d]: v for d, v in scores["docs"].items()}
    ranking = [label[d] for d in scores["ranking"]]
    return {"seed": seed, "labels": label, "scores": mapped, "ranking": ranking,
            "cost_usd": meta.get("total_cost_usd")}


def main(argv):
    opts = {}
    for flag in ("--passes", "--model", "--judge", "--out"):
        if flag in argv:
            opts[flag] = argv[argv.index(flag) + 1]
    arms = [a for a in argv[1:] if not a.startswith("--") and a not in opts.values()]
    passes = int(opts.get("--passes", 2))
    judge = opts.get("--judge", "claude")
    model = opts.get("--model", "grok-4.7" if judge == "grok" else "opus")
    out_dir = ROOT / "judge" / opts.get("--out", judge)
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for seed in range(1, passes + 1):
        res = one_pass(arms, seed, judge, model)
        res["judge"], res["model"] = judge, model
        (out_dir / f"pass{seed}.json").write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n",
                                             encoding="utf-8")
        results.append(res)
        print(f"pass {seed}: ranking {' > '.join(res['ranking'])}")
    summary = {}
    for arm in arms:
        rows = [r["scores"][arm] for r in results]
        summary[arm] = {k: round(sum(r[k] for r in rows) / len(rows), 2) for k in KEYS}
        summary[arm]["mean_rank"] = round(
            sum(r["ranking"].index(arm) + 1 for r in results) / len(results), 2)
        summary[arm]["errors"] = sorted({e for r in rows for e in r.get("errors", [])})
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")
    print("| arm | " + " | ".join(KEYS) + " | mean rank |")
    print("|---" * (len(KEYS) + 2) + "|")
    for arm in sorted(arms, key=lambda a: summary[a]["mean_rank"]):
        s = summary[arm]
        print(f"| {arm} | " + " | ".join(str(s[k]) for k in KEYS) + f" | {s['mean_rank']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
