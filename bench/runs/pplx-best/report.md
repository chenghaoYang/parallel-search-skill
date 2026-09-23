# LLM 时代 API 请求协议：一份快速建立全局认知的对比指南

LLM API 的差异，表面上看是字段名不同，实质上是不同厂商对“**一次模型交互**”的抽象不同：有的以聊天消息（chat/messages）为中心，有的以通用输入与输出事件（responses/items）为中心，有的以多模态内容片段（contents/parts）为中心。工程上最重要的结论是：**“兼容 OpenAI”通常只意味着一部分 Chat Completions 字段和路径可复用，并不表示工具调用、推理、多模态、流式事件、结构化输出、缓存与状态管理完全等价。**

本文建立一套 taxonomy（分类体系），对比至少四个主流协议族：OpenAI Chat Completions、OpenAI Responses、Anthropic Messages、Google Gemini `generateContent`，并讨论 DeepSeek、智谱 GLM 等下游厂商的适配方式、差异与集成策略。

***

## 1. 先建立总地图

### 1.1 API 协议不是“模型能力”本身

应严格区分三层：

| 层级 | 解决的问题 | 典型内容 |
|---|---|---|
| 模型层 | 模型能否推理、看图、调用工具、生成 JSON、处理长上下文 | 模型名、上下文窗口、视觉/音频能力、推理能力、工具能力 |
| 协议层 | 调用方如何把输入发给模型、如何读回输出 | URL、请求体、角色、内容块、流格式、错误格式、usage 字段 |
| SDK/网关层 | 开发者如何方便地接入多个模型 | OpenAI SDK、Anthropic SDK、LiteLLM、Vercel AI SDK、云厂商托管 API、模型路由网关 |

例如，DeepSeek 可提供 OpenAI Chat Completions 风格接口，也可提供 Responses 风格接口；这说明其协议可以模仿 OpenAI，但不意味着全部语义、所有字段默认值、推理输出、工具行为和状态机制都与 OpenAI 完全相同。DeepSeek 文档明确将其 Chat Completions 描述为兼容 OpenAI/Anthropic 的 API 格式，并支持 OpenAI Responses 风格的端点。[1][2]

### 1.2 一个请求协议可拆成八个维度

要真正比较不同 LLM API，建议不要只看 `messages` 与 `content`，而应逐项比较：

1. **端点与资源模型**：是 `/chat/completions`、`/responses`、`/messages`，还是 `:generateContent`。
2. **会话输入模型**：输入是否是纯文本、消息数组、内容块数组，还是通用 item 列表。
3. **角色模型**：是否有 `system`、`developer`、`user`、`assistant`、`tool` 等角色；是否允许任意位置出现。
4. **多模态表示**：文本、图片、音频、文件、视频是通过 URL、base64、file ID，还是 typed parts 传入。
5. **工具调用循环**：模型怎样提出工具调用；应用怎样返回工具结果；调用 ID 如何关联。
6. **输出模型**：回答是在 `choices[0].message.content`、`content[]`、`candidates[]`，还是 typed `output[]` 中。
7. **流式语义**：是不是 SSE；增量事件是“文本 delta”，还是带语义类型的事件流。
8. **状态、缓存与可观测性**：多轮历史由谁保存，是否支持 response ID、conversation ID、prompt cache、token 细分和推理 token。

可以把常见 API 看成以下四个主范式：

| 协议范式 | 代表 | 核心抽象 | 适合的开发心智模型 |
|---|---|---|---|
| Chat completion | OpenAI Chat Completions、DeepSeek Chat、众多兼容端点 | 一串对话消息 → 一个 assistant message | 传统聊天机器人、最广泛的兼容层 |
| Response / item | OpenAI Responses、DeepSeek Responses | 通用输入 items → typed 输出 items/events | Agent、工具调用、多模态、可持续演进 |
| Messages / content blocks | Anthropic Messages | 顶级系统指令 + alternating messages + content blocks | Claude 原生能力、工具与思考块 |
| Contents / parts | Gemini `generateContent` | contents 中的 role + parts，多候选和安全反馈 | 原生 Gemini 多模态与 Google 生态能力 |

***

## 2. 四种主流协议族

## 2.1 OpenAI Chat Completions：事实上的“兼容层语言”

OpenAI Chat Completions 的核心是：

