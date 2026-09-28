# r1-cn3
question: 三家国内大模型 API 的上下文/prompt caching：Kimi、智谱 GLM、通义千问（D1–D7）
checked: https://platform.kimi.com/docs/guide/context-caching.md, https://platform.kimi.com/docs/pricing/chat.md, https://platform.kimi.com/docs/llms.txt, https://docs.bigmodel.cn/cn/guide/capabilities/cache (raw HTML grep), https://help.aliyun.com/zh/model-studio/context-cache (WebFetch + raw HTML grep), https://help.aliyun.com/zh/model-studio/explicit-cache-guide, https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses (snippet), https://github.com/Elarwei001/research_openclaw/blob/main/proposals/kimi-context-cache.md, https://aichina.news/news/moonshot-ai-debuts-context-caching-public-beta-slashing-llm-costs-by-p0i8hs/

## Kimi (platform.kimi.com；platform.moonshot.cn 已 301 至 kimi.com)

- [C1] D1 隐式自动前缀缓存；可选请求字段 `prompt_cache_options`（Chat/Responses），Anthropic Messages 格式用顶层 `cache_control` | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "`prompt_cache_options.mode` 当前仅支持 `implicit`，`ttl` 支持 `5m` 和 `1h`。" | type: official
- [C2] 默认行为 | src: 同上 | quote: "不传 `prompt_cache_options` 时，系统默认使用 `5m` TTL：满足命中条件的前缀会自动写入并尝试复用" | type: official
- [C3] D2 粒度：按块存储+最长匹配前缀，官方未给最小 token 数 | src: 同上 | quote: "缓存按块存储，不足一整块的部分无法写入缓存，会计为缓存未命中"；"前缀指请求 messages 中从开头连续的 token 序列；缓存按最长匹配前缀计算，匹配成功即为命中。" | type: official
- [C4] D3 kimi-k3 计费（每 1M tokens）：缓存写入 5min 档 ¥20、1h 档 ¥40（一次性）；命中输入 ¥2，未命中输入 ¥20 | src: https://platform.kimi.com/docs/pricing/chat.md | quote: "缓存写入 是指将请求前缀写入上下文缓存所产生的费用。" | type: official
- [C5] K2 系列只有命中/未命中两档价（无写入列）：kimi-k2.7-code 命中 ¥1.30/未命中 ¥6.50；kimi-k2.6 命中 ¥1.10/未命中 ¥6.50（每 1M） | src: 同上 | quote: "在有效期内命中缓存的输入仅按"输入价格（缓存命中）"计费，命中后缓存有效期自动续期，不再收取缓存写入费用。" | type: official
- [C6] D4 TTL：5min 或 1h 两档，命中自动按原档续期、不另收费；TTL 写入时锁定；无手动清除 | src: https://platform.kimi.com/docs/guide/context-caching.md | quote: "缓存条目的 TTL 在首次写入时锁定，不能改写"；"缓存不支持手动清除；缓存前缀无活动超过所选 TTL 后自动过期。" | type: official
- [C7] D5 命中字段：Chat `usage.prompt_tokens_details.cached_tokens`；Responses `usage.input_tokens_details.cached_tokens`；Messages(Anthropic) `usage.cache_read_input_tokens` | src: 同上 | type: official
- [C8] D6 失效：前缀任一处变化则其后不可复用；按 org 隔离 | src: 同上 | quote: "前缀中任何一处发生变化，该位置之后的内容都无法复用"；"缓存按组织（org）隔离：同一组织内共享，组织之间不共享" | type: official
- [C9] D7：kimi-k3 支持 Cache Write；kimi-k2.7/k2.7-highspeed/k2.6 不支持 Cache Write（但价格表仍列命中价，见 conflicts） | src: 同上 | quote: "`kimi-k3` 支持 Cache Write；`kimi-k2.7`、`kimi-k2.7-highspeed`、`kimi-k2.6` 不支持。" | type: official
- [C10] 历史显式 Context Cache：`POST https://api.moonshot.cn/v1/caching` 创建缓存对象（`object:"context_cache_object"`，字段 id/status/tokens/expired_at，参数 model/messages/tools/name/ttl），调用时以 `role:"cache"` 消息传 `cache_id=...;reset_ttl=...`；仅 moonshot-v1 系列可用，kimi-k2 报 "model family is invalid"。现行官方文档索引(llms.txt)已无该端点 | src: https://github.com/Elarwei001/research_openclaw/blob/main/proposals/kimi-context-cache.md ; https://aichina.news/news/moonshot-ai-debuts-context-caching-public-beta-slashing-llm-costs-by-p0i8hs/ | quote: "res = requests.post(url = \"https://api.moonshot.cn/v1/caching\" ... \"ttl\": 3600" | type: secondary

## 智谱 GLM (docs.bigmodel.cn)

- [C11] D1 隐式自动缓存，无手动开关字段 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "自动缓存识别：隐式缓存，智能识别重复的上下文内容，无需手动配置" | type: official
- [C12] D2 建议阈值 500 Token（非硬性最小值） | src: 同上 | quote: "要触发上下文缓存，重复的前缀内容必须足够长（建议 500 Token 以上），两三句话的短系统提示词通常无法命中。" | type: official
- [C13] D3 命中按优惠价、通常为标准价 50%；仅限标准 API 计费 | src: 同上 | quote: "缓存命中 Token：按优惠价格计费（通常为标准价格的 50%）"；"仅适用于标准 API 计费，不包括资源包和 GLM Coding Plan 套餐。" | type: official
- [C14] D5 命中字段 | src: 同上 | quote: "详细显示缓存命中的 Token 数量，响应字段 `usage.prompt_tokens_details.cached_tokens`" | type: official
- [C15] D6 前缀复用："重复的长前缀会被自动缓存"；"把稳定不变的说明、规范与知识库放在系统提示词前部…最大化上下文缓存的命中率" | src: 同上 | type: official
- [C16] D4 TTL ∅、D7 模型清单 ∅：已下载原始 HTML 全文 grep，"TTL/有效期/过期/失效/分钟" 0 命中；无支持模型列表（GLM-5.2/GLM-4.5 字样仅出现在示例知识库虚构文本内）；唯一相关表述为"缓存为异步生效，首次请求后稍等片刻再发起后续请求效果更好" | src: 同上 | type: official

