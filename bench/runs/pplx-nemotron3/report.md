# LLM 时代 API 请求协议：从 Chat Completions 到 Responses、Messages 与 generateContent

LLM API 表面上都在做一件事：传入上下文，得到模型输出。但它们并不存在一个真正统一的“对话协议”。最常见的分歧不是 URL、鉴权或模型名，而是**输入如何被建模、输出如何被封装、工具调用如何闭环、流式事件如何表达，以及状态由谁保存**。

可以先记住这个结论：

> **OpenAI Chat Completions 形成了最广泛的兼容层；OpenAI Responses、Anthropic Messages、Google Gemini generateContent 则分别代表了三种不同的原生协议范式。**  
> 下游厂商所谓“OpenAI 兼容”通常只保证核心聊天请求能跑，并不保证多模态、推理、工具、结构化输出、流式事件、状态与错误语义完全一致。

本文以四类主流协议为主线建立 taxonomy：

1. **OpenAI Chat Completions**：历史最广泛的聊天兼容格式
2. **OpenAI Responses**：面向 agent、工具和多模态工作流的 item 协议
3. **Anthropic Messages**：以显式内容块和工具闭环为中心的协议
4. **Google Gemini generateContent**：以 `Content` / `Part` 为基本单元的多模态协议

随后会讨论 DeepSeek、智谱 GLM 等国内或下游模型服务的适配方式，以及落地时真正容易踩坑的地方。

***

## 1. 总览：先按“协议家族”理解

### 1.1 四类主要范式

| 协议家族 | 代表 API | 核心输入对象 | 核心输出对象 | 状态模型 | 主要设计重心 |
|---|---|---|---|---|---|
| Chat Completions | `POST /v1/chat/completions` | `messages[]` | `choices[]` → `message` | 通常由应用传回完整历史 | 聊天补全、生态兼容 |
| Responses | `POST /v1/responses` | `input`，可为字符串或 typed items | `output[]` typed items | 可手动管理，也可通过 response / conversation 关联 | Agent、工具、推理、多模态 |
| Anthropic Messages | `POST /v1/messages` | `system` + `messages[]` | 一个 `Message`，含 `content[]` | 客户端传递历史 | 内容块、多轮工具调用、显式约束 |
| Gemini generateContent | `:generateContent` | `contents[]`，每项含 `parts[]` | `candidates[]`，每项含 `content.parts[]` | 客户端传递历史 | 原生多模态、候选结果、安全反馈 |

OpenAI 的 Chat Completions 以 `messages[]` 为中心，返回 `choices[]`；OpenAI 的 Responses 将输入、输出统一为**有类型的 item 流**。官方迁移说明明确指出：Chat Completions 的 `choices[].message` 在 Responses 中变成 `output[]`，而 message 只是诸多 item 类型之一，另有 reasoning、function call、function-call output 等。[1]

Anthropic 的 Messages API 也叫“messages”，但其语义与 OpenAI Chat Completions 不同：它的顶层 `system` 独立于会话消息，消息内容通常采用 `content[]` 块；Google Gemini 则用 `contents[]` 表示回合，用 `parts[]` 表示一个回合中的文字、图像、文件或函数调用等片段。[2][3]

### 1.2 不应把“聊天”误当作统一模型

以下对象名称相似，但不能视为等价：

| 名称 | 常见来源 | 看起来像什么 | 实际风险 |
|---|---|---|---|
| `messages` | OpenAI Chat、Anthropic、DeepSeek、智谱等 | 对话历史数组 | role、content 类型、system 支持、工具消息语义不同 |
| `message` | Chat Completion 的一条消息 | 单个助手回答 | 在不同 API 中不一定可直接回填 |
| `content` | Anthropic、Gemini、OpenAI 及各兼容层 | 文本字段 | 可能是字符串、内容块数组、`Part` 数组或输出块 |
| `response` | OpenAI Responses、DeepSeek Responses | 一次模型运行结果 | 不等价于 `chat.completion`，包含多类 output item |
| `tool_calls` / `tool_use` / `functionCall` | 各厂商 | 模型请求外部函数 | 字段名、ID、参数编码、结果回传方式全不同 |

因此，系统设计里最好把“供应商协议”与“内部对话模型”分开。不要把 OpenAI 的 `ChatCompletion` 对象直接当成业务层的通用对象。

***

## 2. OpenAI：Chat Completions 与 Responses 的分界

OpenAI 自己就同时存在两种重要接口。理解二者的差别，是理解整个行业协议分化的起点。

## 2.1 Chat Completions：`messages[]` → `choices[]`

Chat Completions 的基本形式是：

```json
POST /v1/chat/completions

{
  "model": "example-model",
  "messages": [
    {
      "role": "developer",
      "content": "你是一个严谨的技术助手。"
    },
    {
      "role": "user",
      "content": "解释 API 协议差异。"
    }
  ],
  "stream": false
}
```

典型响应结构：

```json
{
  "id": "chatcmpl_...",
  "object": "chat.completion",
  "created": 1760000000,
  "model": "example-model",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "……"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 200,
    "total_tokens": 300
  }
}
```

它的核心抽象非常简单：

$$
\text{Conversation} = [\text{message}_1, \text{message}_2, \ldots, \text{message}_n]
$$

$$
\text{Completion} = \text{choices}[i].\text{message}
$$

OpenAI 官方定义中，Chat Completions 的请求是“由一组 messages 构成的对话”，响应是一个 chat completion object；如果开启流式，则返回 chat completion chunk 序列。[4][5]

### Chat Completions 的优势

- 非常适合传统 chatbot、问答、简单 RAG。
- 几乎所有模型网关、开源推理服务、国内模型服务都提供某种兼容层。
- SDK、框架和社区范式成熟。
- 请求与响应都较容易记录、回放、缓存和调试。
- 若只做文本聊天，数据模型足够直观。

### Chat Completions 的结构性局限

- 工具调用、推理痕迹、多模态和文件处理会不断向 `message` 上堆字段。
- 复杂 agent 工作流很难用“只有消息”的模型完整表达。
- 对话状态通常由客户端自行管理：每轮要重传历史，或者依赖自建会话存储。
- 不同厂商都声称兼容，但“兼容范围”不受统一标准约束。

例如，Chat Completions 的工具调用通常放在 assistant message 中：

```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_001",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"city\":\"Shanghai\"}"
      }
    }
  ]
}
```

随后应用必须把工具结果以特定 `tool` role 传回：

