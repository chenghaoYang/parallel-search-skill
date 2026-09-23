#!/usr/bin/env python3
"""Fixed evaluation harness for the deep-search self-evolution loop.

Plays the role of prepare.py in karpathy/autoresearch: the loop's agents must not edit this file,
config.json, judge_pair.md, mech.py or bench/tasks/*. See program.md.

usage:
  evaluate.py run    EXP --skill DIR [--tasks a,b] [--reps N] [--arm dev] [--parallel 4]
  evaluate.py judge  EXP --vs EXP2[,EXP3] [--tasks a,b]
  evaluate.py report EXP [--vs EXP2,...] [--tasks a,b]
  evaluate.py all    EXP --skill DIR [--vs EXP2,...] [--tasks a,b] [--reps N] [--arm dev]

run     runs the skill in DIR on each task with the fixed arm from config.json (default: dev), in
        parallel, outside the repo; copies report + ds/ artifacts + meta.json (with mech metrics)
        back to runs/EXP/<task>[-rN]/. A run that exceeds timeout_min is killed and scored as is.
judge   blind pairwise judging of EXP's runs vs every run of each VS exp on the same task, by every
        judge in config.json, in both orders. Score from EXP's side: +strength win, -strength loss,
        0 tie, so it lies in [-2, 2]. Verdicts are cached under runs/EXP/judge/.
report  prints the summary block (grep "^score:") and writes runs/EXP/summary.json.
"""

import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
TASKS = REPO / "bench" / "tasks"
RUNS = ROOT / "runs"
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
ARENA = Path(os.environ.get("PS_ARENA") or Path(tempfile.gettempdir()) / "ps-arena") / "evolve"
DIMS = ["orientation", "taxonomy", "coverage", "doubts", "pitfalls", "accuracy", "sourcing", "concision"]

sys.path.insert(0, str(REPO / "bench"))
sys.path.insert(0, str(ROOT))
from run_arm import cc_prompt, collect, worker_agent  # noqa: E402
from judge import judge_cmd  # noqa: E402
from mech import mech  # noqa: E402

SKILL_ROOT = ".claude/skills/deep-search"


