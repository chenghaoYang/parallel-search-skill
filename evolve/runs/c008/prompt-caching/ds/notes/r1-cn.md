# r1-cn
question: 国内三家厂商的 prompt/context caching 机制：Kimi（Moonshot）、智谱 GLM（bigmodel.cn）、通义千问（阿里 DashScope/百炼）——机制/门槛/TTL/计费/usage 字段/匹配规则/管理 API/隔离
checked: https://platform.kimi.com/docs/guide/context-caching.md, https://platform.kimi.com/docs/pricing/chat.md, https://platform.kimi.com/docs/llms.txt, https://platform.kimi.com/docs/openapi.json, https://platform.kimi.com/docs/api/caching, https://help.aliyun.com/zh/model-studio/context-cache, https://help.aliyun.com/zh/model-studio/explicit-cache-best-practice, https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses, https://docs.bigmodel.cn/cn/guide/capabilities/cache

## claims

### Kimi / Moonshot（platform.kimi.com，platform.moonshot.cn 已 301 至此）
- [K1] 当前缓存为隐式模式：请求级参数 `prompt_cache_options` 仅含 `mode` 与 `ttl` 两字段 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "`prompt_cache_options.mode` 当前仅支持 `implicit`，`ttl` 支持 `5m` 和 `1h`" | type: official
- [K2] Anthropic 端点用顶层 `cache_control` 控制写入；省略时只读 5m 缓存不写入 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "`cache_control` 只在请求顶层生效，消息体内的同名标记会被忽略" | type: official
- [K3] 仅 kimi-k3 支持 Cache Write；kimi-k2.7、kimi-k2.7-highspeed、kimi-k2.6 不支持写入 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "`kimi-k2.7`、`kimi-k2.7-highspeed`、`kimi-k2.6` 不支持" | type: official
- [K4] TTL 两档 5m/1h，默认 5m；命中免费续期；无手动清除 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "缓存不支持手动清除；缓存前缀无活动超过所选 TTL 后自动过期" | type: official
- [K5] kimi-k3 计费（每 1M tokens）：未命中输入 ¥20，Cache Write 5m ¥20 / 1h ¥40，命中 ¥2 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "缓存命中价格仅为未命中价格的 1/10" | type: official
- [K6] 定价页列出 k2.x 命中价但无写入价：kimi-k2.7-code 命中 ¥1.30、k2.7-code-highspeed ¥2.60、k2.6 ¥1.10（未命中 ¥6.5/¥13/¥6.5） | src: https://platform.kimi.com/docs/pricing/chat.md | quote: "命中缓存的输入仅按'输入价格（缓存命中）'计费，命中后缓存有效期自动续期，不再收取缓存写入费用" | type: official
- [K7] usage 字段：Chat 用 `usage.prompt_tokens_details.cached_tokens`（写入为 `cache_write_tokens`）；Responses 用 `input_tokens_details.cached_tokens`；Messages 用 `cache_read_input_tokens`/`cache_creation_input_tokens` | src: https://platform.kimi.com/docs/openapi.json | quote: "cached_tokens、cache_write_tokens 与未缓存部分互斥，三者之和等于 prompt_tokens" | type: official
- [K8] 匹配为从 messages 开头的最长前缀匹配；按块存储，不足一整块不可写 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "缓存按块存储，不足一整块的部分无法写入缓存，会计为缓存未命中" | type: official
- [K9] 缓存按组织隔离且组织内共享 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "缓存按组织（org）隔离：同一组织内共享，组织之间不共享" | type: official
- [K10] 无 /v1/caching 类管理端点：OpenAPI spec 全部 paths 仅 chat/completions、responses、anthropic/v1/messages、files、batches、models、tokenizers、tools、balance 等 15 条，无缓存对象 CRUD；旧 URL /docs/api/caching 现渲染为快速开始页 | src: https://platform.kimi.com/docs/openapi.json | quote: "/v1/chat/completions, /v1/responses, /anthropic/v1/messages, /v1/files ...（无 caching 路径）" | type: official

### 智谱 GLM（docs.bigmodel.cn）
- [Z1] 隐式自动缓存，无需配置 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [Z2] 门槛为建议值：重复前缀建议 500 Token 以上 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "要触发上下文缓存，重复的前缀内容必须足够长（建议 500 Token 以上），两三句话的短系统提示词通常无法命中" | type: official
- [Z3] 命中按优惠价计费，通常为标准价 50%；仅限标准 API 计费 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "缓存命中 Token：按优惠价格计费（通常为标准价格的 50%）"；"仅适用于 标准 API 计费，不包括资源包和 GLM Coding Plan 套餐" | type: official
- [Z4] usage 字段 `usage.prompt_tokens_details.cached_tokens`，示例 `"cached_tokens": 1024` | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "响应字段 usage.prompt_tokens_details.cached_tokens" | type: official
- [Z5] 前缀式自动缓存，异步生效 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "重复的长前缀会被自动缓存，命中的 Token 按优惠价格计费；缓存为异步生效，首次请求后稍等片刻再发起后续请求效果更好" | type: official

