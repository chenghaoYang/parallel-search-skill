# LLM 时代的 API 请求协议：从 Chat Completions、Responses、Messages 到 Gemini `generateContent`

LLM API 并不存在唯一的“行业标准协议”。当前主流生态可以归为四条主线：**OpenAI Chat Completions**、**OpenAI Responses**、**Anthropic Messages**、以及 **Google Gemini `generateContent`**。大量模型厂商（DeepSeek、智谱 GLM、通义千问、Kimi 等）会兼容其中一种或多种协议，但“兼容”通常只意味着请求能发出去、基础文本能返回；工具调用、多模态、推理、结构化输出、流式事件、状态管理和边界行为仍常有差异。

对工程团队而言，最重要的结论是：不要把“OpenAI-compatible”理解为完全可替换。应以内部统一的对话中间表示（canonical schema）承接业务，再为不同供应商实现显式适配层和能力矩阵。

## 1. 先建立 taxonomy：协议到底在解决什么

一个 LLM 调用协议并不只是“传 prompt、拿文本”。完整协议至少包含以下八层：

| 层次 | 要解决的问题 | 常见字段/对象 | 典型差异 |
|---|---|---|---|
| 1. 资源与端点 | 调哪个模型、哪个 API | `/chat/completions`、`/responses`、`/messages`、`:generateContent` | URL、版本、认证 Header、模型命名不同 |
| 2. 对话输入 | 如何表达历史、身份与上下文 | `messages`、`input`、`contents` | 角色集合、system 指令位置、是否可混合多种 item |
| 3. 内容载体 | 文本、图像、音频、文件、工具结果如何装载 | `content`、content blocks、`parts` | 字符串、数组、typed block 三种风格 |
| 4. 推理控制 | 随机性、长度、停止条件、推理预算 | `temperature`、`max_tokens`、`max_output_tokens`、`reasoning_effort` | 同名参数语义不完全一致，且模型支持度不同 |
| 5. 工具调用 | 模型如何请求外部函数，应用如何回传结果 | `tools`、`tool_calls`、`tool_use`、`functionCall` | 参数 schema、回传角色、关联 ID、并行调用规则不同 |
| 6. 输出结构 | 如何取文本、拒答、JSON、引用、推理项 | `choices[].message`、`output[]`、`content[]`、`candidates[]` | 输出是单条 message、多个 item，还是多个 candidate |
| 7. 流式传输 | 如何逐步接收 token/事件 | SSE chunks、typed events、`data:` | 事件名、delta 字段、完成标志、工具参数增量不同 |
| 8. 状态与治理 | 上下文怎么保留、是否存储、如何追踪和计费 | `previous_response_id`、conversation、usage、request ID | 有状态服务端链路 vs 客户端重放全历史 |

可以把协议分为两个更直观的维度：

1. **对话表示模型**
   - `messages` 型：历史是一串角色消息，如 OpenAI Chat Completions、Anthropic Messages、绝大多数 OpenAI-compatible API。
   - `items` 型：输入和输出都由强类型 item 构成，如 OpenAI Responses。
   - `contents/parts` 型：一轮对话由 `Content` 构成，一个 `Content` 再由多个 `Part` 构成，如 Gemini。

2. **兼容策略**
   - 原生协议：厂商自定义并长期维护，例如 Anthropic Messages、Gemini `generateContent`。
   - OpenAI Chat Completions 兼容：只替换 `base_url`、API key、模型名就可跑基础文本调用。
   - 多协议兼容：同一模型服务暴露多种“方言”；例如 DeepSeek 同时支持 OpenAI/Anthropic 兼容形式，Kimi 同时提供 OpenAI Chat Completions、OpenAI Responses 和 Anthropic Messages 入口。[1][2][3]
   - 网关转译：云平台或 AI gateway 接受一种协议，再在内部转成目标模型协议。此时“接口兼容”不等于目标模型原生具备该协议的全部语义。

***

## 2. 四个主流协议的核心对比

### 快速总览

| 协议 | 典型端点 | 输入主结构 | 系统指令 | 正常输出位置 | 工具调用闭环 | 最适合的使用场景 |
|---|---|---|---|---|---|---|
| OpenAI Chat Completions | `POST /v1/chat/completions` | `messages[]` | `system` / `developer` message | `choices[0].message` | assistant `tool_calls` → `tool` message | 兼容生态最广、传统聊天、跨厂商最容易起步 |
| OpenAI Responses | `POST /v1/responses` | `input` 字符串或 input items | 顶层 `instructions`，或 message item | `output[]` typed items | `function_call` item → `function_call_output` item | 新式 agent、多模态、工具、状态和 OpenAI 原生新能力 |
| Anthropic Messages | `POST /v1/messages` | `messages[]`，内容通常是 blocks | 顶层 `system` | `content[]` blocks | `tool_use` block → 用户 message 中的 `tool_result` block | Claude 原生能力、严格工具循环、block-first 多模态 |
| Gemini `generateContent` | `POST ...:generateContent` | `contents[]`，每条含 `parts[]` | `systemInstruction` | `candidates[].content.parts[]` | `functionCall` part → `functionResponse` part | Gemini 原生多模态、Google 生态、part-based 交互 |

OpenAI 目前把 Responses 定位为 Chat Completions 的演进版，建议新的文本生成应用优先考虑 Responses；它用 typed `output` items 替代 Chat Completions 中的 `choices[].message`，并把工具、图像、文件、音频和状态性能力放到统一对象模型中。[4][5][6]

Anthropic 的 Messages API 接收结构化消息，输入内容可以是字符串或按类型组织的 content blocks；其响应也以 block 数组表达，并通过 `stop_reason` 明确说明是自然结束、达到 token 上限、命中 stop sequence，还是需要工具执行。[7][8]

Gemini 的核心对象是 `Content` 与 `Part`：`contents[]` 承载对话历史，单个 `Content` 包含 `role` 和有序的 `parts[]`；`Part` 可以表达文本、内联媒体、文件、函数调用、函数返回，以及与推理链路相关的字段。[9][10]

***

### 2.1 OpenAI Chat Completions：最广泛的兼容基线

典型请求：

```json
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
  "max_tokens": 800
}
```

典型响应的消费方式：

```json
{
  "id": "chatcmpl_xxx",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "HTTP 流式响应通常……"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 123,
    "completion_tokens": 456,
    "total_tokens": 579
  }
}
```

应用通常读取：

```text
choices[0].message.content
```

OpenAI 官方参考中，Chat Completions 的核心输出是 `choices` 数组，各 choice 含 `message`；message 可包含正文、拒答、注释以及与工具/音频等相关信息。[11]

#### 这个协议的优势

- 最常见的 SDK、代理框架、AI gateway、可观测平台优先支持。
- 对纯文本聊天最直观：`messages in → choices out`。
- 国内外很多提供方选择复刻它，因此迁移成本低。
- 工程团队最容易先实现一个通用适配器。