```http
POST /v1/chat/completions
```

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
      "content": "解释 HTTP 流式输出。"
    }
  ],
  "stream": false
}
```

典型非流式输出形态：

```json
{
  "id": "chatcmpl_xxx",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "HTTP 流式输出通常……"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 80,
    "total_tokens": 180
  }
}
```

这一模型的优点是直观：把截至当前轮的历史塞进 `messages`，读取 `choices[0].message.content`。OpenAI 仍支持 Chat Completions；其官方描述是“从构成对话的一组 messages 中生成模型响应”。但对新项目，OpenAI 明确建议优先考虑较新的 Responses API。[3][4]

### Chat Completions 的关键语义

| 概念 | 常见字段 | 集成时的要点 |
|---|---|---|
| 模型选择 | `model` | 不同模型支持的 modality、工具、推理与 token 参数不同 |
| 历史对话 | `messages` | 应用一般自行保存并在后续轮次重传 |
| 基础角色 | `system`、`user`、`assistant` | 不同兼容方对角色与顺序的限制不同 |
| 输出位置 | `choices[].message` | 不能假设一定只有一个 choice |
| 结束原因 | `finish_reason` | 需处理 `stop`、长度截断、工具调用或内容过滤等情况 |
| 流式 | `stream: true` | 通常以 SSE 分片返回 completion chunks |
| 结构化输出 | `response_format` | JSON mode 与 JSON Schema 严格结构化输出应区分 |
| 工具调用 | `tools`、`tool_choice` | 需要应用执行工具后，以关联调用 ID 的方式回传结果 |

OpenAI Chat Completions 可以返回普通完成对象，或在 `stream: true` 时返回一系列 chat completion chunk。消息内容本身可因模型能力而包含文本、图片或音频等模态。[5]

### 其真正价值与局限

它的最大价值不是“最先进”，而是成为了一种行业接口 lingua franca：大量模型厂、云厂商、聚合平台和自建推理服务会暴露相近的 `/v1/chat/completions` 端点，因此迁移成本低。

但它也有三个结构性局限：

- **输出过于扁平**：应用惯性地只读取 `choices[0].message.content`，但 agent 工作流中的工具调用、推理条目、拒答、文件引用、计算机操作等，天然不止一段字符串。
- **状态责任主要在客户端**：客户端通常保存所有历史、裁剪上下文、处理摘要与缓存策略。
- **“兼容”容易掩盖不兼容**：端点和基本字段可相同，但工具调用 schema、图像字段、JSON mode、reasoning 参数、stream event、usage 字段可能不同。

***

## 2.2 OpenAI Responses：从“聊天消息”转向“通用交互项”

OpenAI Responses API 的定位是 Chat Completions 的演进式替代方案，核心端点为：

```http
POST /v1/responses
```

概念上，它不是“传 messages，拿 assistant message”，而是：

> 传入 input（可为消息或其他输入项），获得由不同类型 item 构成的 output。

简化示意：

```json
{
  "model": "example-model",
  "instructions": "你是一个严谨的技术助手。",
  "input": "解释 HTTP 流式输出。",
  "store": false
}
```

返回时，不要把消费逻辑绑定在一个固定路径上，例如 `choices[0].message.content`。更稳健的思路是遍历 `output`，按 item 类型提取文本、函数调用、推理项、文件或其他结果。

OpenAI 的迁移文档将这种变化概括为三件事：请求发往 `/v1/responses`、从带类型的 `output` 数组读取结果、重新选择多轮上下文的承载方式。其文档仍说明 Chat Completions 被支持，但推荐新项目使用 Responses。[6]

### Responses API 的核心变化

| 维度 | Chat Completions | Responses |
|---|---|---|
| 基本输入 | `messages` | `input`，可容纳更广义的输入项 |
| 主输出读取点 | `choices[].message` | typed `output[]` |
| 系统级指令 | 常见为 `system` message | 可使用顶级 `instructions` |
| 工具结果关联 | 常见基于 tool call ID | 基于 `call_id` 等 typed item 关联 |
| 多轮状态 | 客户端重放历史消息 | 可选择 `previous_response_id`、Conversations API 或手动重放 |
| 流式消费 | completion chunks / delta | 语义化、带类型的 Responses events |
| 面向对象 | Chat UI 为主 | Agent、工具、多模态、长流程为主 |

### 状态并非只有一种选择

Responses API 中至少有三种会话策略：

1. **手动无状态重放**：应用自己保存和发送完整历史；最可控，也利于跨厂商。
2. **`previous_response_id` 串联**：把上一轮 response ID 传给下一轮，让服务端关联上下文。
3. **Conversations API**：使用持久的会话对象管理状态。

OpenAI 特别提醒：如果使用 `previous_response_id`，先前请求的顶级 `instructions` 不会自动继承，因此稳定的系统指令仍需在每轮重新发送。Responses 默认存储；如果需要无状态或零数据保留类策略，应明确设置 `store: false`，并在需要延续推理上下文时妥善保存并回传所需的推理项。[6]

### 为什么这对架构重要

对于只做简单问答的系统，Chat Completions 往往已经足够；但当系统包含以下需求时，Response/item 模型通常更自然：

- 模型要调用多个工具，应用要回传多个工具结果。
- 输入包含文字、图片、文件、音频或外部搜索结果。
- 模型输出不只是一段文本，还包括结构化产物、工具调用、推理过程引用或其他对象。
- 系统希望对长链条 agent 任务进行可观测、回放和状态管理。
- 平台 API 在未来可能继续添加新的 item 或 event 类型。

工程建议：**内部不要把“一次模型输出”等同于 `string`。**至少建模成 `AssistantTurn { textParts, toolCalls, citations, rawProviderResponse, usage, finishReason }`，再按厂商适配。

***

## 2.3 Anthropic Messages：顶级 system 与内容块优先

Anthropic Claude 的原生接口通常称为 Messages API，其核心模式是：

```http
POST /v1/messages
```

```json
{
  "model": "claude-example",
  "max_tokens": 1024,
  "system": "你是一个严谨的技术助手。",
  "messages": [
    {
      "role": "user",
      "content": "解释 HTTP 流式输出。"
    }
  ]
}
```

Anthropic 的重要设计选择是：`system` 通常是顶级字段，而不是历史 `messages` 数组中的普通 role；对话则围绕 `user` 与 `assistant` 的交替回合建模。官方文档强调，调用方构造每一个回合、管理对话状态，并实现自己的工具循环。[7]

### Anthropic content blocks 才是核心

Anthropic 中，一条消息的 `content` 不一定是字符串；它可以是内容块数组：

```json
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "请阅读这张图并总结。"
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

响应也往往应被理解为 `content[]`，而不是单一文本。例如一轮 assistant 输出可包含：

- `text`：给用户展示的自然语言文本。
- `tool_use`：要求应用调用某个工具及其输入。
- 其他供应商定义的内容块类型，例如涉及推理或扩展能力的块。

AWS 对 Anthropic Messages 的说明也强调，每个输入 message 都有 `role` 和 `content`，其中 `content` 可以是单个字符串，也可以是带类型的 content blocks 数组。[8]

### Anthropic 与 OpenAI Chat 的关键不同

