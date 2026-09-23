# bench 结果：api-protocol-v2（2026-09-23）

**一句话**：4 个「外层 + 模型 + deep-search skill」方法全部明显好于 8 个单次 Perplexity 调用；两个不同家族的评审（Opus 5.5、Grok 4.7）各跑两遍、共 4 遍，前四名顺序完全一致。
Opus→Sonnet 与 Opus→Opus 同在第一档，Sonnet 工人版便宜 44%、快 14%，但把用户点名的智谱问题答错了一处。Perplexity 模型之间这轮没法比：Pro 配额用完，8 个里有 7 个被静默回退到同一个模型。

## 题和方法

- 任务：`tasks/api-protocol/task.md`，团队 2026-09-23 给出的提示词原文，所有方法同一份。
- **直接调 Perplexity skill**（`pplx-*`）：`pplx-web` 单次请求，答案即报告。模型取 Perplexity 选择器里 Pro 可用的 8 个（有 Thinking 变体的用 Thinking）。按外层微调提示词：去掉只对多 agent 有意义的三句，末尾加「直接在回答正文里输出完整文档」（不加这句时 Perplexity 把「产出文档」当成生成文件，正文只剩 1–2k 字摘要）。
- **外层 + 模型调 deep-search skill**：主 agent → 工人。工人检索走 Perplexity（`pplx-safe`），打开一手页面用各外层自己的抓取工具（或 curl）；各外层的原生网页搜索关掉或禁用。每个外层按 `skills/deep-search/references/harness.md` 微调「怎么派、怎么等、怎么选工人模型」。
  - Claude Code：Opus 5.5 → Opus 5.5；Opus 5.5 → Sonnet 5
  - Kimi Code 2.0.2：GLM-5.3 → GLM-5.3-Flash（GLM Coding Plan，同时最多 3 个工人）
  - Grok Build：grok-4.7 → grok-4.7
- 评价：
  - 盲评：报告匿名、乱序，评审只读文件不联网，8 个维度 1–10 分 + 排名。Opus 5.5 两遍、Grok 4.7 两遍（换家族，检查自家偏好）。
  - v1 golden：12 条官方文档事实的机械针（`golden.json`），只计召回。
  - 字数、用时、花费（Claude Code 取 CLI 的 list 价；Grok 取 xAI 的 cost ticks；Kimi 走 Coding Plan 订阅，无按量价）、spawn 数、skill 的自审计数、每轮快照字数。

## 结果

| arm | 模型 | Opus 评审 overall（名次） | Grok 评审 overall（名次） | v1 命中/12 | 字数 | 用时 min | 花费 $ | spawn | 自审 支撑/弱/无据/矛盾 | 快照字数轨迹 |
|---|---|---|---|---|---|---|---|---|---|---|
| cc-opus-sonnet | Opus 5.5 → Sonnet 5 | 9.0 (1.0) | 9.0 (1.0) | 9 | 19703 | 83 | 54.03 | 19 (+4 追问) | 72/12/1/2 | 19813 → 19723 → 19704 → 19703 |
| cc-opus-opus | Opus 5.5 → Opus 5.5 | 9.0 (2.0) | 8.5 (2.0) | 8 | 17898 | 96 | 96.26 | 19 (+1 追问) | 122/31/3/1 | 17919 → 17905 → 17898 → 17898 |
| kimi-glm53-glm53flash | GLM-5.3 → GLM-5.3-Flash | 8.5 (3.0) | 8.5 (3.0) | 10 | 19918 | 111 | 订阅 | 15 | 39/8/0/0 | 17933 → 19996 → 19991 → 19918 |
| grok-47-47 | grok-4.7 → grok-4.7 | 7.5 (4.0) | 8.0 (4.0) | 11 | 18659 | 91 | ≈36.24 | 15 | 20/6/0/4 | 18720 → 18696 → 18659 → 18659 |
| pplx-gemini38flash | Gemini 3.8 Flash Thinking ⇒ 实际 gpt56_terra_thinking | 5.0 (6.0) | 5.5 (7.0) | 8 | 40488 | 2 | 订阅 | – | – | – |
| pplx-sonnet5 | Claude Sonnet 5 Thinking ⇒ 实际 gpt56_terra_thinking | 5.0 (6.5) | 5.5 (7.0) | 8 | 33545 | 3 | 订阅 | – | – | – |
| pplx-gpt6sol | GPT-6 Sol Thinking ⇒ 实际 gpt56_terra_thinking | 5.0 (7.0) | 5.5 (7.0) | 8 | 40578 | 3 | 订阅 | – | – | – |
| pplx-grok46 | Grok 4.6 Thinking ⇒ 实际 gpt56_terra_thinking | 5.0 (7.0) | 6.0 (5.0) | 8 | 38171 | 3 | 订阅 | – | – | – |
| pplx-nemotron3 | Nemotron 3 Ultra ⇒ 实际 gpt56_terra_thinking | 4.5 (9.5) | 4.5 (11.0) | 6 | 35965 | 2 | 订阅 | – | – | – |
| pplx-best | Best（pplx_pro） | 4.5 (10.0) | 5.0 (10.0) | 7 | 30970 | 2 | 订阅 | – | – | – |
| pplx-glm53 | GLM-5.3 ⇒ 实际 gpt56_terra_thinking | 4.5 (10.0) | 5.0 (9.0) | 6 | 39761 | 2 | 订阅 | – | – | – |
| pplx-kimik3 | Kimi K3 ⇒ 实际 gpt56_terra_thinking | 3.5 (12.0) | 4.0 (12.0) | 9 | 32589 | 2 | 订阅 | – | – | – |

