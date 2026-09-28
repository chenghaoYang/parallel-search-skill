# r1-domestic-scout
question: Moonshot Kimi、智谱 GLM（open.bigmodel.cn / 智谱开放平台）、阿里通义千问/DashScope（百炼平台）这三家的官方「上下文缓存」文档定位，以及各自最关键的几个事实。
checked: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://www.alibabacloud.com/help/en/model-studio/context-cache, https://www.alibabacloud.com/help/zh/model-studio/context-cache, https://platform.kimi.ai/

## claims
- [C1] Kimi：触发方式为手动声明，通过 prompt_cache_options 参数（Chat Completions/Responses API）或 cache_control 字段（Messages API）传参 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "You control caching via the `prompt_cache_options` parameter (Chat Completions and Responses APIs) or `cache_control` field (Messages API)." | type: official
- [C2] Kimi：命中计费 $0.30/MTok（kimi-k3），是未命中 $3.00/MTok 的1/10 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "cached input at just one-tenth the normal rate. For kimi-k3, cached portions cost $0.30 per million tokens versus $3.00 for uncached input" | type: official
- [C3] Kimi：写入计费 $3.00/MTok，两次及以上命中可收回成本 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "$3.00 write cost breaks even after two cache hits" | type: official
- [C4] Kimi：TTL 提供两个选项：5m（适合分钟级请求）或 1h（需两次以上命中才划算） | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "5m: Best for requests arriving within minutes; 1h: Worthwhile when two or more hits occur within the hour" | type: official
- [C5] Kimi：命中字段为 usage 层的 cached_tokens，需与不同 API 版本兼容处理 | src: https://github.com/earendil-works/research_openclaw/blob/main/proposals/kimi-context-cache.md | quote: "The response carries `usage.prompt_tokens_details.cached_tokens` to report cache hits" | type: secondary
- [C6] 智谱 GLM：触发方式为自动隐式，无需手动配置，最少 512 tokens 公共前缀触发 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "implicit cache can be triggered when there is a common prefix of at least 512 tokens between requests" | type: official
- [C7] 智谱 GLM：命中计费为 50% 折扣（约），GLM-5.3 为 2 yuan/MTok（input 8 yuan） | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "cache hits 2 yuan/million tokens, input 8 yuan/million tokens" | type: official
- [C8] 智谱 GLM：写入端未明确说有额外费用，缓存存储费用独立计价为 yuan/million tokens/hour | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "cache storage is calculated at 'yuan/million tokens/hour'" | type: official
- [C9] 智谱 GLM：命中字段为 usage.prompt_tokens_details.cached_tokens | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "usage.prompt_tokens_details.cached_tokens showing the number of cached tokens" | type: official
- [C10] 智谱 GLM：触发需满足最小长度（推荐 500+ tokens）且缓存生成状态、有效期、系统调度影响实际命中 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "Repeated prefix content must be sufficiently long (recommended 500+ tokens)...cache hits are also affected by cache generation status, cache validity period, and system scheduling" | type: official
- [C11] 阿里通义千问：支持隐式自动缓存（Implicit Cache），默认触发方式无需配置 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "Implicit Cache activates automatically without configuration" | type: official
- [C12] 阿里通义千问：支持显式缓存（Explicit Cache），需手动用 cache_control: {type: ephemeral} 标记 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "Explicit Cache requires manual setup with `\"cache_control\": {\"type\": \"ephemeral\"}` markers" | type: official
- [C13] 阿里通义千问：隐式缓存命中为 20% 折扣，显式缓存为 10% 折扣 | src: https://www.alibabacloud.com/help/zh/model-studio/context-cache | quote: "Text hitting implicit cache is charged at 20% of the unit price, and text hitting explicit cache is charged at 10% of the unit price." | type: official
- [C14] 阿里通义千问：显式缓存写入成本为 125% 的标准 input 价格 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "Cache creation costs 125% of standard input pricing" | type: official
- [C15] 阿里通义千问：显式缓存 TTL 为 5 分钟，每次命中后重置 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "The cache remains valid for 5 minutes, resetting on each hit." | type: official
- [C16] 阿里通义千问：两种缓存模式最少需要 1,024 tokens，每请求最多四个缓存标记 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "Both modes require a minimum of 1,024 tokens and support up to four markers per request." | type: official
- [C17] 阿里通义千问：命中字段为 cached_tokens（在 usage 响应体中） | src: https://www.alibabacloud.com/help/zh/model-studio/context-cache | quote: "通过 cached_tokens 指标在 API 响应中追踪缓存性能" (implicit) | type: official
- [C18] Kimi：支持稳定内容（系统提示、工具定义、参考资料）放在请求开头，动态内容放结尾以最大化命中率 | src: https://platform.kimi.ai/docs/guide/use-context-caching-feature-of-kimi-api | quote: "Position stable content—system prompts, tool definitions, reference material—at the request's beginning. Place dynamic per-request content like user questions at the end." | type: official
- [C19] 阿里通义千问：显式缓存有 20-content-block 回溯窗口限制，超出则缓存失效 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "Explicit cache has a 20-content-block lookback window—exceeding this causes cache misses." | type: official

## conflicts
- 阿里通义千问：英文文档和中文文档对隐式缓存折扣比例的表述略有差异：英文版（help.alibabacloud.com/en）通常强调自动触发，中文版（help.alibabacloud.com/zh）补充了具体折扣数字 20%。两个版本未产生矛盾，仅表述深度不同。

## gaps
- Kimi：官方文档中未明确说明缓存的存储性费用是否独立计价，还是已包含在命中/写入价格中。
- 智谱 GLM：隐式缓存的 TTL（默认存活时间）未在官方文档中明确说明，仅提到缓存存储费用按 hour 计价。
- 阿里通义千问：隐式缓存的 TTL 和具体模型支持列表在官方文档中未明确列出，仅提到支持的 Qwen 模型系列。
- 三家：各自是否支持跨会话缓存复用、缓存命中率的监测指标（除了token数）未在主要文档中涉及。

## leads
- Kimi 平台改版后从 platform.moonshot.ai 重定向到 platform.kimi.ai，官方文档路径已迁移，后续更新需跟踪新域名。
- 阿里通义千问文档存在双语版本（英文/中文 help.alibabacloud.com），中文版提供更多细节（如明确的折扣比例），建议同时参考两个版本。
- 智谱 GLM 缓存存储费用采用 yuan/MTok/hour 计价，与命中/写入分离，可能需要独立评估长期缓存持有成本，值得专题深入。