| 问题 | OpenAI Chat Completions 常见写法 | Anthropic Messages 常见写法 | 迁移含义 |
|---|---|---|---|
| 系统指令 | `{"role":"system","content":"..."}` | 顶级 `system` | 不能直接机械复制 messages |
| 对话角色 | 常见 `system/user/assistant/tool`，部分场景有 developer 语义 | 核心为交替的 `user/assistant` | 角色映射需要明确规则 |
| 多模态 | 依模型与 content item 类型决定 | content blocks | 建议统一到内部的 typed parts |
| 工具调用 | `tool_calls` 常见于 assistant message | `tool_use` content block | 工具调用对象与回传格式不同 |
| 工具结果 | `tool` role 或相关 message | `tool_result` block，通常装入 user turn | 必须保存并正确映射调用 ID |
| 输出读取 | `choices[0].message.content` | `content[]` 中筛选 `text` block | 不能只假设文本字段存在 |
| 上下文状态 | 客户端重传为主 | 客户端重传为主 | 需要有统一的 history policy |

最危险的迁移错误是把 Anthropic 当作“把 `system` 改名即可”的 OpenAI endpoint。实际应转换的是**对话语义结构**：系统约束、用户内容块、assistant 工具意图、工具结果块，以及其关联标识。

***

## 2.4 Gemini `generateContent`：contents / parts 与候选结果

Google Gemini API 的原生生成端点为：

```http
POST https://generativelanguage.googleapis.com/v1beta/{model=models/*}:generateContent
```

流式版本一般是：

```http
POST ...:streamGenerateContent
```

Gemini 的核心抽象不是 `messages`，而是 `contents`；每一个 content 由 `role` 和 `parts` 构成。[9][10]

简化请求：

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
          "text": "解释 HTTP 流式输出。"
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.2
  }
}
```

简化响应形态：

```json
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "HTTP 流式输出通常……"
          }
        ]
      },
      "finishReason": "STOP",
      "safetyRatings": []
    }
  ],
  "usageMetadata": {
    "..."
  }
}
```

Gemini 的 `GenerateContentResponse` 是“支持多个候选输出”的响应对象；其安全信息有两层：提示词层面的 `promptFeedback`，以及各 candidate 上的 `finishReason` 与 `safetyRatings`。因此，不能只把“没有文本”处理为普通空响应，它也可能意味着 prompt 被拦截或候选内容因安全原因未返回。[9]

### Gemini 的 parts 模型

在 Gemini 中，一轮输入通常由多个 `parts` 组成，常见承载方式包括：

| part 类型 | 表示内容 | 典型用途 |
|---|---|---|
| `text` | 文本、代码、指令 | 最常见文本 prompt |
| `inlineData` | 内联原始字节 | 小型图片、音频等直接传输 |
| `fileData` | 指向已上传或托管文件 | 较大文件、可复用文件输入 |
| function call / response 相关 part | 工具调用与工具回传 | 函数工具循环 |
| 其他厂商支持的多模态 part | 模型特定能力 | 图像、视频、音频等 |

Google 的文档说明，`Content` 由 `role` 与 `parts` 构成；`parts` 可表示文本、内联 blob 数据或文件数据等。[10]

### Gemini 与其他协议最容易混淆的点

- Gemini 使用 `contents`，不是 OpenAI 风格的 `messages`。
- 内容分段的字段叫 `parts`，不是 Anthropic 的 `content` blocks，也不是 OpenAI Responses 的 `input` items。
- 返回是 `candidates[]`，而非 `choices[]` 或顶级 `output[]`。
- 安全反馈既可能在 `promptFeedback`，也可能在 candidate 中。
- 非流式 `generateContent` 在生成完成后返回一个 `GenerateContentResponse`；流式 `streamGenerateContent` 使用同样请求体，但持续返回一串 `GenerateContentResponse` 实例。[11]

***

## 3. 统一比较：请求、响应、流式与工具

## 3.1 最小文本请求映射

下面是同一个意图——“你是技术助手，解释 HTTP 流式输出”——在四种原生协议中的概念映射。

| 协议 | 端点 | 系统指令 | 用户输入 | 主输出位置 |
|---|---|---|---|---|
| OpenAI Chat Completions | `/v1/chat/completions` | `messages` 中的 `system` | `messages` 中的 `user` | `choices[].message.content` |
| OpenAI Responses | `/v1/responses` | 顶级 `instructions` | 顶级 `input` 或 input items | typed `output[]` 中的文本项 |
| Anthropic Messages | `/v1/messages` | 顶级 `system` | `messages[].content` | `content[]` 中的 `text` block |
| Gemini GenerateContent | `:generateContent` | `systemInstruction.parts[]` | `contents[].parts[]` | `candidates[].content.parts[]` |
| DeepSeek Chat | `/chat/completions` | 通常沿 OpenAI 消息方式 | `messages[]` | `choices[].message.content` |
| DeepSeek Responses | `/responses` | Response 风格字段 | Response 风格 input | Response 风格 `output[]` |

### 一个重要推论

如果你的内部模型只定义为：

```ts
type ChatMessage = {
  role: "system" | "user" | "assistant";
  content: string;
};
```

它只能覆盖“最小文本对话交集”，无法无损覆盖：

- 一条消息中混合文字与图片。
- assistant 同时输出文字和多个工具调用。
- 一条 tool result 回应多个工具调用。
- 结构化输出或引用块。
- 思考/推理类条目与展示文本的分离。
- 供应商特有的安全、缓存、音频和文件能力。

因此，跨厂商架构应使用更宽泛的中间表示（IR），而不是只在字符串 `content` 上做字段重命名。

***

## 3.2 建议的内部统一表示

下面不是某家厂商的 wire format，而是应用内部可采用的抽象。目标是：对普通文本足够简单，对工具和多模态又不丢失信息。

```ts
type Role = "system" | "developer" | "user" | "assistant" | "tool";

