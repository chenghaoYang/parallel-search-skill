#!/usr/bin/env python3
"""Latest Claude subscription utilization seen in any run transcript (five_hour, seven_day).

usage: quota.py            prints the most recent reading
The loop stops launching Claude runs when seven_day >= STOP (program.md).
"""
import json
import os
import sys
from pathlib import Path

STOP = 0.85
roots = [Path(__file__).resolve().parent / "runs"] + list(Path("/var/folders").glob("*/*/T/ps-arena/evolve"))
best = None
for root in roots:
    for t in root.glob("*/*/transcript.jsonl"):
        mt = os.path.getmtime(t)
        if best and mt <= best[0]:
            continue
        last = None
        with open(t, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"type":"rate_limit_event"' in line:
                    last = line
        if last:
            best = (mt, t, json.loads(last)["rate_limit_info"])
if not best:
    sys.exit("no rate_limit_event found")
w = best[2].get("unifiedWindows", {})
five, week = w.get("five_hour", {}).get("utilization"), w.get("seven_day", {}).get("utilization")
print(f"five_hour {five}  seven_day {week}  (stop at {STOP})  from {best[1].parent.parent.name}/{best[1].parent.name}")
sys.exit(3 if week is not None and week >= STOP else 0)
