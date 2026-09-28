#!/usr/bin/env python3
"""Run one proposer agent (Grok Build by default) in a sandbox copy of the repo.

usage: propose.py EXP --direction TEXT --evidence EXP[,EXP...] [--model grok-4.7] [--base DIR] [--note TEXT]

The sandbox holds what program.md lets a proposer read -- README, program.md, results.tsv,
journal.md, the task prompts (no golden.json / answers.md), the incumbent skill and the evidence
runs (no transcripts) -- so hidden answers and the harness are out of reach by construction.
Only candidates/EXP/{skill,hypothesis.md} come back; skill.diff is regenerated here, and added
lines that mention task-specific terms are flagged.
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
sys.path.insert(0, str(REPO / "bench"))
from run_arm import GROK_ENV  # noqa: E402

GROK = str(Path.home() / ".grok" / "bin" / "grok")
ARENA = Path(os.environ.get("PS_ARENA") or Path(tempfile.gettempdir()) / "ps-arena") / "propose"

BRIEF = """你是 deep-search skill 自进化实验的提案者。实验号 {exp}，方向：{direction}。当前目录就是仓库（精简副本）。
先读 evolve/program.md（尤其「不能做什么」），再读 evolve/results.tsv、evolve/journal.md、skills/deep-search/ 全部文件。
证据：evolve/runs/<实验号>/<任务>/（report.md、prompt.md、ds/log.md、ds/grid.md、ds/brief.md、ds/notes/、ds/audit*.md、ds/snapshots/、meta.json），
盲评判决 evolve/runs/<实验号>/judge/**.json（reason、errors_x、errors_y、dims；x 是该实验自己的运行）。这次可用的实验号：{evidence}。
任务原文在 bench/tasks/<任务>/task.md。
运行设置（固定，不能改）：{arm_desc}，参数 --rounds 3 --workers 6 --budget 9000。
{note}
要做的：
1. 从证据里找一个具体失分点或浪费（写出是哪几次运行、哪一段、判决里哪条理由），提出一个可检验的假设。不要重复 journal.md 里已经弃掉的想法，除非你能说清这次有什么不同。
2. 执行 cp -R skills/deep-search evolve/candidates/{exp}/skill，只改这个副本。改动围绕这一个想法，越小越好；删规则也是合法的实验。
3. 不写任何领域事实或任务相关提示（产品名、厂商名、字段名、结论），skill 必须对任意调研题都成立。不改其他任何文件。
4. 写 evolve/candidates/{exp}/hypothesis.md：证据 → 假设 → 改动（文件、大意）→ 预期变好的维度/指标 → 风险。
最后回复 ≤ 6 行：一句话描述（会写进 results.tsv）、改了哪些文件、预期效果。
"""


def build_sandbox(exp, evidence, base):
    box = ARENA / exp
    if box.exists():
        shutil.rmtree(box)
    (box / "evolve" / "runs").mkdir(parents=True)
    for name in ("README.md",):
        shutil.copy2(REPO / name, box / name)
    for name in ("program.md", "results.tsv", "journal.md", "INCUMBENT", "README.md"):
        if (ROOT / name).exists():
            shutil.copy2(ROOT / name, box / "evolve" / name)
    for t in (REPO / "bench" / "tasks").iterdir():
        if (t / "task.md").exists():
            (box / "bench" / "tasks" / t.name).mkdir(parents=True)
            shutil.copy2(t / "task.md", box / "bench" / "tasks" / t.name / "task.md")
    shutil.copytree(base, box / "skills" / "deep-search", ignore=shutil.ignore_patterns("__pycache__"))
    for e in evidence:
        if (ROOT / "runs" / e).exists():
            shutil.copytree(ROOT / "runs" / e, box / "evolve" / "runs" / e,
                            ignore=shutil.ignore_patterns("transcript.jsonl", "stderr.txt", "judge.v1-*"))
    (box / "evolve" / "candidates").mkdir()
    for e in evidence:  # earlier proposals: hypothesis + diff only (not the skill copy)
        src = ROOT / "candidates" / e
        if src.exists():
            (box / "evolve" / "candidates" / e).mkdir()
            for name in ("hypothesis.md", "skill.diff"):
                if (src / name).exists():
                    shutil.copy2(src / name, box / "evolve" / "candidates" / e / name)
    return box


def leak_terms():
    terms = set()
    for t in (REPO / "bench" / "tasks").iterdir():
        g = t / "golden.json"
        if g.exists():
            for c in json.loads(g.read_text(encoding="utf-8"))["claims"]:
                for group in c["groups"]:
                    terms.update(n for n in group if len(n) >= 4 and not n.isdigit())
    return sorted(terms)


def main(argv):
    exp = argv[1]
    opts = {argv[i][2:]: argv[i + 1] for i in range(2, len(argv) - 1, 2) if argv[i].startswith("--")}
    evidence = [e for e in opts.get("evidence", "").split(",") if e]
    base = Path(opts.get("base", REPO / "skills" / "deep-search")).resolve()
    model = opts.get("model", "grok-4.7")
    arm_desc = opts.get("arm_desc", "Grok Build，grok-4.7 主 agent → grok-4.7 或 swe-2 工人，web_search + web_fetch")
    box = build_sandbox(exp, evidence, base)
    prompt = BRIEF.format(exp=exp, direction=opts["direction"], evidence="、".join(evidence) or "无",
                          arm_desc=arm_desc, note=opts.get("note", ""))
    (box / "brief.txt").write_text(prompt, encoding="utf-8")
    t0 = time.time()
    if model.startswith("swe"):  # claude-devin routes every model name to swe-2-max via devin2api
        cmd = [str(Path.home() / ".local" / "bin" / "claude-devin"), "-p", prompt, "--model", model,
               "--output-format", "stream-json", "--verbose", "--dangerously-skip-permissions",
               "--strict-mcp-config", "--disallowedTools", "Agent", "WebSearch", "WebFetch"]
        env = dict(os.environ)
    else:
        cmd = [GROK, "-p", prompt, "-m", model, "--output-format", "streaming-messages-json",
               "--permission-mode", "bypassPermissions", "--always-approve", "--no-subagents",
               "--disable-web-search", "--cwd", str(box)]
        env = dict(os.environ, **GROK_ENV)
    with open(box / "transcript.jsonl", "w") as fo, open(box / "stderr.txt", "w") as fe:
        proc = subprocess.Popen(cmd, cwd=box, stdout=fo, stderr=fe, env=env,
                                stdin=subprocess.DEVNULL, start_new_session=True)
        try:
            proc.wait(timeout=int(opts.get("timeout", 2400)))
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, 15)
            proc.wait()
    final = ""
    for line in (box / "transcript.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
        if '"type":"result"' in line[:40]:
            try:
                final = json.loads(line).get("result") or ""
            except json.JSONDecodeError:
                pass
    src = box / "evolve" / "candidates" / exp
    dst = ROOT / "candidates" / exp
    if not (src / "skill").exists():
        print(f"[propose] {exp}: no candidate produced ({round((time.time() - t0) / 60, 1)} min)\n{final[:800]}")
        return 1
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    shutil.copytree(src / "skill", dst / "skill", ignore=shutil.ignore_patterns("__pycache__"))
    if (src / "hypothesis.md").exists():
        shutil.copy2(src / "hypothesis.md", dst / "hypothesis.md")
    shutil.copy2(box / "brief.txt", dst / "brief.txt")
    diff = subprocess.run(["diff", "-ruN", str(base), str(dst / "skill")], capture_output=True, text=True).stdout
    diff = diff.replace(str(base), "a/skills/deep-search").replace(str(dst / "skill"), "b/skills/deep-search")
    (dst / "skill.diff").write_text(diff, encoding="utf-8")
    added = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    leaks = [t for t in leak_terms() if t.lower() in added.lower()]
    (dst / "proposer.md").write_text(
        f"model: {model}\nminutes: {round((time.time() - t0) / 60, 1)}\nleak_terms: {leaks}\n\n{final}\n", encoding="utf-8")
    n_add = sum(1 for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    n_del = sum(1 for l in diff.splitlines() if l.startswith("-") and not l.startswith("---"))
    print(f"[propose] {exp}: +{n_add}/-{n_del} lines, leak_terms={leaks}, {round((time.time() - t0) / 60, 1)} min")
    print(final[:1200])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