type Part =
  | { type: "text"; text: string }
  | { type: "image_url"; url: string; detail?: string }
  | { type: "image_base64"; mediaType: string; data: string }
  | { type: "audio"; mediaType: string; dataOrUrl: string }
  | { type: "file"; fileId?: string; url?: string; mimeType?: string }
  | {
      type: "tool_call";
      id: string;
      name: string;
      argumentsJson: string;
    }
  | {
      type: "tool_result";
      toolCallId: string;
      content: string | Part[];
      isError?: boolean;
    }
  | {
      type: "reasoning";
      summary?: string;
      opaqueProviderData?: unknown;
    }
  | {
      type: "provider_extension";
      provider: string;
      raw: unknown;
    };

type Turn = {
  role: Role;
  parts: Part[];
  name?: string;
};

type NormalizedRequest = {
  model: string;
  instructions?: string;
  turns?: Turn[];
  tools?: NormalizedTool[];
  toolChoice?: ToolChoice;
  outputSchema?: JsonSchema;
  stream?: boolean;
  temperature?: number;
  maxOutputTokens?: number;
  metadata?: Record<string, string>;
};
```

这里有四项原则：

1. **所有内容都是 part**：即使纯文本也表示成 `{ type: "text" }`。
2. **工具调用要有稳定 ID**：工具结果必须回到对应调用，而不是仅以函数名匹配。
3. **保留 provider extension escape hatch**：不强迫各厂商特性降级成字符串。
4. **区分 canonical data 与 raw payload**：业务层用规范化数据；调试、审计、灰度和升级时保留原始厂商请求/响应。

***

## 3.3 工具调用不是“模型调用函数”，而是一个协议循环

跨厂商最常见的误解是：在请求中传一个工具 schema 后，模型会直接执行函数。实际通常不是。模型只是提出一个“调用意图”，真正的执行由你的应用完成。

通用循环如下：

1. 应用把工具定义和用户输入发给模型。
2. 模型输出一个或多个工具调用请求。
3. 应用验证参数、鉴权、执行本地函数或外部服务。
4. 应用将工具结果连同正确的调用 ID 回传模型。
5. 模型依据工具结果生成最终回答，或继续请求更多工具。

### 不同厂商中的工具语义

| 语义环节 | OpenAI Chat / Responses | Anthropic Messages | Gemini GenerateContent |
|---|---|---|---|
| 工具定义 | `tools` | `tools` | function declarations / tools 配置 |
| 模型的调用意图 | tool call 对象或 typed output item | `tool_use` block | function call part |
| 结果关联键 | `tool_call_id` / `call_id` | `tool_use_id` | function call 名称及关联语义，具体依 SDK/API 版本 |
| 工具结果回传 | `tool` message 或 function-call output item | `tool_result` block，常置于 user message | function response part |
| 并行调用 | 常见支持，需按模型能力处理 | 可产生多个 tool use block | 取决于模型/API 能力 |
| 应用负责执行 | 是 | 是 | 是 |

OpenAI 的函数调用文档指出，工具输出应引用特定模型工具调用的 `call_id`，且工具输出可以是结构化 JSON 或纯文本；流式模式下也可增量获取函数参数。[12]

### 工具调用的工程安全边界

不要因为模型给出了参数就直接执行。至少需要：

- JSON 解析和 JSON Schema 验证。
- 认证与授权；模型本身不是用户身份。
- 对写操作进行人工确认或策略确认。
- 网络目标 allowlist，防止 SSRF。
- 限制文件路径、SQL、Shell、HTTP 方法与资源范围。
- 限速、超时、幂等键、重试策略。
- 对工具返回内容进行不可信输入处理，防范 prompt injection。
- 记录 `toolCallId`、输入、结果摘要、执行者和时间。

尤其是“读取网页/邮件/文档后再执行操作”的 agent，工具结果本身也是不可信文本；不能把它视为系统指令。

***

## 3.4 结构化输出：JSON mode 不等于 Schema adherence

“让模型返回 JSON”至少有三个不同层级：

| 级别 | 含义 | 典型风险 |
|---|---|---|
| Prompt 要求 JSON | 在自然语言中要求“请返回 JSON” | 最不可靠，可能夹带 Markdown、解释文字或不合法 JSON |
| JSON mode | 协议要求生成有效 JSON object | JSON 可解析，但字段、类型、枚举、必填项未必满足业务 schema |
| Structured Outputs / JSON Schema | 传入 JSON Schema，并要求严格符合 | 最适合机器消费，但仍需处理拒答、截断、模型支持差异与 schema 限制 |

OpenAI 明确区分 JSON mode 与 Structured Outputs：前者确保有效 JSON，后者才确保遵守开发者指定的 schema；Structured Outputs 可通过 function calling 或 JSON Schema response format 使用。[13]

DeepSeek 的 JSON Output 文档同样要求设置 `response_format: {"type": "json_object"}`，并建议在提示词中包含 “json” 且给出目标格式示例；这说明即使协议提供 JSON mode，提示设计与输出截断控制仍是实际可靠性的一部分。[14]

### 可移植结构化输出的建议

- 把 JSON Schema 当成业务契约，存入版本控制。
- 区分“能解析 JSON”和“通过业务 schema 校验”。
- 保留服务端二次校验，不依赖模型承诺。
- 对不支持严格 schema 的供应商，使用：JSON mode + 强提示 + schema validation + 一次有限重试/修复。
- 对空结果、拒答、内容拦截、长度截断，不要盲目 JSON parse。
- 不要将 JSON 包裹在 Markdown code fence 后直接当成功；应先明确约定输出通道。

***

## 3.5 流式：都是 SSE，但事件语义不同

很多 API 的流式底层都采用 Server-Sent Events（SSE），但“都是 SSE”不代表客户端可复用。

| 协议 | 常见流式形态 | 客户端应关注什么 |
|---|---|---|
| OpenAI Chat Completions | chat completion chunks / `delta` | 聚合角色、文本 delta、工具参数 delta、结束原因 |
| OpenAI Responses | typed semantic events | 按事件类型路由，而不是只拼字符串 |
| Anthropic Messages | content block start/delta/stop 等语义事件 | 跟踪 block 索引和 block 类型 |
| Gemini | 多个 `GenerateContentResponse` 实例 | 合并 candidate/content/parts，并处理安全及结束状态 |
| DeepSeek Chat | OpenAI 风格 chat completion chunks | 基本可沿用 OpenAI chunk 处理器，但需验证扩展字段 |
| DeepSeek Responses | 语义化 SSE events | 接近 OpenAI Responses 事件消费模型 |

Gemini 对 `generateContent` 与 `streamGenerateContent` 的说明非常直接：请求体相同；非流式返回单个 `GenerateContentResponse`，流式则返回一串该响应对象。[11]

### 不要用 `buffer += delta.content` 处理所有模型

这种写法只适合“单一文本流”的最小情况：

```ts
buffer += chunk.choices?.[0]?.delta?.content ?? "";
```

它会在以下情形失效：

- 正在流的是工具参数，而非用户可见文本。
- 返回的是多个候选结果。
- 输出分为多个 content block。
- 某些事件表示“开始/结束/拒答/安全过滤/usage”，不是文本。
- 流中携带 reasoning、引用、音频或计算机操作等非文本内容。

更稳妥的做法是维护一个流聚合器状态机：

```ts
type StreamAccumulator = {
  visibleText: string;
  toolCalls: Map<string, {
    id: string;
    name?: string;
    argumentBuffer: string;
  }>;
  parts: Part[];
  finishReason?: string;
  usage?: Record<string, number>;
  rawEvents: unknown[];
};
```

然后针对供应商事件适配为统一事件：

```ts
type NormalizedStreamEvent =
  | { type: "text_delta"; text: string }
  | { type: "tool_call_started"; id: string; name: string }
  | { type: "tool_arguments_delta"; id: string; delta: string }
  | { type: "tool_call_completed"; id: string }
  | { type: "usage"; inputTokens?: number; outputTokens?: number }
  | { type: "completed"; finishReason?: string }
  | { type: "error"; error: unknown };
