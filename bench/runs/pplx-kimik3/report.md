# LLM 时代 API 请求协议：从 Chat Completions 到 Responses、Messages 与 GenerateContent

LLM API 看似都在“发消息、拿回答”，但不同厂商对**会话历史、消息角色、多模态内容、工具调用、推理过程、流式事件和状态管理**的建模并不相同。最有效的认知方式不是记住每家字段，而是先建立一个稳定的协议 taxonomy：先识别 API 属于哪一种“交互原语”，再处理它的方言和能力差异。

本文以 OpenAI、Anthropic、Google Gemini、DeepSeek 为四个主要原生协议家族，并补充智谱（Z.AI/GLM）及其他“OpenAI 兼容”下游模型服务，说明请求与响应协议的关键区别、迁移风险和工程设计建议。OpenAI 当前建议新项目优先采用 Responses API；Chat Completions 仍受支持，但属于较早的接口模型。Gemini 的 GenerateContent 也仍可用，但 Google 已将 Interactions API 定为 2026 年 6 月起的新默认接口。[1][2][3]

***

## 1. 先建立 taxonomy：你到底在调用什么？

不要把所有模型 API 都称作“Chat API”。从协议抽象上，至少应区分以下五类：

| 协议范式 | 代表接口 | 核心输入 | 核心输出 | 会话状态如何保存 | 适合什么 |
|---|---|---|---|---|---|
| 传统聊天补全 | OpenAI Chat Completions、DeepSeek Chat Completions、很多兼容服务 | `messages` | `choices[].message` | 通常由客户端回传完整历史 | 普通问答、已有 OpenAI SDK 的快速接入 |
| 通用响应对象 | OpenAI Responses | `input` + `instructions` + 工具等 | `output[]`，带类型的 item | 可用 `previous_response_id` 链接响应 | Agent、工具调用、多模态、复杂工作流 |
| 单次“下一条消息” | Anthropic Messages | `system` + `messages` | 单个 message 对象及 `content[]` | 客户端通常维护与发送上下文 | Claude 原生能力、缓存、复杂工具流程 |
| 内容生成 | Google Gemini GenerateContent | `contents` + `systemInstruction` | `candidates[].content` | 一般由客户端发送历史 | 原生 Gemini 多模态、Google 工具生态 |
| 交互/事件对象 | Gemini Interactions、实时 API 等 | interaction / event 流 | 结构化事件或 interaction | 平台管理或基于 ID 延续 | 实时、Agent、长任务、复杂交互 |

真正的分界不是 URL 中是否出现 `chat`，而是：

1. **输入是 transcript，还是通用 item 列表？**
2. **输出是单一 assistant message，还是多种类型的事件/item？**
3. **服务端是否持久化会话或可通过 ID 续接？**
4. **工具调用是“嵌在消息里”，还是一等公民的输出 item？**
5. **文本、多模态、推理、引用、代码执行等是否有独立的 typed parts？**

***

## 2. 四个主流原生协议

### 2.1 OpenAI：Chat Completions 与 Responses 是两套思维模型

OpenAI 同时保留两种重要接口：

- **Chat Completions**：以 `messages` 为中心，是行业兼容层最常模仿的协议。
- **Responses**：以“通用输入与多类型输出”为中心，面向新一代 agent 与工具工作流。OpenAI 明确建议新文本生成项目优先使用 Responses API。[1][2][4]

#### Chat Completions 的心智模型

典型请求：

```json
{
  "model": "gpt-4.1",
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
  "temperature": 0.2
}
```

典型非流式响应：

```json
{
  "id": "chatcmpl_...",
  "object": "chat.completion",
  "created": 1750000000,
  "model": "gpt-4.1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "HTTP 流式响应是……"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "total_tokens": 150
  }
}
```

读取文本的经典路径是：

```ts
completion.choices[0].message.content
```

它的优点是简单、广泛兼容、生态成熟；其局限是：当输出不再只是“一条文本消息”，而可能同时包括推理项、函数调用、图像生成、检索结果、计算机操作等内容时，`choices[0].message` 会逐渐变成不够自然的容器。

#### Responses 的心智模型

Responses API 把输入和输出分离：

```json
{
  "model": "gpt-4.1",
  "instructions": "你是一个严谨的技术助手。",
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "解释 HTTP 流式响应。"
        }
      ]
    }
  ]
}
```

它不以 `choices[].message` 作为唯一输出入口，而是返回一个 response 对象及 `output[]`。其中可包含 message、reasoning、function call、function call output 等不同 item。[2]

```json
{
  "id": "resp_...",
  "object": "response",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "HTTP 流式响应是……"
        }
      ]
    }
  ]
}
```

对应读取方式更像：

```ts
response.output_text
// 或遍历 response.output 中 type === "message" 的 item
```

#### OpenAI 的关键差异

| 维度 | Chat Completions | Responses |
|---|---|---|
| 请求主字段 | `messages` | `input` |
| 指令字段 | 通常放在 `system` / `developer` message | 独立的 `instructions`，也可使用 input message |
| 输出主字段 | `choices[]` | `output[]` |
| 文本读取 | `choices[0].message.content` | `output_text` 或解析 `output[]` |
| 工具调用 | `tool_calls` 挂在 assistant message | `function_call` 等 typed item |
| 对话管理 | 客户端维护并回传 `messages` | 可使用 `previous_response_id` 续接 |
| 适配目标 | 传统聊天、兼容生态 | 新项目、Agent、多模态、复杂编排 |

OpenAI 的角色优先级也不能被误解为普通标签：当前文档将 `developer` 定位为应用开发者给出的指令，其优先级高于 `user`；`assistant` 则代表历史模型输出。[1][5]

***

### 2.2 Anthropic：Messages API，不等于 OpenAI 的 `messages`

Anthropic 的原生接口是：