#### 不要忽略的限制

- “兼容 Chat Completions”并不自动意味着支持全部 OpenAI 参数。
- `temperature`、`top_p`、`max_tokens`、`response_format`、`seed`、`logprobs`、`parallel_tool_calls` 等参数，可能被忽略、被限制，或语义不同。
- 视觉输入、音频输入、JSON Schema、函数调用、reasoning 相关字段往往是差异最大的区域。
- 有些新模型或推理模型不支持传统采样参数，或者支持但不建议随意设置。
- `finish_reason` 的可选值、空文本与工具调用共存时的表现、usage 字段是否含缓存/推理 token，也需逐供应商验证。

***

### 2.2 OpenAI Responses：从“聊天消息”走向“统一任务事件”

Responses API 的思路不是只做“下一条 assistant message”，而是让一次模型执行产出一组不同类型的输出 item。

最简请求可以是：

```json
{
  "model": "example-model",
  "instructions": "你是一个严谨的技术助手。",
  "input": "解释 HTTP 流式响应。"
}
```

也可以显式传输入消息：

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
          "text": "解释 HTTP 流式响应。"
        }
      ]
    }
  ]
}
```

逻辑响应形态：

```json
{
  "id": "resp_xxx",
  "object": "response",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "HTTP 流式响应通常……"
        }
      ]
    }
  ]
}
```

从 Chat Completions 迁移时，最重要的字段映射是：

| Chat Completions | Responses |
|---|---|
| `messages[]` | `input`，可为字符串或 input items |
| `system` / `developer` 指令 | 顶层 `instructions`，或保留为兼容消息 |
| `choices[].message.content` | 遍历 `output[]` 中的 message / `output_text` |
| assistant 的工具调用 | `function_call` output item |
| `tool` message 的函数结果 | `function_call_output` input item，依靠 `call_id` 关联 |
| 客户端保存完整 messages | 传完整 input/output，或使用服务端状态/会话能力 |

OpenAI 的迁移文档明确指出：Chat Completions 返回 `choices` 中的 message；Responses 返回带类型的 `output` items。若手动管理多轮状态，则需要把前一轮所需输出回传到下一次的 `input`；对于含 reasoning 的场景，不能只抽取可见文本，而应保留必要 output items。[4][12]

#### Responses 的真正变化

- **输出不再必然是一条文本消息。** 一次响应可能包含 assistant message、函数调用、推理相关 item、内建工具调用结果等。
- **输入也不只是 messages。** 可传文本、结构化消息、文件/图像/音频输入，以及前一轮的输出对象。
- **状态管理成为显式设计决策。** 你可以使用服务端的 response/conversation 链路，也可以自己保存并回放上下文。
- **工具调用的身份关联更通用。** 通过 `call_id` 把模型发起的函数请求与应用返回的结果绑定。
- **适配难度会更高。** 如果下游只“兼容 OpenAI Chat”，不要假设它也对 Responses 的 item 模型完全兼容。

#### 常见误区：只取文本，丢掉非文本 item

下面是风险较高的伪代码：

```python
answer = response.output_text
save_history(user_text, answer)
```

它对简单问答可能没问题，但对于工具调用、推理模型或多轮 agent，可能丢失继续执行所需的调用 ID、工具调用项或模型需要复用的上下文项。

更安全的抽象是：

```python
record = {
    "provider": "openai",
    "protocol": "responses",
    "response_id": response.id,
    "raw_output_items": response.output,
    "visible_text": extract_visible_text(response.output)
}
```

业务展示用 `visible_text`，协议续接用 `raw_output_items` 或受控的服务端 conversation/reference。

***

### 2.3 Anthropic Messages：把内容块和工具循环当作一等公民

典型请求：

```json
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
          "text": "解释 HTTP 流式响应。"
        }
      ]
    }
  ]
}
```

典型响应：

```json
{
  "id": "msg_xxx",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "HTTP 流式响应通常……"
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 123,
    "output_tokens": 456
  }
}
```

核心消费路径：

```text
content[] → 找 type == "text" 的 blocks → 拼接 text
```

#### 与 OpenAI Chat 最重要的结构差异

| 维度 | OpenAI Chat Completions | Anthropic Messages |
|---|---|---|
| 系统指令 | 通常是 `messages[]` 中的 `role: "system"` | 顶层 `system`，不是普通 chat message |
| 内容形态 | 可为字符串或 OpenAI 定义的 content parts | string 是简写，原生思想是 typed content blocks |
| 正常文本 | `choices[0].message.content` | `content[]` 中的 `text` block |
| 完成原因 | `finish_reason` | 顶层 `stop_reason` |
| 工具请求 | `tool_calls[]` | `content[]` 中的 `tool_use` block |
| 工具返回 | `role: "tool"`，带 `tool_call_id` | `role: "user"`，内容含 `tool_result` block |
| assistant 预填充 | 各服务实现与兼容性不一 | 可使用末尾 assistant message 续写，但需谨慎对待跨厂商兼容性 |

Anthropic 的 Messages API 要求应用围绕 content blocks 和 `stop_reason` 编排。模型需要调用工具时，返回一个或多个 `tool_use` block，且 `stop_reason` 为 `tool_use`；应用执行工具后，必须将结果作为紧随其后的用户消息中的 `tool_result` block 回传，并使用 `tool_use_id` 关联。[13][14][15]

#### Anthropic 工具调用的严格性

模型响应：

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

应用执行后，下一次请求必须包含：

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_abc",
      "content": "晴，22°C"
    }
  ]
}
```

这不是一个可以“随便插入一条普通 user message”的松散约定。Anthropic 明确要求工具结果紧接对应工具调用；在包含工具结果的用户消息内，`tool_result` 必须排在文本之前。违背这些排序约束通常会被 API 拒绝，而不是静默修复。[8][13]

这类严格协议的好处是工具循环更确定；代价是跨协议转换时最容易出错。

***

### 2.4 Google Gemini `generateContent`：`Content` / `Part` 的多模态模型

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
    "temperature": 0.2,
    "maxOutputTokens": 800
  }
}
```

典型响应形态：

```json
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "HTTP 流式响应通常……"
          }
        ]
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 123,
    "candidatesTokenCount": 456,
    "totalTokenCount": 579
  }
}
```

核心消费路径：

```text
candidates[0].content.parts[] → 找 text part → 拼接 text
```

Gemini 的 `generateContent` 把会话历史放到 `contents[]`，每个 `Content` 由 `role` 与多个 `parts[]` 组成；`Part` 可以是文本、内联数据、文件数据、函数调用或函数结果。多轮聊天时，模型历史的角色通常是 `model`，而不是 `assistant`。[9][10]

#### Gemini 相对 message 协议的认知转换

不要试图把 Gemini 机械地理解为“`messages` 改名成 `contents`”。更准确的理解是：

```text
Conversation
  ├── Content(role=user)
  │     ├── Part(text)
  │     ├── Part(inlineData/image)
  │     └── Part(fileData)
  └── Content(role=model)
        ├── Part(text)
        └── Part(functionCall)
