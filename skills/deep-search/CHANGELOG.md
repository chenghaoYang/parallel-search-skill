# deep-search changelog

## v2.1（2026-09-30，按问题调研，自然表达）

- 保留来源追溯、回原始材料核验重要结论、否定与排他主张找反例，以及明确区分事实、推断和不确定性。
- 去掉至少两轮、固定词表数量、主 agent 禁止查原页、整批等待、每轮全文重写和固定报告章节。根据独立问题和剩余缺口选择并行、补查及停止时机。
- 词表、网格、C# 笔记、快照、atlas/details 改为按需使用。旧参数继续接受，轮数/人数是上限；保留显式路径与格式要求。保留入口 YAML 的 argument-hint，参数提示改为通用占位值，不暗示默认数量。
- 同步 worker 定义与所有 references，避免入口放松后被旧参考文件重新锁死。环境说明不再把单次模型/机器故障推广成通用规则；Perplexity 包装器仍为可选工具。
- 机械检查只作诊断：自由格式笔记明确标为未评估；篇幅限制需显式传入，旧版布局通过 `--legacy-layout` 选择。增加离线兼容回归测试。
- 本版未运行付费模型或联网 A/B bench。历史 bench/evolve 记录与 incumbent 保持不变；其固定章节/C# 指标不等价于新版研究质量。来源正确性与表达质量仍需实际任务评估。

## v2.0（2026-09-28，vocabulary-first 集成 + 分层成稿 + GLM-5.3 默认栈）

