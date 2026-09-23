# LLM 时代的 API 请求协议：一份面向工程实践的分类与对比指南

LLM API 并不存在一个真正统一的“行业标准”。表面上，许多服务都接收 `messages`、返回文本、支持流式输出和工具调用；但一旦进入多模态、工具循环、推理模型、结构化输出、会话状态与错误恢复，协议差异会直接影响 SDK 封装、网关设计、迁移成本和线上稳定性。

本文建立一个可操作的 taxonomy：先识别协议家族，再按关键维度比较 OpenAI、Anthropic、Google Gemini、DeepSeek 与智谱 GLM 等主流接口，最后给出多供应商适配时应抽象和不应抽象的边界。

***

## 1. 先建立正确认知

### 1.1 “兼容 OpenAI”通常不是“语义完全一致”

许多模型厂商称自己的 API “OpenAI-compatible”，通常意味着：

- 路径和基本请求形状接近，例如 `POST /v1/chat/completions`
- 使用 `model`、`messages`、`temperature`、`max_tokens`、`stream` 等常见字段
- 使用 `choices[0].message.content` 读取非流式结果
- 使用 SSE 返回 `data: ...` 与结束标记 `data: [DONE]`
- 工具调用近似 OpenAI Chat Completions 的 `tools`、`tool_calls` 与 `tool_call_id`

但这不是契约上的等价。兼容接口往往在以下方面存在实质差异：

- 支持的 role、role 顺序和相邻消息合并规则不同
- `content` 是字符串、数组，还是强类型内容块
- 工具调用参数是 JSON 字符串、JSON 对象，还是独立事件
- 思维链/推理内容以 `reasoning_content`、`thinking`、`reasoning`、`thought` 或不可见状态存在
- `temperature`、`top_p`、`tool_choice` 等字段可能被忽略、限制取值，或与推理模式冲突
- JSON 输出只是“要求 JSON”，还是“按 schema 严格约束”
- streaming 中 token、工具参数、使用量、停止原因和错误的事件结构不同
- 某些“兼容”层只覆盖最常用的文本对话，不能覆盖原生能力

因此，**API 的字段名相同，不代表行为、保证、成本或状态机相同**。

### 1.2 协议演进的核心方向

可以把 LLM API 的演进看成三个阶段：

1. **Prompt / Completion**
   - 输入：`prompt: string`
   - 输出：一段补全文本
   - 适合早期文本生成，但不能良好表示多轮对话、图像、工具或结构化中间状态。

2. **Chat / Messages**
   - 输入：`messages: [{role, content}]`
   - 输出：一个 assistant message 或 `choices`
   - 这是当前最广泛的互操作层；OpenAI Chat Completions、DeepSeek Chat Completions、智谱对话补全等基本属于该族。

3. **Item / Event / Agent Runtime**
   - 输入输出不再只是一问一答 message，而是由多种“对象”或“事件”组成，例如文本、推理、函数调用、函数结果、引用、文件、图像、浏览器操作等。
   - OpenAI Responses API 是典型代表：`input` / `output` 中是 typed items，而不只是 `messages`。
   - Google Gemini 的 `Content` / `Part` 模型与其工具调用结构，也天然更接近多模态对象图。
   - 该方向更适合 agent、长链路工具调用、多模态和可恢复执行。

OpenAI 对新项目推荐 Responses API，同时仍支持 Chat Completions；其迁移文档明确指出，Chat Completions 以 `messages` 作为输入和输出，而 Responses 使用由多种类型组成的 `input` 与 `output` items。[1][2]

***

## 2. 协议 taxonomy：不要只按厂商分类

工程上，最有价值的分类不是“OpenAI vs Anthropic vs Gemini”，而是下面六层。一个供应商的不同 endpoint 甚至可能分别属于不同层级。

| 层级 | 需要回答的问题 | 典型字段或对象 | 为什么重要 |
|---|---|---|---|
| 传输层 | 怎样发请求、怎样接收流 | HTTP、JSON、SSE、WebSocket、gRPC | 决定客户端、超时、断线恢复与代理能力 |
| 资源层 | 调用哪个 endpoint、资源是否可持久化 | `/chat/completions`、`/messages`、`/responses`、`/generateContent` | 决定 API 的心智模型 |
| 会话层 | 历史由谁保存 | 全量历史重传、`previous_response_id`、conversation/session ID | 决定状态、隐私、成本与可恢复性 |
| 内容层 | 一条消息能承载什么 | string、parts、content blocks、typed items | 决定多模态与工具结果如何编码 |
| 编排层 | 如何定义、选择和回传工具 | `tools`、`tool_calls`、`tool_use`、`functionCall` | 决定 agent loop 的状态机 |
| 控制与观测层 | 怎样约束、终止、计费和排错 | JSON schema、finish reason、usage、request ID、safety metadata | 决定可靠性、成本控制与审计 |

以下四类协议家族，是理解市场上多数 LLM API 的最短路径：

| 协议家族 | 核心抽象 | 典型代表 | 最适合的使用方式 |
|---|---|---|---|
| OpenAI Chat Completions 风格 | `messages` + `choices` | OpenAI Chat Completions、DeepSeek、智谱、众多推理托管商 | 统一文本聊天、快速兼容、存量迁移 |
| OpenAI Responses 风格 | `input` / `output` typed items | OpenAI Responses、部分厂商的兼容实现 | 新建 agent、原生工具、状态与复杂输出 |
| Anthropic Messages 风格 | 顶层 `system` + `messages` + content blocks | Claude Messages API | 强内容块建模、显式工具循环、Claude 原生能力 |
| Gemini GenerateContent 风格 | `contents[]` + `parts[]` + `candidates[]` | Google Gemini API | 多模态、Google 工具生态、Gemini 原生能力 |

***

## 3. 主流协议的速览对比

下表把“一个简单的用户问题”放入各自的原生心智模型中。示例仅用于显示结构，不代表每项能力在每个模型版本中均可用。

