# Taxonomy grid v2

v0→v1：分类轴不变。实体从「公司」拆成「端点」。
v1→v2：加上 Interactions。它用 `previous_interaction_id` 把状态放在服务端，工具结果是 `function_result`，不是 generateContent 的 `functionResponse`。总览与参考页对它是否取代 generateContent 仍冲突，所以不把它写成「Google 的唯一现行协议」。

| 家族 | 为什么是一类 | 参照 | 已核适配 |
|---|---|---|---|
| Chat Completions | 客户端每轮重放 `messages[]`；工具结果多是 `role=tool` | OpenAI Chat | DeepSeek Chat、智谱 Chat、百炼 compatible-mode、Moonshot；Gemini 另有一条官方 OpenAI 兼容层 |
| Responses | 输入/输出是 item；服务端 id 可有可无 | OpenAI Responses | DeepSeek Responses（形状像，但文档写明不存会话） |
| Messages | 顶层 `system` + typed blocks；工具结果在 user 的 `tool_result` | Anthropic Messages | 智谱 Messages（只有路径和一句「有差异」，无字段表） |
| generateContent | `contents[].parts[]`，`systemInstruction`，`generationConfig` | Gemini `:generateContent` | 官方 OpenAI 兼容层属于 Chat 家族 |
| Interactions | 服务端 `previous_interaction_id`；step 不是 part | Gemini `POST /interactions` | 无下游行。是否取代上一行，文档冲突 |

未进矩阵的 leads：百炼 Anthropic / Responses 页、xAI Responses、Mistral Conversations、Bedrock 四族、Cohere `/v2/chat`。

## 维度

| ID | 这一列回答什么 |
|---|---|
| D1 | 请求打到哪条路径、必需 header 叫什么？ |
| D2 | 下一轮靠客户端全量重放，还是靠服务端 id？ |
| D3 | 角色枚举有哪些，content 是字符串还是块？ |
| D4 | 系统指令放在哪个字段？ |
| D5 | 工具如何声明，工具结果以什么角色或块回传？ |
| D6 | 最大长度、温度、思考/推理的请求字段叫什么？ |
| D7 | 流式开关在哪，如何结束？ |
| D8 | 非流式正文、结束原因、usage 的字段路径？ |
| D9 | 强制 JSON / schema 的请求字段叫什么？ |
| D10 | 相对被模仿的官方协议，文档写明少了、改了、多了什么？ |

## 格子

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| OpenAI Chat Completions | ✅ | ⚔ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ |
| OpenAI Responses | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Anthropic Messages | ✅ | ✅ | ⚔ | ⚔ | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ |
| Gemini generateContent | ⚔ | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ |
| DeepSeek Chat | ✅ | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ | ⚔ |
| DeepSeek Responses | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 智谱 Chat | ✅ | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ⚔ | ✅ | ✅ |
| 智谱 Messages | ✅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ✅ |
| 百炼 compatible-mode | ⚔ | ✅ | ✅ | ⚔ | ⚔ | ✅ | ✅ | ⚔ | ✅ | ✅ |
| Moonshot Chat | ✅ | ✅ | ⚔ | ✅ | ⚔ | ⚔ | ⚔ | ✅ | ✅ | ✅ |
| MiniMax Messages | ✅ | ✅ | ✅ | ✅ | ⚔ | ⚔ | ✅ | ⚔ | ∅ | ✅ |
| Gemini Interactions | ✅ | ✅ | ❓ | ❓ | ✅ | ❓ | ✅ | ✅ | ✅ | ⚔ |

智谱 Messages 的 ∅ 是两轮定向查过（含 sitemap 236 条）仍没有字段表。D10=✅ 只表示官方承认有差异但未列清单。DeepSeek Responses 的 D5 从 ⚔ 改为 ✅：`tool_choice` 的 400 只写在 Chat。Interactions 的 D3/D4/D6 本轮没派。Gemini generateContent 的 D9 仍是 ⚔。
