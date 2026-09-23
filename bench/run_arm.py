#!/usr/bin/env python3
"""Run one arm from arms.json and collect report + metrics into runs/<arm>/.

usage: run_arm.py ARM_ID [--force]

pplx        one pplx-safe search with the adapted task text; answer + citations = report.md
claude-code headless `claude -p` in a fresh arena dir with the deep-search skill installed;
            workers are the skill's research-worker agent pinned to the arm's worker model.
Runs are executed outside the repo (PS_ARENA, default $TMPDIR/ps-arena) so the run cannot
see golden.json; artifacts are copied back afterwards.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SKILL = REPO / "skills" / "deep-search"
RUNS = ROOT / "runs"
ARENA = Path(os.environ.get("PS_ARENA") or Path(tempfile.gettempdir()) / "ps-arena")
PPLX_DROP = ("大规模并行调研", "不停的refine", "不允许文章越来越长")
# Perplexity treats "产出文档" as "generate a file": the answer is then only a summary of a file that
# pplx-web cannot fetch, and the request is served by gpt56_terra whatever model was asked for.
PPLX_INLINE = "直接在回答正文里输出完整文档（Markdown），不要生成、附加或引用文件。"

sys.path.insert(0, str(ROOT))
from render_pplx import citations_md  # noqa: E402


def load_arm(arm_id):
    spec = json.loads((ROOT / "arms.json").read_text(encoding="utf-8"))
    task = (ROOT / spec["task"]).read_text(encoding="utf-8")
    for arm in spec["arms"]:
        if arm["id"] == arm_id:
            return arm, task
    raise SystemExit(f"unknown arm {arm_id}")


def pplx_prompt(task):
    kept = [line for line in task.splitlines() if not line.strip().startswith(PPLX_DROP)]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip() + "\n\n" + PPLX_INLINE


def cc_prompt(task):
    skill = ".claude/skills/deep-search"
    return (
        "/deep-search " + task.strip() + "\n\n---\n"
        "外层说明（Claude Code，benchmark 固定设置）：\n"
        f"- skill 目录是 {skill}。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。\n"
        "- 工人用 subagent_type \"research-worker\"（模型已由外层固定，不要传 model）。\n"
        f"- 检索走 Perplexity：在每份简报里写明工人用 `{skill}/scripts/pplx-safe search \"<query>\" --json --timeout 180` "
        "检索（每个工人最多 4 次），再用 WebFetch 打开引用里的一手页面取原句。本次运行没有 WebSearch。\n"
        "- 当前目录之外的文件与本任务无关，不要读。\n"
    )


def other_prompt(task, harness, worker_line, fetch):
    skill = ".claude/skills/deep-search"
    return (
        task.strip() + "\n\n---\n"
        f"外层说明（{harness}，benchmark 固定设置）：\n"
        f"- 用 deep-search skill 完成上面的任务：先完整读取 {skill}/SKILL.md（按需读 references/），严格按它执行。"
        "工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。\n"
        f"- {worker_line}\n"
        f"- 检索走 Perplexity：在每份简报里写明工人用 `{skill}/scripts/pplx-safe search \"<query>\" --json --timeout 180` "
        f"检索（每个工人最多 4 次），再用 {fetch} 或 curl 打开引用里的一手页面取原句。不要用内置的网页搜索工具。\n"
        "- 当前目录之外的文件与本任务无关，不要读。\n"
    )


def worker_body(skill=SKILL):
    text = (Path(skill) / "agents" / "research-worker.md").read_text(encoding="utf-8")
    _, front, body = text.split("---", 2)
    desc = re.search(r"^description:\s*(.+)$", front, re.M).group(1).strip()
    return desc, body.strip()


def worker_agent(model, skill=SKILL, extra_tools=()):
    text = (Path(skill) / "agents" / "research-worker.md").read_text(encoding="utf-8")
    _, front, body = text.split("---", 2)
    desc = re.search(r"^description:\s*(.+)$", front, re.M).group(1).strip()
    return {
        "research-worker": {
            "description": desc,
            "prompt": body.strip(),
            "model": model,
            "tools": ["Bash", "WebFetch", "Read", "Write", "Grep", "Glob", *extra_tools],
        }
    }


def fresh_dir(path, force):
    if path.exists():
        if not force:
            raise SystemExit(f"{path} exists; pass --force to overwrite")
        shutil.rmtree(path)
    path.mkdir(parents=True)


def run_pplx(arm, task, out):
    prompt = pplx_prompt(task)
    (out / "prompt.md").write_text(prompt + "\n", encoding="utf-8")
    t0 = time.time()
    proc = subprocess.run(
        [str(SKILL / "scripts" / "pplx-safe"), "search", prompt, "--model", arm["model"],
         "--json", "--timeout", "2400" if arm.get("mode") else "600"]
        + (["--mode", arm["mode"]] if arm.get("mode") else []),
        capture_output=True, text=True,
    )
    secs = round(time.time() - t0, 1)
    (out / "01.json").write_text(proc.stdout, encoding="utf-8")
    (out / "01.err").write_text(proc.stderr, encoding="utf-8")
    meta = {"arm": arm, "returncode": proc.returncode, "seconds": secs}
    if proc.returncode == 0:
        data = json.loads(proc.stdout)
        meta["model_reported"] = data.get("model")
        meta["citations"] = len(data.get("citations") or [])
        report = f"{data['answer'].rstrip()}\n\n## Citations\n\n{citations_md(data, snippets=False)}\n"
        (out / "report.md").write_text(report, encoding="utf-8")
    return meta


def collect(work, out):
    for name in ("report.md", "transcript.jsonl", "stderr.txt"):
        if (work / name).exists():
            shutil.copy2(work / name, out / name)
    # only the skill's artifacts; workers leave raw downloads (tens of MB) elsewhere under ds/
    ds = work / "ds"
    names = ["brief.md", "grid.md", "log.md", "report.md", "notes", "snapshots"]
    names += sorted(p.name for p in ds.glob("audit*.md")) if ds.exists() else []
    for name in names:
        src = ds / name
        if src.is_dir():
            shutil.copytree(src, out / "ds" / name, dirs_exist_ok=True)
        elif src.exists():
            (out / "ds").mkdir(exist_ok=True)
            shutil.copy2(src, out / "ds" / name)


def run_logged(cmd, work, env=None):
    t0 = time.time()
    with open(work / "transcript.jsonl", "w", encoding="utf-8") as fo, \
            open(work / "stderr.txt", "w", encoding="utf-8") as fe:
        proc = subprocess.run(cmd, cwd=work, stdout=fo, stderr=fe, env=env)
    return proc.returncode, round(time.time() - t0, 1)


def run_kimi(arm, task, out, force):
    """Kimi Code: lead model via -m; workers pinned through a throwaway KIMI_CODE_HOME whose
    config.toml is the user's plus [secondary_model] force=true and an extra agent dir."""
    work = ARENA / arm["id"]
    fresh_dir(work, force)
    shutil.copytree(SKILL, work / ".claude" / "skills" / "deep-search")
    agents = ARENA / f"{arm['id']}-agents"
    home = ARENA / f"{arm['id']}-kimi-home"
    for d in (agents, home):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    desc, body = worker_body()
    (agents / "research-worker.md").write_text(
        f"---\nname: research-worker\ndescription: {desc}\ndisallowedTools: WebSearch\n---\n\n{body}\n"
        "\n你的最后一条消息就是交给主 agent 的完整交付（上面的 ≤ 10 行摘要）。\n", encoding="utf-8")
    user_cfg = (Path.home() / ".kimi-code" / "config.toml").read_text(encoding="utf-8")
    cfg = (f'extra_agent_dirs = ["{agents}"]\n' + user_cfg.rstrip() + "\n\n[secondary_model]\n"
           f'default_model = "{arm["worker"]}"\nforce = true\n')
    (home / "config.toml").write_text(cfg, encoding="utf-8")
    os.chmod(home / "config.toml", 0o600)
    cap = arm.get("max_parallel")
    batch = (f"模型提供方限制并发：同时最多 {cap} 个工人在跑，一轮工人多于 {cap} 个就分批派，每批等返回后再派下一批。"
             if cap else "")
    prompt = other_prompt(task, "Kimi Code",
                          "工人用 subagent_type \"research-worker\"（模型由外层决定，不要传 model）。一轮的工人用一次 AgentSwarm"
                          "（prompt_template 写 {{item}}，items 是各份完整简报）或同一步里多个前台 Agent 调用并行派出，"
                          "等全部返回再收束；不要用后台任务、sleep 或定时唤醒来等。" + batch,
                          "FetchURL")
    (out / "prompt.md").write_text(prompt, encoding="utf-8")
    env = dict(os.environ, KIMI_CODE_HOME=str(home))
    if cap:
        env["KIMI_CODE_AGENT_SWARM_MAX_CONCURRENCY"] = str(cap)
    cmd = [str(Path.home() / ".kimi-code" / "bin" / "kimi"), "-p", prompt, "-m", arm["lead"],
           "--output-format", "stream-json",
           "--skills-dir", str(work / ".claude" / "skills")]
    try:
        rc, secs = run_logged(cmd, work, env)
    finally:
        if (home / "sessions").exists():  # subagent wire logs: which model each worker really ran
            shutil.copytree(home / "sessions", work / "kimi-sessions", dirs_exist_ok=True)
        shutil.rmtree(home, ignore_errors=True)  # holds a copy of the user's provider keys
    collect(work, out)
    return {"arm": arm, "returncode": rc, "seconds": secs, "arena": str(work)}


