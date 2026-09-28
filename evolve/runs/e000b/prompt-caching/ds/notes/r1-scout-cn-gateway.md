# r1-scout-cn-gateway
question: 侦察任务：(a) 智谱 AI（Zhipu / BigModel，GLM 系列模型）的 API 缓存机制；(b) 阿里通义千问（Qwen / DashScope）的 API 缓存机制；(c) OpenRouter 网关对上游各厂商 prompt caching 的处理方式（是透传上游原生机制、还是自己统一封装了一层）
checked: https://docs.bigmodel.cn/cn/guide/capabilities/cache,https://help.aliyun.com/zh/model-studio/context-cache,https://openrouter.ai/docs/guides/best-practices/prompt-caching,https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/,https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope

## claims
### 智谱 GLM
- [C1] D1 触发方式：自动隐式（F1），系统自动识别重复内容，无需参数 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "系统会通过计算输入消息内容来识别和重用之前请求中的相同内容" | type: official
- [C2] D3 最小可缓存长度：500+ tokens | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "重复前缀内容需要足够长（推荐 500+ tokens）" | type: official
- [C3] D4 命中计费：约 50% 折扣（原价的 50%）| src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "缓存 tokens 按标准价格的约 50% 收费" | type: official
- [C4] D6 TTL：5 分钟，自动刷新 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "缓存有效期 5 分钟，命中时自动刷新" | type: official
- [C5] D8 命中确认：usage.prompt_tokens_details.cached_tokens（数字，>0 表示命中）| src: https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8 | quote: "使用 usage.prompt_tokens_details.cached_tokens 查看命中的缓存 token 数" | type: official
- [C6] D2 代码改动：不需要修改代码，自动生效 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "无需配置任何参数，自动启用" | type: official

### 阿里通义千问 / DashScope
- [C7] D1 触发方式：既有自动隐式（F1），也有显式缓存（F2），支持两种模式 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "支持显式缓存（需添加 cache_control marker）和隐式缓存（系统自动识别）" | type: official
- [C8] D1-显式 cache_control 参数：cache_control: {type: "ephemeral"} 在消息内容块上标记 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "在 message content 上添加 cache_control: {type: \"ephemeral\"} 来标记缓存边界" | type: official
- [C9] D3 最小可缓存长度（显式）：1024 tokens | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "显式缓存要求最少 1024 token" | type: official
- [C10] D4 命中计费（显式）：10%（原价的 10%）| src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "显式缓存命中部分按输入价格的 10% 计费" | type: official
- [C11] D4 命中计费（隐式）：约 20%（原价的 20%）| src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "隐式缓存命中部分约为标准价的 20%" | type: official
- [C12] D5 写入计费（显式）：125%（比标准输入费贵 25%）| src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "创建缓存需要 125% 的输入 token 费用" | type: official
- [C13] D6 TTL（显式）：5 分钟，命中时重置 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "显式缓存有效期 5 分钟，每次命中时自动续期" | type: official
- [C14] D7 失效条件：系统检查最近 20 个 content block 内的缓存匹配 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "系统会自动检查最近 20 个内容块是否有缓存匹配" | type: official
- [C15] D9 支持范围：Qwen Max/Plus/Flash/Coder/VL，plus DeepSeek/Kimi/GLM through Bailian | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "支持 Qianwen Max/Plus/Flash/Coder/VL 等模型，以及通过 Bailian 部署的 DeepSeek/Kimi/GLM" | type: official
- [C16] D2 代码改动（显式）：需要在请求中添加 cache_control 参数 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "显式缓存需在消息内容上添加 cache_control marker" | type: official
- [C17] D2 代码改动（隐式）：不需要修改代码 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "隐式缓存自动启用，无需配置" | type: official

