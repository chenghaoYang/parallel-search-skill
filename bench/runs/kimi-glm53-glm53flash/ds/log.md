# log

## R0
观察：任务为四大主流 LLM API 请求协议对照 + 下游兼容差异 + 用户点名疑点（DeepSeek vs OpenAI、智谱 vs Anthropic）。→ 动作：建 taxonomy v0（12 实体 × 11 维度，四家族分类轴），规划 R1 共 6 个工人（2 批，每批 ≤3），含 1 个 scout。 → spawn：6（未派出）。字符：0。

## R1（spawn 6：openai-chat / openai-responses / anthropic-messages / google-gc / deepseek / scout，2 批）
结果：168 claims（official 168）；四主流行基本 ✅；deepseek 行 ✅；scout 给出兼容层坑。收束：grid v0→v1（行改按「协议面」划分，新增 deepseek-responses/deepseek-anthropic/google-interactions 行）；report.md 重写 17933 字符 ≤ 20000，快照 r1。填率 55/145。
R1 观察：① 点名疑点②智谱与 qwen/moonshot/xai/mistral 四行全 ❓；② google responseSchema 标弃用+新 Interactions API（谱系 D 可能换代）；③ openai 三处 ⚔（seed、parallel_tool_calls 默认、encrypted_content 默认）；④ deepseek 两处 ⚔（/responses 模型范围、strict 是否须 /beta）。→ 动作：R2 派 6 个定向工人（zhipu-anthropic 点名优先、google-interactions、openai-verify 核验、deepseek-faces、compat-cn=qwen+moonshot、compat-west=xai+mistral），每批 ≤3。 → 预计 spawn：6。

## R2（spawn 6：zhipu-anthropic / google-interactions / openai-verify / deepseek-faces / compat-cn / compat-west，2 批）
结果：317 claims（official 317）。智谱行：接入/模型映射/thinking/缓存 ✅，工具/SSE 逐项 ∅（官方零文档）；google-interactions 全行 ✅（GA 2026-06、generateContent legacy、response_format 取代 responseSchema、服务端状态）；openai 三处 ⚔ 全部裁决（seed 参数级弃用属实、parallel_tool_calls 默认 true、encrypted_content 默认填充）；deepseek ⚔ 裁决（responses 两模型均支持、strict 须 /beta）+ /anthropic 面 ✅；qwen/moonshot/xai/mistral 行 ✅（新 ⚔：百炼 tools×stream、xAI penalties 三口径）。收束：grid v1→v2（Interactions 归 D 族但注明向 B 收敛；分类轴仍成立）；report.md 从头重写并压回预算内 19996（新增 §2.7 Interactions、§3.1 多协议面总表、§3.3 智谱表、§3.4 下游表；为腾空间删/压：SO 模型下限、deepseek 缓存细节、来源标题精简、§4 由 12 条并 11 条、§5 合并）。填率 117/126（93%）。
R2 观察：① 剩余 ❓/∅ 中可文档解决的只剩：智谱 coding /api/v1（responses 面）、moonshot responses/anthropic 入口；② 两个 ⚔（百炼 tools×stream、xAI penalties）可定向核验；③ 核心格子全部 ✅/∅，接近停。→ 动作：R3 派 2 个定向工人（zhipu-coding-faces、moonshot-faces+百炼 tools×stream+xAI penalties 核验），随后终审 1 工人。 → 预计 spawn：3。

## R3（spawn 2：zhipu-coding、conflicts）
结果：41 claims。智谱 /api/v1 Responses 面 ✅（官方明示与 OpenAI 三差异：store 默认 false、流式无 [DONE]、无 cancel；/api/coding/paas/v4=Coding 套餐 OpenAI 入口）；百炼 tools×stream 裁决=已放开（tool_stream 非标参数管复杂工具，迁移页滞后）；xAI penalties 裁决=端点级×模型级两维叠加，非打架；Moonshot 双面入口 ✅（/docs/api/responses、/docs/api/messages）。收束：report 更新并压回 19991（新增智谱 responses 三差异、Kimi 双面、两处裁决结论；删/压：o 系 max_tokens 注、stop_reason 全枚举、qwen n 限制等 P2 细节）。
R3 观察：核心格子全部 ✅/∅，仅剩官方零文档项与 ⚠ 小项；轮数与收益均到位。→ 动作：终审——派 1 个审稿工人抽查 ≥20 条主张，随后按结果改稿并停。 → 预计 spawn：1。

## 终审（spawn 1：audit）
结果：抽查 47 条主张——39 supported / 8 weak / 0 unsupported / 0 contradicted；来源编号 [1]–[58] 连续、无悬空引用。按审计改稿 9 处：硬伤「§0.9」→「§0.8」；8 处 weak 全部降级/软化（Responses「无 [DONE]」、Gemini functionResponse「user role」、tool_choice「每工具开关」、mode ANY…、Interactions「无 role/parts」、Mistral conversations(β) 入表、DeepSeek「无 /v1」→「示例无 /v1」、智谱映射/计费句重写为有据版本）。终稿 19918 ≤ 20000，快照 report.final.md，并复制到 ./report.md。填率 117/126。停止：核心格子全部 ✅/∅，剩余为官方零文档项与 ⚠ 小项，已写入成稿 §5。
