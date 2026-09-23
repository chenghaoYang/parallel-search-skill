# LLM API 请求协议：从 Chat Completions 到 Responses、Messages 与 Gemini `generateContent`

LLM API 的“兼容”通常只意味着**路径和少数 JSON 字段相似**，不代表行为、状态管理、多模态、工具调用、流式事件、推理输出或结构化输出可以无损互换。建立正确认知的关键不是记住各厂商字段，而是先识别它属于哪一种协议家族，再在适配层中显式处理差异。

本文以四个主流原生协议为主线：

1. OpenAI **Chat Completions**
2. OpenAI **Responses**
3. Anthropic **Messages**
4. Google Gemini **`generateContent`**

并讨论 DeepSeek、智谱 GLM、阿里云 Qwen 等下游厂商如何“OpenAI 兼容”、兼容的边界在哪里，以及在生产系统中应如何设计统一适配层。

***

## 1. 先建立 taxonomy

不要把所有 LLM API 都当成“传 prompt，取文本”的同一协议。更合适的分法是按 API 的**会话表示、输出表示和执行模型**划分。

| 协议家族 | 典型接口 | 请求中的核心对话单位 | 响应中的核心单位 | 设计重心 | 典型厂商 |
|---|---|---|---|---|---|
| Chat Completions 家族 | `/v1/chat/completions` | `messages[]` | `choices[].message` | 对话生成、历史由客户端维护 | OpenAI 传统接口、DeepSeek、智谱、Qwen、绝大多数兼容网关 |
| Responses 家族 | `/v1/responses` | `input`（字符串或 typed items） | `output[]`（typed items） | Agent、多步骤工具、推理项、统一输入输出 | OpenAI、部分 DeepSeek、Qwen 等 |
| Anthropic Messages 家族 | `/v1/messages` | `system` + `messages[]` + `content blocks` | 单个 `Message` + `content[]` | 显式内容块、工具使用、模型原生交互 | Anthropic Claude、部分代理/兼容层 |
| Gemini Content/Part 家族 | `:generateContent` | `contents[]`，每轮由 `parts[]` 组成 | `candidates[]`，每项含 `content.parts[]` | 原生多模态、候选答案、Google 工具与 grounding | Google Gemini |
| 供应商私有/扩展协议 | 厂商路径或兼容路径 | 常常伪装为上述之一 | 在标准对象中加入厂商字段 | 模型功能暴露、迁移成本控制 | DeepSeek、智谱、Qwen、云平台代理等 |

可以将任何调用归约到下面的通用模型：

$$
\text{Request}
=
\text{Model}
+
\text{Instructions}
+
\text{Conversation State}
+
\text{Content Parts}
+
\text{Generation Config}
+
\text{Tools}
+
\text{Output Contract}
$$

其中：

- **Model**：模型标识、版本、能力集合。
- **Instructions**：系统策略、开发者指令、行为边界。
- **Conversation State**：历史消息、服务端会话 ID、上一个 response ID，或二者混合。
- **Content Parts**：文本、图片、音频、视频、文件、引用、工具结果等。
- **Generation Config**：温度、采样、最大输出 token、停止词等。
- **Tools**：函数、搜索、代码执行、文件检索、浏览器等。
- **Output Contract**：自由文本、JSON mode、JSON Schema、工具调用、流式事件。

所有协议差异，本质上都在于这七部分用什么字段表示、哪些能力存在、状态由谁维护、结果以何种对象返回。

***

## 2. 四类主流协议对比

### 2.1 一张速查表

| 维度 | OpenAI Chat Completions | OpenAI Responses | Anthropic Messages | Gemini `generateContent` |
|---|---|---|---|---|
| 典型路径 | `/v1/chat/completions` | `/v1/responses` | `/v1/messages` | `/v1beta/models/{model}:generateContent` |
| 基本输入 | `messages[]` | `input` | `system` + `messages[]` | `contents[]` |
| 内容表示 | `content` 为字符串或 content parts | typed input/output items | `content` 为字符串或 block 数组 | 每轮为 `Content`，内部为 `parts[]` |
| 基本输出 | `choices[].message` | `output[]` | 一个 message，含 `content[]` | `candidates[].content.parts[]` |
| 系统指令 | `system` 或 `developer` 消息 | `instructions` | 顶层 `system`，不作为普通 message role | `systemInstruction` |
| 工具调用 | `tools` → `tool_calls` → `tool` 消息 | `tools` → `function_call` / output item | `tools` → `tool_use` / `tool_result` blocks | `tools` → `functionCall` / `functionResponse` parts |
| 会话状态 | 客户端回传历史 | 可回传历史，也可借助 `previous_response_id` 等能力 | 客户端回传 `messages[]` | 客户端回传 `contents[]` |
| 流式传输 | SSE，`chat.completion.chunk` | SSE，多种 `response.*` 事件 | SSE，content-block 生命周期事件 | SSE，多个 `GenerateContentResponse` |
| 结构化输出 | `response_format` | `text.format` | 主要通过 tool schema / prompt 约束 | 常见为 `responseMimeType` + schema |
| 最适合 | 已有 OpenAI 生态的传统聊天应用 | Agent、复杂工具编排、统一多模态输入输出 | Claude 原生工具与内容块能力 | Gemini 原生多模态与 Google 生态能力 |

OpenAI 将 Responses API 定义为 Chat Completions 的演进：Chat Completions 以 `messages` 作为输入和输出的主体；Responses 则使用 `input` 和 `output` 的 typed items，消息只是其中一种 item，其他 item 可包括 reasoning、function call 与 function-call output。Responses 的 `output` 也不应被假定为只有一条文本消息。[1][2]

Gemini 的核心抽象是 `Content` 和 `Part`：一轮对话是一个 `Content`，一轮里可有多个 `Part`，从而自然表达“同一轮里文字 + 图片 + 视频 URI”等混合输入；其响应以 `candidates` 返回，每个 candidate 又携带一个 `Content`。[3]

Anthropic Messages 则明确把输入和输出视为 content blocks 的组合，并以 `system` 顶层字段、`messages` 对话数组以及多类型的 `ContentBlock` / `ContentBlockParam` 建模。[4]

***

### 2.2 协议 1：OpenAI Chat Completions

