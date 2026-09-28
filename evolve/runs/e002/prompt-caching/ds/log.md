# Log

## R0
观察：任务给定 4 家核心 + 3 家国内 + 1 个网关 = 8 实体，用户点名 4 条疑点（自动/手动、计费、TTL、以及隐含的「现在还是这样吗」时效性）。
决策：taxonomy v0 = 8 实体 × 10 维度（D1–D10，见 grid.md），分类轴 A（自动/手动）B（内存/磁盘）。
R1 按来源边界拆 6 个工人（workers 上限 6），四大核心各一个，国内三家 + OpenRouter 合并进 2 个工人。
预计 spawn：6

## R1
观察：6/6 工人返回，92 条主张（official 90/secondary 2），4 冲突，24 缺口。最重要的发现：
(a) Anthropic 笔记称官方新增「自动缓存」（顶层加一个 cache_control 字段即可，系统自动移动断点），这与用户「Anthropic 必须手动打断点」的假设相反，属于反常识主张，需 R2 复核；
(b) OpenAI 的写入端（cache write）也有 1.25x 溢价，且 D9 缺 Chat Completions 是否支持；
(c) Gemini explicit/implicit 在计费与 TTL 上有 3 处「Gemini API 官方沉默、仅 Vertex AI 二手给数字」的缺口；
(d) 触发是否自动 与 写入是否溢价 是两条独立的轴——DeepSeek/Gemini implicit/Qwen 隐式「零改动+零溢价」，OpenAI/Anthropic/Kimi/Qwen 显式「触发方式不同但写入普遍溢价」，打破「自动=免费，手动=收费」的简单二元想象。
决策：taxonomy v0→v1：分类轴 B 由「内存/磁盘」（∅ 太多，解释力弱）换成「写入/未命中是否有溢价」（能解释计费差异，且是这次调研最大的意外发现）。
R2 派 4 个针对性工人（少于 R1 的 6，只打缺口/复核冲突，不再普查）：r2-verify-anthropic（复核反常识主张）、r2-openai-gaps（Chat Completions + 写入溢价是否仅限显式模式）、r2-ttl-gaps（DashScope/智谱 TTL 数字、Gemini API 官方 implicit 折扣数字）、r2-openrouter-kimi（OpenRouter 官方来源核实不加价、Kimi 存储介质/断点上限）。
预计 spawn：4

收束结果：report.r1.md = 7043 字符（budget 9000，余量~2000）；grid 87% resolved（✅67 ⚠6 ⚔3 ❓2 ∅7）。已镜像到 ./report.md。

## R2
观察：4/4 工人返回，18 条主张全 official，2 冲突，8 缺口。核心结果：Anthropic 自动缓存反常识主张复核通过（真实、2026-02-19上线、非零改动，双源确认）；OpenAI Chat Completions 缺口填上（支持，经prompt_cache_options）且发现指南页与API reference覆盖面不一致；3 处 TTL/折扣「缺口」二次核实后确认是官方真沉默而非漏查；OpenRouter 从"仅二手"升级为"官方给倍率表但不给不加价承诺，部分倍率比直连贵"——这是本轮最大的意外发现，改写了 OpenRouter 那一行的结论方向。
决策：重写 report.md（非追加），纳入以上更新，删除已解决的"未决"条目、新增 OpenRouter 加价疑点。核心矩阵格子已 ✅/∅，用户 4 条点名疑点均有官方一手结论，唯一的反常识主张（Anthropic）已完成反证式复核。按停止条件（核心格子解决+边界主张已反证），跳过 R3，直接进入终审，不再新开扩展轮。
预计 spawn：1（终审审稿工人）

收束结果：report.r2.md = 7795 字符（budget 9000，余量~1200）；已镜像到 ./report.md。

## 终审
观察：审稿工人抽查 44 条具体主张，42 supported / 2 weak / 0 unsupported / 0 contradicted。两条 weak 都是「单个笔记里没有把两份官方数字放在一起比较的那句话」，不是事实错误：(a) OpenRouter 倍率表 vs OpenAI 直连价的比较，(b) 通义千问≠原厂API 的推断。
决策：不重新调研，直接改写这两处措辞，明确标出"本报告对比两份官方数字得出"，并为通义千问那条补上支撑证据（DashScope 与 DeepSeek/Kimi 自家文档给出的参数数值不一致，本身就是两者不是同一套系统的证据）。其余 42 条 supported 不改。
结果：report.md = 7959 字符（budget 9000，余量~1000）。已镜像到 ./report.md。审计文件：ds/audit.md。

## 收尾
3 家核心厂商用户点名疑点（自动/手动、计费、TTL）+ 4 家扩展厂商 + OpenRouter 全部有官方一手结论；唯一的反常识主张（Anthropic 自动缓存）已双源核实；终审 0 处矛盾。任务结束，未再开新一轮。
总 spawn 数：11（R1: 6 + R2: 4 + 终审: 1）。
