# Log

参数：rounds=3 workers=6 budget=9000 worker-model=swe-2-shim dir=./ds。无 pplx-safe。工人用 web_search 找页、web_fetch 取原句。

## R0

观察：用户疑点集中在「自动 vs 必须 cache_control」「命中计费」「TTL」，并要求命中信号、失效条件，以及 Kimi / 智谱 / 通义 / OpenRouter。这些都是边界主张高发区（必须、自动、仍是）。

决策：分类轴 v0 = 客户端如何声明缓存边界。四家族 F1 隐式前缀 / F2 请求内断点 / F3 显式缓存资源 / F4 网关映射。Gemini 隐式与显式拆行。9 个正交维度。R1 按来源边界派 5 个实体工人（OpenAI、Anthropic、Gemini、DeepSeek、OpenRouter）+ 1 个 scout。国内三家整行留 ❓，R2 再打，避免 R1 用「再全面查一遍」盖过种子文档站。

taxonomy：v0 建立，尚未用证据改轴。

spawn：0

字数：无成稿。

## R1

观察：6 份笔记均可解析（140 条 official，0 条缺 src/quote）。超长笔记：r1-openai、r1-gemini、r1-scout，收束时只采用摘录能对上的句子。用户听说的「Anthropic 必须逐块打 cache_control」被 2026-02-19 顶层 automatic 推翻；「零标记绝不缓存」仍无逐字句。OpenAI 默认仍自动，但 gpt-5.6+ 的 explicit 且无断点会整段跳过。DeepSeek 仍默认开启并忽略 cache_control。Gemini 官方写明是两套机制。OpenRouter 的 prompt cache 在上游，另有命中免费的整响应缓存。

taxonomy：v0→v1。v0 把 OpenAI 只放进隐式前缀，装不下「默认同 implicit、又可切 explicit」。轴改为「默认路径要不要放缓存标记」。计费不并进家族：GPT-5.6+ 零标记仍收 1.25× 写费。

格子：OpenAI D4 ⚔（retention 的 future models only 24h vs ttl=30m）。Anthropic D9 ⚔（2026-02-19 平台范围窄于现行指南）。DeepSeek D3 ⚠（64 token 只在已声明改价的 2024 公告）。Gemini 隐式 D4/D5 ∅，D3 ❓（分模型表的数字不在摘录）。Kimi/智谱/通义整行 ❓（scout 只进 leads）。

新增：四家+OpenRouter 的触发、TTL、计费、命中字段、失效。为守住 9000，删掉未摘录的倍率、2048/4096 档、gpt-4o 标价，以及 scout 里的变体细节。字数：无成稿 → 8983。

spawn：6（r1-openai、r1-anthropic、r1-gemini、r1-deepseek、r1-openrouter、r1-scout）。

R1 观察：核心疑点的边界主张还没单独反证；国内三家整行是用户点名的缺口；OpenAI TTL 是关键 ⚔。→ 动作：R2 只打这三件事，不重查已 ✅ 的格。→ 预计 spawn：6（Kimi、智谱、通义各一人；Anthropic 只反证零标记并补门槛表原句；OpenAI 只裁定 retention 与 ttl=30m；Gemini 只抄隐式门槛表和隐式倍率/TTL）。DeepSeek 的 64 token、OpenRouter markup、火山/Bedrock 留到下一轮，避免这一轮变宽。
