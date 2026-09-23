# 外层（harness）适配

SKILL.md 里的流程不变：R0 → 扩展 → 收束 → 观察 → 下一步 → 终审。换外层时只改三件事：
「一次 spawn」具体是什么调用、工人用什么取数、并发和失败谁来管。任务提示词里依赖外层的句子也按下表改。

| 外层 | 一次 spawn = | 选工人模型 | 等一批的正确方式 | 状态 |
|---|---|---|---|---|
| Claude Code | 一次 Agent 调用（或一次 SendMessage 追问） | `research-worker` 定义里的 `model`，或 Agent 调用传 `model` | 同一条消息发出整批，然后直接结束回合，完成通知会唤醒你 | bench 已测 |
| Kimi Code（≥ 0.36） | 一次 Agent 调用，或 AgentSwarm 里的一项 | `config.toml` 的 `[secondary_model] default_model`（`force = true` 钉死） | 一次 AgentSwarm，或同一步多个前台 Agent 调用 | bench 已测 |
| Grok Build | 一次 `spawn_subagent` | 每次调用显式传 `model` | 同一条消息发出整批，再用一次 `get_command_or_subagent_output`（wait_all） | bench 已测 |
| 纯 Perplexity | 一次 `pplx-safe search` | `--model`（配额用完会被静默回退，见下） | 并行进程 | bench 已测 |
| Codex CLI / 任意带 shell 的外层 | 一个后台 `codex exec` 或 `claude -p` 进程 | 进程参数 | shell 的 `&` + `wait` | 未测 |

所有外层共用一条：**等待就是阻塞在「等整批」那一步，或者结束回合交给通知**。不要用 sleep、定时唤醒、轮询来等。

## Claude Code（agent team）

- 工人类型：有 `research-worker`（本 skill 的 `agents/research-worker.md`，或启动时 `--agents` 定义）就用它；没有就用
  `general-purpose`，并在 Agent 调用里显式传 `model`（`sonnet` / `opus`），同时把 `references/worker.md` 的规则整段放进简报。
- 一轮的所有简报放在**同一条消息**里发出多个 Agent 调用，`name` 用 `r<轮>-<slug>`，方便之后 SendMessage 追问。
- 工人默认在后台跑，完成时会通知你。等整批通知到齐再收束；不要轮询，也不要在等的时候自己去搜。
- 等待就是直接结束本回合。不要用 ScheduleWakeup、CronCreate、`sleep` 来「等」：headless（`claude -p`）下，
  主 agent 排了唤醒就会结束会话，进程退出时所有还在跑的工人被杀掉（bench 里 cc-opus-opus 第 1 次就这样丢了 10 个工人）。
  跑 headless 时最好直接用 `--disallowedTools ScheduleWakeup CronCreate`。
- 追问优先 SendMessage 给原工人（它保留了读过的页面），比新 spawn 便宜；同样计入 turn。
- 工人不再往下派工人。范围很大时（> 12 个实体）才考虑两层：给 sub-leader 用 `general-purpose`，让它对自己那一枝跑 R1+收束，
  只交回枝笔记（主张 + 来源），不交成稿。默认不开。
- 不用 Workflow 工具编排这套流程（团队约定：dynamic workflow 不作为推荐实现）。

## Kimi Code

- 版本要 ≥ 0.36（2026-08-13 起才有 subagent 模型池）；0.34 下子 agent 一律继承主模型。bench 用的是 2.0.2。
- 工人类型：把 `agents/research-worker.md` 放进 agent 目录（项目级 `.kimi-code/agents/`、`.agents/agents/`，或 `config.toml`
  顶层 `extra_agent_dirs`），用 `subagent_type: "research-worker"` 派。agent 文件里的 `model` 字段会被忽略。
- 工人模型：`[secondary_model] default_model = "<alias>"`，要钉死就加 `force = true`（此时 Agent 调用不接受 `model` 参数）。
- 一轮用一次 AgentSwarm（`prompt_template` 写 `{{item}}`，`items` 放各份完整简报；AgentSwarm 必须是该步唯一的工具调用），
  或同一步多个前台 Agent 调用。`kimi -p` 下 subagent 默认不超时。
- skill：`--skills-dir <父目录>`，或放进 `.kimi-code/skills/` / `.agents/skills/`；也可以在提示词里让主 agent 先读 SKILL.md。
- `kimi -p` 不能和 `--auto` / `--yolo` 同用；权限按 `config.toml` 的 `default_permission_mode`。

