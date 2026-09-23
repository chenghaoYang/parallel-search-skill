# LLM 时代的 API 请求协议：从 Chat Completions 到 Responses、Messages 与 GenerateContent

LLM API 并不存在一个真正统一的“聊天协议”。目前生态可归纳为四类主流原生范式：**OpenAI Chat Completions、OpenAI Responses、Anthropic Messages、Google Gemini GenerateContent**。DeepSeek、智谱 GLM、Qwen、Mistral 等大量厂商常以“OpenAI 兼容”降低接入成本，但这种兼容通常只覆盖基础聊天路径；在多模态、推理、工具调用、结构化输出、流式事件和状态管理上，仍可能存在决定工程成败的差异。[1][2][3][4]

本文的目标不是枚举每家字段，而是建立一套可迁移的 taxonomy：你看到任意一家模型 API 时，知道它属于哪一类、该对比什么、哪些“兼容”最容易踩坑。

***

## 1. 先建立总认知

### 1.1 LLM API 的本质

一个 LLM 调用不只是“输入 prompt，拿到 text”。完整协议至少要表达：

1. **上下文**：先前对话、系统指令、用户输入、历史工具结果。
2. **内容模态**：文本、图片、音频、视频、文件、引用内容等。
3. **生成控制**：模型、最大输出、温度、停止词、采样参数。
4. **输出形态**：纯文本、JSON、受 JSON Schema 约束的对象、图像、音频。
5. **模型动作**：函数调用、搜索、文件检索、代码执行、计算机操作。
6. **会话与状态**：由客户端每次重放历史，还是服务端通过 ID 保存与续接。
7. **传输语义**：一次性 JSON，还是 SSE 流；流中是 token delta，还是有类型的事件流。
8. **可观测与计费**：token 用量、缓存 token、停止原因、请求 ID、限流信息。

因此，所谓“协议差异”，核心不是 URL 或 `Authorization` 头，而是对以上八个问题的**数据建模方式**不同。

### 1.2 四类主流原生协议

| 协议家族 | 核心对象 | 输入组织 | 输出组织 | 典型定位 |
|---|---|---|---|---|
| OpenAI Chat Completions | `message` | `messages[]` | `choices[].message` | 传统聊天、兼容生态的事实标准 |
| OpenAI Responses | `item` / `response` | `input`，可为字符串或 typed items | `output[]` typed items | Agent、多工具、多模态、服务端状态 |
| Anthropic Messages | `message` + `content block` | `system` 顶层 + `messages[]` | 一个 assistant message，含 content blocks | 块级多模态与工具协作 |
| Gemini GenerateContent | `Content` + `Part` | `contents[]`、`systemInstruction` | `candidates[].content.parts[]` | Google 的内容/候选人/安全模型 |

OpenAI 自己明确把 Chat Completions 描述为 `messages` 数组，而 Responses 使用类型化的 `input` 和 `output` items；其中 message、function call、function result、reasoning 等都可以是独立 item。[2][5]

***

## 2. 四种原生协议对比

## 2.1 总体结构

| 维度 | OpenAI Chat Completions | OpenAI Responses | Anthropic Messages | Gemini GenerateContent |
|---|---|---|---|---|
| 主要请求路径 | `/v1/chat/completions` | `/v1/responses` | `/v1/messages` | `models/{model}:generateContent` |
| 对话输入根字段 | `messages` | `input` | `messages` | `contents` |
| 系统指令 | `system` 或 `developer` message | 顶层 `instructions`，或输入 item | 顶层 `system` | 顶层 `systemInstruction` |
| 核心内容模型 | message 内容 | typed items | content blocks | `Content.parts[]` |
| 主要输出位置 | `choices[].message` | `output[]` | `content[]` | `candidates[].content.parts[]` |
| 多候选 | `choices[]` | 常以一个 response 的 items 表达 | 通常单消息 | `candidates[]` 是一等概念 |
| 工具调用 | `tool_calls` 挂在 assistant message 上 | 独立 `function_call` output item | `tool_use` content block | `functionCall` part |
| 工具结果回传 | `role: "tool"` + `tool_call_id` | `function_call_output` + `call_id` | `tool_result` content block | `functionResponse` part |
| 状态续接 | 客户端重传 `messages[]` 为主 | `previous_response_id` 可链式续接 | 无状态，客户端重传 | 通常客户端重传 `contents[]` |
| 流式语义 | 兼容式 chunk/delta | 语义化 typed events | 块生命周期事件 | GenerateContent SSE 分块 |

Chat Completions 仍是最广泛被模仿的接口：一组 `messages` 进来，一个 `choices` 数组出去。OpenAI 的较新模型也区分 `developer` 与 `system`：在部分新模型中，`developer` message 取代了此前的 system message 语义。[6]

Responses 是一次重新抽象：它认为“上下文的基本单位”不应只是一条聊天消息，而是 item；模型消息、推理项、函数调用和函数结果都能被独立保留、回放或审计。[2]

Anthropic 采用“**消息是容器，content block 是内容和动作**”的结构。单个 `content` 可写成字符串，但它只是一个 text content block 数组的简写。[4][7]

Gemini 则采用“**一轮内容 Content 由若干 Part 组成**”的方式，且把安全反馈、候选结果与 usage metadata 纳入响应结构。[3][8]

***

## 2.2 最小请求的横向映射

以下四个请求语义相同：给模型一条用户输入“解释量子计算”。

### OpenAI Chat Completions

```json
{
  "model": "gpt-4.1",
  "messages": [
    {
      "role": "user",
      "content": "解释量子计算。"
    }
  ]
}
```

核心心智模型：

```text
messages[] -> choices[] -> choices[i].message
```

### OpenAI Responses

```json
{
  "model": "gpt-4.1",
  "instructions": "请用简明中文回答。",
  "input": [
    {
      "role": "user",
      "content": "解释量子计算。"
    }
  ]
}
```

或在简单场景中：

```json
{
  "model": "gpt-4.1",
  "input": "解释量子计算。"
}
```

核心心智模型：

```text
input -> response object -> output[] typed items
```

Responses 可接受文本或 item 数组作为 `input`；输出并不是“某个 choice 的 message”，而是 response 里的 typesafe `output` item 集合。[2][5]

### Anthropic Messages

```json
{
  "model": "claude-sonnet",
  "max_tokens": 512,
  "system": "请用简明中文回答。",
  "messages": [
    {
      "role": "user",
      "content": "解释量子计算。"
    }
  ]
}
```

若显式使用 block：

```json
{
  "model": "claude-sonnet",
  "max_tokens": 512,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "解释量子计算。"
        }
      ]
    }
  ]
}
```

