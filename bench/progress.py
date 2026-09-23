#!/usr/bin/env python3
"""One-screen progress of running claude-code arms (reads the arena transcript).

usage: progress.py ARM_ID [ARM_ID ...]
"""

import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path

ARENA = Path(os.environ.get("PS_ARENA") or Path(tempfile.gettempdir()) / "ps-arena")


def summarize(arm):
    work = ARENA / arm
    tx = work / "transcript.jsonl"
    if not tx.exists():
        return f"== {arm}: no transcript at {tx}"
    lead_tools, sub_tools, last_text, result = Counter(), Counter(), "", None
    for line in tx.read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            result = ev
        if ev.get("type") != "assistant":
            continue
        is_sub = bool(ev.get("parent_tool_use_id"))
        for block in ev.get("message", {}).get("content", []):
            if block.get("type") == "tool_use":
                (sub_tools if is_sub else lead_tools)[block["name"]] += 1
            elif block.get("type") == "text" and not is_sub:
                last_text = block["text"].strip().replace("\n", " ")[:300]
    ds = work / "ds"
    notes = sorted(p.name for p in (ds / "notes").glob("*.md")) if (ds / "notes").exists() else []
    snaps = sorted(p.name for p in (ds / "snapshots").glob("*.md")) if (ds / "snapshots").exists() else []
    rep = work / "report.md"
    lines = [f"== {arm}",
             f"lead tools: {dict(lead_tools)}",
             f"subagent tools: {dict(sub_tools)}",
             f"notes ({len(notes)}): {', '.join(notes)}",
             f"snapshots: {', '.join(snaps)}; report.md: {len(rep.read_text(encoding='utf-8')) if rep.exists() else '-'} chars",
             f"last lead text: {last_text}"]
    if result:
        lines.append(f"RESULT: error={result.get('is_error')} reason={result.get('terminal_reason')} "
                     f"cost=${result.get('total_cost_usd')} turns={result.get('num_turns')}")
    return "\n".join(lines)


if __name__ == "__main__":
    print("\n".join(summarize(a) for a in sys.argv[1:]))