```

也就是说，Gemini 的基本单位不是“纯文本消息”，而是可混合多种 Part 的内容回合。

#### Gemini 函数调用的语义

Gemini 会在 model 的 `parts[]` 中返回 `functionCall`，应用运行函数后，用 `functionResponse` part 继续会话。其工具调用的关联和消息归属方式与 OpenAI / Anthropic 都不同，不能把 OpenAI 的 `role: "tool"` 原样搬过去。Google 文档中明确列出 `functionCall`、`functionResponse`、`thought` 和 `thoughtSignature` 都属于 `Part` 的不同联合类型。[10]

***

## 3. 同一个业务请求，在四种协议中的写法

假设业务目标是：

> “用中文简洁解释 JWT；如果不确定，调用 `search_docs` 工具。”

### OpenAI Chat Completions

```json
{
  "model": "example-model",
  "messages": [
    {
      "role": "system",
      "content": "请用中文简洁回答。"
    },
    {
      "role": "user",
      "content": "解释 JWT；若不确定可检索文档。"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "search_docs",
        "description": "检索内部技术文档",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string"
            }
          },
          "required": ["query"]
        }
      }
    }
  ]
}
```

模型工具请求通常在：

```text
choices[0].message.tool_calls[]
```

工具结果通常回传为：

```json
{
  "role": "tool",
  "tool_call_id": "call_123",
  "content": "检索结果……"
}
```

***

### OpenAI Responses

```json
{
  "model": "example-model",
  "instructions": "请用中文简洁回答。",
  "input": "解释 JWT；若不确定可检索文档。",
  "tools": [
    {
      "type": "function",
      "name": "search_docs",
      "description": "检索内部技术文档",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string"
          }
        },
        "required": ["query"]
      }
    }
  ]
}
```

模型可能在 `output[]` 中给出：

```json
{
  "type": "function_call",
  "call_id": "call_123",
  "name": "search_docs",
  "arguments": "{\"query\":\"JWT 定义\"}"
}
```

工具执行结果作为新的 input item 回传：

```json
{
  "type": "function_call_output",
  "call_id": "call_123",
  "output": "检索结果……"
}
```

***

### Anthropic Messages

```json
{
  "model": "claude-example",
  "max_tokens": 1024,
  "system": "请用中文简洁回答。",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "解释 JWT；若不确定可检索文档。"
        }
      ]
    }
  ],
  "tools": [
    {
      "name": "search_docs",
      "description": "检索内部技术文档",
      "input_schema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string"
          }
        },
        "required": ["query"]
      }
    }
  ]
}
```

模型返回的工具请求：

```json
{
  "type": "tool_use",
  "id": "toolu_123",
  "name": "search_docs",
  "input": {
    "query": "JWT 定义"
  }
}
```

工具执行结果必须回传为用户内容块：

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_123",
      "content": "检索结果……"
    }
  ]
}
```

***

### Gemini `generateContent`

```json
{
  "systemInstruction": {
    "parts": [
      {
        "text": "请用中文简洁回答。"
      }
    ]
  },
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "解释 JWT；若不确定可检索文档。"
        }
      ]
    }
  ],
  "tools": [
    {
      "functionDeclarations": [
        {
          "name": "search_docs",
          "description": "检索内部技术文档",
          "parameters": {
            "type": "object",
            "properties": {
              "query": {
                "type": "string"
              }
            },
            "required": ["query"]
          }
        }
      ]
    }
  ]
}
```

模型会在 `candidates[0].content.parts[]` 中给出类似：

```json
{
  "functionCall": {
    "name": "search_docs",
    "args": {
      "query": "JWT 定义"
    }
  }
}
```

然后应用以 `functionResponse` part 将执行结果纳入后续上下文。

***

## 4. “messages” 并不是同一个东西

虽然多个厂商都使用 `messages` 字段，但它们的语义并不完全一致。

| 问题 | OpenAI Chat | OpenAI Responses | Anthropic Messages | Gemini |
|---|---|---|---|---|
| 历史主字段 | `messages[]` | `input` | `messages[]` | `contents[]` |
| 系统规则 | system/developer message | `instructions` 优先；也支持 message item | 顶层 `system` | `systemInstruction` |
| 人类角色 | `user` | `user` | `user` | `user` |
| 模型角色 | `assistant` | `assistant` output item | `assistant` | `model` |
| 工具结果角色 | `tool` | `function_call_output` input item | `user` 内嵌 `tool_result` | `functionResponse` part，SDK/具体形态依实现 |
| 内容结构 | string 或 content parts | typed input/output content | string 或 typed blocks | `parts[]` |
| 关键标识 | `tool_call_id` | `call_id` | `tool_use_id` | 通常按 function call/response 的上下文结构关联 |

### 角色不能按名称机械映射

一个常见但危险的适配逻辑是：

```python
ROLE_MAP = {
    "system": "system",
    "user": "user",
    "assistant": "assistant",
    "tool": "tool"
}
```

它对 OpenAI-compatible API 可能能工作，但在 Anthropic 和 Gemini 上不够：

- Anthropic 的系统提示通常不应作为 `messages[].role = "system"` 发送，而应转为顶层 `system`。
- Anthropic 的工具结果不能简单转成独立 `tool` role；它是 user turn 中的 `tool_result` block。
- Gemini 的 assistant 角色是 `model`。
- Responses 既可接受消息，也可接受 function output、历史 output、文件等 typed items；用四个角色无法完整表达。

### 建议：内部采用“语义事件”而非“供应商消息”

应用内部可以先定义一个足够表达业务的中间层：

```ts
type Turn =
  | {
      kind: "instruction";
      text: string;
      priority: "system" | "developer";
    }
  | {
      kind: "user_message";
      content: ContentPart[];
    }
  | {
      kind: "assistant_message";
      content: ContentPart[];
    }
  | {
      kind: "tool_call";
      callId: string;
      name: string;
      arguments: unknown;
    }
  | {
      kind: "tool_result";
      callId: string;
      name?: string;
      result: unknown;
      isError?: boolean;
    };

type ContentPart =
  | { type: "text"; text: string }
  | { type: "image_url"; url: string }
  | { type: "image_bytes"; mimeType: string; data: string }
  | { type: "file"; fileId?: string; url?: string; mimeType?: string }
  | { type: "audio"; mimeType: string; data: string };
```

然后明确写四个 renderer：