```

***

## 4. DeepSeek、智谱与“OpenAI 兼容”究竟意味着什么

## 4.1 DeepSeek：兼容层较强，但要区分 Chat 与 Responses

DeepSeek 文档展示了 `/chat/completions`、`messages`、`choices`、`response_format`、`stream` 等典型 OpenAI Chat Completions 风格字段；其 Chat Completions 响应也被定义为 chat completion object 或 streamed chat completion chunks。[1][15]

例如，以下形式通常符合其 Chat API 心智模型：

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
      "content": "解释 HTTP 流式输出。"
    }
  ],
  "stream": false
}
```

但 DeepSeek 不应被简单归类为“只有 OpenAI Chat 协议”。其官方也提供 Responses API，并说明响应对象与 OpenAI Responses API 的 `response` 结构兼容。值得注意的是，它同时明确了部分尚未支持能力的字段会取固定值，例如 `store: false`、`previous_response_id: null`、`parallel_tool_calls: true`。这意味着客户端即使看到 Responses 兼容字段，也不能假设 OpenAI 的服务端状态管理语义已经实现。[2]

其原生 Responses 端点还明确声明：API 是无状态的，response 和 conversation 不在服务端存储。[16]

### DeepSeek 的集成结论

- 对纯文本 Chat：可以较高概率复用 OpenAI Chat 客户端和抽象。
- 对 JSON 输出：可用 `response_format: {"type":"json_object"}`，但仍应做业务 schema 校验。[14]
- 对多轮：Chat 路径中需像经典 Chat Completions 一样，把 assistant 输出追加回 `messages`，再继续发送。[17]
- 对 Responses：要把它视为“结构兼容”，而不是自动获得 OpenAI 的服务端会话、存储或全部 hosted tools。
- 对 reasoning：不能把内部思考字段当成稳定的、跨厂商可移植的业务接口；只应消费官方承诺的字段，并为缺失、脱敏或不同计费口径预留空间。

***

## 4.2 智谱 GLM：需区分“接口兼容”与“原生扩展能力”

智谱 GLM / Z.AI 生态中常见 OpenAI 风格的 SDK 与端点设计，实际项目里经常可通过替换 `base_url`、API key、`model` 来复用一部分 OpenAI 客户端代码。尤其在基本 `messages`、文本输出、温度参数、流式选项等层面，这种适配能快速起步。

但工程上不应把“SDK 调用形式相似”误认为“协议逐字段相同”。尤其需要单独验证：

- `system`、`developer`、`user`、`assistant` 角色的接受范围与优先级。
- `content` 是否只接受字符串，还是接受多模态数组。
- 工具调用字段、工具结果字段、调用 ID 关联规则。
- 是否有平台特有的 MCP、联网搜索、检索、代码执行或电脑操作能力。
- 推理模型是否返回特殊 reasoning 字段，是否允许向后传递。
- 流式 chunk/event 格式是否完整复刻 OpenAI。
- `usage` 是否具有缓存 token、推理 token、音频 token 等子项。
- 结构化输出是 JSON mode、JSON Schema，还是仅提示词约束。

Z.AI 的开发者文档中展示了 MCP 调用能力，并使用 `server_label`、`server_url`、鉴权信息等概念。这类能力属于平台扩展，无法直接压缩成最传统的 OpenAI Chat Completions 最小子集。[18]

### “智谱的 message 对比 Anthropic 官方”应如何理解

如果比较的是对话消息抽象，重点不是“二者是否都有 `messages`”，而是以下差异：

