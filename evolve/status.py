#!/usr/bin/env python3
"""One line per in-flight or finished run in the arena: age, lead spawns, notes, snapshots, report size.

usage: status.py [EXP ...]
"""

import json
import os
import sys
import tempfile
import time
from pathlib import Path

ARENA = Path(os.environ.get("PS_ARENA") or Path(tempfile.gettempdir()) / "ps-arena") / "evolve"
if not ARENA.exists():  # sandboxed shells see a different TMPDIR than the unsandboxed runs
    ARENA = next(Path("/var/folders").glob("*/*/T/ps-arena/evolve"), ARENA)
RUNS = Path(__file__).resolve().parent / "runs"


def line(work):
    t = work / "transcript.jsonl"
    if not t.exists():
        return None
    spawns, done = 0, (RUNS / work.parent.name / work.name / "meta.json").exists()
    for raw in t.read_text(encoding="utf-8", errors="replace").splitlines():
        if '"tool_use"' in raw and '"parent_tool_use_id":null' in raw.replace(" ", ""):
            try:
                ev = json.loads(raw)
            except json.JSONDecodeError:
                continue
            spawns += sum(1 for c in ev.get("message", {}).get("content", [])
                          if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") in ("Agent", "Task"))
    ds = work / "ds"
    notes = len(list((ds / "notes").glob("*.md"))) if (ds / "notes").exists() else 0
    snaps = sorted(p.name.replace("report.", "").replace(".md", "") for p in (ds / "snapshots").glob("*.md")) \
        if (ds / "snapshots").exists() else []
    rep = ds / "report.md"
    age = (time.time() - (work / ".claude").stat().st_mtime) / 60
    return (f"{work.parent.name}/{work.name:<16} {'done' if done else 'live'} {age:5.1f}m  spawns {spawns:2d}  "
            f"notes {notes:2d}  snaps {','.join(snaps) or '-':<14} report {len(rep.read_text(errors='replace')) if rep.exists() else 0}")


def main(argv):
    exps = argv[1:] or sorted(p.name for p in ARENA.iterdir() if p.is_dir())
    for exp in exps:
        for work in sorted((ARENA / exp).iterdir()) if (ARENA / exp).exists() else []:
            s = line(work)
            if s:
                print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