Anthropic 的 `max_tokens` 在请求层通常是必要控制项；`system` 不放进普通消息列表，而是顶层字段。其 API 是无状态的多轮接口：应用负责保留并发送所需的会话历史。[4][7]

### Gemini GenerateContent

```json
{
  "systemInstruction": {
    "parts": [
      {
        "text": "请用简明中文回答。"
      }
    ]
  },
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "解释量子计算。"
        }
      ]
    }
  ]
}
```

核心心智模型：

```text
contents[] -> candidates[] -> candidate.content.parts[]
```

Gemini 的 `contents` 表达整个对话历史；每个 Content 由多个 `parts` 构成。单个请求也可能返回多个 candidate，且 prompt 层面的拦截信息在 `promptFeedback`，候选层面的停止与安全信息则随 candidate 返回。[3][8]

***

## 2.3 “消息”到底是什么：Message、Item、Block、Part

这是协议分歧的根源。

| 抽象层级 | Chat Completions | Responses | Anthropic | Gemini |
|---|---|---|---|---|
| 会话条目 | `message` | `item` | `message` | `Content` |
| 文本内容 | `content` | `input_text` / `output_text` 等 | `text` block | `text` part |
| 图像内容 | message content part | `input_image` 等 item content | image block | inline/file data part |
| 工具调用 | `tool_calls[]` | `function_call` item | `tool_use` block | `functionCall` part |
| 工具结果 | `tool` message | `function_call_output` item | `tool_result` block | `functionResponse` part |
| 推理轨迹 | 厂商扩展字段较常见 | 可为独立 reasoning item | 厂商定义的 thinking block | 模型/平台特定字段 |

### Chat Completions：消息优先

Chat Completions 将一个 turn 的多种元素较多地聚合在 message 中。例如 assistant message 可能同时有文本 `content` 和 `tool_calls`。这种方式对聊天很直观，但对复杂 agent 工作流不够自然：一个函数调用、一个工具返回、一段推理，都被迫映射到 message 附属字段或特殊 role。[2][6]

### Responses：事件/物品优先

Responses 将“模型在上下文中产生或需要处理的一件事”建模为 item：

- `message`
- `function_call`
- `function_call_output`
- reasoning 类 item
- 图像、文件、其他多模态对象
- 内置工具调用相关项目

这更适合 agent：模型先输出一个 function call item；应用执行后把 function-call output item 放回下一次 input；模型再继续生成。OpenAI 的 `previous_response_id` 还可把新请求接在上一个 response 后面，而不必由调用方每轮完整重放所有历史。[2][9]

### Anthropic：块优先

Anthropic 中，一条 assistant message 的 `content` 不是“一个字符串”，而是多个 block：

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "我来查询天气。"
    },
    {
      "type": "tool_use",
      "id": "toolu_123",
      "name": "get_weather",
      "input": {
        "city": "Shanghai"
      }
    }
  ]
}
```

这种设计有两个工程优势：

- 文本、工具调用、思考内容、引用或媒体在同一个输出中保持明确顺序。
- 工具调用并非 message 的“特殊附加字段”，而是与 text 平级的内容块。

Anthropic 的工具调用返回 `tool_use` block，并在 `stop_reason: "tool_use"` 时要求应用执行并回传 `tool_result`。[10][11]

### Gemini：Part 优先

Gemini 也把一个对话单元拆成 `parts[]`，但其命名与生态明显不同：

- 文本：`text`
- 函数调用：`functionCall`
- 函数结果：`functionResponse`
- 多模态数据：inline data 或文件数据引用

Gemini 的 `functionCall` 在较新的 Gemini 3 系列中带唯一 ID；应用执行函数之后，把 `functionResponse` part 放回对话上下文。[12][13]

***

## 3. 四个最容易混淆的差异

## 3.1 `system`、`developer` 与指令层级

不要把各家“系统提示词”当成可逐字段复制的语义。

| 平台 | 建议位置 | 重要语义 |
|---|---|---|
| OpenAI Chat Completions | `system` 或 `developer` message | 新模型中 `developer` 可能替代 `system` 的优先级角色 |
| OpenAI Responses | 顶层 `instructions` | 也可用 message/item，但 `instructions` 是清晰的全局指令入口 |
| Anthropic | 顶层 `system` | 不应简单当作 `messages[]` 内的一条 system role |
| Gemini | 顶层 `systemInstruction` | 与 `contents[]` 对话记录分离 |

**迁移原则**：把“平台/应用固定政策”和“用户可见对话”分离保存；每个适配器根据目标平台填到 `instructions`、`system`、`systemInstruction`、`developer` 或消息列表中。不要只做机械的字段重命名。

例如，把 Anthropic 顶层 `system` 直接插入 Gemini 的 `contents`，或把 Gemini `systemInstruction` 粗暴降为 OpenAI user message，都会改变它的指令层级与冲突处理方式。

OpenAI 的 Chat Completions 文档特别指出，在 o1 及更新模型中，developer messages 取代此前的 system messages；而 Responses 为全局指令提供了顶层 `instructions`。[2][6]

***

## 3.2 工具调用：名字相似，回传协议不同

四家工具调用的共同流程是：

1. 开发者声明工具及参数 schema。
2. 模型决定是否调用，并输出函数名和参数。
3. **应用自己执行工具**，模型不会替你执行你的本地函数。
4. 应用将工具结果带回模型。
5. 模型基于结果生成最终回答，或者继续调用工具。

Gemini 的官方说明明确强调：模型返回结构化函数名与参数，但执行由开发者应用负责。Anthropic 与 OpenAI 的机制也遵循同一责任边界。[9][10][13]

### 工具调用映射表

| 阶段 | OpenAI Chat Completions | OpenAI Responses | Anthropic Messages | Gemini GenerateContent |
|---|---|---|---|---|
| 工具定义 | `tools: [{type:"function", function:{...}}]` | `tools` | `tools: [{name, description, input_schema}]` | `tools[].functionDeclarations[]` |
| 模型请求工具 | `assistant.tool_calls[]` | `function_call` item | `tool_use` block | `functionCall` part |
| 调用关联 ID | `tool_call_id` | `call_id` | `tool_use.id` | 新系列通常带 function-call ID |
| 工具结果回传 | `role:"tool"` message | `function_call_output` item | `tool_result` block | `functionResponse` part |
| 是否支持多个调用 | 取决于模型/参数 | 支持工作流编排 | 可含一个或多个 block | 可并行或组合调用，取决于模型与配置 |

### OpenAI Chat Completions

模型返回：

```json
{
  "role": "assistant",
  "tool_calls": [
    {
      "id": "call_abc",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"city\":\"Shanghai\"}"
      }
    }
  ]
}
```

应用执行后追加：

```json
{
  "role": "tool",
  "tool_call_id": "call_abc",
  "content": "{\"temperature_c\":22,\"condition\":\"cloudy\"}"
}
```

### OpenAI Responses

模型返回独立 item：

```json
{
  "type": "function_call",
  "call_id": "call_abc",
  "name": "get_weather",
  "arguments": "{\"city\":\"Shanghai\"}"
}
```

应用回传：

```json
{
  "type": "function_call_output",
  "call_id": "call_abc",
  "output": "{\"temperature_c\":22,\"condition\":\"cloudy\"}"
}
```

这里最重要的变化是：工具调用不是 assistant message 的嵌套字段，而是 response 的独立 output item；工具结果也不是 `role: "tool"` 的聊天消息，而是输入中的 `function_call_output`。[2][9]

### Anthropic Messages

模型返回：

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_abc",
      "name": "get_weather",
      "input": {
        "city": "Shanghai"
      }
    }
  ],
  "stop_reason": "tool_use"
}
```