这是最广泛被模仿的协议表面。它的基本请求通常是：

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
      "content": "解释 API 协议适配。"
    }
  ],
  "temperature": 0.2
}
```

典型非流式响应：

```json
{
  "id": "chatcmpl_xxx",
  "object": "chat.completion",
  "model": "example-model",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "API 适配不只是字段改名。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 30,
    "total_tokens": 130
  }
}
```

其核心特征：

- `messages[]` 是完整上下文，调用方通常负责在每次请求中拼接历史。
- 结果被包在 `choices[]` 中；即便大多数应用只请求一个候选结果，也应正确读取 `choices[0]`。
- 传统文本回答在 `choices[0].message.content`。
- 工具调用通常位于 `choices[0].message.tool_calls`；此时 `content` 可能为空。
- 结构化输出常使用 `response_format`。OpenAI 将 `json_schema` 形式称为 Structured Outputs，并建议在支持时优先于旧的 JSON mode。[5][6]
- 多模态虽被支持，但各模型所支持的 image/audio/content-part 形态并不完全相同。OpenAI 的官方参考明确提示，不同模型支持不同的消息模态。[5]

**不能误解的地方：**“OpenAI-compatible” 并不意味着支持 OpenAI 所有字段。一个提供商可能接受 `messages`、`model`、`temperature`，但忽略、拒绝或以不同语义实现 `seed`、`logprobs`、`response_format.json_schema`、`parallel_tool_calls`、音频参数或预测输出参数。

***

### 2.3 协议 2：OpenAI Responses

Responses API 不应简单视为“Chat Completions 换了 endpoint”。它将 API 的最小单位从“聊天消息”扩展为“有类型的输入输出项”，更适合 Agent 场景。

一个简化请求：

```json
{
  "model": "example-model",
  "instructions": "你是一个严谨的技术助手。",
  "input": "解释为什么不能只按字段名判断 LLM API 兼容性。"
}
```

也可以使用更显式的输入项：

```json
{
  "model": "example-model",
  "instructions": "用中文回答。",
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "比较两种 API 协议。"
        }
      ]
    }
  ]
}
```

概念上的响应形态：

```json
{
  "id": "resp_xxx",
  "status": "completed",
  "output": [
    {
      "type": "reasoning",
      "id": "rs_xxx"
    },
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "协议兼容应同时验证语法、语义与生命周期。"
        }
      ]
    }
  ]
}
```

需要建立的关键认知：

- `instructions` 与 `input` 分离。`instructions` 承担高层行为约束，且其优先级高于 `input` 中的普通提示。[2]
- `output[]` 可以有多项。它不只是最终文本，还可能带 reasoning、工具调用、工具结果关联项等。[2]
- 结构化输出的位置变化：Chat Completions 使用 `response_format`，Responses 使用 `text.format`。这不是简单的字段重命名，因为响应对象、流事件和工具交互生命周期也一起变化。[1][6]
- 许多 Responses 风格实现允许使用 `previous_response_id` 管理上下文，而不是每次由客户端手工拼完整历史。例如阿里云 Model Studio 的 OpenAI-compatible Responses 接口提供此机制，并说明 response ID 可用于后续上下文续接。[7]

**适合什么场景：**

- 一个任务可能经历“推理 → 调用工具 → 读取工具结果 → 继续回答”的多阶段过程。
- 需要统一表达文本、图像、工具调用和工具结果。
- 希望抽象“工作流/Agent 运行”而非只抽象“聊天消息”。
- 希望在 API 层依赖 provider 的服务端状态续接能力。

**迁移风险：**

- 原来只读取 `choices[0].message.content` 的代码会失效。
- 需要遍历 `output[]`，根据 item 的 `type` 处理，而不能假设第一项就是最终文本。
- 历史消息的拼接策略与状态归属会改变。
- SSE 事件名、事件粒度与终态判定也会改变。

***

### 2.4 协议 3：Anthropic Messages

Anthropic 的 API 名称也有 “Messages”，但它不是 OpenAI 的 `messages[]` 的同义替代。其最大差异是：**系统指令、会话消息和内容块的边界更显式。**

概念化请求：

```json
{
  "model": "claude-like-model",
  "max_tokens": 1024,
  "system": "你是一个严谨的技术助手。",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "解释工具调用生命周期。"
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
      "text": "模型先返回 tool_use block，应用执行后再回传 tool_result block。"
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 100,
    "output_tokens": 60
  }
}
```

其重要设计点：

- `system` 通常位于请求顶层，而非 `messages[]` 中的 `role: "system"` 消息。
- `messages[]` 常围绕 `user` 与 `assistant` 组织，内容可以是字符串或 content blocks。
- 响应的 `content[]` 是多块结构：文本、thinking、redacted thinking、tool use 等可能并存。Anthropic 文档将 ContentBlock 建模为多个具体 block 类型的联合。[4]
- 工具结果不是 OpenAI 风格的独立 `role: "tool"` 消息；在 Anthropic 原生协议里，它通常以 `tool_result` content block 发送回模型。
- `max_tokens` 在该协议中是一个十分显式且通常必填的输出上限概念；不能假定其他厂商默认值、字段名或 token 会计方式相同。
- 流式响应是**内容块生命周期**，包括 `message_start`、`content_block_start`、若干 `content_block_delta`、`content_block_stop`、`message_delta`、`message_stop`；中间还可能出现 `ping`。[8]

这意味着，把 Anthropic 映射到 Chat Completions 时，最难的部分并不只是：

```text
system → system message
```

而是以下结构性转换：

| Anthropic | OpenAI Chat Completions | 映射风险 |
|---|---|---|
| 顶层 `system` | `system` 或 `developer` message | 指令优先级与拼接方式不必然等价 |
| `content: [{type:"text"}]` | 字符串或 text content part | 一般较容易 |
| `tool_use` block | `assistant.tool_calls[]` | call ID、参数字符串化、并发语义要验证 |
| `tool_result` block | `role:"tool"` 消息 | 必须保留与 tool call 的关联 ID |
| thinking block | `reasoning_content`、reasoning item 或被丢弃 | 高度供应商相关，常无法无损迁移 |
| `stop_reason` | `finish_reason` | 值集合与取消、长度截断、工具调用含义不完全一致 |

LiteLLM 等适配系统也明确指出，Anthropic `messages` 到 OpenAI Responses 的映射是“结构变换”而非字段直接复制：一个 Anthropic message 可以展开为一个或多个 Responses input item，而顶层 `system` 的文本块可能被拼接为 `instructions`。[9]

***

### 2.5 协议 4：Google Gemini `generateContent`

Gemini 不以 `messages` 为中心，而是使用 `contents[]` 与 `parts[]`：

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
          "text": "解释 API 协议差异。"
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.2,
    "maxOutputTokens": 1024
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
            "text": "Gemini 以 Content/Part 表示一轮及其多模态组成。"
          }
        ]
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 100,
    "candidatesTokenCount": 40,
    "totalTokenCount": 140
  }
}
```

