# r1-qwen
question: 阿里云百炼 / Model Studio（DashScope）上的 Qwen API 提供哪些协议端点——OpenAI 兼容 Chat Completions（compatible-mode）、OpenAI Responses 兼容（若有）、Anthropic 兼容（若有）、DashScope 原生协议——各自的端点与相对参考协议的差异？
checked: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions, https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope, https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api, https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses, https://help.aliyun.com/zh/model-studio/anthropic-api-messages, https://help.aliyun.com/zh/model-studio/regions, https://www.alibabacloud.com/help/en/model-studio/regions, https://help.aliyun.com/zh/model-studio/deep-thinking, https://help.aliyun.com/zh/model-studio/context-cache, https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope

## claims
- [C1] [D1] Chat 端点（北京示例；页 2026-09-22） | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "HTTP 请求地址：POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" | type: official
- [C2] [D1] 旧 base_url 与迁移目标 | src: https://help.aliyun.com/zh/model-studio/regions | quote: "OpenAI 兼容接口：从 https://dashscope.aliyuncs.com/compatible-mode/v1 替换为 https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1" | type: official
- [C3] [D1] 旧域名自 2026-09-30 起不加新特性（页 2026-09-18） | src: https://help.aliyun.com/zh/model-studio/regions | quote: "DashScope 域名（dashscope.aliyuncs.com）自2026年9月30日起不再支持新特性。" | type: official
- [C4] [D1] Responses 新路径（与 Chat 同 base_url） | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "请尽快迁移至新版路径 /compatible-mode/v1/responses。" | type: official
- [C5] [D1] Anthropic 兼容端点（base_url 止于 /apps/anthropic） | src: https://help.aliyun.com/zh/model-studio/anthropic-api-messages | quote: "HTTP 请求地址：POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages" | type: official
- [C6] [D1] Anthropic 鉴权：x-api-key 或 Bearer | src: https://help.aliyun.com/zh/model-studio/anthropic-api-messages | quote: "支持通过 x-api-key 或 Authorization: Bearer 请求头传入" | type: official
- [C7] [D1] 原生端点分纯文本和多模态两条 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "纯文本模型（如qwen-plus）：POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation 多模态模型（如qwen3.7-plus或qwen3-vl-plus）：POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" | type: official
- [C8] [D2] 原生 HTTP 流式靠请求头 X-DashScope-SSE 开启 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "通过HTTP实现流式输出请在Header中指定X-DashScope-SSE为enable。" | type: official
- [C9] [D2] 原生请求体：messages 放 input 对象 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "通过HTTP调用时，请将messages放入 input 对象中。" | type: official
- [C10] [D2] result_format 等参数放 parameters 对象 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "通过HTTP调用时，请将 result_format放入 parameters 对象中。" | type: official
- [C11] [D9] 原生响应：result_format=message 时回复在 output.choices | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "当result_format为message时返回choices参数。" | type: official
- [C12] [D9] 原生 usage 用 input_tokens/output_tokens | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "为input_tokens与output_tokens之和。" | type: official
- [C13] [D6] enable_thinking：SDK 用 extra_body，HTTP 直接放 body 顶层 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "则无需 extra_body，直接将 enable_thinking 与 model、messages 等参数一样放在请求体（body）的顶层即可" | type: official
- [C14] [D6] 思考内容在 reasoning_content | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "开启后，思考内容将通过reasoning_content字段返回。" | type: official
- [C15] [D6] thinking_budget 经 extra_body 传 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "配置方式为：extra_body={"thinking_budget": xxx}。" | type: official
- [C16] [D6] 只支持思考模式的模型（部分） | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "仅思考模式：qwen3-next-80b-a3b-thinking、qwen3-235b-a22b-thinking-2507、qwen3-30b-a3b-thinking-2507" | type: official
- [C17] [D6] 只支持流式的模型 | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "部分模型（如 qwen3-235b-a22b、qwen3-32b 等开源版）仅支持流式输出，非流式调用会报错" | type: official
- [C18] [D4] parallel_tool_calls 默认 false | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "parallel_tool_calls boolean （可选）默认值为 false" | type: official
- [C19] [D4] 联网搜索 enable_search 是私有字段，经 extra_body 传 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "配置方式为：extra_body={"enable_search": True}。" | type: official
- [C20] [D5] previous_response_id：id 有效期 7 天 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "当前响应id有效期为7天。" | type: official
- [C21] [D5] store 默认 true | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "store boolean （可选）默认值为 true" | type: official
- [C22] [D5] 内置工具（web_search、code_interpreter、file_search、mcp 等）可和 function 混用 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "支持内置工具和自定义 function 工具，可混合使用。" | type: official
- [C23] [D7] Qwen 不支持 tool_choice="required" | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "Qwen 系列模型暂不支持required" | type: official
- [C24] [D7] max_completion_tokens 含思维链，max_tokens 只限回答 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "max_completion_tokens 限制模型完整输出（思维链 + 回答），而 max_tokens 仅限制回答部分。" | type: official
- [C25] [D7] json_object 模式要求提示词里有 JSON | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "若指定为{"type": "json_object"}，需在提示词中明确指示模型输出JSON" | type: official
- [C26] [D11] top_k 等非标准参数经 extra_body 传 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "配置方式为：extra_body={"top_k":xxx}。" | type: official
- [C27] [D10] 隐式缓存自动开启，无法关闭 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "隐式缓存：此为自动模式，无需额外配置，且无法关闭" | type: official
- [C28] [D10] 显式缓存在 messages 里加 cache_control ephemeral | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "在 messages 中加入"cache_control": {"type": "ephemeral"}标记" | type: official
- [C29] [D10] 显式缓存创建数报在 cache_creation_input_tokens | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "创建缓存所用的 Token数通过cache_creation_input_tokens 参数查看。" | type: official
- [C30] [D10] OpenAI 兼容：命中数计入 prompt_tokens | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "在usage.prompt_tokens_details.cached_tokens可以查看命中缓存的 Token 数（该数值为usage.prompt_tokens的一部分）" | type: official

## conflicts
- 弗吉尼亚 DashScope 域名：https://www.alibabacloud.com/help/en/model-studio/regions 写 "Not supported"；https://help.aliyun.com/zh/model-studio/regions 写 "dashscope-us.aliyuncs.com"
- 思考模式是否只能流式：https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope "Qwen3商业版（思考模式）、Qwen3开源版、QwQ、QVQ只支持流式输出。"；https://help.aliyun.com/zh/model-studio/deep-thinking "商业版深度思考模型同时支持非流式（同步）输出"
- tools 与 stream：https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope（2026-09-11）"The tools parameter cannot be used with stream=True simultaneously."；https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions tool_stream "仅在stream=true时生效。"

## gaps
- Chat 页没说明未列出的 OpenAI 参数如何处理（Responses 页写明忽略）
- Responses 页没有 text.format/json_schema 的说明

## leads
- Anthropic 兼容没有 /v1/models；缓存命中数在 cache_read_input_tokens，不计入 input_tokens
- 另有 conversations 与 GET/DELETE /responses/{id} 端点
- Responses：会话缓存头 x-dashscope-session-cache: enable；不支持 background
