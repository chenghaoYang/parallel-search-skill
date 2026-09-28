# e002：边界主张要过反证（方向：扩展与证据）

一句话：否定/排他/强制/全称/时间边界类主张进「一屏看懂」和疑点结论之前，先找反例（自查 grid → 反证简报）；工人写这类主张要重取页面、查 changelog 最早条目；终审不许把「没找到来源」改写成否定句。

## 证据

**1. 决定胜负的硬错，大多是「边界主张」。** A/A 的 12 份判决（e000b vs e000a）里，确信错误去重后 27 条，约 16 条属于这一类：
否定（不支持/没有/未查到）、排他（唯一/只能）、强制（强制/仍需）、全称（不分代际、一律）、时间边界（仍是预览、自某版起）。
reason 里被当成决定因素的，几乎都是这一类：

- agent-protocols：4/4 份判决都靠两条定胜负——e000b「Google ❓ 未查到官方 MCP 支持声明」（一屏看懂 + 矩阵），
  e000a「MCP强制OAuth2.1+PKCE」（判决：规范写的是 authorization OPTIONAL）。另有 e000b「没有厂商发布第五个独立协议」。
- py-packaging：e000b「uv…唯一有官方 GH Action 的一体化工具」（4 份判决都点名，和它自己的 D10 列矛盾）、「Poetry 明确不会（BYOP）」；
  e000a「uv 仍在 preview（导出+校验，0.12.11+）」「conda 免费层对大型商业组织不再免费」「PyPI 系只能装 wheel」「conda 原生不感知 PyPI」。
- prompt-caching：e000a「Kimi 反而是纯手动」（判决存疑）、「OpenRouter 行：OpenAI 仍需 prompt_cache_breakpoint」、「传言已过时」；
  e000b「DeepSeek、智谱写入不加价」「其余厂商是分钟/小时级精确时长」（都和自己的矩阵矛盾）。

**2. 这些主张从哪来（三处）。**
- 工人拿一页的原句推出「没有 / 只有 / 自某版起」：e000b r1-poetry [C5] 只看了 basic-usage 页；e000a r1-uv 只读了 CHANGELOG 最新两条
  （0.12.11 / 0.12.17），status 那条的 quote 还是转述；e000a r1-domestic-scout 一人兼三家，[C1] 把 "You control caching via…" 推成「手动声明」，
  而 e000b 专职工人从 API reference 摘到 "When omitted, cache write is enabled by default"；e000a r1-mcp-authgov [C2]「强制 PKCE、所有客户端」
  的 quote 只是 "follows standard OAuth 2.1 … with PKCE conventions"。
- WebFetch 返回的是摘要：e000a r2-domestic-deepen 报告智谱缓存页「未提及 TTL」→ grid 记 `∅ 官方未写（已定向查过）`；
  e000b r1-scout 从**同一个 URL** 摘到「缓存有效期 5 分钟，命中时自动刷新」。摘要里没有 ≠ 页面上没有。
- 主 agent 收束时自己泛化成排他句（「唯一…」「写入不加价」「其余厂商…」），没对照自己的矩阵。
- 终审把「引用不对」翻成否定：e000b agent-protocols 审稿判 Google×MCP unsupported、建议「找来源或降级」，
  因为「这一步不再做新调研」，主 agent 降成 ❓ 并改了一屏看懂——这就是 4 份判决都点名的那条。

**3. 现有流程漏掉的正是它们。** 观察表只把 `❓/⚠/⚔` 和「正面的反常说法」（例：某字段已弃用、某厂已支持）送去核验。
上面这些边界主张在 grid 里全是 ✅（带原句，看着很稳）：e000a Kimi「纯手动」✅、e000b Poetry D4 BYOP ✅、e000a uv PEP751「preview」✅。
R2/R3 的核验简报几乎都在问「这条正面说法是真的吗」（e000b r2-verify-openai、r2-verify-anthropic-auto、r2-conda-lock-verify，
e000a r2-mcp-lifecycle、r2-pip-pylock-verify）。终审只对照笔记，笔记错了照样判 supported（e000b py-packaging audit A10「Poetry 未支持 PEP 751」、A24「BYOP」）。

**4. 反证有效，而且有预算。** 少数真被送去反证的否定格，一大半被推翻：e000a py-packaging R2「PDM 没有 CI 指南」（R1 是 404）→ 有官方 setup-pdm；
「pixi 对 PEP751 沉默」→ 两个官方 issue 在推进；e000a agent-protocols r2-vendor-gaps（「官方明确不支持还是我们没搜全」）之后，
厂商矩阵被判「整体也正确」。同时六次运行都提前停：spawn 10–13，R3 在 4 次运行里没派扩展工人（e000a 三题、e000b prompt-caching），
另 2 次只派 1 个；花费 $6.3–9.1（上限 $20），22–34 分钟（上限 60）。

## 假设

