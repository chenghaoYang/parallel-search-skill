# e001：终审加一遍成稿自洽检查（方向：收束与成稿）

一句话：终审工人在原子抽查之外，逐条拿「一屏看懂」、家族归属、坑、未决去对照矩阵，重算推导数字、核对 `[n]`；主 agent 按笔记原句把概括句改到和矩阵一致；流程信息不写进成稿。

## 证据

**1. 评审「确信的错误」里，约四成不需要任何外部知识，读成稿本身就能确认：前后说法打架。**
A/A 的 12 份判决（`evolve/runs/e000b/judge/*/*.json`）共列出 54 条 errors；去重后 12 条是成稿内部不一致，出现在 6 份成稿中的 5 份，被点名 23 次：

| 运行 | 段落 | 不一致 | 点名的判决 |
|---|---|---|---|
| e000b/py-packaging | §0「uv…唯一有官方 GH Action 的一体化工具」 | 同文 D10 列写着 PDM 官方 `pdm-project/setup-pdm` | 4/4（claude-xy/yx、grok-xy/yx） |
| e000b/prompt-caching | §0 第 3 条「Kimi…明确收写入费(1.25x起)」「智谱写入不加价」 | 矩阵 Kimi「5m档=标准价」、智谱写入费「∅官方未详述」，§5 也写未详述 | claude-xy、grok-xy、grok-yx |
| e000b/prompt-caching | §0 第 4 条「其余厂商是分钟/小时级精确时长」 | 矩阵里两家的 TTL 是 ∅ / 「系统自动」 | grok-yx |
| e000b/prompt-caching | §4「1小时档写入价接近5分钟档的2倍」 | 同文矩阵 1.25x 对 2x，比值 1.6 | claude-xy、claude-yx |
| e000a/prompt-caching | taxonomy「双轨（自动兜底）」收了 Anthropic，导语「传言已过时」 | 同文 §0 和矩阵：Anthropic 仍要在顶层加 `cache_control` | claude-yx、grok-xy、grok-yx（grok-yx 和 claude-xy 的 reason 都把它当决定因素） |
| e000a/prompt-caching | OpenRouter 行「OpenAI仍需`prompt_cache_breakpoint`」 | 同文 OpenAI 行和 §0 第 1、7 条写的是「可选」 | claude-xy、grok-xy |
| e000a/agent-protocols | §0 第 3 条「…独立生效，没有协商」 | 坑 4「判断兼容性看运行时 `protocolVersion` 协商结果」 | claude-xy、claude-yx（grok 两份放进 unsure） |
| e000b/agent-protocols | §5「仅二手来源（workos.com 博客）[9]」 | [9] 实际是 ibm.com，来源节里没有 workos.com | claude-xy、claude-yx |
| e000b/agent-protocols | 「独立挂牌 LF 近一年后」 | 同文日期 2025-06-23 → 2026-08-27，约 14 个月 | claude-xy |
| e000b/agent-protocols | 「没有厂商发布第五个独立协议」 | 同文矩阵称 A2UI 为「独立声明式 UI 协议」 | claude-yx |
| e000b/py-packaging | §5「抽查 34 条：30 supported、2 weak、1 unsupported、0 contradicted」 | 加起来是 33（成稿里写流程计数引入的错） | claude-yx |

判决的 reason 里也拿它们定胜负。prompt-caching grok-yx 的原话是「『双轨』把 Anthropic 与 OpenAI 并在一起……又容易让人以为可以不再传 cache_control」；
agent-protocols claude-xy 的原话是「B 自己也有…版本协商前后矛盾的错误，所以只算略胜」。评审被要求「只在确信时算错」，而自相矛盾不需要外部知识，是最容易被确信的一类错。

**2. 这些矛盾是重写时漂移出来的，每一轮都活了下来。** 从快照看，e000b/py-packaging 的「唯一有官方 GH Action」在 `report.r1/r2/r3` 里一直没变，
矩阵 D10 从 r1 起就列着 PDM 的 `setup-pdm`。e000b/prompt-caching 的「智谱写入不加价」r1 就有，那时矩阵写的是「❓未查到」。
e000a/agent-protocols 的 §0「没有协商」是 R2 加进来的新发现，r1 就有的坑 4 没有跟着改。「每轮从头重写」管不住一屏看懂：它常被沿用或只改一半，矩阵却被新笔记更新了。