## Grok Build

- `spawn_subagent` 没有「选 agent 类型」的参数，项目里的 `.grok/agents/research-worker.md` 能被发现（`grok inspect`），
  但主 agent 选不到它，派出来的是 `general-purpose`。所以：**每次调用都显式传 `model`**，并把 `agents/research-worker.md` 的正文整段放进简报。
- 用户配置里 `[subagents.models] general-purpose = ...` 会给没传 `model` 的工人定模型；显式 `model` 参数优先。
- 工人默认后台运行；同一条消息发出整批后，用一次 `get_command_or_subagent_output`（传全部 id、`timeout_ms` 给足）等全部完成。
- grok-4.7 主 agent 不守「主 agent 不抓网页」：bench 里它派出 R1 的 10 个工人后，等待期间自己 `web_fetch` 了 88 次，R2 又 15 次。
  结果更全（v1 召回最高），但分工被打破、主上下文里灌进了原始页面。要严格分工，就在外层提示词里再强调一次，或试
  `--disallowed-tools web_fetch`（是否同时去掉工人的 web_fetch 未验证）。
- Grok Build 不读 macOS 系统代理；网络需要代理时，启动 grok 要显式带上 HTTPS_PROXY / NO_PROXY（bench 的 runner 读 `PS_PROXY`、`PS_NO_PROXY`）。
- 自定义 Responses 后端的模型（bench 里是一个本地反代提供的 `swe-2`）若返回的 `usage` 缺 `output_tokens_details`，Grok 会报
  `serialization error` 直接失败，主模型和工人都一样。先用一句 `grok -p "reply ok" -m <model>` 试通再排进 bench。

## 纯 Perplexity

- 每份简报的窄问题 → 一次 `pplx-safe search "<问题>" --json`，答案和 citations 就是笔记。
- 这类笔记没有原文摘录，按规则全部算 `secondary`；收束时要在第 5 节说明「未经一手来源核对」。
- 只能做「一轮扩展 + 一次收束」或「多轮但每轮都是搜索答案」，没有追问能力。
- 提示词里写「产出文档」时，Perplexity 会改成「生成文件」：正文只剩 1–2k 字的文件摘要，文件本身 `pplx-web` 拿不到。
  要在提示词末尾加一句「直接在回答正文里输出完整文档，不要生成、附加或引用文件」。

## Codex CLI / 通用 shell 外层（未测）

- 一个工人 = 一个后台进程：`codex exec -s workspace-write "<worker.md 规则 + 简报>"`，或 `claude -p --model sonnet "<同上>"`。
  用 shell 的 `&` + `wait` 控制一批，进程退出码非 0 记为失败。
- 进程的笔记写到简报里的路径；主 agent 只读笔记文件，不读进程的完整输出。

## 已知坑：Perplexity

`pplx-web` 是本仓库之外的本地工具（Perplexity Pro 网页会话客户端），`scripts/pplx-safe` 只是给它加并行安全；用 `PPLX_WEB_SCRIPT` 指向它的 `pplx_web.py`。没有它就让工人用外层自带的网页搜索。

- **并行写 cookie**：`pplx-web` 每次搜索都会把 cookie 写回 `~/.config/perplexity-web/cookies.json`，临时文件名固定为
  `cookies.json.tmp`，多进程同时跑时后一个 `replace` 报 `FileNotFoundError`。`scripts/pplx-safe` 给每个进程一个临时 HOME
  和一份 cookie 副本，并行不会互相踩；代价是这次刷新的 cookie 不会写回主文件。
- **配额回退**：Pro 配额（`/rest/rate-limit/all` 的 `remaining_pro`）用完后，除 `pplx_pro`（Best）外，请求的模型会被静默换成
  `gpt56_terra(_thinking)`，返回 JSON 的 `model` 字段是实际模型。比较 Perplexity 模型前先看配额，结果里要核对 `model`。
- **研究模式**：`pplx-safe --mode research`（`pplx_alpha`）请求能返回，但 `remaining_research` 不减、实际模型是回退模型，
  说明没有进入 Deep Research；`agentic_research` 直接返回空答案。经 `pplx-web` 暂时用不了这两种模式。
- 遇到 `AUTHENTICATION` 错误时，按 perplexity-research skill 的说明在 Chrome 里重新登录，再跑一次 `pplx-web login`。
