# LLM 时代 API 请求协议：从 Chat Completions 到 Responses、Messages 与 Gemini `generateContent`

LLM API 的主要差异，不在于“都能传一段 prompt、回一段文本”，而在于它们如何表达**对话历史、多模态内容、推理、工具调用、结构化输出、流式事件和会话状态**。实践中，OpenAI Chat Completions 已成为最广泛的兼容层；但它不是统一标准，更不是功能语义的完整交集。

如果只记住一句话：**不要把“OpenAI-compatible”理解成“OpenAI-equivalent”。**它通常意味着基础的请求路径、鉴权和 `messages → choices[0].message` 外壳相近；到了 tool calling、thinking/reasoning、多模态、JSON Schema、流式事件、上下文回传等能力，行为和字段往往显著分叉。DeepSeek 同时提供 OpenAI 与 Anthropic 兼容入口，但其 reasoning 回传规则就是一个典型例子：带工具的后续请求必须完整回传历史 `reasoning_content`，否则会收到 400 错误。[1][2]

***

## 1. 先建立分类法

理解 LLM 协议时，建议不要按“厂商 API 名称”死记，而是按下面六个层次拆解。任何一个模型接口都可以放进这个 taxonomy。

| 层次 | 要回答的问题 | 典型字段或对象 | 最常见的兼容性误区 |
|---|---|---|---|
| HTTP 外壳 | 请求发到哪里、怎么认证、如何流式传输？ | `POST /v1/chat/completions`、`Authorization`、SSE | 路径一样，不代表请求/响应对象完全一样 |
| 上下文模型 | 传入的是 `messages`、`contents`、`input`，还是服务端会话 ID？ | `messages[]`、`contents[]`、`input[]` | 将“整段历史由客户端回传”和“服务端保存会话”混为一谈 |
| 内容模型 | 一条消息是纯字符串，还是由多种 typed parts/blocks 组成？ | `content: "..."`、`content[]`、`parts[]` | 以为 `content` 永远是字符串 |
| 控制面 | 系统指令、采样参数、最大输出、停止条件、JSON 输出如何表达？ | `system`、`instructions`、`temperature`、`max_tokens` | 相同字段名不保证同样默认值、范围或优先级 |
| 执行面 | 工具、内置检索、代码执行、MCP、推理如何参与调用链？ | `tools`、`tool_calls`、`function_call`、`reasoning` | 把“模型请求调用工具”误当成“模型已执行工具” |
| 输出与事件 | 最终答案、工具调用、引用、拒答、token 使用量、流事件如何返回？ | `choices[]`、`output[]`、`candidates[]`、SSE event | 只解析文本字段，遗漏工具调用、拒答与终止原因 |

因此，所谓“协议适配”至少包含三件不同的工作：

1. **语法适配**：字段名、JSON 结构、HTTP 路径、SSE 格式相互转换。  
2. **语义适配**：同名参数的实际含义、默认值、约束与生命周期对齐。  
3. **能力降级或增强**：一个协议无法原样表达另一个协议的原生能力时，决定丢弃、模拟，还是保留扩展字段。

最危险的是只做第一层：JSON 能发出去、接口能返回 200，并不代表 Agent、工具循环、多轮推理或结构化输出真的正确。

***

## 2. 四个核心协议家族

截至目前，最值得建立直接认知的四个主流家族是：

1. OpenAI **Chat Completions**
2. OpenAI **Responses**
3. Anthropic **Messages**
4. Google Gemini **`generateContent`**

它们共同覆盖对话、多模态、工具和流式生成，但其“基本单位”完全不同。

| 协议家族 | 主端点/调用模型 | 输入的核心单位 | 输出的核心单位 | 协议设计中心 |
|---|---|---|---|---|
| OpenAI Chat Completions | `POST /v1/chat/completions` | `messages[]` | `choices[].message` | 一轮对话补全 |
| OpenAI Responses | `POST /v1/responses` | `input`，可为字符串或 typed `input` items | `output[]` typed items | 多步骤、工具、推理与多模态执行 |
| Anthropic Messages | `POST /v1/messages` | `messages[]`，每条含 typed `content` blocks | 单个 assistant `content[]` blocks | 内容块与显式工具循环 |
| Gemini `generateContent` | `models/{model}:generateContent` | `contents[]`，每条含 `parts[]` | `candidates[].content.parts[]` | 多模态 `Part` 组合与候选响应 |

OpenAI 官方将两代接口的核心区别总结为：Chat Completions 的输入和输出都是 **Messages**；Responses 则使用 `input` 和 `output` 的 **typed Items**。在 Responses 中，`message` 只是 item 的一种，`reasoning`、`function_call`、`function_call_output` 等也是一等对象。[3]

### 2.1 OpenAI Chat Completions：事实上的兼容层

Chat Completions 的典型请求如下：

```json
POST /v1/chat/completions

{
  "model": "example-model",
  "messages": [
    {
      "role": "system",
      "content": "你是一个严谨的技术助手。"
    },
    {
      "role": "user",
      "content": "解释 HTTP 流式响应。"
    }
  ],
  "temperature": 0.2,
  "stream": false
}
```

典型响应：

```json
{
  "id": "chatcmpl_xxx",
  "object": "chat.completion",
  "created": 0,
  "model": "example-model",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "HTTP 流式响应通常使用……"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```

这个模型的认知重点是：

- 上下文由客户端在每次请求时通过 `messages[]` 传入。
- 输出通常在 `choices[]` 中；多候选生成的抽象仍被保留。
- 核心成功路径是读取 `choices[0].message.content`。
- 工具调用通常挂在 assistant message 的 `tool_calls[]` 上。
- 这是目前开源推理服务、国内模型平台、聚合平台最爱声明“兼容”的协议。

OpenAI 对 Chat Completions 的定义仍是：根据一组构成对话的 messages 生成响应；其文档也建议新项目优先考虑 Responses，以使用其较新的平台能力。[4]

**它适合什么：**

- 已有 OpenAI SDK、LangChain、LiteLLM、各类 Agent 框架。
- 单轮或普通多轮聊天。
- 以文本/图像输入、函数调用、JSON 输出为主的可移植应用。
- 希望以最低接入成本切换供应商的场景。

**它不再天然适合什么：**

- 把推理步骤、工具调用结果、文件检索、代码解释器事件等视为原生对象并可靠保存。
- 需要精确表达复杂 agent trajectory。
- 希望减少“把厂商扩展字段偷偷塞进 assistant message”的协议债务。

***

### 2.2 OpenAI Responses：从“消息补全”转向“执行轨迹”

Responses API 不是简单把 Chat Completions 改名。它改变了程序的基本数据模型：你不再只处理“历史消息 + 下一条 assistant 消息”，而是处理一个**输入 items 与输出 items 的执行过程**。

一个概念化请求：