```http
POST /v1/messages
```

它要求你发送结构化的输入消息，由模型生成会话中的下一条消息。[6][7]

典型请求：

```json
{
  "model": "claude-sonnet-4",
  "max_tokens": 1024,
  "system": "你是一个严谨的技术助手。",
  "messages": [
    {
      "role": "user",
      "content": "解释 HTTP 流式响应。"
    }
  ]
}
```

典型响应：

```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "HTTP 流式响应是……"
    }
  ],
  "model": "claude-sonnet-4",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  }
}
```

表面上它也有 `messages`，但不应简单视为 OpenAI Chat Completions 的同义替换。

#### Anthropic 的核心特征

**第一，`system` 通常是顶层字段，不是 `messages` 中的一个 role。**

OpenAI Chat Completions 常见形式是：

```json
{
  "messages": [
    { "role": "system", "content": "..." },
    { "role": "user", "content": "..." }
  ]
}
```

Anthropic 原生形式则是：

```json
{
  "system": "...",
  "messages": [
    { "role": "user", "content": "..." }
  ]
}
```

因此，一个“把 OpenAI messages 原样转发到 Claude”的适配器，至少要完成：

- 收集或合并 system instructions；
- 转移到 Anthropic 的顶层 `system`；
- 处理目标协议实际支持的角色集合；
- 将 OpenAI 的 tool message/tool call 语义转换为 Anthropic 的 tool-use 内容块与 tool-result 内容块。

**第二，`content` 从一开始就是 block 数组。**

Anthropic 常用：

```json
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "分析这张图片"
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
```

而 OpenAI 传统 Chat Completions 中，`content` 可能是字符串，也可能是兼容模型特定的数组结构。故不能假定所有厂商的 `content` JSON 形状一致。

**第三，返回的是一个 message，不是 choices 数组。**

这意味着通用解析器如果硬编码：

```ts
response.choices[0].message.content
```

面对原生 Anthropic 响应会直接失败。正确思路是根据协议 adapter 提供统一的内部抽象，例如：

```ts
normalized.text
normalized.toolCalls
normalized.finishReason
normalized.usage
```

而不是让业务代码直接理解每家原始字段。

***

### 2.3 Google Gemini：`contents`、`parts`、`candidates` 与 `generateContent`

Gemini 的经典内容生成接口是：

```http
POST /v1beta/models/{model}:generateContent
```

它接受 `GenerateContentRequest`，生成模型响应。Gemini 支持图像、音频、代码、工具等内容能力，但具体输入能力取决于模型。[8]

典型请求：

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
          "text": "解释 HTTP 流式响应。"
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.2
  }
}
```

典型响应形状：

```json
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "HTTP 流式响应是……"
          }
        ]
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 100,
    "candidatesTokenCount": 50,
    "totalTokenCount": 150
  }
}
```

#### Gemini 的几个重要语义

**角色名称通常是 `user` 与 `model`，而不是 `user` 与 `assistant`。**

因此，若你维护的是跨供应商对话历史，需要做映射：

| 内部规范角色 | OpenAI | Anthropic | Gemini |
|---|---|---|---|
| 平台/应用指令 | `developer` / `system` / `instructions` | 顶层 `system` | `systemInstruction` |
| 最终用户输入 | `user` | `user` | `user` |
| 历史模型输出 | `assistant` | `assistant` | `model` |
| 工具请求 | assistant `tool_calls` 或 Responses item | `tool_use` block | `functionCall` part |
| 工具结果 | `tool` message 或 function-call output item | `tool_result` block | `functionResponse` part |

**内容单位是 `parts`。**

Gemini 的一条 content 不是单一文本，而是由 parts 组成。文本只是 part 的一种形式。多模态输入、函数调用、函数响应及其他结构化内容，通常在 part 层表达。这一点和 Anthropic 的 content blocks 相似，但字段名和 JSON 结构不同。

**候选结果是 `candidates[]`。**

对 OpenAI 用户而言，`candidates[]` 可以类比为 `choices[]`，但不是完全同义。候选项中包含 `content.role = "model"` 与 `parts[]`，文本通常需要遍历并拼接 text parts，而非读取固定的 `message.content`。

**GenerateContent 仍支持，但不应假设它是 Google 的长期默认新接口。**

Google 文档显示，Gemini Interactions API 已在 2026 年 6 月成为默认方向；GenerateContent 被标为 legacy，但仍受支持。对于新系统，尤其是要构建 agent、状态化交互或长期维护的系统，需同时评估其 Interactions API，而不是只围绕 `generateContent` 建抽象。[3][9]

Gemini 也同时提供：

- `generateContent`：一次性返回完整结果；
- `streamGenerateContent`：使用 SSE 逐块推送；
- Live API：通过 WebSocket 实现双向、实时、状态化交互；
- Batch：批量异步生成。[10]

这说明“是否流式”不是一个简单的 `stream: true/false` 参数问题；不同 API 家族可能连传输方式都是不同的。

***

### 2.4 DeepSeek：高度 OpenAI 兼容，但“兼容”不代表“完全相同”

DeepSeek 的 Chat Completions API 使用：

```http
POST /chat/completions
```

其目标是对给定 chat conversation 生成响应。DeepSeek 官方也明确说明其 API 可按 OpenAI/Anthropic 兼容格式接入：可通过配置使用相应 SDK 或兼容软件，OpenAI 兼容入口使用 `https://api.deepseek.com`，Anthropic 兼容入口使用 `https://api.deepseek.com/anthropic`。[11][12]

典型 OpenAI 兼容请求：

```json
{
  "model": "deepseek-flash",
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
  "stream": false
}
```

但在实际工程中，DeepSeek 不能仅被理解为“换一个 `base_url`”。

#### DeepSeek 的关键协议差异

**1. 对话通常是无状态的。**