```json
{
  "role": "tool",
  "tool_call_id": "call_001",
  "content": "{\"temperature_c\": 25}"
}
```

这是一个**消息驱动的工具循环**：模型输出 assistant message，应用执行工具，再构造一条 tool message 继续请求模型。

***

## 2.2 Responses：从“聊天消息”扩展到“类型化工作项”

OpenAI Responses API 的关键变化不是把 `messages` 改名成 `input`，而是改变底层抽象：

- 输入不只是消息；它可以是文字、图像、文件、之前的 assistant 输出、函数执行结果等。
- 输出不只是 assistant message；它可以包含文本消息、reasoning、函数调用、内建工具调用等不同 item。
- agent 的执行轨迹可被表达为一系列明确类型的对象。

简单请求可以非常短：

```json
POST /v1/responses

{
  "model": "example-model",
  "input": "解释 API 协议差异。"
}
```

但更具代表性的请求是 typed input：

```json
{
  "model": "example-model",
  "instructions": "你是一个严谨的技术助手。",
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "比较 Chat Completions 与 Responses。"
        }
      ]
    }
  ]
}
```

响应的核心不再是 `choices[0].message.content`，而是：

```json
{
  "id": "resp_...",
  "object": "response",
  "status": "completed",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "……"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 100,
    "output_tokens": 200
  }
}
```

OpenAI 将其定义为新的 API primitive：Chat Completions 使用 `messages` 同时承载输入与输出；Responses 使用 `input` 和 `output` 两套 typed item 数组。`message` 只是 output item 的一种，另有 `reasoning`、`function_call`、`function_call_output` 等。[1]

### Responses 的关键概念

| 概念 | 含义 | 与 Chat Completions 的关系 |
|---|---|---|
| `instructions` | 高优先级全局指令 | 通常替代或补充 system / developer message |
| `input` | 本轮输入，可为字符串或 item 数组 | 替代请求中的 `messages` |
| `output` | 本轮产生的全部 typed items | 替代 `choices[]` |
| `response.output_text` | SDK 常见的便利访问器 | 不应假设所有结果都只是文本 |
| `function_call` | 模型对自定义函数的调用项 | 类似旧式 `tool_calls`，但属于 output item |
| `function_call_output` | 应用返回的工具执行结果 | 下一轮作为 input item 传入 |
| `previous_response_id` / conversation | 服务端或逻辑上的上下文关联方式 | 减少手工回填整段历史的需求 |

官方文档还指出，Responses 可以接受文字、图像、文件等输入，也可以让模型调用自定义代码或内建工具，例如 web search、file search；conversation 关联时，该会话此前的 items 会被自动添加进当前请求上下文。[6]

### 为什么 Responses 是“agent 协议”而不只是新 endpoint

假设用户问：“查一下北京今天的天气，并说明是否适合跑步。”

模型可能产生的不是一个纯文本回答，而是一个工作流：

```text
input message
  → function_call(get_weather)
  → function_call_output(weather result)
  → output message
```

用伪 JSON 表示：

```json
{
  "output": [
    {
      "type": "function_call",
      "call_id": "call_weather_01",
      "name": "get_weather",
      "arguments": "{\"city\":\"Beijing\"}"
    }
  ]
}
```

应用执行函数后继续：

```json
{
  "model": "example-model",
  "previous_response_id": "resp_previous",
  "input": [
    {
      "type": "function_call_output",
      "call_id": "call_weather_01",
      "output": "{\"temperature_c\":22,\"rain\":false,\"aqi\":55}"
    }
  ]
}
```

这样，工具调用不再被视为 assistant message 的附属字段，而被视为一等的、可追踪的执行 item。

### 迁移时最容易犯的错误

- 继续硬编码 `choices[0].message.content`。
- 把 `response.output` 当成一定只有一个 item。
- 只读取文本，而忽略函数调用、拒绝、推理相关或工具输出 item。
- 将旧的 `tool` role 消息不加转换地塞进 Responses。
- 认为 `instructions` 与历史中的 system message 永远可完全等价。
- 以为“状态化”意味着不用再考虑上下文边界、隐私、成本或缓存。

***

## 3. Anthropic Messages：显式 system、内容块与 tool_use

Anthropic 的主对话接口是 `POST /v1/messages`。它也接收 `messages[]`，但绝不能把它机械看成 OpenAI Chat Completions 的同义物。Anthropic 官方将其描述为：发送结构化消息列表，模型生成下一条消息。[2]

一个简化请求：

```json
POST /v1/messages

{
  "model": "claude-model",
  "max_tokens": 1024,
  "system": "你是一个严谨的技术助手。",
  "messages": [
    {
      "role": "user",
      "content": "比较 Chat Completions 和 Responses。"
    }
  ]
}
```

典型响应形态：

```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "……"
    }
  ],
  "model": "claude-model",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 100,
    "output_tokens": 200
  }
}
```

## 3.1 与 OpenAI Chat Completions 的关键差异

| 维度 | OpenAI Chat Completions | Anthropic Messages |
|---|---|---|
| 顶层系统指令 | system / developer message 可在 `messages[]` 中 | 常用独立顶层 `system` 字段 |
| assistant 输出 | `choices[].message` | 顶层单个 `Message` |
| 内容形态 | 常见为字符串，也可为内容部分 | 典型为 `content[]` block 数组 |
| 结束原因 | `finish_reason` | `stop_reason` |
| 工具调用 | `tool_calls[]` | `content[]` 中的 `tool_use` block |
| 工具结果回传 | `role: "tool"` + `tool_call_id` | 通常由 `user` message 中的 `tool_result` block 回传 |
| 多轮工具协议 | message/tool message 交替 | tool use / tool result 内容块闭环 |
| max token 参数 | 历史上可选/模型相关 | 通常是显式重要参数 |

### 重要区别：Anthropic 的工具结果通常仍在 user content 中

Anthropic 风格的工具请求：

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_01",
      "name": "get_weather",
      "input": {
        "city": "Shanghai"
      }
    }
  ]
}
```

工具执行结果通常这样回传：

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01",
      "content": "{\"temperature_c\":25}"
    }
  ]
}
```

这与 OpenAI 的：

```json
{
  "role": "tool",
  "tool_call_id": "call_01",
  "content": "{\"temperature_c\":25}"
}
```

存在根本不同。若适配层只做字段重命名而没有转换**消息拓扑**，工具对话很容易失效。

## 3.2 Anthropic 的内容块心智模型

与“一个 message 基本等于一段文本”相比，Anthropic 更强调：