```json
POST /v1/responses

{
  "model": "example-model",
  "instructions": "你是一个严谨的技术助手。",
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "北京现在天气如何？"
        }
      ]
    }
  ],
  "tools": [
    {
      "type": "function",
      "name": "get_weather",
      "description": "查询某城市天气",
      "parameters": {
        "type": "object",
        "properties": {
          "city": { "type": "string" }
        },
        "required": ["city"]
      }
    }
  ]
}
```

概念化输出：

```json
{
  "id": "resp_xxx",
  "output": [
    {
      "type": "reasoning",
      "id": "rs_xxx"
    },
    {
      "type": "function_call",
      "call_id": "call_xxx",
      "name": "get_weather",
      "arguments": "{\"city\":\"北京\"}"
    }
  ]
}
```

工具执行后，应用应将工具结果作为新的 input item 回传，而不是“伪造一段 user 文本”：

```json
{
  "model": "example-model",
  "input": [
    {
      "type": "function_call_output",
      "call_id": "call_xxx",
      "output": "{\"temperature_c\": 21, \"condition\": \"晴\"}"
    }
  ]
}
```

Responses 的价值在于它让以下对象获得明确类型与生命周期：

- 用户/助手消息：`message`
- 推理相关对象：`reasoning`
- 工具请求：`function_call`
- 工具结果：`function_call_output`
- 不同模态的输入/输出 content part
- 内置工具产生的执行事件与结果

换言之，Chat Completions 更像“对话文本的下一步补全”，Responses 更像“模型驱动工作流的一次执行”。官方迁移材料明确指出，Chat Completions 用 `messages` 同时承载输入和输出；Responses 则以 `input` / `output` 的 typed Items 表达，且 `function_call`、`function_call_output` 与消息同属 item。[3]

**迁移时的重要误区：**

- 不要把 Responses 的 `output` 当成单一 assistant 文本；它可能先含 reasoning 或 function call。
- 不要假设 `output_text`、`message.content[0].text`、`choices[0].message.content` 三者可机械互换。
- 设计自己的持久化层时，应保留**原始 typed output**，而非只存最终可见文本。
- 如果适配供应商声称支持 Responses，仍应逐项验证：reasoning、内置工具、结构化输出、流事件、会话/前一响应关联是否为原生支持，还是做了 Chat Completions 反向封装。

***

### 2.3 Anthropic Messages：内容块优先，而非“一个 content 字符串”

Anthropic Messages API 的关键不是 `/v1/messages` 这个路径，而是它从设计上就将一条 message 的 `content` 视为**内容块数组**。纯字符串只是一个简写。

概念化请求：

```json
POST /v1/messages

{
  "model": "claude-example",
  "max_tokens": 1024,
  "system": "你是一个严谨的技术助手。",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "分析这张图片。"
        },
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": "..."
          }
        }
      ]
    }
  ]
}
```

概念化响应：

```json
{
  "id": "msg_xxx",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "图片中包含……"
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

Anthropic 文档体系中，每一条输入消息都有 `role` 与 `content`；`content` 可为字符串，或由不同类型的 content blocks 组成的数组，而字符串等价于单个 `text` block。[5][6]

它的结构特征如下：

- `system` 通常是顶层请求字段，不是对话 `messages[]` 内普通的一条 system message。
- 主对话角色的基本抽象集中于 `user` 和 `assistant`。
- 文本、图片、文档、工具调用、工具结果、thinking 等都可表示为 content block。
- 工具调用会出现在 assistant 的 `tool_use` block 中。
- 工具结果不是 OpenAI 风格的顶层 `role: "tool"` 消息，而常被作为后续 user message 内的 `tool_result` block 回传。
- 流式传输围绕“消息开始、内容块开始、内容块增量、内容块结束、消息增量、消息结束”组织。

工具调用的核心形态：

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_xxx",
      "name": "get_weather",
      "input": {
        "city": "北京"
      }
    }
  ]
}
```