Gemini 协议的关键点：

- `Content` 是一轮输入或输出的容器；`Part` 是该轮中的具体内容片段。
- 同一轮可含多个 `Part`，天然适合组合文字、图片、视频 URI、内联二进制数据和工具相关部分。Google 文档明确将 `Content` 定义为对话回合容器、将 `Part` 定义为一轮中的数据片段。[3]
- 常规调用返回一个完整的 `GenerateContentResponse`；流式调用使用相同请求体，但返回一系列 `GenerateContentResponse` 对象。[3]
- 文本通常不应通过“整个响应对象转字符串”取得，而应从 candidate 的 `content.parts[]` 中合并符合预期类型的 part。
- 候选结果是 `candidates[]`，而非 OpenAI 的 `choices[]`；虽然概念相似，安全过滤、finish reason、grounding metadata 等伴随字段的语义并不一样。
- Google Search grounding、URL context 等功能往往会把额外 metadata 放在 Gemini 自己的响应结构中；例如 URL context 的响应可包含检索 URL 及其处理状态，适合审计与调试。[10][11]
- Gemini 允许将 thinking 摘要作为 response parts 的一种信息暴露，需通过配置显式开启并检查该 part 的 `thought` 标志；它不等同于 OpenAI 的 reasoning item，也不等同于 DeepSeek 的 `reasoning_content`。[12]

***

## 3. “OpenAI 兼容”到底兼容什么

“兼容 OpenAI”至少有四个层级，不能混为一谈。

| 兼容层 | 含义 | 可否直接替换 SDK | 风险 |
|---|---|---|---|
| 路径兼容 | 有 `/v1/chat/completions` | 不一定 | 认证、错误码、字段可能不同 |
| 请求形状兼容 | 接受 `model`、`messages`、`temperature` 等 | 有时可以 | 高级字段可能不支持或静默忽略 |
| 响应形状兼容 | 返回 `choices[].message.content` | 基础场景多半可以 | tool calls、usage、finish reason 常不同 |
| 语义与生命周期兼容 | 角色、工具、流式、结构化输出、状态管理均近似 | 才接近真正可替换 | 极少完全成立 |

生产系统最危险的是“前两层兼容，却被误认为第四层兼容”。

例如，Qwen 的 Model Studio 提供 OpenAI-compatible Chat 接口，官方定位是只需修改 API key、base URL 和 model name 即可迁移既有 OpenAI 代码；其聊天响应也沿用 `choices[i].message` 等形态。  但这适合的结论是“**基础 Chat Completions 场景迁移成本低**”，不是“每一个 OpenAI 特性和行为都等价”。[13]

同样，阿里云还提供 OpenAI-compatible Responses API，接口从 `/v1/chat/completions` 转为 `/v1/responses`，并支持 `previous_response_id` 这类 Responses 风格的上下文续接。  这说明同一平台可能同时存在多个协议面，而模型能力、地区 endpoint、兼容范围和生命周期语义仍须分别核验。[7][14]

***

## 4. DeepSeek：兼容外形下的关键差异

DeepSeek 是理解“协议看似兼容、语义实则不同”的代表。

### 4.1 基础层：Chat Completions 外形

DeepSeek 提供 Chat Completions 形式的接口，并表示 API 可兼容 OpenAI/Anthropic 风格，因此可以通过调整配置使用相应 SDK 或软件。[15][16]

基础请求通常仍像：

```json
{
  "model": "deepseek-reasoner",
  "messages": [
    {
      "role": "user",
      "content": "给我一个架构建议。"
    }
  ]
}
```

所以在仅做“输入文本、获得普通文本”时，既有 OpenAI 客户端往往可以快速接入。

### 4.2 推理输出：`reasoning_content` 不是普通 `content`

在 thinking mode 下，DeepSeek 将推理内容暴露在 assistant message 的 `reasoning_content` 字段，与最终 `content` 同级。官方说明 `response.choices[0].message` 中可以同时包含 `content`、`reasoning_content` 和 `tool_calls`。[17]

概念上：

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "reasoning_content": "……内部推理或思考内容……",
        "content": "最终面向用户的答案。",
        "tool_calls": []
      }
    }
  ]
}
```

这与其他协议不同：

| 系统 | 推理/思考的主要位置 | 应否回传 | 适配要点 |
|---|---|---|---|
| OpenAI Responses | 独立 `reasoning` output item | 视具体状态续接与产品机制而定 | 不能只取第一条 message |
| Anthropic | `thinking` / related content block | 取决于原生调用流程和产品约束 | block 类型要保留 |
| Gemini | 带 `thought` 标志的 part/摘要能力 | 不应假定等同于原始 CoT | 通过配置启用并逐 part 处理 |
| DeepSeek | `message.reasoning_content` | 特定工具场景必须回传 | Chat completion 的扩展字段 |

最重要的 DeepSeek 特例是：

- 如果后续请求**带有 `tools` 参数**，此前每轮的 `reasoning_content` 必须完整回传，否则可能返回 HTTP 400。
- 如果后续请求**不带 tools**，先前 reasoning content 通常不需要回传，即使发送也可能被忽略而不拼入上下文。[17]

因此，以下“通用 OpenAI 历史裁剪代码”在 DeepSeek tool-calling + reasoning 模式中可能出错：

```python
# 不安全示意：会丢掉厂商扩展字段
history.append({
    "role": response.choices[0].message.role,
    "content": response.choices[0].message.content
})
```

更稳健的做法是保留标准字段和必要的 provider extension：

```python
assistant_message = {
    "role": response.choices[0].message.role,
    "content": response.choices[0].message.content
}

if response.choices[0].message.reasoning_content is not None:
    assistant_message["reasoning_content"] = (
        response.choices[0].message.reasoning_content
    )

if response.choices[0].message.tool_calls:
    assistant_message["tool_calls"] = response.choices[0].message.tool_calls
