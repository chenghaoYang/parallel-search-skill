# log

turn 计数：一次 Agent 调用或一次 SendMessage = 1 turn。

## R0（不 spawn）
- 写 brief.md、grid.md（taxonomy v0：3 条分类轴、10 个维度、9 行实体）。
- R1 计划：按来源边界拆 10 个工人 —— 4 个参照协议各 1（整行 D1–D10）；DeepSeek、智谱、Kimi、Qwen/百炼各 1（相对参照协议的偏差）；
  1 个「参照厂商自家兼容层」（Anthropic OpenAI SDK 兼容 + Gemini OpenAI 兼容）；1 个 scout（网格外实体/标准/网关 + 用户会踩的坑，只进 leads）。
- MiniMax、火山方舟、xAI、OpenRouter、vLLM/Ollama、Bedrock、Open Responses、Gemini Interactions 等留给 R2，视 scout 结果决定。
- budget 20000；策略：R1 成稿接近上限（≈19k），之后每轮只替换不增长。

## R1 扩展
- spawn 10（turn 1–10）：r1-openai-chat、r1-openai-responses、r1-anthropic-messages、r1-gemini-generatecontent、r1-deepseek、r1-zhipu、r1-kimi、r1-qwen、r1-firstparty-compat、r1-scout。
- 10/10 返回，无失败。

## R1 收束
- notes_lint：10 份，316 条主张（official 314 / secondary 2），16 conflicts，36 gaps，27 leads。
  格式修正（机械、未改内容）：anthropic 笔记的相对路径、gemini 笔记的短码 [GC] 等、zhipu/scout 缺 https:// 的 src 展开成完整 URL；scout 的 [P1]–[P9] 改编号为 [C18]–[C26]。
- taxonomy v0→v1：新增 D11「厂商暴露哪些协议入口」、D12「不支持字段是忽略还是报错」（R1 笔记里大量「Ignored / 400 / 截断 / 重映射」主张装不进 D1–D10）；
  A2 细化为「兼容 Responses ≠ 托管状态」（OpenRouter/Ollama 仅无状态、智谱默认 store=false）；A3 加「开放规范」；
  新增行：GGL-Interactions（Google 2026-06 GA、官方推荐新项目）、DeepSeek Responses（Q1 核心：DeepSeek 2026-08-13 起原生支持 Responses）、
  智谱 ANT 兼容（Q2）、MiniMax、火山方舟、Open Responses、网关/自托管/云（只填 D3、D11）。
- 成稿 r1：19,813 字符（初稿 20,082 超 82 → 删去重复的流式行、缩短来源标题、坑节改为引用 §2）。
  改错 3 处：拒答误引 Gemini 来源；FIM 误引 KV cache 页；「智谱服务端重映射模型名」无依据 → 改为客户端 ANTHROPIC_DEFAULT_*_MODEL。
- roundstat：r1 19813；grid ✅104 ⚔6 ❓57，resolved 62%。

R1 观察：Q1 的关键事实变了——DeepSeek 已有 Responses API，但字段级只知 3 条（❓×7）；Q2 智谱官方无字段表（❓×8，需定向再查一次才能判 ∅）；
⚔ 关键格：OAI-Resp D8（Responses 流是否发 [DONE]，与智谱的「差异」说法相关）、OAI-Resp D6（encrypted_content 默认 vs include）；
Anthropic D1「Bearer 为主、x-api-key 为旧回退」与 D9「Opus 4.6 后弃用 temperature/top_p/top_k」是与常识相反的高影响主张，需一手复核；
scout leads：Gemini Interactions API 是 Google 当前推荐入口（全 ❓）、Open Responses 规范、MiniMax/方舟两家国内厂商只有 base URL。
→ 动作：R2 定向 7 个新工人 + 1 次 SendMessage（Kimi Responses 状态，D3 ❓）；Bedrock/Azure/vLLM 等只保留一行，不再派人。→ 预计 spawn：8