```text
Canonical Turn[] 
  ├── OpenAI Chat renderer
  ├── OpenAI Responses renderer
  ├── Anthropic Messages renderer
  └── Gemini Content/Part renderer
```

不要反过来直接把一种厂商的原始 JSON 当成所有模型的通用数据模型。

***

## 5. DeepSeek：高度兼容，不等于没有差异

DeepSeek 官方文档声明其 API 提供 OpenAI/Anthropic 兼容格式；OpenAI 风格调用使用 `https://api.deepseek.com`，Anthropic 兼容入口使用 `https://api.deepseek.com/anthropic`。它同时提供 Chat Completions 和对 OpenAI Responses 格式的支持。[1][2]

### DeepSeek Chat Completions 的工程含义

基础调用通常可以沿用 OpenAI SDK 的习惯：

```python
from openai import OpenAI

client = OpenAI(
    api_key="DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": "你是一个技术助手。"},
        {"role": "user", "content": "解释 SSE。"}
    ]
)
```

这降低了接入门槛，但不代表可把 OpenAI 所有模型特性照搬。

### DeepSeek 的典型差异点

1. **模型与能力不是 OpenAI 同构的**
   - 模型名、上下文上限、视觉能力、工具调用、结构化输出、缓存、reasoning 能力均需按 DeepSeek 文档和目标模型校验。
   - 文档示例出现了如 `thinking`、`reasoning_effort` 一类推理控制字段，它们不应被假定对所有 OpenAI 兼容供应商通用。[1]

2. **Responses 兼容可能带固定值或不支持的能力**
   - DeepSeek 官方说明其 Responses API 对响应结构兼容，但对未支持能力关联的字段会给固定值，例如 `store: false`、`previous_response_id: null`、`parallel_tool_calls: true`。因此，代码不能根据“字段存在”就推断服务端真正提供了相应语义。[2]

3. **结构化输出的支持范围要逐模型测试**
   - DeepSeek Chat Completions 文档列出了 `response_format: {"type":"json_object"}` 的 JSON Output，但这不等价于 OpenAI 式严格 JSON Schema Structured Outputs。生产环境应验证：无效 JSON 的概率、schema 约束、流式 JSON、工具调用与 JSON 输出是否能组合。[16]

4. **兼容层本身也有版本性**
   - 即使路径和 SDK 调用稳定，具体参数、模型能力和错误类型仍可能随着模型或平台版本变化。

### DeepSeek 的最佳实践

- 把它作为一个明确的 `provider=deepseek`，而不是把它伪装成 `provider=openai`。
- 为每个部署模型记录能力：文本、图像、工具调用、JSON mode、stream、reasoning、Responses。
- 对工具调用、JSON 输出、流式 delta、拒答/错误、重试和 usage 写契约测试。
- 将原始 request/response 做安全脱敏后保留，便于定位兼容差异。

***

## 6. 智谱 GLM：主要走 OpenAI-compatible，但模型能力仍须单独管理

智谱 AI 的开放文档提供 OpenAI API 兼容接口：可复用现有 OpenAI SDK，通过替换 API key、`base_url` 和模型名进行调用。其对话补全请求以 `model` 与 `messages` 为核心，支持 system、user、assistant、tool 四种角色。[17][18]

基础模式类似：

```python
from openai import OpenAI

client = OpenAI(
    api_key="ZHIPU_API_KEY",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

response = client.chat.completions.create(
    model="glm-5.3",
    messages=[
        {
            "role": "system",
            "content": "你是一个严谨的技术助手。"
        },
        {
            "role": "user",
            "content": "解释 JWT。"
        }
    ],
    temperature=0.2
)
```

### 智谱 `messages` 与 Anthropic Messages 的关键区别

用户特别容易混淆的是：两者都出现“messages”，但协议哲学不同。

| 维度 | 智谱 GLM 的 OpenAI-compatible Chat | Anthropic Messages |
|---|---|---|
| 主要定位 | 复用 OpenAI Chat Completions 开发方式 | Claude 的原生 API |
| 系统提示 | `messages[]` 中 `role: "system"` | 顶层 `system` |
| 普通角色 | `system`、`user`、`assistant`、`tool` | 通常 `user`、`assistant`；system 独立 |
| 工具调用结果 | 使用 `tool` role，按 OpenAI 风格 | 使用 user message 中的 `tool_result` block |
| 内容建模 | 普通模型多为纯文本；视觉模型支持多模态内容 | string 为简写，核心为 typed blocks |
| 对话约束 | 输入不能只由 system/assistant 构成 | 工具调用与工具结果存在严格相邻和排序规则 |
| 输出读取 | 通常遵从 `choices[].message` 思维模型 | 遍历 `content[]`，看 block 类型和 `stop_reason` |

智谱官方文档说明：普通对话模型支持纯文本对话和工具调用；视觉模型可支持文本、图片、视频、文件等内容；并明确约束输入消息不能只有 system 或 assistant。[18]

因此，如果你的上游框架是 Anthropic SDK 或 Claude Code 风格，不能仅靠“模型很强”或“某个网关提供 Anthropic endpoint”推断智谱原生 OpenAI endpoint 会理解 Anthropic 的 `tool_use/tool_result` 对话历史。必须使用对应 endpoint，或者让一个可靠的网关完成并测试协议转译。

***

## 7. 其他主流适配路线

### 通义千问 / Model Studio

阿里云 Model Studio 同时有原生/SDK 路线与 OpenAI-compatible Chat 路线。其 OpenAI 兼容入口可使用 `/chat/completions`，并以 `messages` 传上下文；但官方文档同时标注了一些模型级注意事项，例如 QwQ 模型不应设置 system message、某些模型的 system message 不生效。[19][20]

这说明一个重要事实：

> **协议兼容只说明 JSON 长得像；模型指令层级是否生效，仍由模型与服务端实现决定。**

若路由到多个 Qwen、QwQ、视觉、推理或第三方托管模型，不要把 system prompt 策略做成全局固定规则。

***

### Kimi / Moonshot

Kimi 是“多协议暴露”很典型的案例：其官方 API 平台列出 OpenAI Chat Completions、OpenAI Responses 和 Anthropic Messages 三种兼容格式，分别对应不同 base URL/endpoint，旨在复用 OpenAI SDK、Anthropic SDK、Claude Code 及相关工具。[3][21]

这对用户的意义是：

- 已有 OpenAI Chat 应用，可以选择 Chat Completions endpoint。
- 已迁移到 OpenAI Responses 的 agent，可以使用 Responses endpoint。
- 已有 Claude Code 或 Anthropic SDK 工作流，可以选 Messages endpoint。
- 但仍要以 Kimi 官方各协议的参数支持表为准，不能因 endpoint 名称相同就假定所有高级功能一一等价。

***

### Z.AI / GLM 系列的另一类兼容表面