| 平台 / 协议 | 典型 endpoint | 指令位置 | 用户输入模型 | 主要输出入口 | 会话状态默认值 |
|---|---|---|---|---|---|
| OpenAI Chat Completions | `/v1/chat/completions` | `system` / `developer` message | `messages[]` | `choices[].message` | 调用方重传历史 |
| OpenAI Responses | `/v1/responses` | 顶层 `instructions`，也可用 input items | `input: string \| items[]` | `output[]` typed items | 可用 `previous_response_id`、Conversations 或自行回放 output |
| Anthropic Messages | `/v1/messages` | 顶层 `system` | `messages[]` | `content[]` blocks | 调用方重传历史 |
| Google Gemini GenerateContent | `models/{model}:generateContent` | `systemInstruction` | `contents[].parts[]` | `candidates[].content.parts[]` | REST 默认无状态，调用方重传历史 |
| DeepSeek Chat Completions | `/chat/completions` | `system` message | `messages[]` | `choices[].message` | 调用方重传历史 |
| 智谱 GLM 对话补全 | `/paas/v4/chat/completions` | `system` message | `messages[]` | `choices[].message` | 调用方重传历史 |

OpenAI 的 Chat Completions 请求包含 `messages`；Responses 改为 `input` 与 typed `output`，并提供 `previous_response_id`、手工回放 output、Conversations API 三种常见的多轮状态管理路径。 Gemini 的 `generateContent` 使用 `contents[]`，每个 content 由 `role` 和有序的 `parts[]` 组成；其 REST 接口是无状态的，调用方需传入完整历史。[1][3][4]

### 3.1 四个最重要的“对象形状”

#### A. OpenAI Chat Completions：消息数组

```json
{
  "model": "example-model",
  "messages": [
    {
      "role": "system",
      "content": "你是一名严谨的技术助手。"
    },
    {
      "role": "user",
      "content": "解释什么是向量数据库。"
    }
  ],
  "temperature": 0.2
}
```

典型响应：

```json
{
  "id": "chatcmpl_xxx",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "向量数据库用于存储和检索向量表示……"
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

这是最容易被下游厂商复刻的形状，因此生态最大。其缺点也明显：文本回答、工具调用、推理、图像、音频等不同语义常被塞进 `message`、`tool_calls`、nullable `content` 和各种扩展字段中，复杂度逐渐累积。

#### B. OpenAI Responses：输入和输出都是类型化对象

```json
{
  "model": "example-model",
  "instructions": "你是一名严谨的技术助手。",
  "input": "解释什么是向量数据库。"
}
```

概念响应：

```json
{
  "id": "resp_xxx",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "向量数据库用于存储和检索向量表示……"
        }
      ]
    }
  ]
}
```

重点不在字段名，而在对象模型：

- `message` 只是 item 的一种
- 还可能有 `reasoning`、`function_call`、`function_call_output` 等 item
- 输出顺序本身有语义
- 下一轮既可传 `previous_response_id`，也可将前一轮 `output` 回放到输入
- 要读取纯文本，应用往往不能再硬编码 `choices[0].message.content`

OpenAI 的迁移文档明确把 `message` 描述为 Responses item 的一种类型，并列出 reasoning、function call 和 function-call output 等同级对象。[1]

#### C. Anthropic Messages：顶层 system + 内容块

```json
{
  "model": "claude-example",
  "max_tokens": 1024,
  "system": "你是一名严谨的技术助手。",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "解释什么是向量数据库。"
        }
      ]
    }
  ]
}
```

概念响应：

```json
{
  "id": "msg_xxx",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "向量数据库用于存储和检索向量表示……"
    }
  ],
  "stop_reason": "end_turn"
}
```

Anthropic 的核心特点：

- `system` 不作为 `messages` 里的普通 role，而是顶层字段
- `content` 可为字符串，也可为强类型 block 数组；字符串只是单个 text block 的简写
- 助手输出天然是 blocks 数组，文本、工具调用等可并列
- 客户端需要按 block 类型处理，而不是假定只有一个文本字段

Anthropic Messages API 的官方参考将请求定义为带文本或图像内容的结构化消息列表；消息 content 可以是字符串或带类型的内容块数组。[5]

#### D. Gemini GenerateContent：Content / Part 的多模态对象模型

```json
{
  "systemInstruction": {
    "parts": [
      {
        "text": "你是一名严谨的技术助手。"
      }
    ]
  },
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "解释什么是向量数据库。"
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.2
  }
}
```

概念响应：

```json
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "向量数据库用于存储和检索向量表示……"
          }
        ]
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 100,
    "candidatesTokenCount": 200,
    "totalTokenCount": 300
  }
}
```

Gemini 的关键抽象是：

- `Content`：一轮发言，由 `role` 和多个 `parts` 组成
- `Part`：文本、内联二进制数据、文件 URI、函数调用、函数结果等
- `Candidate`：候选生成结果；需结合 `finishReason`、safety 和 grounding 元数据判断可用性
- `contents` 是完整对话历史，不是仅当前用户问题

Gemini 官方文档将 `contents[]` 定义为当前会话内容，多轮时包含历史与最新请求；响应候选项携带 `content`、`finishReason`、安全评级、引用或 grounding 元数据等。[3]

***

## 4. 关键差异：逐层拆解

### 4.1 指令与角色：`system` 不是可互换的字符串

角色字段看起来简单，却是迁移中最容易产生行为偏差的区域。

| 协议 | 指令的规范位置 | 常见角色 | 工程含义 |
|---|---|---|---|
| OpenAI Chat Completions | `system` / `developer` message | `system`、`developer`、`user`、`assistant`、`tool` | 指令与历史同在 messages 序列中 |
| OpenAI Responses | `instructions` 或 input items | 取决于 item / message 类型 | `instructions` 是独立的高优先级控制面 |
| Anthropic Messages | 顶层 `system` | 通常 `user`、`assistant`；工具结果通过 content block 表达 | 不能机械地把 system message 直接塞回 messages |
| Gemini | `systemInstruction` | `user`、`model` | 助手角色叫 `model`，不是 `assistant` |
| DeepSeek / 智谱 | 多为 `system` message | `system`、`user`、`assistant`、`tool` | 接近 OpenAI Chat，但支持范围应按模型检查 |

OpenAI 文档说明，`instructions` 用于模型行为、目标、语气与示例等高层控制，且优先级高于 `input` 中的提示内容。 这意味着从 Chat Completions 迁移到 Responses 时，不应只是把 `messages` 改名为 `input`；应当把稳定的系统策略从历史消息中分离为 `instructions`，并理解它与状态复用的关系。[2]

**常见误区：**

- 把 Anthropic 的顶层 `system` 直接变成一条 `{"role":"system"}` message，再期望完全同样的提示行为。
- 把 Gemini 的 `model` role 改成 `assistant`，或反之。
- 在多轮消息中反复插入系统指令，导致上下文膨胀或指令冲突。
- 使用兼容层时默认所有 role 都被支持；很多服务实际仅支持 `system/user/assistant/tool` 子集。

### 4.2 内容模型：字符串、parts、blocks、items 的区别

可以把内容模型从弱到强排列：

```text
string
  → message.content: string | parts[]
    → message.content: typed content blocks[]
      → input/output typed items[]
