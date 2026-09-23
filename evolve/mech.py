#!/usr/bin/env python3
"""Mechanical metrics for one deep-search run directory (part of the fixed evaluation harness).

usage: mech.py RUN_DIR TASK_ID [--budget 9000]

report   chars, len_ok (0 < chars <= budget), required sections present
golden   recall over bench/tasks/<task>/golden.json (hidden from the loop's proposers)
sources  unique URLs in the report; share of them that also appear as a `src:` in the notes
notes    note files, claims, share of claims with a full-URL src and a quote
process  snapshot lengths per round (from ds/snapshots)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS = ROOT.parent / "bench" / "tasks"
URL = re.compile(r"https?://[^\s<>()\[\]{}\"'`，。；、）」|]+")
SECTIONS = {
    "overview": r"一屏|速览|TL;?DR|先看结论|结论先行",
    "taxonomy": r"taxonomy|分类|谱系|家族",
    "matrix": r"对照|矩阵|对比表|比较表",
    "pitfalls": r"坑|陷阱|注意事项|需要知道",
    "open": r"未决|置信|待核|未解决|缺口",
    "sources": r"来源|参考|引用|Sources|References",
}


def norm_url(u):
    u = u.rstrip(".,;:!?*_~")
    u = u.split("#", 1)[0]
    return u.rstrip("/").lower()


def golden_recall(text, task_id):
    path = TASKS / task_id / "golden.json"
    if not path.exists():
        return None, []
    claims = json.loads(path.read_text(encoding="utf-8"))["claims"]
    low = text.lower()
    missed = []
    for c in claims:
        if not all(any(n.lower() in low for n in group) for group in c["groups"]):
            missed.append(c["id"])
    return round(1 - len(missed) / len(claims), 3), missed


def note_stats(notes_dir):
    files = sorted(notes_dir.glob("*.md")) if notes_dir.exists() else []
    srcs, claims, good = set(), 0, 0
    for f in files:
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not re.match(r"\s*-\s*\[C\d+\]", line):
                continue
            claims += 1
            m = re.search(r"src:\s*(\S+)", line)
            if m and m.group(1).startswith("http"):
                srcs.add(norm_url(m.group(1)))
                if "quote:" in line:
                    good += 1
    return {"files": len(files), "claims": claims,
            "claims_ok": round(good / claims, 3) if claims else 0.0}, srcs


def mech(run_dir, task_id, budget):
    run_dir = Path(run_dir)
    rp = run_dir / "report.md"
    text = rp.read_text(encoding="utf-8", errors="replace") if rp.exists() else ""
    heads = "\n".join(l for l in text.splitlines() if l.lstrip().startswith("#"))
    sections = {k: bool(re.search(p, heads, re.I)) for k, p in SECTIONS.items()}
    recall, missed = golden_recall(text, task_id)
    notes, note_srcs = note_stats(run_dir / "ds" / "notes")
    urls = {norm_url(u) for u in URL.findall(text)}
    traced = sum(1 for u in urls if u in note_srcs or any(s.startswith(u) or u.startswith(s) for s in note_srcs))
    snaps = sorted((run_dir / "ds" / "snapshots").glob("report.*.md")) if (run_dir / "ds" / "snapshots").exists() else []
    return {
        "chars": len(text),
        "len_ok": 0 < len(text) <= budget,
        "sections": round(sum(sections.values()) / len(sections), 3),
        "sections_missing": [k for k, v in sections.items() if not v],
        "golden": recall,
        "golden_missed": missed,
        "urls": len(urls),
        "traceable": round(traced / len(urls), 3) if urls else 0.0,
        "notes": notes,
        "snapshots": {p.name: len(p.read_text(encoding="utf-8", errors="replace")) for p in snaps},
    }


def main(argv):
    if len(argv) < 3:
        raise SystemExit(__doc__)
    budget = int(argv[argv.index("--budget") + 1]) if "--budget" in argv else 9000
    print(json.dumps(mech(argv[1], argv[2], budget), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