Z.AI 文档的 Chat Completion 也以 OpenAI 风格 `messages` 作为输入，并显式支持 system、user、assistant、tool 角色及流式/非流式输出、多模态输入和工具使用。[22]

这类接口通常是“OpenAI Chat 作为共同语言”的代表，适合构建统一 Chat adapter；但其多模态 part 格式、工具定义、模型名、参数上限、错误码和扩展字段仍应保留 provider-specific 分支。

***

## 8. 工具调用：最容易被“兼容”误导的区域

四种协议的工具调用可以抽象成同一件事：

```text
模型声明“我要调用 X，并给出参数”
→ 应用执行 X
→ 应用把结果与调用 ID 关联后回传
→ 模型继续生成
```

但编码方式不同：

| 协议 | 模型发起调用 | 调用标识 | 应用回传工具结果 | 下一步判断 |
|---|---|---|---|---|
| OpenAI Chat | assistant `tool_calls[]` | `tool_call.id` | `role: "tool"` + `tool_call_id` | `finish_reason` / 是否存在 tool calls |
| OpenAI Responses | `output[]` 的 `function_call` item | `call_id` | `function_call_output` input item | 遍历 output item 类型 |
| Anthropic | `content[]` 的 `tool_use` block | `tool_use.id` | user content 中 `tool_result` block | `stop_reason == "tool_use"` |
| Gemini | model Content 中 `functionCall` Part | 按 function-call 上下文/SDK对象关联 | `functionResponse` Part | 检查 candidate parts |

### 统一工具调用循环

无论厂商如何编码，应用层都应该具备同样的状态机：

```text
1. 发送规范化的对话与可用工具定义。
2. 解析响应中的一个或多个工具调用。
3. 验证工具名、参数 schema、权限与业务安全策略。
4. 执行工具，捕获超时、异常和结构化错误。
5. 以供应商要求的关联 ID 和消息结构回传结果。
6. 重复，直到模型自然结束、达到最大轮数或触发故障策略。
```

### 生产环境必须加的护栏

- 允许列表：模型不能调用未注册工具。
- 参数校验：用服务端 schema 验证，而不是相信模型生成的 JSON。
- 授权校验：工具调用必须携带/继承最终用户权限，不能因为“模型建议”而越权。
- 幂等设计：带副作用的工具要有幂等键，防止模型重试或网络重放导致重复执行。
- 最大轮数：防止工具调用循环。
- 超时与预算：工具和整个 agent run 都应有 deadline。
- 审计日志：记录调用 ID、工具名、摘要化参数、执行状态和耗时。
- 人工确认：支付、删除、发信、发布、权限变更等外部副作用动作必须经过用户确认或策略审批。

***

## 9. 流式协议：不要只处理“文本 delta”

多数 LLM API 以 Server-Sent Events（SSE）做流式输出，但事件模型不同。

### 最低限度的错误处理

不少应用只做：

```text
收到 chunk → 取 delta.content → 拼接
```

这在纯文本问答时或许足够，但在工具、多模态、reasoning、结构化输出下不够可靠。流式适配器至少应能处理：

- 文本增量。
- 工具调用名称与参数的分段增量。
- 多个并行工具调用。
- 完成原因或停止原因。
- usage 最终统计，若供应商在流尾提供。
- 错误事件与中断。
- 响应 ID、请求 ID 和可恢复的状态标识。
- 供应商特有 item/block/part 开始、增量、完成事件。

### 各协议的流式思路

- **OpenAI Chat Completions**：常见为 chunk 中的 `choices[].delta`，最终以 finish reason 收束。
- **OpenAI Responses**：更适合按“typed event / item lifecycle”理解，而不仅是文本；工具、输出 message、reasoning 或其他 output item 可能各有事件。
- **Anthropic Messages**：流中会涉及 message、content block、delta 等阶段，最终应从相应事件读取 `stop_reason`。Anthropic 明确建议流式场景从 message delta 事件读取 stop reason。[8]
- **Gemini**：流式调用返回一系列 `GenerateContentResponse`，每个响应可能逐步补全 candidate content 或其他元信息。[9]

### 推荐的内部流事件

```ts
type NormalizedStreamEvent =
  | { type: "response_started"; responseId?: string }
  | { type: "text_delta"; text: string }
  | { type: "tool_call_started"; callId: string; name?: string }
  | { type: "tool_arguments_delta"; callId: string; delta: string }
  | { type: "tool_call_completed"; callId: string; name: string; args: unknown }
  | { type: "usage"; inputTokens?: number; outputTokens?: number; totalTokens?: number }
  | { type: "response_completed"; reason?: string }
  | { type: "error"; code?: string; message: string; retryable?: boolean };
```

前端只消费 `text_delta` 并显示；后端必须完整消费所有事件，尤其不能丢掉工具调用、完成原因和使用量。

***

## 10. 结构化输出：JSON mode 不等于 JSON Schema

“让模型返回 JSON”至少有三层不同承诺：

| 能力层级 | 含义 | 风险 |
|---|---|---|
| Prompt 要求 JSON | 在 system/user prompt 中要求输出 JSON | 最不可靠，可能带 Markdown、解释文字、无效 JSON |
| JSON object mode | 保证或倾向于生成可解析 JSON object | 不必然满足字段、枚举、嵌套结构等业务 schema |
| JSON Schema / Structured Outputs | 输出按给定 schema 约束 | 仍需关注供应商、模型、流式、工具并用时的支持范围 |

OpenAI Chat Completions 文档提供 `json_schema` 类型的 Structured Outputs 描述；DeepSeek Chat 文档列出的 `json_object` 则是 JSON Output。二者不能仅因都写作“JSON”而视为同一保证等级。[11][16]

### 工程建议

- 将结构化输出解析失败作为正常的可恢复路径，而不是异常分支。
- 仍在服务端做 JSON parse 与 schema validation。
- 对失败策略做明确设计：重试、修复提示、降级到普通文本、人工审核或直接报错。
- 不要把模型输出直接写进数据库、直接执行 SQL、直接拼接 shell 命令，或直接触发有副作用 API。
- 若同时允许工具调用和业务 JSON 输出，优先使用协议的工具调用机制表达行动；把最终用户可见结果单独做 schema 化，避免一个 JSON 同时承担“命令”和“展示”职责。

***

## 11. 状态管理：无状态重放、服务端会话与混合模式

### 模式 A：客户端无状态重放

每次都将完整历史发送：

```text
turn 1: [system, user1]
turn 2: [system, user1, assistant1, user2]
turn 3: [system, user1, assistant1, user2, assistant2, user3]
```

优点：

- 最可移植。
- 供应商切换和离线重放容易。
- 数据控制权在应用侧。

代价：

- token 成本和延迟随历史增长。
- 应用必须正确存储多模态内容、工具调用和工具结果。
- 如果错误地只保存“可见文本”，可能破坏 reasoning 或工具对话的后续语义。

