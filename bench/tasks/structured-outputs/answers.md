# structured-outputs 任务参考答案

给人工检查者用的简明答案，对应 task.md 里用户提出的疑问。核实日期：2026-09-24。

## 1. "OpenAI strict 模式 100% 保证 schema 合法、连 allOf 都支持" —— 半对半错

**前半句基本对，后半句错。** `strict: true` + `json_schema` 确实是对"被接受的 schema"的结构性保证：字段不缺、类型/枚举不越界、不多出未声明的键——官方原话是"ensures the model will always generate responses that adhere to your supplied JSON Schema"。但它只保证**受支持的 JSON Schema 子集**：组合/条件类关键字 `allOf`、`not`、`if`/`then`/`else`、`dependentRequired`/`dependentSchemas` 都不支持，传了会直接报错；根 schema 必须是 object，顶层不能用 `anyOf`（Zod discriminated union 这种写法要拆掉）。另外"保证"只管结构不管内容正确性，refusal/截断时也可能拿不到完整对象。
来源：https://developers.openai.com/api/docs/guides/structured-outputs

## 2. "Anthropic 没有正式结构化输出、只能 tool use 硬凑" —— 已过时

**Anthropic 现在有原生 Structured Outputs**（2025 年 11 月公测，2026 年已 GA）：
- 响应 JSON：用 `output_config.format`（`type: "json_schema"`），beta 期的 `output_format` 参数已迁移过去，beta header 也不再必需。
- 工具参数：tool 定义上加 `strict: true`，对 tool 名称和 input 做 grammar-constrained 校验——以前的"假工具强凑 JSON"套路正式转正。
和 OpenAI 的重要差异：Anthropic **允许可选字段**（不必把所有 properties 列进 required），字段顺序是 required 在前、optional 在后；schema 子集也不同——不支持递归 schema、不支持外部 `$ref`（本地 `$ref`/`$def` 可以）、不支持 `minimum`/`maximum`/`multipleOf` 数值约束和 `minLength`/`maxLength`。流式可用；与 Citations 不兼容。
来源：https://platform.claude.com/docs/en/build-with-claude/structured-outputs ；https://claude.com/blog/structured-outputs-on-the-claude-developer-platform

## 3. "Gemini responseSchema 不支持 $ref、字段顺序要靠 propertyOrdering" —— 半对半错

- **responseSchema vs responseJsonSchema 是两个不同字段**：`responseSchema` 是老的 OpenAPI 3.0 Schema 子集（确实功能有限）；后来新增的 `responseJsonSchema` 接受标准 JSON Schema 文档，支持 `anyOf`、`$ref`（含递归）、`prefixItems`、`additionalProperties`、`type: "null"`、数值边界等，能直接吃 Pydantic `model_json_schema()` / Zod 输出。已覆盖所有 actively supported Gemini 模型，OpenAI 兼容接口同样适用。
- **字段顺序**：Gemini 2.5+ 输出自动保持 schema 键序，不需要手写；只有 Gemini 2.0 需要显式 `propertyOrdering`。
- 两边都要求 `responseMimeType`/`mime_type` 设为 `application/json`。
来源：https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-structured-outputs/ ；https://ai.google.dev/gemini-api/docs/generate-content/structured-output

## 4. DeepSeek：只有"合法 JSON"档，没有 schema 强制

DeepSeek 的 JSON Output（`response_format: {"type": "json_object"}`）只保证输出是**可解析的合法 JSON 字符串**，不保证符合你给的 schema——字段名、类型、多余字段都不保。官方要求：system 或 user prompt 里**必须包含单词 "json"**、建议附上期望格式的示例、`max_tokens` 要留够防止 JSON 被截断（文档还提示偶尔会返回空内容）。要做 schema 级校验得自己在应用层做（Pydantic/Zod 校验 + 重试）。
来源：https://api-docs.deepseek.com/guides/json_mode/

## 5. 次要实体：xAI Grok、Mistral