目标：调研任何领域直接 `/deep-search`，成稿对标并超越 [justinatusa/llm-api-protocols](https://github.com/justinatusa/llm-api-protocols)
（bench 里它三层全量 8.0/9.0、Layer 0 单独看 orientation 全场最高，但 135k 字、跨页重复）。三个来源定了这版：

- **词表先行（vocabulary-first，方法来自 [justinatusa/vocabulary-first](https://github.com/justinatusa/vocabulary-first)，MIT）**：
  R0 主 agent 凭知识反向生成 `vocab.md`（入口词/骨架词/圈内暗号/门槛概念/外行→标准名/概念边，全标 ⚠ 不编出处）；
  taxonomy 从词表长出来（对象词→行、问题词→列、对立轴→分类轴）；工人简报带词表切片、搜索用标准词；
  R1 派词表核验工人对官方 glossary 核验（错词换官方叫法、漏词补、⚠→✅）；缺词急救——某格反复 ❓ 先怀疑词没对上，
  先补词再派调研简报；成稿固定 §1「先认识这些词」（压缩自 vocab.md，暗号带易混邻域，外行→标准名小表），
  超越手册的扁平术语表。新增 `references/vocab.md`、worker.md 词表核验简报模板。
- **分层成稿（对 bench 结论「单文档 20k 做不到快速认知 + 字段细节兼得」的回应）**：
  `report.md` 导读（≤ budget，必须单独成立）+ 可选 `atlas.md` 字段对照册（≤ 2×budget，全维度字段级、不复述结论）
  + 可选 `details/<slug>.md` 细节页（每页 ≤ 4000、≤ 8 页）。去重规则：字段级事实只在 atlas、叙事只在 details、
  report 只放概括 + 指针，内容不抄两遍；引用各自页尾解析。观察表加「字段级细节被压掉 → 开 atlas/details」一行；
  roundstat.py 加 atlas/details 预算与 vocab.md 存在性检查。骨架重排：0 一屏看懂 → 1 先认识这些词 → 2 Taxonomy
  → 3 对照矩阵 → 4 变体与适配层 → 5 坑（选型/接入类收「上手检查清单」）→ 6 未决与置信度。
- **默认栈 ZCode + GLM-5.3**：`worker-model` 默认 `inherit`（主/工人同模）；harness.md 加 ZCode 节
  （Agent 工具派 general-purpose、继承会话模型、整批同消息 + 结束回合等通知、SendMessage 追问），
  SKILL.md 描述放宽到任何领域的调研/入门。仓库带 `.agents/skills/deep-search` 符号链接，本仓内直接 `/deep-search`。

未跑盲评（bench 待恢复）；分层与词表的增益先按手册评审证据定向设计，恢复评测后 v2.0 作为整体对打 v1.3-dev 参照。

## v1.3-dev（2026-09-24，evolve 候选 e003/e004/e005 人工合并；未过盲评，待强臂复验）

因 Grok 余额耗尽、cc-swe2 并发限流，三个已产出候选没走完盲评流程，按证据人工合并：

- **终审核验群（e005）**：审稿工人「对笔记抽查」换成「回原页逐条核验」——主 agent 先列核验清单
  （一屏/疑点结论全条 + 坑节事实 + 被引用/⚔裁决/单源高影响矩阵格，一 URL 一判定项，按域名聚簇
  ≤ workers 个核验工人），工人回原页判 confirmed / wrong 附原句 / not-on-page / 走样，主 agent 按判定改稿。
  起因：e002 审稿 44 条全 supported，盲评仍点名 ≥4 条硬错——笔记本身可能就是错的源头。
- **引文保全（e003，折进核验的改稿步）**：改句必须留该格 `[n]`、`[§k]` 不算来源、来源节 URL 照抄笔记
  `src` 完整 `https://`；roundstat.py 新增 `cite:` 检查（无来源节/来源节无 URL/一屏无 [n] 会打出警告）。
- **等待窗口纪律（e004）**：派出整批→返回之间只许写 `待查：` 并等整批或结束回合，不开页面不取 URL
  不再 spawn；想开的页面写成下一轮简报。终审回原页只由核验工人做。硬规则改工具级禁令，不约束工人。
  起因：Grok 主 agent 实测等待窗口自抓 80–170 次页面（transcript `model` 字段实锤），约 2MB 原始页面
  进主上下文，是 Grok 臂超时主因。
- **harness.md**：删掉「grok 自己抓更全」的错误记述；Claude Code 段补 `claude -p` 后台等待上限 600s
  （`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`）和 devin2api/swe-2-max 入口；Grok 段补 SSRF fake-ip 拦域名。
- **converge.md**：审稿节换核验改稿规则；「同一事实一处写全」补 `[§k]` 不是来源；来源节 URL 照抄规则。

## v1.2-dev（2026-09-24 起，evolve/ 自进化循环收下的改动）

- **e002 边界主张先反证**（Claude Code dev 臂 +0.50，2/3 题胜；doubts +15、accuracy +9；单次花费反而低 11%）：
  否定、排他、强制、全称、时间边界类主张进「一屏看懂」或疑点结论前，先用自己的笔记找反例，找不到再派反证简报；
  工人写这类主张前重取页面、版本起点查 changelog 最早条目；终审不许把「没找到来源」改写成否定句。
  起因：A/A 判决里约六成硬错是这类主张，grid 里标 ✅ 却从没被核验过。

## v1.1（2026-09-23，bench 第一轮之后）

按 bench 里看到的现象改，不改流程：

- harness.md：加 Kimi Code、Grok Build 两节；写明各外层「等一批」的正确方式；Claude Code headless 下不许用 ScheduleWakeup /
  CronCreate 等待（cc-opus-opus 第 1 次因此丢了 10 个工人）；Perplexity 的配额回退、研究模式不可用、「产出文档」变成生成文件。
- worker.md / research-worker.md：`src` 必须是完整 URL（Sonnet 工人常写相对路径）；每个工人约 20–25 次工具调用，
  大文件只 grep 需要的段落（Opus 工人整份下载规范逐段核对，R1 用了 40 分钟以上、笔记超长）。
- SKILL.md：观察表加一行「与常识或旧版本相反、影响大的主张 → 先复核」。
- notes_lint.py：标出超过 8000 字符的笔记。
- harness.md（Grok）：记下 grok-4.7 主 agent 在等工人时自己抓网页（R1 88 次）。

## v1.0（2026-09-23）

bench 第一轮（cc-opus-sonnet、cc-opus-opus 重跑、grok-47-47、kimi-glm53-glm53flash）用的版本。