DeepSeek 文档明确指出，其 `/chat/completions` 为 stateless API：服务端不记录请求上下文；多轮对话时，客户端必须将完整历史拼接后在每次请求中传回。[13]

这意味着：

```text
第 1 轮：system + user_1
第 2 轮：system + user_1 + assistant_1 + user_2
第 3 轮：system + user_1 + assistant_1 + user_2 + assistant_2 + user_3
```

如果你的上游同时接 OpenAI Responses 的 `previous_response_id` 等服务端续接模式，就不能把它的状态管理假设照搬到 DeepSeek。

**2. 推理内容可能有专门字段。**

DeepSeek 文档说明：对于 thinking mode，assistant message 可包含位于最终回答之前的 reasoning content。它不是普通最终正文的一部分，需要你在 UI、日志、上下文回传和隐私策略中单独处理。[11]

工程上的正确原则是：

- 不要默认把 reasoning 字段直接展示给终端用户；
- 不要默认把 reasoning 字段原样回注到下一轮上下文；
- 不要把“最终可见答案”与“模型内部或中间推理字段”混在同一个业务字段中；
- 不同模型对 reasoning 字段的提供、稳定性、可回传性和计费语义均可能不同。

**3. 流式 usage 的出现时机可能不同。**

DeepSeek 在流式模式中支持 `stream_options.include_usage`：当该设置开启时，各 chunk 可能携带 `usage` 字段，但除最后一个 chunk 外其值可以为 `null`；未开启时，usage 字段可能仅在最后一个 chunk 中出现。[11]

所以流式消费者不要假设：

```ts
for await (const chunk of stream) {
  totalTokens += chunk.usage.total_tokens
}
```

更安全的做法是只在出现有效 usage 的最终事件或明确的 usage event 后记录费用与令牌数。

**4. 工具调用的增量结构有状态。**

DeepSeek 的工具调用流中，最初 chunk 带有 `id`、`type`、`function` 等标识，后续 chunk 往往只追加 function arguments。[11]

因此你需要按 tool call index 或 call ID 缓冲与合并参数增量，而不是将每个 stream chunk 当作可独立执行的 JSON 工具调用。

***

## 3. 请求协议横向对比

### 3.1 最小文本请求对比

| 厂商/协议 | 端点思路 | 模型字段 | 顶层指令 | 用户输入容器 | 模型输出角色 |
|---|---|---|---|---|---|
| OpenAI Chat Completions | `/v1/chat/completions` | `model` | `system`/`developer` message | `messages[]` | `assistant` |
| OpenAI Responses | `/v1/responses` | `model` | `instructions` | `input` | `assistant` message / typed output |
| Anthropic Messages | `/v1/messages` | `model` | `system` | `messages[]` | `assistant` |
| Gemini GenerateContent | `models/{model}:generateContent` | URL path 或 model resource | `systemInstruction` | `contents[]` | `model` |
| DeepSeek Chat Completions | `/chat/completions` | `model` | 通常是 `system` message | `messages[]` | `assistant` |
| 智谱/Z.AI Chat Completions | Chat Completion 接口 | `model` | 一般兼容 system message 语义 | `messages[]` | `assistant` |

Z.AI 的 Chat Completion 文档将 `messages` 定义为当前对话提示的 JSON 数组，示例为 `{"role":"user","content":"Hello"}`，并列出 system、user、assistant、tool 等消息类型；它还强调输入不能只由 system 或 assistant messages 构成。[14]

### 3.2 文本内容结构对比

| 协议 | 最简单文本写法 | 复杂内容表达 | 常见解析坑 |
|---|---|---|---|
| OpenAI Chat Completions | `content: "文本"` | 部分模型/API 使用 content parts | 以为 content 永远是 string |
| OpenAI Responses | `input: "文本"` 或 typed input item | `input_text`、图像、文件及其他 item | 以为输出总在 `choices[0]` |
| Anthropic Messages | `content: "文本"` | `content: [{type:"text", text:"..."}]` 及 block | 以为 response content 是 string |
| Gemini | `parts: [{text:"文本"}]` | `parts[]` 承载文本、多模态、工具内容 | 以为 text 在固定 `content` 字段 |
| DeepSeek | 多数情况下沿用 OpenAI 风格 | 模型特有的 reasoning / tool call 扩展 | 以为兼容意味着所有参数都生效 |
| 智谱/Z.AI | 多数情况下沿用 Chat Completions 风格 | 多模态、文件、工具等扩展 | 以为 OpenAI 客户端类型定义完全够用 |

### 3.3 响应提取对比

| 协议 | 常见最终文本位置 | 完成原因字段 | token 用量位置 |
|---|---|---|---|
| OpenAI Chat Completions | `choices[0].message.content` | `choices[0].finish_reason` | `usage` |
| OpenAI Responses | `output_text` 或解析 `output[]` | item / response 级状态 | response usage 相关字段 |
| Anthropic Messages | `content[]` 中 `type: "text"` 的 block | `stop_reason` | `usage.input_tokens`、`usage.output_tokens` |
| Gemini GenerateContent | `candidates[0].content.parts[]` 的 text | `candidates[0].finishReason` | `usageMetadata` |
| DeepSeek Chat Completions | 通常为 `choices[0].message.content` | `choices[0].finish_reason` | `usage`，流式需特别处理 |
| 智谱/Z.AI | 通常近似 OpenAI choices/message | 通常近似 `finish_reason` | 通常近似 `usage` |

***

## 4. `message`、`content` 与 role：最容易被低估的差异

### 4.1 `message` 不是跨厂商统一数据结构

以下四个 JSON 都表达“用户说：你好”，但并不可以无损互换：

```json
// OpenAI Chat Completions
{
  "role": "user",
  "content": "你好"
}
```

