# e004 等待窗口只许等整批

## 证据

这四组没有 `judge/**.json`（盲评还没落盘），失分用运行状态和成稿停在哪一段来记。

`g000a` / `s000a` / `g002` / `s002` 各 3 题，12 次 `status` 全是 `timeout` 或 `error`，没有一份 `audit.md`。`lead_web` 从 46 到 197。

- `g000a/agent-protocols`：`lead_web` 175，75 分钟超时，快照只有 `report.r1.md`。streaming transcript 里，第一次 `get_command_or_subagent_output`（6 个 id）之后、主 agent 写出「六份笔记都回来了」之前，同一会话连续 `web_fetch` 175 次，返回的是整页正文（合计约 2.1MB，单次最大约 6.6 万字符）。log 的 R1 段已经写好下一轮只派厂商核验，进程在这之前被杀掉，终审没发生。
- `g002/agent-protocols`：`lead_web` 117，只等了 1 次，spawn 停在 R1 的 6 个。log 写明厂商列全空，所以第 0 节不给厂商结论，并计划再派 6 个工人；成稿就停在这里。`golden` 0.5，`error_during_execution`，这次运行累计 input 约 3000 万 token。
- `s002/agent-protocols`：`lead_web` 170（其中 `web_fetch` 123、`web_search` 47）。log 末段已经决定进入终审、预计 spawn 1，目录里没有 `audit.md`，`status` error。
- `s000a/prompt-caching`：log 末段同样是「终审，预计 spawn 1」，`spawns` 17 对得上三轮加这一名审稿，仍无 `audit.md`，75 分钟超时，`lead_web` 132。

对照主会话 `chat_history`：这 12 次里主 agent 自己的 `tool_calls` 没有 `web_fetch` / `web_search`，等待返回的是工人 ≤10 行摘要。`evaluate.py` 只把 `parent_tool_use_id` 为空的工具算进 `lead_web`，而 Grok 的 streaming 把工人抓页写进父会话且该字段一直为空。所以公布的 `lead_web` 主要是工人流量。

技能对此的反应写在 `references/harness.md` Grok 节，而 12 次运行的主 agent 都读了这一节：它把「等待期间自己抓了几十上百次」记成事实，并写「结果更全（召回最高）」，接着建议在外层再喊一句口号，或 `--disallowed-tools web_fetch`。后一条会连工人和终审工人的抓页一起拿掉。口号已经在 SKILL.md 里（「不亲自搜索网页」），没有给出等待窗口里的替代动作。

这不是 journal 里弃掉的 e001（成稿自洽改稿）或收下的 e002（边界主张先反证）。那两次改的是收束和笔记，这次只改等待窗口里主 agent 的下一个动作。

## 假设

主 agent 在一批工人返回之前，如果手里没有「只许等」的替代动作，就会把父会话里冒出来的页面当成自己的调研接着翻；harness 里「自己抓更全」会强化这件事。把这一窗口收成可执行的两步（先把缺口写成 `log.md` 的 `待查：`，然后一次等整批或结束回合；想开的页面留给下一轮工人），成稿就只能源自笔记。在 60 分钟上限里，少掉等待窗口中的抓页回合，更可能做完下一轮和终审，而不是交一份 R1 草稿。

可检验：相对这 12 次，`status` 里 `ok` 变多，`audit.md` 出现，`minutes` 下降；盲评上 coverage / doubts / accuracy 上升，因为第 0 节和点名疑点不再停在「这轮没查」。`lead_web` 本身可能降不多——见风险。

## 改动

只改副本 `evolve/candidates/e004/skill/`。没改 `references/worker.md`、`agents/research-worker.md`：工人自己的搜索和终审回原页保持原样。

- `SKILL.md`：扩展一节写成等待窗口的动作序列（`待查：` 一行 → 一次等整批或结束回合；窗口内不开页面、不取 URL、不再 spawn）。返回之后想开页面就写成下一轮窄简报。终审写明回原页只由审稿工人做。硬规则改成工具级禁令，并写明不约束工人和终审。
- `references/harness.md`：删掉 Grok 节里「自己抓更全」和 `--disallowed-tools web_fetch`。换成下一条消息只能是一次 `get_command_or_subagent_output`（或结束回合），父会话里的抓页记录不要顺着再抓，并写明不要禁用工人的 `web_fetch` / `web_search`。共用的「怎么等」和 Claude 的结束回合补上同一条：窗口里不开页面，缺口记 `待查：`。

## 预期变好的维度 / 指标

- 运行能走完：`status` 从 timeout/error 转向 ok；出现 `audit.md`；`minutes` 下降（不再把等待窗口花在抓页上）。
- 盲评：coverage（厂商列、点名疑点不再停在 R1）、doubts / accuracy（主张来自笔记摘录，而不是主上下文里的原始页）。`traceable` 不下降。
- 底线：`len_ok` 仍全过；工人照旧搜索，终审仍可回原页，所以不靠少查来源换分数。`cost_usd` 应不高于在位者的 1.5 倍。

## 风险

- `lead_web` 的计数把工人抓页算进父会话。主 agent 本来就很少自己抓的那些运行，这个数不会掉到 0。不要用 `lead_web` 单独判定成败。
- 若这 12 次的主 agent 已经在正确等待，行为不变，分数可能持平，同时 `skill_chars` 略增。
- 等待窗口写得太死：重派被推迟到错误的时机，或收束时不敢读笔记。文本把重派放在返回之后、收束仍只读笔记，用来避开这个误伤。
- 删掉「自己抓更全」之后，如果主 agent 抓页确实曾提高召回，coverage 可能下降。换来的是终审和下一轮还来得及做。