```

| 表达模型 | 优点 | 限制 | 常见平台 |
|---|---|---|---|
| 纯字符串 | 最简单；便于快速接入 | 无法自然表达图像、文件、工具、引用 | 早期 completion |
| `content` 字符串或数组 | 可渐进支持多模态 | block 类型常受 OpenAI 形状约束 | Chat Completions 生态 |
| typed blocks | 文本、图像、工具、缓存等语义明确 | 适配器需要逐类转换 | Anthropic Messages |
| typed items | 整个执行轨迹可结构化表达 | 客户端状态机更复杂 | OpenAI Responses |

不要将“多模态”理解成在文本 prompt 中嵌一个 URL。真正的协议差异包括：

- 图片是 URL、base64 data URL、上传文件 ID、文件 URI，还是 inline bytes
- 文件是否必须先上传
- 音频/视频是输入 part、独立 endpoint，还是实时会话事件
- 文本与图片的顺序是否保留并影响语义
- 工具调用是否也属于 content 的一个 block
- 是否可以把上轮模型原样输出的 block 回传，形成可恢复上下文

DeepSeek Chat Completions 已支持用户内容为字符串或内容部件数组，包括 `text`、`image_url` 与文件相关字段；这表明它在表面上属于 OpenAI Chat 风格，但其具体部件类型、可用模型与限制仍是供应商特定的。[6]

### 4.3 会话状态：无状态 HTTP 不等于无状态应用

LLM API 的 HTTP 调用通常是无状态的，但“对话”必须有状态。实际可分三种：

| 状态策略 | 做法 | 优点 | 风险 |
|---|---|---|---|
| 客户端全量重传 | 每次把完整消息历史带上 | 最可控、跨供应商、便于审计 | token 成本高；需自行裁剪和总结 |
| 供应商引用上轮结果 | 如 `previous_response_id` | 请求较短；可保留复杂中间对象 | 锁定供应商；有存储、保留和重试语义 |
| 供应商会话资源 | conversation / thread / session | 支持长期 agent 与协作对象 | 生命周期、权限、版本与可观察性更复杂 |

最稳妥的跨厂商架构是：**你的系统是会话的事实来源，供应商状态只是性能或便利性优化。**

建议保留一个供应商中立的内部事件日志，例如：

```json
[
  {"kind": "instruction", "text": "回答必须简洁并给出来源"},
  {"kind": "user_text", "text": "北京天气怎么样？"},
  {
    "kind": "tool_call",
    "call_id": "call_001",
    "name": "get_weather",
    "arguments": {"city": "北京"}
  },
  {
    "kind": "tool_result",
    "call_id": "call_001",
    "content": {"temperature_c": 25, "condition": "晴"}
  },
  {"kind": "assistant_text", "text": "北京当前……"}
]
```

在调用前，再将内部事件投影为 OpenAI、Anthropic、Gemini 或其他供应商要求的具体协议。这样可以保留审计能力，也能在切换供应商时重新编译历史，而非依赖某个厂商不可迁移的 conversation ID。

### 4.4 工具调用：最容易被“伪兼容”坑到的领域

工具调用绝不等于“模型返回一段 JSON”。它是一个闭环状态机：

```text
定义工具
→ 发起模型请求
→ 模型请求调用工具
→ 验证并执行工具
→ 将工具结果按原始 call ID 回传
→ 再次请求模型
→ 模型给出最终回答，或再次调用工具
```

#### OpenAI Chat Completions 风格

模型返回：

```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_weather_1",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"city\":\"北京\"}"
      }
    }
  ]
}
```

应用执行工具后，回传：

```json
{
  "role": "tool",
  "tool_call_id": "call_weather_1",
  "content": "{\"temperature_c\":25,\"condition\":\"晴\"}"
}
```

注意：`arguments` 通常是 JSON **字符串**，而不是已解析的对象；必须在执行前解析、做 schema 验证、鉴权与业务校验。

#### Anthropic Messages 风格

工具调用通常表现为 assistant content 中的 `tool_use` block，工具结果作为 user message 的 `tool_result` block 回传。其重点是**工具请求和工具结果都嵌在内容块中**，不是单独的 `role: tool` 消息。

#### Gemini 风格

Gemini 可在 `parts` 中返回 `functionCall`，调用方把 `functionResponse` 作为后续 `Content` 中的 part 发送回去。函数调用与函数结果是 `Part` 的不同联合类型。

#### Responses 风格

OpenAI Responses 将调用和结果提升为 item，例如 `function_call` 与 `function_call_output`。这更接近“执行日志”，而不是“聊天消息附加字段”。

**跨协议的最低共同原则：**

- 不把工具参数当作可信输入。
- 对每个 call 保存原始 provider ID；回传时严格关联。
- 一次响应可能包含多个工具调用。
- 流式输出中，函数参数可能是分片到达的；必须缓冲并在完成后解析。
- 工具执行要有超时、幂等键、重试策略和审计日志。
- 工具结果过大时要截断、存外部对象或摘要，否则会挤占上下文并抬升成本。
- 不要假定 tool call 后一定会得到自然语言“最终回答”；模型可能继续请求工具。

DeepSeek 的 Chat Completions 文档支持 `tools`、`tool_choice` 和 `tool_calls`，但也明确指出 thinking mode 下不支持 `required` 与指定工具名的强制选择；这是“字段存在但语义受模式约束”的典型例子。[6]

### 4.5 推理模型与思维链：字段可见性不是标准能力

推理模型引入了额外复杂度：

| 形态 | 可能的协议表示 | 集成建议 |
|---|---|---|
| 不暴露推理 | 仅返回最终文本 | 最简单；不要假定模型没有内部推理 |
| 公开 reasoning 字段 | `reasoning_content`、`thinking` 等 | 将其视为供应商专有扩展 |
| 不透明推理状态 | 加密或内部 item；后续调用可复用 | 原样保存和回传，不要修改 |
| 可配置推理预算 | `reasoning_effort` 等 | 这是性能/成本控制面，不应假定跨厂商可映射 |

DeepSeek 的 Chat Completions 接口暴露 `thinking` 和 `reasoning_effort`，且响应可包含 `reasoning_content`；文档同时注明部分采样参数在不同思考模式下会失效或被固定处理。 智谱也提供 `thinking`、`reasoning_effort` 与 `clear_thinking` 等控制，并在流式响应中定义 `reasoning_content`；如果要保留跨轮推理上下文，文档要求完整、未修改、按原顺序透传历史推理内容。[6][7]

因此，应用层应区分三种内容：

1. **面向用户的可展示文本**：可以渲染、索引和进入聊天记录。
2. **工具控制信息**：只供编排器消费。
3. **模型专有推理状态**：按供应商文档决定是否存储、是否加密、是否原样回传；不要自行拼接、翻译或作为用户文本显示。

### 4.6 结构化输出：`json_object` 不等于可靠 JSON Schema

结构化输出能力至少有四个成熟度等级：

| 等级 | 含义 | 可靠性 |
|---|---|---|
| Prompt 约束 | “请只输出 JSON” | 最低；可能夹带 Markdown 或解释 |
| JSON mode | API 保证是可解析 JSON | 只保证语法，不必然满足业务 schema |
| JSON Schema / Structured Outputs | 输出须满足给定 schema | 较高，但仍需验证 |
| 工具调用 | 模型按函数参数 schema 生成参数 | 适合动作和受控数据提取 |

DeepSeek 的 `response_format: {"type":"json_object"}` 保证生成结果是有效 JSON，但官方也要求调用方在 system 或 user prompt 中明确要求输出 JSON；否则模型可能输出持续空白直至达到 token 上限。即使是 JSON mode，仍可能因 `finish_reason: "length"` 被截断。[6]

**生产建议：**

- 任何模型输出都要通过 JSON parser 和业务 schema 二次验证。
- JSON 解析失败时，不要直接重试同一个请求；优先使用“修复 JSON”提示、降低输出长度、加强 schema 或切换到工具调用。
- 如果输出驱动写库、付款、发邮件、权限变更等副作用，必须增加业务规则验证和人工/策略审批。
- 不要把 `<think>`、代码块围栏、额外解释文字当作稳定协议；它们不是结构化输出。

### 4.7 流式输出：SSE 一样，事件语义不一样

很多 API 都使用 Server-Sent Events，但不能因为都叫“stream”就复用同一个 parser。

| 协议形态 | 典型流式内容 | 消费策略 |
|---|---|---|
| Chat Completions | `choices[].delta.content`、`delta.tool_calls` | 按 choice/index 拼接文本和工具参数 |
| Anthropic Messages | 事件类型区分 message、content block、delta、stop | 按 block 生命周期管理 |
| Gemini | 连续 `GenerateContentResponse` 或 SDK chunk | 合并 candidate/content/part，并处理安全与结束原因 |
| Responses | typed response events | 按事件类型处理文本、函数调用、完成、错误 |

OpenAI Chat Completions 返回 chat completion chunk；DeepSeek 同样采用 SSE `data:` 帧，并以 `data: [DONE]` 终止。其流式工具调用中，首个 chunk 可携带 ID、类型和函数名，后续 chunk 只补充 `arguments` 片段。 智谱的文档也说明 `stream: true` 使用 SSE，结束时返回 `data: [DONE]`，且 `tool_calls` 可逐步生成。[6][7]

**正确的流式实现应做到：**

- 基于 UTF-8 字节流和 SSE 帧解析，而不是按 TCP chunk 或行直接拼接。
- 将展示文本与控制数据分开累计。
- 对多个并行 tool calls 按 `index` / call ID 分桶。
- 等到参数完整且流结束后再做 JSON 解析。
- 不把 `[DONE]` 当作“调用成功”；还要检查 finish reason、错误事件、内容安全与 usage。
- 记录首 token 时间、完成时间、取消原因与最终 usage。
- 客户端断开后要决定：取消上游请求、后台继续、还是保存可恢复 ID。

***

## 5. DeepSeek 与智谱：为何“OpenAI 兼容”仍有显著差异

### 5.1 DeepSeek：主接口接近 Chat Completions，但有原生扩展和多协议入口

DeepSeek 的主 Chat Completions endpoint 是 `POST /chat/completions`，其 `messages` 支持 `system`、`user`、`assistant` 与 `tool` 角色，整体形状接近 OpenAI Chat Completions。[6]

但至少有以下不应忽略的差异：

| 维度 | DeepSeek 的表现 | 对接影响 |
|---|---|---|
| 思考控制 | `thinking` 与 `reasoning_effort` | 需要按模式调整工具和采样配置 |
| 推理返回 | `reasoning_content` 可与最终 content 分离 | UI、存储与回放不能只保存 `content` |
| 参数生效 | thinking / non-thinking 模式下，`temperature`、`top_p` 的有效性不同 | “同一参数”不一定产生可比行为 |
| JSON mode | `json_object` 仍要求 prompt 明确要求 JSON | 不能把 API 开关当作完整协议保证 |
| 工具限制 | thinking mode 对强制或指定工具选择有限制 | agent 策略要能降级 |
| 多协议能力 | 提供 OpenAI/Anthropic 兼容入口，亦支持 Responses 格式 | 不能只靠 base URL 切换就假设功能等价 |

DeepSeek 的首页声明其 API 兼容 OpenAI/Anthropic 格式，配置不同 base URL 即可使用相关 SDK；同时其 Responses API 文档把 OpenAI 的 Responses 定义作为完整格式参考，并列出实际支持度。 这意味着“兼容”应被理解为**适配入口**，而不是承诺与原厂所有字段、事件和行为完全一致。[8][9]

尤其需要注意工具历史。DeepSeek 文档指出，Chat Completion API 不支持在对话中途插入 tool calls；若需要插入工具调用，应使用 Anthropic API 或 Responses API。 这是一个典型的状态回放差异：你的内部会话日志若允许任意重排或补写工具事件，就不能保证能投影回所有 Chat Completions 兼容端点。[10]

### 5.2 智谱 GLM：形状接近 OpenAI，能力与约束高度模型化

智谱的对话补全 endpoint 为 `/paas/v4/chat/completions`，其文本请求以 `model` 和 `messages` 为核心，支持 `system`、`user`、`assistant`、`tool` 四种角色；工具调用使用 `tool_calls` 与 `tool_call_id`，整体上属于 OpenAI Chat Completions 家族。[7]

但与 OpenAI 官方接口相比，至少应关注：

| 对比点 | 智谱 GLM 文档中的特点 | 对集成的影响 |
|---|---|---|
| 工具类型 | 除 function 外，文档列出 web search、retrieval、MCP 等能力 | 不能将所有工具都抽象成纯本地 function |
| 推理控制 | `thinking.type`、`reasoning_effort`、`clear_thinking` | 需要定义是否保留历史 reasoning 的策略 |
| 采样开关 | `do_sample` 可使 `temperature` 与 `top_p` 被忽略 | 参数层要保留供应商专用表达 |
| 温度范围 | 文档限制为 `[0, 1]` | 不可把别家 `0~2` 的参数原样透传 |
| 输出限制 | `response_format` 收敛为 `text` / `json_object` | schema 级结构化输出需另行设计 |
| 结束原因 | 包含 `sensitive`、`network_error`、`model_context_window_exceeded` 等 | 应把厂商枚举映射为内部分类，而非硬编码 `stop/length/tool_calls` |
| 流式思维内容 | `delta.reasoning_content` 可单独出现 | 渲染器与持久化层需区分可见与不可见内容 |

智谱文档说明，`messages` 应包含完整上下文；工具响应使用 `tool_call_id` 关联 assistant 的调用；流式 `delta` 可能包含文本、`reasoning_content` 或逐步生成的 `tool_calls`。[7]

### 5.3 智谱与 Anthropic Messages 的实质差别

“智谱的 message 对比 Anthropic 官方的不同”不能只回答 role 名称不同。两者的**内容与工具状态机**不同：

| 项目 | 智谱 GLM 对话补全 | Anthropic Messages |
|---|---|---|
| 总体家族 | OpenAI Chat Completions 风格 | Anthropic 原生 Messages 风格 |
| 系统指令 | `messages` 中的 `role: "system"` | 顶层 `system` 字段 |
| 文本 content | 常见为字符串；多模态时可为数组 | string 或 typed blocks；string 是 text block 简写 |
| 助手工具请求 | `assistant.tool_calls[]` | assistant `content[]` 中的 `tool_use` block |
| 工具结果 | `role: "tool"` + `tool_call_id` + content | user `content[]` 中的 `tool_result` block |
| 助手回复读取 | `choices[0].message.content` | `content[]`，需筛选 `type: "text"` |
| 流式解析 | `choices[].delta` | block 生命周期与 delta 事件 |
| 指令迁移 | system message 基本可保留 | 应拆到顶层 `system`，不能机械转为 message |

Anthropic 的设计中，content block 是协议的一等公民；工具调用不是 Chat Completion message 上的附加数组，而是助手输出的一个内容块类型。官方参考也明确规定，Messages 创建请求发送结构化的消息列表，支持文本或图像内容。[5]

**结论：**将智谱接口适配到 Anthropic SDK，或将 Claude 接入一个 OpenAI 风格网关，不能只写字段重命名。至少要进行：

- role 映射；
- 系统指令位置重组；
- text / image / tool content block 转换；
- tool call ID 映射；
- 工具结果 role 变换；
- 流事件状态机转换；
- finish/stop reason 归一化；
- usage、缓存与 reasoning 字段的降级或扩展保存。

***

## 6. 下游模型厂商的适配模式

市场上的下游模型服务常见四种适配策略。了解它们能帮助你判断：该使用官方 SDK、统一网关，还是自建 adapter。

### 模式 A：OpenAI Chat Completions 兼容层

**形态：**

```text
POST /v1/chat/completions
{
  "model": "...",
  "messages": [...],
  "tools": [...],
  "stream": true
}
```

**优点：**

- 最低迁移成本。
- 现有 OpenAI SDK、LangChain、LiteLLM 等工具通常可较快接入。
- 文本对话、基础图片输入、工具调用的共同子集较容易统一。

**风险：**

- 同名参数的默认值、范围和实际生效逻辑不同。
- 视觉、音频、JSON schema、推理、缓存、批处理和实时协议可能并不兼容。
- 模型枚举、错误码、限流头、usage 字段和 finish reason 会漂移。
- 有的兼容层仅接受格式，但悄悄忽略未知字段；这是最难排查的失败模式。

### 模式 B：Anthropic `/messages` 兼容层

**形态：**

```text
POST /v1/messages
{
  "model": "...",
  "system": "...",
  "messages": [...],
  "tools": [...]
}
```

**优点：**

- 更适合 Claude SDK、Claude Code 或 content-block-first 的客户端。
- 工具调用和多模态对象的表达通常更自然。

**风险：**

- 参数、prompt caching、思维块、stream event 版本与停止原因未必完整复刻。
- 服务商可能在网关侧把 Anthropic 请求转换为自己的原生格式；转换损失会发生在边界层，而非你的代码中。

例如，部分第三方网关会明确说明其 GLM endpoint “兼容 Anthropic Claude `/messages` API”，并由网关自动转换 Anthropic 请求格式；这种描述本身就说明兼容性是网关映射，而非模型原生协议等价。[11]

### 模式 C：原生多模态协议

**代表：**Gemini GenerateContent 及其他各厂商原生接口。

**优点：**

- 最容易使用该平台的最新多模态、grounding、文件、原生工具与安全能力。
- 协议通常更贴合模型能力，而不是受兼容层限制。

**风险：**

- 厂商锁定更强。
- 统一网关需要更强的内容模型和状态机。
- 需要专门测试角色规则、文件传输、工具结果和安全元数据。

### 模式 D：Agent / Responses / 运行时协议

**代表：**OpenAI Responses、各种 agent runtime、MCP 相关运行时接口。

**优点：**

- 原生支持多步骤执行、工具轨迹、引用、推理状态、持久会话或托管工具。
- 更适合复杂 agent，而不是只做“聊天框”。

**风险：**

- 表面 API 更简单，但应用的事件处理、状态管理、幂等与观测要求更高。
- 供应商托管状态会带来保留、删除、重试、区域与合规问题。
- 很难通过“最低共同分母”完整抽象。

***

## 7. 一个实用的跨供应商内部协议

如果你的产品确实要同时支持多个供应商，推荐建立“内部规范化事件模型”，而不是把任一家请求 JSON 当作内部数据结构。

### 7.1 建议的内部对象

```ts
type ConversationEvent =
  | {
      kind: "instruction";
      text: string;
      scope: "session" | "turn";
    }
  | {
      kind: "user_message";
      parts: InputPart[];
    }
  | {
      kind: "assistant_message";
      parts: OutputPart[];
      providerMetadata?: Record<string, unknown>;
    }
  | {
      kind: "tool_call";
      callId: string;
      name: string;
      argumentsJson: string;
    }
  | {
      kind: "tool_result";
      callId: string;
      result: ToolResultPart[];
      isError?: boolean;
    }
  | {
      kind: "provider_state";
      provider: string;
      opaque: unknown;
    };

