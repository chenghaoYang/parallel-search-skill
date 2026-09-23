# r2-deepseek-conflicts
question: DeepSeek 官方三处冲突各自的原句到底约束哪一个端点、哪一个字段？
checked: https://api-docs.deepseek.com/guides/thinking_mode | https://api-docs.deepseek.com/api/create-chat-completion | https://api-docs.deepseek.com/api/create-response | https://api-docs.deepseek.com/guides/responses_api

## claims
- [C1] Chat D6，字段 reasoning_effort：思考页 OpenAI 列、Thinking Effort Control 行。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "{"reasoning_effort": "low/high/max"}" | type: official
- [C2] Responses，字段 reasoning.effort：思考页 Responses 列 rowspan 盖住 Toggle 与 Effort；不是 Responses D5。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "{"reasoning": {"effort": "none/low/high/max"}} (none disables thinking mode)" | type: official
- [C3] 未标端点，脚注 (2) 在行标签 Thinking Effort Control 上：表行左格 ultra、右格 max。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "The mapping between the effort set by the user and the model's actual reasoning effort is as follows:" | type: official
- [C4] Chat D6，字段 reasoning_effort：POST /chat/completions。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "none disables thinking mode; low / high / max enable thinking mode." | type: official
- [C5] Chat D6，字段 reasoning_effort：同页兼容映射。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "For compatibility with existing software, minimal is accepted and mapped to low, and medium / xhigh are accepted and mapped to high." | type: official
- [C7] Responses，字段 reasoning.effort：POST /responses，不是 D5。 | src: https://api-docs.deepseek.com/api/create-response | quote: "none disables thinking mode; low / high / max enable thinking mode." | type: official
- [C8] Responses，字段 reasoning.effort：同页兼容映射。 | src: https://api-docs.deepseek.com/api/create-response | quote: "For compatibility with existing software, minimal is accepted and mapped to low, and medium / xhigh are accepted and mapped to high." | type: official
- [C9] 未标路径，字段 presence_penalty：思考页 Input and Output Parameters；原句也点名 temperature 与 frequency_penalty，本条只记 presence_penalty。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "Thinking mode does not support the temperature, presence_penalty, or frequency_penalty parameters." | type: official
- [C10] 未标路径，字段 frequency_penalty：与 C9 同一句，本条只记 frequency_penalty。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "Thinking mode does not support the temperature, presence_penalty, or frequency_penalty parameters." | type: official
- [C11] 未标路径，字段 presence_penalty：these parameters 回指上一句。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "Please note that, for compatibility with existing software, setting these parameters will not trigger an error but will also have no effect." | type: official
- [C12] 未标路径，字段 frequency_penalty：与 C11 同一句，回指也包括 frequency_penalty。 | src: https://api-docs.deepseek.com/guides/thinking_mode | quote: "Please note that, for compatibility with existing software, setting these parameters will not trigger an error but will also have no effect." | type: official
- [C13] Chat D10，字段 presence_penalty：POST /chat/completions，标 deprecated，不写 Thinking mode。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "This parameter is no longer supported." | type: official
- [C14] Chat D10，字段 frequency_penalty：同页另一属性，同文，标 deprecated。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "This parameter is no longer supported." | type: official
- [C15] Chat D10，字段 presence_penalty：同属性下一句。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "It will not take effect if you pass it to the API." | type: official
- [C16] Chat D10，字段 frequency_penalty：同页下一句，与 C15 同文。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "It will not take effect if you pass it to the API." | type: official
- [C17] Chat D5，字段 tool_choice：只在 POST /chat/completions。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "required and named tool choices are not supported in thinking mode; the API returns a 400 error." | type: official
- [C18] Chat D5，字段 tool_choice：同一属性下一句。 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Disable thinking mode first to use them." | type: official
- [C19] Responses D5，字段 tool_choice：指南顶层参数表，无思考模式、无 400。 | src: https://api-docs.deepseek.com/guides/responses_api | quote: "Supported. none / auto / required / a specific tool ({"type": "function", "name": ...})" | type: official
- [C20] Responses D5，字段 tool_choice：POST /responses 的 required，无 400。 | src: https://api-docs.deepseek.com/api/create-response | quote: "required means the model must call one or more tools." | type: official
- [C6] Responses D5，字段 tool_choice：POST /responses 的具名选择，无 400。 | src: https://api-docs.deepseek.com/api/create-response | quote: "Specifying a particular tool via {"type": "function", "name": "my_function"} forces the model to call that tool." | type: official

## conflicts
- Chat 字段 reasoning_effort：https://api-docs.deepseek.com/guides/thinking_mode "{"reasoning_effort": "low/high/max"}" vs https://api-docs.deepseek.com/api/create-chat-completion "none disables thinking mode; low / high / max enable thinking mode."
- Chat 字段 reasoning_effort 别名：https://api-docs.deepseek.com/guides/thinking_mode "The mapping between the effort set by the user and the model's actual reasoning effort is as follows:" 下表行左格 ultra、右格 max vs https://api-docs.deepseek.com/api/create-chat-completion "For compatibility with existing software, minimal is accepted and mapped to low, and medium / xhigh are accepted and mapped to high."
- Responses 字段 reasoning.effort 别名（D6，不是 D5）：同一思考页引导句与 ultra / max vs https://api-docs.deepseek.com/api/create-response "For compatibility with existing software, minimal is accepted and mapped to low, and medium / xhigh are accepted and mapped to high."
- Chat 字段 presence_penalty：https://api-docs.deepseek.com/guides/thinking_mode "Thinking mode does not support the temperature, presence_penalty, or frequency_penalty parameters." 与 "Please note that, for compatibility with existing software, setting these parameters will not trigger an error but will also have no effect." vs https://api-docs.deepseek.com/api/create-chat-completion "This parameter is no longer supported." 与 "It will not take effect if you pass it to the API."
- Chat 字段 frequency_penalty：同一对思考页原句 vs https://api-docs.deepseek.com/api/create-chat-completion "This parameter is no longer supported." 与 "It will not take effect if you pass it to the API."
- 字段 tool_choice（Chat D5 vs Responses D5，跨端点）：https://api-docs.deepseek.com/api/create-chat-completion "required and named tool choices are not supported in thinking mode; the API returns a 400 error." 与 "Disable thinking mode first to use them." vs https://api-docs.deepseek.com/guides/responses_api "Supported. none / auto / required / a specific tool ({"type": "function", "name": ...})" 与 https://api-docs.deepseek.com/api/create-response "required means the model must call one or more tools." 与 "Specifying a particular tool via {"type": "function", "name": "my_function"} forces the model to call that tool."

## gaps
- 四页无 dateModified / lastUpdated。样例 2026-04-19 不是更新日期。
- create-chat-completion、create-response、responses_api 无 ultra 一词。
- create-response 与 responses_api 无 presence_penalty、frequency_penalty。
- thinking_mode 无 tool_choice；该页唯一 400 只写没回传 reasoning_content。responses_api 的 reasoning 行无 effort 枚举。

## leads
- Responses 的 reasoning.effort 枚举属 D6 不属 D5；思考页 Anthropic 列是 {"output_config": {"effort": "low/high/max"}}，Toggle 行 {"thinking": {"type": "enabled/disabled"}} 只 colspan 到 OpenAI 与 Anthropic，未打开 Using the Anthropic API。