```json
// Anthropic
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "你好"
    }
  ]
}
```

```json
// Gemini
{
  "role": "user",
  "parts": [
    {
      "text": "你好"
    }
  ]
}
```

```json
// OpenAI Responses
{
  "role": "user",
  "content": [
    {
      "type": "input_text",
      "text": "你好"
    }
  ]
}
```

即使 SDK 帮你接受字符串简写，系统内部也不应该把这个简写当作底层规范。面向多模型系统时，推荐把消息统一成自己的 canonical representation，再由每个 provider adapter 完成降级或编译。

例如：

```ts
type CanonicalPart =
  | { type: "text"; text: string }
  | { type: "image_url"; url: string; mediaType?: string }
  | { type: "file"; fileId?: string; url?: string; data?: string }
  | { type: "tool_call"; id: string; name: string; argumentsJson: string }
  | { type: "tool_result"; toolCallId: string; result: unknown };

type CanonicalMessage = {
  role: "system" | "developer" | "user" | "assistant" | "tool";
  parts: CanonicalPart[];
  metadata?: Record<string, unknown>;
};
```

然后分别实现：

```text
CanonicalMessage[] -> OpenAI Chat Completions request
CanonicalMessage[] -> OpenAI Responses input
CanonicalMessage[] -> Anthropic Messages request
CanonicalMessage[] -> Gemini GenerateContent request
CanonicalMessage[] -> DeepSeek request
```

这比让上层业务直接拼 JSON 更稳定。

***

### 4.2 `system` 与 `developer` 不可简单等价

常见误区是把所有上游约束都塞进一条 system prompt。实际上，各厂商对“谁有更高指令优先级”的模型不同：

- OpenAI 明确区分 `developer`、`user`、`assistant`，并将 developer instructions 排在 user 之前；Responses 还提供独立的 `instructions` 参数。[1][5]
- Anthropic 常将系统级指令放在顶层 `system`。
- Gemini 使用 `systemInstruction`。
- OpenAI 兼容 API 往往接收 `system`，但并不表示其底层模型一定完全采用 OpenAI 的角色优先级或安全策略。

建议在你的业务模型中至少区分三类信息：

| 内部层级 | 示例 | 应放在哪里 |
|---|---|---|
| 平台不可覆盖政策 | 安全、合规、工具边界、数据隔离规则 | 平台/服务端固定层，不交给终端用户编辑 |
| 产品开发者指令 | 语气、任务目标、输出 schema、工具策略 | OpenAI developer/instructions、Anthropic system、Gemini systemInstruction 等 |
| 用户输入 | 问题、材料、偏好、临时要求 | user message/content |

不要让用户可控文本直接拼接进系统提示词；也不要将工具返回的外部内容当成等价的系统指令。

***

### 4.3 历史 assistant message 不是可有可无

在无状态 Chat Completions 风格 API 中，历史模型回复是上下文的一部分。DeepSeek 明确要求多轮调用时由客户端把先前模型输出与新用户问题一起拼接并重新发送。[13]

常见的正确历史序列：

```json
[
  {
    "role": "system",
    "content": "你是客服助手。"
  },
  {
    "role": "user",
    "content": "订单什么时候到？"
  },
  {
    "role": "assistant",
    "content": "请提供订单号。"
  },
  {
    "role": "user",
    "content": "A12345"
  }
]
```

如果漏掉 assistant 历史，模型会失去先前提问或承诺的语境；如果把 assistant 历史错误标成 user，模型可能把自己此前生成的文本误认为用户指令。

***

## 5. 工具调用：表面相似，执行循环不同

工具调用不是“模型帮你执行函数”。更准确地说，是一个由模型建议、应用执行、模型再读取结果的**协议闭环**：

1. 客户端声明可调用工具及其 JSON Schema。
2. 模型输出工具调用请求。
3. 应用验证、授权并实际执行工具。
4. 应用将结果以协议规定格式回传。
5. 模型根据结果生成最终答案，或者继续提出工具调用。

核心安全原则：**模型不能直接拥有你的数据库、支付、发信、删库或生产环境权限；工具执行层必须由你的应用控制。**

### 5.1 工具调用的结构映射

| 协议 | 模型要求调用工具 | 应用回传工具结果 |
|---|---|---|
| OpenAI Chat Completions | assistant message 的 `tool_calls[]` | role 为 `tool` 的 message，带 `tool_call_id` |
| OpenAI Responses | `function_call` output item | `function_call_output` input item |
| Anthropic Messages | `content[]` 中的 `tool_use` block | 后续 user content 中的 `tool_result` block |
| Gemini GenerateContent | content part 中的 `functionCall` | 下一轮 content part 中的 `functionResponse` |
| DeepSeek | 通常兼容 OpenAI 的 `tool_calls` | 通常兼容 tool message 回传 |
| 智谱/Z.AI | 通常支持 tool use / function calling | 具体结构依 SDK、模型及版本确认 |

### 5.2 一个跨协议工具调用的概念例子

假设定义工具：

```json
{
  "name": "get_weather",
  "description": "查询指定城市天气",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      }
    },
    "required": ["city"],
    "additionalProperties": false
  }
}
```

模型可能产生统一语义：

```text
调用 get_weather(city="上海")
```

但不要依赖统一 JSON：

- OpenAI Chat Completions 常在 `tool_calls[].function.arguments` 给出 JSON 字符串；
- Anthropic 会在 `tool_use` block 的 `input` 中给出对象；
- Gemini 以 function call part 表达；
- OpenAI Responses 中工具调用是独立 typed item。

因此，跨供应商工具层需要做两次转换：

```text
Provider 原始调用
    ↓
CanonicalToolCall { id, name, arguments }
    ↓
执行器：校验 JSON Schema、权限、幂等性、审计、超时控制
    ↓
CanonicalToolResult { callId, content, isError }
    ↓
Provider 所需的 tool-result / function-response 格式
```