### 模式 B：服务端状态引用

通过 response ID、conversation ID 或供应商提供的会话资源续接。

优点：

- 减少重复传输。
- 某些模型能更好地维护其原生执行上下文。
- 对复杂 agent 可能更方便。

代价：

- 供应商锁定更强。
- 存储、保留期、删除、跨区域、合规和可复现性要单独审查。
- 迁移模型时必须把历史重新转为自己的 canonical schema。

OpenAI Responses 文档指出，Responses 可以将输入和输出自动加入 conversation；手动管理状态时，需要在下一轮输入中保留模型前一轮的相关 output。[6][12]

### 推荐：混合模式

1. 应用自己的数据库保存 canonical transcript、工具审计和可展示文本。
2. 对某供应商保留其 response/conversation ID 作为性能优化，而非唯一事实来源。
3. 发生故障、迁移、审计、A/B test 或 provider fallback 时，从 canonical transcript 重建请求。
4. 每轮记录协议版本、模型版本、能力开关与原始响应摘要。

***

## 12. 不同厂商的兼容性，应该如何验收

不要只测试下面这一个 happy path：

```python
client.chat.completions.create(
    model="x",
    messages=[{"role": "user", "content": "hi"}]
)
```

这只能证明“基础文本能通”。

### 最小兼容验收矩阵

| 测试类别 | 应验证什么 |
|---|---|
| 认证与端点 | API key、Header、base URL、API version、区域 endpoint |
| 模型发现 | 模型 ID 是否真实存在，别名是否稳定，模型是否退役 |
| 纯文本 | system/user/assistant 多轮、中文、长文本、Unicode、空输入 |
| 指令优先级 | system/developer/instructions 与用户输入冲突时的行为 |
| 上下文 | 历史回放、历史压缩、超窗错误、自动截断策略 |
| 多模态 | 图片 URL、base64、文件 ID、MIME type、单轮和多轮复用 |
| 工具调用 | 单工具、并行工具、空参数、参数流式增量、工具错误、重试 |
| 结构化输出 | JSON object、JSON Schema、无效 schema、流式 JSON |
| 流式 | 文本、工具、完成事件、usage、网络中断、客户端取消 |
| 停止原因 | 正常结束、长度限制、内容过滤、工具调用、stop sequence |
| usage | 输入、输出、缓存、推理 token 的字段与计费口径 |
| 错误 | 400/401/403/404/409/429/5xx，重试建议、request ID |
| 安全 | prompt injection、工具越权、敏感数据、日志脱敏 |
| 限流与并发 | RPM、TPM、并发、队列、超时、指数退避 |
| 版本演进 | SDK 升级、模型升级、字段新增、弃用通知、回归测试 |

### 契约测试的关键思想

把每个 provider 的 request/response 解析写成契约：

```text
给定 canonical tool_call
→ 渲染成 provider request
→ 由 mock / sandbox 返回 provider response
→ 解析回 canonical tool_call
→ 验证 callId、名称、参数和错误语义没有丢失
```

尤其要验证：

- 多个工具调用是否都保留下来。
- JSON 参数字符串是否被正确累积和解析。
- tool result 是否进入正确角色/part/block。
- 正常文本和工具调用混合时，文本是否被意外丢弃。
- stream 与 non-stream 的最终归一化结果是否一致。
- 模型拒答、内容过滤、空响应如何表达。

***

## 13. 常见失败模式

### 失败 1：只替换 `base_url` 和 `model`

这可用于验证最基础的 OpenAI-compatible 文本调用，但不能作为完整迁移方案。工具、多模态、stream、JSON Schema、reasoning、usage 与错误处理必须逐项验证。

### 失败 2：把 `messages` 当作跨厂商通用 AST

`messages` 只是同名字段，不是同一个抽象语法树。Anthropic 的系统提示和工具结果、Gemini 的 role/part、Responses 的 item 都与 OpenAI Chat 不同。

### 失败 3：丢弃 assistant 的原始工具调用

很多系统只把 assistant 文本存下来。下一轮模型没有得到先前的 tool call ID、参数与结果对应关系，就可能无法正确继续。

### 失败 4：只在流式文本上做拼接

一旦模型返回工具参数增量、多个 blocks、多个 candidates 或错误事件，只拼文本会导致状态不完整。

### 失败 5：认为 `temperature=0` 就完全确定

不同模型、不同后端路由、不同工具和不同推理机制仍可能使输出不同。若需要稳定性，应控制模型版本、提示模板、工具数据、随机采样设置，并做好结果验证。

### 失败 6：用 prompt 强迫模型自己“调用 API”

工具调用应走协议提供的 function/tool 机制，并在服务端执行权限检查。让模型输出伪 JSON 命令再直接执行，是典型安全风险。

### 失败 7：把 schema 兼容误认为能力兼容

一个 gateway 可以把 Anthropic `/messages` 转成某模型的内部请求，但目标模型不一定拥有同样的工具遵循度、长上下文稳定性、视觉理解、指令优先级或结构化输出可靠性。

***

## 14. 推荐的落地架构

### 分层设计

```text
业务层
  └── 任务定义、用户权限、产品交互

LLM 编排层
  └── 会话状态、模型路由、工具循环、重试、预算、fallback

Canonical 模型层
  └── Turn / ContentPart / ToolCall / ToolResult / Usage / StreamEvent

Provider Adapter 层
  ├── OpenAI Chat Completions adapter
  ├── OpenAI Responses adapter
  ├── Anthropic Messages adapter
  ├── Gemini generateContent adapter
  ├── DeepSeek adapter
  ├── Zhipu / GLM adapter
  ├── Qwen adapter
  └── Kimi adapter

传输与治理层
  └── HTTP/SSE、密钥、限流、日志、追踪、脱敏、审计
```

### Adapter 的职责

每个 adapter 应负责：

- 将 canonical 请求渲染为厂商请求。
- 校验该模型是否支持请求中所需能力。
- 将非流式响应解析为 canonical result。
- 将流式事件归一为 canonical stream events。
- 将工具调用与工具结果正确映射。
- 标准化错误、可重试性、request ID、usage。
- 暴露 provider-specific extensions，但避免让业务层依赖它们。

### 能力矩阵而不是 `if provider == ...`

建议维护每个“供应商 + 模型 + endpoint”的显式能力配置：

```yaml
provider: deepseek
endpoint: chat_completions
model: deepseek-flash
capabilities:
  text: true
  image_input: true
  audio_input: false
  streaming: true
  tools: true
  parallel_tool_calls: verify_per_model
  json_object: true
  json_schema: false
  server_side_conversation: false
  responses_protocol: true
  prompt_cache: verify_per_model
```

为什么必须细到 endpoint 和 model？