**3. 现在的终审查不到这类错，终审后的改稿几乎什么都没改。** 6 份 `ds/audit.md` 都只做「原子主张对笔记」：
supported 约 93–100%（45/45、19/20、27/29、19/22、34/36、30/34），5 份 contradicted 为 0，没有一份对照过成稿内部。
被评审点名的句子，有的根本没被抽到（「唯一」、Anthropic 的家族归属、OpenRouter 行），有的被判了 supported：
e000b/prompt-caching 的审稿把「接近2倍」判 supported，e000a/agent-protocols 的审稿把「强制 OAuth2.1」判 supported。
结果终审后 e000a 的两题直接写「无需改动」，e000b/py-packaging 反倒往成稿里加了一段抽查计数，而且加错了。

## 假设

一屏看懂、家族归属、坑是主 agent 自己的概括，最容易和带引用的矩阵打架，评审也最容易认定这是错误。
终审加一遍成稿内部的自洽检查（这些概括逐条对照矩阵，重算推导出的数字，核对 `[n]`），再规定改稿以笔记原句为准、改概括去贴合矩阵、流程信息不进成稿，
预期判决里点名候选的错误会变少，accuracy、taxonomy、doubts 的净胜会上升，overall 胜多负少。

和 e002（边界主张先找外部反证）的关系：e002 在扩展阶段为否定、排他、全称这类主张派反证工人，并改了「未查到不许改写成否定句」；
本候选不加 spawn、不查新来源，只在终审里做成稿内部对照。两者只在「唯一 / 都 / 没有」这类句子上有重叠，这里靠矩阵里的反例抓，两边可以叠加。

## 改动（2 个文件，+6/−5 行，skill_chars 13564 → 14025，+3.4%）

- `SKILL.md` 终审第 1 步：审稿简报原样带上 `converge.md` 的「审稿标准」；抽查之外再做一遍自洽检查。第 2 步：自洽检查列出的每一处都改到全文一致。
- `references/converge.md`「审稿标准」：
  - 新增第 3 步自洽检查：导语、一屏看懂、家族归属、坑、未决逐条对照矩阵同一实体同一属性的格子；「唯一 / 都 / 没有」在矩阵里有反例就算不一致；重算倍数、比例、时间跨度、合计；核对 `[n]`。
  - 第 4 步：`audit.md` 里自洽检查单列一节，每处写 `甲处原文 | 乙处原文 | 哪处有笔记支撑`。
  - 改稿规则：以笔记原句为准，改概括贴合矩阵，不改矩阵迁就概括；审稿过程和抽查计数只写 `log.md`。
- `references/converge.md` 骨架「0. 一屏看懂」加一句：每条都要和后文矩阵、坑一致（终审会逐条对照）。

不加 spawn，不动工人规则、扩展流程、字数预算。

## 预期变好的维度 / 指标

- 主指标：`score > 0`，目标过门槛 +0.30。
- errors_x 里「矛盾 / 前后 / 同文 / 对不上 / 自己的矩阵」这类条目：基线 12 份判决共 23 次（约 1 次 / 判决），目标减半以上。
- `dims_net`：accuracy ↑；taxonomy ↑（家族归属和矩阵一致）；doubts ↑（疑点结论不再被自家矩阵反驳）；concision 略 ↑（成稿里不再有流程计数）。
- 过程上可以直接看：`ds/audit.md` 有非空的自洽检查一节；终审后 `report.md` 有对应修改；成稿里没有「终审 / 抽查 N 条」这类字样。
- 成本和时间基本不变：同一个审稿工人多读一遍成稿、多写一张表，预计 +0–3 分钟、+$0–0.5。golden、`len_ok` 不受影响（改的是措辞，删掉流程计数还能省字）。

## 风险

- Haiku 审稿工人可能漏检，也可能误报。误报时主 agent 可能把本来对的概括改弱，一屏看懂变得含糊，orientation 或 doubts 反而下降。
  缓解：要求审稿写出双方原文和「哪处有笔记支撑」，最后由主 agent 裁决。
- 矩阵本身错、概括反而对的时候，「以笔记原句为准」救不回来。笔记本身有错（如 Poetry BYOP、uv pylock 版本）属于证据方向的问题，本候选不处理。
- 有些决定胜负的错不在这一类。比如 e000b/agent-protocols 输掉，靠的是终审后把 Google×MCP 降成 ❓ 的否定句（那是 e002 管的）。
  所以单题收益可能被别的硬错盖住，要看三题合并的结果。
- 贴着 9000 字的稿子，改稿时要守住 budget。多数修正是换措辞，不增字。