### 5.3 工具调用不能忽略的工程问题

- **JSON 不可信**：函数参数必须 parse、schema validate、类型检查。
- **模型不可信**：模型请求调用不等于用户已授权调用。
- **工具输出也不可信**：网页、文档、CRM 字段可能包含提示注入内容。
- **必须设置超时与重试策略**：工具网络调用会失败。
- **幂等性必不可少**：流式重连或重复请求不应重复扣费、下单或发消息。
- **区分业务错误与模型错误**：例如 `customer_not_found` 应作为工具结果回传，不能只在服务端抛异常后丢失上下文。
- **不要过早执行流式增量 tool call**：DeepSeek 等流式接口中参数可能分段到达，必须等到完整、可验证的调用参数再执行。[11]

***

## 6. 流式协议：`stream: true` 只是开始

流式输出通常使用 SSE（Server-Sent Events），但事件命名、chunk 内容、结束标志、usage 发送方式和工具调用增量形态都不统一。

| 厂商/接口 | 常见传输方式 | 文本增量大致位置 | 结束方式 | 需要特别注意 |
|---|---|---|---|---|
| OpenAI Chat Completions | SSE | `choices[].delta.content` | `finish_reason` / `[DONE]` | role、文本、tool args 可能分不同 chunk 到达 |
| OpenAI Responses | SSE typed events | 依事件类型读取 text delta | response 完成事件 | 不能按 choices/delta 假设解析 |
| Anthropic Messages | SSE events | content block delta | message stop 等事件 | block start/delta/stop 的生命周期 |
| Gemini streamGenerateContent | SSE | candidates/content parts 增量 | 最终候选完成状态 | content parts 与候选状态需组合 |
| DeepSeek Chat Completions | SSE，近似 OpenAI | `choices[].delta` | 最终 chunk | usage 可仅在最后一个 chunk 有效；tool args 是增量 [11] |
| Gemini Live API | WebSocket | 双向事件 | session/event 生命周期 | 不是普通 HTTP SSE 流 [10] |

推荐的流式处理状态机：

```text
INIT
  -> RECEIVING_TEXT
  -> RECEIVING_TOOL_CALL
  -> TOOL_CALL_COMPLETE
  -> EXECUTING_TOOL
  -> SENDING_TOOL_RESULT
  -> RECEIVING_FOLLOW_UP
  -> COMPLETED / FAILED / CANCELLED
```

不要把流式处理写成“看到任何 chunk 就向页面 append 字符串”。更可靠的实现应分别累积：

```ts
type StreamAccumulator = {
  text: string;
  reasoning?: string;
  toolCalls: Map<string, {
    id: string;
    name?: string;
    argumentsJson: string;
  }>;
  usage?: {
    inputTokens?: number;
    outputTokens?: number;
    totalTokens?: number;
  };
  finishReason?: string;
};
```

***

## 7. “OpenAI 兼容”到底兼容什么？

许多国内外推理平台、模型托管平台、网关产品都宣称“OpenAI compatible”。这通常非常有价值：你可以复用 HTTP 客户端、鉴权方式、`model` 与 `messages` 基础结构，常常只需切换：

```ts
baseURL
apiKey
model
```

DeepSeek 官方明确支持按 OpenAI/Anthropic 兼容格式接入，智谱/Z.AI 的 Chat Completion 文档也采用了 `messages`、system/user/assistant/tool 等与 Chat Completions 接近的语义。[12][14]

但“兼容”应被视为一个**兼容层声明**，不是“行为完全一致”的保证。

### 7.1 常见兼容级别

| 兼容级别 | 含义 | 可以期待 | 不能默认期待 |
|---|---|---|---|
| URL/鉴权兼容 | Bearer token、近似 endpoint | SDK 能发出请求 | 参数与错误码完全相同 |
| 基础 Chat Completions 兼容 | `model` + `messages` + `choices` | 普通文本对话可迁移 | 多模态、JSON schema、logprobs、seed 等 |
| 流式兼容 | SSE 与 delta 结构近似 | 基础逐字输出 | tool call chunk 顺序、usage、结束事件完全一致 |
| 工具调用兼容 | tools/tool_calls 可用 | 简单 function calling | 多轮 tool state、并行调用、strict schema 行为 |
| 语义兼容 | 角色/参数效果大致相近 | 基础使用体验 | 相同 prompt 得到相同行为或同样安全边界 |
| 生命周期兼容 | 模型和版本策略稳定 | 短期可跑 | 模型别名、弃用期、默认模型长期稳定 |

### 7.2 DeepSeek 与 OpenAI 官方协议的典型不同

即便 DeepSeek 支持 OpenAI 风格调用，至少应注意：

- DeepSeek API 被文档描述为无状态，多轮历史需要由客户端显式拼接；而 OpenAI Responses 可以通过 `previous_response_id` 建立响应链。[2][13]
- DeepSeek 的 thinking mode 可能暴露 `reasoning_content` 等特定字段；OpenAI Responses 则将 reasoning 作为 typed output item 的一部分建模，二者不是相同结构。[2][11]
- DeepSeek 的 stream usage 行为、工具调用参数增量行为有专门约定，不能仅依赖通用 OpenAI SDK 的静态类型或旧版解析逻辑。[11]
- 参数名称即使相同，例如 `temperature`、`max_tokens`、`stream`、`tools`，其支持范围、默认值、约束和模型效果也可能不同。

### 7.3 智谱/GLM 对比 Anthropic：不要从 `messages` 名称推断协议相同

智谱/Z.AI 的 Chat Completion 接口强调 `messages` 消息数组，以及 system、user、assistant、tool 等角色，这更接近 OpenAI Chat Completions 的使用直觉。[14]

