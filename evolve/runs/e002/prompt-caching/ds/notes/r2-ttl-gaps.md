# r2-ttl-gaps
question: 三个独立缺口核查：(1) 阿里云百炼隐式缓存 TTL 具体数字；(2) 智谱 GLM 上下文缓存 TTL 数值；(3) Gemini implicit caching 折扣百分比
checked: https://help.aliyun.com/zh/model-studio/context-cache, https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://ai.google.dev/gemini-api/docs/caching, https://ai.google.dev/gemini-api/docs/pricing

## claims
- [C1] 阿里云百炼隐式缓存无固定 TTL 数字，系统根据使用频率动态清理 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "由系统自动管理，无固定有效期，系统会定期清理长期未使用的缓存数据。" | type: official
- [C2] Gemini implicit caching 在官方定价文档中无具体折扣百分比，pricing 页仅列 batch API 的 50% 折扣 | src: https://ai.google.dev/gemini-api/docs/pricing | quote: "Batch API (50% cost reduction)" | type: official
- [C3] Gemini caching 页确认 implicit caching 存在但未给折扣数字，仅说"We automatically pass on cost savings if your request hits caches" | src: https://ai.google.dev/gemini-api/docs/caching | quote: "We automatically pass on cost savings if your request hits caches" | type: official

## conflicts
无

## gaps
- 智谱 GLM 上下文缓存 TTL：已查 https://docs.bigmodel.cn/cn/guide/capabilities/cache，文档未提及具体过期时间或分钟/小时数值。只提到"缓存为异步生效"但无 TTL 数字。

## leads
- Gemini pricing 表格中 context caching 价格（$0.075/1M tokens）与 implicit caching 关系需澄清，当前文档未明确区分
