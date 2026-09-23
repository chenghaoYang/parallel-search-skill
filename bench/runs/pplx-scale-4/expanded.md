## 01.json

两者都是 `POST`：`Chat Completions` 使用 `/v1/chat/completions`，对话放在 `messages`；`Responses` 使用 `/v1/responses`，对话放在 `input`，系统/开发者指令通常放在顶层 `instructions`。[1]

## 官方字段对照

| API | HTTP 方法与路径 | 对话内容字段 | 系统提示 / 开发者指令 |
|---|---|---|---|
| Chat Completions | `POST https://api.openai.com/v1/chat/completions` | `messages`：消息数组，每条含 `role` 和 `content` | 放在 `messages` 中，`role: "system"` 或 `role: "developer"` |
| Responses | `POST https://api.openai.com/v1/responses` | `input`：可以是字符串或 Input Item 数组 | 推荐放在顶层 `instructions`；也可在 `input` 消息中使用 `role: "system"` 或 `role: "developer"` |

官方迁移文档明确给出的路径是 `post /v1/chat/completions` 和 `post /v1/responses`，并分别使用请求字段 `messages` 与 `input`。[1]

## Chat Completions

- 官方参考：[Create chat completion](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
- `messages` 是“迄今为止组成对话的消息列表”。
- 每条消息使用 `role` 标识作者、`content` 存放内容。
- 开发者指令可写成 `role: "developer"` 的消息；官方说明，o1 及更新模型用 `developer` 消息取代之前的 `system` 消息。[2]

```json
{
  "model": "MODEL_ID",
  "messages": [
    {
      "role": "developer",
      "content": "你是一个简洁、准确的中文助手。"
    },
    {
      "role": "user",
      "content": "你好"
    }
  ]
}
```

兼容旧式写法时，也可以把第一条消息的 `role` 写成 `"system"`；其指令内容仍然放在该消息的 `content` 字段。[2]

## Responses

- 官方参考：[Create a model response](https://developers.openai.com/api/reference/resources/responses/methods/create)
- `input` 存放文本、图片、文件等模型输入；字符串 `input` 等价于一条 `user` 消息。[3]
- 多轮对话时，`input` 可以是多个消息 Item，`role` 可为 `"user"`、`"assistant"`、`"system"` 或 `"developer"`。[3]
- 顶层 `instructions` 用于模型行为、语气、目标和示例等高层指令；官方说明其优先级高于 `input` 中的提示，且只适用于当前生成请求。[4]

```json
{
  "model": "MODEL_ID",
  "instructions": "你是一个简洁、准确的中文助手。",
  "input": [
    {
      "role": "user",
      "content": "你好"
    }
  ]
}
```

单轮简单请求也可以写成：

```json
{
  "model": "MODEL_ID",
  "instructions": "你是一个简洁、准确的中文助手。",
  "input": "你好"
}
```

若为了迁移而保留现有消息结构，也可以把系统指令作为 `input` 数组中的消息传入：

```json
{
  "model": "MODEL_ID",
  "input": [
    {
      "role": "system",
      "content": "你是一个简洁、准确的中文助手。"
    },
    {
      "role": "user",
      "content": "你好"
    }
  ]
}
```

官方迁移文档将映射概括为：Chat Completions 的 `messages[]` 对应 Responses 的 `input`；“system 或 developer guidance”对应顶层 `instructions`，或者在需要保留原有对话记录时使用兼容的消息 Item。[1]

## 02.json

创建 Anthropic Messages API 消息的 HTTP 路径是：

```http
POST /v1/messages
```

官方文档原句：“`POST /v1/messages`”。  
官方 URL：[Anthropic / Claude API Reference — Create a Message](https://platform.claude.com/docs/en/api/messages/create)[1]

## 系统提示的位置

系统提示应通过请求体**顶层**的 `system` 参数提供，而不是作为常规输入消息中的 `role: "system"`。

官方原句：

> “Note that if you want to include a system prompt, you can use the top-level `system` parameter — there is no `"system"` role for input messages in the Messages API.”

即：若要加入系统提示，应使用顶层 `system`；Messages API 的输入消息中没有 `"system"` 角色。[1]

示例：

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 1024,
  "system": "You are a concise assistant.",
  "messages": [
    {
      "role": "user",
      "content": "Explain recursion."
    }
  ]
}
```

## 输入消息允许的 role

常规 `messages` 输入数组中，允许使用：

- `user`
- `assistant`

官方原句：

> “You can specify a single `user`-role message, or you can include multiple `user` and `assistant` messages.”

此外，官方说明每条输入消息都必须包含 `role` 和 `content`：

> “Each input message must be an object with a `role` and `content`.”[1]

## 注意文档中的表面矛盾

同一 API 参考页的类型枚举可能显示 `role: "user" or "assistant" or "system"`，但该页针对**输入消息**的文字规范明确指出没有 `"system"` role，系统提示应使用顶层 `system`。因此，若你的问题是“创建消息请求中的 `messages` 数组应如何写”，应采用：

```json
"messages": [
  { "role": "user", "content": "..." },
  { "role": "assistant", "content": "..." }
]
```

并把全局系统指令放在：

```json
"system": "..."
```

该结论以 Anthropic 官方 Create a Message API 文档对输入消息和系统提示的明确说明为准。[1]

## 03.json

答案如下，全部来自 Google 官方 Gemini API 文档（[Generating content | Gemini API](https://ai.google.dev/api/generate-content)）。

## 完整 HTTP URL

`generateContent` 的完整调用形态是：POST 请求，模型名放在 URL 路径里，API key 放在查询参数 `[1][9]`

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key=$GEMINI_API_KEY
```

官方 curl 示例原文（请求头部为 `Content-Type: application/json`）：[1]

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
 -H 'Content-Type: application/json' \
 -X POST \
 -d '{ "contents": [{ "parts":[{"text": "Write a story..."}] }] }'
```

流式版本则把方法换成 `:streamGenerateContent` 并加 `alt=sse` 参数 。[1]

## 对话历史：contents

对话历史放在请求体的 **`contents`** 字段（不是 OpenAI 的 `messages`）。它是一个数组，每个元素是 `{"role": ..., "parts": [...]}`，其中 `role` 取 `"user"` 或 `"model"`（OpenAI 用 `assistant`，Gemini 用 `model`）。官方多轮对话的 Shell 示例：[1]

```json
{
  "contents": [
    {"role": "user",  "parts": [{"text": "Hello"}]},
    {"role": "model", "parts": [{"text": "Great to meet you. What would you like to know?"}]},
    {"role": "user",  "parts": [{"text": "I have two dogs in my house. How many paws are in my house?"}]}
  ]
}
```

## 系统指令：system_instruction

系统指令是请求体顶层的 **`system_instruction`**（SDK 与部分文档示例中也写作 camelCase 的 `systemInstruction`），值为一个 Content 对象 。官方函数调用示例中的用法：[1][2]

```json
{
  "system_instruction": {
    "parts": {"text": "You are a helpful lighting system bot..."}
  },
  "contents": {"role": "user", "parts": {"text": "Turn on the lights please."}}
}
```

## 与 OpenAI 的字段名对照

不同名。对比如下 ：[2]

| 概念 | OpenAI Chat Completions | Gemini generateContent |
|---|---|---|
| ICT对话历史 | `messages` | `contents` |
| 助手角色 | `assistant` | `model` |
| 系统指令 | `messages` 中的 system 消息 | 顶层 `system_instruction` |
| 内容单元 | `content` | `parts[]` |

另外注意一点：Google 也提供了 OpenAI 兼容端点（用 `messages` 格式调用 Gemini），但那是兼容层，不是上面这个原生 `generateContent` API 。[3]

官方文档 URL：
- [Generating content | Gemini API - Google AI for Developers](https://ai.google.dev/api/generate-content?hl=zh-cn)
- 英文版：[https://ai.google.dev/api/generate-content](https://ai.google.dev/api/generate-content)

## 04.json

按两家**当前官方文档**，核心配置如下：

| 平台/协议 | base URL | 聊天接口路径 |
|---|---|---|
| DeepSeek OpenAI 兼容 | `https://api.deepseek.com` | `POST /chat/completions`，完整地址为 `https://api.deepseek.com/chat/completions` [1][2] |
| DeepSeek Anthropic 兼容 | `https://api.deepseek.com/anthropic` | Anthropic SDK 调用 Messages API；HTTP 完整路径为 `POST https://api.deepseek.com/anthropic/v1/messages` [3] |
| 智谱 Claude Code / Anthropic SDK | `https://open.bigmodel.cn/api/anthropic` | HTTP 完整路径为 `POST https://open.bigmodel.cn/api/anthropic/v1/messages` [4][5] |

## DeepSeek 思考字段

OpenAI Chat Completions 兼容响应中的思维链字段名是：

```text
reasoning_content
```

具体位置为：

- 非流式：`choices[0].message.reasoning_content`
- 流式：`choices[0].delta.reasoning_content`
- 最终回答仍是 `content`，两者同级[2][6]

需要注意：`reasoning_content` 是**返回的思维链字段**；`thinking` 通常用于控制思考模式，两者不是同一个字段。Anthropic 兼容格式则支持 `thinking` 内容块 。[3][6]

## 官方 URL

- DeepSeek 首次调用与 base URL：[Your First API Call](https://api-docs.deepseek.com/)[1]
- DeepSeek Anthropic 兼容：[使用 Anthropic API](https://api-docs.deepseek.com/zh-cn/guides/anthropic_api/)[3]
- DeepSeek 聊天路径：[Chat Completions API](https://api-docs.deepseek.com/zh-cn/api/create-chat-completion/)[2]
- DeepSeek 思考字段：[思考模式](https://api-docs.deepseek.com/zh-cn/guides/thinking_mode)[6]
- 智谱 Anthropic SDK 兼容：[Claude API 兼容](https://docs.bigmodel.cn/cn/guide/develop/claude/introduction)[4]
- 智谱 Claude Code 配置：[Claude Code](https://docs.bigmodel.cn/cn/guide/develop/claude)[5]