一句原文只能证明「这一页写了什么」，证明不了「别处没有」「后来没变」「所有情况都这样」。
把边界主张当成必须反证的对象，用现在闲着的 R2/R3 预算专门找反例，就能去掉判决里最致命、也最容易被评审凭常识抓到的那类错误。
预期 accuracy 和 doubts 两维净胜，score 过门槛（+0.30）。

## 改动（skill_chars 13564 → 14500，+936 / +6.9%；diff +17/−8 行，其中 5 行是编号顺延）

- `SKILL.md` 观察表：
  - 「与常识或旧版本相反…」一行换成「要进一屏看懂或疑点结论的边界主张还没反证过 → 反证简报，过反证前不写进一屏看懂」。
  - 表下加一段，定义边界主张（否定、排他、强制、全称、时间边界、反常识），给出做法：先拿自己的 grid/笔记找反例，不 spawn；
    找不到就派反证简报（交主张 + 原句 + URL，只许找反例，同一站点的几条打包给一个工人）。有一手反例就改写；
    没有就保留，但写出范围（「截至 <日期>，<查过的页> 未见」）。矩阵里的否定格按影响挑着查。
  - 停止行：「核心格子 ✅/∅ 或网格没变」之外，还要求一屏看懂和疑点结论里的边界主张都已反证（轮数用完除外）。
- `SKILL.md` 终审第 2 步加一句：「没找到来源」不等于「不支持」。没有支撑的正面主张只能删掉或标「未核实」，不许改写成否定句。
- `agents/research-worker.md`、`references/worker.md`（两处同步）：加一条工人规则。
  - 否定/排他/起始版本类主张：WebFetch 摘要里没有 ≠ 页面上没有，要用直接的问题再取一次；版本起点要查 changelog 最早的相关条目。拿不准就写进 gaps。
  - 接到反证简报只找反例：推翻了写成 claim，并在 conflicts 里注明推翻了哪条。
- 没加领域事实：只有语言类别（不支持/唯一/必须/自某版起）和来源类型（changelog、release notes、API reference），这些原 skill 里本来就有。

## 预期变好的维度 / 指标

- `score` ≥ +0.30。主要来自 dims 里的 accuracy、doubts（点名疑点的结论更可信），orientation 次之（一屏看懂里少了错的排他句）。
- 判决 `errors_x` 里边界类错误（未查到/唯一/强制/仍需/不分代际）明显少于 `errors_y`。
- 过程可查：`log.md` 里有反证简报和「推翻 / 维持 + 范围」的记录；R3 更常被用上。spawn 从 10–13 升到约 13–17。
- 花费每次多 $1–2，在 1.5× 在位者（约 $11.5）以内。时长多 4–8 分钟，最慢的 agent-protocols 预计 40 分钟上下。golden 持平或略升（反证常常找回漏掉的正面事实）。

## 风险

- 反证工人（Haiku）可能把社区插件、第三方适配器、fork 当反例，把真的否定翻成假的肯定。规则要求「一手反例」才改写，但 Haiku 未必守得住。
- spawn 花在反证上，可能挤掉补缺口的工人，coverage 下降。主 agent 也可能把矩阵里大量「无/—」都当边界主张去查，浪费预算。
  规则只强制一屏看懂和疑点结论两处，矩阵按影响挑。
- 写法变保守：「截至…未见」多了，doubts 结论读起来不够干脆，评审可能嫌含糊。
- 多一轮会让个别题接近时间上限，主 agent 的重写成本也更高。
- 和 e001（收束与成稿）可能重叠：终审第 2 步那一句属于「终审后怎么改稿」，两边都改的话合并时手工处理。
- 评测噪声大：单题 ±0.5。见下面附注，Grok 的 yx 顺序可能有标签颠倒，会掩盖或放大真实差异。

## 附注（评测观察，不属于本候选）

Grok 的 yx 判决有两份把 A/B 标签整份颠倒了，不是位置偏好（已用 raw 字段核对）。yx 顺序下 A.md = e000a、B.md = e000b：
- `e000b/judge/py-packaging/*grok-yx.json`：`raw.errors.A` 引的是「唯一有官方 GH Action」，只出现在 e000b 的成稿里；
  `raw.errors.B` 引的是「200+ 员工/合同工的组织需付费」，只出现在 e000a 的成稿里。reason 夸的也是带 D1–D11 的那份（e000b）。
  `overall: A` 却被记成 e000b −2。
- `e000b/judge/agent-protocols/*grok-yx.json`：`raw.errors.A` 引的是「未查到官方 MCP 支持声明」（只在 e000b），
  `raw.errors.B` 引的是「MCP强制OAuth2.1」（只在 e000a）。`overall: A` 被记成 e000b −1。
- prompt-caching 的 grok-yx，以及所有 grok-xy 和 claude 判决，标签都和原文对得上。
按原文纠正后，Grok 在三题上两种顺序都选同一个赢家。A/A 变成 agent-protocols 0、prompt-caching +0.5、py-packaging +1.5，
合计约 +0.67，而不是 +0.167。journal 里写的「Grok 位置偏好」可能其实是这个标签问题，它会随机翻转之后候选的 Grok-yx 判决。
建议主 agent 核对后再用门槛。