$$
\text{Message} = [\text{Content Block}_1, \text{Content Block}_2, \ldots]
$$

这些块可能是：

- `text`
- `image`
- `document`
- `tool_use`
- `tool_result`
- 其他模型或功能相关块

这使得一个 assistant turn 可以包含多个不同类别的输出，例如先给解释，再给工具调用；也使多模态和工具调用不必被挤进一个字符串字段。

### 设计启示

如果业务层只存：

```ts
{ role: "assistant", content: string }
```

那么它最终会丢失：

- 工具调用 ID
- 工具名称与参数
- 一个回合中多个内容块的顺序
- 图像、文档、引用或其他非文本块
- 停止原因与执行状态
- 需要回放 agent 轨迹时的关键语义

因此，更适合的内部表示是“回合 + 有序内容块”，而不是“role + string”。

***

## 4. Google Gemini：Content / Part 与候选响应

Google Gemini 的 generateContent API 使用不同的命名体系：

```json
POST /v1beta/models/{model}:generateContent

{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "解释不同 LLM API 协议。"
        }
      ]
    }
  ]
}
```

官方将其核心对象定义为：

- `Content`：一个对话回合的容器
- `Part`：一个回合中的数据单元，例如文本、图像、视频 URI 等
- `contents[]`：整个对话历史的回合列表。[3]

响应通常具有 candidate 结构：

```json
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "……"
          }
        ]
      },
      "finishReason": "STOP",
      "safetyRatings": []
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 100,
    "candidatesTokenCount": 200,
    "totalTokenCount": 300
  }
}
```

## 4.1 Gemini 与 Chat Completions 的映射

| 语义 | OpenAI Chat Completions | Gemini generateContent |
|---|---|---|
| 会话历史 | `messages[]` | `contents[]` |
| 一轮消息 | `message` | `Content` |
| 一轮内的多模态元素 | content parts / 扩展字段 | `parts[]` |
| 用户角色 | `user` | 通常为 `user` |
| 模型角色 | `assistant` | 常见为 `model` |
| 模型结果 | `choices[]` | `candidates[]` |
| 文本输出 | `choices[0].message.content` | `candidates[0].content.parts[].text` |
| 停止原因 | `finish_reason` | `finishReason` |
| 用量 | `usage` | `usageMetadata` |

Gemini 的 `generateContent` 为完整响应接口，`streamGenerateContent` 则通过 SSE 流式推送生成片段；二者请求体结构相同。[3][7]

## 4.2 Gemini 的 protocol 特征

### 以原生多模态为中心

Gemini 中的 `Part` 是基本多模态单元。文字、内联二进制数据、文件引用、视频 URI、函数调用等概念更自然地被放进 parts。

这与“先有文本 chat 协议，再逐步往 message 加 image/audio/tool 字段”的路线不同。

### 返回候选而不是单一 message

OpenAI 的传统接口也有 `choices[]`，但许多业务代码默认只取第一项。Gemini 的 `candidates[]` 提醒开发者：一个请求可能有多个候选，且候选会附带自己的结束原因、安全相关信息及 content。

### 角色不完全对等

OpenAI/Anthropic 常见模型输出角色为 `assistant`，Gemini 常见为 `model`。若把会话历史从 OpenAI 原样迁移到 Gemini，需要转换角色名；更重要的是，需要确认每个 SDK、每个模型版本及功能模式中可接受的角色范围，而不能只替换字符串。

### 系统指令不应强行伪装为一条 user message

Gemini 体系通常有独立的 system instruction 配置概念。虽然某些兼容层接受 system message，但原生协议中应按它要求的 system-instruction 机制传递，而不是假定其一定和 OpenAI 的 `role: "system"` 完全相同。

***

## 5. DeepSeek、智谱等：什么叫“OpenAI 兼容”

“兼容 OpenAI”最好拆成四个层级，而不是当作 yes/no 属性。

| 兼容层级 | 说明 | 常见情况 |
|---|---|---|
| URL 与鉴权兼容 | 可用类似 `/chat/completions`、Bearer Key | 最容易做到 |
| 基础请求兼容 | `model`、`messages`、`temperature`、`stream` 可用 | 多数供应商覆盖 |
| 基础响应兼容 | `choices[0].message.content` 可读取 | 多数供应商覆盖 |
| 语义与能力兼容 | tools、JSON Schema、vision、reasoning、流式事件、usage、状态等行为一致 | 最容易出现差异 |

一个服务能够让你这样写：

```python
client = OpenAI(
    api_key="...",
    base_url="https://vendor.example.com/v1"
)
```

只说明它可能提供 OpenAI 风格入口；它不代表所有 OpenAI 参数、对象、事件和能力都可无改动迁移。

## 5.1 DeepSeek：同时提供 Chat Completions 和 Responses 兼容面

DeepSeek 官方说明其 API 可以使用 OpenAI/Anthropic 风格，文档中的基础示例采用 OpenAI Chat Completions 形式：`/chat/completions`、`model`、`messages`、`stream` 等。[8]

其 Chat Completions 文档描述：

- 非流式响应是 `chat completion object`
- 对象类型为 `chat.completion`
- 生成内容在 `message.content`
- 流式采用 SSE，最后以 `data: [DONE]` 结束
- `response_format: {"type":"json_object"}` 可启用 JSON 输出。[9]

但重要的是，DeepSeek 的 JSON mode 并不等价于任意厂商的严格 schema structured output：其文档要求在 system 或 user prompt 中包含“json”字样，并建议显式给出目标 JSON 示例，同时提醒该模式可能偶发空内容。[10]

这意味着：

- 你不能只看参数名相同。
- 需要把“合法 JSON”与“严格符合给定 JSON Schema”分开测试。
- 应将 JSON 解析、schema 校验和重试策略放在应用层。

DeepSeek 还提供了对 OpenAI Responses 格式的兼容支持。其文档说明返回对象兼容 OpenAI Responses 的 `response` 结构，但不支持的能力会采用固定值，例如 `store: false`、`previous_response_id: null`、`parallel_tool_calls: true`；同时 usage 使用 `input_tokens`、`output_tokens` 等字段，并在明细中包含缓存命中与 reasoning token 相关信息。[11]

这正是一个典型案例：**对象轮廓兼容，不代表状态行为、能力集和默认值完全相同。**

### DeepSeek 特别需要验证的点

