# r2-bailian
question: 阿里云百炼/通义千问/Model Studio 上下文缓存有几套（隐式、显式断点、Session），各自是否改请求、断点字段、门槛、TTL、创建价/命中价/存储价、观测字段、失效条件、可用模型
checked: https://help.aliyun.com/zh/model-studio/context-cache ; https://www.alibabacloud.com/help/en/model-studio/context-cache ; https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api ; https://www.alibabacloud.com/help/en/model-studio/compatibility-with-openai-responses-api (fetched 2026-09-24)

## claims
- [C1] [implicit] 自动开启、无需配置、无法关闭 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "此为自动模式，无需额外配置，且无法关闭" | type: official
- [C2] [implicit] 机制=对 messages 公共前缀做前缀匹配，未命中则写入缓存 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "系统基于前缀匹配原则，检查缓存中是否存在请求中 messages 数组内容的公共前缀" | type: official
- [C3] [implicit] 门槛=相同前缀≥1024 Token（百炼部署）；智谱GLM、稀宇MiniMax 为 512 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "不少于 1024 Token 的相同前缀…智谱部署的GLM、稀宇科技部署的 MiniMax 模型为 512" | type: official
- [C4] [implicit] TTL=不确定，系统定期清理长期未用缓存 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "不确定，系统会定期清理长期未使用的缓存数据" | type: official
- [C5] [implicit] 命中率不保证，相同上下文也可能未命中 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "上下文缓存命中概率并非100%" | type: official
- [C6] [implicit] 创建价=标准输入价 100%，无额外费用 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "开启隐式缓存模式无需额外付费" | type: official
- [C7] [implicit] 命中价=多数百炼部署模型 cached_token 为 input_token 价的 20% | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "cached_token 单价为 input_token 单价的 **20%**" | type: official
- [C8] [implicit] 命中价例外：deepseek-v4.1-flash 10%；kimi-k3 10%；glm-5.3/5.2/5.2-fast-preview 25%；ZHIPU GLM 25%（FlashX 28.5%）；vanchin 2%–40%；qwen3.8-max/flash/2.4t-a95b 非20%；qwen3.8-omni-flash 固定价 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "deepseek-v4.1-flash：cached_token 单价为 input_token 单价的 **10%**" | type: official
- [C9] [implicit] 观测字段（OpenAI兼容/DashScope）=usage.prompt_tokens_details.cached_tokens，计入 prompt_tokens/input_tokens | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "在`usage.prompt_tokens_details.cached_tokens`可以查看命中缓存的 Token 数" | type: official
- [C10] [implicit] 观测字段（Anthropic）=usage.cache_read_input_tokens，单独报告不计入 input_tokens | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "通过 `usage.cache_read_input_tokens` 查看（该数值不计入 `usage.input_tokens`，而是单独报告）" | type: official
- [C11] [implicit] 观测例外：DashScope 视觉模型新加坡看 usage.cached_tokens | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "新加坡地域：所有模型均查看 `usage.cached_tokens`" | type: official
- [C12] [implicit] 排除：Batch（文件输入）调用无缓存折扣 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "OpenAI兼容-Batch（文件输入）方式调用无法享受缓存折扣" | type: official
- [C13] [implicit] 北京可用模型含 qwen3.8-max、qwen3.7-max、qwen3-max、qwen-max、qwen3.7-plus、qwen-plus、qwen3.8-flash、qwen-turbo、qwen3-coder-plus、qwen3.8-omni-flash、deepseek 系、kimi-k3、glm-5.3、MiniMax-M2.5、qwen-vl-max 等（按地域分） | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "千问 Max：qwen3.8-max、qwen3.8-max-0902、qwen3.7-max" | type: official
- [C14] [explicit] 需改请求：在 messages 的 content 块加 cache_control 标记 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "在 messages 中加入`\"cache_control\": {\"type\": \"ephemeral\"}`标记" | type: official
- [C15] [explicit] 断点字段=cache_control，type 仅 ephemeral；可加于 system/user/assistant/tool 消息 content | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "仅支持将 `type` 设置为 `ephemeral`，有效期为 5 分钟" | type: official
- [C16] [explicit] 单请求最多 4 个标记（超出仅最后 4 个生效）；自标记向前回溯最多 20 个 content 块 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "向前回溯最多 20 个 `content` 块，尝试命中缓存" | type: official
- [C17] [explicit] 门槛：缓存块最少 1024 Token | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "缓存块的内容最少为 1024 Token" | type: official
- [C18] [explicit] TTL=5 分钟，命中后重置 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "将该缓存块的有效期重置为5分钟" | type: official
- [C19] [explicit] 创建价=标准输入价 125%，仅对增量部分计费 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "新创建的缓存内容按标准输入单价的 125% 计费" | type: official
- [C20] [explicit] 命中价=标准输入价 10%；例外 qwen3.8-max、qwen3.8-flash、qwen3.8-2.4t-a95b 非10%（中文页名单） | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "命中缓存：按标准输入单价的 10% 计费" | type: official
- [C21] [explicit] 缓存在模型响应后才创建，须等创建请求完成再命中 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "缓存创建发生在模型响应之后" | type: official
- [C22] [explicit] 观测字段=cache_creation_input_tokens（创建）、cached_tokens（命中）；Anthropic 为 cache_read_input_tokens | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "创建缓存所用的 Token数通过`cache_creation_input_tokens` 参数查看" | type: official
- [C23] [explicit] tools 并入 system 消息参与缓存且须逐字节一致，标记加在 tools 上被忽略 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "工具定义会作为系统消息的一部分参与缓存计算。工具定义不支持独立缓存" | type: official
- [C24] [explicit] 失效：5 分钟未命中即清除；标记与缓存块间隔>20 个 content 块不命中 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "The system clears the cache block if it is not hit within its 5-minute validity period" | type: official
- [C25] [explicit]+[implicit] 缓存按账号隔离、按模型隔离 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "isolated at the account level … Cache data is isolated between models" | type: official
- [C26] [explicit]+[implicit] 两模式互斥 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "显式缓存、隐式缓存两者互斥，单个请求只能应用其中一种模式" | type: official
- [C27] [explicit] 系统追加少量内部 Token（≤10）按标准输入价计费 | src: https://www.alibabacloud.com/help/en/model-studio/context-cache | quote: "appends a small number of tokens (typically 10 or fewer)" | type: official
- [C28] [explicit] 北京可用模型：qwen3.8/3.7/3.6-max、qwen3-max、qwen3.7/3.6/3.5-plus、qwen3.8/3.7/3.6/3.5-flash、qwen3-coder、qwen3-vl、deepseek-v3.2、kimi-k2.x、glm-5.1 等（按地域分） | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "千问 Max：qwen3.8-max、qwen3.8-max-0902、qwen3.7-max…qwen3.6-max-preview、qwen3-max" | type: official
- [C29] [session] Responses API 的 Session 缓存经请求头开启，默认 disable | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "在请求 Header 中添加 `x-dashscope-session-cache: enable` 开启" | type: official
- [C30] [session] 无独立计费：模型支持显式则按显式规则，否则按隐式规则 | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "模型支持显式缓存：使用显式缓存，计费和相关约束参照显式缓存" | type: official
- [C31] [session] 门槛=累计上下文超 1024 Token 触发创建；配合 previous_response_id 串联 | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "后续累积对话上下文超过1024 Token时将触发缓存创建" | type: official
- [C32] [session] 观测字段=usage.input_tokens_details.cached_tokens | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "usage.input_tokens_details.cached_tokens" | type: official
- [C33] [session] previous_response_id 串联上下文，响应 id 有效期 7 天 | src: https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api | quote: "当前响应`id`有效期为7天" | type: official

