#!/usr/bin/env python3
"""Block until every listed run has a meta.json (or a summary.json for judge phases), up to --max seconds.

usage: wait.py [--max 540] [--summary] EXP[/TASK] ...
"""
import sys
import time
from pathlib import Path

RUNS = Path(__file__).resolve().parent / "runs"
args = sys.argv[1:]
limit = int(args[args.index("--max") + 1]) if "--max" in args else 540
summary = "--summary" in args
targets = [a for a in args if not a.startswith("--") and not a.isdigit()]
t0 = time.time()
while True:
    pending = []
    for t in targets:
        if summary:
            if not (RUNS / t / "summary.json").exists():
                pending.append(t)
        elif "/" in t:
            if not (RUNS / t / "meta.json").exists():
                pending.append(t)
    if not pending or time.time() - t0 > limit:
        break
    time.sleep(20)
print("pending:", " ".join(pending) if pending else "none", f"({int(time.time() - t0)}s)")
