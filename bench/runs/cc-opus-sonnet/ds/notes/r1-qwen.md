# r1-qwen
question: 阿里云百炼/DashScope（通义千问Qwen）对外提供哪些协议端点，各自相对参照协议（OpenAI Chat Completions、OpenAI Responses、Anthropic Messages）的偏差是什么？
checked: https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope, https://help.aliyun.com/zh/model-studio/deep-thinking, https://help.aliyun.com/zh/model-studio/qwen-function-calling, https://help.aliyun.com/zh/model-studio/context-cache, https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope, https://help.aliyun.com/zh/model-studio/anthropic-api-messages, https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope, https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api, https://help.aliyun.com/zh/model-studio/qwen-vl-compatible-with-openai, https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions, https://help.aliyun.com/zh/model-studio/base-url, https://help.aliyun.com/zh/model-studio/vision

## claims
- [C1][D1] OpenAI兼容base_url(按量付费) | src: https://help.aliyun.com/zh/model-studio/base-url | quote: "华北2（北京）：https://dashscope.aliyuncs.com/compatible-mode/v1"；新加坡dashscope-intl，弗吉尼亚dashscope-us，香港cn-hongkong.dashscope，均.../compatible-mode/v1 | type: official
- [C2][D1] 业务空间专属域名格式 | src: https://help.aliyun.com/zh/model-studio/base-url | quote: "https://{WorkspaceId}.[region].maas.aliyuncs.com/"，含北京/新加坡/东京/法兰克福/弗吉尼亚/香港 | type: official
- [C3][D1] DashScope原生端点 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "POST .../api/v1/services/aigc/text-generation/generation"（多模态为multimodal-generation/generation）；base-url页：原生=按量付费域名"路径替换为/api/v1" | type: official
- [C4][D1] Anthropic兼容base_url与路径 | src: https://help.aliyun.com/zh/model-studio/anthropic-api-messages | quote: "base_url：.../apps/anthropic；HTTP 请求地址：POST .../apps/anthropic/v1/messages"；按量付费北京为dashscope.aliyuncs.com/apps/anthropic | type: official
- [C5][D1] Anthropic兼容接口范围 | src: https://help.aliyun.com/zh/model-studio/anthropic-api-messages | quote: "仅提供 Messages 接口（/v1/messages），不提供模型列表接口（/v1/models）"，模型发现请求返回404 | type: official
- [C6][D1] Responses兼容端点 | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "POST .../compatible-mode/v1/responses"，同式端点覆盖新加坡/弗吉尼亚/法兰克福/东京/香港 | type: official
- [C7][D2] roles限制 | src: https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope | quote: "角色当前可选值：system、user、assistant，其中，仅messages[0]中支持role为system" | type: official
- [C8][D2] 视频输入type区分 | src: https://help.aliyun.com/zh/model-studio/vision | quote: "输入视频文件时"type"设为"video_url"；输入图片列表形式的视频时设为"video"" | type: official
- [C9][D2] image_url三种来源 | src: https://help.aliyun.com/zh/model-studio/vision | quote: "公网URL、Base64（data:image/png;base64,{base64_image}）、本地file://{文件的绝对路径}" | type: official
- [C10][D5] tool_choice默认值(function-calling页) | src: https://help.aliyun.com/zh/model-studio/qwen-function-calling | quote: "'auto'（默认）、'none'，kimi/kimi-k3 还支持 'required'" | type: official
- [C11][D5] tool_choice可选值列表(chat-completions参数页) | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "可选值：auto、none、required、{type:function,function:{name:...}}" | type: official
- [C12][D5] parallel_tool_calls | src: https://help.aliyun.com/zh/model-studio/qwen-function-calling | quote: "可设置请求参数parallel_tool_calls为true"；"Qwen-Omni-Realtime 系列不支持 tool_choice 和 parallel_tool_calls 参数" | type: official
- [C13][D5] enable_search非标准参数 | src: https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope | quote: "top_p、temperature、presence_penalty、n、max_tokens、seed、stream、stop、tools、stream_options、enable_search" | type: official
- [C14][D6] enable_thinking行为与默认值差异 | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "设为true：模型先思考再回复；设为false：模型直接回复"；千问3.8 Max系列默认开启思考模式，千问3商业版默认不开启 | type: official
- [C15][D6] thinking_budget定义与适用范围 | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "可设置推理过程的最大 Token 数，超过限制后模型立即输出回复"；适用Qwen3.8/3.7/3.6/3.5/3-VL/3系列及GLM/Kimi阿里云直供，kimi-k3不支持 | type: official
- [C16][D6] reasoning_content与content分离 | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "思考内容通过reasoning_content字段返回，回复内容通过content字段返回" | type: official
- [C17][D6] 部分模型仅支持流式 | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "部分模型（如 qwen3-235b-a22b、qwen3-32b 等开源版）仅支持流式输出，非流式调用会报错" | type: official
- [C18][D7] response_format三种取值 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "json_object：输出标准格式的JSON字符串；json_schema：输出严格符合指定JSON Schema的JSON字符串" | type: official
- [C19][D8] stream_options支持 | src: https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope | quote: "stream_options include_usage is supported for displaying token usage in streaming output" | type: official
- [C20][D8] incremental_output默认值随模型不同 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "默认false，Qwen3-Max/Qwen3-VL/Qwen3开源版/QwQ/QVQ默认true；true时后续输出不包含已输出内容" | type: official
- [C21][D8] 原生协议SSE header与result_format | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "X-DashScope-SSE: enable"；result_format可选text/message，默认text，Qwen3-Max等默认message | type: official
- [C22][D10] 隐式缓存自动开启不可关 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "此为自动模式，无需额外配置，且无法关闭" | type: official
- [C23][D10] 显式缓存需cache_control标记 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "在messages中加入cache_control: {type: ephemeral}标记" | type: official
- [C24][D10] OpenAI兼容/DashScope原生usage缓存字段(context-cache页) | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "usage.prompt_tokens_details.cache_creation_input_tokens/.cached_tokens（OpenAI兼容）；同路径方括号写法（DashScope原生）" | type: official
- [C25][D10] chat-completions参数页usage缓存字段(嵌套路径不同) | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "cached_tokens：命中 Cache 的 Token 数"；"cache_creation object...ephemeral_5m_input_tokens：创建显式缓存的 Token 数" | type: official
- [C26][D10] Anthropic兼容usage字段(顶层非嵌套) | src: https://help.aliyun.com/zh/model-studio/anthropic-api-messages | quote: "input_tokens、output_tokens、cache_creation_input_tokens、cache_read_input_tokens" | type: official
- [C27][D10] 缓存有效期与最小Token阈值 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "缓存有效期为 5分钟（命中后重置）"；"缓存最少 Token 数：1024" | type: official
- [C28][Anthropic兼容] 支持参数清单 | src: https://help.aliyun.com/zh/model-studio/anthropic-api-messages | quote: "model、max_tokens、system、messages、stream、temperature、top_p、top_k、stop_sequences、thinking、tools、tool_choice、output_config" | type: official
- [C29][Anthropic兼容] temperature范围偏差 | src: https://help.aliyun.com/zh/model-studio/anthropic-api-messages | quote: "百炼取值范围为 [0, 2)，与 Anthropic 官方的 [0.0, 1.0] 不同" | type: official
- [C30][Responses兼容] 内置工具 | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "内置联网搜索、网页抓取、代码解释器、文搜图、图搜图等工具" | type: official
- [C31][Responses兼容] previous_response_id续接上下文 | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "通过传递上一轮响应的 previous_response_id，无需手动构建完整的消息历史数组" | type: official

## conflicts
- tool_choice"required"范围：C10称仅kimi/kimi-k3支持required；C11(参数页)列出required未限定模型。两官方页不一致，未裁决。
- usage缓存字段命名：C24(context-cache页)称OpenAI兼容为扁平字段cache_creation_input_tokens；C25(参数页)称在嵌套对象cache_creation.ephemeral_5m_input_tokens下。路径不同，未裁决。

## gaps
- Responses兼容页未给出官方"不支持/部分支持字段"逐条清单。
- vision页未给出支持视频理解的完整模型清单，仅示例出现qwen3.8-max/qwen3.7-plus。
- 英文compatibility-of-openai-with-dashscope页WebFetch提取时"Beijing"与"Singapore"网址重复，疑似抓取误差，未采信入claims。
- 多数页面"更新时间："后日期未被WebFetch提取到，无法标注版本日期。
- 未检索github.com/QwenLM，本轮聚焦协议层文档。

## leads
- openai-compatible-conversations页：OpenAI Conversations兼容层，配合Responses自动管理历史，可能是D1额外入口，未核实。
- Qwen-Audio称"不支持OpenAI兼容协议"（仅原生），或可作表格脚注例外（来自pplx线索，未直接核实原句）。