- `thinking`、`reasoning_effort` 等推理控制参数是否适用于选定模型。
- reasoning 内容是否返回、以什么字段返回、是否允许持久化或回放。
- 结构化输出究竟是 JSON mode 还是严格 JSON Schema。
- tool calling 是否支持并行调用、参数格式和流式 delta 格式如何。
- Responses 兼容接口中，哪些字段为固定占位值。
- 缓存 token、推理 token 与标准 input/output token 的计费及 observability 含义。

## 5.2 智谱 GLM / Z.AI：基础 Chat Completions 兼容不等于全协议复制

智谱 Z.AI 的快速开始示例使用：

```text
POST https://api.z.ai/api/paas/v4/chat/completions
```

并采用标准的 `model`、`messages[]`、`role`、`content` 结构。[12]

例如：

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

从接入体验看，它接近 OpenAI Chat Completions：大量既有 SDK 调用代码可以较容易复用。但实际集成仍要逐项确认：

- 支持哪些 roles：`system`、`developer`、`user`、`assistant`、`tool` 是否均可用。
- 支持 `content` 字符串还是也支持 content parts。
- 支持哪些 tool/function schema 方言。
- 是否支持 `response_format`、JSON Schema 或仅 JSON object。
- 流式 SSE 的 event/data 格式是否可被现有解析器直接消费。
- response 中的 `usage` 字段含义、token 口径与缓存 token 是否一致。
- 模型的 reasoning / thinking 输出如何配置与返回。
- 多模态输入使用何种字段；不要假设它与 OpenAI、Anthropic 或 Gemini 的字段一致。

智谱此类“OpenAI 风格”的接口最适合通过兼容 provider 快速接入，但在生产环境仍应使用其对应模型与能力的官方文档进行契约测试。快速开始文档只能证明基础聊天路径，不能证明完整功能矩阵。[12]

***

## 6. 核心 Taxonomy：按协议维度而不是厂商维度比较

仅按厂商列字段表，容易越写越碎。更实用的分类是把 API 协议拆为九个维度。

## 6.1 维度一：会话输入模型

| 类型 | 协议 | 抽象 | 对应用开发的含义 |
|---|---|---|---|
| 线性消息列表 | Chat Completions | `messages[]` | 最容易实现，但复杂过程会被压缩成消息附属字段 |
| 独立 system + 消息列表 | Anthropic Messages | `system` + `messages[]` | 指令与会话历史区分更明确 |
| 回合 + 内容片段 | Gemini | `contents[]` → `parts[]` | 多模态是原生概念 |
| 通用 item 列表 | OpenAI Responses | `input[]` typed items | 可表达消息、文件、工具结果、旧输出等多类事件 |

### 建议的内部抽象

不要把内部模型绑死为某厂商的 JSON。可采用：

```ts
type Turn = {
  role: "system" | "developer" | "user" | "assistant" | "tool";
  blocks: ContentBlock[];
  metadata?: Record<string, unknown>;
};

type ContentBlock =
  | { type: "text"; text: string }
  | { type: "image_url"; url: string }
  | { type: "file"; fileId?: string; mimeType?: string; data?: string }
  | { type: "tool_call"; id: string; name: string; arguments: unknown }
  | { type: "tool_result"; toolCallId: string; result: unknown }
  | { type: "reasoning"; summary?: string }
  | { type: "refusal"; text: string };
```

然后针对供应商做 adapter：

```text
Internal Conversation
    ├── OpenAI Chat adapter
    ├── OpenAI Responses adapter
    ├── Anthropic adapter
    ├── Gemini adapter
    └── Vendor-compatible adapter
```

关键是：**内部模型应保留信息，adapter 才负责降级。**  
反过来，如果内部模型只有 `role + string`，以后无论接 Anthropic、Gemini、Responses 还是 agent 框架，都会被迫丢信息。

***

## 6.2 维度二：角色与指令优先级

| 角色 / 概念 | OpenAI Chat | OpenAI Responses | Anthropic Messages | Gemini |
|---|---|---|---|---|
| 系统指令 | `system`，或 `developer` | `instructions`，也可有带 role 的 input item | 顶层 `system` | 通常为独立 system instruction 概念 |
| 开发者指令 | 常见 `developer` role | 支持 developer/system 的指令层级 | 不应假定有直接一一对应 role | 不应假定有直接一一对应 role |
| 终端用户 | `user` | `user` input message | `user` | `user` |
| 模型 | `assistant` | output message 的 `assistant` | `assistant` | `model` |
| 工具结果 | `tool` role | `function_call_output` item | `tool_result` content block，通常随 user message 传回 | function response 相关 part / 原生调用结构 |

OpenAI Responses 文档明确表示：developer 或 system role 的指令优先级高于 user role；assistant role 消息通常被视为模型先前生成的内容。[13]

### 不要做的映射

不要简单地把：

```json
{ "role": "developer", "content": "..." }
```

映射成：

```json
{ "role": "user", "content": "..." }
```

因为这会改变模型对指令来源与权重的理解。正确做法是：

- 若目标协议有原生 system/developer 机制，映射到该机制。
- 若目标协议没有等价层级，记录降级警告，并在 prompt 模板中采取明确分隔。
- 对安全关键规则、产品政策和工具约束，不要因兼容层限制而静默降级。

***

## 6.3 维度三：内容表示与多模态

| 形式 | 示例 | 优点 | 迁移风险 |
|---|---|---|---|
| 纯字符串 | `"content": "hello"` | 简单 | 无法携带图像、文件、多个块、工具调用等 |
| content parts | `content: [{type, ...}]` | 能逐步扩展多模态 | 各厂商 part type 名称不同 |
| `Content.parts[]` | Gemini `contents[].parts[]` | 多模态原生 | role、文件引用、函数调用格式不同 |
| typed items | Responses `input[]` / `output[]` | 支持复杂 agent 事件 | 不能再只取一个 content 字段 |

Google Gemini 将 `Content` 定义为一个对话回合，将 `Part` 定义为该回合中的数据片段；一个 `Content` 中可以放置多个 `Part`，用于组合文本、图像和视频 URI 等不同输入。[3]

### 实际建议

对多模态接口，至少分别测试：

- 文本 + 图片是否可以在同一用户回合传递。
- 多图片的顺序是否保留。
- 图像支持 URL、base64、file ID 还是 provider-specific upload handle。
- 文档、PDF、音频、视频是否走同一个 content 类型。
- 输出是文本、图像、音频还是混合内容块。
- token usage 是否包含图像 / 音频 / 文件处理成本。
- 兼容层是否仅“接受字段”但实质忽略某种模态。

***

## 6.4 维度四：工具调用协议