## R2 扩展
- spawn 7（turn 11–17）：r2-deepseek-responses（DeepSeek Responses D3/D4/D6/D7/D9/D10/D12）、r2-zhipu-anthropic（智谱 ANT 兼容 D2/D4/D5/D7–D10/D12 + Responses D12）、
  r2-gemini-interactions（GGL-Interactions D2–D10 + GGL-Gen D9 + D2⚔）、r2-open-responses（规范 D2–D8/D11/D12）、r2-minimax（D2–D12）、r2-ark（D1⚔ + D2–D12）、
  r2-verify-ref（OAI-Resp D6⚔/D8⚔、ANT D1、ANT D9）。
- SendMessage 1（turn 18）：r1-kimi → r2-kimi-responses（Kimi D3）。
- 8/8 返回，无失败。

## R2 收束
- notes_lint（r2）：8 份，188 条主张（official 187 / secondary 1），0 缺来源/原句，9 conflicts，31 gaps，23 leads。
- 裁决：OAI-Resp D8（Responses 流无 [DONE]，ResponseStreamEvent 不含 DoneEvent）；OAI-Resp D6（无状态模式默认返回 encrypted_content，include 写法 legacy）；
  ANT D1（Bearer 为主、x-api-key legacy fallback，属实）；ANT D9 修正（Opus 4.6 之后的模型：temperature 仅 1.0、top_p 仅 ≥0.99，top_k 任何值 400——不是「忽略」）；
  Ark D1（/api/coding* 是 Coding Plan 独立网关，误用 /api/v3 另计费）。GGL-Gen D2 在 proto 源码里同样矛盾 → 保持 ⚔，写进 §5。
- Q1 结论升级：DeepSeek Responses 是「形状兼容、语义无状态」的 Codex 适配层（store 恒 false、无 previous_response_id、明文 reasoning、托管工具忽略、静默忽略未知参数）。
- Q2 结论定稿：智谱 Anthropic 端 7 个字段定向全文检索无果 → ∅；能证实的只有内置 MCP/image_analysis 替代、effort 折叠、客户端模型映射。
- taxonomy v1→v2：A1 加 Steps 家族（Gemini Interactions）；A3 加「按 Codex/Claude Code 裁剪」解释；§3 改为 Items/Blocks/Chat 三张家族表（原 Q1 表、Kimi/Qwen 表并入）。
- 成稿 r2 从头重写：初稿 20,025 → 压到 19,723（R1 19,813，-90）。
  新增：Responses 兼容表、Anthropic 兼容表、Gemini 两入口对照、Open Responses 规则、MiniMax/方舟两行、Anthropic 采样参数 400 规则。
  为此删/压：来源节改为「域名前缀 + 路径」（4.4k→3.0k）；§2 格内引用改为表头列级引用；§3 原 Q1 表、Kimi/Qwen 表、其他实现段并入家族表；
  删 SGLang 细节、Azure api-version（P2）；§4 与 §2/§3 重复的数值改为引用。
- roundstat：r1 19813 → r2 19723；grid ✅145 ⚔3 ❓12 ∅7，resolved 91%（R1 62%）。

R2 观察：P0 格子（4 参照 + DeepSeek + 智谱）全部 ✅/∅，只剩 GGL-Gen D2 规范级矛盾（文档无法裁决）。剩余 ❓ 集中在 §3.2「Responses 兼容」表：
方舟、Qwen 的推理表示/不支持字段（6 格 ❓）、MiniMax Responses 状态未知；§3.3 Qwen/MiniMax 的 Anthropic 端鉴权 ❓。Responses 是种子词，该表是核心对照之一。
→ 动作：R3 只做 3 次 SendMessage 追问（复用 r2-ark、r1-qwen、r2-minimax 已读过的文档上下文，比新 spawn 便宜），每条点名 §3.2/§3.3 的 ❓ 格；
  R3 后直接终审，不再扩展。→ 预计 spawn：3（turn 19–21）

## R3 扩展
- SendMessage 3（turn 19–21）：r2-ark → r3-ark-responses（§3.2 方舟行 3 格 + §3.3 方舟 header）；r1-qwen → r3-qwen-responses（§3.2 Qwen 行 + §3.3 鉴权 + Qwen D10⚔）；
  r2-minimax → r3-minimax-responses（§3.2 MiniMax 行 + §3.3 鉴权/模型名）。
- 3/3 返回，无失败。

