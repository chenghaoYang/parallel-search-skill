# log

## R0（不 spawn）
- 写 brief.md、grid.md（taxonomy v0：4 分类轴、12 维度、16 行实体，其中 GG-OAI/AN-OAI/ORS/GW/SH/CL 为预期实体，留给 R2 按 scout 线索决定）。
- R1 规划（按来源边界拆，10 个工人）：openai-chat、openai-responses、anthropic-messages、gemini、deepseek（Q1）、zhipu（Q2）、moonshot-minimax、qwen、ark、scout（坑 + 未列实体/维度，只进 leads）。
- spawn 计数：0

## R1 扩展
- spawn 10（turn 1–10）：r1-openai-chat、r1-openai-responses、r1-anthropic-messages、r1-gemini、r1-deepseek、r1-zhipu、r1-moonshot-minimax、r1-qwen、r1-ark、r1-scout。累计 spawn：10
- R1 全部返回（10/10，无失败重派）。事故：r1-anthropic-messages 工人误删 /tmp/anth（另一进程 20:05–20:16 的下载文件），已重下 24 个 .md；sdk_mcp.py 以推断文件替代未核对，verify.py 无法恢复。需在终稿回复中告知用户。

## R1 收束
- notes_lint：10 份笔记，295 条主张（official 294 / secondary 1），0 缺 src/quote，32 冲突，28 缺口，38 线索。
- taxonomy v0→v1：
  - 新增行 GG-IA（Gemini Interactions API）：Google 把 generateContent 标为 Legacy、推荐 Interactions [r1-gemini C4, r1-scout C1]，G 家族拆成 Legacy/新协议两行。
  - 新增行 ZP-M（智谱 Anthropic 端点）：Q2 需单独成行；官方无字段表 → 多格 ∅。
  - 分类轴新增 A3「协议面」（下游厂商同时暴露 CC/M/R，按端点而非厂商判断兼容性）。
  - D7 改名「输出控制与采样」，吸收 scout 建议的「采样参数被拒/弃用」（不另设维度）；D5 吸收「托管状态留存期」；D11 明确含「静默忽略 vs 报错」。
- 成稿：从头写 R1 版。来源节改为按站点分组（前缀一次 + 路径），来源字数 6786 → 约 3900。report.r1.md = 17919 字符（预算 20000），85 条来源。
- roundstat：r1=17919；grid ✅101 ⚠0 ⚔4 ❓30 ∅9，resolved 110/144（76%）。

## R1 观察 → R2 动作
- R1 观察：核心 4 行几乎全 ✅；新核心实体 GG-IA 全 ❓（且 D1 端点 v1/v1beta 线索冲突）→ 动作：定向简报 r2-gemini-interactions → 预计 spawn：1
- R1 观察：ZP/MS/MM 的 Responses 兼容只在 leads（R 家族兼容实现不全）；MM D4 tool_choice ⚔ → 动作：定向简报 r2-cn-responses（附带核验 MM tool_choice）→ 1
- R1 观察：GG-OAI 全 ❓、AN-OAI D1/D6 ❓（scout 只给线索）→ 动作：r2-origin-compat → 1
- R1 观察：GW/SH/CL 只有 scout leads（范围内，用户需知）→ 动作：探索简报 r2-hosting（每实体 1–3 条）→ 1
- R1 观察：Q2 用户点名，ZP-M 多格 ∅；ZP D6 ⚔ → 动作：r2-zhipu-anthropic（官方页面补漏 + 二手证据标 secondary + 核验 D6 冲突）→ 1
- R1 观察：OA-R D7 ❓，但工人称已查到原句只是超篇幅 → 动作：SendMessage 追问 r1-openai-responses 写补充笔记 → 1 turn
- 不派：QW D6 流式冲突、Gemini role 冲突等次要冲突，直接进 §5。
- R2 字数约束：≤ 17919（不许变长），新增内容靠替换 ❓、删 P2 腾位。

