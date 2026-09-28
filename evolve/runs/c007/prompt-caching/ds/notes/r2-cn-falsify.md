# r2-cn-falsify
question: 反证国内三家缓存文档中的「官方未写」格子——智谱 D4/D7、Kimi D2、通义显式 D7，只找反例
checked: docs.bigmodel.cn/llms.txt + cn/guide/start/pricing.md + model-overview.md + capabilities/cache.md + api-reference/模型-api/对话补全.md + develop/{openai,responses,claude}/introduction.md + models/text/glm-5.3.md + models/vlm/glm-5.3-flash.md ; docs.z.ai/llms.txt + guides/capabilities/cache.md ; open.bigmodel.cn ; platform.kimi.com/docs/llms.txt + api/{chat,messages,responses,models-overview}.md + models.md + guide/{kimi-k3-quickstart,kimi-k2-7-code-quickstart,kimi-k2-6-quickstart,context-caching,troubleshooting,use-moonpalace}.md + changelog/index.md ; help.aliyun.com/zh/model-studio/context-cache

## claims

### 智谱（D7 推翻，D4 部分推翻）
- [C1] D7 反例：定价页按模型列「缓存命中」单价=官方支持清单。有命中价：GLM-5.3 ¥2、5.3-Flash ¥0.23、5.3-FlashX ¥0.57、5.2 ¥2、5.1 ¥1.3/2、5-Turbo ¥1.2/1.8、5 ¥1/1.5、4.7 ¥0.4-0.8、4.5-Air ¥0.16/0.24、4.7-FlashX ¥0.1、4.7-Flash 免费、4-Plus ¥2.5、4-Air-250414 ¥0.25、4-Long ¥0.5、4-FlashX-250414 ¥0.05、5V-Turbo ¥1.2/1.8、4.6V ¥0.2/0.4、4.6V-FlashX ¥0.03、4.6V-Flash 免费、4.5V ¥0.4/0.8、4V-Plus-0111 ¥2；标「不支持」：GLM-4-AirX、4-Assistant、Z1-Air/AirX/FlashX/Flash、4-Flash-250414、GLM-OCR、4V-Flash、4.1V-Thinking-FlashX/Flash | src: https://docs.bigmodel.cn/cn/guide/start/pricing.md | quote: "缓存存储（元/百万 Tokens/小时） | 缓存命中（元/百万 Tokens）" | type: official
- [C2] D4 部分反例：计费公式含「缓存存储费用」按 元/百万Tokens/小时 计、当前限时免费——存在按时长计费维度，但仍无 TTL 数值 | src: https://docs.bigmodel.cn/cn/guide/start/pricing.md | quote: "调用费用 = 未命中缓存的输入费用 + 缓存命中费用 + 输出费用 + 缓存存储费用"；"缓存存储当前限时免费" | type: official
- [C3] D7 反例（英文站） | src: https://docs.z.ai/guides/capabilities/cache.md | quote: "Supports all mainstream models, including GLM-5, GLM-4.7, GLM-4.6, GLM-4.5 series, etc." | type: official
- [C4] D4 弱反例（英文站）：承认过期、无时长 | src: https://docs.z.ai/guides/capabilities/cache.md | quote: "Cache has reasonable time limits, will recalculate after expiration" | type: official
- [C5] 模型页佐证：GLM-5.3/5.3-Flash 详情页列上下文缓存为能力 | src: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3.md | quote: "[上下文缓存](/cn/guide/capabilities/cache)：智能缓存机制，优化长对话性能" | type: official
- [C6] 无显式开关未找到反例：对话补全 ref 仅响应字段 cached_tokens，无请求侧缓存参数；三个兼容指南页 grep cache 无请求字段 | src: https://docs.bigmodel.cn/api-reference/模型-api/对话补全.md | quote: "cached_tokens: description: 命中的缓存 `Token` 数量" | type: official