应用回传的用户消息中包含：

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_abc",
      "content": "{\"temperature_c\":22,\"condition\":\"cloudy\"}"
    }
  ]
}
```

Anthropic 的典型判断条件是 `stop_reason === "tool_use"`；仅检查“有没有文本”会漏掉模型等待工具结果的状态。[10][11]

### Gemini GenerateContent

模型返回候选内容的 part：

```json
{
  "functionCall": {
    "name": "get_weather",
    "args": {
      "city": "Shanghai"
    }
  }
}
```

应用将结果作为 `functionResponse` part 写回后续 `contents`：

```json
{
  "role": "function",
  "parts": [
    {
      "functionResponse": {
        "name": "get_weather",
        "response": {
          "temperature_c": 22,
          "condition": "cloudy"
        }
      }
    }
  ]
}
```

实际 SDK 或 API 版本可能对 role、ID 及外层结构有细微差别，应以所用 Gemini API 版本为准。核心是 `functionCall` / `functionResponse` 成对出现，而不是 OpenAI 风格的 `tool_call_id` + `role:"tool"`。[12][14]

### 工程上最重要的规则

**不要把工具结果当成可信指令。** 工具输出可能包含恶意文本、用户数据、网页内容或不可控第三方内容。应将它视为数据，做 schema 校验、长度限制、来源标记与权限控制，而不是让工具输出覆盖系统策略。

此外：

- 工具参数必须在执行前做 JSON Schema 或业务层校验。
- “模型调用了删除/转账/发信工具”不等于应当自动执行。
- 高风险动作应要求用户确认、最小权限、审计日志与幂等键。
- 用 `call_id`、`tool_use_id`、function call ID 关联请求与结果，不能仅按工具名称匹配。
- 同一轮可能有并行工具调用，执行器不应假设“一轮只会调用一个函数”。

***

## 3.3 结构化输出：JSON mode 不等于 JSON Schema

这是跨供应商最常见的误解之一。

### 三个不同层次

| 层次 | 目标 | 可靠性 | 典型做法 |
|---|---|---|---|
| Prompt 要求 JSON | “请输出 JSON” | 最弱 | 在 system/user prompt 写格式要求 |
| JSON mode | 输出可解析为合法 JSON | 中等 | `response_format: {type: "json_object"}` 等 |
| JSON Schema / Structured Outputs | 输出匹配给定 schema | 更强 | 指定 JSON Schema，平台约束字段与类型 |
| 本地验证与重试 | 业务对象真正可用 | 必需 | JSON parse + schema validator + 修复/重试 |

DeepSeek 文档说明，其 `response_format: {"type":"json_object"}` 可启用 JSON Output；同时要求在 system 或 user prompt 中出现 “json” 并最好给出预期格式。它保证的是有效 JSON 字符串，**不等价于业务 schema 必然满足**。[15]

Gemini 支持 `responseMimeType: "application/json"`，并结合 `responseSchema`；Google 文档明确建议两者共同使用以获得符合 schema 的 JSON 对象。[16]

Mistral 将 `json_object` 与 `json_schema` 区分开：前者保证 JSON，后者才强调符合你提供的 schema。[17]

### 实务建议

无论使用哪个供应商，都使用以下四层防线：

1. 在协议层开启该厂商最强的 structured output/schema 模式。
2. 提供简洁、明确的 schema，避免模糊的超大自由文本字段。
3. 在本地重新执行 JSON Schema、Pydantic、Zod、TypeScript validator 等校验。
4. 校验失败时，将错误摘要作为修复上下文重试；不要静默把半合法 JSON 写入数据库或执行系统。

***

## 3.4 流式：同为 SSE，不同事件语义

多数 LLM 平台都通过 `text/event-stream` / Server-Sent Events 流式返回结果，但不要把“都叫 SSE”误解为事件可互换。

| 协议 | 流式单位 | 消费方式 | 关键注意点 |
|---|---|---|---|
| Chat Completions | chunk，常见 `choices[].delta` | 拼接 delta | 工具参数可能分片到多个 chunk |
| Responses | 有类型的语义事件 | 监听事件名 | 如 `response.created`、`response.output_text.delta`、`response.completed` |
| Anthropic Messages | 消息/块生命周期事件 | 按 block index 重建 | text、tool use、thinking 可交错或独立更新 |
| Gemini | 多个 GenerateContentResponse | 拼接 candidate content parts | 注意 candidate、finish reason 与 safety |

OpenAI Responses 的流式接口被设计为语义化事件流；官方列出的常见事件包括 `response.created`、`response.output_text.delta`、`response.completed` 和 `error`。[18][19]

Mistral 的 Chat Completions 风格流则是更传统的 data-only SSE，并以 `data: [DONE]` 结束，这与许多 OpenAI-compatible 服务一致。[17]

### 正确的流式实现方式

不要直接把每个原始 SSE `data:` 片段打印给用户。你至少要有一个**协议专属 stream assembler**：

1. 解析 SSE frame。
2. 按事件类型/choice index/block index/call ID 分发。
3. 逐步拼接文本。
4. 逐步拼接工具参数 JSON。
5. 在完成事件或终止原因出现后，再把完整工具参数提交给 JSON 解析器。
6. 记录 usage、finish/stop reason、request ID。
7. 在断连、超时、取消时处理“部分输出已展示但调用未完成”的状态。

特别是工具调用，`arguments` 常常跨多个流 chunk 到达。对未完成 JSON 字符串调用 `JSON.parse()`，或在参数还没完整到达时执行工具，是典型 bug。

***

## 4. DeepSeek、智谱等兼容层到底差在哪

## 4.1 “OpenAI compatible” 的正确理解

“OpenAI compatible”最好理解为：

> 基础调用形状相似，让你能复用 HTTP 客户端、SDK 调用风格、`messages` 数组以及一部分请求参数。

它**不应**被理解为：

> 所有 endpoint、模型能力、字段语义、错误码、token 计费、流事件、工具调用、多模态与推理行为都与 OpenAI 完全一致。

例如 Together 的兼容文档明确指出：有些字段被接受但忽略，有些参数是 best-effort，有些 OpenAI 参数根本不支持，且其 logprobs shape 与 OpenAI 不同。[20]

vLLM 也声明兼容多个 OpenAI 接口，但仍列出明确限制，例如 Chat Completions 中 `user` 参数会被忽略、`parallel_tool_calls` 的实际行为受模型能力影响。[21]

### 兼容层的三种模式

| 模式 | 典型厂商/平台 | 特征 | 风险 |
|---|---|---|---|
| 原生协议 | OpenAI、Anthropic、Gemini | API 按自身对象模型设计 | 迁移成本高，但能力表达完整 |
| OpenAI-compatible facade | DeepSeek、智谱 GLM、Qwen、Mistral、Together、vLLM 等 | `/chat/completions`、`messages`、`choices` 接近 OpenAI | 字段支持与实际语义有差异 |
| 聚合/网关标准化 | OpenRouter、LiteLLM 等 | 将多厂商适配为统一接口 | 会丢失厂商特性，需处理扩展字段 |

OpenRouter 明确表示其请求/响应 schema 与 OpenAI Chat API 非常相似，并对不同模型/提供商进行规范化；LiteLLM 则以 OpenAI 格式为统一接口，支持跨 100+ 提供商。[22][23]

***

## 4.2 DeepSeek：兼容接口之外的两套思路

DeepSeek 的 Chat Completions 文档沿用典型 OpenAI 风格：

```json
{
  "model": "deepseek-flash",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Hello!"
    }
  ],
  "stream": false
}
```

其非流式响应是 chat completion object，核心文本在 choice 的 `message.content`，工具调用也采用 chat-completion 风格。[24][25]

但 DeepSeek 并不只有一种接入面：

- 它提供 OpenAI 风格的 `/chat/completions`。
- 它还提供 Anthropic-compatible base URL。
- 它也文档化了 Responses API，并支持 `message`、`function_call` 等更接近现代 item 语义的对象。[25][26]

### DeepSeek 与 OpenAI 文档的实际差异点

1. **模型专属控制参数**  
   DeepSeek 示例中出现 `thinking: {"type":"enabled"}` 与 `reasoning_effort: "high"`。这些不是传统 Chat Completions 的跨厂商稳定子集，迁移到其他供应商时必须走 capability mapping。[25]

2. **推理内容的处理**  
   推理模型常带 reasoning/thinking 相关字段或配置。不要假设它一定是普通 `message.content`，也不要把可见推理字段当成长期稳定 API 合约。

3. **工具调用历史回放限制**  
   DeepSeek 文档提示，其 Chat Completion API 不支持在对话中间插入 tool calls；若需要该能力，应使用 Anthropic API 或 Responses API。也就是说，即使 endpoint 看起来是 OpenAI Chat Completions，工具调用循环的“可重放性”也可能不同。[27]

4. **JSON mode 使用条件**  
   它的 JSON Output 不只是加 `response_format`；还要求 prompt 中提到 JSON。[15]

**结论**：DeepSeek 的“兼容”很适合迁移基础文本问答，但若你的系统依赖 reasoning 开关、工具调用历史、图像输入或 Responses item 工作流，必须按 DeepSeek 的具体 endpoint 单独测试。

***

## 4.3 智谱 GLM / Z.AI：Chat 形状接近 OpenAI，不等于 Claude Messages

智谱 Z.AI 的现代 Chat Completion 文档表面上十分接近 OpenAI：

```json
{
  "model": "glm-5.3",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful AI assistant."
    },
    {
      "role": "user",
      "content": "Hello, please introduce yourself."
    }
  ]
}
```

其 `messages` 是 prompt 对话列表，支持 system、user、assistant、tool 等消息类别，并有 chat completions 风格 endpoint。[28][29]

### 智谱的 `message` 与 Anthropic `Messages` 的关键不同

| 问题 | 智谱 GLM / OpenAI-like Chat | Anthropic Messages |
|---|---|---|
| `system` 放置 | 常作为 `messages[]` 的 `role:"system"` | 顶层 `system` 字段 |
| 内容基础单元 | 常见 `content` 字符串或 OpenAI 风格 part | `content` 是 string 或 typed block array |
| 工具调用表达 | 通常贴近 OpenAI `tool_calls` 生态 | `tool_use` 作为 content block |
| 工具结果 | 常为 `role:"tool"` + 调用 ID | `tool_result` block，关联 `tool_use_id` |
| 协议哲学 | 对话消息为中心 | 消息容器 + 内容块为中心 |
| 状态模型 | 客户端重传消息历史 | 同样无状态、客户端重传，但消息/块表示不同 |

因此，把智谱的 `messages` 直接当作 Anthropic 的 `messages` 是不安全的：

- 看起来都用 `role`、`content`。
- 但 Anthropic 的 content block 里可以原生承载 `tool_use` / `tool_result` 等对象。
- Anthropic 的 `system` 不应被当成普通 messages 内的一条 message。
- 工具调用及回传的字段、ID 和消息位置不同。

Anthropic 官方将 `content` 字符串定义为单个 text block 数组的简写，工具调用则使用 `tool_use` block 和 `input_schema`。[4][7][10]

### 对 GLM 等 OpenAI-compatible 提供商的建议

如果你只做“系统提示 + 用户文本 + assistant 文本”的基础对话，OpenAI-compatible 适配器通常足够。

但如果你做以下任意一项，应建立 provider-specific adapter：

- 函数调用与多轮工具循环。
- 视觉、音频、文件等多模态输入。
- 深度思考/推理开关与推理 token 计费。
- 结构化输出与 JSON Schema。
- 流式工具参数。
- Prompt caching、上下文缓存或服务端会话。
- 原生搜索、代码执行、网页浏览等内置工具。

***

## 4.4 Qwen、Mistral、Together、vLLM：兼容但必须有能力表

Qwen 的阿里云 Model Studio 支持 OpenAI-compatible Chat API，并可在同一个兼容接口中接入多种模型；但并非所有模型都支持该协议，例如 Qwen-Audio 只支持 DashScope 原生协议。[30]

Mistral 的 Chat Completions 接受 role 为 system、user、assistant、tool 的消息，且 `content` 可以是字符串或不同类型块的列表；其 JSON schema 模式和流式行为也有自身说明。[17][31]

Together 明确提供 OpenAI-compatible API，但公开列出许多差异：部分字段被忽略、`seed` 只是 best-effort、并非全部模型支持 `n`、多数模型不支持 `logit_bias`，且其推理配置可能采用额外的厂商字段。[20]

vLLM 为自托管模型提供 OpenAI-compatible server，并兼容 Chat Completions 与 Responses 等接口；但兼容程度同时依赖 vLLM 实现、模型的 chat template、模型本身的工具调用训练程度，以及 server 配置。[21][32]

**核心结论**：所谓协议兼容，必须从“endpoint 能否成功返回 200”升级为“该模型在此 endpoint 上支持哪些能力、语义是否可接受”。

***

## 5. 建立可迁移的协议 Taxonomy

## 5.1 用六层模型理解任意 LLM API

面对一个新厂商，不要先背字段。先从以下六层问问题。

| 层 | 要问的问题 | 典型差异 |
|---|---|---|
| 1. Transport | HTTP 路径、认证、SSE、重试、限流是什么？ | `Authorization`、API key header、SSE 格式 |
| 2. Conversation | 历史如何表示和续接？ | `messages`、`input`、`contents`、server state |
| 3. Content | 文本/图像/音频/文件如何编码？ | string、content parts、blocks、parts |
| 4. Control | 如何控制输出与推理？ | temperature、max tokens、thinking、seed、stop |
| 5. Actions | 工具如何声明、调用、回传？ | `tool_calls`、`function_call`、`tool_use`、`functionCall` |
| 6. Observability | 如何判断成功、停止、计费、缓存与排障？ | finish reason、usage、request ID、safety feedback |

这六层比“是否 OpenAI compatible”更有用。两个 API 即使 endpoint 和 JSON 字段都很像，也可能在第 4、5、6 层完全不同。

***

## 5.2 推荐的内部 Canonical IR

多供应商系统不应把 OpenAI、Claude 或 Gemini 的原始 JSON 直接传播到业务层。应该建立自己的中间表示（IR），然后为每个 provider 写 translator。

一个可行的概念模型：

```ts
type CanonicalTurn =
  | {
      kind: "message";
      role: "system" | "developer" | "user" | "assistant" | "tool";
      parts: CanonicalPart[];
    }
  | {
      kind: "tool_result";
      callId: string;
      name?: string;
      result: unknown;
      isError?: boolean;
    };