| 维度 | OpenAI 兼容式 GLM 接口的常见模式 | Anthropic Messages 原生模式 |
|---|---|---|
| 系统提示词 | 通常可作为 `system` message | 典型方式为顶级 `system` |
| 用户/助手消息 | 通常 `messages[]`，`content` 常从字符串起步 | `messages[]`，`content` 可为字符串或 typed blocks |
| 角色限制 | 常参照 OpenAI，但要看具体版本 | 强调 `user` / `assistant` 的交替对话结构 |
| 工具调用 | 通常接近 OpenAI 的 tools/tool_calls | `tool_use` 与 `tool_result` content blocks |
| 多模态 | 依 GLM 具体模型/API 而定 | 原生 content blocks 是基本抽象 |
| 平台扩展 | 可能包含 MCP、搜索等供应商能力 | Claude 有其原生工具、思考、搜索等能力 |
| 最佳接入策略 | 以官方版本化文档为准，不依赖“兼容”标签 | 按 Anthropic 原生 block 语义建模 |

结论是：对纯文本多轮对话，二者可以映射到同一个内部 `Turn[]`；但若涉及工具、图像、MCP、推理或流式 block，应该走各自 adapter，不应试图用“字段替换”完成迁移。

***

## 4.3 兼容性可分为五个等级

“OpenAI-compatible”建议拆成以下等级，而不是二元判断：

| 等级 | 含义 | 能否直接切换 `base_url` |
|---|---|---|
| L0：认证兼容 | 都使用 Bearer token 等相似认证形式 | 不够 |
| L1：端点兼容 | 有 `/v1/chat/completions` 或相近端点 | 仅能发请求 |
| L2：文本消息兼容 | 支持 `model`、`messages`、基础 role、文本输出 | 简单聊天通常可以 |
| L3：高级请求兼容 | 温度、停止词、JSON mode、视觉、工具等部分可用 | 需逐项测试 |
| L4：语义兼容 | 角色优先级、工具循环、流式事件、错误、finish reason、usage 意义一致 | 很少完全成立 |
| L5：生命周期兼容 | 状态、存储、缓存、批处理、文件、评测、微调等平台能力也一致 | 几乎不应假设 |

现实中，大多数“OpenAI 兼容”服务只应被默认视为 **L2 到局部 L3**。达到 L4 或 L5 必须依据当前模型版本、端点版本和功能逐项验收。

***

## 5. 实战：如何设计可迁移的 LLM 接入层

## 5.1 不要追求“一个 JSON 打天下”

合理目标不是让所有提供商都完全归一，而是划分能力层：

| 能力层 | 策略 | 示例 |
|---|---|---|
| 通用核心层 | 强制统一并测试 | 文本、system instruction、user/assistant 历史、温度、最大输出、基本 usage |
| 扩展能力层 | 标准化接口 + provider capability 检查 | 图像、工具调用、流式、JSON Schema、缓存 |
| 厂商专属层 | 显式 namespaced 配置，不伪装成通用能力 | Gemini 文件、Claude 特有 block、OpenAI hosted tools、GLM MCP |
| 降级层 | 定义替代路径或明确失败 | 无严格 schema 时转 JSON mode + 验证；无视觉能力时拒绝或先 OCR |
| 观测层 | 统一记录，但保留 raw 数据 | 延迟、输入/输出 token、finish reason、原始请求响应 ID |

推荐接口形态：

```ts
interface LLMProvider {
  capabilities(): ProviderCapabilities;

  generate(request: NormalizedRequest): Promise<NormalizedResponse>;

  stream(
    request: NormalizedRequest,
    onEvent: (event: NormalizedStreamEvent) => void
  ): Promise<NormalizedResponse>;
}
```

不要把所有厂商参数都塞进一个巨型 `options: Record<string, any>`；那会让兼容性问题在运行时才暴露。应使用：

```ts
type ProviderOptions = {
  openai?: {
    previousResponseId?: string;
    store?: boolean;
  };
  anthropic?: {
    thinking?: { enabled: boolean };
  };
  gemini?: {
    safetySettings?: unknown[];
    cachedContent?: string;
  };
  deepseek?: {
    reasoningEffort?: "low" | "medium" | "high";
  };
  zhipu?: {
    mcp?: unknown;
  };
};
```

这样可让供应商扩展显式、可审计、可逐步淘汰。

***

## 5.2 建立 capability matrix，而不是散落 `if provider === ...`

每个模型、端点与版本都应该有能力元数据，例如：

```json
{
  "provider": "example",
  "model": "example-model",
  "endpointFamily": "responses",
  "supports": {
    "text": true,
    "imageInput": true,
    "audioInput": false,
    "fileInput": true,
    "streaming": true,
    "toolCalling": true,
    "parallelToolCalls": true,
    "jsonMode": true,
    "jsonSchema": true,
    "serverSideConversation": false,
    "promptCaching": true,
    "reasoningControls": true
  },
  "limits": {
    "contextTokens": 128000,
    "maxOutputTokens": 8192,
    "maxImages": 20
  }
}
```

然后所有请求先经过预检：

1. 用户是否发送图片？
2. 目标模型是否支持图片输入？
3. 用户是否需要严格 JSON Schema？
4. 目标端点是否原生支持 strict schema？
5. 是否要求工具调用？
6. 是否允许工具并发？
7. 是否要求服务端维护多轮状态？
8. 是否满足数据驻留、存储关闭或审计策略？

这比在某次 API 调用失败后临时加一个 provider-specific patch 更可靠。

***

## 5.3 多轮状态：先决定谁是事实来源

多轮对话存在两类架构：

| 架构 | 做法 | 优点 | 风险 |
|---|---|---|---|
| 应用掌握历史 | 数据库保存 canonical turns；每轮按目标协议渲染 | 可迁移、可审计、可切换模型、可做摘要 | 需承担 token 增长、裁剪与缓存策略 |
| 厂商掌握历史 | 传 conversation / thread / previous response ID | 接口简单，可能利用平台状态能力 | 锁定供应商；迁移、灾备和跨模型路由更复杂 |
| 混合模式 | 应用保存 canonical transcript，同时可使用 provider ID 加速 | 灵活且可恢复 | 需要处理双份状态一致性 |