工具调用是各协议分化最明显的地方之一。

| 阶段 | OpenAI Chat | OpenAI Responses | Anthropic | Gemini |
|---|---|---|---|---|
| 工具声明 | `tools[]` | `tools[]`，可含自定义与内建工具 | `tools[]` | `tools` / function declarations |
| 模型请求调用 | `assistant.tool_calls[]` | `function_call` output item | `tool_use` content block | `functionCall` part 等原生结构 |
| 调用标识 | `id` / `tool_call_id` | `call_id` | `id` / `tool_use_id` | call ID 机制依实现 |
| 参数载体 | 常见 JSON 字符串 `arguments` | function call arguments | 常见对象 `input` | 常见结构化 args |
| 工具结果回传 | `role: "tool"` | `function_call_output` input item | `tool_result` block | `functionResponse` 等 part |
| 继续生成 | 再发一次聊天请求 | 使用 response 关联或继续 input | 将 tool result 加入后继续 | 将 function response 加入 contents 后继续 |

### 工具调用 adapter 的最低要求

一个可靠 adapter 不能只转换字段名，必须完整转换：

1. 工具名称。
2. JSON Schema / 参数定义。
3. 调用 ID。
4. 参数字符串与对象之间的序列化。
5. 工具结果的 MIME / 文本 / JSON 表达。
6. 一个回合中多个工具调用的顺序。
7. 并行调用语义。
8. 模型要求工具调用、禁止调用或自动选择工具的控制字段。
9. 工具执行异常、超时、权限失败和重试的回传格式。
10. 流式过程中函数参数的增量拼接方式。

### 一个常见失败模式

错误流程：

```text
模型要求调用 get_weather
→ 应用执行完成
→ 把结果作为普通 user 文本文字发回
→ 模型无法可靠地把结果和刚才的调用关联
```

正确流程：

```text
模型工具调用（带 call ID）
→ 应用执行
→ 用目标协议指定的 tool-result 结构回传相同 ID
→ 模型继续生成
```

工具调用的真正协议核心不是函数名，而是**调用与结果之间的可验证关联 ID**。

***

## 6.5 维度五：结构化输出

“让模型输出 JSON”至少有四种不同强度：

| 层级 | 目标 | 常见方式 | 风险 |
|---|---|---|---|
| Prompt JSON | 提示模型“请输出 JSON” | 文本提示 | 最弱，可能夹杂解释、Markdown 或无效 JSON |
| JSON mode | 保证可解析 JSON | `response_format: {"type":"json_object"}` 等 | 结构仍可能不符合业务 schema |
| JSON Schema / Structured Outputs | 满足指定 schema | `json_schema` / provider schema | 支持模型与兼容层差异大 |
| Tool / Function schema | 让模型生成调用参数 | 工具参数 JSON Schema | 输出通常结构更稳定，但语义仍需校验 |

OpenAI 的 Chat Completions 文档区分了 `json_object` 与 `json_schema`：后者用于 Structured Outputs，使模型匹配提供的 JSON Schema。[5]

DeepSeek 文档中的 JSON Output 则要求使用 `response_format: {"type":"json_object"}`，并要求 prompt 中包含“json”及输出样例，同时提醒可能出现空 content。[10]

### 生产建议

即使供应商宣称严格结构化输出，也应：

- 使用 JSON parser，而不是正则。
- 使用 JSON Schema、Pydantic、Zod、Ajv 或等价工具做业务校验。
- 区分“格式正确”与“业务语义正确”。
- 对必填字段、枚举、数值边界、日期格式做二次验证。
- 对截断输出、空结果、拒答、工具调用替代文本输出建立分支。
- 保留原始响应，以便排查 schema 漂移。

***

## 6.6 维度六：流式协议

主流 LLM API 多数使用 SSE，但“SSE”只说明传输机制，不说明事件语义一致。

| 维度 | 常见 Chat Completions | Responses | Anthropic Messages | Gemini |
|---|---|---|---|---|
| 传输 | SSE | SSE | SSE | SSE |
| 文本增量 | `choices[].delta.content` | 事件化 output text delta | content block delta | candidate/content part chunk |
| 工具参数 | 常为增量 `arguments` 字符串 | 函数调用相关事件 | tool-use input JSON delta | function call part / chunk |
| 结束 | `[DONE]` 或终止 chunk | completion / done 类型事件 | message stop / event sequence | stream 完成事件 |
| 解析难点 | 合并 delta | 按 item / event 类型做状态机 | 按 block 索引与事件组合 | 合并 candidates 与 parts |

DeepSeek 的 Chat Completions 文档说明，流式模式会作为 data-only SSE 返回部分 message delta，最终以 `data: [DONE]` 结束。  Gemini 的 `streamGenerateContent` 也使用 SSE，但它与 `generateContent` 虽共享请求体，响应是按生成片段推送的。[3][7][9]

### 流式实现建议：不要只拼接文本

最低限度应维护：

```ts
type StreamAccumulator = {
  text: string;
  toolCalls: Map<string, {
    id: string;
    name?: string;
    argumentsJsonText: string;
  }>;
  blocks: ContentBlock[];
  finishReason?: string;
  usage?: unknown;
};
```

原因是流中可能出现：

- 文本 delta
- function name delta
- JSON arguments delta
- reasoning delta
- tool call completed
- usage / rate-limit metadata
- refusal / safety stop
- 完成状态

如果只做：

```ts
fullText += chunk.delta.content ?? "";
```

那么在进入 tools、reasoning、多模态或 structured output 后就会失效。

***

## 6.7 维度七：状态与上下文

| 模式 | 代表 | 谁保存历史 | 优点 | 风险 |
|---|---|---|---|---|
| 无状态请求 | Chat Completions、Anthropic、Gemini 常见方式 | 应用 | 可控、易迁移、隐私边界明确 | 每轮需重传或自建裁剪 |
| response 链接 | Responses | API / 客户端共同维护 | 适合复杂多步骤执行 | 需理解 response 生命周期与存储行为 |
| conversation 容器 | Responses 等 | 服务端会话对象 | 减少手工拼历史 | 迁移、审计与数据保留需额外设计 |

OpenAI Responses 文档说明，可把一个 response 归入 conversation；该 conversation 的历史 items 会在后续请求前置，并且本次 input/output items 会在完成后自动加入 conversation。[6]

### 选择建议

**选择无状态历史重传**，如果你重视：

- 多供应商切换。
- 自己控制上下文截断。
- 强数据隔离或可审计要求。
- 离线回放、测试和缓存。
- 将模型调用视为纯函数。