- 同一供应商中，不同模型支持的模态和参数不同。
- 同一模型通过不同兼容协议暴露时，能力也可能不同。
- 供应商文档或兼容层可能把“字段接受”与“能力生效”区分开。
- 模型升级或别名变化会改变行为。

***

## 15. 选型建议：什么时候用哪一种

| 目标 | 优先考虑 | 原因 |
|---|---|---|
| 快速接入多个厂商的基础文本聊天 | OpenAI Chat Completions 适配层 | 生态覆盖面最大，国内外兼容接口多 |
| 新建 OpenAI 原生 agent / 多工具系统 | OpenAI Responses | item 化输出、工具、状态和新能力更统一 |
| 深度使用 Claude 原生特性 | Anthropic Messages | 直接使用 block、tool use、stop reason 语义 |
| 深度使用 Gemini 原生多模态和 Google 生态 | Gemini `generateContent` | Content/Part 模型最贴近原生能力 |
| 已有 OpenAI SDK，接入 DeepSeek / 智谱 / Qwen / Kimi | Chat Completions 起步 | 多数支持替换 base URL 的低成本迁移 |
| 已有 Claude Code 或 Anthropic SDK 工作流 | 优先官方支持的 Anthropic Messages endpoint | 避免自行模拟 `tool_use/tool_result` 的严格语义 |
| 希望支持多模型 fallback | Canonical schema + provider adapters | 不能依赖任何一家 raw protocol 作为内部事实模型 |
| 高风险工具自动化 | 任何协议都需独立安全控制 | 协议只表达调用，不替代授权、审计和确认机制 |

***

## 16. 最终认知框架

可以用下面四句话建立稳定认知：

1. **Chat Completions 是最常见的兼容基线，不是统一标准。**  
   DeepSeek、智谱、通义、Kimi 等接入时，往往可以先用它跑通，但不能止步于此。DeepSeek 官方提供 OpenAI/Anthropic 兼容形态；智谱提供 OpenAI-compatible 接口；Kimi 则同时提供 OpenAI Chat、Responses 和 Anthropic Messages 入口。[1][3][17]

2. **Responses、Messages、Gemini 分别代表三种不同的对象模型。**  
   Responses 是 typed input/output items；Anthropic 是 block-first messages；Gemini 是 `Content` / `Part`。它们不是字段重命名关系。[4][7][10]

3. **工具调用与状态管理是协议差异最深、生产事故最多的区域。**  
   必须保留 call ID、严格遵循工具结果回传格式，并通过状态机实现，而不是临时拼 JSON。Anthropic 尤其要求工具结果紧邻工具调用并按特定顺序发送。[8][13]

4. **真正可移植的是你的内部语义模型、测试和治理，而不是某个供应商 JSON。**  
   用 canonical schema、能力矩阵、contract tests、观测日志和安全策略，让供应商协议成为可替换的 adapter，而不是渗透到业务代码的底层事实。

如果只需要一条最实用的工程原则：**以 OpenAI Chat Completions 作为“最低共同接入层”，但以 canonical event/content/tool 模型作为内部标准；当要使用工具、多模态、推理、结构化输出或服务端状态时，必须切换到各厂商协议的原生语义，而不是依赖“兼容”的想象。**

## Citations