## R2 扩展
- spawn 5（turn 11–15）：r2-gemini-interactions、r2-cn-responses、r2-origin-compat、r2-hosting、r2-zhipu-anthropic；SendMessage 追问 1（turn 16）：r1-openai-responses → r2-oa-responses-add。累计 turn：16
- 每份简报都点名格子与 R1 线索/冲突原句，并加成本上限（WebFetch ≤ 8–14、主张 ≤ 25–30）。
- R2 全部返回（5 spawn + 1 追问，无失败）。r2-oa-responses-add 为追问产物（12 条，均 official）。

## R2 收束
- notes_lint（r2）：6 份笔记，116 条主张（official 104 / secondary 12，secondary 全在 r2-zhipu-anthropic），0 缺 src/quote，12 冲突。
- taxonomy v1→v2：主轴由「谱系」换成「代际」。理由：Gemini Interactions 与 OpenAI Responses 共享形状（扁平函数工具、call_id 关联的调用/结果条目、store 默认 true、previous_*_id 续接、background、queued/incomplete 状态、语义流事件）[r2-gemini-interactions C8 C9 C11 C13 C19 C22；r1-openai-responses C6 C8 C10]，按谱系分会把它归入 G 家族、解释不了它与 generateContent 的差异。一代内部的差别降为次轴「切分粒度」。A3 协议面新增 Responses 兼容的「有状态/忽略/拒绝」三分。
- 成稿变化：新增 Interactions 列（§2 三张表改 5 列）、Responses 兼容状态对比（§0.4、§3.1）、Zhipu Anthropic 端点官方 + 二手证据（§3.3）、源头厂兼容层 + 网关 + 云托管表（§3.4）。为此：§2 改用表头默认来源（删同列重复引用）；来源节换成更细的站点前缀；删 P2：DeepSeek 模型版本、Qwen 原生协议、方舟 Model ID、Vertex/Gemini 以外的 LiteLLM/SGLang/Azure 行、OpenRouter reasoning 参数、MiniMax 被动缓存、DeepSeek 限流坑、智谱套餐额度坑、两条次要冲突；§0.5/§0.8 改为指向 §2/§3。
- 字数：r1 17919 → r2 17905（−14）。来源 85 → 112。
- roundstat：见下行。
grid: ✅ 129, ⚠ 6, ⚔ 4, ❓ 4, ∅ 1 | resolved 130/144 (90%)
notes per round: r1=10, r2=6

## R2 观察 → R3 动作
- R2 观察：核心 5 协议 × D2/D4/D5/D6/D8/D9 全 ✅；Q1/Q2 有一手结论；剩余 ❓ 集中在核心矩阵里的 OA-CC 内置工具与采样、GG-OAI 结构化输出（成稿里是可见的 ❓ 格）→ 动作：定向简报 r3-openai-gaps → 预计 spawn：1
- R2 观察：下游差异表剩 Qwen 推理回传 ❓、MiniMax OpenAI 层工具 ❓、DS 图片输入 ❓、QW D6 ⚔ → 动作：定向简报 r3-cn-gaps → 1
- 不派：GG-IA D1/D7、MM D4 是官方文档自相矛盾（R2 已复核），再查无增量，直接进 §5；ZP-M ⚠ 官方两轮定向查无文档，不再派。
- R3 后直接终审（grid 已 90%，R3 只补残余格）。R3 字数约束：≤ 17905。

## R3 扩展
- spawn 2（turn 17–18）：r3-openai-gaps、r3-cn-gaps。累计 turn：18
- R3 全部返回（2/2，无失败）。