type CanonicalPart =
  | { type: "text"; text: string }
  | { type: "image_url"; url: string; detail?: "low" | "high" | "auto" }
  | { type: "image_bytes"; mimeType: string; data: string }
  | { type: "file"; fileId?: string; uri?: string; mimeType?: string }
  | { type: "tool_call"; callId: string; name: string; arguments: unknown }
  | { type: "reasoning"; text?: string; opaque?: unknown };

type GenerationRequest = {
  model: string;
  instructions?: string;
  history: CanonicalTurn[];
  tools?: CanonicalTool[];
  output?: {
    mode?: "text" | "json_object" | "json_schema";
    schema?: object;
  };
  generation?: {
    maxOutputTokens?: number;
    temperature?: number;
    topP?: number;
    stop?: string[];
    reasoningEffort?: "low" | "medium" | "high";
  };
  stream?: boolean;
};
```

重点不是这段类型是否完美，而是以下原则：

- **业务层只依赖 canonical 类型**，不依赖 `choices[0].message.content`。
- 每家 provider 都有 request mapper 与 response normalizer。
- 将供应商扩展参数隔离为 capability-specific options，而不是污染通用接口。
- 无法无损映射时显式报错、降级或记录 warning，不能静默“看起来成功”。

***

## 5.3 能力矩阵比字段映射更关键

为每个“供应商 + API surface + 模型”记录 capability profile，例如：

```yaml
provider: deepseek
api_surface: chat_completions
model: deepseek-flash
capabilities:
  text_input: true
  image_input: true
  audio_input: false
  tools: true
  parallel_tool_calls: unknown
  tool_history_replay: false
  json_object: true
  json_schema: verify
  streaming: true
  server_state: false
  reasoning_control: true
  system_message: true
