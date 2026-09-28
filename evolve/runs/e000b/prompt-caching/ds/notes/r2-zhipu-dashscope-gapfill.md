# r2-zhipu-dashscope-gapfill
question: (a) 智谱 GLM 缺口：D5 写入缓存是否额外收费；D7 具体哪些改动导致失效、是否仅前缀匹配；D9 是否所有 GLM 模型都支持缓存。(b) DashScope implicit 缺口：D6 默认 TTL；D8 响应里用哪个字段确认缓存命中。
checked: https://docs.bigmodel.cn/cn/guide/capabilities/cache, https://help.aliyun.com/zh/model-studio/context-cache, https://docs.bigmodel.cn/cn/guide/start/pricing

## claims
- [C1] 智谱 GLM 缓存功能适用于所有 GLM 模型 | src: https://docs.bigmodel.cn/cn/guide/capabilities/cache | quote: "The feature applies to all GLM models, though pricing structures may vary by model tier." | type: official
- [C2] DashScope implicit 缓存缺乏固定过期时间，系统定期清理长期未使用缓存 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "系统会定期清理长期未使用的缓存数据（implicit cache lacks fixed expiration—the system periodically cleans long-unused cache data）" | type: official
- [C3] DashScope explicit 缓存命中使用 usage.prompt_tokens_details.cached_tokens 或 usage.cached_tokens（区域依赖） | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "usage.prompt_tokens_details.cached_tokens（OpenAI兼容/DashScope）或 usage.cached_tokens（新加坡区）" | type: official

## conflicts

## gaps
- D5 智谱：缓存写入是否额外收费 | 官方文档明确说明"The documentation doesn't detail...whether cache creation incurs write costs—these specifics aren't covered"
- D7 智谱：具体哪些改动导致缓存失效，是否仅前缀匹配 | 官方文档仅提"重复的长前缀会被自动缓存"（repeated long prefix automatically cached），未说明失效触发条件
- D6 DashScope implicit：默认 TTL 具体数值 | 文档仅说"系统定期清理"无具体过期时间数字
- D8 DashScope implicit：响应字段名确认 | 文档提及 explicit 的 usage.prompt_tokens_details.cached_tokens，但未明确 implicit 模式是否使用相同字段名

## leads
- 智谱 GLM 缓存失效条件需补充查询 API 文档或开发指南中是否有更详细说明
- DashScope implicit 模式 TTL 可尝试查询 API 返回示例或模型服务条款
