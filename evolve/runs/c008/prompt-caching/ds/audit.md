# r3-audit：report.md 主张抽查（30 条）

判定图例：supported=笔记有 official 主张+原句；weak=仅部分/间接支撑或措辞失真；unsupported=笔记无；contradicted=与笔记相反。
笔记简称：A=r1-anthropic, CN=r1-cn, DS=r1-deepseek, G=r1-gemini, O=r1-openai, OR=r1-openrouter, CN2=r2-cn, F=r2-falsify, P=r2-platforms。

## 第 0 节（一屏看懂）

- supported | "2026-02-19 起有 automatic caching——请求顶层加一个 cache_control 字段即可，系统自动移动断点" | A C1/C2（release notes 原句 "We've launched automatic caching…Add a single cache_control field"）、F C2 | 无需改
- supported | "缓存仍非默认开启：不加字段=不缓存（官方两种启用方式都要求该字段）" | F C1（"There are two ways to enable prompt caching…"） | 可；A gaps 注明文档无"默认关闭"明文原句，措辞保留括号限定即可
- supported | "Anthropic 写 1.25×/2×、读 0.1×" | A C15（"5-minute cache write tokens are 1.25 times…1-hour…2 times…Cache read…0.1 times"） | 无需改
- supported | "Qwen 显式写 +25%、读省 90%" | CN2 C30（"首次写入缓存仅产生标准价格 25% 的额外开销，后续命中可节省 90% 成本"）、CN A5（125%/10%） | 无需改
- supported | "Kimi K3 写 5m=原价/1h=2×、读 1/10" | CN K5（未命中 ¥20、Write 5m ¥20/1h ¥40、命中 ¥2、"缓存命中价格仅为未命中价格的 1/10"） | 无需改
- supported | "OpenAI GPT-5.6+ 写 1.25×/读 0.1×；旧模型读 0.1–0.5×" | O C18/C19/C20（pricing 表 0.1×/0.25×/0.5× 实例） | 无需改
- supported | "DeepSeek 命中 1/30–1/50" | DS C8（flash $0.006/$0.30=1/50；v4-pro $0.044/$1.32=1/30） | 无需改
- supported | "Gemini explicit 另收存储费 $0.5–4.5/1M tok·hr；智谱定价页也有缓存存储列（限时免费）" | G C13（$4.50/$1.00/$0.50 档）、CN2 C14（"缓存存储当前限时免费"） | 无需改
- supported | "TTL：DeepSeek 几小时到几天；智谱、Gemini implicit 未公布" | DS C6（"usually within a few hours to a few days"）、G C12+gaps、CN2 gaps | 无需改
- supported | "OpenRouter 只做 cache_control↔prompt_cache_breakpoint 互译+粘性路由、推理无加价；另有自建 Response Caching（edge、X-OpenRouter-Cache 头族、默认 300s）" | OR C1/C3/C9、F C3/C4（"Caching operates at the OpenRouter layer…stored in edge infrastructure"） | 无需改；两功能区分正确
- supported | "阿里 Session 缓存更严——system+user prompt 字符级精确匹配" | CN2 C19/C20（"任意字符变更（包括空格和标点）都会使 cached_tokens 归零"） | 无需改

## 第 2 节（对照矩阵）