生成：`python3 bench/summarize.py`。评审明细在 `judge/claude/`、`judge/grok/`（每遍的逐维分数、确信错误、优缺点各一句）。
早一次只有 11 份报告（无 Kimi）的 Opus 评审在 `judge/claude-11docs/`，重叠方法的名次顺序与这次相同。

## 结论

1. **外层 + skill ≫ 单次 Perplexity。** 两个评审家族、4 遍排名的前四名都是 skill 方法，overall 7.5–9.0；Perplexity 全部 3.5–6.0。差距最大的维度是 downstream（下游厂商差异、用户点名的两个疑点）和 concision：Perplexity 单次答案 31–41k 字、没有长度控制，skill 方法都在 20k 预算内。Grok 评审把 Grok 自己外层的报告排第 4、把 Claude 外层的两份排 1、2，说明排名不是「Claude 评审偏爱 Claude」。
2. **Opus→Opus 对 Opus→Sonnet：质量同档，Sonnet 工人更便宜。** 评审分数并列（Opus 评审都是 9.0；Grok 评审 9.0 对 8.5），Sonnet 工人版 $54 对 $96、83 对 96 分钟。区别在精度和可追溯：
   - 用户点名的智谱问题（Q2），Opus→Opus 写对了「套餐下默认服务端模型映射」，Opus→Sonnet 在收束时把它当成无依据删掉、改成「客户端 `ANTHROPIC_DEFAULT_*_MODEL` 指定」，错了（见下节核验）。
   - Opus 工人的 R1 笔记 295 条主张全部带完整 URL 和原句；Sonnet 工人有 122 条 `src` 写成相对路径或简称，靠主 agent 收束时机械补全。
   - Opus 工人慢且啰嗦：整份下载规范逐段核对，R1 用了 40 分钟以上；重跑的 R1 笔记有 3 份超过 8000 字上限（最长 9,987），失败那次有一份 17,216。已在 skill v1.1 加工具调用预算。
3. **Kimi Code（GLM-5.3 → GLM-5.3-Flash）排第 3。** 走 GLM Coding Plan 订阅、不按量计费，v1 召回 10/12，Q2 写对；Opus 评审给它的 accuracy 最低（7.0）。缺点是 Coding Plan 限并发，只能 3 个工人一批，用时最长（111 分钟）。
4. **Grok Build（grok-4.7 → grok-4.7）v1 召回最高（11/12），评审第 4。** 它的主 agent 不守「主 agent 不抓网页」：派出 R1 的 10 个工人后自己 `web_fetch` 了 88 次、R2 又 15 次。事实覆盖因此更全（两位评审给的 accuracy 都是 skill 方法里最高：8.5、9.0），但 taxonomy（6.5、8.0）和四主流字段对照（7.0、7.5）在两位评审里都是 skill 方法中最低；Q2 没写模型映射。Claude Code 两个主 agent 的网页调用都是 0，分工守住了。
5. **「文章不许越来越长」在 4 个 skill 方法上都做到了**：所有快照都在 20,000 字预算内。Claude Code 与 Grok 每轮只减不增；Kimi 在 R2 涨了约 2,000 字（仍在预算内），之后没再涨。
6. **Perplexity 模型之间这轮不能下结论。** 账号 `remaining_pro=0`，除 Best 外 7 个请求的模型都被换成 `gpt56_terra_thinking`（`meta.json` 的 `model_reported`）。这 7 份等于同一模型的 7 次采样：评审 overall 3.5–6.0、v1 6–9，可以当作单次 Perplexity 答案的波动范围。Perplexity 的 Deep research / Agentic research 模式经 `pplx-web` 调不起来（见 `arms.json` 的 `excluded`）。
7. **v1 golden 区分度弱。** 12 条针只看关键词：skill 方法漏的多是写法不同（写「`system` 在顶层」而不是「顶层 system」、为压字数写成 `…/api/anthropic`），Perplexity 单次答案靠长度也能碰上。这轮排序以评审和人工核验为准，v1 只作参考。