## R3 收束
- notes_lint（r3）：3 份，43 条主张（official 42 / secondary 1），0 缺来源/原句。
- 填格：§3.2 方舟行（reasoning item＝summary＋encrypted_content、previous_response_id 默认存 3 天/最长 7 天、工具含 Remote MCP）、Qwen 行（store 默认 true、7 天、reasoning item＋summary、不支持 background）、
  新增 MiniMax 行（无 previous_response_id、明文 reasoning_text、仅 function、temperature (0,1]）；§3.3 Qwen/MiniMax 鉴权（两者都收 x-api-key 与 Bearer）、MiniMax model 只收 MiniMax-*、cache_control 有定义。
- 更正 R2：MiniMax signature / cache_control 在 OpenAPI 参考页有正式定义（R2 据 guide 页判「未文档化」是文档分层造成的）。
- 成稿 r3：加 MiniMax 行、扩方舟/Qwen 行、5 个新来源（初稿 20,483）→ 为此删 §2「多模态」行、合并 §4 两条（模型代际并入参数条、删流式分片条）、
  Interactions 表压缩、§0-1 的 Interactions 句并入 §0-2、§0-6 细节改指向 §3.3、DashScope 原生端点路径改一句话 → 19,704（R2 19,723，-19）。
- roundstat：r1 19813 → r2 19723 → r3 19704；grid ✅151 ⚔3 ❓5 ∅8，resolved 95%。

R3 观察：核心格子全部 ✅/∅；剩余 ❓（MiniMax D7/D8、方舟 D2、Open Responses D7/D8）为 P2，⚔ 3 个均为官方文档自相矛盾（已写进 §5），再派工人也只能记录矛盾。
→ 动作：停止扩展，进入终审。报告覆盖 §0–§5 共约 200 条具体主张，范围大 → 派 2 个审稿工人（A：§0–§2 参照协议；B：§3–§5 厂商），各抽查 ≥ 20 条。→ 预计 spawn：2（turn 22–23）

## 终审
- spawn 2（turn 22–23）：audit-a（§0–§2，≥22 条）、audit-b（§3–§5 + §0 第 3/5/6 条，≥24 条）。
- 2/2 返回。audit-a（§0–§2）：37 条，supported 31 / weak 4 / unsupported 1 / contradicted 1；audit-b（§3–§5）：50 条，supported 41 / weak 8 / unsupported 0 / contradicted 1。合计 87 条，supported 72（83%）。

## 按审稿改稿（不做新调研）
- contradicted → 改正：Gemini `finishReason`「19 项」→「20 项」（审稿直接核对原页枚举）；智谱 token 偏差「43–249%」→「JSON 多 43–49%，特殊字符多 143–149%」（笔记原句本就是两档，成稿合并时写错）。
- unsupported → 补依据：Responses 鉴权「同左」补 [7]（OpenAI 鉴权页适用于整个 API）。
- weak → 处理：Messages 的 `anthropic-version` 补 [12]；§1 Chat/Parts 的「无状态」标「（推断）」；§0-3 MiniMax 等改成「不支持 previous_response_id，历史要自己回传」（不再笼统写「无状态」）；
  §3.1 DeepSeek/智谱行补 [31]/[37]；Qwen 原生协议补来源页 qwen-api-via-dashscope；MiniMax「须回传完整 message」改为 [57] 原句支持的「都须完整保留回传」；
  llama.cpp 加「README 称支持」限定；§4 补 [27]、[59]。
  「generateContent 为 legacy」一条保留：原句 "While it is now considered legacy, the original generateContent API remains fully supported." 中 it 为后指，指的就是 generateContent。
- 为抵消新增字数：删 §3.3 Kimi 行与 §4 重复的 input_tokens 口径、§3.2 Kimi「图片只收 data URL」、§4-2/§4-5 的重复说明。
- 终稿 19,703 字符（r1 19,813 → r2 19,723 → r3 19,704 → final 19,703，逐轮不增，均 ≤ 20,000）；grid resolved 95%（✅151 ∅8 ⚔3 ❓5）。
- turn 合计 23：R1 10 spawn，R2 7 spawn + 1 SendMessage，R3 3 SendMessage，终审 2 spawn。
- 终稿复制到 ./report.md。