```

### 4.3 DeepSeek Responses：不是所有 OpenAI Responses 字段都完整等价

DeepSeek 也提供 Responses API 支持，但其官方兼容说明中明确列出具体支持范围。例如：

- `message` 支持，但角色和 content part 有限制；
- `developer` 角色会被当作 `user` 对待；
- `function_call` 被并入相邻 assistant message；
- reasoning 的纯文本 content 可以被并入相邻 assistant message；
- `summary` 与 `encrypted_content` 不支持；
- 文件输入不支持。[18]

所以，即便 endpoint 是 `/responses`，也不应假定其行为等同于 OpenAI 原生 Responses。尤其是优先级模型、安全语义、输出 item 的独立性以及多模态支持范围，都可能不同。

***

## 5. 智谱 GLM：与 Anthropic 的 message 模型有何不同

智谱的对话补全接口主要属于 **OpenAI Chat Completions 家族**：请求需要 `model` 和 `messages`，支持流式/非流式、多模态输入、采样参数、最大 token、工具调用等；工具调用生成时，`content` 通常为空，信息位于 `tool_calls`。[19]

其快速开始示例采用：

```http
POST /api/paas/v4/chat/completions
```

并传入 `model` 和 `messages`。[20]

### 5.1 智谱与 Anthropic 的核心结构差异

| 主题 | 智谱 GLM Chat Completions | Anthropic Messages | 对适配的影响 |
|---|---|---|---|
| 系统指令 | 常作为 `messages` 中 `role: "system"` | 顶层 `system` 参数 | 不能无脑把所有 role 原样转发 |
| 对话数组 | `messages[]`，类似 OpenAI | `messages[]`，但常以 user/assistant 为中心 | 同名字段，不代表同构 |
| 角色 | 常见 system/user/assistant/tool | 原生模型强调 system 与 messages 分离 | tool result 的承载位置不同 |
| 内容表达 | Chat Completions 风格 `content`，可扩展多模态 | 字符串或显式 content blocks | Anthropic 更强调 block union |
| 工具调用输出 | `tool_calls[]`，`content` 常为空 | `tool_use` block，嵌于 `content[]` | 需转换 ID、参数、输出结构 |
| 工具结果回传 | `role: "tool"` + tool call ID 关联 | `tool_result` block，常放在 user content 中 | 不能只变字段名 |
| 停止状态 | 通常 `finish_reason` | `stop_reason` | 枚举值、工具调用和长度截断含义要映射 |
| 流式格式 | 常贴近 OpenAI delta chunk | block-level SSE 生命周期 | 前端流渲染器不可直接复用 |

智谱 API 参考也把可用角色描述为 system、user、assistant、tool，并将工具生成结果置于 `tool_calls`。  与此同时，Anthropic 的原生 API 用顶层 `system`、content block 和 `tool_use`/`tool_result` 的模型来表达相同领域概念。[4][8][19][21]

**结论：**智谱与 Anthropic 都可以完成“系统提示 + 用户消息 + 工具调用 + 工具结果”的任务，但它们的**状态机编码方式不同**。用智谱/OpenAI 风格 SDK 写出的完整工具循环，不能仅替换 base URL 后对接 Anthropic；反过来也一样。

***

## 6. 工具调用：最容易被低估的协议差异

工具调用不是一个 JSON 字段，而是一个跨多次请求的状态机：

$$
\text{User Input}
\rightarrow
\text{Model Tool Request}
\rightarrow
\text{Application Executes Tool}
\rightarrow
\text{Tool Result}
\rightarrow
\text{Model Continues}
$$

不同协议在每一环的表示都不同。

| 阶段 | OpenAI Chat Completions / 智谱类 | OpenAI Responses | Anthropic Messages | Gemini |
|---|---|---|---|---|
| 声明工具 | `tools[]`，通常为 function schema | `tools[]`，可含更多原生工具概念 | `tools[]` | `tools[]`，常含 function declarations |
| 模型请求工具 | `message.tool_calls[]` | `function_call` output item | `tool_use` content block | `functionCall` part |
| 工具调用 ID | `tool_call_id` / call ID | `call_id` 等关联字段 | `id` | function call 标识/关联信息 |
| 应用回传结果 | `role: "tool"` 消息 | `function_call_output` input item | `tool_result` content block | `functionResponse` part |
| 可否并行调用 | 取决于模型与参数 | 更适于多 item 编排 | 支持能力与模型相关 | 取决于模型与 SDK |
| 流式解析 | delta 中逐步出现 tool calls | item 与 content-part 事件 | block start/delta/stop | 一系列响应对象/parts |

### 6.1 适配时必须保存什么

不要把工具调用“规范化”为只有函数名和参数。至少保留：

- provider；
- protocol family；
- provider-native tool-call ID；
- 函数名；
- 原始参数字节串或 JSON；
- 解析后的参数对象；
- 并发组或调用顺序；
- 工具执行状态；
- 工具结果原文；
- 工具结果是否需要被完整回传；
- 产生该调用的 assistant turn / response ID；
- 适配器版本。

特别是 DeepSeek reasoning + tools 的组合，既要保留 tool calls，也要根据官方规则保留并回传前序 `reasoning_content`，否则下一轮可能被服务端拒绝。[17]

### 6.2 推荐的内部工具调用 IR

应用内部可使用一个不绑定厂商的中间表示：

```ts
type ToolCall = {
  provider: "openai" | "anthropic" | "google" | "deepseek" | "zhipu";
  protocol: "chat_completions" | "responses" | "messages" | "generate_content";
  id: string;
  name: string;
  argumentsText: string;
  arguments?: unknown;
  status: "requested" | "running" | "completed" | "failed";
};