## 通义千问 / 阿里云百炼 (help.aliyun.com/zh/model-studio/context-cache)

- [C17] D1 两种模式互斥：显式缓存 = 在 message 上加 `"cache_control": {"type": "ephemeral"}`（content 须为数组形式，最多 4 个标记）；隐式缓存 = 自动公共前缀缓存，"无需额外配置，且无法关闭"。含 cache_control 则走显式，否则自动走隐式 | src: https://help.aliyun.com/zh/model-studio/context-cache ; https://help.aliyun.com/zh/model-studio/explicit-cache-guide | quote: "同一请求只能使用一种缓存模式。若请求中包含 `cache_control` 标记则使用显式缓存，否则系统自动使用隐式缓存。" | type: official
- [C18] D2 最小 1024 Token（两种模式相同）；例外："智谱部署的GLM、稀宇科技部署的 MiniMax 模型为 512" | src: context-cache 页 | quote: "当请求之间存在不少于 1024 Token 的相同前缀时，该公共前缀具备隐式缓存写入和命中的技术条件。" | type: official
- [C19] D3 显式：创建按标准输入价 125% 计费（新增部分计费），命中按 10% 计费 | src: context-cache 页 + explicit-cache-guide | quote: "用于创建缓存 Token 计费 通常为输入 Token 单价的 125%"；"命中缓存的 Token 仅按标准输入价格的 10% 计费。" | type: official
- [C20] D3 隐式：写入不另收费（输入价 100%），命中按输入价 20%（例外：deepseek-v4.1-flash 10%、kimi-k3 10%、部分 GLM 25%、qwen3.8-omni-flash 固定单价等，以页面列表为准） | src: context-cache 页 | quote: "cached_token 单价为 input_token 单价的 20%" | type: official
- [C21] D4 显式 TTL 5 分钟、"每次命中都会将该缓存块的有效期重置为5分钟"；隐式 "不确定，系统会定期清理长期未使用的缓存数据" | src: 同上 | type: official
- [C22] D5 命中字段：OpenAI 兼容/DashScope `usage.prompt_tokens_details.cached_tokens`（新加坡地域全部模型用 `usage.cached_tokens`，文档称将迁移）；Anthropic 兼容 `usage.cache_read_input_tokens`（不计入 input_tokens）；显式另有 `usage.prompt_tokens_details.cache_creation_input_tokens` | src: 同上 | type: official
- [C23] D6 显式"选取最长的匹配前缀作为命中的缓存块"；Tools 定义参与缓存计算，改变则不命中；隐式命中不保证 100%（"即使请求上下文完全一致，仍可能未命中"），例：已缓存 ABCD，请求 ABE 可命中 AB、请求 BCD 不命中 | src: 同上 | type: official
- [C24] D7 隐式缓存按地域列模型清单（北京）：qwen Max/Plus/Flash/Turbo/Coder/开源系列、qwen3-vl-plus/flash、qwen-vl-max/plus，及百炼部署的第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）等；显式缓存模型列表"请参见上下文缓存"页；示例用 qwen3.7-max；Qwen3.5 起仅支持消息级截断点，之前支持 content 级 | src: 同上 | type: official

## conflicts
- Kimi：指南称 k2.7/k2.6「不支持 Cache Write」，但价格表仍列这些模型的「缓存命中」价（k2.7-code ¥1.30/1M）。解读：K2 系自动缓存命中享折扣但不收写入费/不能选 TTL；两页未直接矛盾但表述易混淆。
- 智谱 D7：搜索引擎快照曾显示「支持所有主流模型，包括 GLM-5.2、GLM-5.1、GLM-5 系列等」，但当前页面原始 HTML 中不存在该句（grep 0 命中），按 ∅ 处理。

## gaps
- Kimi：缓存块大小/最小 token 数官方未公布（二手观察 K2 命中常为 1024 倍数）。
- 智谱：TTL/有效期、失效规则、支持模型清单、是否有显式开关——官方页均未写。
- 阿里云：显式缓存各模型/各地域完整支持清单（文档仅指回 context-cache 页）；DashScope 原生 API 是否支持 cache_control 标记未演示（仅 OpenAI/Anthropic 兼容端点）。
- Kimi 历史 /v1/caching 现状：现行 kimi.com 文档索引已无该端点，仅二手资料（moonshot-v1 专用）。

## leads
- 阿里云 Session 缓存：Responses API 请求头 `x-dashscope-session-cache: enable`，最小 1024 Token、精确匹配，`usage.input_tokens_details.cached_tokens`（help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses）。
- 阿里云 PTU 预置吞吐命中缓存按折扣系数折算额度（ptu-long-input-and-cache 页）。
- Kimi 批量推理另有「缓存命中 token 价格」（platform.kimi.com/docs/pricing/batch.md）。
- 火山豆包/百度缓存能力未查（超出本轮范围）。