### Kimi（D2 推翻：256 token 阈值）
- [C7] D2 反例：K3 快速开始页给官方数值——前一请求 prompt tokens>256 才可被缓存，<256 不缓存直接丢弃 | src: https://platform.kimi.com/docs/guide/kimi-k3-quickstart.md | quote: "当前一个请求的 prompt tokens 大于 256 时，新的请求才能命中前缀缓存；当前一个请求的 prompt tokens 小于 256 时，请求不会被缓存而是被丢弃。" | type: official
- [C8] 显式断点被拒绝 | src: https://platform.kimi.com/docs/api/chat.md | quote: "暂不支持显式缓存断点：`content` 中出现 `prompt_cache_breakpoint` 时请求会被拒绝（HTTP 400）" | type: official
- [C9] Messages API：不传顶层 cache_control 则只读 5m 档不写入；usage 细分 cache_creation.ephemeral_5m/1h_input_tokens | src: https://platform.kimi.com/docs/api/messages.md | quote: "不传 `cache_control`：本次请求只尝试读取缓存（`5m` 档），不写入缓存，不产生缓存写入费用。" | type: official
- [C10] 过期表述 | src: https://platform.kimi.com/docs/api/chat.md | quote: "不支持手动清除缓存，已缓存的前缀在至少 5 分钟不活动后自动过期。" | type: official
- [C11] changelog：2024-08 "Cache 存储费用降低"；2024-11 全量放开+续期免创建费；2025-10 "下线手动 Cache 展示功能" | src: https://platform.kimi.com/docs/changelog/index.md | quote: "Context Caching 功能放开给全量用户，Cache 续期不再收取创建费用" | type: official

### 通义显式（D7 推翻 + DashScope 原生支持推翻）
- [C12] D7 反例：context-cache 页内含显式缓存「支持的模型」分地域表。北京：Max qwen3.8-max/0902、qwen3.7-max(+-05-20/-06-08)、qwen3.6-max-preview、qwen3-max；开源 qwen3.8-2.4t-a95b、qwen3.8-27b；Plus qwen3.7-plus(+-05-26)、qwen3.6/3.5-plus(+-04-20)、qwen-plus；Flash qwen3.8/3.7(+-07-15)/3.6/3.5-flash、qwen-flash；Coder qwen3-coder-plus/flash；VL qwen3-vl-plus/flash；Character qwen-plus-character；第三方 deepseek-v3.2、kimi-k2.6/k2.5/k2.7-code、glm-5.1。另有美/新/法兰克福/东京/香港清单 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "支持的模型 华北 2（北京） 千问 Max：qwen3.8-max、qwen3.8-max-0902、qwen3.7-max…GLM：glm-5.1" | type: official
- [C13] DashScope 原生支持 cache_control：官方示例用原生 SDK（Python MultiModalConversation、Java Generation≥2.21.6）打原生端点 /api/v1，消息内放 cache_control | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "以下示例展示了在 OpenAI 兼容、DashScope 和 Anthropic 兼容协议中…dashscope.base_http_api_url = \"https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1\"" | type: official
- [C14] 原生响应字段：usage.prompt_tokens_details['cache_creation_input_tokens']、['cached_tokens'] | src: 同上 | type: official
- [C15] 显式机制细节：标记向前回溯最多 20 个 content 块；中间 message 超 20 条不命中旧块（仍新建块）；缓存创建发生在模型响应之后 | src: 同上 | quote: "向前回溯最多 20 个 content 块，尝试命中缓存" | type: official

## conflicts
- 推翻 r1-cn3 智谱 D7「∅」：清单在 pricing.md 缓存命中列（含「不支持」）+ z.ai "all mainstream models"，仅指南页无。
- 推翻 r1-cn3 Kimi D2「∅」：256 阈值存在但只在 K3 快速开始页；context-caching.md 仍无数字，块大小仍无。
- 推翻 r1-cn3 通义显式 D7「⚠ 清单指回主页」与 gap「DashScope 原生未演示」：清单就在 context-cache 页显式节，原生 SDK 示例即用 cache_control。
- 智谱内部矛盾：指南称命中「通常为标准价格的 50%」，定价表 GLM-5.3 命中 2/8=25%、5.1≈22%、4.7=20%，旗舰实为 ~20-25%。

## gaps
- 智谱 TTL 数值、失效规则仍无：cache.md grep TTL/有效期/过期/清理/存储 0 命中。显式开关无反例（对话补全 ref+三兼容页均无请求字段），主张成立。open.bigmodel.cn 为控制台落地页非文档。
- Kimi 缓存块大小仍无官方数值；256 阈值是否限 K3 未写明（K2.7/K2.6 快速开始页无此句）。

## leads
- 智谱「缓存存储 元/百万Tokens/小时」为 Gemini explicit 式按时计费维度，免费期结束或公布 TTL/费率。
- Kimi 曾有 Cache 存储费（2024-08 changelog），现行无。
- context-cache 页注明 PTU 命中按折扣系数折算、Responses API 另有 Session 缓存（x-dashscope-session-cache）。