## R3 收束
- notes_lint（r3）：2 份笔记，21 条主张（全 official），0 缺 src/quote，2 冲突。
- taxonomy：v2 不变（R3 只补格子，未出现装不进维度的主张）。
- 成稿变化：替换 3 个 ❓（CC 内置工具 `web_search_options`；CC/Responses 采样：temperature 0–2、stop ≤ 4、GPT-6 effort≠none 去掉 temperature/top_p；Qwen `preserve_thinking` 回传规则）；DeepSeek Anthropic 层补「image 支持」；§0.6 加 OpenAI 一条。为此：合并「系统指令」行入「容器/角色」行；压缩 §4.1、§1 维度行、§5 时效/∅ 行；删 OpenRouter comment 在 §3.4 的重复（保留在 §4.7）、Anthropic 兼容层 n=1、Kimi 在 §0.6 的重复指针。
- 字数：r2 17905 → r3 17898（−7）。来源 112 → 114。
- roundstat：grid ✅133 ⚠6 ⚔4 ❓0 ∅1，resolved 134/144（93%）。

## R3 观察 → 下一步
- R3 观察：核心格全 ✅/∅；剩余 ⚔ 均为官方文档自相矛盾（已两轮复核）；剩余 ❓ 为 P2 → 动作：终审（2 个审稿工人，按章节拆：§0–§2 / §3–§5，各抽 ≥ 15 条，共 ≥ 30 条），然后按审稿改稿并收束。不再扩展。

## 终审
- spawn 2（turn 19–20）：audit-a（§0–§2）、audit-b（§3–§5）。累计 turn：20
- 终审返回（2/2）。audit-a（§0–§2）61 条：supported 45 / weak 14 / unsupported 2 / contradicted 0；audit-b（§3–§5）96 条：supported 77 / weak 17 / unsupported 1 / contradicted 1。合计 157 条。

## 终审后收束（r4 快照 = 按审稿改稿，无新扩展）
- contradicted 1：§3.3 DeepSeek Anthropic 层 tool_choice 漏了 none → 改为 auto/any/tool/none（审稿回原页核对，转录进 notes/audit-addendum.md C1）。
- unsupported 3：Interactions `last_event_id` 续流（实为 r2-gemini-interactions C21，src 为 interactions-api；补显式引用）；「免费 1 天」（C11 原句已含，审稿误判，未改）；智谱 server_tool_use「回灌会 400」（审稿回原页取得原句，转录进 audit-addendum C3）。
- weak 31：按审稿逐条收窄措辞或补引用。例：DeepSeek 停用改「按公告」；Q2 三项服务端改写统一限定 Coding Plan 场景，并补标准 API 下 GLM-5.3 disabled 报错；Gemini 3 签名限定「函数调用时」；§0.7 两极改按场景分；「仅 Google」改「未见第三方」；Responses「角色同左」改「无 tool 角色」；缓存 40–80% 注明内测；方舟删「≤ 7 天」与「互斥」（原句不支持）；智谱 effort 限 GLM-5.3、clear_thinking 分端点；Kimi 分 K3/k2.x；Qwen preserve_thinking 默认值写全；智谱列表头注明「官方行为条目限 Coding Plan」；Opus 槽映射；二手条目补站点/型号；Bedrock anthropic_version 限 InvokeModel；§4.1 限 CC；§5 ❓ 收窄、⚔ 补 4 条（Anthropic 中途 system、Interactions response_mime_type、Vertex 忽略采样、并入 Interactions 一行）。Interactions tool_choice 降为 ❓。
- 为守字数：删 §3.4 Vertex 行、§4.6、方舟 logprobs、CC 内置工具子字段、§5 中已在 §0.3 写明的 GLM-5.3 冲突，压缩 §5 冲突表述。
- 字数：r3 17898 → r4 17898（±0）。来源 113 条。notes 总计 19 份、433 条主张（official 420 / secondary 13），0 缺 src/quote。
- 最终：turn 共 20（spawn 19 + SendMessage 1）；R1 10、R2 6、R3 2、终审 2。成稿已复制到 ./report.md。
- 事故（需告知用户）：R1 r1-anthropic-messages 工人误删 /tmp/anth（另一进程 20:05–20:16 的下载内容）；24 个 .md 已按原字节数重下，sdk_mcp.py 用推断文件替代未核对，verify.py 丢失。