### OpenRouter
- [C18] D1 触发方式：透传上游原生机制，Anthropic/Alibaba 使用显式缓存（F2），OpenAI/DeepSeek/Gemini 2.5 使用自动隐式（F1）| src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "大多数厂商（OpenAI/DeepSeek/Gemini）自动缓存，Anthropic 和 Alibaba 需显式 cache_control breakpoint" | type: official
- [C19] D1-OpenRouter 增强机制：粘性路由（sticky routing），后续请求自动路由到同一端点以增强缓存命中 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "OpenRouter 自动在缓存命中时激活粘性路由，将后续请求路由到同一端点，10 分钟无活动后失效" | type: official
- [C20] D2 代码改动：可选，使用 session_id 头或请求体来控制粘性路由；cache_control 取决于上游 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "session_id 可在请求头 x-session-id 或请求体中指定，长度最长 256 字符" | type: official
- [C21] D3 最小可缓存长度（按上游）：OpenAI 1024，Anthropic 1024-4096，Gemini 1024-4096 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "OpenAI 1024 token minimum；Anthropic/Gemini 1024-4096" | type: official
- [C22] D4 命中计费（OpenAI）：0.25-0.5x input | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "OpenAI 缓存读取成本 0.25-0.5x 输入价" | type: official
- [C23] D4 命中计费（Anthropic）：0.1x input | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Anthropic 缓存读取成本 0.1x 输入价" | type: official
- [C24] D4 命中计费（Gemini）：0.25x input | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Google Gemini 缓存读取成本 0.25x 输入价" | type: official
- [C25] D4 命中计费（DeepSeek）：0.1x input | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "DeepSeek 缓存读取成本 0.1x 输入价" | type: official
- [C26] D5 写入计费（Anthropic）：1.25x (5min TTL) 或 2.0x (1hour TTL) | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "Anthropic cache write 1.25x input (5min) 或 2.0x (1hour)，未使用写入成本超过不缓存" | type: official
- [C27] D6 TTL（Anthropic）：5 分钟（默认）或 1 小时（可配置）| src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Anthropic TTL 5 min (default) or 1 hour" | type: official
- [C28] D6 TTL（Gemini）：3-5 分钟 | src: https://openrouter.ai/docs/guides/best-practices/prompt-caching | quote: "Google Gemini TTL 3-5 minutes" | type: official
- [C29] D8 命中确认：usage.prompt_tokens_details.cached_tokens（>0 表示命中）| src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "检查响应的 usage.prompt_tokens_details.cached_tokens 字段确认缓存命中" | type: official
- [C30] D1-粘性路由激活时机：首次成功请求后立即激活，无需等待缓存命中 | src: https://openrouter.ai/blog/tutorials/prompt-caching-sticky-routing/ | quote: "With session_id, sticky routing kicks in after the first successful request, before any cache hit has happened" | type: official

## conflicts
- 无直接冲突，但 OpenRouter 的成本结构（粘性路由）与透传原生机制的关系需进一步澄清：是否所有厂商都支持 sticky routing，还是只有特定厂商？

## gaps
- 智谱 GLM：D5（写入计费）、D7（失效条件是否仅限前缀变化）、D9（所有 GLM 模型是否都支持缓存）、D10（存储位置）未明确
- 阿里 DashScope：隐式缓存的 D6（TTL）、D8（命中确认字段名是否与显式相同）未明确；D10（存储位置）未说明
- OpenRouter：D9（是否默认对所有上游模型启用 sticky routing）、D10（存储位置）未说明；与各上游原生 cache 的具体计费关系需确认
- 三家都未找到明确的「手动清缓存」或「强制 miss」API

## leads
- **智谱 GLM** 值得 R2 深挖：官方文档缺少写入计费、TTL 可否配置等细节，需查阅 API reference 的完整 response schema（特别是 usage 对象的其他字段）和最新更新日志
- **阿里 DashScope** 值得 R2 深挖：显式 vs 隐式缓存的完整对比（D5-D10 维度都需补全），特别是隐式缓存的 TTL 和 usage 响应字段名；建议查阅官方 API reference 和最新的最佳实践指南
- **OpenRouter** 尤其值得 R2 深挖：粘性路由的完整文档、对不同厂商的统一计费和计费透明度（是否各厂独立计费还是统一标价）、session_id 的具体行为边界（TTL、跨地域、多会话管理），需查阅 OpenRouter 的完整 API reference 和成本计算器
