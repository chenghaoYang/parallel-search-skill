# log

## R0

观察：用户要的是协议谱系对照，不是厂商清单。点名疑点是 DeepSeek 响应 vs OpenAI 官方文档，以及智谱 message vs Anthropic 官方。种子四个对象正好是四个请求谱系。

决策：分类轴 v0 = 下一轮上下文靠什么接上 + 内容是字符串还是块。网格 8 行 × D1–D10。R1 按来源边界派 8 个实体工人 + 2 个 scout（新实体/新维度；用户会踩的坑）。scout 只进 leads。

预计 spawn：10。

## R1

观察：10/10 笔记可解析，258 条 official，0 条缺 src/quote。DeepSeek 点名疑点已能结论：同时有 `/chat/completions` 与 `/responses`，后者写明不存会话并静默忽略 `previous_response_id`；Chat 与 Responses 的 JSON、思维字段、`finish_reason` 都不等于 OpenAI 文档的同名对象。智谱 Messages 只有路径和「有差异但未列清单」，D2–D9 为 ❓（已查介绍页、llms.txt、OpenAPI，OpenAPI 无 `/anthropic`）。分类轴仍解释四个谱系；v0→v1 把实体改成「端点」而不是「公司」，否则 DeepSeek/智谱的两套协议挤在一行。字数贴近预算，R2 必须替换而不是追加。Scout 不进成稿；范围内值得加行的是 MiniMax Messages（有公开有损字段）和 Gemini Interactions（可能把 Google 从「客户端重放 contents」拆出服务端 id）。

动作：不重查已 ✅ 的四套官方谱系。R2 只打 (1) 智谱 Messages 字段表或坐实官方未写 (2) DeepSeek 三处 ⚔ 的原句归属 (3) MiniMax 新行 (4) Interactions 是否另一协议，并顺手摘结构化输出当前字段名。xAI、百炼 Anthropic/Responses 页留给下一轮，避免这轮再铺开。

spawn：10。结果：258 claims。成稿 18720 字符（预算 20000）。预计 R2 spawn：4。

## R2

观察：4/4 笔记可解析，92 条 official。用户点名的两处可以收束：DeepSeek 的 `/responses` 不存会话，`tool_choice` 400 只属于 Chat 思考模式，Responses 写 Supported；智谱 Messages 在 sitemap 236 条和多份 404 之后记 ∅，不是「还没查」。MiniMax 补上了「Messages 适配有哪些写明的差异」。Interactions 让分类轴多一个家族，但 GA/Beta/legacy 三页冲突，不能写成已取代 generateContent。taxonomy v1→v2 只加这一家族。

新增：MiniMax 行、Interactions 行、智谱 ∅、DeepSeek 冲突按端点拆开。为了不增长，删掉百炼/Moonshot/智谱 Chat 里和第 4 节重复的枚举，以及第 5 节里已经按端点拆开的 tool_choice 长句。

动作：不再加实体。再加一行就要删掉已有下游，而点名疑点已经有结论；剩下的 ⚔ 是同一官方站点两页并存，再派核验也不会出现第三份裁决。下一步终审。

spawn：4。成稿 18696（R1 为 18720）。预计终审 spawn：1。

## 终审

观察：审稿 30 条，supported 20，weak 6，unsupported 0，contradicted 4。错句是：智谱 `tool_choice` 写成了「默认且仅 auto」；百炼 `preserve_thinking` 写成一律默认 false；DeepSeek `prefix=true` 被写成工具回放的通用条件；penalty 被写成「全局」。weak 已改成与原句一致：静默忽略列表去掉 `truncation`（超窗是 400）；模型名分开写公告路由 `deepseek-v4-flash` 和定价表 `deepseek-flash`；Moonshot 温度按模型写；MiniMax 的 JSON 字段改成「已开页没有原句」；`role=tool` 的引用去掉 DeepSeek；`interactions.md.txt` 写成三句并存。

动作：只改稿，不再调研。删/改上述句子，压缩第 4 节长度字段段以保持不增长。

spawn：1。成稿 18659。停止。网格仍有 Interactions 的 D3/D4/D6 为 ❓，以及文档内部 ⚔，都写在第 5 节。