Anthropic 的 Messages API 虽然同样使用 `messages` 字段，但其原生设计有明显区别：

| 方面 | 智谱/Z.AI Chat Completion 风格 | Anthropic Messages 原生风格 |
|---|---|---|
| 系统指令 | 通常作为 system message 的兼容语义处理 | 顶层 `system` |
| 用户/助手消息 | `messages[]` 中按 role 表达 | `messages[]` 中按 role 表达 |
| 内容组织 | 常见为 OpenAI 风格 content，兼具多模态扩展 | 以 typed `content[]` blocks 为核心 |
| 工具调用 | 倾向 Chat Completions 的 tool calls 语义 | `tool_use` / `tool_result` blocks |
| 返回形态 | 通常近似 `choices[]` | 单个 message，`content[]` blocks |
| 迁移难点 | OpenAI adapter 多可复用但须测扩展 | 需专门处理 system、blocks、tool loop |

所以，把 GLM/Z.AI 接到一个面向 OpenAI Chat Completions 的应用中，通常可以先从兼容适配开始；但把同一应用切到 Anthropic 原生 API，通常应设计独立 adapter，而不是只改 host、model 与 API key。

***

## 8. 推荐的跨模型架构

如果你只调用一家厂商，直接用官方 SDK 和原生 API 通常是最低维护成本方案。只有在以下情况下，才值得引入统一抽象层：

- 需要在不同模型间做路由、回退或 A/B 测试；
- 同时使用 OpenAI、Claude、Gemini、DeepSeek、GLM 等；
- 需要统一工具调用、可观测性、计费和审计；
- 需要在模型供应商变更、模型下线或区域可用性变化时快速切换；
- 需要对不同模型实施同一套隐私、内容安全与数据保留策略。

### 8.1 推荐：语义统一，能力保留

不要选择两个极端：

- **极端 A：完全不用抽象。** 业务代码到处是 `choices[0].message.content`、`candidates[0]`、`content[0].text`，替换模型成本极高。
- **极端 B：过度抽象。** 强行把所有能力压成 `prompt -> string`，导致工具、图像、引用、推理、缓存、实时语音等原生能力全部丢失。

更好的结构是三层：

```text
业务层
  ├─ 任务定义：生成、摘要、抽取、客服、检索、Agent
  ├─ 输出契约：文本 / JSON / 工具调用 / 多模态结果
  └─ 策略：模型选择、预算、延迟、风险等级

统一语义层
  ├─ CanonicalMessage / CanonicalPart
  ├─ CanonicalToolDefinition / CanonicalToolCall / CanonicalToolResult
  ├─ NormalizedResponse / Usage / FinishReason
  └─ CapabilityProfile

Provider Adapter 层
  ├─ OpenAI Chat Completions adapter
  ├─ OpenAI Responses adapter
  ├─ Anthropic Messages adapter
  ├─ Gemini GenerateContent / Interactions adapter
  ├─ DeepSeek adapter
  └─ Z.AI / GLM adapter
```

### 8.2 不要统一掉 capability matrix

每种模型/API 建议显式维护能力矩阵：

```ts
type CapabilityProfile = {
  text: boolean;
  imageInput: boolean;
  audioInput: boolean;
  videoInput: boolean;
  fileInput: boolean;
  jsonMode: boolean;
  jsonSchema: boolean;
  toolCalling: boolean;
  parallelToolCalls: boolean;
  streaming: boolean;
  realtime: boolean;
  serverSideConversationState: boolean;
  promptCaching: boolean;
  reasoningOutput: "none" | "limited" | "provider_specific";
  batch: boolean;
};
```

模型路由不要只看“价格”和“最大上下文”。还要按任务检查：

- 是否支持所需输入模态；
- 是否支持严格结构化输出；
- 是否支持工具调用及并行工具调用；
- 是否支持流式与取消；
- 是否需要客户端完整回传历史；
- 是否会暴露或需要管理 reasoning 相关内容；
- 是否能满足数据驻留、审计、保留与合规要求；
- 模型别名和版本是否可锁定。

***

## 9. 最小可移植接口建议

以下接口不追求覆盖所有厂商特性，而是为上层业务提供稳定的最低公分母。

```ts
type Role = "system" | "developer" | "user" | "assistant" | "tool";

type Part =
  | { type: "text"; text: string }
  | { type: "image_url"; url: string }
  | { type: "file"; mimeType: string; data: string }
  | {
      type: "tool_call";
      id: string;
      name: string;
      argumentsJson: string;
    }
  | {
      type: "tool_result";
      toolCallId: string;
      content: string;
      isError?: boolean;
    };

type Message = {
  role: Role;
  parts: Part[];
};

type ToolDefinition = {
  name: string;
  description?: string;
  inputSchema: Record<string, unknown>;
};

type GenerateRequest = {
  model: string;
  instructions?: string;
  messages: Message[];
  tools?: ToolDefinition[];
  temperature?: number;
  maxOutputTokens?: number;
  stream?: boolean;
  responseFormat?: "text" | "json";
};

type GenerateResponse = {
  id: string;
  text: string;
  toolCalls: Array<{
    id: string;
    name: string;
    argumentsJson: string;
  }>;
  finishReason:
    | "stop"
    | "length"
    | "tool_calls"
    | "content_filter"
    | "error"
    | "unknown";
  usage?: {
    inputTokens?: number;
    outputTokens?: number;
    totalTokens?: number;
  };
  raw: unknown;
};
```

关键是保留 `raw`。原因是：

- 供应商会新增字段；
- 某些能力无法映射到统一对象；
- 排障时必须能看见原始响应；
- 计费、请求 ID、供应商 safety metadata、引用信息等可能只存在于原始响应中；
- 不能为了“统一”而丢失重要上下文。

***

## 10. 迁移与适配清单

