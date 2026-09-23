#!/usr/bin/env python3
"""Build the comparison table for arms.json from runs/<arm>/ and judge/summary.json.

usage: summarize.py            print markdown table
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from score import load_golden, score_text  # noqa: E402


def trajectory(run):
    snaps = sorted((run / "ds" / "snapshots").glob("report.r*.md"),
                   key=lambda p: int(re.search(r"r(\d+)", p.name).group(1)))
    lengths = [len(p.read_text(encoding="utf-8")) for p in snaps]
    if snaps and (run / "report.md").exists():
        lengths.append(len((run / "report.md").read_text(encoding="utf-8")))  # final, after audit
    return " → ".join(map(str, lengths))


def audit_counts(run):
    """Sum the auditors' final counts (skill arms only): supported/weak/unsupported/contradicted."""
    tot = {"supported": 0, "weak": 0, "unsupported": 0, "contradicted": 0}
    found = False
    for f in (run / "ds").glob("audit*.md"):
        text = f.read_text(encoding="utf-8")
        tail = text[text.rfind("计数"):] if "计数" in text else text[-600:]
        for key, pat in (("supported", r"(?<!un)supported\s*[:：]?\s*(\d+)"), ("weak", r"weak\s*[:：]?\s*(\d+)"),
                         ("unsupported", r"unsupported\s*[:：]?\s*(\d+)"),
                         ("contradicted", r"contradicted\s*[:：]?\s*(\d+)")):
            m = re.findall(pat, tail)
            if m:
                tot[key] += int(m[-1]); found = True
    return tot if found else None


def row(arm, golden, judges):
    run = ROOT / "runs" / arm["id"]
    meta = json.loads((run / "meta.json").read_text(encoding="utf-8")) if (run / "meta.json").exists() else {}
    rep = run / "report.md"
    if not rep.exists():
        return {"id": arm["id"], "status": "no report"}
    text = rep.read_text(encoding="utf-8")
    sc = score_text(text, golden)
    stats = meta.get("subagent_stats") or {}
    jc = judges.get("claude", {}).get(arm["id"], {})
    jg = judges.get("grok", {}).get(arm["id"], {})
    model = arm.get("model") or f"{arm.get('lead')}→{arm.get('worker')}"
    if arm.get("mode"):
        model += f" ({arm['mode']})"
    reported = meta.get("model_reported")
    if reported and reported != arm.get("model"):
        model += f" ⇒ 实际 {reported}"
    return {
        "id": arm["id"], "model": model, "hits": sc["hits"], "sourced": sc["sourced"],
        "chars": sc["chars"], "seconds": meta.get("seconds"),
        "cost": meta.get("total_cost_usd"), "spawns": stats.get("spawned"),
        "overall": jc.get("overall"), "rank": jc.get("mean_rank"),
        "g_overall": jg.get("overall"), "g_rank": jg.get("mean_rank"), "traj": trajectory(run),
        "audit": audit_counts(run),
    }


def main():
    spec = json.loads((ROOT / "arms.json").read_text(encoding="utf-8"))
    golden = load_golden()
    judges = {}
    for name, folder in (("claude", "claude-12docs"), ("grok", "grok-12docs")):  # the 12-arm bench round
        jpath = ROOT / "judge" / folder / "summary.json"
        if jpath.exists():
            judges[name] = json.loads(jpath.read_text(encoding="utf-8"))
    rows = [row(a, golden, judges) for a in spec["arms"] if a["harness"] != "external"]
    print("| arm | 模型 | Opus 评审 overall（名次） | Grok 评审 overall（名次） | v1 命中/12 | 字数 | 用时 min | 花费 $ | spawn | 自审 支撑/弱/无据/矛盾 | 快照字数轨迹 |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (r.get("rank") is None, r.get("rank") or 0)):
        if r.get("status"):
            print(f"| {r['id']} | {r['status']} |" + " |" * 9)
            continue
        cost = f"{r['cost']:.2f}" if isinstance(r["cost"], (int, float)) else ""
        mins = f"{r['seconds'] / 60:.0f}" if r["seconds"] else ""
        fmt = lambda o, k: f"{o} ({k})" if o is not None else ""
        audit = "/".join(str(r["audit"][k]) for k in ("supported", "weak", "unsupported", "contradicted")) if r["audit"] else ""
        print(f"| {r['id']} | {r['model']} | {fmt(r['overall'], r['rank'])} | {fmt(r['g_overall'], r['g_rank'])} | "
              f"{r['hits']} | {r['chars']} | {mins} | {cost} | {r['spawns'] if r['spawns'] is not None else ''} | "
              f"{audit} | {r['traj']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