- supported | OpenAI 行："1,024 tok（5.6+；旧模型随设置变）；每请求≤4 写；lookup 最多 80 断点" | O C4/C29（"up to four breakpoints…considers up to the latest 80 breakpoints"） | 注：O conflicts 记 guide 另有 "latest 50 explicit + first 2 + 20 earlier" 口径未裁决，可加脚注
- supported | Anthropic 行："512–4,096 按模型（Opus5.5=512、Sonnet系=1024、Haiku4.5=4096）；≤4 断点；20-block lookback" | A C7/C20/C21 | 无需改（C7 所列 Sonnet 全系确为 1024）
- supported | Gemini implicit："2.5+ 默认开；Vertex 可 PATCH cacheConfig disableCache:true 项目级关闭，AI Studio 侧未见开关" | G C1、F C12（PATCH …/cacheConfig {"disableCache": true}）、F C11+gaps | 无需改；"未见"措辞准确反映 silence
- supported | Gemini implicit 门槛 "2,048–6,144（2.5 Flash/Pro=2048；3.x Flash=4096/6144）" | G C6（AI Studio：3.x Flash=4096、2.5=2048）、G C8（Vertex：部分 3.x implicit-only=6144） | 建议标 "4096（AI Studio）/6144（Vertex）" 以免混读
- supported | Gemini explicit："POST /v1beta/cachedContents、cachedContent 引用、patch 只改过期、当前页未列最小值（旧版 1024/2048）" | G C4/C11/C20/C7+gaps | 无需改
- supported | DeepSeek："Anthropic 端点 cache_control 标 Ignored；固定 token 间隔切分（数值未公布；2024 公告为 64）；无管理 API" | F C6（"cache_control — Ignored"）、DS C3/C4/C16 | 无需改
- supported | Kimi："prompt_cache_options{mode:implicit,ttl}；Anthropic 端点顶层 cache_control 控写；无对象 CRUD、不可手动清"；分类表 "旧 /v1/caching 2025 年已下线实测 404" | CN K1/K2/K4/K10、F C9（CDX 2025-12-09 已 404 + 实测 404）、F C10 | 无需改
- supported | 智谱："建议重复前缀 ≥500 tok；部分型号不支持（GLM-4-AirX、GLM-Z1 系）" | CN Z2、CN2 C14（定价页"不支持"标注=事实清单） | 无需改
- supported | Qwen："隐式不可关；显式 messages 打 cache_control；Session 缓存 x-dashscope-session-cache 头；隐式 1024（第三方 GLM/MiniMax 512）；显式≤4 仅 ephemeral" | CN A1/A2/A3/A10 | 无需改
- supported | OpenRouter："TTL 不翻译；Anthropic≤4；Gemini 只用最后一个；粘性会话 10min 无活动过期" | OR C4/C17/C19 | 无需改
- supported | Anthropic TTL/价："默认 5m、ttl:1h、命中免费刷新、长 TTL 排短 TTL 前；5m=1.25×/1h=2×；读 0.1×（Fable5.1/Mythos5.1=0.025×、Opus5.5=0.05×）" | A C11/C12/C14/C15 | 无需改
- supported | OpenAI TTL："30m 滑动（写/复用刷新）；in_memory 5–10min≤1h；非 ZDR 默认 24h（典型 30min≤24h）" | O C12/C13/C14/C15/C16 | 无需改
- supported | Gemini explicit："默认 1h 无上下限（Vertex ≥1min）；写=输入原价；读 0.1×（Vertex 2.5+ 90%、2.0 75%）；$4.50/$1.00" | G C9/C10/C14/C15、P C10 | 无需改
- supported | usage 行：OpenAI input_tokens_details/prompt_tokens_details.*；Anthropic cache_creation{5m,1h} 细分；Gemini cachedContentTokenCount 两机制同字段；DeepSeek hit/miss；Kimi/智谱/Qwen cached_tokens（Qwen Anthropic 端点 cache_read_input_tokens）；OpenRouter 归一+native_tokens_cached | O C21/C22、A C16/C17、G C17/C19、DS C11、CN K7/Z4/A6、OR C11–C13 | 无需改
- weak | Anthropic 隔离："API/AWS 平台/Foundry 到 workspace 级" | A C23（workspace 级仅限 Claude API/Claude Platform on AWS/Foundry；Bedrock 与 Google Cloud 仅 org 级） | "AWS 平台"缩写歧义——Bedrock 也在 AWS 但只有 org 级；建议写 "Claude Platform on AWS（非 Bedrock）"
- weak | OpenRouter："粘性键=账户×模型×会话（session_id/prompt_cache_key）" | OR C14/C16/C17（键实为「首条 system+首条非 system 消息哈希」，session_id 直接作键、回退 prompt_cache_key；"账户×模型"无明文） | 建议改为官方口径：默认哈希首两条消息，可传 session_id（≤256 字符）或回退 prompt_cache_key

## 第 3 节（变体与适配层）

