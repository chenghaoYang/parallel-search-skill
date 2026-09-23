# r3-qwen-responses
question: 百炼 Responses 兼容接口的推理表示、不支持字段与状态保存期限；Anthropic 兼容鉴权 header；裁决 R1 的缓存字段冲突（D10）。
checked: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api, https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses, https://help.aliyun.com/zh/model-studio/anthropic-api-messages, https://help.aliyun.com/zh/model-studio/context-cache, https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions, https://help.aliyun.com/zh/model-studio/error-code

## claims
- [C1] store参数默认值与作用 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "store boolean（可选）默认值为 true"；"false：不储存，对话内容不能被 previous_response_id 和后续 API 使用" | type: official
- [C2] previous_response_id保存期限7天 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "previous_response_id string（可选）上一个响应的唯一 ID，当前响应id有效期为7天" | type: official
- [C3] 推理内容以reasoning类型输出项返回，含summary必选字段 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "type string（必选）固定为 reasoning"；"summary array（必选）思考摘要内容" | type: official
- [C4] reasoning.effort思考强度7档 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "effort string（可选）：思考强度档位。支持 none、minimal、low、medium、high、xhigh、max 共 7 个递增档位" | type: official
- [C5] 明确不支持background异步参数 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "不支持部分 OpenAI Responses API 参数，例如异步执行参数background（当前仅支持同步调用）等" | type: official
- [C6] 兼容总览页对reasoning的措辞 | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "思考内容通过 reasoning 类型的输出项返回" | type: official
- [C7] 流式事件类型（未见[DONE]原句） | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "response.created"/"response.completed"/"response.output_text.delta"等event字段值出现在流式示例中 | type: official
- [C8] Anthropic兼容鉴权二选一 | src: https://help.aliyun.com/zh/model-studio/anthropic-api-messages | quote: "通过 x-api-key 请求头或 Authorization: Bearer 请求头传入百炼 API Key，二者选其一即可" | type: official
- [C9] Anthropic兼容curl示例用x-api-key | src: https://help.aliyun.com/zh/model-studio/anthropic-api-messages | quote: "-H "x-api-key: $DASHSCOPE_API_KEY"" | type: official
- [C10] context-cache页JSON示例仅含cached_tokens | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "usage": {"prompt_tokens": 3019, "completion_tokens": 104, "total_tokens": 3123, "prompt_tokens_details": {"cached_tokens": 2048}}（命中缓存案例，代码块内无cache_creation_input_tokens） | type: official
- [C11] 同页cache_creation_input_tokens仅见于变量访问语句非JSON schema | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "first_completion.usage.prompt_tokens_details.cache_creation_input_tokens"（代码示例中的变量访问写法，未见于正式JSON字段表） | type: secondary
- [C12] chat-completions参数页cache_creation为独立同级对象 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "cache_creation object：[显式缓存]创建信息"，与prompt_tokens_details同级，含ephemeral_5m_input_tokens、cache_creation_input_tokens、cache_type三子字段 | type: official
- [C13] prompt_tokens_details完整子字段清单 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions | quote: "audio_tokens、cached_tokens、text_tokens、image_tokens、video_tokens"为prompt_tokens_details五个子字段 | type: official

## conflicts
- 【D10裁决】cached_tokens路径两页一致（均为usage.prompt_tokens_details.cached_tokens，见C10/C13），不冲突。cache_creation_input_tokens路径仍冲突：context-cache页仅在Python变量访问语句里出现"prompt_tokens_details.cache_creation_input_tokens"这一写法（C11，且该页正式JSON示例代码块里完全不出现该字段，见C10）；chat-completions参数页的正式schema表格明确将cache_creation_input_tokens放在独立的cache_creation对象下、与prompt_tokens_details同级（C12）。两处并非"同一响应里并存的两个不同字段"，而是对同一字段路径的两种不同记法，倾向认为chat-completions页的正式schema表更权威（结构完整、非孤立代码变量名），但未能用一手抓包响应验证，故仍标记为未完全裁决，建议读者以chat-completions参数页的cache_creation.cache_creation_input_tokens为准。

## gaps
- 未找到"encrypted_content"字段的官方文档记载（在Responses兼容总览页与参考页均未出现）。
- 未找到官方"不支持/忽略字段"完整清单，仅C5明确点名background一例，原句用"等"字暗示还有其他未列出项。
- 未找到"未知/不支持请求字段是报错还是静默忽略"的官方说明；error-code页逐字检查后未见unrecognized/invalid_parameter类未知字段错误码。
- 未见流式响应末尾是否发送[DONE]或等价终止标记的官方原句，仅确认存在response.completed等命名事件。
- 未找到"previous_response_id引用已过期/已删除response"时的报错行为原句。

## leads
- pplx综合（非一手）提到百炼另有独立的请求加密机制，header为X-DashScope-EncryptionKey，页面https://help.aliyun.com/zh/model-studio/encrypted-access-to-model-inference，与OpenAI的encrypted_content无关，未核实原句。
- Anthropic兼容鉴权header的英文版页面（alibabacloud.com/help/en/model-studio/anthropic-api-messages）未核实，若需双语对照可补查。
