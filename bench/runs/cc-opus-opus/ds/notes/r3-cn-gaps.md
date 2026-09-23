# r3-cn-gaps
question: 补 3 家国内厂商的 4 个具体缺口/冲突格：Qwen 的推理内容回传规则与"思考模式是否只能流式"的冲突、MiniMax OpenAI 兼容层的 tool_choice 支持、DeepSeek 是否支持图片输入。
checked: https://help.aliyun.com/zh/model-studio/deep-thinking, https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope, https://platform.minimax.io/docs/api-reference/text-openai-api, https://platform.minimax.io/docs/guides/text-m3-function-call, https://platform.minimax.io/docs/api-reference/text-post, https://api-docs.deepseek.com/api/create-chat-completion, https://api-docs.deepseek.com/guides/anthropic_api

## claims
- [C1] QW preserve_thinking 决定模型是否读取历史 reasoning_content | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "多轮对话中，preserve_thinking 控制模型是否读取历史 assistant 消息中的 reasoning_content。设为 true 后，这些思考内容会拼接到下一轮输入。" | type: official
- [C2] QW preserve_thinking 默认 false，qwen3.8-max/flash 默认 true | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "默认值为false（qwen3.8-max/qwen3.8-flash 默认值为true）" | type: official
- [C3] QW preserve_thinking 限列出型号 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "目前支持qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash（默认开启）、qwen3.7-max" | type: official
- [C4] QW 开启时须完整回传历史 reasoning_content，不能拼进 content | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "必须将历史对话中所有的 reasoning_content 完整回传。不支持将 reasoning_content 拼接到 content 字段中回传。" | type: official
- [C5] QW 历史里缺 reasoning_content 也不报错 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "若历史消息中不包含 reasoning_content，开启此参数不会报错，正常兼容。" | type: official
- [C6] QW stream 参数：Qwen3 商业版思考模式只能流式 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope | quote: "Qwen3商业版（思考模式）、Qwen3开源版、QwQ、QVQ只支持流式输出。" | type: official
- [C7] QW FAQ：商业版也支持非流式 | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "商业版深度思考模型（如 qwen-plus、qwen3-max、qwen-flash 等）也支持非流式（同步）输出" | type: official
- [C8] QW FAQ：开源版只能流式 | src: https://help.aliyun.com/zh/model-studio/deep-thinking | quote: "部分模型（如 qwen3-235b-a22b、qwen3-32b 等开源版）仅支持流式输出，非流式调用会报错" | type: official
- [C9] MM 原生端点 POST /v1/text/chatcompletion_v2（非 OpenAI 层）：tool_choice 枚举 none/auto，默认 auto | src: https://platform.minimax.io/docs/api-reference/text-post | quote: "Controls how the model uses tools: none: never call tools auto: decide automatically (default)" | type: official
- [C10] DS /chat/completions 的 user content 接受图片 | src: https://api-docs.deepseek.com/api/create-chat-completion | quote: "Either a string, or an array of content parts (for image input)." | type: official
- [C11] DS Anthropic 兼容层 image 行：Supported | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "Supported. source.type can be base64 (media types: jpeg, png, gif, webp), url, or file" | type: official

## conflicts
- QW 非流式：C6 说 Qwen3 商业版思考模式只能流式，C7 说 qwen-plus/qwen3-max/qwen-flash 也支持非流式；开源版仅流式两页一致（C8）。两页都没抓到日期；C6 没点名型号，且和含 qwen3.8-max-0902 的 C3 同页。没有说明版本差异的原句，不裁决。

## gaps
- QW 工具调用时的回传规则：两页都没有原句；qwen-function-calling 没打开。
- QW preserve_thinking 关闭时，回传的 reasoning_content 是被忽略还是报错：没有明说。
- MM OpenAI 层 tool_choice、parallel_tool_calls：text-openai-api（tools 只写 "Function tool definitions."）和 M3 工具指南都没提。
- DS 支持图片的 model、页面日期：没查到。

## leads
- MiniMax POST /v1/responses：pplx 称 tool_choice 仅 auto/none，未核实；https://platform.minimax.io/docs/llms.txt
- https://api-docs.deepseek.com/guides/vision
- MiniMax M3 指南要求回传含 reasoning_details 的整个 response_message（MM D6）