应用执行工具后，继续发送：

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_xxx",
      "content": "北京：晴，21°C"
    }
  ]
}
```

Anthropic 的工具循环要求应用从 `tool_use` block 取得 `id`、`name` 和 `input`，执行本地工具后，以匹配的 `tool_result` 回传。其流式协议则依次发出 `message_start`、content block 相关事件、`message_delta` 和 `message_stop`。[6]

**为什么这会影响适配：**

把 Anthropic 转成 OpenAI Chat Completions 时，最容易丢失的是“一个 assistant turn 内多个异构 blocks 的顺序和边界”。例如模型可输出：

1. `thinking`；
2. `text`；
3. `tool_use`；
4. 后续继续输出 text 或另一个工具调用。

如果你的内部模型只保存 `assistant.content: string` 和 `assistant.tool_calls[]`，可能无法无损保存这些 block 的交错顺序，也很难保证重放时的语义一致。

***

### 2.4 Gemini `generateContent`：`Content` 与 `Part` 的多模态模型

Gemini 的经典 REST 调用以模型动作作为路径的一部分：

```text
POST /v1beta/models/{model}:generateContent
```

它的核心结构不是 `messages[]`，而是：

```text
contents[] -> Content -> parts[] -> Part
```

概念化请求：

```json
{
  "systemInstruction": {
    "parts": [
      {
        "text": "你是一个严谨的技术助手。"
      }
    ]
  },
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "描述这张图中的内容。"
        },
        {
          "inlineData": {
            "mimeType": "image/jpeg",
            "data": "..."
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.2
  }
}
```

概念化响应：

```json
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "这张图展示了……"
          }
        ]
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 0,
    "candidatesTokenCount": 0,
    "totalTokenCount": 0
  }
}
```

Gemini 的 `contents` 是多轮上下文；每个 `Content` 由 `role` 与有序 `parts[]` 组成。`Part` 可以承载 `text`、内联数据、文件数据、`functionCall`、`functionResponse`、thought 及 thought signature 等多种形式。[7]

关键差异包括：

- Gemini 常用 `role: "model"`，不是 `assistant`。
- 一条 content 的载荷是有序 `parts[]`，不是一个统一 `content` 字段。
- 多模态在 `Part` 层自然表达：`text`、`inlineData`、`fileData` 等并列。
- 函数调用与函数结果也以 `functionCall` / `functionResponse` 的 Part 形式存在。
- 一个响应可以有多个 `candidates[]`，最终需要选择其中一个 candidate。
- `systemInstruction` 与对话 `contents[]` 分开。
- 安全拒绝、候选状态和用量元数据通常在 response 的不同层中表达，不能只盯住 `candidates[0].content.parts[0].text`。

Google 的 `GenerateContentResponse` 可包含多个候选响应，且 API 定义了 `PromptFeedback`、阻断原因、usage metadata 等对象；流式调用会返回一串 `GenerateContentResponse` 实例。[8]

***

## 3. 四种协议逐维度对比

### 3.1 上下文、角色与消息结构

| 维度 | OpenAI Chat Completions | OpenAI Responses | Anthropic Messages | Gemini `generateContent` |
|---|---|---|---|---|
| 输入容器 | `messages[]` | `input`，字符串或 items | `messages[]` | `contents[]` |
| 基础上下文单位 | Message | Typed Item | Message + Content Block | Content + Part |
| 常见角色 | `system`、`developer`、`user`、`assistant`、`tool` | message item 中的 `developer`、`system`、`user`、`assistant` 等 | 主要为 `user`、`assistant`；系统指令顶层表达 | 常见为 `user`、`model` |
| 系统指令 | 常见为 `system` / `developer` message | `instructions` 或 input message | 顶层 `system` | `systemInstruction` |
| 纯文本简写 | 多数场景 `content: "text"` | `input: "text"` 或 content part | `content: "text"` | `parts: [{"text": "..."}]` |
| 多模态结构 | `content` 可为 parts 数组 | typed input/output content parts | typed content blocks | typed `Part` |
| 服务器会话 | 传统模式多由客户端回传历史 | 可使用 response/会话相关能力，具体依赖接口能力 | 通常客户端回传历史 | 通常客户端回传 `contents[]` 历史 |

一个实用判断法：

- 如果 API 的核心对象是 **message**，优先考虑“谁说了什么”；
- 如果核心对象是 **item**，优先考虑“系统发生了什么步骤”；
- 如果核心对象是 **block / part**，优先考虑“这一轮中包含哪些有序的异构内容”。

### 3.2 工具调用：最容易“看起来兼容、实际不兼容”的部分

所有主流协议都支持某种函数/工具调用，但工具循环的“消息归属、关联 ID、参数编码、结果回传位置、并行调用方式”并不一致。

| 协议 | 模型请求工具的位置 | 参数形态 | 工具结果如何回传 | 关联 ID |
|---|---|---|---|---|
| Chat Completions | assistant `tool_calls[]` | 通常 `function.arguments` 为 JSON 字符串 | `role: "tool"` message | `tool_call_id` |
| Responses | `output[]` 中 `function_call` item | 常见为 `arguments` 字符串 | `function_call_output` input item | `call_id` |
| Anthropic Messages | assistant `content[]` 中 `tool_use` block | `input` 为 JSON 对象 | user `content[]` 中 `tool_result` block | `tool_use_id` |
| Gemini | response `parts[]` 中 `functionCall` | `args` 为结构化对象 | 后续 `parts[]` 中 `functionResponse` | 通常依函数调用/响应关系处理，具体字段依实现版本 |

**不要把工具调用当成模型执行工具。**模型只是在输出一个“建议调用 X，参数是 Y”的结构。你的应用仍需：

1. 解析模型请求的所有工具调用；
2. 校验工具名、权限和参数；
3. 执行外部系统操作；
4. 将成功结果或错误结果以正确协议形态回传；
5. 继续请求模型，直到得到最终答案或达到循环上限。

以 Cohere 的 V2 Chat 为例，其工具循环也是典型的“模型先生成 `tool_calls`，应用执行，再把带 `tool_call_id` 的 tool message 回传，最后得到基于工具结果的响应”的模式。 这说明工具调用的基本控制流具有行业共性，但 JSON 外壳不应被视为标准。[9]

### 3.3 推理/Thinking：字段存在不代表可随意保存或回传

推理模型带来的最大协议变化，是模型输出除了最终可见答案外，还可能包含 reasoning/thinking 相关数据。不同平台对其可见性和回传规则差别很大。

| 形态 | 典型表达 | 是否应视作普通文本 | 后续轮次是否应回传 |
|---|---|---|---|
| OpenAI Responses 风格 | 独立 `reasoning` item | 否，应保留类型与顺序 | 依平台与工作流机制处理 |
| DeepSeek Chat 风格 | assistant message 的 `reasoning_content` | 否，独立于 `content` | 带 `tools` 时必须完整回传 |
| Anthropic 风格 | `thinking` content block | 否，属于 typed block | 按官方模型与工具规则处理 |
| Qwen/OpenAI-compatible 风格 | `reasoning_content` 扩展字段 | 否 | 可由参数决定保留或忽略 |

DeepSeek 的 thinking mode 在 assistant message 中将 `reasoning_content` 与最终 `content` 并列；没有工具时，历史 reasoning 不必回传，回传也可能被忽略；但请求携带 `tools` 时，历史所有 assistant turns 的 `reasoning_content` 都必须原样回传，否则 API 返回 400。[2]

Qwen 的 OpenAI-compatible Chat 文档也表明，thinking 内容可以放在 `reasoning_content` 中，并通过类似 `clear_thinking` / preserve-thinking 的控制决定历史 reasoning 是否作为后续上下文；若需要保留，历史内容必须完整、未修改、顺序不变。[10][11]

因此，应用应区分至少三类数据：

- **展示给终端用户的答案**：最终可见文本或富内容。
- **发送回模型的上下文材料**：可能含隐藏 reasoning、工具调用、工具结果、签名。
- **可审计的运行轨迹**：需要按权限、保留期与安全政策单独处理。

不要为了“节省 token”或“数据库结构简单”盲目剥离 reasoning 字段；也不要默认将所有推理文本展示给用户。正确做法是按具体供应商、模型和请求模式实现**协议级的 round-trip preservation**。

### 3.4 流式响应：不要只拼 `delta.content`

流式输出通常使用 Server-Sent Events（SSE），但 SSE 只是传输包装；不同协议对事件类型、事件顺序和完成标志的定义差异很大。

| 协议 | 常见流式认知模型 | 典型增量内容 | 最终完成标记 |
|---|---|---|---|
| Chat Completions | 一串 completion chunks | `choices[].delta.content`、`tool_calls` 增量 | `finish_reason`，常见 `[DONE]` 结束 |
| Responses | 具名 response events | output item/part 的 added、delta、done | response completed/failed 等事件 |
| Anthropic | block 生命周期事件流 | `content_block_delta` | `message_stop` |
| Gemini | 多个 response 实例或流式候选更新 | candidate/content/part 更新 | 候选结束原因、流结束 |

Anthropic 的流事件有非常明确的生命周期：`message_start` 后是一个或多个 `content_block_start`、对应的 `content_block_delta`、`content_block_stop`；随后有 `message_delta`，最终为 `message_stop`。[6]

对于工具调用，不能只把所有 delta 当成普通字符串拼接：

- 工具参数 JSON 可能跨多个 chunk 才完整。
- 先出现工具名/调用 ID，后续才逐渐出现参数字符串。
- 单个响应可能并行产生多个工具调用。
- 文本和工具调用、reasoning 或引用事件可能交错。
- 最终 token usage 或 finish reason 往往只在末尾出现。

**推荐实现方式：**

- 用 `(response_id, choice/index, content_block/index, tool_call/index)` 等稳定标识组织状态。
- 为每个 tool call 单独累积参数字符串。
- 只在收到完整事件或终止事件后 JSON parse 工具参数。
- 将“可显示文本”、“模型动作”、“运行元数据”分别累积。
- 网络中断时区分：连接断开、模型完成、内容被安全阻断、工具调用未完成、服务端错误。

***

## 4. DeepSeek、智谱与下游适配的真实差异

### 4.1 “OpenAI-compatible”的三个层级

一个厂商写“兼容 OpenAI API”时，至少可能指以下三种不同承诺：

| 兼容层级 | 通常意味着什么 | 不能据此推断什么 |
|---|---|---|
| SDK/连接兼容 | 可以复用 OpenAI SDK，替换 `base_url`、API key 和模型名 | 所有 OpenAI 参数都有效 |
| Chat schema 兼容 | 接受 `model`、`messages`、`tools` 等常见字段，返回 `choices[].message` | 字段默认值、角色支持、工具流程和流式事件一致 |
| 功能语义兼容 | 特定功能的行为和边界也可互换 | 这需要逐项测试，几乎不能只靠营销语判断 |

DeepSeek 官方说明其 API 可以通过不同配置以 OpenAI/Anthropic 格式访问，并提供了 Anthropic 兼容 base URL。 但 DeepSeek 又为 thinking mode 定义了专用 `reasoning_content` 字段及特殊的工具多轮回传要求。 这正好说明：**外层兼容不等于完整的状态机兼容。**[1][2][12]

### 4.2 DeepSeek：外壳兼容，推理与工具状态有专有约束

DeepSeek Chat Completions 的核心响应仍然是熟悉的 OpenAI 形态：

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "最终答案",
        "reasoning_content": "推理内容",
        "tool_calls": []
      }
    }
  ]
}
```

