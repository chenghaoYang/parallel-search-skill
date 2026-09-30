#!/usr/bin/env python3
"""Optional size, citation-shape and existing-grid diagnostics for a research workspace.

usage: roundstat.py DIR [--budget CHARS] [--legacy-layout]

No layout, vocabulary file or length limit is required by default. --budget checks
report/snapshot character counts. --legacy-layout additionally checks the old source
section, numbered overview citations, atlas (2x budget) and 4000-character detail pages.
All findings are advisory: successful execution does not validate research quality.
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

STATUSES = ["✅", "⚠", "⚔", "❓", "∅"]


def cite_lines(text, legacy=False):
    """Check citation shape only, without claiming to verify sources or support."""
    if not legacy:
        if not re.search(r"https?://", text):
            return ["cite: no full source URL found; check provenance manually"]
        return []
    lines = []
    marker = re.search(r"^##\s*来源\s*$", text, re.M)
    body = text[: marker.start()] if marker else text
    src = text[marker.start() :] if marker else ""
    if marker is None:
        lines.append("cite: legacy layout has no 来源 section")
    elif not re.search(r"https?://", src):
        lines.append("cite: legacy 来源 section has no full source URL")
    screen = re.search(r"^##\s*0\.[^\n]*\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    if screen and len(screen.group(1).strip()) > 80 and not re.search(r"\[\d+\]", screen.group(1)):
        lines.append("cite: legacy overview has no numbered citation; check manually")
    return lines


def snapshot_key(path):
    match = re.fullmatch(r"report\.r(\d+)\.md", path.name)
    return (0, int(match.group(1))) if match else (1, path.name)


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--budget", type=int, help="optional report character cap")
    parser.add_argument("--legacy-layout", action="store_true")
    args = parser.parse_args(argv[1:])
    root, budget = args.directory, args.budget
    if not root.is_dir():
        parser.error(f"workspace directory does not exist: {root}")
    if budget is not None and budget < 1:
        parser.error("--budget must be positive")

    print("Diagnostics only; factual accuracy and source support are NOT ASSESSED.")
    print(f"budget {budget}" if budget is not None else "budget not specified (sizes only)")
    snaps = sorted(root.glob("snapshots/report.*.md"), key=snapshot_key)
    lengths = [(p.name, len(p.read_text(encoding="utf-8"))) for p in snaps]
    report = root / "report.md"
    report_text = report.read_text(encoding="utf-8") if report.exists() else None
    if report_text is not None:
        lengths.append(("report.md", len(report_text)))
    else:
        print("report.md not present; main report NOT ASSESSED")
    prev = None
    for name, n in lengths:
        flag = []
        if budget is not None and n > budget:
            flag.append("OVER BUDGET")
        if prev is not None and n != prev:
            flag.append(f"change {n - prev:+d}")
        print(f"  {name}: {n} {' '.join(flag)}".rstrip())
        prev = n
    if report_text is not None:
        for line in cite_lines(report_text, legacy=args.legacy_layout):
            print(line)

    atlas = root / "atlas.md"
    if atlas.exists():
        n = len(atlas.read_text(encoding="utf-8"))
        cap = 2 * budget if args.legacy_layout and budget is not None else None
        flag = " OVER BUDGET" if cap is not None and n > cap else ""
        print(f"atlas.md: {n}" + (f" (legacy cap {cap})" if cap is not None else "") + flag)
    for p in sorted(root.glob("details/*.md")):
        n = len(p.read_text(encoding="utf-8"))
        flag = " OVER 4000 (legacy cap)" if args.legacy_layout and n > 4000 else ""
        print(f"details/{p.name}: {n}{flag}")

    grid = root / "grid.md"
    if grid.exists():
        cells = Counter()
        for line in grid.read_text(encoding="utf-8").splitlines():
            if line.startswith("|"):
                for status in STATUSES:
                    cells[status] += line.count(status)
        total = sum(cells.values())
        print("grid markers: " + ", ".join(f"{s} {cells[s]}" for s in STATUSES) +
              f" | {total} total (marker counts, not verified coverage)")

    notes = Counter()
    for p in root.glob("notes/r*-*.md"):
        match = re.match(r"r(\d+)-", p.name)
        if match:
            notes[int(match.group(1))] += 1
    if notes:
        print("notes per round: " + ", ".join(f"r{k}={notes[k]}" for k in sorted(notes)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