def _proxy_env():
    """Grok Build ignores the macOS system proxy; pass one explicitly if PS_PROXY is set."""
    proxy = os.environ.get("PS_PROXY")
    if not proxy:
        return {}
    no_proxy = os.environ.get("PS_NO_PROXY", "localhost,127.0.0.1,::1")
    return {"HTTPS_PROXY": proxy, "HTTP_PROXY": proxy, "https_proxy": proxy, "http_proxy": proxy,
            "NO_PROXY": no_proxy, "no_proxy": no_proxy}


GROK_ENV = _proxy_env()


def run_grok(arm, task, out, force):
    """Grok Build: lead via -m; research-worker is a project agent file pinned to the worker model."""
    work = ARENA / arm["id"]
    fresh_dir(work, force)
    shutil.copytree(SKILL, work / ".claude" / "skills" / "deep-search")
    desc, body = worker_body()
    (work / ".grok" / "agents").mkdir(parents=True)
    (work / ".grok" / "agents" / "research-worker.md").write_text(
        f"---\nname: research-worker\ndescription: {desc}\nmodel: {arm['worker']}\n---\n\n{body}\n",
        encoding="utf-8")
    prompt = other_prompt(task, "Grok Build",
                          f"工人用 spawn_subagent 派出，每次调用都必须显式传 model=\"{arm['worker']}\"（外层固定的工人模型）。"
                          "这个外层没有 research-worker 类型：把 .claude/skills/deep-search/agents/research-worker.md 的正文"
                          "（工人规则和笔记格式）整段放进每份简报。一轮的所有工人在同一条消息里并行派出，再用一次 "
                          "get_command_or_subagent_output 等全部返回后收束；不要用 sleep 或定时唤醒来等。",
                          "web_fetch")
    (out / "prompt.md").write_text(prompt, encoding="utf-8")
    cmd = [str(Path.home() / ".grok" / "bin" / "grok"), "-p", prompt, "-m", arm["lead"],
           "--output-format", "streaming-messages-json", "--permission-mode", "bypassPermissions",
           "--always-approve", "--disallowed-tools", "web_search", "--cwd", str(work)]
    rc, secs = run_logged(cmd, work, dict(os.environ, **GROK_ENV))
    collect(work, out)
    return {"arm": arm, "returncode": rc, "seconds": secs, "arena": str(work)}


