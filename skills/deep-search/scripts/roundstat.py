#!/usr/bin/env python3
"""Length trajectory and grid fill for a deep-search workspace.

usage: roundstat.py DIR [--budget CHARS]

Prints: chars of each snapshot and of report.md against the budget, whether any snapshot
grew past the budget or grew round over round, grid cell status counts, notes per round.
"""

import re
import sys
from collections import Counter
from pathlib import Path

STATUSES = ["✅", "⚠", "⚔", "❓", "∅"]


def cite_lines(text):
    """Warn if the source section has no URL, or the lead summary has no [n]."""
    lines = []
    marker = re.search(r"^##\s*来源\s*$", text, re.M)
    body = text[: marker.start()] if marker else text
    src = text[marker.start() :] if marker else ""
    if marker is None:
        lines.append("cite: 没有来源节")
    elif not re.search(r"https?://", src):
        lines.append("cite: 来源节没有 https:// URL（每条照抄笔记 src，不要去掉协议或用花括号合并）")
    screen = re.search(r"^##\s*0\.[^\n]*\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    if screen and len(screen.group(1).strip()) > 80 and not re.search(r"\[\d+\]", screen.group(1)):
        lines.append("cite: 一屏看懂没有 [n]（概括句要带矩阵格上的 [n]，[§k] 不算）")
    return lines


def main(argv):
    if len(argv) < 2:
        raise SystemExit("usage: roundstat.py DIR [--budget CHARS]")
    root = Path(argv[1])
    budget = int(argv[argv.index("--budget") + 1]) if "--budget" in argv else 20000

    snaps = sorted(root.glob("snapshots/report.r*.md"),
                   key=lambda p: int(re.search(r"r(\d+)", p.name).group(1)))
    lengths = [(p.name, len(p.read_text(encoding="utf-8"))) for p in snaps]
    report = root / "report.md"
    report_text = report.read_text(encoding="utf-8") if report.exists() else None
    if report_text is not None:
        lengths.append(("report.md", len(report_text)))
    print(f"budget {budget}")
    prev = None
    for name, n in lengths:
        flag = []
        if n > budget:
            flag.append("OVER BUDGET")
        if prev is not None and n > prev:
            flag.append(f"+{n - prev}")
        print(f"  {name}: {n} {' '.join(flag)}")
        prev = n
    if report_text is not None:
        for line in cite_lines(report_text):
            print(line)

    grid = root / "grid.md"
    if grid.exists():
        cells = Counter()
        for line in grid.read_text(encoding="utf-8").splitlines():
            if line.startswith("|"):
                for s in STATUSES:
                    cells[s] += line.count(s)
        total = sum(cells.values())
        filled = cells["✅"] + cells["∅"]
        pct = f"{100 * filled / total:.0f}%" if total else "n/a"
        print("grid: " + ", ".join(f"{s} {cells[s]}" for s in STATUSES) + f" | resolved {filled}/{total} ({pct})")

    notes = Counter()
    for p in root.glob("notes/r*-*.md"):
        notes[int(re.match(r"r(\d+)-", p.name).group(1))] += 1
    if notes:
        print("notes per round: " + ", ".join(f"r{k}={notes[k]}" for k in sorted(notes)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