type InputPart =
  | { type: "text"; text: string }
  | { type: "image_url"; url: string }
  | { type: "file_ref"; id: string; mimeType?: string }
  | { type: "audio"; dataRef: string; mimeType: string };

type OutputPart =
  | { type: "text"; text: string }
  | { type: "citation"; source: string; label?: string }
  | { type: "tool_use"; callId: string; name: string; argumentsJson: string }
  | { type: "refusal"; text: string };
```

这个内部模型有几个刻意的设计：

- `instruction` 与普通用户消息分离。
- `parts` 允许多模态，而不是把内容锁死为 string。
- 工具调用与工具结果成为独立事件，且通过稳定的 `callId` 关联。
- `argumentsJson` 保留原始文本，避免解析—序列化导致精度、顺序或供应商签名变化。
- `provider_state` 用于保存无法跨供应商解释的 opaque state，例如某些 reasoning token、加密 item、conversation ID 或 thought signature。
- 用户可见文本与供应商专有状态分离。

### 7.2 Adapter 的职责

每个 provider adapter 至少应实现：

| 能力 | 作用 |
|---|---|
| `compileRequest()` | 内部事件 → 厂商请求 JSON |
| `parseResponse()` | 厂商响应 → 内部 assistant/tool/usage 事件 |
| `parseStream()` | 厂商 SSE / event stream → 增量内部事件 |
| `capabilities()` | 声明模型支持的输入、工具、JSON、流式、状态等能力 |
| `normalizeError()` | HTTP / SDK / provider error → 内部错误分类 |
| `estimateOrReadUsage()` | 统一输入、输出、缓存、推理 token 与成本记录 |
| `replayPolicy()` | 决定历史能否完全回放、是否需要 opaque state |

不要让业务代码出现这种逻辑：

```ts
if (provider === "x") {
  return response.choices[0].message.content;
}
```

而要让业务层消费统一的流：

```ts
for await (const event of modelGateway.generate(request)) {
  if (event.kind === "text_delta") render(event.text);
  if (event.kind === "tool_call_ready") await executeTool(event);
  if (event.kind === "completed") recordUsage(event.usage);
}
```

***

## 8. 兼容性能力矩阵：在路由前判断，而不是在报错后修补

供应商与模型的能力应以“模型版本 × endpoint × 区域 × 账户权限”为单位管理，而不是以“厂商”管理。

建议维护类似如下的注册表：

| 能力 | 需要记录的细项 |
|---|---|
| 文本输入 | 最大上下文、最大输出、语言与编码限制 |
| 图像输入 | URL / base64 / file ID / 文件 URI，支持格式与大小 |
| 音频 / 视频 | 输入、输出、实时与否、文件限制 |
| 工具调用 | 本地函数、并行调用、强制调用、严格 schema、流式参数 |
| 结构化输出 | JSON mode、JSON schema、工具 schema |
| 推理控制 | 是否支持、字段、是否可见、历史是否必须保留 |
| 流式输出 | SSE 事件模型、usage 是否在最后一帧、取消协议 |
| 会话 | 全量重传、response ID、conversation/session 资源 |
| 安全 | 拒答、内容过滤、可用安全元数据 |
| 缓存 | 自动缓存、显式断点、usage 中命中字段 |
| 可观测性 | request ID、trace ID、system fingerprint、模型版本 |
| 数据治理 | 是否默认存储、保留时长、区域、ZDR / 零数据保留选项 |

调用前先做 capability negotiation，例如：

```json
{
  "required": {
    "streaming": true,
    "toolCalling": true,
    "parallelToolCalls": true,
    "jsonSchema": true,
    "imageInput": false
  },
  "preferred": {
    "providerManagedState": false,
    "reasoningVisible": false
  }
}
```

路由器据此选择模型，或明确返回“该模型不支持所需能力”，而不是把不支持的字段静默删除。

***

## 9. 参数映射：哪些可以抽象，哪些不该强行统一

### 9.1 相对适合统一的参数

以下参数可作为内部通用参数，但仍要让 adapter 做能力校验和范围转换：

| 内部参数 | 常见外部名称 | 注意事项 |
|---|---|---|
| `model` | `model` | 模型名不跨供应商通用 |
| `maxOutputTokens` | `max_tokens`、`max_output_tokens` | 输入/输出限制的定义可能不同 |
| `temperature` | `temperature` | 范围与推理模式下的生效性不同 |
| `topP` | `top_p` | 不要与 temperature 同时盲调 |
| `stopSequences` | `stop` | 数量和长度限制不同 |
| `stream` | `stream` | 传输相同不代表事件相同 |
| `tools` | `tools`、`functionDeclarations` | schema 方言与工具类别不同 |
| `structuredOutput` | `response_format`、schema config | JSON mode 和 schema 保证不能混为一谈 |

### 9.2 不建议伪装成通用参数的能力

以下能力应保留为 provider-specific extension，或定义高级能力接口并允许“不支持”：

- `reasoning_effort`
- `thinking` 开关与 reasoning 保留策略
- prompt caching breakpoint / TTL
- Google grounding、引用和搜索配置
- hosted tools、computer use、browser use
- 供应商 conversation/thread/session ID
- prediction/prefix completion
- 图像 detail、视频抽帧、音频语音选择
- logprobs 的返回形状
- 供应商安全策略与内容过滤开关
- 队列、批处理、异步任务的生命周期

一个良好的抽象不是“隐藏一切差异”，而是：

1. 统一稳定且真正同义的共同能力；
2. 显式表达能力缺失；
3. 让原生能力以受控扩展方式存在；
4. 保留原始请求、响应和事件，便于排错与升级。

***

## 10. 生产集成的高频陷阱

### 10.1 只取 `choices[0].message.content`

这只适用于部分 Chat Completions 的非流式文本路径。会遗漏：

- 多个 choice 或 candidate
- content blocks 中的多个文本段
- refusal、citation、工具调用
- Responses 中的多个 output item
- reasoning 与最终答案的分离
- multimodal output

应实现“从供应商响应提取规范化事件”的 parser，而不是到处写字段访问。

### 10.2 将工具参数直接 `JSON.parse()` 后执行

模型输出即使看起来符合 schema，也仍可能：

- 非法 JSON
- 缺字段或字段类型不正确
- 包含未定义参数
- 包含越权资源 ID
- 重复触发可能造成副作用的动作
- 被提示注入诱导调用危险工具

正确流程：

```text
收集完整参数
→ JSON parse
→ JSON Schema 校验
→ 业务权限校验
→ 风险策略检查
→ 幂等性检查
→ 执行工具
→ 脱敏并限制工具结果
→ 通过对应 call ID 回传
```

### 10.3 忽略 stop / finish reason

“HTTP 200”只说明请求成功处理，不说明回答完整或可用。至少应区分：

| 内部归一化原因 | 可能的外部枚举 |
|---|---|
| `completed` | `stop`、`end_turn`、`STOP` |
| `needs_tool` | `tool_calls`、`tool_use`、function call |
| `truncated` | `length`、`MAX_TOKENS` |
| `safety_blocked` | `content_filter`、`sensitive`、safety block |
| `context_exceeded` | provider-specific context error / finish reason |
| `cancelled` | aborted / client cancel |
| `provider_failure` | resource/network/internal errors |

DeepSeek 明确将 `stop`、`length`、`content_filter`、`tool_calls`、`insufficient_system_resource` 与 `aborted` 区分为不同结束原因。 智谱还列出 `sensitive`、`network_error`、`model_context_window_exceeded` 等情形。[6][7]

### 10.4 把系统 prompt、用户数据、工具结果混在一个字符串里

这样做短期容易，长期会损失：

- 权限边界
- 审计可追溯性
- 提示注入防护空间
- 多模态与工具协议能力
- 上下文裁剪质量
- 供应商迁移能力

至少应将 instruction、user input、retrieved context、tool result、assistant output 作为不同内部事件处理。

### 10.5 未保存原始 provider 响应

规范化后仍建议保存受控、脱敏后的原始请求/响应或可重放记录，原因包括：

- 发现模型版本或网关行为漂移
- 排查 adapter 漏字段
- 对比不同供应商的工具调用差异
- 复现流式拼接问题
- 审计内容安全与用户投诉
- 估算 token 与缓存成本

注意日志中不得直接记录 API key、完整个人数据、未授权文件内容或敏感工具结果。

### 10.6 把“上下文窗口”当作唯一 token 限制

至少要分别追踪：

- 输入 token
- 输出 token
- reasoning token
- 工具定义 token
- 工具结果 token
- 缓存命中 / 未命中 token
- 图像、音频、视频的计费换算
- 系统指令与服务端注入上下文的成本

DeepSeek 的 usage 结构会额外给出 prompt cache hit / miss token 与 reasoning token 等细分；这类字段不能简单压扁为一个 total token 后就丢弃。[6]

***

## 11. 推荐的实现路线

### 路线一：单一供应商、简单文本聊天

适合 MVP、内部工具或低复杂度问答。

- 直接使用供应商官方 SDK。
- 选定一种主 API，不要同时混用多个 endpoint。
- 记录 model、request ID、usage、finish reason。
- 实现超时、重试、限流退避和内容截断。
- 仅当确有需要时再引入工具调用和多模态。

对于新 OpenAI 项目，优先评估 Responses API；若存量代码、第三方生态或简单聊天场景依赖 Chat Completions，后者仍可继续使用。[1][12]

### 路线二：多供应商、以文本和基础工具为主

适合希望在模型质量、成本、可用性之间路由的产品。

- 定义内部 message/part/tool 事件模型。
- 为每种协议家族实现独立 adapter。
- 在路由前做 capability check。
- 内部保存完整会话事实，避免依赖供应商会话 ID。
- 统一 trace、usage、错误和重试策略。
- 不把供应商专有字段强塞入公共 DTO；提供 `extensions`。

### 路线三：复杂 agent、原生工具、多模态和长流程

适合 coding agent、研究 agent、业务工作流自动化。

- 使用事件溯源式的 conversation log。
- 工具调用使用显式状态机和幂等执行。
- 实现可恢复 run：保存 request、call ID、工具结果、provider state。
- 将用户可见流与编排控制流分开。
- 区分无副作用工具与有副作用工具；后者加入审批、策略和审计。
- 保留厂商原生路径；不要试图用 OpenAI Chat Completions 的最小子集吞掉所有能力。

***

## 12. 最终决策框架

面对任意一个模型厂商或“兼容 API”，按以下顺序判断即可快速建立认知：

1. **它属于哪个协议家族？**
   - Chat Completions、Messages、GenerateContent、Responses，还是完全自定义？

2. **它的最小请求单位是什么？**
   - string、message、content block、part、item，还是 event？

3. **系统指令放在哪里？**
   - 顶层字段、message role、developer instruction，还是模板资源？

4. **会话由谁持有？**
   - 你重传完整历史，还是供应商用 response/conversation/session ID 保存？

5. **工具调用如何往返？**
   - `tool_calls` + tool role、`tool_use` + `tool_result`、functionCall + functionResponse，还是 typed items？

6. **流式协议如何结束与恢复？**
   - SSE 帧格式、事件类型、usage 到达时机、取消和错误语义是什么？

7. **推理和结构化输出有什么保证？**
   - 是否只是一条 prompt 约定，还是 JSON mode、schema constraint、opaque reasoning state？

8. **哪些字段“看起来兼容”但语义不同？**
   - `temperature`、`max_tokens`、`top_p`、`tools`、`response_format`、`finish_reason`、`usage` 都要逐项验证。

9. **失败与安全如何表达？**
   - HTTP error、finish reason、safety metadata、上下文超限、限流与可重试性分别是什么？

10. **如果明天切换供应商，哪些数据能迁移？**
    - 纯文本历史通常能迁移；供应商 conversation ID、缓存句柄、加密 reasoning state、文件 ID、托管工具轨迹通常不能直接迁移。

***

## 结论

LLM API 的真正分水岭不是有没有 `messages` 字段，而是协议能否忠实表示并编排以下对象：**指令、对话、不同模态、工具调用、工具结果、推理状态、结构化输出、流式事件与会话状态**。

在实践中，可以把 OpenAI Chat Completions 当作广泛采用的兼容基线，把 Anthropic Messages、Gemini GenerateContent 与 OpenAI Responses 看作各自更原生、更强表达力的协议范式。DeepSeek、智谱等厂商的 OpenAI 兼容接口很有价值，尤其适合快速迁移和生态接入；但必须逐项验证其推理模式、工具调用、结构化输出、多模态、流式事件和 usage 语义，而不能把“兼容”理解为无差别替换。[6][7][8][9]

最耐用的架构是：**内部使用供应商中立的事件与能力模型，边缘使用厂商适配器，保留必要的原生扩展，并让你的应用自身成为会话与审计的事实来源。**

## Citations

1. [Migrate to the Responses API | OpenAI API](https://developers.openai.com/api/docs/guides/migrate-to-responses)
2. [Text generation | OpenAI API](https://developers.openai.com/api/docs/guides/text)
3. [Generating content - Gemini API | Google AI for Developers](https://ai.google.dev/api/generate-content)
4. [Getting started - generateContent API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/get-started)
5. [Messages - Claude API Reference](https://docs.anthropic.com/en/api/messages)
6. [Chat Completions API](https://api-docs.deepseek.com/api/create-chat-completion)
7. [对话补全- 智谱AI开放文档](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)
8. [DeepSeek API Docs: Your First API Call](https://api-docs.deepseek.com/)
9. [Using the Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/guides/responses_api/)
10. [Tool Calls | DeepSeek API Docs](https://api-docs.deepseek.com/guides/tool_calls/)
11. [Compatible API (/messages) | API References](https://docs.console.zenlayer.com/api-reference/compute/aig/chat-completion/zai-glm/zai-glm-message)
12. [Create chat completion | OpenAI API Reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/)
13. [Anthropic Claude Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html)
14. [Assistants migration guide - OpenAI API](https://developers.openai.com/api/docs/assistants/migration)
15. [Method: endpoints.generateContent | Gemini Enterprise Agent ...](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/v1/projects.locations.endpoints/generateContent)
16. [Change Log | DeepSeek API Docs](https://api-docs.deepseek.com/updates/)
17. [API Overview | OpenAI API Reference](https://developers.openai.com/api/reference/overview/)
18. [Generate content with the Gemini API | Gemini Enterprise ...](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/inference)
19. [GitHub - openai/completions-responses-migration-pack ...](https://github.com/openai/completions-responses-migration-pack)
20. [Create a Message - Fireworks AI Docs](https://docs.fireworks.ai/api-reference/anthropic-messages)
21. [Lists Models - DeepSeek API Docs](https://api-docs.deepseek.com/api/list-models/)
22. [openai/completions-responses-migration-pack - GitHub](https://github.com/openai/completions-responses-migration-pack/tree/main)
23. [Query with the Anthropic Messages API - Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/model-serving/query-anthropic-messages)
24. [Open AI Responses API vs. Chat Completions vs. Messages API](https://portkey.ai/blog/open-ai-responses-api-vs-chat-completions-vs-anthropic-anthropic-messages-api)
25. [How to Migrate from Chat Completions to the Responses API](https://ctxwire.com/articles/responses-api-migration-guide/)
26. [Responses API Reference | openai/completions-responses ...](https://deepwiki.com/openai/completions-responses-migration-pack/6-responses-api-reference)
27. [Introducing the Responses API - OpenAI Developer Community](https://community.openai.com/t/introducing-the-responses-api/1140929)
28. [Chat Completions vs Responses API: The Contract You Are Actually ...](https://www.aifreeapi.com/en/posts/chat-completions-vs-responses-api)
29. [Chat Completions vs Responses and pdf file (new PDF file vision ...](https://community.openai.com/t/chat-completions-vs-responses-and-pdf-file-new-pdf-file-vision-upload-modality-added-to-cc/1143115)
30. [Getting Started | openai/completions-responses-migration-pack ...](https://deepwiki.com/openai/completions-responses-migration-pack/2-getting-started)
31. [TIP: Chat Completions API reference - as a single request, for AI ...](https://community.openai.com/t/tip-chat-completions-api-reference-as-a-single-request-for-ai-understanding/1355654)
32. [Native API (/messages) | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/ai/aig/chat-completion/anthropic-claude/anthropic-claude-message)
33. [Anthropic Messages - Introduction to Langdock - Docs](https://docs.langdock.com/en/developer/completion-api/anthropic)
34. [CLASP/docs/api-reference/anthropic-messages.md at main - GitHub](https://github.com/jedarden/CLASP/blob/main/docs/api-reference/anthropic-messages.md)
35. [[Bug] Anthropic API Error: Empty text content blocks in messages](https://github.com/anthropics/claude-code/issues/26870)
36. [streamGenerateContent Method of Gemini Rest APIs giving ...](https://discuss.google.dev/t/streamgeneratecontent-method-of-gemini-rest-apis-giving-multiple-json-objects/146282)
37. [REST API Usage | google-gemini/cookbook | DeepWiki](https://deepwiki.com/google-gemini/cookbook/9.3-rest-api-usage)
38. [Basic Content Generation | google-gemini/cookbook | DeepWiki](https://deepwiki.com/google-gemini/cookbook/2.2-basic-content-generation)
39. [Anthropic | AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/anthropic)
40. [Add OpenAI Responses API Compatibility for Codex Desktop #245](https://github.com/deepseek-ai/awesome-deepseek-agent/issues/245)
41. [Chat Completions - DeepInfra docs](https://docs.deepinfra.com/chat/overview)
42. [DeepSeek-V4-Flash Now Supports the Responses API and Codex](https://apidog.com/blog/deepseek-v4-flash-responses-api-codex/)
43. [Zhipu GLM model selection and integration | 兔子API](https://api.tu-zi.com/en/docs/models/glm)
44. [Zhipu GLM API and platform guide | 兔子API](https://business.tu-zi.com/en/docs/providers/zhipu-glm)
45. [Zhipu | AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/zhipu)
46. [GLM Anthropic Messages](https://docs.hai.network/en/api/glm-messages)
47. [Glm 5 | AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/zhipu/glm-5)
48. [GLM 5 API: Official API for Zhipu AI GLM-5 | Chat, Code ...](https://glm5api.com/)
