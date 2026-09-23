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


def main(argv):
    if len(argv) < 2:
        raise SystemExit("usage: roundstat.py DIR [--budget CHARS]")
    root = Path(argv[1])
    budget = int(argv[argv.index("--budget") + 1]) if "--budget" in argv else 20000

    snaps = sorted(root.glob("snapshots/report.r*.md"),
                   key=lambda p: int(re.search(r"r(\d+)", p.name).group(1)))
    lengths = [(p.name, len(p.read_text(encoding="utf-8"))) for p in snaps]
    report = root / "report.md"
    if report.exists():
        lengths.append(("report.md", len(report.read_text(encoding="utf-8"))))
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