- **xAI Grok**：`response_format: {"type": "json_schema", "json_schema": {..., "strict": true}}`，官方承诺"使用受支持 schema 特性时响应保证匹配 schema"；工具 schema 的 `strict` 隐式恒为 true（始终强制）。注意细节差异：xAI 的 `additionalProperties` **默认就是 false**，想放开要显式设 true（和 OpenAI 强制 false 相反方向）；部分关键字"接受但不做结构强制"（如多子 schema 的 allOf、超限的 min/maxItems），工具侧结构化输出限 Grok 4 系模型。
- **Mistral**：`response_format` 分 `json_object`（只保证合法 JSON）和 `json_schema`（保证遵循所给 schema）两档，语义和 OpenAI 对齐；json_object 档也建议在 prompt 里明确要求返回 JSON。
来源：https://docs.x.ai/developers/model-capabilities/text/structured-outputs ；https://docs.mistral.ai/api/ ；https://docs.mistral.ai/studio/conversations/structured-output/json_mode

## 6. 各家 schema 子集差异速查（都在打"JSON Schema 子集"，但子集不一样）

| 维度 | OpenAI strict | Anthropic | Gemini (responseJsonSchema) | xAI | Mistral |
|---|---|---|---|---|---|
| 保证级别 | schema 级（受限子集） | schema 级（constrained decoding） | schema 级 | schema 级（受支持特性内） | schema 级 |
| 全部字段必须 required | 是（可空用 `[T,"null"]`） | 否，可选字段合法 | 否 | — | — |
| `additionalProperties` | 必须 false | objects 须 false | 支持（布尔或 schema） | 默认 false，可显式 true | — |
| `allOf` | 不支持 | 支持（带 `$ref` 的 allOf 不行） | — | 多子 schema 仅尽力 | — |
| `anyOf` | 支持（但根不能是 anyOf） | 支持 | 支持 | — | — |
| `$ref`/递归 | 本地 `$defs` + `#` 递归都支持 | 本地可以，外部不行；不支持递归 | `$ref` 含递归支持 | 非循环 `$ref`/`$defs` | — |
| 数值/字符串约束 | `minimum`/`maximum`/`pattern` 等支持（微调模型除外） | 不支持 `minimum`/`maximum`/`minLength`/`maxLength` | `minimum`/`maximum`/`format`/`minItems`/`maxItems` 支持 | 有界内保证（如 min/maxLength ≤2048） | — |
| schema 大小限制 | ≤5000 属性、≤10 层、≤120k 字符、≤1000 枚举 | 未给硬上限 | 过大/过深可能被拒 | — | — |

结论：同一份 Zod/Pydantic schema 不能假设跨家通用，最稳的公共子集是 object/array/标量/enum/required/additionalProperties:false + 浅嵌套。

## 7. 流式与 function calling 的关系

- **流式**：OpenAI（`text.format` + `stream:true`，SDK 有结构化流式解析）、Anthropic（"Stream structured outputs like normal responses"）、Gemini 都支持流式下用结构化输出；单个 delta 不是合法 JSON，要累积或走 SDK 解析。Anthropic 侧注意：structured outputs 与 Citations 不兼容。
- **与 function calling**：两家都把"工具参数 schema"和"响应 schema"打通——OpenAI 是同一个 strict 机制用在 `text.format` 和 tool 定义上（但 strict 与 parallel_tool_calls 不兼容，要关并行调用）；Anthropic 拆成 `output_config.format`（管回答）和 `strict:true` 工具（管入参），可同请求并用；xAI 工具隐式 strict；Gemini 的 function declaration 用的还是 `responseSchema` 那套 OpenAPI 子集。
来源：https://developers.openai.com/api/docs/guides/structured-outputs ；https://platform.claude.com/docs/en/build-with-claude/structured-outputs ；https://docs.x.ai/developers/model-capabilities/text/structured-outputs

## 8. 字段顺序

- OpenAI：输出按 schema `properties` 键序生成（可用来把要先渲染的字段排前面，配合流式）。
- Anthropic：保持 schema 定义顺序，但 required 字段先出、optional 后出。
- Gemini：2.5+ 自动保持 schema 键序；2.0 需手写 `propertyOrdering`。
- 注意：JSON 语义上对象键无序，别把键序当业务契约，只当生成顺序/体验优化。
