#!/usr/bin/env python3
"""Score a report against bench/golden.json. Recall only."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GOLDEN_PATH = ROOT / "golden.json"


def load_golden():
    return json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))


def claim_hits(text, claim):
    folded = text.lower()
    missing = []
    for group in claim["groups"]:
        if not any(needle.lower() in folded for needle in group):
            missing.append(group[0])
    sourced = not missing and any(host.lower() in folded for host in claim["hosts"])
    return missing, sourced


def score_text(text, golden):
    rows = []
    for claim in golden["claims"]:
        missing, sourced = claim_hits(text, claim)
        rows.append(
            {
                "id": claim["id"],
                "hit": not missing,
                "sourced": sourced,
                "missing": missing,
            }
        )
    total = len(rows)
    hits = sum(1 for row in rows if row["hit"])
    sourced = sum(1 for row in rows if row["sourced"])
    return {
        "task_id": golden["task_id"],
        "claims": total,
        "hits": hits,
        "sourced": sourced,
        "recall": hits / total,
        "sourced_recall": sourced / total,
        "chars": len(text),
        "rows": rows,
    }


def render(result):
    lines = [
        f"{result['hits']}/{result['claims']} 命中，{result['sourced']}/{result['claims']} 同时带到来源主机，{result['chars']} 字",
        "",
        "| claim | 命中 | 带来源 | 缺的针 |",
        "|---|---|---|---|",
    ]
    for row in result["rows"]:
        mark = "yes" if row["hit"] else "no"
        src = "yes" if row["sourced"] else "no"
        missing = "、".join(row["missing"]) if row["missing"] else ""
        lines.append(f"| {row['id']} | {mark} | {src} | {missing} |")
    return "\n".join(lines)


def self_test():
    golden = load_golden()
    blank = score_text("nothing here", golden)
    if blank["hits"] != 0:
        raise SystemExit(f"blank scored {blank['hits']}")
    needles = []
    for claim in golden["claims"]:
        for group in claim["groups"]:
            needles.append(group[0])
        needles.append(claim["hosts"][0])
    full = score_text("\n".join(needles), golden)
    if full["hits"] != full["claims"] or full["sourced"] != full["claims"]:
        raise SystemExit(f"full scored {full['hits']} sourced {full['sourced']}")
    print(f"self-test ok {full['claims']} claims")


def main(argv):
    if len(argv) == 2 and argv[1] == "--self-test":
        self_test()
        return 0
    if len(argv) != 2:
        raise SystemExit("usage: score.py REPORT.md | score.py --self-test")
    text = Path(argv[1]).read_text(encoding="utf-8")
    result = score_text(text, load_golden())
    print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