**选择 provider-managed state**，如果你重视：

- 快速构建多步 agent。
- 减少传输与本地拼接复杂度。
- 原生工具、文件、推理项目之间的关联。
- 对单一供应商形成更深的能力集成。

一个成熟系统常常同时支持两种模式：业务层保存 canonical transcript；在特定 provider 上可额外维护 provider response / conversation ID，以获得原生能力。

***

## 6.8 维度八：用量、缓存与推理 token

不同协议的 usage 字段不能简单相加比较。

| 概念 | 常见字段示例 | 说明 |
|---|---|---|
| 输入 token | `prompt_tokens` / `input_tokens` | 用户消息、系统提示、历史、文件等的处理量 |
| 输出 token | `completion_tokens` / `output_tokens` | 可见文本或全部生成消耗，口径需确认 |
| 推理 token | `reasoning_tokens` 或 provider-specific | 内部推理相关用量，未必等于用户可见内容 |
| 缓存命中 token | `cached_tokens` | 输入中可能按缓存优惠或不同规则计费 |
| 总 token | `total_tokens` | 不同厂商是否包含 reasoning / cache 明细并不一致 |
| 候选 token | Gemini `candidatesTokenCount` 等 | 候选响应维度下的用量口径 |

DeepSeek 的 Responses 兼容说明指出，其 usage 中包含 `input_tokens`、`output_tokens`，并可在明细中返回 context cache 命中 token 与 reasoning token。[11]

### 监控时应记录什么

不要仅记录 `total_tokens`。至少记录：

- provider、endpoint、model、model revision。
- 请求与响应 ID。
- 输入、输出、推理、缓存 token 的原始 usage 字段。
- TTFT（time to first token）。
- 总延迟。
- 工具调用次数和每次工具延迟。
- 成功、拒答、限流、超时、JSON 失败、schema 失败等结果类型。
- 是否使用流式、是否命中缓存、是否使用文件或多模态输入。

***

## 6.9 维度九：错误、拒答与停止原因

不同协议返回的“模型没有给普通文本”的原因可能包括：

- 正常停止。
- 输出达到长度限制。
- 内容安全拦截。
- 供应商策略拒答。
- 工具调用结束，等待应用回传。
- JSON / schema 生成失败。
- 上下文窗口超限。
- 速率限制或配额耗尽。
- 服务器超时。
- 流中断。
- 模型侧临时故障。

因此，业务代码不能把“HTTP 200”当成“任务成功”，也不能把 `content == null` 当成一个可忽略的空字符串。

推荐的成功条件是：

```text
HTTP transport success
AND provider response parsed
AND terminal state is expected
AND required output type exists
AND structured payload validates
AND business constraints validate
```

***

## 7. 厂商之间的实用对比

## 7.1 最小文本对话

### OpenAI Chat Completions / 兼容服务

```json
{
  "model": "model-name",
  "messages": [
    {
      "role": "system",
      "content": "你是助手。"
    },
    {
      "role": "user",
      "content": "你好"
    }
  ]
}
```

### OpenAI Responses

```json
{
  "model": "model-name",
  "instructions": "你是助手。",
  "input": "你好"
}
```

### Anthropic Messages

```json
{
  "model": "model-name",
  "max_tokens": 512,
  "system": "你是助手。",
  "messages": [
    {
      "role": "user",
      "content": "你好"
    }
  ]
}
```

### Gemini generateContent

```json
{
  "systemInstruction": {
    "parts": [
      {
        "text": "你是助手。"
      }
    ]
  },
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "你好"
        }
      ]
    }
  ]
}
```

## 7.2 文本响应读取位置

| 协议 | 不建议硬编码的旧习惯 | 更稳妥的读取方式 |
|---|---|---|
| Chat Completions | 假设永远只有 `choices[0].message.content` | 检查 choices、message、content、tool calls、finish reason |
| Responses | 假设 `output[0]` 永远是文本 | 遍历 `output[]` 并按 item type 处理 |
| Anthropic | 假设 `content[0].text` 永远存在 | 遍历全部 content blocks，分别处理 text / tool_use 等 |
| Gemini | 假设 `candidates[0].content.parts[0].text` 永远存在 | 检查 candidates、finish reason、安全结果与全部 parts |

***

## 8. 推荐的应用架构：Canonical IR + Provider Adapter

如果产品只接一个模型、只做简单文本问答，直接使用官方 SDK 是最省心的选择。

如果产品需要以下任一能力：

- 同时接 OpenAI、Anthropic、Gemini、DeepSeek、GLM 或模型网关。
- 根据成本、区域、能力和健康状态切模型。
- 支持工具调用、RAG、多模态、结构化输出或 agent。
- 长期保留会话、审计轨迹、回放与评测。
- 避免业务逻辑被单一 provider response shape 污染。

那么建议采用三层架构。

```text
业务层
  ↓
Canonical LLM Interface
  ↓
Provider Adapter Layer
  ├── OpenAI Chat Completions Adapter
  ├── OpenAI Responses Adapter
  ├── Anthropic Messages Adapter
  ├── Gemini generateContent Adapter
  ├── DeepSeek Adapter
  └── Zhipu / GLM Adapter
  ↓
Provider SDK / HTTP API
```

## 8.1 Canonical 请求模型

```ts
type GenerateRequest = {
  model: {
    provider: string;
    name: string;
  };
  instructions?: string;
  turns: Turn[];
  tools?: ToolDefinition[];
  toolChoice?: "auto" | "none" | "required" | { name: string };
  responseSchema?: object;
  generation?: {
    temperature?: number;
    topP?: number;
    maxOutputTokens?: number;
    stopSequences?: string[];
  };
  stream?: boolean;
  metadata?: Record<string, string>;
};
```

## 8.2 Canonical 响应模型

```ts
type GenerateResult = {
  id: string;
  status: "completed" | "requires_tool_result" | "refused" | "incomplete" | "failed";
  blocks: ContentBlock[];
  finishReason?: string;
  usage?: {
    inputTokens?: number;
    outputTokens?: number;
    reasoningTokens?: number;
    cachedInputTokens?: number;
    raw?: unknown;
  };
  providerMetadata?: Record<string, unknown>;
};
```

### 关键原则

- 不要强制所有 provider 都假装支持全部能力。
- adapter 应明确返回 capability error 或 degradation warning。
- 将 provider-specific raw response 作为诊断信息保存。
- 把“模型能力判断”做成显式 capability registry，而不是 if/else 散落在业务代码中。