对需要多模型路由、A/B 测试、灾备切换或长期合规留存的产品，建议将**应用数据库中的 canonical transcript 作为事实来源**。provider response ID、conversation ID、cache handle 等仅作为可失效的优化索引，而不是唯一历史。

***

## 5.4 参数不能想当然地横向映射

以下字段看似通用，语义却经常不同：

| 参数类别 | 常见字段 | 常见陷阱 |
|---|---|---|
| 随机性 | `temperature`、`top_p` | 可取范围、默认值、是否允许同时指定、对推理模型是否生效都可能不同 |
| 输出上限 | `max_tokens`、`max_completion_tokens`、`max_output_tokens` | 有的含推理 token，有的不含；字段名和计费口径不同 |
| 结束控制 | `stop` | 有些模型/端点不支持，或在推理模型上被限制 |
| 候选数 | `n`、candidate count | 可能不支持、多候选成本高、流式语义更复杂 |
| 结构化输出 | `response_format`、`text.format`、generation config | JSON object 与 JSON Schema 的可靠性不同 |
| 工具选择 | `tool_choice` | `auto`、`required`、指定函数、禁用并行等语义并不统一 |
| 推理控制 | `reasoning_effort`、thinking 配置等 | 几乎都是厂商特有能力，不应假设可迁移 |
| 存储控制 | `store` 等 | 有的有服务端持久化，有的明确无状态 |

OpenAI 的迁移文档特别指出，Responses 中结构化输出从 Chat Completions 的 `response_format` 转向 `text.format`，而流式消费者也应改为处理 typed Responses events。[6]

***

## 5.5 错误、拒答、截断与安全反馈必须成为一等公民

生产系统不能只区分 HTTP 200 和非 200。至少应规范化为：

```ts
type Outcome =
  | { type: "success" }
  | { type: "length_truncated" }
  | { type: "content_filtered" }
  | { type: "refused" }
  | { type: "tool_call_required" }
  | { type: "rate_limited"; retryAfterMs?: number }
  | { type: "invalid_request"; details?: unknown }
  | { type: "provider_unavailable" }
  | { type: "unknown_failure"; raw?: unknown };
```

需要重点处理：

- **长度截断**：JSON 或函数参数可能只生成了一半，不能当成有效对象。
- **安全拦截**：Gemini 可能在 `promptFeedback` 或 candidate 层报告安全信息。[9]
- **拒答**：响应可能是正常 HTTP 200，但模型没有完成用户请求。
- **工具调用未完成**：模型输出工具请求不等于最终答案。
- **流中断**：已经展示了部分文本，但最终无 `completed` event，需要 UI 和后端都能恢复。
- **速率限制**：应尊重服务端重试提示，使用退避和请求幂等策略。
- **参数不支持**：不要因一个增强参数导致整个跨供应商 fallback 失败；可先做能力预检和降级。

***

## 6. 推荐的学习与落地顺序

如果你的目标是快速建立认知，而不是一开始陷入每家文档的字段细节，建议按这个顺序学习：

1. **先掌握 Chat Completions 最小模型**  
   理解 `messages → choices[].message`、`stream`、`usage`、多轮历史重传。这仍是最广泛的兼容基线。OpenAI Chat Completions 目前仍受支持。[3]

2. **再掌握 content blocks / parts**  
   将“message content 是字符串”的思维升级为“message 由多个带类型的 part 构成”。Anthropic 与 Gemini 的原生协议尤其体现这一点。[8][10]

3. **学习工具调用双向循环**  
   重点是 call ID 的关联、参数验证、工具结果回传与安全控制，而不是只会声明一个 function schema。[12]

4. **理解 Responses/item 思维**  
   从“读一段 answer string”转向“消费带类型输出项目和事件”。这是处理 agent、复杂多模态与平台演进的关键。[6]

5. **建立 provider adapter + capability matrix**  
   先统一 80% 的文本、流式、工具和 JSON 需求；剩余 20% 作为显式厂商扩展，不要假装它们可完全通用。

6. **最后做跨厂商一致性测试**  
   针对每一家、每个模型、每个端点，至少覆盖文本、多轮、流式、结构化输出、工具调用、工具错误、图像输入、限流、截断与内容安全。

***

## 7. 最终速查表

| 你遇到的问题 | 首先应问什么 | 推荐答案方向 |
|---|---|---|
| “能否替换 base URL？” | 只做文本聊天，还是也做工具、图片、JSON、流式？ | 纯文本可能可以；高级能力必须逐项验证 |
| “messages 是否可以直接复用？” | system/developer 角色与 content 是否同构？ | 通常只能复用最小文本子集 |
| “为什么响应结构不一样？” | 厂商的核心抽象是 message、block、part 还是 item？ | 按协议族写 adapter，不要硬编码单一路径 |
| “如何支持多个模型？” | 是否有 canonical internal representation 与能力矩阵？ | 先统一核心能力，扩展能力显式 namespaced |
| “JSON mode 是否足够？” | 需要有效 JSON，还是必须符合业务 schema？ | 业务自动化优先 strict JSON Schema + 二次校验 |
| “流式客户端能通用吗？” | 你是否只拼文本，还是能处理工具、usage、结束与错误事件？ | 统一为 typed stream events |
| “多轮上下文放哪里？” | 是否需要迁移、路由、审计、跨模型 fallback？ | 应用侧保存 canonical transcript，服务端状态仅作优化 |
| “OpenAI-compatible 可信到什么程度？” | 属于 L1、L2、L3，还是语义级 L4？ | 默认只信到 L2/L3，靠 contract tests 验证 |

***

## 结语

最有用的心智模型是：