需要特别注意：

- `reasoning_content` 是 DeepSeek thinking mode 的专用扩展，和最终 `content` 并列。[12]
- 工具调用中，流的首个 tool-call chunk 承载 `id`、`type`、`function` 等字段，后续 chunk 可能只补充函数参数。[12]
- 只要请求携带 `tools`，多轮对话必须把所有历史 `reasoning_content` 原样带回。[2]
- DeepSeek 也开始提供 Responses API 形态；其文档明确声明此 API 是无状态的，responses/conversations 不存储在服务端，仍需自行管理上下文。[13]

**适配建议：**

- 内部 canonical model 不要只定义 `AssistantMessage { content, tool_calls }`；至少加入 `reasoning` 或不透明的 `provider_state`。
- 对 DeepSeek 建立“带工具”和“不带工具”两种上下文序列化策略。
- 不能在工具循环中把历史 assistant message 重新格式化、删字段、重排字段后再回传。
- 流式解析应逐个 tool call 聚合，而不是将所有 `function.arguments` 混拼。

### 4.3 智谱 / Z.AI GLM：基础 Chat Completions 接近，但不应假设 Anthropic 语义

Z.AI 的 Chat Completion 文档采用了熟悉的 `messages[]` 结构，支持 system、user、assistant、tool 等消息类型；当出现 `tool_calls` 时，`content` 通常为空。 这意味着它在应用接入层可以较自然地接入 OpenAI Chat Completions 风格的工具循环。[14]

概念化的 GLM/OpenAI-compatible message：

```json
{
  "role": "assistant",
  "content": "",
  "tool_calls": [
    {
      "id": "call_xxx",
      "type": "function",
      "function": {
        "name": "search_docs",
        "arguments": "{\"query\":\"LLM API protocol\"}"
      }
    }
  ]
}
```

这与 Anthropic 的相同意图并不是同一种表达：

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_xxx",
      "name": "search_docs",
      "input": {
        "query": "LLM API protocol"
      }
    }
  ]
}
```

两者的关键不同：

| 问题 | 智谱/GLM 常见 Chat 格式 | Anthropic Messages |
|---|---|---|
| 工具调用放在哪里 | `assistant.tool_calls[]` | `assistant.content[]` 的 `tool_use` block |
| 工具参数 | 常为 JSON 字符串 `arguments` | 原生 JSON 对象 `input` |
| 工具结果 | `role: "tool"` message | user message 中 `tool_result` block |
| 文本与工具交错 | 通常以 message 字段组合 | 可以在内容块序列中严格排序 |
| 系统提示 | 常见 `role: "system"` message | 顶层 `system` 参数 |
| 思维/推理 | 需看具体模型和版本扩展 | thinking block 具有独立类型 |

因此，如果你从 GLM/OpenAI-compatible 迁移到 Anthropic，不能只做字段重命名：

- `tool_calls[].function.arguments` 需要 JSON parse 成对象，成为 `tool_use.input`。
- `tool` role 的结果消息要改写为包含 `tool_result` blocks 的 user message。
- 顶层 system prompt 需要从消息数组抽取。
- 需要避免让不合法的 assistant/user 轮次顺序进入 Anthropic 格式。
- 多模态内容要从 OpenAI-style parts 映射为 Anthropic blocks，而非假定同一 `type` 词汇可直传。

Z.AI 还提供 MCP server calling 能力，文档称其可在 `chat/completions` 中直接连接并调用 MCP servers；这属于在 OpenAI 风格外壳下叠加的**厂商专有执行能力**，不应被当作通用 OpenAI `tools` 的等价物。[15]

### 4.4 Qwen、Mistral、Cohere：三种常见“兼容但不同”的模式

#### Qwen：OpenAI 兼容外壳 + reasoning 扩展

阿里云 Model Studio 支持以 OpenAI-compatible Chat API 调用模型，但它明确说明兼容接口仍有参数、功能和行为差异；其 Responses 文档也直接强调“compatible with OpenAI to reduce migration cost, but differs in parameters, functionality, and behavior”。[16]

Qwen/Model Studio 常见差异：

- assistant response 可能增加 `reasoning_content`。[10]
- 历史 thinking 是否进入下轮上下文可由专有参数控制。
- 视觉模型可使用 OpenAI 风格 content array，但模型/能力组合有自己的限制。[17]
- 同一平台可能同时提供 DashScope 原生 SDK、OpenAI-compatible Chat 与 OpenAI-compatible Responses，能力覆盖并不完全相同。[18]

#### Mistral：Chat Completions 兼容，但 content 可为异构事件数组

Mistral Chat Completion 以 `messages[]` 为输入、assistant message 为输出，角色包括 system、user、assistant、tool。 但其输出 `content` 既可以是字符串，也可以是由不同类型 chunk 构成的列表；引用和工具调用等事件可以和文本交错。[19]

这意味着下游若强制写成：

```ts
const text = response.choices[0].message.content as string;
```

会在部分功能中失效。更稳健的内部模型应将 content 视为：

```ts
type Content =
  | { kind: "text"; text: string }
  | { kind: "image"; /* ... */ }
  | { kind: "citation"; /* ... */ }
  | { kind: "tool_call"; /* ... */ }
  | { kind: "provider_extension"; raw: unknown };