## 人工核验：用户点名的两个问题

对照官方原文（2026-09-23 打开）：

- **Q1 DeepSeek 的 response 协议 vs OpenAI 文档**：DeepSeek 更新日志 2026-07-31「The official V4-Flash natively supports the Responses API format」，2026-08-13 整个 API「natively supports the OpenAI Responses API format and is specifically adapted for Codex」；Responses 指南写明 `store` 恒为 false、`previous_response_id` 与 `conversation`「Not supported (stateless API)」、不支持的参数「silently ignored」。12 份报告都提到 DeepSeek 有 Responses 形态的入口；skill 方法把上述逐字段差异写全了。cc-opus-opus 写 7-31、cc-opus-sonnet 写 8-13，两个日期都对，对应更新日志里的两条。
- **Q2 智谱的 messages vs Anthropic 官方**：`docs.bigmodel.cn/cn/guide/develop/claude` 原文「在成功配置套餐后，默认为服务端模型映射，即您界面上看到的是 Claude 模型但实际是 GLM 模型」，默认 Opus/Sonnet/Haiku 都映射到 GLM-4.7，`ANTHROPIC_DEFAULT_*_MODEL` 是改映射用的。

| | 写对服务端模型映射 | 写错 | 没写 |
|---|---|---|---|
| 方法 | cc-opus-opus、kimi-glm53-glm53flash | cc-opus-sonnet | grok-47-47、全部 8 个 pplx-* |

智谱 Anthropic 兼容端点在字段级没有官方差异文档（4 个 skill 方法都把工具、流式、`stop_reason` 等标成「官方未写」），这一点各方法一致。

## 外部参照：justinatusa/llm-api-protocols（d1d3f5d，2026-09-24）