def run_cc(arm, task, out, force):
    work = ARENA / arm["id"]
    fresh_dir(work, force)
    shutil.copytree(SKILL, work / ".claude" / "skills" / "deep-search")
    prompt = cc_prompt(task)
    (out / "prompt.md").write_text(prompt, encoding="utf-8")
    cmd = [
        "claude", "-p", prompt,
        "--model", arm["lead"],
        "--output-format", "stream-json", "--verbose",
        "--dangerously-skip-permissions",
        "--strict-mcp-config",
        # ScheduleWakeup/CronCreate: in -p mode a lead that "waits" with a wakeup ends its turn, the
        # process exits and every running worker is killed (cc-opus-opus attempt 1, 2026-09-23).
        "--disallowedTools", "WebSearch", "ScheduleWakeup", "CronCreate",
        "--settings", json.dumps({"sandbox": {"enabled": False}}),
        "--agents", json.dumps(worker_agent(arm["worker"]), ensure_ascii=False),
        "--max-budget-usd", str(arm.get("max_budget_usd", 150)),
    ]
    t0 = time.time()
    with open(work / "transcript.jsonl", "w", encoding="utf-8") as fo, \
            open(work / "stderr.txt", "w", encoding="utf-8") as fe:
        proc = subprocess.run(cmd, cwd=work, stdout=fo, stderr=fe)
    secs = round(time.time() - t0, 1)
    result = {}
    for line in (work / "transcript.jsonl").read_text(encoding="utf-8").splitlines():
        if line.startswith("{") and '"type":"result"' in line.replace(" ", ""):
            result = json.loads(line)
    collect(work, out)
    keep = ("is_error", "terminal_reason", "duration_ms", "num_turns", "total_cost_usd",
            "modelUsage", "subagent_stats", "permission_denials")
    return {"arm": arm, "returncode": proc.returncode, "seconds": secs, "arena": str(work),
            **{k: result.get(k) for k in keep}}


def main(argv):
    if len(argv) < 2:
        raise SystemExit("usage: run_arm.py ARM_ID [--force]")
    arm, task = load_arm(argv[1])
    force = "--force" in argv
    out = RUNS / arm["id"]
    fresh_dir(out, force)
    runner = {"pplx": lambda: run_pplx(arm, task, out), "claude-code": lambda: run_cc(arm, task, out, force),
              "kimi-code": lambda: run_kimi(arm, task, out, force), "grok-build": lambda: run_grok(arm, task, out, force)}
    meta = runner[arm["harness"]]()
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = out / "report.md"
    print(f"{arm['id']}: exit {meta['returncode']}, {meta['seconds']}s, "
          f"report {'%d chars' % len(report.read_text(encoding='utf-8')) if report.exists() else 'MISSING'}")
    return 0 if report.exists() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