当你从 OpenAI Chat Completions 迁移到另一个协议，逐项检查以下内容。

### 请求侧

- [ ] 模型 ID 是否真实存在，而不是仅在另一厂商可用。
- [ ] API key 传递方式是否相同：`Authorization: Bearer`、`x-api-key`、`x-goog-api-key` 等。
- [ ] endpoint 和 API version 是否不同。
- [ ] system/developer 指令应迁移到哪个字段。
- [ ] assistant 历史是否允许直接回传。
- [ ] `content` 是 string、blocks、parts 还是 typed items。
- [ ] 多模态输入是 URL、base64、file ID 还是 provider-hosted file reference。
- [ ] `max_tokens`、`max_output_tokens`、`max_tokens_to_sample` 等字段是否改名。
- [ ] `temperature`、`top_p`、`seed`、`stop` 等参数是否支持、默认值是否一致。
- [ ] JSON mode 与 JSON Schema 是否真正受支持，还是仅提示词约束。
- [ ] 工具 schema 是 JSON Schema 的哪个方言，是否支持 `additionalProperties: false`、enum、union、嵌套对象。

### 响应侧

- [ ] 文本是在 `choices`、`output`、`content`、`parts` 还是 `candidates`。
- [ ] 完成原因字段是什么，是否存在安全拦截、长度截断、工具调用等不同状态。
- [ ] usage 的字段名和统计口径是否变化。
- [ ] 是否需要处理 reasoning / thinking 字段。
- [ ] 是否包含 citation、grounding、safety、cache、logprobs 等供应商特定 metadata。
- [ ] 流式输出的文本 delta、工具参数 delta 和终止事件是什么。
- [ ] 是否有请求 ID，是否应记录以便供应商排障。OpenAI 的文档特别建议检查响应中的 request ID / `x-request-id` 等信息。[15]

### 会话与数据侧

- [ ] 服务端是否存储请求/响应，默认是否开启。
- [ ] 是否可通过 response/conversation ID 继续会话。
- [ ] 若 API 无状态，是否已经实现历史裁剪、摘要与 token 预算。
- [ ] 是否需要显式关闭存储；OpenAI 文档指出 Responses 与 Chat Completions 都有存储行为及 `store: false` 选项的相关说明。[2]
- [ ] 是否记录了用户授权、工具审计、模型版本、提示词版本与原始响应。
- [ ] 是否将敏感信息最小化发送给第三方模型供应商。

***

## 11. 常见误区

### 误区一：OpenAI 兼容 = 替换 base URL 即可上线

这对最简单的单轮文本对话可能成立，但一旦涉及：

- 工具调用；
- 多模态；
- 流式；
- JSON Schema；
- reasoning；
- 使用量统计；
- 安全拦截；
- 模型别名和版本升级；

就必须按实际 provider 做集成测试。DeepSeek 的无状态多轮模式和流式 usage/tool call 细节就是典型例子。[11][13]

### 误区二：所有 `messages` 都是同一种 messages

OpenAI、Anthropic、DeepSeek、Z.AI 都可出现 `messages` 字段，但：

- system 指令位置不同；
- content 的形状不同；
- 工具调用的表示不同；
- 返回对象不同；
- role 集合不同；
- 是否允许某些消息序列不同。

字段同名不是协议同构。

### 误区三：只抽象 prompt 与 response 文本

这样短期很快，但在需要 function calling、搜索、文件、图像、实时语音、结构化 JSON、引用追踪时会迅速失控。至少应抽象：

```text
文本
多模态 parts
工具定义
工具调用
工具结果
流式事件
usage
finish reason
provider metadata
```

### 误区四：把所有模型参数当成统一含义

`temperature: 0.7` 在不同模型上不是可比较的随机性单位；`max_tokens` 也不总是同一方向的输出上限。不要将某家参数调优经验机械迁移到另一家模型。

### 误区五：把模型输出直接作为可执行命令

无论工具调用格式多么结构化，都必须：

- 进行 server-side schema validation；
- 实施按用户、租户、角色划分的权限校验；
- 对高风险操作要求二次确认；
- 对外部内容实施提示注入隔离；
- 审计调用参数和实际副作用；
- 为写操作设计幂等键。

***

## 12. 选型建议

### 只做普通文本生成

优先使用供应商推荐的当前主接口：

- OpenAI 新项目：优先 Responses。[1][2]
- Anthropic：Messages API。[6][7]
- Gemini 新项目：评估 Interactions API；若已有 GenerateContent 接入，则将其视作仍可用但偏 legacy 的接口。[3][9]
- DeepSeek：可使用 OpenAI 兼容 Chat Completions，但自己管理多轮历史。[12][13]
- 智谱/Z.AI：可从 Chat Completion 协议入手，并对多模态、工具和模型特定限制做单独验证。[14]

### 做多模型路由或成本优化

采用 canonical schema + provider adapters，但不强制所有能力降级到最小公分母。为每个 provider/model 维护 capability matrix 和集成测试。

### 做 Agent 或复杂工具工作流

优先选择将工具、状态、事件建模为一等对象的 API：

- OpenAI Responses 的 `input` / `output` typed items；
- Anthropic 的 content blocks 与 tool-use/tool-result 循环；
- Gemini 的 function call/function response parts，以及新的 Interactions 方向；
- 对 OpenAI compatible provider，应先验证工具调用的完整闭环，而不只验证“模型能返回函数名”。

### 做长会话

明确选择状态策略：

- **客户端状态**：可移植性高、供应商锁定低，但你要承担历史管理、摘要、token 裁剪与存储。
- **服务端状态/响应链**：调用更方便，可能具备更强 agent 原语，但更依赖供应商的对象 ID、保留策略和生命周期。

***

## 结论

理解 LLM API 协议的关键，不是死记 `messages`、`contents`、`parts`、`choices` 或 `candidates` 的字段名，而是识别每个接口的**交互模型**：