```

应注意粒度：不是“DeepSeek 支持 tools”，而是“**DeepSeek 的哪一个模型、哪个 endpoint、哪个版本、在哪个区域/账户配置下支持何种 tools**”。

OpenRouter 的基础设施本身就按功能路由请求，并要求 provider 明确声明如 tools、structured outputs、JSON mode 等能力；这反映了生产系统中的正确思路：能力不是由“厂商名”决定，而是由具体模型和 endpoint 决定。[33]

***

## 5.4 适配器必须处理的不可逆差异

下列差异不能可靠地通过字段重命名解决。

### 指令优先级

`system`、`developer`、`instructions`、`systemInstruction` 的冲突规则各异。迁移时应保留“指令来源”和“优先级意图”，不是只保留纯文本。

### 多模态编码

一个平台可能用 URL，一个要求 data URI，一个支持 file ID，一个要求先上传文件。图片 detail、音频采样率、视频时长、文件引用的生命周期也不同。

### 工具调用回环

需适配：

- 调用对象在哪：message、item、block 或 part。
- 参数是 JSON string 还是 JSON object。
- 工具结果放在哪。
- 调用关联使用什么 ID。
- 是否允许并行调用。
- 是否可将历史 tool call 重新插回中间对话。
- 流式参数如何组合。

### Structured output

不要把 `json_object` 当作 `json_schema`。还要确认：

- schema 是否真的强约束；
- 是否支持 `additionalProperties`、enum、union、recursive schema；
- schema 是否与工具参数共享同一方言；
- refusals / safety block 时返回什么；
- 流式 JSON 是否可能中断。

### 采样参数

`temperature`、`top_p`、`presence_penalty`、`frequency_penalty`、`seed` 看似共通，但支持度和语义可能不同。某些推理模型会忽略、限制或重解释部分采样参数。

### Token 与费用

`max_tokens`、`max_completion_tokens`、`max_output_tokens` 不一定等义。输入 token、输出 token、reasoning token、cached token、工具 token、图像 token 的统计与计费方式也不同。

***

## 6. Chat Completions 与 Responses：该怎么选

### 选择 Chat Completions 的情况

- 你需要最快接入基础文本聊天。
- 你使用的目标厂商以 OpenAI-compatible `/chat/completions` 为主。
- 你已有成熟的 `messages[]` 历史管理。
- 你不需要服务端 response chain、复杂内置工具或细粒度 typed output。
- 你希望最大化对 DeepSeek、GLM、Qwen、Mistral、Together、vLLM 等的可移植性。

### 选择 Responses 的情况

- 你在 OpenAI 生态构建 agent。
- 你需要将 message、工具调用、工具结果、推理/多模态操作建模为独立对象。
- 你需要 `previous_response_id` 形式的服务端状态续接或分叉。
- 你要使用现代内置工具或更语义化的流事件。
- 你愿意接受它不是所有“OpenAI compatible”供应商都能完整实现的现实。

OpenAI 将 Responses 定位为更新的 API primitive，强调 agentic primitives 与 `input`/`output` item 模型；Chat Completions 则仍是大量兼容提供商的共同底座。[2][21][34]

### 一个实际建议

如果你正在设计新系统：

- 对外和业务层：使用自己的 canonical conversation/action IR。
- 默认兼容路径：支持 OpenAI Chat Completions 语义。
- 高级 provider path：为 OpenAI Responses、Anthropic Messages、Gemini GenerateContent 提供原生适配。
- 不要强行把所有高级能力压扁成 `messages[].content: string`。
- 不要反过来假设每个兼容供应商都能接住 Responses 的全部 item 类型。

***

## 7. 生产落地检查清单

## 7.1 接入新模型前

- 确认 endpoint 与模型 ID，而不是只确认品牌名称。
- 确认使用原生 API、OpenAI-compatible API，还是网关/聚合器 API。
- 明确 `system` / `developer` / `instructions` 的正确放置位置。
- 用真实多轮历史验证 assistant message 与 tool result 是否能被正确回放。
- 验证图片、文件、音频等输入的编码、大小、格式和权限要求。
- 验证 JSON mode 与 JSON Schema 的真实保证范围。
- 验证工具调用参数是否稳定、是否支持并行、工具结果如何关联。
- 验证流式 text、tool arguments、错误和完成事件。
- 记录 usage 的字段口径及缓存/推理 token 的计费方式。
- 捕获 request ID、rate-limit headers、原始错误 body，以便排障。

OpenAI 的 API 概览建议检查请求 ID 与限流相关响应头；这类可观测信息应统一纳入你的日志和 trace，而不是在出错后才临时寻找。[35]

## 7.2 最小兼容测试集

每个 provider/model/endpoint 至少跑以下测试：

1. 单轮纯文本。
2. 含系统/开发者指令的单轮文本。
3. 五轮以上的多轮历史。
4. 中文、英文、超长文本和特殊字符。
5. 一张图片或其他目标多模态输入。
6. `json_object` 输出。
7. JSON Schema 输出及本地 schema 验证。
8. 单个工具调用。
9. 并行工具调用。
10. 工具错误返回与模型恢复。
11. SSE 文本流。
12. SSE 工具参数流。
13. 长上下文与上下文溢出。
14. 安全拒绝、内容拦截和停止原因。
15. 超时、429、5xx、网络中断与幂等重试。

## 7.3 常见失败模式

| 症状 | 常见根因 | 修复方向 |
|---|---|---|
| 200 但模型忽略系统提示 | 把 system/developer/instructions 放错位置 | 使用对应原生指令层 |
| 工具永远不调用 | schema 太弱、工具描述差、模型/endpoint 不支持 | 检查 capability，强化工具描述与 schema |
| 工具调用后模型重复提问 | tool result 放错 role/block/item 或 ID 不匹配 | 按 provider 原生回传格式实现 |
| SSE 中 JSON 解析失败 | 在流未结束时解析 arguments | 累积到完成事件后再解析 |
| JSON 可 parse 但业务失败 | 只用了 JSON mode，未做 schema 验证 | 采用 schema mode + 本地 validator |
| 迁移后成本激增 | token 定义、历史重放、缓存机制不同 | 记录各类 usage 并按 endpoint 分析 |
| 同样参数输出明显变了 | 参数被忽略或模型采样语义不同 | capability-driven mapping，建立回归测试 |
| 网关切换模型后功能失效 | “兼容”层丢失厂商高级能力 | 对高级路径保留 provider-native adapter |

***

## 8. 最终结论

要理解 LLM 时代的 API 请求协议，可以记住三句话：

1. **Chat Completions 是最重要的兼容底座，但不是完整标准。**  
   它解决了“消息列表 → assistant 回复”的基础问题，因此成为 DeepSeek、智谱 GLM、Qwen、Mistral、Together、vLLM 等广泛模仿的接口形状；但兼容通常不保证参数、工具、流、推理、多模态和结构化输出的完全一致。[21][24][28][30]

2. **Responses、Anthropic Messages、Gemini GenerateContent 的差异，本质是对象模型不同。**  
   OpenAI Responses 以 typed item 为中心；Anthropic 以 content block 为中心；Gemini 以 Content/Part 与 candidate 为中心；传统 Chat Completions 以 message/choice 为中心。理解对象模型，比背 JSON 字段更能帮助你迁移和排错。[2][3][4]

3. **生产系统应面向能力与语义做适配，而不是面向字段名做字符串替换。**  
   用内部 canonical IR 管理对话与工具循环；用 provider/model/endpoint 粒度的 capability matrix 决定降级；在工具、结构化输出、流式、多模态与可观测性上保留原生适配。这才是“多模型”架构真正稳定的边界。

## Citations

1. [Chat Completions Overview | OpenAI API Reference](https://developers.openai.com/api/reference/chat-completions/overview/)
2. [Migrate to the Responses API - OpenAI Developers](https://developers.openai.com/api/docs/guides/migrate-to-responses)
3. [Generating content | Gemini API - Google AI for Developers](https://ai.google.dev/api/generate-content)
4. [Messages - Claude API Reference](https://platform.claude.com/docs/en/api/messages)
5. [Create a model response | OpenAI API Reference](https://developers.openai.com/api/reference/resources/responses/methods/create/)
6. [Create chat completion | OpenAI API Reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/)
7. [Create a Message - Claude API Reference](https://platform.claude.com/docs/en/api/messages/create)
8. [Gemini API reference | Google AI for Developers](https://ai.google.dev/api)
9. [Function calling | OpenAI API](https://developers.openai.com/api/docs/guides/function-calling)
10. [Tool use with Claude - Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
11. [Stop reasons and fallback - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
12. [Function calling with the Gemini API - ai.google.dev](https://ai.google.dev/gemini-api/docs/generate-content/function-calling)
13. [Function calling with the Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/function-calling)
14. [Introduction to function calling | Gemini Enterprise Agent ...](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/tools/function-calling)
15. [JSON Output - DeepSeek API Docs](https://api-docs.deepseek.com/guides/json_mode/)
16. [Generate content with the Gemini API - Google Cloud Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/inference)
17. [Chat Endpoints - Mistral AI Documentation](https://docs.mistral.ai/api/endpoint/chat)
18. [Streaming API responses - OpenAI Developers](https://developers.openai.com/api/docs/guides/streaming-responses)
19. [Responses streaming events | OpenAI API Reference](https://developers.openai.com/api/reference/resources/responses/streaming-events/)
20. [OpenAI compatibility - Together AI docs](https://docs.together.ai/docs/inference/openai-compatibility)
21. [Online Serving - vLLM Documentation](https://docs.vllm.ai/en/latest/serving/online_serving/)
22. [OpenRouter API Reference - Complete Documentation](https://openrouter.ai/docs/api_reference/overview)
23. [Getting Started - LiteLLM](https://docs.litellm.ai/docs/)
24. [Chat Completions API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-chat-completion/)
25. [DeepSeek API Docs: Your First API Call](https://api-docs.deepseek.com/)
26. [Using the Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/guides/responses_api/)
27. [Tool Calls | DeepSeek API Docs](https://api-docs.deepseek.com/guides/tool_calls/)
28. [Chat Completion - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/api-reference/llm/chat-completion)
29. [Quick Start - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/guides/overview/quick-start)
30. [OpenAI compatible - Chat - 阿里云帮助文档](https://help.aliyun.com/en/model-studio/qwen-api-via-openai-chat-completions)
31. [Chat completions | Mistral Docs](https://docs.mistral.ai/studio/conversations/chat-completion)
32. [OpenAI-Compatible Server - vLLM Documentation](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)
33. [Become a Provider - OpenRouter](https://openrouter.ai/providers/apply)
34. [Responses Overview | OpenAI API Reference](https://developers.openai.com/api/reference/responses/overview/)
35. [API Overview | OpenAI API Reference](https://developers.openai.com/api/reference/overview/)
36. [Anthropic Claude Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html)
37. [Native API (/chat/completions) | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/ai/aig/chat-completion/zai-glm/zai-glm-chat-completion)
38. [Z.AI (Zhipu AI) - LiteLLM](https://docs.litellm.ai/docs/providers/zai)
39. [HTTP API Calls - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/guides/develop/http/introduction)
40. [Create a Message - Fireworks AI Docs](https://docs.fireworks.ai/api-reference/anthropic-messages)
41. [Community Providers: Zhipu AI (Z.AI) - AI SDK](https://ai-sdk.dev/providers/community-providers/zhipu)
42. [Inference using Anthropic Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-messages-api.html)
43. [Function calling reference | Gemini Enterprise Agent Platform ...](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/function-calling)
44. [Stream a Claude response to the browser - Deno Docs](https://docs.deno.com/examples/anthropic_sse/)
45. [How to Interact with APIs Using Function Calling in Gemini](https://codelabs.developers.google.com/codelabs/gemini-function-calling)
46. [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use)
47. [Using tools | OpenAI API](https://developers.openai.com/api/docs/guides/tools)
48. [Providers - LiteLLM](https://docs.litellm.ai/docs/providers)
49. [Mistral AI chat completion - Amazon Bedrock - AWS Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-mistral-chat-completion.html)
50. [OpenAI Compatible Providers - AI SDK](https://ai-sdk.dev/providers/openai-compatible-providers)
51. [OpenRouter Quickstart Guide](https://openrouter.ai/docs/quickstart)
52. [OpenAI-Compatible Server - vLLM Documentation](https://docs.vllm.ai/en/v0.18.0/serving/openai_compatible_server/)
53. [Alibaba Cloud Model Studio:OpenAI-compatible - Batch (file input)](https://www.alibabacloud.com/help/en/model-studio/batch-interfaces-compatible-with-openai)
54. [OpenAI Compatible - Cline documentation](https://docs.cline.bot/provider-config/openai-compatible)
55. [OpenAI-Compatible Endpoints - LiteLLM Docs](https://docs.litellm.ai/docs/providers/openai_compatible)
56. [Migration guides | Mistral Docs](https://docs.mistral.ai/resources/migration-guides)
57. [OpenAI - LiteLLM Docs](https://docs.litellm.ai/docs/providers/openai)
58. [Text generation | OpenAI API](https://developers.openai.com/api/docs/guides/text)
59. [Google Gen AI SDK documentation](https://googleapis.github.io/python-genai/)
60. [Open AI Responses API vs. Chat Completions vs. Messages API](https://portkey.ai/blog/open-ai-responses-api-vs-chat-completions-vs-anthropic-anthropic-messages-api)
61. [[Bug]: Google AI generateContent endpoints require a different ...](https://github.com/BerriAI/litellm/issues/12671)
62. [Google Gemini Generate Content Schema - APIs.io](https://apis.io/schemas/google-gemini/google-gemini-generate-content/)
63. [Introducing the Responses API - OpenAI Developer Community](https://community.openai.com/t/introducing-the-responses-api/1140929)
64. [Chat Completions vs OpenAI Responses API: What Actually Changed](https://dev.to/dev-in-progress/chat-completions-vs-openai-responses-api-what-actually-changed-4bco)
65. [TIP: Chat Completions API reference - as a single request, for AI ...](https://community.openai.com/t/tip-chat-completions-api-reference-as-a-single-request-for-ai-understanding/1355654)
66. [Native API (/messages) | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/ai/aig/chat-completion/anthropic-claude/anthropic-claude-message)
67. [Anthropic Messages - Introduction to Langdock - Docs](https://docs.langdock.com/en/developer/completion-api/anthropic)
68. [Explore DeepSeek API - Chat Completion and more - SerpApi](https://serpapi.com/blog/explore-deepseek-api/)
69. [DeepSeek-V4-Flash Now Supports the Responses API and Codex](https://apidog.com/blog/deepseek-v4-flash-responses-api-codex/)
70. [Messages API (/messages) - TrueFoundry Docs](https://www.truefoundry.com/docs/ai-gateway/messages-overview)
71. [anthropic-sdk-python/src/anthropic/resources/beta/messages ...](https://github.com/anthropics/anthropic-sdk-python/blob/main/src/anthropic/resources/beta/messages/messages.py)
72. [Anthropic | AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/anthropic)
73. [Z.ai API Platform — Start building with GLM-5.3](https://z.ai/model-api)
74. [glm-zhipu - 阿里云文档](https://help.aliyun.com/en/model-studio/glm-zhipu)
75. [智谱AI | 中文| API References](https://docs.console.zenlayer.com/api-reference/cn/compute/aig/chat-completion/zhipu-chat-completion)
76. [GLM API Guide - Tencent Cloud](https://intl.cloud.tencent.com/document/product/1300/80634)
77. [glm-5.3 (Zhipu AI) · Cloudflare AI docs · Cloudflare Workers ...](https://developers.cloudflare.com/workers-ai/models/glm-5.3/)
78. [Z.AI GLM Models Support · olimorris codecompanion.nvim - GitHub](https://github.com/olimorris/codecompanion.nvim/discussions/2850)
79. [Glm 5.2 - AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/zhipu/glm-5.2)
80. [ZhipuAI API - 智谱AI](https://open.bigmodel.cn/dev/api)
81. [chat-completions-quickstart](https://evolink.ai/docs/de/api-manual/language-series/glm/chat-completions/chat-completions-quickstart)
82. [claude-api/references/streaming.md at main - GitHub](https://github.com/diskd-ai/claude-api/blob/main/references/streaming.md)
83. [CLASP/docs/api-reference/anthropic-messages.md at main - GitHub](https://github.com/jedarden/CLASP/blob/main/docs/api-reference/anthropic-messages.md)
84. [Claude API Streaming (SSE) in Practice: From Typewriter Effects to ...](https://apito.ai/en/blog/dev-guides/claude-api-streaming-sse-guide/)
85. [Create a Message | ZenMux | Documentation](https://zenmux.ai/docs/api/anthropic/create-messages.html)
86. [Streaming Tool Calls: Parse Anthropic SSE Without Loading the ...](https://dev.to/gabrielanhaia/streaming-tool-calls-parse-anthropic-sse-without-loading-the-whole-message-2on)
87. [HTTP Streaming Antropic Claude AI - General Usage - Julia Discourse](https://discourse.julialang.org/t/http-streaming-antropic-claude-ai/117666)
88. [Use the Azure OpenAI Responses API - Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses)
89. [Streaming - OpenAI Agents SDK](https://openai.github.io/openai-agents-python/streaming/)
90. [Specification - Open Responses](https://www.openresponses.org/specification)
91. [Responses API streaming - the simple guide to "events"](https://community.openai.com/t/responses-api-streaming-the-simple-guide-to-events/1363122)
92. [Request for example of a custom tool Function Call back using the ...](https://community.openai.com/t/request-for-example-of-a-custom-tool-function-call-back-using-the-client-responses-create-method/1372132)
93. [v1/responses API Documentation - UCloud Global](https://www.ucloud-global.com/en/docs/modelverse/modelverse/text_api/response_api)
94. [OpenAI Responses API - neurals, visualizing agentic AI](https://neurals.ca/tech/openai/responses-api/)
95. [OpenAI Responses API.md - Github-Gist](https://gist.github.com/steipete/b58f0087c02fd97cea73f016e42c8ac0)
96. [Gemini 3 developer guide - generateContent API](https://ai.google.dev/gemini-api/docs/generate-content/gemini-3)
97. [Combine built-in tools and function calling - generateContent API](https://ai.google.dev/gemini-api/docs/generate-content/tool-combination)
98. [Text generation - generateContent API](https://ai.google.dev/gemini-api/docs/generate-content/text-generation)
99. [Gemini Function calling, and how it relates to MCP - GitHub](https://github.com/DinoChiesa/Gemini-Function-Calling)
100. [Function Calling Guide: Google DeepMind Gemini 2.0 Flash](https://www.philschmid.de/gemini-function-calling)
101. [Google gemini generate_content is not working in python API using ...](https://stackoverflow.com/questions/78497434/google-gemini-generate-content-is-not-working-in-python-api-using-function-calli)
102. [Google Gemini API Reference | Wavise OpenLLM](https://openllm.wavise.com/blog/gemini-api-reference)
103. [System Instructions and Prompting Fundamentals | google ...](https://deepwiki.com/google-gemini/cookbook/3.4-system-instructions-and-prompting-fundamentals)
104. [OpenAI API and Models - OpenRouter](https://openrouter.ai/openai)
105. [Provider Routing - Smart Multi-Provider Request Management](https://openrouter.ai/docs/guides/routing/provider-selection)
106. [Auto Router - API Pricing & Providers - OpenRouter](https://openrouter.ai/openrouter/auto)
107. [OpenAI (or Compatible) Language Models - Spice.ai OSS](https://spiceai.org/docs/components/models/openai)
108. [Cline SDK support for OpenAI-compatible APIs (custom baseURL + ...](https://github.com/cline/cline/discussions/10322)
109. [Add ability to choose preferred provider on OpenRouter #737 - GitHub](https://github.com/cline/cline/issues/737)
110. [BASE URL for api provider "OPEN AI COMPATIBLE" : r/RooCode](https://www.reddit.com/r/RooCode/comments/1iekmvd/base_url_para_api_provider_open_ai_compatible/)
111. [OpenRouter Provider : r/OpenWebUI - Reddit](https://www.reddit.com/r/OpenWebUI/comments/1ilcuhv/openrouter_provider/)
112. [LiteLLM Docs](https://docs.litellm.ai/)
113. [Langchain, OpenAI SDK, LlamaIndex, Instructor, Curl examples](https://docs.litellm.ai/docs/proxy/user_keys)
114. [Usage - LiteLLM](https://docs.litellm.ai/docs/completion/usage)
115. [LiteLLM Provider - Access 400+ LLMs with Unified API | Promptfoo](https://www.promptfoo.dev/docs/providers/litellm/)
116. [How to Implement vLLM with OpenAI-Compatible API - OneUptime](https://oneuptime.com/blog/post/2026-01-28-vllm-openai-compatible-api/view)
117. [Support openai responses API interface · Issue #14721 · vllm-project ...](https://github.com/vllm-project/vllm/issues/14721)
118. [General openai compatible provider #8478 - BerriAI/litellm - GitHub](https://github.com/BerriAI/litellm/issues/8478)
119. [Code Review: Deep Dive into vLLM's Architecture and ... - Zerohertz](https://zerohertz.github.io/vllm-openai-2/)
120. [Alibaba Cloud Model Studio:Deep thinking](https://www.alibabacloud.com/help/en/model-studio/deep-thinking)
121. [Documentation - Mistral AI](https://docs.mistral.ai/)
122. [llm — pipecat-ai documentation](https://reference-server.pipecat.ai/en/latest/api/pipecat.services.qwen.llm.html)
123. [mistral-ai-chat-completions-openapi.yml - GitHub](https://github.com/api-evangelist/mistral-ai/blob/main/openapi/mistral-ai-chat-completions-openapi.yml)
124. [Qwen api support? · mem0ai mem0 · Discussion #3032 - GitHub](https://github.com/mem0ai/mem0/discussions/3032)
125. [Alibaba Cloud (Qwen) Provider - Promptfoo](https://www.promptfoo.dev/docs/providers/alibaba/)
126. [Create a Chat Completion | Mistral AI | One](https://www.withone.ai/knowledge/mistral-ai/conn_mod_def::GMZh4byhB1A::1odXn1sYRQGnj4EbkR-lEw)
127. [How to send context between multiple Mistral AI api call to keep ...](https://stackoverflow.com/questions/79116496/how-to-send-context-between-multiple-mistral-ai-api-call-to-keep-conversation-li)
128. [DashScope (Alibaba Cloud Model Studio) API](https://apis.io/apis/qwen/dashscope/)