> Chat Completions 是一个重要的历史兼容基线；Messages、Contents/Parts 和 Responses/Items 则代表不同厂商对多模态、工具、状态和 agent 工作流的原生建模。跨模型工程的关键不是背字段，而是把这些模型归纳为“角色 + 内容块 + 工具调用关联 + 流式事件 + 状态策略 + 能力声明”。

对简单聊天，OpenAI 兼容接口能显著降低接入成本；对生产级 agent、多模态、严格结构化输出、复杂工具链、跨厂商路由和合规需求，则必须以原生协议语义为准，并通过适配器、能力矩阵、契约测试和统一观测来管理差异。OpenAI 已将 Responses 作为新项目的推荐方向，Anthropic 以 Messages/content blocks 表达原生对话与工具语义，Gemini 则围绕 `contents/parts` 和 `candidates` 建模；DeepSeek 等厂商的兼容层应被视作高价值的起点，而不是完整的语义保证。[2][6][7][9]

## Citations

1. [DeepSeek API Docs: Your First API Call](https://api-docs.deepseek.com/)
2. [Using the Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/guides/responses_api/)
3. [Chat Completions Overview | OpenAI API Reference](https://developers.openai.com/api/reference/chat-completions/overview)
4. [Text generation | OpenAI API](https://developers.openai.com/api/docs/guides/text)
5. [Create chat completion | OpenAI API Reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
6. [Migrate to the Responses API - OpenAI Developers](https://developers.openai.com/api/docs/guides/migrate-to-responses)
7. [Documentation - Claude Platform Docs](https://platform.claude.com/docs/en/home)
8. [Anthropic Claude Messages API - Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html)
9. [Generating content - Gemini API | Google AI for Developers](https://ai.google.dev/api/generate-content)
10. [Generate content with the Gemini API - docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/inference)
11. [Text generation - generateContent API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/text-generation)
12. [Function calling | OpenAI API](https://developers.openai.com/api/docs/guides/function-calling)
13. [Structured model outputs | OpenAI API](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses)
14. [JSON Output - DeepSeek API Docs](https://api-docs.deepseek.com/guides/json_mode/)
15. [Chat Completions API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-chat-completion/)
16. [Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-response/)
17. [Multi-round Conversation - DeepSeek API Docs](https://api-docs.deepseek.com/guides/multi_round_chat/)
18. [MCP Calling - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/guides/capabilities/mcp-call)
19. [Assistants migration guide | OpenAI API](https://developers.openai.com/api/docs/assistants/migration)
20. [Introducing Structured Outputs in the API - OpenAI](https://openai.com/index/introducing-structured-outputs-in-the-api/)
21. [Completions | OpenAI API Reference](https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions)
22. [Method: endpoints.generateContent | Gemini Enterprise Agent ...](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/v1/projects.locations.endpoints/generateContent)
23. [Query with the Anthropic Messages API | Databricks on AWS](https://docs.databricks.com/aws/en/machine-learning/model-serving/query-anthropic-messages)
24. [How can I use the Chat Completion API? - OpenAI Help Center](https://help.openai.com/en/articles/7232945-how-can-i-use-the-chat-completion-api)
25. [Using the Anthropic API - DeepSeek API Docs](https://api-docs.deepseek.com/guides/anthropic_api/)
26. [GeminiAPI/docs/gemini_generate_content_api ... - GitHub](https://github.com/AceDataCloud/GeminiAPI/blob/main/docs/gemini_generate_content_api_integration_guide.md)
27. [CLASP/docs/api-reference/anthropic-messages.md at main - GitHub](https://github.com/jedarden/CLASP/blob/main/docs/api-reference/anthropic-messages.md)
28. [Chat Completions API | openai/openai-python | DeepWiki](https://deepwiki.com/openai/openai-python/4.1-chat-completions-api)
29. [Chat Completion - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/api-reference/llm/chat-completion)
30. [Introducing DeepSeek-V3](https://api-docs.deepseek.com/news/news1226)
31. [Explore DeepSeek API - Chat Completion and more - SerpApi](https://serpapi.com/blog/explore-deepseek-api/)
32. [DeepSeek-V4-Flash Now Supports the Responses API and Codex](https://apidog.com/blog/deepseek-v4-flash-responses-api-codex/)
33. [Chat Completion - Hugging Face](https://huggingface.co/docs/inference-providers/en/tasks/chat-completion)
34. [TIP: Chat Completions API reference - as a single request, for AI ...](https://community.openai.com/t/tip-chat-completions-api-reference-as-a-single-request-for-ai-understanding/1355654)
35. [DeepSeek API Docs 2026 — Quickstart & Examples](https://deepseek.ai/docs)
36. [Glm 4.7 - AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/zhipu/glm-4.7)
37. [How V7 gives AI agents institutional memory - OpenAI](https://openai.com/index/v7/)
38. [How to use structured outputs with Azure OpenAI in Microsoft ...](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
39. [Switching from AssistantsAPI to ResponseAPI - No way of using ...](https://learn.microsoft.com/en-us/answers/questions/5533585/switching-from-assistantsapi-to-responseapi-no-way)
40. [openai-node/docs/structured-outputs.md at main · openai ...](https://github.com/openai/openai-node/blob/main/docs/structured-outputs.md)
41. [API Reference — openai-structured documentation](https://openai-structured.readthedocs.io/en/latest/api.html)
42. [How to Migrate from OpenAI Chat Completions to Responses API](https://docs.bswen.com/blog/2026-04-16-migrate-to-responses-api/)
43. [Introducing the Responses API - OpenAI Developer Community](https://community.openai.com/t/introducing-the-responses-api/1140929)
44. [Chat Completions vs Responses API: The Contract You Are Actually ...](https://www.aifreeapi.com/en/posts/chat-completions-vs-responses-api)
45. [Welcome to openai-structured’s documentation! — openai ...](https://openai-structured.readthedocs.io/en/latest/index.html)