1. 输入到底是历史消息、内容 parts，还是通用 typed items？
2. 系统/开发者/用户/工具的权威层级如何表达？
3. 输出是单条 message、候选项，还是异构 item/event 流？
4. 工具调用和工具结果如何组成闭环？
5. 多轮上下文是客户端回传，还是服务端以 ID 管理？
6. 流式、推理、usage、错误和安全 metadata 如何出现？
7. “OpenAI 兼容”覆盖的是基础 JSON 外形，还是经过验证的完整行为？

如果只能记住一条工程原则，应是：

> 以自己的 canonical conversation/tool schema 承载业务语义；以 provider adapter 编译为各家请求并归一化各家响应；同时保留原始响应与能力差异，绝不把“字段名相似”误当成“协议与行为相同”。

OpenAI 的 Responses 与 Chat Completions、Anthropic 的 Messages、Gemini 的 GenerateContent/Interactions、DeepSeek 的兼容接口和 Z.AI 的 Chat Completion，共同构成了当前生态的主要协议分支。它们可以互相适配，但不能无损互换；成熟的系统应把兼容层当作起点，而不是把它当作集成完成的终点。

## Citations

1. [Text generation | OpenAI API](https://developers.openai.com/api/docs/guides/text)
2. [Migrate to the Responses API - OpenAI Developers](https://developers.openai.com/api/docs/guides/migrate-to-responses)
3. [Gemini API - Interactions API - Google AI for Developers](https://ai.google.dev/gemini-api/docs)
4. [Chat Completions Overview | OpenAI API Reference](https://developers.openai.com/api/reference/chat-completions/overview/)
5. [Responses | OpenAI API Reference](https://developers.openai.com/api/reference/python/resources/responses/)
6. [Messages - Claude API Reference - Anthropic](https://platform.claude.com/docs/en/api/messages)
7. [API overview - Claude Platform Docs - Anthropic](https://platform.claude.com/docs/en/api/overview)
8. [Generating content | Gemini API - Google AI for Developers](https://ai.google.dev/api/generate-content)
9. [Getting started - generateContent API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/get-started)
10. [Gemini API reference | Google AI for Developers](https://ai.google.dev/api)
11. [Chat Completions API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-chat-completion/)
12. [DeepSeek API Docs: Your First API Call](https://api-docs.deepseek.com/)
13. [Multi-round Conversation - DeepSeek API Docs](https://api-docs.deepseek.com/guides/multi_round_chat)
14. [Chat Completion - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/api-reference/llm/chat-completion)
15. [API Overview | OpenAI API Reference](https://developers.openai.com/api/reference/overview/)
16. [Responses Overview | OpenAI API Reference](https://developers.openai.com/api/reference/responses/overview/)
17. [Zhipu AI | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/compute/aig/chat-completion/zhipu-chat-completion)
18. [Chat Prefix Completion (Beta) - DeepSeek API Docs](https://api-docs.deepseek.com/guides/chat_prefix_completion/)
19. [Developer quickstart | OpenAI API](https://developers.openai.com/api/docs/quickstart)
20. [Generate content with the Gemini API - Google Cloud Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/inference)
21. [Create chat completion | OpenAI API Reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/)
22. [Use the Azure OpenAI Responses API - Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses)
23. [Work with chat completion models - Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/chatgpt)
24. [Open Responses](https://www.openresponses.org/)
25. [Introducing the Responses API - OpenAI Developer Community](https://community.openai.com/t/introducing-the-responses-api/1140929)
26. [OpenAI Responses API.md - Github-Gist](https://gist.github.com/steipete/b58f0087c02fd97cea73f016e42c8ac0)
27. [Quickstart to OpenAI's Responses API: Build Smarter AI Agents Fast](https://cohorte.co/blog/quickstart-to-openais-responses-api-build-smarter-ai-agents-fast)
28. [TIP: Chat Completions API reference - as a single request, for AI ...](https://community.openai.com/t/tip-chat-completions-api-reference-as-a-single-request-for-ai-understanding/1355654)
29. [Get started with Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start)
30. [Interactions API | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/interactions-overview)
31. [Inference using Anthropic Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-messages-api.html)
32. [Anthropic Claude Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html)
33. [Google Gen AI SDK documentation](https://googleapis.github.io/python-genai/)
34. [generate_content - Google Gen AI Python SDK](https://googleapis-python-genai-70.mintlify.app/api/models/generate-content)
35. [Google Gemini Content Generation API — Documentation, OpenAPI](https://apis.io/apis/google-gemini/google-gemini-content-generation-api/)
36. [Messages API | anthropics/anthropic-sdk-python | DeepWiki](https://deepwiki.com/anthropics/anthropic-sdk-python/5.1-messages-api)
37. [Change Log | DeepSeek API Docs](https://api-docs.deepseek.com/updates/)
38. [Native API (/chat/completions) | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/ai/aig/chat-completion/zai-glm/zai-glm-chat-completion)
39. [DeepSeek Platform](https://platform.deepseek.com/)
40. [DeepSeek API | Documentation | Postman API Network](https://www.postman.com/ai-on-postman/deepseek/documentation/gr0i44z/deepseek-api)
41. [Chat Completion - Hugging Face](https://huggingface.co/docs/inference-providers/en/tasks/chat-completion)
42. [Explore DeepSeek API - Chat Completion and more - SerpApi](https://serpapi.com/blog/explore-deepseek-api/)
43. [Native Support for Z.AI (Zhipu AI) API & Latest GLM Models ... - GitHub](https://github.com/HKUDS/nanobot/issues/2?timeline_page=1)
44. [ZhipuAI API - 智谱AI](https://open.bigmodel.cn/dev/api)
45. [Glm 4.7 - AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/zhipu/glm-4.7)