type ToolResult = {
  toolCallId: string;
  content: Array<
    | { type: "text"; text: string }
    | { type: "json"; value: unknown }
    | { type: "image"; mimeType: string; data: string }
  >;
  isError?: boolean;
};
```

然后让每个 provider adapter 负责：

```text
Provider Request → Internal IR
Internal Tool Result → Provider-specific follow-up request
Provider Response → Internal IR
```

不要让业务层知道 `tool_result`、`functionResponse`、`tool_call_id`、`function_call_output` 等厂商名词。

***

## 7. 流式响应：不要只把它当作“文本 chunk”

所有主流厂商都支持流式调用，但其事件模型差异明显。

| 协议 | 流式基本形态 | 应如何判定完成 | 常见错误 |
|---|---|---|---|
| OpenAI Chat Completions | SSE chunks，`delta` 累加 | 观察结束 chunk / finish reason / `[DONE]` 风格终止 | 只拼 `delta.content`，漏掉 tool call arguments |
| OpenAI Responses | 多种 `response.*` 事件 | 等待 response 完结事件并聚合 item | 假定只有一条文本流 |
| Anthropic Messages | SSE block 生命周期 | `message_stop` 才是完整消息结束 | 把 `content_block_delta` 当作整个回复 |
| Gemini | 多个 `GenerateContentResponse` | 依 finish reason 与流结束聚合 candidate parts | 假设每块只有 `text` |

Anthropic 的流式协议尤为清晰地体现了其内容块模型：一个响应先有 `message_start`，随后每个 block 经历 start / delta / stop，最后才有 `message_delta` 与 `message_stop`。[8]

Gemini 的普通与流式调用使用**相同请求 body**；差别主要是普通模式返回单个完整 `GenerateContentResponse`，流式模式返回多个该类型的响应。[3]

因此，前端或网关不宜抽象为：

```ts
onToken(text: string): void
```

而更推荐：

```ts
type StreamEvent =
  | { type: "text_delta"; text: string }
  | { type: "reasoning_delta"; text: string }
  | { type: "tool_call_started"; call: ToolCall }
  | { type: "tool_arguments_delta"; callId: string; text: string }
  | { type: "tool_call_completed"; call: ToolCall }
  | { type: "usage"; inputTokens?: number; outputTokens?: number }
  | { type: "completed"; finishReason?: string }
  | { type: "error"; error: unknown };
```

这能防止业务层错误地将“流”限定为文本 token 流。

***

## 8. 多模态：统一为 Parts，而不要统一为 String

传统 Chat Completions 让人形成了一个危险惯性：`content` 就是字符串。但在新协议与原生多模态模型中，更正确的抽象是：

```ts
type ContentPart =
  | { type: "text"; text: string }
  | { type: "image_url"; url: string }
  | { type: "image_base64"; mimeType: string; data: string }
  | { type: "audio"; mimeType: string; data: string }
  | { type: "video_url"; url: string }
  | { type: "file"; fileId?: string; mimeType?: string; data?: string }
  | { type: "tool_result"; toolCallId: string; content: unknown };
```

### 8.1 为什么不能只存纯文本历史

如果你将每轮历史强制序列化为：

```json
{
  "role": "user",
  "content": "[图片] 请分析这张图"
}
```

将损失：

- 原始图像或文件的可重放能力；
- MIME type；
- 图像与文本的顺序；
- 对应的工具/引用 metadata；
- provider 对图像、音频、视频等内容的原生理解能力；
- 在不同提供商之间进行真实多模态迁移的可能性。

Gemini 从数据模型上就强调 `Content` / `Part` 的多模态组合；DeepSeek 的 Responses 兼容说明也对不同 role 中可否携带 `input_image`、函数输出中是否可以出现图片、文件是否支持等做了细粒度限制。[3][18]

因此，内部会话存储应保留规范化 parts，而不是仅保存最终拼出的 prompt 字符串。

***

## 9. 结构化输出：JSON mode 不等于 JSON Schema

“让模型返回 JSON”至少有三种不同强度：

| 层级 | 含义 | 应用能否安全直接解析 | 适用场景 |
|---|---|---|---|
| Prompt JSON | 在提示词中要求 JSON | 否 | 临时原型、低风险文本提取 |
| JSON mode | 保证输出是合法 JSON | 仍要验证字段、类型、枚举 | 简单对象输出 |
| JSON Schema / Structured Outputs | 要求遵守给定 schema 的受支持子集 | 仍应做业务校验，但格式可靠性更高 | 工单、表单、自动化决策、函数参数 |
| Tool calling | 将结构化意图表达为函数参数 | 仍须验证与授权 | 调用外部动作、检索、工作流 |

OpenAI 文档区分 JSON mode 与 Structured Outputs：后者要求模型遵循给定 JSON Schema，且 Responses 中配置位置为 `text.format`，Chat Completions 中为 `response_format`。[1][6]

DeepSeek 的 Chat Completions 也说明 `response_format: {"type":"json_object"}` 启用 JSON Output；其 tool calling 还提供 strict mode，以让工具调用参数更严格符合函数 JSON schema。[22][23]

但跨供应商时必须确认：

- 是否真正支持 JSON Schema，还是只支持 JSON object；
- 支持 JSON Schema 的哪一个子集；
- 是否要求 `additionalProperties: false`；
- 是否支持嵌套、联合类型、递归、pattern、enum；
- schema 约束的是最终回答、工具参数，还是二者均可；
- 被拒绝、内容过滤、长度截断时是否仍返回完整有效 JSON；
- 流式时是否有可安全增量解析的保证。

无论供应商宣传什么，业务端仍应做：

1. JSON 解析；
2. schema 验证；
3. 业务权限验证；
4. 语义范围验证；
5. 工具调用前的策略检查。

模型输出的 JSON 合法，不意味着它在业务上可信或被授权。

***

## 10. 参数名相同，语义也可能不同

### 10.1 参数迁移对照

| 业务意图 | Chat Completions 常见位置 | Responses 常见位置 | Anthropic 常见位置 | Gemini 常见位置 |
|---|---|---|---|---|
| 模型 | `model` | `model` | `model` | URL path 中的 model |
| 系统指令 | `system` / `developer` message | `instructions` | 顶层 `system` | `systemInstruction` |
| 当前输入 | `messages[]` | `input` | `messages[]` | `contents[]` |
| 温度 | `temperature` | `temperature` 或同类配置 | `temperature` | `generationConfig.temperature` |
| 最大输出 | `max_tokens` / 新式变体 | 供应商定义字段 | `max_tokens` | `generationConfig.maxOutputTokens` |
| 停止序列 | `stop` | 供应商定义字段 | `stop_sequences` | `generationConfig.stopSequences` |
| 工具定义 | `tools` | `tools` | `tools` | `tools` |
| 强制工具选择 | `tool_choice` | `tool_choice` 或相近控制 | `tool_choice` | function-calling config |
| 输出 JSON | `response_format` | `text.format` | tool/schema 或其他原生机制 | generation config / response MIME/schema |
| 历史管理 | `messages[]` | `input` 或 response 链接 | `messages[]` | `contents[]` |

### 10.2 需要特别验证的参数

- **`temperature`**：不是所有模型都支持，也不意味着数值效果可比较。推理模型、特定托管模型或稳定模式可能固定/限制采样参数。
- **`max_tokens`**：它可能指最大生成 token、最大 completion token、最大输出 token，或不同计费口径；字段名也常变。
- **`stop` / `stop_sequences`**：多字符串、正则、是否包含在输出中、是否与工具调用冲突，各有差异。
- **`seed`**：即便接受，也常只是 best effort；跨模型、跨区域、跨版本或工具调用条件下不应承诺严格复现。
- **`n` / candidates**：OpenAI 的 `n`、Gemini 的 candidates 以及供应商的多候选支持并非一一对应。
- **`logprobs`**：支持范围极不一致，尤其在多模态、推理和工具调用模式中。
- **`user`**：有的用于终端用户标识，有的供应商忽略，有的对隐私、审计、滥用检测有不同规定。
- **`developer` role**：不要假定所有 provider 都有同等优先级。例如 DeepSeek Responses 文档明确指出 developer 被作为 user 处理。[18]

***

## 11. 推荐的统一适配架构

### 11.1 不要以厂商 DTO 作为业务对象

避免这样设计：

```ts
function ask(messages: OpenAI.ChatCompletionMessageParam[]) {
  // 业务逻辑直接依赖 OpenAI DTO
}
```

因为一旦接入 Anthropic、Gemini 或有推理扩展的 DeepSeek，业务逻辑就会被迫理解 provider-specific 字段。

应使用内部中间表示。

```ts
type CanonicalRole =
  | "system"
  | "developer"
  | "user"
  | "assistant"
  | "tool";