例如：

```ts
type Capabilities = {
  text: boolean;
  imageInput: boolean;
  audioInput: boolean;
  fileInput: boolean;
  toolCalling: boolean;
  parallelToolCalls: boolean;
  jsonMode: boolean;
  jsonSchema: boolean;
  streaming: boolean;
  reasoningControls: boolean;
  managedConversation: boolean;
};
```

***

## 9. 迁移与适配检查表

## 9.1 从 OpenAI Chat Completions 迁往 Responses

- 将 `messages[]` 映射为 `input` 或 typed input items。
- 将 system/developer 指令评估为 `instructions` 或保留为 message items。
- 将 `choices[].message` 的读取逻辑改为遍历 `output[]`。
- 将 `tool_calls` 迁移为 `function_call` output items。
- 将 `role: "tool"` 结果迁移为 `function_call_output` input items。
- 决定使用 `previous_response_id`、conversation，还是仍由应用管理完整历史。
- 重写 SSE 解析器，按 event / item 类型建立状态机。
- 测试 output 中含 text、function call、reasoning、拒绝、内建工具时的分支。
- 重新核对 usage 字段、缓存和推理 token 的成本口径。

OpenAI 官方迁移文档明确给出了核心映射：Chat Completions 的 `messages[]` 对应 Responses 的 `input`；工具调用对应 `function_call` output item；工具结果对应以 `call_id` 关联的 `function_call_output` input item。[1]

## 9.2 从 OpenAI Chat Completions 迁往 Anthropic

- 将 system / developer 指令转换到顶层 `system`，并明确 developer 语义是否发生降级。
- 将 `content: string` 改造为可支持 content block 数组。
- 将 OpenAI `tool_calls` 转成 Anthropic `tool_use`。
- 将 OpenAI `tool` role 结果转成 user message 内的 `tool_result` block。
- 将 `finish_reason` 映射为 `stop_reason`。
- 显式提供 Anthropic 所要求的生成长度控制参数。
- 将 assistant 历史中的复杂内容块完整保留，而不是只回填纯文本。

## 9.3 从 OpenAI Chat Completions 迁往 Gemini

- 把 `messages[]` 映射为 `contents[]`。
- 把每条消息内容映射为一个或多个 `parts[]`。
- 将 `assistant` role 转换为 `model` role。
- 使用 Gemini 原生 system instruction，而非盲目复用 system message。
- 将文本读取从 `choices[0].message.content` 改为 `candidates[].content.parts[]`。
- 对候选为空、安全结束、非文本 part、函数调用 part 建立处理逻辑。
- 测试多图、文件、视频等多模态输入的原生表现。

***

## 10. 最常见的误解

### 误解一：“OpenAI 兼容 = 可以直接替换 base URL”

不完全成立。它通常只保证基础 `chat.completions` 调用，实际仍要验证：

- 模型名。
- content part 结构。
- tool calling。
- streaming event shape。
- JSON mode / JSON Schema。
- reasoning 参数。
- usage。
- 错误码与限流 header。
- 图像、音频、文件。
- service-side state。

DeepSeek 就是一个很好的说明：它既支持 OpenAI 风格的 Chat Completions，也支持 Responses 格式，但其 Responses 兼容文档明确列出部分字段使用固定值，意味着它并非对所有 OpenAI 原生语义完全等价。[11]

### 误解二：“所有 message 都是 `{role, content: string}`”

这对简单对话够用，对 agent 与多模态不够用。Anthropic 的 message 是 content blocks；Gemini 的 turn 是 parts；Responses 的 output 是 typed items。[1][2][3]

### 误解三：“工具调用就是模型输出一段 JSON”

工具调用不仅是一段 JSON。它至少包括：

- 模型选择某个工具。
- 有唯一调用 ID。
- 参数符合工具 schema。
- 应用执行工具。
- 工具结果带相同关联 ID 回传。
- 模型基于结果继续执行或作答。

任何一个环节的协议转换错误，都可能导致模型重复调用、无法利用结果、参数不完整或会话失序。

### 误解四：“JSON mode 就是严格结构化输出”

不是。JSON mode 通常保障的是 JSON 可解析性；严格 JSON Schema 遵从则是更强能力。DeepSeek 的 JSON Output 文档还要求 prompt 中明确出现 JSON，并提示可能发生空 content，因此必须做应用层验证与重试。[10]

### 误解五：“流式都一样，照抄 SSE parser 就行”

SSE transport 相似，但每个 provider 的 delta、工具调用增量、停止事件、usage 出现时机和终止信号都可能不同。DeepSeek Chat Completions 使用 `[DONE]` 终止的 SSE 语义，而 Gemini 的 streaming 为其 generateContent 响应分块机制；不能假设二者 JSON payload 结构相同。[7][9]

### 误解六：“只要拿到 HTTP 200 就是成功”

HTTP 200 可能代表：

- 正常文本完成。
- 模型要求工具调用。
- 内容被拒绝或安全中断。
- 输出不完整。
- JSON 空内容。
- 流式连接成功但后续中断。
- 返回了非预期的多模态 / function block。

应用必须依据 provider 的完成状态、停止原因、内容类型和业务 schema 决定是否成功。

***

## 11. 选型建议

| 需求 | 优先考虑 | 原因 |
|---|---|---|
| 已有大量 OpenAI 生态代码，主要是文本聊天 | Chat Completions 兼容层 | 接入成本最低 |
| 需要原生 agent、内建工具、多类输出、复杂工作流 | OpenAI Responses | typed items 比 message-only 更适合表达执行过程 |
| 深度使用 Claude 与其原生工具、多块内容能力 | Anthropic Messages | 遵循其原生 block / tool-use 语义，减少兼容层损失 |
| 原生多模态、Content/Part 工作流 | Gemini generateContent | Part 模型对图像、文件等表达自然 |
| 希望可切换多家模型 | 自建 canonical IR + adapters | 避免业务代码绑定某个 JSON shape |
| 只想快速接入 DeepSeek、GLM 等 | OpenAI-compatible endpoint | 先走基础聊天；上线前逐项验证高级能力 |
| 需要可靠 JSON / 数据提取 | JSON Schema + 应用层校验 | 不依赖 prompt 或单一 JSON mode 承诺 |
| 需要生产级工具调用 | 原生工具协议 + 完整 call-ID 映射 | 避免将工具结果伪装成普通文本 |

***

## 12. 最终心智模型

可以把当代 LLM API 协议视为四次抽象升级：