- supported | "Bedrock Converse 用 cachePoint 块（Claude 走 InvokeModel 仍用 cache_control），Nova 默认隐式，usage=cacheReadInputTokens/cacheWriteInputTokens" | P C1/C2/C3 | 无需改
- supported | "Azure 与 OpenAI 同机制：默认自动、≥1024、GPT-5.6+ 才有 prompt_cache_breakpoint/ttl:30m、旧模型传参报 400" | P C5/C6（"Requests that include these parameters return a 400 error"） | 无需改
- supported | "Anthropic auto 占一个断点槽；legacy Bedrock 顶层 cache_control 400；max_tokens:0 预热需显式断点" | A C6/C21/C25 | 无需改
- supported | "OpenAI 两代口径：5.6+ 走 prompt_cache_options.ttl(30m)；旧模型 prompt_cache_retention(24h) spec 已 deprecated 但 ttl 仅 5.6+ 可用" | O C12/C30+conflicts | 无需改
- contradicted | "Session 缓存（响应头开启…）" | CN2 C18（"只需在请求头中添加 x-dashscope-session-cache: enable"）——是请求头不是响应头 | 改 "响应头开启"→"请求头开启"；同句其余（字符级匹配、≥1024、响应 id 7 天）有 C19/C22/C23 支撑
- supported | "OpenRouter：breakpoint 转 Anthropic/Google 补默认 5m cache_control；发向 OpenAI 时 ttl 丢弃；Bedrock 顶层字段转尾部断点" | OR C3/C4/C5 | 无需改

## 第 4 节（坑）

- supported | "前缀逐 token 相同（从第 0 token 起）；阿里显式连空的可选字段遗漏/新增都失效；Anthropic 分层失效（改 tools 全灭、tool_choice/images 只灭 messages）" | O C25、DS C12、CN2 C28（"即使该字段为空或可选"）、A C18 | 无需改
- supported | "低于门槛静默不缓存（Anthropic 两字段均为 0）" | A C8（"no error is returned"） | 无需改
- weak | "Anthropic/Qwen 显式写 1.25–2×" | A C15（Anthropic 确有 1.25×/2×）；CN A4/A5、CN2 C26/C30（Qwen 显式仅 5m 一档、写固定 +25%，无 2× 档） | 联名区间对 Qwen 失真；改 "Anthropic 写 1.25–2×、Qwen 显式写 1.25×"
- supported | "并发首请求不命中：Anthropic 等首个响应开始才可用；智谱异步生效" | A C22（"only becomes available after the first response begins"）、CN Z5（"异步生效…稍等片刻"） | 无需改
- supported | "OpenAI >15 rpm overflow routing；prompt_cache_key 兼做路由/分账/隔离；OpenRouter provider.order 关粘性→miss" | O C27/C31/C34、OR C15 | 无需改
- weak | "cached tokens 仍占上下文窗口和 TPM（OpenAI/Gemini）" | O C32（TPM 仅 OpenAI 有据）；OR C20（上下文窗口仅 Gemini 有据）；反向组合笔记无 | 改 "占上下文窗口（Gemini）、仍计 TPM（OpenAI）" 以精确归属
- weak | "Anthropic diagnostics 对象（报前缀分歧点，已 GA）" | 仅 A leads 行（"cache-diagnosis-2026-04-07 beta…2026-09 已 GA"），无 claim+原句 | 降格表述或补一手 release-notes 原句后升级

## 第 5 节（抽查）

- supported | "Kimi K2 矛盾未裁决：chat.md 称不传默认开启写入（无 per-model 限制）vs 指南 k2.6/k2.7 不支持 Cache Write" | CN2 C6/C1+conflict K1 | 无需改；成稿如实标注未裁决
- supported | "阿里 session 页内部自相矛盾（user prompt 变更归零 vs 前缀匹配改 user 不影响）未裁决" | CN2 conflict K2 | 无需改

## 汇总

- supported 38 / weak 5 / unsupported 0 / contradicted 1（共 44 行）
- contradicted：阿里 Session 缓存「响应头开启」应为「请求头」（CN2 C18）。
- weak 重点：Anthropic 隔离 "AWS 平台"缩写歧义（Bedrock 实为 org 级）；OpenRouter 粘性键写法偏离官方口径；写溢价 1.25–2× 区间误套 Qwen（仅 1.25×）；cached tokens 占上下文窗口/TPM 的厂商归属错位；Anthropic diagnostics 已 GA 仅见 leads。
- 高风险点复核：计费倍数/TTL（Anthropic 1.25–2×/0.1×、Qwen +25%/省90%、Kimi K3 1×/2×/0.1×、DeepSeek 1/30–1/50、Gemini 存储费 $0.5–4.5）全部有 official 原句；automatic caching 日期与 opt-in 表述正确；Kimi k2.x 矛盾处理得当；Vertex disableCache、OpenRouter 翻译规则与 Response Caching 区分均正确。
