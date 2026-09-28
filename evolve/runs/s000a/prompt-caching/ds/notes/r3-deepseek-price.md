# r3-deepseek-price
question: DeepSeek 现行定价页上 deepseek-flash 与 deepseek-v4-pro 的缓存命中/未命中价（美元和人民币、闲时/峰时）是多少？现行 kv cache 指南是否还写「64 tokens 为一个存储单元」？
checked: https://api-docs.deepseek.com/quick_start/pricing ; https://api-docs.deepseek.com/zh-cn/quick_start/pricing ; https://api-docs.deepseek.com/guides/kv_cache ; https://api-docs.deepseek.com/zh-cn/guides/kv_cache

## claims
- [C1] 美元定价页列出两个模型：deepseek-flash（版本 DeepSeek-V4.1-Flash）与 deepseek-v4-pro（版本 DeepSeek-V4-Pro-0813），上下文 1M，最大输出 384K | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "MODEL VERSION DeepSeek-V4.1-Flash DeepSeek-V4-Pro-0813 ... CONTEXT LENGTH 1M ... MAX OUTPUT MAXIMUM: 384K" | type: official
- [C2] 美元价（每 1M tokens）：缓存命中 — flash 闲时 $0.003、峰时 $0.006；v4-pro 闲时 $0.022、峰时 $0.044（表格列序 flash 在前、v4-pro 在后）| src: https://api-docs.deepseek.com/quick_start/pricing | quote: "1M INPUT TOKENS (CACHE HIT) OFF-PEAK $0.003 $0.022 PEAK $0.006 $0.044" | type: official
- [C3] 美元价：缓存未命中 — flash 闲时 $0.15、峰时 $0.3；v4-pro 闲时 $0.66、峰时 $1.32 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "1M INPUT TOKENS (CACHE MISS) OFF-PEAK $0.15 $0.66 PEAK $0.3 $1.32" | type: official
- [C4] 美元价输出（参照）：flash 闲时 $0.6 / 峰时 $1.2；v4-pro 闲时 $1.98 / 峰时 $3.96 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "1M OUTPUT TOKENS OFF-PEAK $0.6 $1.98 PEAK $1.2 $3.96" | type: official
- [C5] 美元页峰时定义：闲时价为峰时一半；峰时为 UTC 周一至周五 01:00-04:00 与 06:00-10:00，不含中国法定节假日 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "Off-peak rates are half of the peak rates. Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays." | type: official
- [C6] 人民币价（每百万 tokens）：缓存命中 — flash 闲时 0.02元、高峰 0.04元；v4-pro 闲时 0.15元、高峰 0.30元 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "百万tokens输入（缓存命中）空闲时段 0.02元 0.15元 高峰时段 0.04元 0.30元" | type: official
- [C7] 人民币价：缓存未命中 — flash 闲时 1元、高峰 2元；v4-pro 闲时 4.5元、高峰 9.0元 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "百万tokens输入（缓存未命中）空闲时段 1元 4.5元 高峰时段 2元 9.0元" | type: official
- [C8] 人民币价输出（参照）：flash 闲时 4元 / 高峰 8元；v4-pro 闲时 13.5元 / 高峰 27.0元 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "百万tokens输出 空闲时段 4元 13.5元 高峰时段 8元 27.0元" | type: official
- [C9] 中文页峰时定义：北京时间周一至周五（不含法定节假日）9:00-12:00、14:00-18:00 为高峰 | src: https://api-docs.deepseek.com/zh-cn/quick_start/pricing | quote: "空闲时段价格为高峰时段价格的一半。北京时间周一至周五（不含中国法定节假日）9:00 - 12:00、14:00 - 18:00 为高峰时段" | type: official
- [C10] 并发限制：flash 2500，v4-pro 500 | src: https://api-docs.deepseek.com/quick_start/pricing | quote: "Concurrency Limit(3) 2500 500**" | type: official
- [C11] 现行 kv cache 指南（英文）不再提固定 64-token 存储单元；命中判定改为「缓存前缀单元」完整匹配 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Each cached prefix is an independent, complete unit. A subsequent request can only hit the cache if it fully matches a cache prefix unit." | type: official
- [C12] 英文指南对长输入/长输出只说「按固定 token 间隔」切分前缀单元，未给具体数字 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "For long inputs or long outputs, the system will carve out cache prefix units at fixed token intervals" | type: official
- [C13] 中文指南同样只说「以一定的 token 数量为间隔」截取缓存前缀单元，全页无「64」 | src: https://api-docs.deepseek.com/zh-cn/guides/kv_cache | quote: "在长输入或长输出中，系统会以一定的 token 数量为间隔，截取缓存前缀单元" | type: official
- [C14] 落盘时机三条：请求结束位置（用户输入结束 + 模型输出结束各产生一个单元）、公共前缀检测、固定 token 间隔 | src: https://api-docs.deepseek.com/guides/kv_cache | quote: "Each request will produce two cache prefix units at the end position of the user input and the end position of the model output." | type: official

## conflicts
- 无。中英文页价格分别为美元/人民币两套币种，峰时时段表述（UTC 01:00-04:00、06:00-10:00 vs 北京 9:00-12:00、14:00-18:00）互为同一时段的不同时区写法，不构成冲突。

## gaps
- 指南页未出现 64：英文 https://api-docs.deepseek.com/guides/kv_cache 与中文 https://api-docs.deepseek.com/zh-cn/guides/kv_cache 整页均无 "64"；现行门槛句只有 "fully matches a cache prefix unit" 与 "fixed token intervals"/"一定的 token 数量"，未给出任何具体 token 数。「64 tokens 为一个存储单元」的说法仅存在于旧新闻页（news0802），本轮未重开该页。
- 上一轮主张的 v4-pro 人民币价（命中 0.15/0.30 元、未命中 4.5/9.0 元）本轮已证实（C6/C7）；美元与人民币汇率换算关系页未说明，无法判定是否固定汇率。

## leads
- 旧说法「64 tokens 为一个存储单元」出处：https://api-docs.deepseek.com/news/news0802 （超出本轮范围，未重开）。
- 旧模型名 deepseek-v4-flash / deepseek-v4-flash-vision-exp 仍被接受但按 Flash 价计费（定价页脚注 1）。