- [C34] [explicit]+[implicit] PTU 部署也支持，命中按折扣系数折算额度 | src: https://help.aliyun.com/zh/model-studio/context-cache | quote: "预置吞吐（PTU）部署同样支持上下文缓存" | type: official

## conflicts
- 隐式门槛：英文页只写 "For Zhipu-deployed GLM models, the minimum is 512"；中文页另含稀宇 MiniMax 512。
- 显式命中价例外：英文页名单含 qwen3.8-max-0902，中文页例外名单（qwen3.8-max、qwen3.8-flash、qwen3.8-2.4t-a95b）无它。
- 隐式模型清单：中文北京列表比英文多 MiniMax/MiMo/Stepfun/vanchin/智谱GLM/月之暗面Kimi 等来源。

## gaps
- 存储价（按小时/容量收费）：两页均未提及，大概率无此项但未明示。
- Session 缓存自身 TTL 未写明（仅 response id 7 天有效期可作上限）。
- 页面无可见更新日期，日期按抓取日 2026-09-24。
- qwen3.8 系等非标折扣具体价须查百炼控制台，文档未给数值。

## leads
- 显式缓存最佳实践：https://help.aliyun.com/zh/model-studio/explicit-cache-guide （搜索所见，未打开）
- 模型价格页：https://help.aliyun.com/zh/model-studio/model-pricing （qwen3.8 系例外价、omni-flash 固定命中价）
