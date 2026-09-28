# log

## R0（定框架，不 spawn）
- 写 brief.md：8 实体（OpenAI/Anthropic/Gemini/DeepSeek/Kimi/智谱/Qwen/OpenRouter）+ 6 个用户点名疑点。
- 写 grid.md v0：3 家族分类轴（F1 全自动隐式 / F2 请求内显式断点 / F3 独立缓存对象）+ 10 维度。
- 参数：rounds=3, workers≤6/轮, budget=9000 chars, dir=./ds。
- 决策：R1 用满 6 个 worker，优先覆盖用户点名的 4 家 + Kimi（domestic 里文档最成熟)，第 6 个 worker 做智谱+Qwen+OpenRouter 的侦察（scout），因为 8 实体 > 6 workers/轮，且这三家预期文档信息密度较低，先侦察再在 R2 精查。
- 预计 spawn：6

## R1 观察 → 决策 → 结果
- 结果:6/6 工人回收,116 claims(official 114/secondary 2),0 缺 src/quote,4 conflicts,34 gaps,17 leads。r1-anthropic.md 8262 字符,超 8000 硬上限但不影响使用。
- 收束:更新 grid.md v1(taxonomy 细化为 3 家族 + 2 个横切现象:①部分 F1 厂商叠加可选手动断点、②OpenRouter 是网关元层非独立家族);矩阵 71% resolved(57/80 ✅,17 ❓,6 ⚠)。首次重写 report.md,4795 字符(budget 9000,余量充足)。
- 观察:
  1. OpenAI 工人报告"GPT-5.6+/GPT-6 Sol"引入可选手动断点、折扣从50%升到90%、写入费从免费变1.25x——这与用户疑点①("OpenAI自动免改代码")直接相关且数字反常,影响力大,复核前不写进一屏看懂结论(已按此处理)。
  2. Anthropic 工人发现官方文档存在"Automatic Caching"顶层模式(不必逐块标),这也直接关系用户疑点①,需确认它是否真的降低了"必须手动"的门槛,还是仍需加参数。
  3. Gemini explicit CachedContent(F3 家族唯一代表)的 D4/D5/D6/D9 完全空白,不能让核心矩阵留这么大的洞。
  4. OpenRouter 计费关系(是否加价)、sticky routing 覆盖范围未确认。
  5. 智谱/DashScope 有少量格子缺口;Bedrock/Vertex/Azure 三个 leads 反复被独立工人提及,值得一个 scout 核实。
- 决策:R2 派 6 个工人,全部点名具体格子/主张(见 grid.md「R2 待解决」)。不再做大范围检索。
  1. r2-verify-openai:复核 OpenAI D1/D4/D5/D6 反常数字
  2. r2-verify-anthropic-auto:确认 Anthropic「Automatic Caching」的真实改动量
  3. r2-gemini-explicit:填 Gemini explicit CachedContent 的 D4/D5/D6/D9
  4. r2-openrouter-billing:确认 OpenRouter 是否加价、sticky routing 覆盖范围
  5. r2-zhipu-dashscope-gapfill:补智谱 D5/D7/D9、DashScope implicit D6/D8
  6. r2-adapters:AWS Bedrock/Vertex/Azure 与原生 API 的缓存差异,每平台只求1-2条关键事实
- 预计 spawn:6

## R2 观察 → 决策 → 结果
- 结果:6/6 工人回收,54 claims(全 official),0 缺 src/quote,6 conflicts(多为"上一轮混淆新旧模型参数"这类良性修正),18 gaps,13 leads。
- 关键修正:OpenAI TTL 之前误传"GPT-5.6+ 可配置到24h"——实际 GPT-5.6+ 固定 30m(prompt_cache_options.ttl 只接受这一个值),24h 选项属于更早模型的 prompt_cache_retention 参数,两者不能混为一谈,已在矩阵拆成两行(按模型代际)。
- 关键新发现:①Anthropic"Automatic Caching"经核实仍需在请求顶层加 1 次 cache_control,不是零改动,用户疑点①的答案维持"Anthropic 仍需手动"结论,但补充"现在只需1次不必逐块"的细节;②AWS Bedrock 官方文档证实 Claude 在 Bedrock 上有不需要 cache_control 的 Implicit Prompt Caching,是全文唯一的"母协议手动、云托管自动"例外,补进 taxonomy 横切现象3和第3节;③Gemini explicit CachedContent 的计费(存储费$0.50→$1.00/M tok/时)和TTL(默认1h)首次补全,F3 家族不再空白;④OpenRouter 官方 FAQ 确认"no markup",sticky routing 是条件触发(上游缓存价<常规价)而非无条件。
- 收束:重写 grid.md v2(矩阵按实体最终状态整理,加"变体/适配层最终状态"表);重写 report.md,6311 字符(budget 9000,余量2689)。grid 状态 62/63 ✅或∅(98%),仅剩 Vertex AI 上 Claude 的具体费率是 ⚠(两轮工人都没找到官方费率页,判定为深挖边际收益低的 P2 细节)。
- 观察:核心格子(触发/命中价/写入费/TTL/命中字段 × 8实体 + 4适配平台)已全部✅或∅(官方确认未写,非未查到);R2 相比 R1 显著改变了网格(修正1处误传、新填2个此前空白家族代表);本轮结束后剩余缺口全部是已定向查过的 P2 细节。命中 SKILL.md 停止条件"核心格子都是✅/∅"。
- 决策:不开 R3 大规模扩展("不许为了凑轮数派工人")。直接进入终审:派1个审稿工人抽查 report.md 对照 notes 核实≥20条具体主张。
- 预计 spawn:1(终审)

## 终审 → 收尾
- 审稿工人抽查 22 条具体主张(覆盖第0/2/3/4节):19 supported、1 weak(DashScope 隐式折扣)、1 contradicted(但矛盾方是 r1-openai.md 笔记本身的旧记录,report.md 早已用 r2 的修正版本,无需改动)、0 unsupported。用户点名的 6 条核心结论全部 supported。
- 复核 weak 项:直接回查 r1-scout-cn-gateway.md 原文,C11 其实是 `type: official` 且带直接原句"隐式缓存命中部分约为标准价的 20%"——审稿工人核对时误引了 C13/C14(那两条是TTL和失效条件,不是折扣),真实支撑充分,判定为审稿工具自身引用错误,不是 report.md 的问题,不改动正文。
- 终稿:report.md 6311 字符(Python len(),含来源节),budget 9000,余量 2689;grid 62/63 ✅/∅(98%),剩 1 项 Vertex AI Claude 具体费率标 ⚠,已写入第5节「未决」。
- 复制到仓库根目录 ./report.md(外层要求的交付位置)。
- 停止:核心结论全部核实、budget 达标、grid 98% resolved,符合 SKILL.md 终止条件,不再开新一轮。