```

#### Cohere：原生 V2 Chat 是消息驱动，但兼容层另算

Cohere V2 Chat 也使用 `messages[]`，并支持 `user`、`assistant`、`tool`、`system` 角色；响应包含生成的 `message`、`id`、`finish_reason` 与 `meta`。 它支持 `tool_calls` 和可选的 tool choice 控制。[20][21]

不过 Cohere 同时也有 OpenAI SDK Compatibility API。 这应被理解为**第二个入口/翻译层**，而不是其原生 V2 API 的精确复制。工程上要明确：你究竟在适配 Cohere 原生 V2，还是通过 OpenAI compatibility endpoint 调 Cohere；二者可用参数和输出细节可能不同。[22]

***

## 5. 一个统一内部协议应如何设计

如果你的产品需要支持多个供应商，最好的策略通常不是将所有东西强行存成 OpenAI Chat Completions，也不是让业务层直接面对每个厂商 SDK，而是定义一个**能保留语义的内部 canonical protocol**。

### 5.1 推荐的最小内部数据模型

```ts
type Role =
  | "developer"
  | "system"
  | "user"
  | "assistant"
  | "tool"
  | "model";

type ContentPart =
  | {
      type: "text";
      text: string;
    }
  | {
      type: "image";
      source: {
        kind: "url" | "base64" | "file_id";
        mimeType?: string;
        value: string;
      };
    }
  | {
      type: "document";
      source: unknown;
    }
  | {
      type: "tool_call";
      callId: string;
      name: string;
      argumentsJson: string;
      rawArguments?: unknown;
    }
  | {
      type: "tool_result";
      callId: string;
      content: ContentPart[];
      isError?: boolean;
    }
  | {
      type: "reasoning";
      text?: string;
      opaqueState?: unknown;
      visibility: "hidden" | "provider_controlled" | "displayable";
    }
  | {
      type: "citation";
      data: unknown;
    }
  | {
      type: "provider_extension";
      provider: string;
      raw: unknown;
    };

type Turn = {
  id?: string;
  role: Role;
  parts: ContentPart[];
  providerMetadata?: Record<string, unknown>;
};

type GenerationRequest = {
  model: string;
  instructions?: ContentPart[];
  turns: Turn[];
  tools?: ToolDefinition[];
  toolChoice?: "auto" | "none" | "required" | { name: string };
  outputSchema?: unknown;
  generation?: {
    temperature?: number;
    topP?: number;
    maxOutputTokens?: number;
    stopSequences?: string[];
  };
  providerOptions?: Record<string, unknown>;
};

type GenerationResult = {
  id?: string;
  output: Turn[];
  finishReason?: string;
  usage?: {
    inputTokens?: number;
    outputTokens?: number;
    totalTokens?: number;
    cachedInputTokens?: number;
  };
  raw?: unknown;
};
```

这套模型的重点不是“字段多”，而是避免过早丢失不可逆信息：

- `parts[]` 而不是 `content: string`；
- 工具调用与工具结果均为显式 typed parts；
- `reasoning` 与最终 answer 分离；
- `provider_extension` 是受控的逃生口，而不是把未知字段静默丢弃；
- 保存 `raw` 以便调试、审计和未来协议升级；
- 内部 `Role` 容忍 `model` 与 `assistant` 的差异，但在 provider adapter 中再做转换。

### 5.2 适配器职责

建议将每个供应商实现成双向 adapter：

```text
业务 / Agent Runtime
        ↓
Canonical Request
        ↓
Provider Request Adapter
        ↓
OpenAI / Anthropic / Gemini / DeepSeek / GLM API
        ↓
Provider Response Adapter
        ↓
Canonical Result + Raw Provider Payload
        ↓
