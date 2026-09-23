#!/usr/bin/env python3
"""Sum Grok Build usage (lead + every subagent session) for a finished grok-build arm into meta.json.

usage: grok_usage.py ARM_ID
xAI reports cost in ticks; 1 USD = 1e10 ticks.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from run_arm import GROK_ENV, ARENA  # noqa: E402
import os  # noqa: E402

GROK = str(Path.home() / ".grok" / "bin" / "grok")


def usage(session_id, cwd):
    out = subprocess.run([GROK, "usage", session_id], cwd=cwd, capture_output=True, text=True,
                         env=dict(os.environ, **GROK_ENV), stdin=subprocess.DEVNULL).stdout
    try:
        return json.loads(out)["session"]
    except (json.JSONDecodeError, KeyError):
        return None


def main(arm_id):
    run = ROOT / "runs" / arm_id
    text = (run / "transcript.jsonl").read_text(encoding="utf-8")
    lead = json.loads(text.splitlines()[0]).get("session_id")
    subs = sorted(set(re.findall(r"subagent_id: ([0-9a-f-]{36})", text)))
    cwd = ARENA / arm_id
    tot = {"inputTokens": 0, "outputTokens": 0, "cachedReadTokens": 0, "modelCalls": 0, "costUsdTicks": 0}
    found = 0
    for sid in [lead] + subs:
        u = usage(sid, cwd)
        if u:
            found += 1
            for k in tot:
                tot[k] += u.get(k, 0)
    meta = json.loads((run / "meta.json").read_text(encoding="utf-8"))
    meta["grok_usage"] = {**tot, "sessions_found": found, "subagents": len(subs)}
    meta["total_cost_usd"] = round(tot["costUsdTicks"] / 1e10, 2)
    meta["subagent_stats"] = {"spawned": len(subs)}
    (run / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(arm_id, meta["grok_usage"], "cost $", meta["total_cost_usd"])


if __name__ == "__main__":
    main(sys.argv[1])