def skill_fingerprint(skill_dir):
    """Content hash and size of the skill's text (the 'complexity' of the thing being evolved)."""
    h, chars = hashlib.sha1(), 0
    for p in sorted(Path(skill_dir).rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            data = p.read_bytes()
            h.update(str(p.relative_to(skill_dir)).encode() + b"\0" + data)
            if p.suffix == ".md":
                chars += len(data.decode("utf-8", errors="replace"))
    return h.hexdigest()[:10], chars


def dev_prompt(task, arm):
    lines = ["/deep-search " + task.strip(), "", "---", "外层说明（Claude Code，benchmark 固定设置）："]
    if arm.get("params"):
        lines.append(f"- 参数：{arm['params']}。")
    lines += [
        f"- skill 目录是 {SKILL_ROOT}。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。",
        "- 工人用 subagent_type \"research-worker\"（模型已由外层固定，不要传 model）。",
        "- 检索：工人用 WebSearch 找页面，再用 WebFetch 打开一手页面取原句。本次运行没有 pplx-safe。",
        "- 当前目录之外的文件与本任务无关，不要读。",
    ]
    return "\n".join(lines) + "\n"


def parse_transcript(path):
    tools, result, http429 = Counter(), {}, 0
    if not path.exists():
        return {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("{"):
            continue
        if "rate_limit" in line or '"status":429' in line.replace(" ", ""):
            http429 += 1
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            result = ev
        elif ev.get("type") == "assistant" and not ev.get("parent_tool_use_id"):
            for c in (ev.get("message") or {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    tools[c.get("name")] += 1
    return {
        "spawns": tools["Agent"] + tools["Task"],
        "followups": tools["SendMessage"],
        "lead_web": tools["WebSearch"] + tools["WebFetch"],
        "lead_tools": dict(tools),
        "cost_usd": result.get("total_cost_usd"),
        "num_turns": result.get("num_turns"),
        "is_error": result.get("is_error"),
        "terminal_reason": result.get("terminal_reason") or result.get("subtype"),
        "rate_limit_lines": http429,
    }


def run_one(exp, task_id, rep, skill_dir, arm_id):
    arm = CFG["arms"][arm_id]
    name = task_id if rep == 1 else f"{task_id}-r{rep}"
    out, work = RUNS / exp / name, ARENA / exp / name
    for d in (out, work):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    shutil.copytree(skill_dir, work / SKILL_ROOT, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    task = (TASKS / task_id / "task.md").read_text(encoding="utf-8")
    websearch = arm["search"] == "websearch"
    prompt = dev_prompt(task, arm) if websearch or arm.get("params") else cc_prompt(task)
    (out / "prompt.md").write_text(prompt, encoding="utf-8")
    disallow = ["ScheduleWakeup", "CronCreate"] + ([] if websearch else ["WebSearch"])
    agents = worker_agent(arm["worker"], skill_dir, ("WebSearch",) if websearch else ())
    cmd = ["claude", "-p", prompt, "--model", arm["lead"], "--output-format", "stream-json", "--verbose",
           "--dangerously-skip-permissions", "--strict-mcp-config", "--disallowedTools", *disallow,
           "--settings", json.dumps({"sandbox": {"enabled": False}}),
           "--agents", json.dumps(agents, ensure_ascii=False),
           "--max-budget-usd", str(arm["max_budget_usd"])]
    env = dict(os.environ)
    if websearch:
        env["PPLX_WEB_SCRIPT"] = "/nonexistent/pplx_web.py"
    status, t0 = "ok", time.time()
    with open(work / "transcript.jsonl", "w", encoding="utf-8") as fo, \
            open(work / "stderr.txt", "w", encoding="utf-8") as fe:
        proc = subprocess.Popen(cmd, cwd=work, stdout=fo, stderr=fe, env=env,
                                stdin=subprocess.DEVNULL, start_new_session=True)
        try:
            rc = proc.wait(timeout=arm["timeout_min"] * 60)
        except subprocess.TimeoutExpired:
            status = "timeout"
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                rc = proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                rc = proc.wait()
    minutes = round((time.time() - t0) / 60, 1)
    collect(work, out)
    if not (out / "report.md").exists() and (work / "ds" / "report.md").exists():
        shutil.copy2(work / "ds" / "report.md", out / "report.md")
    stats = parse_transcript(out / "transcript.jsonl")
    m = mech(out, task_id, arm["budget"])
    if status == "ok" and (rc != 0 or stats.get("is_error")):
        status = "error"
    if not m["chars"]:
        status = "crash"
    sha, skill_chars = skill_fingerprint(skill_dir)
    meta = {"exp": exp, "task": task_id, "rep": rep, "arm": arm_id, "skill_dir": str(skill_dir),
            "skill_sha": sha, "skill_chars": skill_chars, "status": status, "returncode": rc,
            "minutes": minutes, **stats, "mech": m, "arena": str(work)}
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[run] {exp}/{name}: {status}, {minutes} min, {m['chars']} chars, golden {m['golden']}, "
          f"spawns {stats.get('spawns')}, ${stats.get('cost_usd')}", flush=True)
    return meta


def run_dirs(exp, task_id):
    base = RUNS / exp
    return sorted(p for p in base.glob(f"{task_id}*") if p.is_dir() and re.fullmatch(
        re.escape(task_id) + r"(-r\d+)?", p.name))


def judge_once(judge, model, task_id, doc_a, doc_b):
    work = Path(tempfile.mkdtemp(prefix="pair-"))
    shutil.copy2(TASKS / task_id / "task.md", work / "task.md")
    shutil.copy2(doc_a, work / "A.md")
    shutil.copy2(doc_b, work / "B.md")
    prompt = (ROOT / "judge_pair.md").read_text(encoding="utf-8")
    cmd, env = judge_cmd(judge, model, prompt)
    for _ in range(2):
        try:
            subprocess.run(cmd, cwd=work, capture_output=True, text=True, env=env,
                           stdin=subprocess.DEVNULL, timeout=1500)
        except subprocess.TimeoutExpired:
            continue
        vp = work / "verdict.json"
        if vp.exists():
            try:
                return json.loads(vp.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                vp.unlink()
    return None


def judge_job(job):
    task_id, xdir, vs, ydir, j, order, dest = job
    xr, yr = xdir / "report.md", ydir / "report.md"
    if not xr.exists() or not yr.exists():
        res = {"score": -2 if not xr.exists() else 2, "note": "missing report", "dims": {}}
    else:
        a, b = (xr, yr) if order == "xy" else (yr, xr)
        v = judge_once(j["judge"], j["model"], task_id, a, b)
        if v is None:
            return None
        x_label = "A" if order == "xy" else "B"
        sign = lambda w: 0 if w not in ("A", "B") else (1 if w == x_label else -1)  # noqa: E731
        strength = int(v.get("strength") or 0) or (1 if v.get("overall") in ("A", "B") else 0)
        res = {"score": sign(v.get("overall")) * min(strength, 2),
               "dims": {d: sign((v.get("dims") or {}).get(d)) for d in DIMS},
               "errors_x": (v.get("errors") or {}).get(x_label, []),
               "errors_y": (v.get("errors") or {}).get("B" if x_label == "A" else "A", []),
               "reason": v.get("reason"), "raw": v}
    res.update({"task": task_id, "x": str(xdir.relative_to(RUNS)), "y": str(ydir.relative_to(RUNS)),
                "judge": j["judge"], "model": j["model"], "order": order})
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return res


def judge(exp, vs_list, tasks):
    jobs = []
    for task_id in tasks:
        for xdir in run_dirs(exp, task_id):
            for vs in vs_list:
                for ydir in run_dirs(vs, task_id):
                    for j in CFG["judges"]:
                        for order in ("xy", "yx"):
                            dest = (RUNS / exp / "judge" / task_id /
                                    f"{xdir.name}__{vs}-{ydir.name}__{j['judge']}-{order}.json")
                            if not dest.exists():
                                jobs.append((task_id, xdir, vs, ydir, j, order, dest))
    print(f"[judge] {exp} vs {','.join(vs_list)}: {len(jobs)} verdicts to collect", flush=True)
    with ThreadPoolExecutor(CFG["judge_parallel"]) as pool:
        failed = sum(1 for r in pool.map(judge_job, jobs) if r is None)
    if failed:
        print(f"[judge] {failed} verdicts failed (rerun judge to retry)", flush=True)


def load_verdicts(exp, vs_list, task_id):
    rows = []
    for p in sorted((RUNS / exp / "judge" / task_id).glob("*.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        if r["y"].split("/")[0] in vs_list:
            rows.append(r)
    return rows


def refresh(meta_path):
    """Recompute the mechanical metrics (goldens may be added or fixed after a run)."""
    m = json.loads(meta_path.read_text(encoding="utf-8"))
    m["mech"] = mech(meta_path.parent, m["task"], CFG["arms"][m["arm"]]["budget"])
    return m


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 3) if xs else None


def report(exp, vs_list, tasks=None):
    metas = [refresh(p) for p in sorted((RUNS / exp).glob("*/meta.json"))]
    tasks = tasks or sorted({m["task"] for m in metas})
    metas = [m for m in metas if m["task"] in tasks]
    vs_metas = [refresh(p) for vs in vs_list for p in sorted((RUNS / vs).glob("*/meta.json"))]
    vs_metas = [m for m in vs_metas if m["task"] in tasks]
    task_scores, dims, n_verdicts = {}, Counter(), 0
    for t in tasks:
        rows = load_verdicts(exp, vs_list, t) if vs_list else []
        task_scores[t] = mean([r["score"] for r in rows])
        n_verdicts += len(rows)
        for r in rows:
            for d, s in (r.get("dims") or {}).items():
                dims[d] += s
    scored = [s for s in task_scores.values() if s is not None]
    s = {
        "exp": exp, "vs": vs_list, "tasks": tasks,
        "score": mean(scored) if scored else None,
        "task_scores": task_scores,
        "wins": f"{sum(1 for x in scored if x > 0)}/{len(scored)}",
        "losses": sum(1 for x in scored if x < 0),
        "verdicts": n_verdicts,
        "dims_net": {d: dims[d] for d in DIMS} if n_verdicts else {},
        "golden": mean([m["mech"]["golden"] for m in metas]),
        "golden_vs": mean([m["mech"]["golden"] for m in vs_metas]) if vs_metas else None,
        "chars_max": max((m["mech"]["chars"] for m in metas), default=0),
        "len_ok": f"{sum(1 for m in metas if m['mech']['len_ok'])}/{len(metas)}",
        "traceable": mean([m["mech"]["traceable"] for m in metas]),
        "spawns": mean([m.get("spawns") for m in metas]),
        "lead_web": sum(m.get("lead_web") or 0 for m in metas),
        "cost_usd": round(sum(m.get("cost_usd") or 0 for m in metas), 2),
        "cost_vs_per_run": mean([m.get("cost_usd") for m in vs_metas]) if vs_metas else None,
        "minutes": mean([m.get("minutes") for m in metas]),
        "skill_chars": metas[0]["skill_chars"] if metas else None,
        "skill_sha": metas[0]["skill_sha"] if metas else None,
        "statuses": dict(Counter(m["status"] for m in metas)),
        "runs": len(metas),
    }
    (RUNS / exp / "summary.json").write_text(json.dumps(s, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fmt = lambda v: "n/a" if v is None else (f"{v:+.3f}" if isinstance(v, float) else str(v))  # noqa: E731
    print("---")
    print(f"exp:          {exp}")
    print(f"vs:           {','.join(vs_list) or '-'}")
    print(f"score:        {fmt(s['score'])}")
    print("task_scores:  " + " ".join(f"{t}:{fmt(v)}" for t, v in task_scores.items()))
    print(f"wins:         {s['wins']}  (verdicts {n_verdicts})")
    print("dims_net:     " + " ".join(f"{d}:{v:+d}" for d, v in s["dims_net"].items()))
    print(f"golden:       {s['golden']}  (vs {s['golden_vs']})")
    print(f"chars_max:    {s['chars_max']}")
    print(f"len_ok:       {s['len_ok']}")
    print(f"traceable:    {s['traceable']}")
    print(f"spawns:       {s['spawns']}")
    print(f"lead_web:     {s['lead_web']}")
    print(f"cost_usd:     {s['cost_usd']}  (vs per run {s['cost_vs_per_run']})")
    print(f"minutes:      {s['minutes']}")
    print(f"skill_chars:  {s['skill_chars']}")
    print(f"statuses:     {s['statuses']}")
    return s


def parse(argv):
    opts, pos, i = {}, [], 0
    while i < len(argv):
        if argv[i].startswith("--"):
            opts[argv[i][2:]] = argv[i + 1]
            i += 2
        else:
            pos.append(argv[i])
            i += 1
    return pos, opts


def main(argv):
    pos, opts = parse(argv[1:])
    if len(pos) != 2 or pos[0] not in ("run", "judge", "report", "all"):
        raise SystemExit(__doc__)
    cmd, exp = pos
    tasks = opts["tasks"].split(",") if "tasks" in opts else None
    vs_list = [v for v in opts.get("vs", "").split(",") if v]
    if cmd in ("run", "all"):
        skill = Path(opts["skill"]).resolve()
        arm_id = opts.get("arm", "dev")
        tasks = tasks or CFG["dev_tasks"]
        reps = int(opts.get("reps", 1))
        jobs = [(exp, t, r, skill, arm_id) for t in tasks for r in range(1, reps + 1)]
        with ThreadPoolExecutor(int(opts.get("parallel", 4))) as pool:
            list(pool.map(lambda a: run_one(*a), jobs))
    if cmd in ("judge", "all") and vs_list:
        judge(exp, vs_list, tasks or sorted({re.sub(r"-r\d+$", "", p.parent.name) for p in (RUNS / exp).glob("*/meta.json")}))
    if cmd in ("report", "all", "judge"):
        report(exp, vs_list, tasks)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