### 通义千问 / 百炼（help.aliyun.com）
- [A1] 双模式：隐式自动且不可关 + 显式 cache_control 标记 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "此为自动模式，无需额外配置，且无法关闭"；"在 messages 中加入`\"cache_control\": {\"type\": \"ephemeral\"}`标记" | type: official
- [A2] 最小可缓存 1024 Token；隐式模式下百炼外部部署的 GLM/MiniMax 为 512 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "当请求之间存在不少于 1024 Token 的相同前缀时，该公共前缀具备隐式缓存写入和命中的技术条件。智谱部署的GLM、稀宇科技部署的 MiniMax 模型为 512" | type: official
- [A3] 显式缓存单次请求最多 4 个标记，仅支持 ephemeral | src: https://help.aliyun.com/zh/model-studio/explicit-cache-best-practice | quote: "单次请求最多支持 4 个缓存标记" | type: official
- [A4] 显式 TTL 5 分钟、命中续期；隐式 TTL 不确定 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "5分钟（命中后重置）"；"不确定，系统会定期清理长期未使用的缓存数据" | type: official
- [A5] 计费：隐式命中=输入单价 20%（deepseek-v4.1-flash 为 10%）；显式创建=125%、命中=10% | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "对命中缓存的部分，通常按输入 Token 标准单价的 20% 计费"；"用于创建缓存的 Token 通常按输入 Token 标准单价的 125% 计费，后续命中通常仅需支付 10% 的费用" | type: official
- [A6] usage 字段：OpenAI/DashScope 为 `usage.prompt_tokens_details.cached_tokens`（新加坡部分模型用 `usage.cached_tokens`）；Anthropic 为 `usage.cache_read_input_tokens`（不计入 input_tokens）；显式创建量为 `cache_creation_input_tokens` | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "命中缓存的 Token 数通过`usage.cache_read_input_tokens`查看（该数值不计入`usage.input_tokens`，而是单独报告）" | type: official
- [A7] 显式匹配：从后向前检查最近 20 个 content 块，取最长匹配前缀；tools 定义计入 system 前缀 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "缓存采用从后向前的前缀匹配策略，系统会自动检查最近的 20 个 content 块" | type: official
- [A8] 支持模型（显式，北京地域示例）：qwen3.8-max、qwen3.7-max/plus/flash、qwen3.6-plus/flash、qwen3.5-plus/flash、qwen3-coder-plus/flash、qwen3-vl-plus/flash、qwen-plus-character、deepseek-v3.2、kimi-k2.5/k2.6/k2.7-code、glm-5.1；隐式范围更广（含 qwen-turbo、qwen-max、第三方部署 GLM/MiniMax/MiMo/Stepfun 等），按地域分表 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "千问 Max：qwen3.8-max、qwen3.8-max-0902、qwen3.7-max…Kimi：kimi-k2.6、kimi-k2.5、kimi-k2.7-code；GLM：glm-5.1" | type: official
- [A9] 隔离：账号级隔离 + 模型间隔离 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "无论是隐式缓存还是显式缓存，数据都在账号级别隔离，不会共享"；"缓存数据存在模型间隔离，不会共享" | type: official
- [A10] Responses API 另有第三种 Session 缓存，靠请求头开启 | src: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses | quote: "只需在请求头中添加`x-dashscope-session-cache: enable`（默认值为 disable），服务端即可自动缓存对话上下文" | type: official

## conflicts
- Kimi：指南称 kimi-k2.6/k2.7 "不支持" Cache Write，但定价页为这些模型列了"缓存命中"价格（k2.6 ¥1.10/1M 等）——可能意味着它们只读命中而不能控制写入，两页未解释清楚，未裁决。
- 智谱：WebSearch 摘录曾出现"支持所有主流模型，包括 GLM-5.2、GLM-5.1、GLM-5 系列等"，但对页面全量 HTML grep 未见"兼容"字样及该句——以页面正文为准：无官方支持模型清单（示例均用 glm-5.3）。

## gaps
- Kimi：缓存"块"大小/最小可缓存 token 数的具体数字未公开；k2.x 命中缓存的触发机制不明（见 conflicts）。
- 智谱：TTL/存活时长、缓存隔离范围、官方支持模型清单均未在文档页说明（已 grep 全量 HTML 确认无 TTL/过期/隔离/兼容 字样）。
- 阿里：隐式缓存的具体清理周期未量化（只说"定期清理"）；context-cache 页"更新时间"字段为空。

## leads
- 旧版 platform.moonshot.cn 曾有的显式 Context Cache API（/v1/caching）疑似随平台迁移下线：旧文档 URL 301 到 platform.kimi.com 且页面变成快速开始；如需历史证据可查 web.archive.org。
- 阿里 Session 缓存（x-dashscope-session-cache）是与隐式/显式并列的第三种模式，精确匹配非前缀匹配，详见 qwen-api-via-openai-responses 页"缓存命中规则"。
- 智谱 GLM Coding Plan 端点的缓存/计费规则可能不同（cache 页明确排除该套餐）。