业务 / UI / 持久化 / 观测
```

每个 adapter 都要明确处理：

1. **角色映射**  
   `assistant ↔ model`、顶层 system ↔ system message、developer 是否支持。

2. **内容映射**  
   文本、图片、文件、音频、视频、URL、base64、file ID 的映射，以及不支持时的明确失败或降级策略。

3. **工具映射**  
   JSON Schema 方言、`arguments` string/object 差异、工具结果所在位置、多个并行调用、工具错误表示。

4. **推理映射**  
   是否保留、是否回传、是否可展示、是否需要签名或 opaque state、是否会影响 token/cost。

5. **结构化输出映射**  
   `json_object` 与 `json_schema` 的支持范围、schema 严格性、工具调用和 JSON 输出是否可同时启用。

6. **流式映射**  
   将 provider SSE 转成内部事件，例如 `text_delta`、`reasoning_delta`、`tool_call_delta`、`usage`、`completed`、`error`。

7. **错误映射**  
   HTTP 400/401/429/5xx、内容审核拦截、上下文长度、schema 无效、工具参数无法解析、模型拒答。

### 5.3 不要做“最低公分母”适配

很多团队为了多模型切换，最后只保留：

```json
{
  "messages": [
    { "role": "user", "content": "..." }
  ]
}
```

这可以完成 demo，却会使高级能力无处安放。更好的策略是把能力分为三档：

| 档位 | 策略 | 示例 |
|---|---|---|
| 可移植核心 | 在所有供应商上稳定支持 | 文本、多轮历史、基本温度参数、单个函数调用 |
| 规范化扩展 | 内部有统一表达，但允许不同实现质量 | 多模态 parts、并行工具调用、JSON Schema、reasoning |
| Provider 原生能力 | 显式挂在 `providerOptions` 或 extension 上 | Anthropic prompt caching、Gemini thought signature、Mistral 内置工具、GLM MCP 调用 |

这样既能实现跨厂商的基本可替换性，也不会为了“统一”而牺牲高级能力。

***

## 6. 实战检查清单

在选择、替换或适配一个 LLM API 前，应至少验证以下问题，而不是只看“支持 OpenAI SDK”。

### 请求与消息

- 该接口要求的真实路径、API 版本、认证 header 是什么？
- 请求是无状态的吗？是否需要每一轮完整回传历史？
- 系统提示放在 `system` message、`developer` message、顶层字段，还是 `instructions`？
- 支持哪些角色？`developer`、`tool`、`model` 是否有效？
- assistant 历史消息能否回传？是否支持 assistant prefix/prefill？
- `content` 是 string、array，还是必须为 blocks/parts？
- 多模态内容用 URL、base64、file ID、上传 API 还是 provider-hosted file reference？

### 生成控制与结构化输出

- `max_tokens`、`max_output_tokens`、`max_completion_tokens` 的含义是否一致？
- `temperature`、`top_p`、`seed`、stop sequences 的范围、默认值和模型支持情况是什么？
- JSON mode 只保证“合法 JSON”，还是保证满足 JSON Schema？
- JSON Schema 是否支持 strict mode？不支持的 JSON Schema 关键字怎样处理？
- 当输出受 schema 约束时，工具调用是否仍可用？
- 是否有模型特定的 reasoning effort、thinking budget 或深度推理开关？

Mistral 的文档就区分 `json_object` 与 `json_schema`：前者保证 JSON，后者保证符合你提供的 schema，并且 JSON mode 时仍需要在提示中要求模型输出 JSON。[23]

### 工具与 Agent 循环

- tools 的定义是否采用 JSON Schema？schema 支持到什么程度？
- 模型是返回 JSON 字符串参数，还是 JSON 对象？
- 一轮能否返回多个/并行 tool calls？
- 工具结果在 `tool` role、`tool_result` block，还是专门 output item 中回传？
- tool result 是否允许富内容、图片、文档、结构化 JSON 或错误标记？
- 需要保留哪些 ID：`tool_call_id`、`tool_use_id`、`call_id`？
- 工具调用期间是否必须完整回传 hidden reasoning？
- 是否有内置工具、远程 MCP、代码执行、搜索等与用户定义 function tools 不同的生命周期？

### 流式与可靠性

- SSE 的终止标志是什么？`[DONE]`、`message_stop`、response completed event，还是连接关闭？
- 文本、reasoning、工具参数、引用是否各有独立 delta？
- 是否会在末尾才返回 usage？中途断线时如何处理计费与重试？
- 同一个 request 是否可安全重试？是否支持 idempotency key？
- 流式工具调用的参数何时才保证是合法 JSON？
- 是否应将原始 SSE events 持久化用于复盘和故障恢复？

### 成本、隐私与安全

- 输入、缓存输入、输出、reasoning、工具调用、音视频是否分别计费？
- 供应商是否保存 prompt、response 或 conversations？
- 历史 reasoning 是否会显著增加上下文 token 与成本？
- 是否需要在日志中脱敏 API key、个人数据、工具返回数据和内部 reasoning？
- 用户是否能诱导模型调用敏感工具？工具层是否独立做鉴权和参数验证？
- 是否需要区分“模型拒答”“内容被安全拦截”“工具失败”“网络失败”？

***

## 7. 推荐的决策原则

**如果你只需要多供应商文本聊天：**  
优先以 OpenAI Chat Completions 作为接入层，但将响应解析写成可容忍扩展字段的代码；不要只假设 `content` 是非空字符串。

**如果你做的是 Agent、代码助手、检索/浏览/执行工作流：**  
优先采用 item/block/part 级别的内部状态模型。Responses、Anthropic Messages 和 Gemini 的设计都表明，未来重点不只是“下一句文本”，而是“模型生成并协调多种执行对象”。[3][6][7]

**如果你要支持 reasoning 模型：**  
将 reasoning 定义为独立、权限受控、供应商特定的状态。不要把它和最终回答拼接，也不要未经验证地删除或修改后回传。

**如果供应商宣称兼容 OpenAI：**  
建立一份 capability matrix，逐项跑集成测试：文本、多轮、system/developer、图像、JSON Schema、单/并行工具调用、工具结果、多轮 thinking、SSE、usage、错误码、上下文上限。不要用一次“Hello world 返回 200”判定兼容性。

**如果你需要从 Anthropic 迁到 OpenAI-style，或反向迁移：**  
把迁移当作**对话状态机转换**，而不是字段 rename。尤其要处理：top-level system、block/part 序列、工具参数的 string/object 转换、工具结果位置、thinking 生命周期与流事件模型。

***

## 结论

LLM API 正在从单纯的“prompt → text completion”演化为多模态、工具驱动、可流式执行的应用协议。Chat Completions 仍是最重要的互操作基线；Responses 代表 item/执行轨迹导向的方向；Anthropic 强调有序 content blocks；Gemini 将多模态 `Part` 放在核心位置。

真正稳健的工程方案不是押注某一种 JSON 外壳，而是：

1. 用自己的 canonical typed content model 保存对话与执行状态；  
2. 将每个供应商协议实现为可测试的双向 adapter；  
3. 把 reasoning、tool calls、tool results、citations、stream events 当成一等数据；  
4. 对“OpenAI-compatible”逐项验证语义，而非仅验证请求能否发出；  
5. 在可移植性与原生能力之间显式选择，而不是让能力在静默转换中丢失。

## Citations

1. [DeepSeek API Docs: Your First API Call](https://api-docs.deepseek.com/)
2. [Thinking Mode - DeepSeek API Docs](https://api-docs.deepseek.com/guides/thinking_mode/)
3. [Migrate to the Responses API - OpenAI Developers](https://developers.openai.com/api/docs/guides/migrate-to-responses)
4. [Chat Completions Overview | OpenAI API Reference](https://developers.openai.com/api/reference/chat-completions/overview)
5. [Anthropic Claude Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html)
6. [API usage primer for Claude - Claude Platform Docs](https://platform.claude.com/docs/en/claude_api_primer)
7. [Generate content with the Gemini API - Google Cloud Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/inference)
8. [Generating content | Gemini API - Google AI for Developers](https://ai.google.dev/api/generate-content)
9. [Basic usage of tool use (function calling) - Cohere Documentation](https://docs.cohere.com/docs/tool-use-overview)
10. [Alibaba Cloud Model Studio:OpenAI compatible - Chat](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions)
11. [OpenAI chat - QwenCloud](https://docs.qwencloud.com/api-reference/chat/openai-chat)
12. [Chat Completions API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-chat-completion/)
13. [Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-response/)
14. [Chat Completion - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/api-reference/llm/chat-completion)
15. [MCP Calling - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/guides/capabilities/mcp-call)
16. [Create a response - Alibaba Cloud Model Studio](https://docs.modelstudio.console.alibabacloud.com/en/model-studio/qwen-api-via-openai-responses)
17. [Call Qwen VL models through the OpenAI interface](https://www.alibabacloud.com/help/en/model-studio/qwen-vl-compatible-with-openai)
18. [Make your first API call to Qwen - Alibaba Cloud Model Studio](https://www.alibabacloud.com/help/en/model-studio/first-api-call-to-qwen)
19. [Chat completions | Mistral Docs](https://docs.mistral.ai/studio/conversations/chat-completion)
20. [Using the Cohere Chat API for Text Generation](https://docs.cohere.com/docs/chat-api)
21. [Chat - Cohere Documentation](https://docs.cohere.com/reference/chat)
22. [Using Cohere models via the OpenAI SDK](https://docs.cohere.com/docs/compatibility-api)
23. [Chat Endpoints - Mistral AI Documentation](https://docs.mistral.ai/api/endpoint/chat)
24. [Completions | OpenAI API Reference](https://developers.openai.com/api/reference/python/resources/chat/subresources/completions)
25. [Gemini API reference | Google AI for Developers](https://ai.google.dev/api)
26. [Chat Completions | OpenAI API Reference](https://platform.openai.com/docs/api-reference/chat)
27. [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use)
28. [Native API (/messages) | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/compute/aig/chat-completion/anthropic-claude/anthropic-claude-message)
29. [Text generation | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/text-generation)
30. [Completions | OpenAI API Reference](https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions)
31. [Create a Message - Fireworks AI Docs](https://docs.fireworks.ai/api-reference/anthropic-messages)
32. [Gemini Interactions API - Google AI for Developers](https://ai.google.dev/api/interactions-api)
33. [Chat Completions Guide - OpenAI Platform](https://platform.openai.com/docs/guides/chat-completions)
34. [vllm.entrypoints.anthropic.protocol](https://docs.vllm.ai/en/stable/api/vllm/entrypoints/anthropic/protocol/)
35. [Getting started - generateContent API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/get-started)
36. [OpenAI Platform](https://platform.openai.com/docs/guides/text-generation/chat-completions-response-format)
37. [Anthropic Messages - Introduction to Langdock - Docs](https://docs.langdock.com/en/developer/completion-api/anthropic)
38. [Native API (/chat/completions) | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/ai/aig/chat-completion/zai-glm/zai-glm-chat-completion)
39. [Language Model API Overview - Tencent Cloud](https://www.tencentcloud.com/document/product/1300/80632)
40. [Tool Calls | DeepSeek API Docs](https://api-docs.deepseek.com/guides/tool_calls/)
41. [Z.AI (Zhipu AI) - LiteLLM](https://docs.litellm.ai/docs/providers/zai)
42. [Introducing DeepSeek-V3](https://api-docs.deepseek.com/news/news1226)
43. [GLM-4.5: Reasoning, Coding, and Agentic Abililties - Z.ai](https://z.ai/blog/glm-4.5)
44. [DeepSeek API Upgrade](https://api-docs.deepseek.com/news/news0725/)
45. [thinking_mode_api_example_to...](https://api-docs.deepseek.com/api_samples/thinking_mode_api_example_tool_call/)
46. [Z.ai API Platform — Start building with GLM-5.3](https://z.ai/model-api)
47. [Change Log | DeepSeek API Docs](https://api-docs.deepseek.com/updates/)
48. [Top-Level Request...](https://api-docs.deepseek.com/guides/responses_api/)
49. [Chat Completions API](https://api-docs.deepseek.com/api/create-chat-completion)
50. [glm-5.3 (Zhipu AI) · Cloudflare AI docs · Cloudflare Workers ...](https://developers.cloudflare.com/workers-ai/models/glm-5.3/)
51. [HTTP API 调用- 智谱AI开放文档](https://docs.bigmodel.cn/cn/guide/develop/http/introduction)
52. [model-parameters-mistral-chat-completion.md](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-mistral-chat-completion.md)
53. [Function Calling | Mistral Docs](https://docs.mistral.ai/studio/conversations/function-calling)
54. [Introducing updated APIs - Cohere](https://cohere.com/blog/new-api-v2)
55. [Using Connectors in Chat Completions - Mistral AI Cookbook](https://docs.mistral.ai/resources/cookbooks/mistral-connectors-05-connectors-in-completions)
56. [Alibaba Cloud Model Studio:Deep thinking](https://www.alibabacloud.com/help/en/model-studio/deep-thinking)
57. [Chat - Mistral](https://docs.mistral.ai/api)
58. [Usage patterns for tool use (function calling) - Cohere Documentation](https://docs.cohere.com/docs/tool-use-usage-patterns)
59. [Deprecated Agents Endpoints - Mistral AI Documentation](https://docs.mistral.ai/api/endpoint/deprecated/agents)
60. [Chat with Streaming](https://docs.cohere.com/reference/chat-stream)
61. [OpenAI Integration](https://learn.microsoft.com/en-us/agent-framework/hosting/self-hosting/openai-endpoints)
62. [OpenAI Chat Completions Protocol Field Descriptions - Tencent Cloud](https://intl.cloud.tencent.com/document/product/1300/82345)
63. [Chat Completions API | openai/openai-python | DeepWiki](https://deepwiki.com/openai/openai-python/4.1-chat-completions-api)
64. [Responses API Reference | openai/completions-responses ...](https://deepwiki.com/openai/completions-responses-migration-pack/6-responses-api-reference)
65. [OpenAI Responses API Tutorial: 14 Python Examples | TECHSY](https://techsy.io/en/blog/openai-responses-api-tutorial)
66. [OpenAI Responses API Tutorial 2026: Build Stateful AI Apps in ...](https://baeseokjae.github.io/posts/openai-responses-api-tutorial-2026/)
67. [OpenAI API Python Tutorial — Chat Completions, Streaming ...](https://machinelearningplus.com/gen-ai/openai-api-python-tutorial/)
68. ["Responses" API endpoint - reference documentation ...](https://community.openai.com/t/responses-api-endpoint-reference-documentation-errors-and-issues/1140994)
69. [CLASP/docs/api-reference/anthropic-messages.md at main - GitHub](https://github.com/jedarden/CLASP/blob/main/docs/api-reference/anthropic-messages.md)
70. [Anthropic · Messages - LM-Kit One API](https://docs.lm-kit.com/lm-kit-one/api/anthropic-messages.html)
71. [Create a message - OpenRouter | Documentation](https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-a-message)
72. [Anthropic | AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/anthropic)
73. [Anthropic Messages (Claude Code) · Docs · Surplus Intelligence](https://www.surplusintelligence.ai/docs/api-reference/messages)
74. [Anthropic Messages Format | FastRouter.AI Docs](https://docs.fastrouter.ai/api-reference/anthropic-messages-format)
75. [Section 2 — Agentic Loops & stop_reason Handling](https://ccaf-exam.guide/docs/02-agentic-loops/)
76. [Create a Message](https://zenmux.ai/docs/api/anthropic/create-messages.html)
77. [Gemini thinking - generateContent API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/thinking)
78. [Image understanding - generateContent API](https://ai.google.dev/gemini-api/docs/generate-content/image-understanding)
79. [Google Gen AI SDK documentation](https://googleapis.github.io/python-genai/)
80. [Class GenerateContentResponse](https://googleapis.github.io/js-genai/release_docs/classes/types.GenerateContentResponse.html)
81. [[Bug]: Google AI generateContent endpoints require a different ...](https://github.com/BerriAI/litellm/issues/12671)
82. [Google Gemini Generate Content Schema - APIs.io](https://apis.io/schemas/google-gemini/google-gemini-generate-content/)
83. [HTTP Request to Gemini API fails with "contents is not specified ...](https://community.n8n.io/t/http-request-to-gemini-api-fails-with-contents-is-not-specified-despite-correct-configuration/208657?tl=en)
84. [Gemini Native Format: Streaming & Non-Streaming Responses](https://docs.apiyi.com/en/api-capabilities/gemini/response-handling)
85. [Gemini generateContent and streaming via Anyone](https://docs.anyone.ai/api-reference/gemini-chat)
86. [Reasoning Model (deepseek-reasoner)](https://api-docs.deepseek.com/guides/reasoning_model)
87. [deepseek-reasoning-chat.md - new-api-docs - GitHub](https://github.com/QuantumNous/new-api-docs/blob/main/docs/en/api/deepseek-reasoning-chat.md)
88. [DeepSeek-V4-Flash Now Supports the Responses API and Codex](https://apidog.com/blog/deepseek-v4-flash-responses-api-codex/)
89. [Explore DeepSeek API - Chat Completion and more - SerpApi](https://serpapi.com/blog/explore-deepseek-api/)
90. [Deepseek Reasoner V3.1 Terminus - AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/deepseek/deepseek-reasoner-v3.1-terminus)
91. [DeepSeek API Docs 2026 — Quickstart & Examples](https://deepseek.ai/docs)
92. [Quick Start](https://docs.z.ai/guides/overview/quick-start)
93. [GLM API Guide - Tencent Cloud](https://intl.cloud.tencent.com/document/product/1300/80634)
94. [Z.AI GLM Models Support · olimorris codecompanion.nvim - GitHub](https://github.com/olimorris/codecompanion.nvim/discussions/2850)
95. [Glm 5.2 - AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/zhipu/glm-5.2)
96. [ZhipuAI API - 智谱AI](https://open.bigmodel.cn/dev/api)
97. [GLM API - Access Zhipu AI glm-5, glm-5.1, and glm-5.2 via AIsa](https://aisa.one/docs/guides/chinese-llms/glm)
98. [Glm 5](https://docs.aimlapi.com/api-references/text-models-llm/zhipu/glm-5)
99. [Chat Completions - DeepInfra docs](https://docs.deepinfra.com/chat/overview)
100. [Chat Completions (OpenAI-Compatible LLMs) - Documentation | Hive](https://docs.thehive.ai/docs/chat-completions-openai-compatible-llms)
101. [Add Compatibility for Open-Source Models like DeepSeek, Llama ...](https://github.com/langflow-ai/langflow/issues/6505)
102. [OpenAI-compatible APIs explained: All You Need to Know - CometAPI](https://www.cometapi.com/openai-compatible-apis-explained/)
103. [TIP: Chat Completions API reference - as a single request, for AI ...](https://community.openai.com/t/tip-chat-completions-api-reference-as-a-single-request-for-ai-understanding/1355654)
104. [Free AI Models on AIHubMix](https://aihubmix.com/blog/free-ai-models-on-aihubmix)
105. [DeepSeek API Guide: Pricing, Models & Setup](https://deepseek-usa.ai/docs/api/)
106. [Migration guides | Mistral Docs](https://docs.mistral.ai/resources/migration-guides)
107. [Beta Conversations](https://docs.mistral.ai/api/endpoint/beta/conversations)
108. [mistral-ai-chat-completions-openapi.yml - GitHub](https://github.com/api-evangelist/mistral-ai/blob/main/openapi/mistral-ai-chat-completions-openapi.yml)
109. [Open AI Responses API vs. Chat Completions vs. Messages API](https://portkey.ai/blog/open-ai-responses-api-vs-chat-completions-vs-anthropic-anthropic-messages-api)
110. [Mistral Nemo | AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/mistral-ai/mistral-nemo)
111. [Need help understanding function calls : r/MistralAI - Reddit](https://www.reddit.com/r/MistralAI/comments/1ngqo3f/need_help_understanding_function_calls/)
112. [AIKit and Mistral - Errors with ChatCompletion - 4D Forum](https://discuss.4d.com/t/aikit-and-mistral-errors-with-chatcompletion/36685)
113. [How can I use function calling with response format (structured ...](https://community.openai.com/t/how-can-i-use-function-calling-with-response-format-structured-output-feature-for-final-response/965784)
114. [Tool Execution](https://docs.cohere.com/docs/building-an-agent-with-cohere)
115. [Tool calling](https://docs.cohere.com/docs/migrating-v1-to-v2)
116. [About API Reference](https://docs.cohere.com/reference/about)
117. [chat-api.mdx - cohere-developer-experience - GitHub](https://github.com/cohere-ai/cohere-developer-experience/blob/main/fern/pages/v2/text-generation/chat-api.mdx?plain=1)
118. [[Feature]: Add API v2 support for Cohere · Issue #6980 · BerriAI/litellm](https://github.com/BerriAI/litellm/issues/6980)
119. [Cohere | AutoGen 0.2 - Microsoft Open Source](https://microsoft.github.io/autogen/0.2/docs/topics/non-openai-models/cloud-cohere/)
120. [Cohere Chat API — Documentation, OpenAPI - APIs.io](https://apis.io/apis/cohere/chat-api/)
121. [Introduction to the Cohere Chat API - LinkedIn](https://www.linkedin.com/learning/mastering-large-language-models-with-the-cohere-api/introduction-to-the-cohere-chat-api)
122. [Alibaba Cloud Model Studio:OpenAI compatible - Chat](https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope)
123. [Alibaba Cloud Model Studio - Text generation](https://www.alibabacloud.com/help/en/model-studio/text-generation)
124. [Qwen3.8-27B Practical Guide: Control Reasoning Depth and ...](https://www.alibabacloud.com/blog/qwen3-8-27b-practical-guide-control-reasoning-depth-and-extend-context-to-1m-tokens_603509)
125. [Alibaba Cloud Model Studio:Code capabilities (Qwen-Coder)](https://www.alibabacloud.com/help/en/model-studio/qwen-coder)
126. [Qwen3.6-Max-Preview: Smarter, Sharper, Still Evolving](https://qwen.ai/blog?id=qwen3.6-max-preview)
127. [Text Generation API Reference - Alibaba Cloud](https://www.alibabacloud.com/help/en/model-studio/qwen-api-reference/)
128. [Alibaba Cloud Model Studio:OpenAI-compatible - Batch (file input)](https://www.alibabacloud.com/help/en/model-studio/batch-interfaces-compatible-with-openai)
129. [Streaming output for Qwen models - Alibaba Cloud Model Studio](https://www.alibabacloud.com/help/en/model-studio/stream)
130. [Qwen-Omni-Alibaba Cloud Model Studio(Model Studio) - 阿里云文档](https://help.aliyun.com/en/model-studio/qwen-omni)
