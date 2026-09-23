# r2-kimi-responses
question: Kimi /v1/responses（Responses 兼容）服务端是否保存状态；store 默认值；previous_response_id/conversation 支持；不支持/忽略字段；推理内容表示方式；内置工具支持情况。
checked: https://platform.kimi.com/docs/api/overview, https://platform.kimi.com/docs/api/responses

## claims
- [C1][D3] store 字段固定为 false，不支持服务端保存 | src: https://platform.kimi.com/docs/api/responses | quote: "store: type: boolean description: 固定为 `false`。" | type: official
- [C2][D3] previous_response_id 固定为 null，不支持串联历史响应 | src: https://platform.kimi.com/docs/api/responses | quote: "previous_response_id: ... description: 固定为 `null`。" | type: official
- [C3][D3] conversation 固定为 null，不支持 conversation 对象 | src: https://platform.kimi.com/docs/api/responses | quote: "conversation: type: - object - 'null' description: 固定为 `null`。" | type: official
- [C4][D3] input 可为字符串（等价单条 user 消息）或数组（含历史/工具调用/结果），需客户端自管历史 | src: https://platform.kimi.com/docs/api/responses | quote: "传字符串等价于一条 user 消息；传数组时按顺序给出带类型的 item，可包含历史对话、工具调用与工具结果" | type: official
- [C5][D12] Responses 接口当前仅支持 kimi-k3 一个模型 | src: https://platform.kimi.com/docs/api/responses | quote: "使用的模型 ID。本接口当前支持 `kimi-k3`。" | type: official
- [C6][D3] 推理内容表示为 output 数组中独立 item（非字段嵌套），type=reasoning，含 id（如 rs_...） | src: https://platform.kimi.com/docs/api/responses | quote: "ResponsesOutputReasoningItem ... type: enum: - reasoning ... id: type: string example: rs_68f0c1c2d3e4f5a6b7c8d9e0" | type: official
- [C7][D3] reasoning item 内 summary 数组元素 type=reasoning_text，含 text 字段，status=completed | src: https://platform.kimi.com/docs/api/responses | quote: "type: enum: - reasoning_text ... text: type: string ... status: enum: - completed" | type: official
- [C8][D3] reasoning.effort 三档 low/high/max，默认 max | src: https://platform.kimi.com/docs/api/responses | quote: "effort: ... enum: - low - high - max default: max" | type: official
- [C9][D3] 内置工具仅支持四类：function/custom(仅apply_patch)/namespace/web_search，其他类型不支持 | src: https://platform.kimi.com/docs/api/responses | quote: "支持 `function`、`custom`（仅 `apply_patch`）、`namespace` 与 `web_search`，其他工具类型不支持" | type: official
- [C10][D3] web_search 工具部分参数不支持会报错，部分被忽略 | src: https://platform.kimi.com/docs/api/responses | quote: "`search_context_size`、`blocked_domains`、`filters.blocked_domains` 不支持，传入会返回 `invalid_request_error`；`user_location`、`external_web_access`、`indexed_web_access` 会被忽略" | type: official
- [C11][D3] 不支持显式缓存断点 prompt_cache_breakpoint，传入返回 HTTP 400 | src: https://platform.kimi.com/docs/api/responses | quote: "暂不支持显式缓存断点：`content` 中出现 `prompt_cache_breakpoint` 时请求会被拒绝（HTTP 400）" | type: official
- [C12][D3] 不支持手动清除缓存，前缀至少 5 分钟不活动后自动过期 | src: https://platform.kimi.com/docs/api/responses | quote: "不支持手动清除缓存，已缓存的前缀在至少 5 分钟不活动后自动过期" | type: official
- [C13][D3] status 枚举 in_progress/completed/incomplete/failed，达上限时 incomplete_details.reason=max_output_tokens | src: https://platform.kimi.com/docs/api/responses | quote: "status: type: string enum: - in_progress - completed - incomplete - failed" | type: official
- [C14][D3] 图片输入仅支持 base64 data URL，不支持公网 http(s) URL | src: https://platform.kimi.com/docs/api/responses | quote: "图片的 data URL，例如 `data:image/png;base64,<base64>`。不支持公网 http(s) URL。" | type: official
- [C15][D3] 流式事件含 reasoning_summary 专属事件，命名与 OpenAI Responses SSE 事件风格一致 | src: https://platform.kimi.com/docs/api/responses | quote: "response.reasoning_summary_part.added ... response.reasoning_summary_text.delta ... response.web_search_call.completed" | type: official

## gaps
- 页面未标注更新日期或版本/beta 标记。
- 未查到 max_tokens/max_output_tokens 之外，temperature/top_p/n 等采样参数在 Responses 端是否同样"固定不可改"（Chat Completions 端 kimi-k3 已固定，Responses 页未见对应参数表，未展开查）。
- 未找到官方对"为何 previous_response_id/conversation 固定 null"的解释性原句（可能是尚未实现，页面未说明原因）。

## leads
- image_generation/code_interpreter/file_search 等 OpenAI Responses 内置工具在 Kimi 端完全不在支持列表内（C9 隐含），如需逐条确认"不支持"需另开工单。
- Responses 与 Anthropic Messages 端点（R1 笔记）均把可用模型限定为仅 kimi-k3，Chat Completions 端支持 kimi-k3/kimi-k2.7-code/kimi-k2.6 三个模型，形成"新协议端点只跟旗舰模型走"的一致模式。