1. [DeepSeek API Docs: Your First API Call](https://api-docs.deepseek.com/)
2. [Using the Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/guides/responses_api/)
3. [API Overview - Kimi API Platform](https://platform.kimi.ai/docs/api/overview)
4. [Migrate to the Responses API - OpenAI Developers](https://developers.openai.com/api/docs/guides/migrate-to-responses)
5. [Text generation | OpenAI API](https://developers.openai.com/api/docs/guides/text)
6. [Create a model response | OpenAI API Reference](https://developers.openai.com/api/reference/resources/responses/methods/create/)
7. [Messages - Claude API Reference](https://docs.anthropic.com/en/api/messages)
8. [Stop reasons and fallback - Claude Platform Docs](https://docs.anthropic.com/en/api/handling-stop-reasons)
9. [Generating content | Gemini API - Google AI for Developers](https://ai.google.dev/api/generate-content)
10. [Generate content with the Gemini API - Google Cloud Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/inference)
11. [Create chat completion | OpenAI API Reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/)
12. [Conversation state | OpenAI API](https://developers.openai.com/api/docs/guides/conversation-state)
13. [Handle tool calls - Claude Platform Docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/handle-tool-calls)
14. [Tool use with Claude - Claude Platform Docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)
15. [How tool use works - Claude Platform Docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/how-tool-use-works)
16. [Chat Completions API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-chat-completion/)
17. [OpenAI API 兼容 - 智谱AI开放文档](https://docs.bigmodel.cn/cn/guide/develop/openai/introduction)
18. [对话补全 - 智谱AI开放文档](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)
19. [Alibaba Cloud Model Studio:OpenAI compatible - Chat](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions)
20. [Make your first API call to Qwen - Alibaba Cloud Model Studio](https://www.alibabacloud.com/help/en/model-studio/first-api-call-to-qwen)
21. [Quickstart - Kimi API Platform](https://platform.kimi.ai/docs/overview)
22. [Chat Completion - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/api-reference/llm/chat-completion)
23. [Quick Start - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/guides/overview/quick-start)
24. [Assistants migration guide | OpenAI API](https://developers.openai.com/api/docs/assistants/migration)
25. [Anthropic Claude Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html)
26. [Claude Code - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/scenario-example/develop-tools/claude)
27. [Gemini API reference | Google AI for Developers](https://ai.google.dev/api)
28. [Google Gen AI SDK documentation](https://googleapis.github.io/python-genai/)
29. [API Overview | OpenAI API Reference](https://developers.openai.com/api/reference/overview/)
30. [Create a Message - Fireworks AI Docs](https://docs.fireworks.ai/api-reference/anthropic-messages)
31. [Compatible API (/messages) | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/compute/aig/chat-completion/zai-glm/zai-glm-message)
32. [Anthropic Messages - Introduction to Langdock - Docs](https://docs.langdock.com/en/developer/completion-api/anthropic)
33. [Moonshot AI provider - AI SDK](https://ai-sdk.dev/v5/providers/ai-sdk-providers/moonshotai)
34. [原生API (/chat/completions) | 中文 | API References](https://docs.console.zenlayer.com/api-reference/cn/compute/aig/chat-completion/zai-glm/zai-glm-chat-completion)
35. [Chat Completions API - Kimi API Platform](https://platform.kimi.ai/docs/api/chat)
36. [Search results - Claude Platform Docs](https://docs.anthropic.com/en/docs/build-with-claude/search-results)
37. [Community Providers: Zhipu AI (Z.AI) - AI SDK](https://ai-sdk.dev/providers/community-providers/zhipu)
38. [Programmatic tool calling - Claude Platform Docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/programmatic-tool-calling)
39. [Alibaba Cloud Model Studio:OpenAI-compatible - Batch (file input)](https://www.alibabacloud.com/help/en/model-studio/batch-interfaces-compatible-with-openai)
40. [Migrate Python apps from Azure OpenAI Chat Completions to the ...](https://learn.microsoft.com/en-us/azure/developer/ai/how-to/azure-openai-to-responses)
41. [How V7 gives AI agents institutional memory - OpenAI](https://openai.com/index/v7/)
42. [GitHub - openai/completions-responses-migration-pack: Developer ...](https://github.com/openai/completions-responses-migration-pack)
43. [Migration Guide for Assistants API to Responses API is now available](https://community.openai.com/t/migration-guide-for-assistants-api-to-responses-api-is-now-available/1354626)
44. [Introducing the Responses API - OpenAI Developer Community](https://community.openai.com/t/introducing-the-responses-api/1140929)
45. [Transition from Assistants API to Responses API](https://community.openai.com/t/transition-from-assistants-api-to-responses-api/1146931)
46. [Chat Completions vs OpenAI Responses API: What Actually Changed](https://dev.to/dev-in-progress/chat-completions-vs-openai-responses-api-what-actually-changed-4bco)
47. [TIP: Chat Completions API reference - as a single request, for AI ...](https://community.openai.com/t/tip-chat-completions-api-reference-as-a-single-request-for-ai-understanding/1355654)
48. [Open AI Responses API vs. Chat Completions vs. Messages API](https://portkey.ai/blog/open-ai-responses-api-vs-chat-completions-vs-anthropic-anthropic-messages-api)
49. [anthropic-sdk-python/src/anthropic/resources/beta/messages ...](https://github.com/anthropics/anthropic-sdk-python/blob/main/src/anthropic/resources/beta/messages/messages.py)
50. [JSON Results with Google Gemini Generative AI API Calls](https://www.raymondcamden.com/2024/04/17/json-results-with-google-gemini-generative-ai-api-calls)
51. [Google gemini generate_content is not working in python API using ...](https://stackoverflow.com/questions/78497434/google-gemini-generate-content-is-not-working-in-python-api-using-function-calli)
52. [Create a Message | ZenMux | Documentation](https://zenmux.ai/docs/api/anthropic/create-messages.html)
53. [Google Gemini Generate Content Schema - APIs.io](https://apis.io/schemas/google-gemini/google-gemini-generate-content/)
54. [HTTP Request to Gemini API fails with "contents is not specified ...](https://community.n8n.io/t/http-request-to-gemini-api-fails-with-contents-is-not-specified-despite-correct-configuration/208657?tl=en)
55. [Anthropic | AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/anthropic)
56. [Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-response/)
57. [Dealing with DeepSeek JSON Response Format Issues - Support](https://meta.discourse.org/t/dealing-with-deepseek-json-response-format-issues/384640?tl=en)
58. [Wrong GLM (China) preset base URL causes 404 with Anthropic ...](https://github.com/AndyMik90/Aperant/issues/1450)
59. [Add OpenAI Responses API Compatibility for Codex Desktop #245](https://github.com/deepseek-ai/awesome-deepseek-agent/issues/245)
60. [DeepSeek - Bifrost AI Gateway](https://docs.getbifrost.ai/providers/supported-providers/deepseek)
61. [DeepSeek-V4-Flash Now Supports the Responses API and Codex](https://apidog.com/blog/deepseek-v4-flash-responses-api-codex/)
62. [How to Use GLM 4.5 with Claude Code - Apidog](https://apidog.com/blog/glm-4-5-with-claude-code-2/)
63. [ZhipuAI API - 智谱AI](https://open.bigmodel.cn/dev/api)
64. [How to setup GLM-4.6 in Claude Code (The full, working method)](https://www.reddit.com/r/AIToolsPerformance/comments/1nvxa9k/how_to_setup_glm46_in_claude_code_the_full/)
65. [Pricing - Claude Platform Docs](https://docs.anthropic.com/en/docs/about-claude/pricing)
66. [Define tools - Claude Platform Docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use)
67. [Fine-grained tool streaming - Claude Platform Docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/fine-grained-tool-streaming)
68. [Conta token messaggio - Anthropic API](https://docs.anthropic.com/it/api/messages-count-tokens)
69. [Récupérer les Résultats du Lot de Messages - Anthropic](https://docs.anthropic.com/fr/api/retrieving-message-batch-results)
70. [Streaming Messages - Anthropic](https://docs.anthropic.com/en/api/messages-streaming?debug_url=1&debug=1&debug=true)
71. [Mensajes en Streaming - Anthropic](https://docs.anthropic.com/es/api/messages-streaming)
72. [Crear un Lote de Mensajes - Anthropic](https://docs.anthropic.com/es/api/creating-message-batches)
73. [Quickstart - Kimi API Platform](https://platform.kimi.ai/docs/api/quickstart)
74. [Moonshot AI - OpenClaw Docs](https://docs.openclaw.ai/providers/moonshot)
75. [Generated 2 API keys - All invalid for direct curl, use in OpenCode ...](https://github.com/MoonshotAI/Kimi-K2/issues/109)
76. [Kimi Code Docs](https://www.kimi.com/code/docs/en/)
77. [Providers and models | Kimi Code Docs](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/providers.html)
78. [Model dropdown greyed out when using Moonshot/Kimi API ...](https://discourse.devontechnologies.com/t/openai-compatible-model-dropdown-greyed-out-when-using-moonshot-kimi-api-category-devonthink-artificial-intelligence/86689)
79. [API not fully OpenAI-compatible - Kimi Forum](https://forum.moonshot.ai/t/api-not-fully-openai-compatible/67)
80. [Kimi k2.5 | AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/moonshot/kimi-k2-5)
81. [Introduction - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/api-reference/introduction)
82. [Z.ai API Platform — Start building with GLM-5.3](https://z.ai/chat)
83. [zhipuai-agent-to-openai/README.md at master - GitHub](https://github.com/LLM-Red-Team/zhipuai-agent-to-openai/blob/master/README.md)
84. [智谱AI GLM-4免费API直连指南：OpenAI兼容性实战配置-CSDN博客](https://blog.csdn.net/weixin_30197529/article/details/162160497)
85. [Z.ai Coding Plan API endpoint support #13965 - GitHub](https://github.com/CherryHQ/cherry-studio/discussions/13965)
86. [智谱 对话（OpenAI 兼容） - 数字先锋API文档](https://docs.cxsee.com/doc/view_106.html)
87. [智谱AI开放平台 GLM-5 API免费接入 2026最新大模型接口，ChatGLM智能...](https://aizhipu.com.cn/)
88. [Glm 4.7 - AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/zhipu/glm-4.7)