type CanonicalMessage = {
  id: string;
  role: CanonicalRole;
  parts: ContentPart[];
  providerMetadata?: Record<string, unknown>;
};

type GenerationRequest = {
  model: {
    provider: string;
    id: string;
  };
  instructions?: ContentPart[];
  messages: CanonicalMessage[];
  tools?: ToolDefinition[];
  output?: {
    mode: "text" | "json_object" | "json_schema";
    schema?: unknown;
  };
  generation?: {
    temperature?: number;
    maxOutputTokens?: number;
    stopSequences?: string[];
  };
};
```

适配器承担三类职责：

```text
Canonical Request
        ↓
Provider-specific Request Builder
        ↓
Provider API
        ↓
Provider-specific Response / Stream Parser
        ↓
Canonical Response / Events
```

### 11.2 每个适配器必须有 capability matrix

不要只存 `provider = "openai"`。至少存储模型级能力：

| Capability | 示例值 |
|---|---|
| `chat_completions` | true / false |
| `responses` | true / false |
| `anthropic_messages` | true / false |
| `gemini_generate_content` | true / false |
| `text_input` | true |
| `image_input` | true / false / 限制列表 |
| `audio_input` | true / false |
| `file_input` | true / false |
| `tool_calling` | true / false |
| `parallel_tool_calls` | true / false |
| `structured_outputs` | none / json_object / json_schema |
| `streaming` | true / false |
| `reasoning_visible` | none / summary / raw / provider_extension |
| `stateful_conversation` | none / response_id / session_id |
| `system_instruction_mode` | role / top_level / dedicated_field |
| `developer_role_semantics` | native / mapped / unsupported |

这比“这家兼容 OpenAI”有用得多。

### 11.3 让降级行为可见

当某项能力不能无损映射时，适配器不能静默吞掉，应输出明确的降级信息。例如：

```json
{
  "warnings": [
    {
      "code": "DEVELOPER_ROLE_DOWNGRADED",
      "message": "Target provider maps developer instructions to user content."
    },
    {
      "code": "JSON_SCHEMA_DOWNGRADED",
      "message": "Target provider supports JSON mode but not strict schema conformance."
    }
  ]
}
```

这种设计能避免应用误把“请求成功”理解成“行为保持一致”。

***

## 12. 迁移与接入检查清单

### 接入新模型前

- 确认原生协议：Chat Completions、Responses、Messages、`generateContent`，还是私有协议。
- 确认 endpoint、认证方式、地区路由、API 版本与 SDK 版本。
- 验证角色语义，而非只验证角色字段是否被接受。
- 验证系统提示的位置与优先级。
- 验证是否支持字符串 content、数组 content parts、图片、音频、文件。
- 验证工具调用的声明、返回、工具结果回传、并行行为和错误恢复。
- 验证流式事件的完整状态机。
- 验证 JSON mode、JSON Schema、strict tool schema 的实际支持范围。
- 验证 token usage 字段、缓存 token、推理 token、输入输出 token 的计费定义。
- 验证限流、重试、超时、幂等、请求取消与错误对象结构。
- 验证内容过滤、拒答、截断时的 response shape。
- 验证模型版本固定策略；不要只使用可能滚动升级的别名而没有回归测试。

### 从 OpenAI Chat Completions 迁往 Responses 时

- 将 `messages[]` 的业务抽象升级为 typed items / content parts。
- 用 `instructions` 表达高层指令，明确其覆盖范围。
- 改为遍历 `output[]`，不要只找一条 assistant message。
- 重新实现工具调用循环。
- 重写流式解析器以支持 response item 与 content part 事件。
- 评估是否采用 `previous_response_id`，并制定会话过期、重试和跨区域策略。
- 将 `response_format` 迁移为 `text.format`，并重新测试 schema 约束。[1][6]

### 从 OpenAI 兼容端点迁往 Anthropic 时

- 将 system message 提升为顶层 `system`。
- 将 `role: "tool"` 工具结果转换为 `tool_result` blocks。
- 将 `tool_calls[]` 转为 `tool_use` blocks，并保留 ID。
- 由 `choices[].message` 改为读取 `content[]`。
- 由 delta 聚合改为 block 生命周期处理。
- 明确 `max_tokens` 约束。
- 检查 assistant prefill、thinking、缓存、工具调用等 Claude 特有或版本特有行为。

### 从 OpenAI/Anthropic 迁往 Gemini 时

- 将每轮消息转为 `Content`，将具体输入转为 `Part`。
- 将系统指令转为 `systemInstruction`。
- 把结果读取逻辑改为遍历 `candidates[].content.parts[]`。
- 将工具结果转换为 function response parts。
- 为 grounding、URL context、safety、thought summary 等 Gemini metadata 建立独立处理分支。
- 重新验证图片、视频、音频、文件 URI 与内联数据的格式和大小限制。[3][10][12]

***

## 13. 一个最实用的判断框架

当某厂商宣称“兼容 OpenAI / Anthropic”时，依次问下面十个问题：

1. 兼容的是哪个 endpoint：Chat Completions、Responses，还是两者？
2. 系统提示应放在哪里，优先级是否相同？
3. 支持哪些 role，`developer` 是否有原生语义？
4. `content` 是纯字符串、数组，还是 typed parts？
5. 工具调用如何返回、如何回传结果、如何关联 ID？
6. 流式事件名称、顺序、结束条件是什么？
7. 推理内容在哪里，是否可见，后续轮次是否必须回传？
8. 是否支持 JSON object、JSON Schema、strict tool schema？分别支持什么子集？
9. usage 的 token 分类和计费口径是什么？
10. 哪些 OpenAI/Anthropic 字段会被拒绝、忽略、降级或改写？

如果这十个问题没有答案，就只能说“**基础请求可能可用**”，不能说“协议兼容”。

***

## 14. 最终结论

LLM API 的演进已从“文本补全接口”转向“多模态、工具、推理、状态和流式事件共同组成的执行协议”。

- **Chat Completions** 是最常见的兼容基线，适合传统聊天和简单工具调用，但通常由客户端维护完整会话历史。
- **Responses** 将消息扩展为 typed input/output items，更适合 Agent、多步骤工具工作流与服务端状态续接。[1][2]
- **Anthropic Messages** 以顶层 system、content blocks 和 block 生命周期为核心；它与 OpenAI 的相似性停留在“都能对话”，而不在完整请求/响应状态机。[4][8]
- **Gemini `generateContent`** 用 Content/Part 原生表示多模态对话，结果通过 candidates 与 parts 返回，并扩展了 grounding、URL context、thought 等自身生态能力。[3][10][12]
- **DeepSeek、智谱、Qwen 等**经常提供 OpenAI-compatible 路径，使基础接入更简单；但 reasoning、tool loop、developer role、Responses 支持范围、多模态和流式行为仍可能具有供应商特例。DeepSeek 的 `reasoning_content` 在 tools 场景需跨轮回传，就是典型例子。[17][18]
- 最可靠的工程策略是：用**规范化内部 IR + provider adapter + capability matrix + 显式降级告警**，而不是把一种厂商的 SDK DTO 当作整个业务系统的对话标准。

真正可移植的不是某个 JSON 字段，而是你对“指令、消息、内容部分、工具调用、工具结果、推理、流、状态与输出契约”的完整建模。

## Citations

1. [Migrate to the Responses API - OpenAI Developers](https://developers.openai.com/api/docs/guides/migrate-to-responses)
2. [Text generation | OpenAI API](https://developers.openai.com/api/docs/guides/text)
3. [Text generation - generateContent API](https://ai.google.dev/gemini-api/docs/generate-content/text-generation)
4. [Messages - Claude API Reference - Anthropic](https://platform.claude.com/docs/en/api/messages)
5. [Create chat completion | OpenAI API Reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/)
6. [Structured model outputs | OpenAI API](https://developers.openai.com/api/docs/guides/structured-outputs)
7. [Alibaba Cloud Model Studio:OpenAI-compatible - Responses](https://www.alibabacloud.com/help/en/model-studio/compatibility-with-openai-responses-api)
8. [Streaming Messages - Anthropic](https://docs.anthropic.com/en/api/messages-streaming?debug_url=1&debug=1&debug=true)
9. [v1/messages → /responses Parameter Mapping](https://docs.litellm.ai/docs/anthropic_unified/messages_to_responses_mapping)
10. [URL context - generateContent API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/url-context)
11. [Grounding with Google Search - generateContent API](https://ai.google.dev/gemini-api/docs/generate-content/google-search)
12. [Gemini thinking - generateContent API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/thinking)
13. [Alibaba Cloud Model Studio:OpenAI compatible - Chat](https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope)
14. [Alibaba Cloud Model Studio:Create a response](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-responses)
15. [DeepSeek API Docs: Your First API Call](https://api-docs.deepseek.com/)
16. [Reasoning Model (deepseek-reasoner)](https://api-docs.deepseek.com/guides/reasoning_model)
17. [Thinking Mode - DeepSeek API Docs](https://api-docs.deepseek.com/guides/thinking_mode/)
18. [Using the Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/guides/responses_api/)
19. [对话补全- 智谱AI开放文档](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)
20. [快速开始- 智谱AI开放文档 - 平台介绍](https://docs.bigmodel.cn/cn/guide/start/quick-start)
21. [Chat Completion - Overview - Z.AI DEVELOPER DOCUMENT](https://docs.z.ai/api-reference/llm/chat-completion)
22. [Chat Completions API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-chat-completion/)
23. [Tool Calls | DeepSeek API Docs](https://api-docs.deepseek.com/guides/tool_calls/)
24. [Using the Messages API - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
25. [Getting started - generateContent API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/get-started)
26. [Chat Completions Overview | OpenAI API Reference](https://developers.openai.com/api/reference/chat-completions/overview/)
27. [Language Model API Overview - Tencent Cloud](https://intl.cloud.tencent.com/document/product/1300/80632)
28. [Gemini API reference | Google AI for Developers](https://ai.google.dev/api)
29. [Convert Anthropic Messages to OpenAI Chat Completions](https://docs.api7.ai/api7-gateway/ai-gateway/use-cases/protocol-conversion)
30. [API Reference - OpenAI API](https://platform.openai.com/docs/api-reference/chat/completions/create)
31. [OpenAI Platform](https://platform.openai.com/docs/guides/text-generation/chat-completions-response-format)
32. [CLASP/docs/api-reference/anthropic-messages.md at main - GitHub](https://github.com/jedarden/CLASP/blob/main/docs/api-reference/anthropic-messages.md)
33. [OpenAI-compatible - Respons](https://docs.modelstudio.console.alibabacloud.com/id/model-studio/compatibility-with-openai-responses-api)
34. [Native API (/chat/completions) | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/ai/aig/chat-completion/zai-glm/zai-glm-chat-completion)
35. [Native API (/chat/completions) | API References - Zenlayer Docs](https://docs.console.zenlayer.com/api-reference/compute/aig/chat-completion/zai-glm/zai-glm-chat-completion)
36. [Alibaba Cloud Model Studio - Alibaba Cloud Documentation Center](https://www.alibabacloud.com/help/en/model-studio/what-is-model-studio)
37. [Reasoning Outputs - vLLM](https://docs.vllm.ai/en/v0.24.0/features/reasoning_outputs/)
38. [Alibaba Cloud Model Studio:OpenAI compatible - Chat](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions)
39. [%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8%E5%BC%82%E6%AD%A5](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8%E5%BC%82%E6%AD%A5)
40. [Completions | OpenAI API Reference](https://developers.openai.com/api/reference/python/resources/chat/subresources/completions)
41. [OpenAI Platform](https://platform.openai.com/docs/guides/text-generation/using-the-api)
42. [Use the Azure OpenAI Responses API - Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses)
43. [How to use structured outputs with Azure OpenAI ... - Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
44. [Migrate Python apps from Azure OpenAI Chat Completions ...](https://learn.microsoft.com/en-us/azure/developer/ai/how-to/azure-openai-to-responses)
45. [Responses API documentation on structured outputs is lacking](https://community.openai.com/t/responses-api-documentation-on-structured-outputs-is-lacking/1356632)
46. [Chat Completions vs OpenAI Responses API: What Actually Changed](https://dev.to/dev-in-progress/chat-completions-vs-openai-responses-api-what-actually-changed-4bco)
47. [TIP: Chat Completions API reference - as a single request, for AI ...](https://community.openai.com/t/tip-chat-completions-api-reference-as-a-single-request-for-ai-understanding/1355654)
48. [Messages API (/messages) - TrueFoundry Docs](https://www.truefoundry.com/docs/ai-gateway/messages-overview)
49. [Anthropic Messages API Documentation: Endpoints, Requests ...](https://blogs.novita.ai/anthropic-messages-api-documentation/)
50. [OpenAI vs Anthropic API Compatibility Guide | Lofee](https://llmfly.ai/blog/2026/08/28/openai-vs-anthropic-api-compatibility-guide/)
51. [Anthropic Messages vs OpenAI Chat Completions: Mapping the ...](https://flo2.com/blog/anthropic-to-openai-format)
52. [LLM API Parameter Compatibility Reference - Anthropic, OpenAI ...](https://hidekazu-konishi.com/entry/llm_api_parameter_compatibility_reference.html)
53. [OpenAI Responses API vs. Chat Completions vs. Anthropic ...](https://live.paloaltonetworks.com/t5/engineering-blogs/openai-responses-api-vs-chat-completions-vs-anthropic-messages/ba-p/1264688)
54. [Messages (Anthropic) - ai& API Documentation](https://docs.aiand.com/api/messages/)
55. [6 Reasons Why Claude Code Uses OpenAI Compatibility Mode ...](https://help.apiyi.com/en/claude-code-openai-compatible-mode-instead-of-v1-messages-en.html)
56. [Generating content | Gemini API | Google AI for Developers](https://ai.google.dev/api/generate-content)
57. [Generate content with the Gemini API | Gemini Enterprise Agent Platform | Google Cloud Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/inference?authuser=1)
58. [Method: googleapis.aiplatform.v1.projects.locations.endpoints ...](https://cloud.google.com/workflows/docs/reference/googleapis/aiplatform/v1/projects.locations.endpoints/generateContent)
59. [Examples](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/function-calling)
60. [Examples](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/grounding)
61. [Specify a MIME response type for the Gemini API - Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-gemini-controlled-generation-response-schema)
62. [Structured output | Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/control-generated-output)
63. [/generateContent | liteLLM](https://docs.litellm.ai/docs/generateContent)
64. [Google Gen AI SDK documentation - googleapis.github.io](https://googleapis.github.io/python-genai/)
65. [thinking_mode_api_example_tool_call | DeepSeek API Docs](https://api-docs.deepseek.com/api_samples/thinking_mode_api_example_tool_call/)
66. [Introducing DeepSeek-V3](https://api-docs.deepseek.com/news/news1226)
67. [Responses API - DeepSeek API Docs](https://api-docs.deepseek.com/api/create-response/)
68. [deepseek-reasoning-chat.md - new-api-docs - GitHub](https://github.com/QuantumNous/new-api-docs/blob/main/docs/en/api/deepseek-reasoning-chat.md)
69. [Testing DeepSeek V4 Pro's Three API Formats - Apidog](https://apidog.com/blog/deepseek-v4-pro-api-formats-compared/)
70. [Deepseek Reasoner V3.1 Terminus - AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/deepseek/deepseek-reasoner-v3.1-terminus)
71. [How can I use function calling with response format (structured ...](https://community.openai.com/t/how-can-i-use-function-calling-with-response-format-structured-output-feature-for-final-response/965784)
72. [DeepSeek API Docs 2026 — Quickstart & Examples](https://deepseek.ai/docs)
73. [联网搜索- 智谱AI开放文档](https://docs.bigmodel.cn/cn/guide/tools/web-search)
74. [工具调用](https://docs.bigmodel.cn/cn/guide/capabilities/function-calling)
75. [HTTP API 调用- 智谱AI开放文档](https://docs.bigmodel.cn/cn/guide/develop/http/introduction)
76. [api-evangelist/zhipu-ai - GitHub](https://github.com/api-evangelist/zhipu-ai)
77. [Z AI (Zhipu AI) - Cline documentation](https://docs.cline.bot/provider-config/zai)
78. [ZhipuAI / ChatGLM / BigModel - Portkey Docs](https://docs.portkey.ai/docs/integrations/llms/zhipu)
79. [Glm 4.5 - AI/ML API Documentation](https://docs.aimlapi.com/api-references/text-models-llm/zhipu/glm-4.5)
80. [ZhipuAI API - 智谱AI](https://open.bigmodel.cn/dev/api)
81. [Alibaba Cloud Model Studio:FAQ - Coding Plan](https://www.alibabacloud.com/help/en/model-studio/coding-plan-faq)
82. [Alibaba Cloud Model Studio:DashScope API Reference](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-dashscope)
83. [Alibaba Cloud Model Studio - Text generation](https://www.alibabacloud.com/help/en/model-studio/text-generation)
84. [Make your first API call to Qwen - Alibaba Cloud Model Studio](https://www.alibabacloud.com/help/en/model-studio/first-api-call-to-qwen)
85. [Call Qwen VL models through the OpenAI interface](https://www.alibabacloud.com/help/en/model-studio/qwen-vl-compatible-with-openai)
86. [Alibaba Cloud Model Studio:Code capabilities (Qwen-Coder)](https://www.alibabacloud.com/help/en/model-studio/qwen-coder)
87. [Alibaba Cloud Model Studio:Obtain an API key](https://www.alibabacloud.com/help/en/model-studio/get-api-key)
88. [OpenAI API error: Connection error.] · Issue #96 · QwenLM/qwen-code](https://github.com/QwenLM/qwen-code/issues/96)
89. [Responses Protocol - OpenModel](https://docs.openmodel.ai/en/docs/api-reference/responses)
