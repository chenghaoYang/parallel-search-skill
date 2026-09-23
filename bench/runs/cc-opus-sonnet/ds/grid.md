# grid（taxonomy v2，R2 收束后）

状态图例（不放表格里）：
- ✅ 一手来源 + 原文摘录；⚠ 只有二手；⚔ 来源冲突；❓ 缺口；∅ 官方未写（已定向查过）；— 不适用

## 分类轴 v1
- A1 请求形状谱系：Chat（messages→choices）/ Items（input items→output items）/ Blocks（content blocks）/ Parts（contents→parts）。
  v1 新增：Google Interactions API（2026-06 GA，服务端状态）作为 Google 第二个参照入口，形状待 R2。
- A2 状态在哪端：无状态 / 可选服务端状态。v1 细化：「兼容 Responses」≠ 托管状态（OpenRouter、Ollama 只做无状态；智谱默认 store=false）。
- A3 实体角色：参照协议 / 参照厂商自家兼容层 / 第三方模型厂兼容实现 / 网关与自托管 / 开放规范（Open Responses）。

## 维度 v1（v0→v1：新增 D11、D12）
- D1 端点鉴权：打到哪个 URL、用什么 header 鉴权、版本怎么指定？
- D2 输入结构：对话放在哪个字段、有哪些角色、system 放哪、多模态块叫什么？
- D3 状态：历史谁保存？有哪些服务端状态字段，保留多久？
- D4 输出结构：结果在哪个容器里，能否多候选，拒答怎么表示？
- D5 工具调用：工具怎么声明、调用怎么表示（id、参数类型）、结果怎么回传、有哪些内置工具？
- D6 推理：推理强度怎么控制、推理内容是否返回、多轮/工具循环时要不要原样回传？
- D7 结构化输出：JSON Schema 约束用哪个参数、是否严格？
- D8 流式：怎么开启、事件怎么分帧、怎么结束、用量何时给？
- D9 生成参数：max tokens 叫什么/是否必填、temperature 范围、top_k/stop/n/seed？
- D10 停止与用量缓存：停止原因枚举、usage 字段名、缓存怎么触发和计量？
- D11 协议入口（仅兼容实体）：同一厂商暴露哪些协议（Chat / Responses / Messages / 原生），base URL 各是什么？
- D12 不支持字段的处理（仅兼容实体）：静默忽略、截断/重映射，还是 400？

## 网格（v2，R3 收束后）

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OAI-Chat | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| OAI-Resp | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| ANT-Msg | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| GGL-Gen | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| GGL-Interactions（Steps） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| DeepSeek Chat/ANT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DeepSeek Responses（Q1） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 智谱 v4/Responses | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 智谱 ANT 兼容（Q2） | ✅ | ✅ | — | ∅ | ✅ | ✅ | ∅ | ∅ | ∅ | ∅ | ✅ | ∅ |
| Kimi | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Qwen/百炼 | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ∅ |
| 自家兼容层（ANT→OAI、Gemini→OAI） | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MiniMax | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❓ | ❓ | ✅ | ✅ | ✅ | ✅ |
| 火山方舟 Ark | ✅ | ❓ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ∅ |
| Open Responses 规范 | — | ✅ | ✅ | ✅ | ✅ | ✅ | ❓ | ❓ | — | — | ✅ | ✅ |
| 网关/自托管/云 | — | — | ✅ | — | — | — | — | — | — | — | ✅ | — |

## taxonomy v1→v2
- A1 新增第 5 个形状家族 Steps（Gemini Interactions：Content 无 role，角色靠 Step.type；扁平函数声明；event_type 流式）。
- A3 新增解释：第三方兼容端点按 Codex / Claude Code 需要裁剪（custom 只支持 apply_patch、Coding Plan 专用网关）。
- §3 改为按家族分表（Items / Blocks / Chat 兼容实现各一张），Q1/Q2 的细节落在对应行，不再单列。

## 冲突登记（⚔）
- R3：Qwen D10 部分裁决（cached_tokens 两页一致；cache_creation_input_tokens 按参数页 cache_creation 对象）；MiniMax 新增 ⚔：Responses 端 temperature (0,1] vs Chat/Anthropic 端 [0,2]；R2 所记 MiniMax signature/cache_control「未文档化」被 OpenAPI 参考页推翻。
- R2 已裁：OAI-Resp D8（Responses 流无 [DONE]，schema 级确认）；OAI-Resp D6（无状态模式默认返回 encrypted_content，include 写法 legacy；store:true 情形未写明，留 §5）；Ark D1（/api/coding* 是 Coding Plan 独立网关）。
- R2 新增：Interactions safety_settings（参考页列出 vs 概览页称不支持）；方舟 thinking.type（Chat 用 auto，Anthropic 端用 adaptive）；MiniMax thinking signature（示例有、参考页未写）。
- （R1 登记）OAI-Resp D6：openapi.yaml 称 reasoning.encrypted_content「populated by default」，但 include 枚举仍把它列为需显式选择。
- （R1 登记）OAI-Resp D8：OpenAI 侧只从示例推断「无 [DONE]」；智谱把「流式结束不发 [DONE]」列为与 OpenAI Responses 的差异 → 需一手确认 OpenAI Responses 流是否以 [DONE] 结束。
- （R1 登记）GGL-Gen D2：Content.role「只能 user/model」vs functionDeclarations 说明写 FunctionResponse 用 role "function"（同页）。
- （R1 登记）Qwen D5：tool_choice=required 支持范围两页不同；Qwen D10：缓存 usage 字段路径两页不同。
- （R1 登记）Ark D1：/api/v3 vs /api/coding/v3。
- （R1 登记）Kimi D9（已按时效裁决）：迁移指南 temperature [0,1] 可调 vs 模型总览「固定」→ 取模型总览（现役模型）。