[justinatusa/llm-api-protocols](https://github.com/justinatusa/llm-api-protocols) 是同一题目的一份三层手册：第 0 层导读、第 1 层字段对照、第 2 层 9 个细节页，另有分类说明、来源页（242 个不重复 URL）和冲突页（36 条冲突 / 未核实）。仓库里没写它是怎么做出来的。
上文「前四名都是 skill 方法」指不含手册的 12 个方法那一轮，这一节不改那句结论。手册和 bench 的单文档形态不同，所以分两种方式、各自与同一批 12 份报告放在一起盲评（Opus、Grok 各两遍，共 13 份），避免评审同时看到重叠的正文。手册正文不收进本仓库，`python3 bench/fetch_external.py` 会按固定 commit 重建这两份输入。

| 版本 | Opus 评审 overall（名次/13） | Grok 评审 overall（名次/13） | v1 命中/12 | 字数 |
|---|---|---|---|---|
| 只看第 0 层导读 | 5.0（7.5） | 5.5（9.5） | 8 | 15,505 |
| 三层全部（按 README 阅读顺序拼接） | 8.0（3.0） | 9.0（1.5） | 10 | 135,711 |

- **三层全部：第一档。** Opus 评审排在两个 Claude Code 方法之后（9.0、9.0），Grok 评审与 cc-opus-sonnet 并列第一。四主流字段级对照（mainstream 10.0 / 9.0）和来源（sourcing 10.0 / 9.5）是全部文档里最高；简洁度最低一档（concision 5.0 / 6.5），两位评审都点名「篇幅远超其他文档、各页重复链接定义」，与「不许越写越长」相悖，点名的两个疑点要跨页拼。
- **只看第 0 层：最好的入门读物，但单独交付不够。** orientation 9.0 / 8.5 是全部文档里最高：开篇四件事、术语表、「轮次型 / 条目型 × 工具参数是字符串 / 对象」的 2×2 地图、命名口诀、接新厂商的检查清单。字段对照和厂商差异都在别的文件，单独看 mainstream 4.0 / 3.5、downstream 4.0。
- **人工核验。** Q1 写对：DeepSeek 的 Responses「不存对话」、不支持 `previous_response_id`，Chat 只有 `json_object`。Q2 写对了「智谱 Anthropic 入口没有字段级文档」，还独有一条「思考力度映射在三份官方页面里对不上」；但把「Claude 模型名被换成 `glm-4.7`」写成未核实的社区报告。它引用的是 `…/guide/develop/claude/introduction`，没有引用写明「默认为服务端模型映射」的 `…/guide/develop/claude`，与 cc-opus-sonnet 属于同一类漏页。抽查「GPT-5.4 起 Chat Completions 在 `reasoning_effort` 不是 `none` 时不支持工具调用」：与 OpenAI 迁移指南原文一致（cc-opus-opus、Kimi 也写到了）。
- **对 skill 的启发。** 分层交付（一屏导读 + 写代码时查的字段表 + 按需细节页）同时满足了「快速建立认知」和「详细」，这是单文档 20k 预算做不到的；代价是总篇幅和跨页重复。skill 可以加「分层成稿」：第 0 层受 `budget` 约束、必须单独给出点名疑点的结论，细节页另计字数并要求去重。

## 各外层踩到的坑（都已写进 `skills/deep-search/references/harness.md`）

- **Claude Code**：headless（`claude -p`）下主 agent 用 ScheduleWakeup「等工人」会让会话结束、进程退出时 10 个工人全部被杀（cc-opus-opus 第 1 次，白花 $35.44，记录在 `runs/_failed-cc-opus-opus-wakeup/`）。修复：runner 禁用 ScheduleWakeup / CronCreate，skill 写明「等待 = 结束回合，交给完成通知」。
- **Kimi Code**：0.34 没有 subagent 模型池，工人一律继承主模型；升级到 2.0.2 后用 `[secondary_model] default_model + force = true` 钉住工人模型（runner 用临时 `KIMI_CODE_HOME`，不改用户配置）。`kimi -p` 不能和 `--auto`/`--yolo` 同用。GLM Coding Plan 限并发：第 1 次启动时主 agent 在 R0 就卡在 `APIEmptyResponseError`（只有思考、没有正文）重试，约 10 分钟无进展；改成同时最多 3 个工人、分批派之后跑通。
- **Grok Build**：`spawn_subagent` 没有选 agent 类型的参数，只能每次显式传 `model`、把工人规则整段放进简报；需要带用户的 Clash 代理环境；`swe-2`（本机 devin2api）返回的 usage 缺 `output_tokens_details`，Grok 直接报错，grok-47-swe2 本轮跳过。
- **Perplexity**：`pplx-web` 并行写 cookie 会撞（`pplx-safe` 已解决）；配额用完后静默换模型；「产出文档」会被当成生成文件；研究模式经 `pplx-web` 调不起来。

## 花费（list 价）

Claude Code：cc-opus-sonnet $54.03（Opus 主 $13.47、Sonnet 工人 $37.98、Haiku 抓页摘要 $2.58）；cc-opus-opus $96.26（Opus $95.06、Haiku $1.19）；失败的第 1 次 $35.44。
Grok：约 $36.24（主 + 15 个工人会话，1.24 亿 token，其中 1.01 亿命中缓存）。评审：Opus 两遍 $7.94。Kimi、Perplexity 走订阅。

## 局限

- 每个方法只跑了 1 次（n=1）。7 份同模型 Perplexity 采样显示单次答案的评审分波动约 ±1，skill 方法之间 0.5–1 分的差不应过度解读；第一档（两个 Claude Code）与第二档（Kimi、Grok）的差在 4 遍评审里方向一致。
- 评审是 LLM，只凭自身知识判「确信的错误」，漏掉了 cc-opus-sonnet 的 Q2 错误；精度上以人工核验为准，这轮只核了两个点名问题。
- skill 方法的自审计数是各方法自己派的审稿工人对照自己的笔记判的，衡量的是「成稿能否追到笔记」，不是绝对正确率。
- 花费口径不同（Claude list 价 / xAI ticks / 订阅），不能直接横比。

## 下一步

1. Perplexity 配额恢复后，串行重跑 8 个 `pplx-*`（先看 `rest/rate-limit/all` 的 `remaining_pro`，跑完核对 `model_reported`），才能回答「哪个 Perplexity 模型好」。
2. 用 skill v1.1（工人工具预算、完整 URL、反常识主张先复核）重跑 cc-opus-sonnet，看 Q2 这类错误能否消掉，以及 Opus 工人是否变快。
3. devin2api 补上 `usage.output_tokens_details` 后补跑 grok-47-swe2。
4. 每个方法至少再跑 1 次，估计方差。