$$
\text{Prompt String}
\rightarrow
\text{Chat Messages}
\rightarrow
\text{Multimodal Content Blocks}
\rightarrow
\text{Typed Agent Execution Items}
$$

对应地：

- **Prompt String**：最早的 completion 思路，输入文本，输出文本。
- **Chat Messages**：OpenAI Chat Completions 及其兼容生态，输入输出围绕对话角色组织。
- **Multimodal Content Blocks**：Anthropic content blocks 与 Gemini `Content` / `Part`，一条消息不再等于一段文字。
- **Typed Agent Execution Items**：OpenAI Responses 等，将文本、工具调用、工具结果、推理、文件和操作统一为可组合事件。

真正值得长期保存的不是某一家 API 的字段名，而是以下能力认知：

1. **文本不是唯一内容类型。**
2. **消息不是唯一事件类型。**
3. **工具调用不是普通文本，而是带身份关联的协议闭环。**
4. **“兼容”通常只覆盖一个能力子集。**
5. **流式的难点在事件状态机，不在 SSE 本身。**
6. **JSON 有效、schema 合格和业务正确是三件不同的事。**
7. **状态由应用管理还是 provider 管理，是架构决策，不是小参数。**
8. **多模型系统应使用 canonical IR 与 adapter，而不是在业务层散落供应商 JSON。**
9. **生产环境必须做 capability matrix、契约测试、错误分类、usage 观测和回归评测。**
10. **当你开始做 agent 时，优先关注 output item、tool call、tool result、状态和流事件，而不是只关注 `content`。**

OpenAI 的官方资料已将 Responses 描述为对 Chat Completions 的演进：前者将文本、图像、文件、内建工具与自定义工具调用整合到更通用的 response/item 模型中；而 Chat Completions 仍是广泛兼容的对话接口。  Anthropic 与 Gemini 则分别以内容块和 `Content`/`Part` 模型提出了不同的原生抽象。[1][2][3][6][14]

## Citations

1. [Migrate to the Responses API - OpenAI Developers](https://developers.openai.com/api/docs/guides/migrate-to-responses)
2. [Messages - Claude API Reference - Anthropic](https://platform.claude.com/docs/en/api/messages)
3. [Text generation - generateContent API](https://ai.google.dev/gemini-api/docs/generate-content/text-generation)
4. [Chat Completions Overview | OpenAI API Reference](https://developers.openai.com/api/reference/chat-completions/overview/)
5. [Create chat completion | OpenAI API Reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/)
6. [Create a model response | OpenAI API Reference](https://developers.openai.com/api/reference/resources/responses/methods/create/)
7. [Gemini API reference | Google AI for Developers](https://ai.google.dev/api)
8. [DeepSeek API Docs: Your First API Call](https://api-docs.deepseek.com/)
9. [Chat Completions API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-chat-completion/)
10. [JSON Output - DeepSeek API Docs](https://api-docs.deepseek.com/guides/json_mode/)
11. [Using the Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/guides/responses_api/)
12. [Quick Start - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/guides/overview/quick-start)
13. [Responses | OpenAI API Reference](https://developers.openai.com/api/reference/python/resources/responses/)
14. [Responses Overview | OpenAI API Reference](https://developers.openai.com/api/reference/responses/overview/)
15. [API overview - Claude Platform Docs - Anthropic](https://platform.claude.com/docs/en/api/overview)
16. [API Overview | OpenAI API Reference](https://developers.openai.com/api/reference/overview/)
17. [Inference using Anthropic Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-messages-api.html)
18. [Z.ai API Platform — Start building with GLM-5.3](https://z.ai/model-api)
19. [Anthropic Claude Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html)
20. [Getting started - generateContent API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/get-started)
21. [List input items | OpenAI API Reference](https://developers.openai.com/api/reference/resources/responses/subresources/input_items/methods/list/)
22. [Completions API - OpenAI Developers](https://developers.openai.com/api/docs/guides/completions)
23. [Text generation | OpenAI API](https://developers.openai.com/api/docs/guides/text)
24. [Specification - Open Responses](https://www.openresponses.org/specification)
25. [Missing API for retrieving outputs - OpenAI Developer Community](https://community.openai.com/t/missing-api-for-retrieving-outputs/1361134)
26. ["Responses" API endpoint - reference documentation errors and ...](https://community.openai.com/t/responses-api-endpoint-reference-documentation-errors-and-issues/1140994)
27. [Introducing the Responses API - OpenAI Developer Community](https://community.openai.com/t/introducing-the-responses-api/1140929)
28. [OpenAI Responses API.md - Github-Gist](https://gist.github.com/steipete/b58f0087c02fd97cea73f016e42c8ac0)
29. [Generating content | Gemini API | Google AI for Developers](https://ai.google.dev/api/generate-content)
30. [Grounding with Google Search - generateContent API](https://ai.google.dev/gemini-api/docs/generate-content/google-search)
31. [Use Code Execution](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start)
32. [Membuat konten dengan Gemini API di Vertex AI | Generative AI on Vertex AI | Google Cloud Documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference?authuser=2&hl=id)
33. [Generate content with the Gemini API | Gemini Enterprise Agent Platform | Google Cloud Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/inference?authuser=1)
34. [docs.claude.com](https://docs.claude.com/en/docs/intro.md)
35. [Claude Platform - Anthropic](https://claude.com/platform/api)
36. [Messages API | anthropics/anthropic-sdk-python | DeepWiki](https://deepwiki.com/anthropics/anthropic-sdk-python/5.1-messages-api)
37. [Z.AI (Zhipu AI) - LiteLLM](https://docs.litellm.ai/docs/providers/zai)
38. [Community Providers: Zhipu AI (Z.AI) - AI SDK](https://ai-sdk.dev/providers/community-providers/zhipu)
39. [Tool Calls | DeepSeek API Docs](https://api-docs.deepseek.com/guides/tool_calls/)
40. [Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-response/)
41. [GLM-5: From Vibe Coding to Agentic Engineering - Z.ai](https://z.ai/blog/glm-5)
42. [How to Use the GLM-4.6 API - Apidog](https://apidog.com/blog/glm-4-6-api/)
43. [Native Support for Z.AI (Zhipu AI) API & Latest GLM Models ... - GitHub](https://github.com/HKUDS/nanobot/issues/2?timeline_page=1)
44. [ZhipuAI API - 智谱AI](https://open.bigmodel.cn/dev/api)
45. [Glm 4.5 - AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/zhipu/glm-4.5)
