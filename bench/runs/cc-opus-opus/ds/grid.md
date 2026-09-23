# grid v2（R3 收束后更新状态；taxonomy 未变）

## 分类轴
- A1 代际（主轴）：一代「无状态 · 消息列表」= CC / Messages / generateContent；二代「可选服务端状态 · 类型化条目 · 语义流事件」= Responses（+Open Responses）/ Gemini Interactions
- A2 切分粒度（一代内部）：整条消息（CC）/ 类型化 content blocks（Messages）/ parts（generateContent）
- A3（下游专用）协议面：同一厂商暴露 CC / Messages / Responses 中的哪几种；Responses 兼容再分「有状态 / 忽略 / 拒绝」
- A4 与协议的关系：所有者 / 兼容实现 / 网关 / 自托管 / 云托管

## 维度（这一列回答什么）
| 列 | 名称 | 问题 |
|---|---|---|
| D1 | 接入 | 怎么连上？base URL、路径、鉴权头、版本头、模型名在 URL 还是 body |
| D2 | 对话形状 | 容器字段、角色集合、system 放哪、同角色连续规则 |
| D3 | 多模态 | 图片/音频/文件用什么块类型和字段？ |
| D4 | 工具 | 定义 schema、调用表示、结果回传与关联 id、tool_choice、strict、内置工具 |
| D5 | 状态 | 对话历史谁保存？留存期多久？ |
| D6 | 推理 | 怎么开关/控制？怎么返回？多轮/工具循环是否必须回传？ |
| D7 | 输出控制与采样 | 结构化输出字段；长度参数名/是否必填；采样参数是否被拒/弃用 |
| D8 | 流式 | 事件形状、结束标记、用量在哪 |
| D9 | 响应与停止 | 结果字段、停止原因枚举、用量字段口径 |
| D10 | 缓存 | 自动还是显式？怎么报告？ |
| D11 | 兼容度 | （兼容实体）参考字段支持/忽略/报错；不支持时静默忽略还是报错；私有扩展 |
| D12 | 错误 | 错误体形状、特有状态码 |

## 网格
| 实体 | A1/A4 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OA-CC OpenAI Chat Completions | 一代 所有者 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| OA-R OpenAI Responses | 二代 所有者 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| AN-M Anthropic Messages | 一代 所有者 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| GG-GC Gemini generateContent（legacy） | 一代 所有者 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| GG-IA Gemini Interactions | 二代 所有者 | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ | — | ✅ |
| DS DeepSeek | CC+M+R 兼容 | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ZP 智谱（CC/R 端点） | CC+M+R | ✅ | — | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ZP-M 智谱 Anthropic 端点 | M 兼容 | ✅ | ⚠ | ⚠ | ✅ | — | ✅ | ∅ | ⚠ | ⚠ | ⚠ | ✅ | ⚠ |
| MS Kimi | CC+M+R | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | — |
| MM MiniMax | M+CC+R | ✅ | — | ✅ | ⚔ | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | — |
| QW Qwen / 百炼 | CC+R+M+原生 | ✅ | ✅ | — | ✅ | ✅ | ⚔ | ✅ | — | ✅ | ✅ | ✅ | — |
| ARK 火山方舟 | CC+R+M | ✅ | — | — | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | — |
| GG-OAI Gemini 的 OpenAI 兼容层 | CC 兼容（源头厂） | ✅ | — | — | ✅ | — | ✅ | ✅ | — | — | — | ✅ | — |
| AN-OAI Anthropic 的 OpenAI 兼容层 | CC 兼容（源头厂） | ✅ | ✅ | — | ✅ | — | ✅ | ✅ | — | — | — | ✅ | — |
| ORS Open Responses 规范 | 二代 开放化 | ✅ | ✅ | — | — | ✅ | — | — | ✅ | — | — | ✅ | — |
| GW 网关（OpenRouter / LiteLLM） | 归一化 | ✅ | — | — | — | — | ✅ | — | — | — | — | ✅ | — |
| SH 自托管（vLLM / Ollama / SGLang / llama.cpp） | 多协议兼容 | ✅ | — | — | — | — | — | — | — | — | — | ✅ | — |
| CL 云托管（Bedrock / Vertex-Claude / Azure） | 转封装 | ✅ | ✅ | — | — | — | — | — | — | — | — | ✅ | — |

状态：✅ 一手+原文 · ⚠ 仅二手 · ⚔ 冲突 · ❓ 缺口 · ∅ 官方未写（已查） · — 不适用

## 冲突与缺口备忘（R2）
- GG-IA D1：参考页 `/v1beta`（另有 v1）vs v1 参考页 `/v1` vs 迁移指南示例 `/v1beta2`（官方文档自相矛盾，无法再核）
- GG-IA D7：文字说明提到 temperature，OpenAPI/SDK schema 无；safety_settings "not supported" vs 参考页有字段
- MM D4：Anthropic 层 tool_choice "Fully supported" vs "Only auto and none"（R2 复核：同日两页，非版本差异）
- QW D6：思考模式是否仅流式（两页不一）
- ZP D6：R2 判明为通道差异（标准 API 报错 / Coding Plan 转 low），不再列冲突
- ZP-M：官方仍无字段级文档（∅ 已定向查两轮）；⚠ 格来自 2026-05～09 GitHub 报告
- R3 补齐：OA-CC 内置工具与采样、GG-OAI 结构化输出（SDK parse）、DS 图片输入、Qwen 推理回传（preserve_thinking）。
- ❓ 残余（不在网格格内）：MiniMax OpenAI 层 tool_choice（原生端点有 none/auto，OpenAI 层页未写）；Qwen 工具调用回传；各家 Responses 对未知字段的处理。QW D6 ⚔（仅流式）R3 复核仍无法裁决。
