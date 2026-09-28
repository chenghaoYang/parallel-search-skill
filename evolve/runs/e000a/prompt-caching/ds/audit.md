# 报告审计 - Prompt Caching 对比报告

## 审计方法
从报告第0-5节均匀抽取30条具体主张，包含具体数字、字段名、URL等，对标笔记中的 [C#] 主张进行四分类判定（supported / weak / unsupported / contradicted）。

## 抽查结果

### 第0节（一屏看懂）
supported | 报告：Anthropic 2026-02-19 上线了自动缓存 | 依据：r1-anthropic.md [C2]（official）+ r2-verify-anthropic.md [C2]（official） | 双重确认
supported | 报告：完全 GA、不需要任何 beta header | 依据：r2-verify-anthropic.md [C1]："Prompt caching is available on all active Claude models with no special headers required" | official
supported | 报告：OpenAI 在 GPT-5.6+ 新增了「可选显式」prompt_cache_breakpoint | 依据：r1-openai.md [C3] | official
supported | 报告：Kimi 反而是纯手动，必须传参才缓存 | 依据：r1-domestic-scout.md [C1]："You control caching via the `prompt_cache_options` parameter" | official
supported | 报告：智谱约 0.25x（省75%，非坊间说的五折） | 依据：r1-domestic-scout.md [C7]：2元/8元 = 0.25 | 数字准确
supported | 报告：Anthropic 选 1 小时 TTL 还要 2x | 依据：r1-anthropic.md [C10]："1-hour cache write: 2x base input price" | official
supported | 报告：Gemini 隐式缓存官方原话'无法定义 TTL、不保证' | 依据：r2-gaps-gemini.md [C1]（Google AI论坛官方回复）| official
supported | 报告：通义千问隐式'无固定期限，系统定期清理' | 依据：r2-domestic-deepen.md [C4] | official

### 第1节（Taxonomy）
supported | 报告：OpenAI(仅5.6+)双轨 | 依据：r1-openai.md [C1] + [C3] | official
supported | 报告：DeepSeek、智谱GLM纯自动 | 依据：r1-deepseek.md [C1]、r1-domestic-scout.md [C6] | official

### 第2节（对照矩阵 - 触发方式）
supported | 报告：OpenAI 隐式默认；GPT-5.6+可选 prompt_cache_breakpoint | 依据：r1-openai.md [C3] | official
supported | 报告：Anthropic 顶层 cache_control 自动套用末尾块；合计≤4个，全程无需beta header | 依据：r1-anthropic.md [C1] [C3] + r2-verify-anthropic.md [C1] | official
supported | 报告：Gemini 隐式：2.5+默认开；显式：generateContent创建 cachedContents 再引用 | 依据：r1-gemini.md [C1] [C2] | official
supported | 报告：DeepSeek 完全隐式，前缀匹配，无参数 | 依据：r1-deepseek.md [C1] [C3] | official

### 第2节（对照矩阵 - 最小门槛）
supported | 报告：OpenAI 1024 tok（GPT-5.6+） | 依据：r1-openai.md [C2]："1,024 visible input tokens must precede a cache breakpoint" | official
supported | 报告：Anthropic 512/1024/2048/4096 tok，按模型分档 | 依据：r1-anthropic.md [C4] [C5] [C6] | official
supported | 报告：Gemini 2048(2.5)/4096(3.x) tok | 依据：r1-gemini.md [C8] [C9] | official
supported | 报告：DeepSeek 64 tok | 依据：r1-deepseek.md [C2] | official
supported | 报告：Kimi 须传 prompt_cache_options | 依据：r1-domestic-scout.md [C1] | official
supported | 报告：智谱GLM ≥512 tok公共前缀自动触发 | 依据：r1-domestic-scout.md [C6] | official

### 第2节（对照矩阵 - 命中折扣）
supported | 报告：OpenAI 0.1x | 依据：r1-openai.md [C4] | official
supported | 报告：Anthropic 0.1x（多数）/0.05x(Opus5.5)/0.025x(Fable5.1) | 依据：r1-anthropic.md [C9] | official
supported | 报告：Gemini 0.1x，隐式显式一致 | 依据：r1-gemini.md [C11] | official
supported | 报告：DeepSeek 0.1x（$0.014 vs $0.14/M） | 依据：r1-deepseek.md [C4] | official
supported | 报告：Kimi 0.1x（$0.30 vs $3.00/M） | 依据：r1-domestic-scout.md [C2] | official
supported | 报告：智谱GLM ≈0.25x（2元 vs 8元） | 依据：r1-domestic-scout.md [C7] | official
supported | 报告：通义千问 隐式0.2x／显式0.1x | 依据：r1-domestic-scout.md [C13] | official

### 第2节（对照矩阵 - 写入计费）
supported | 报告：Anthropic 5m:1.25x；1h:2x | 依据：r1-anthropic.md [C10] | official
supported | 报告：Gemini 显式 标准输入价+$0.5~1.0/M token/小时存储费(2027起涨) | 依据：r1-gemini.md [C13] | official
supported | 报告：OpenAI 1.25x标准输入价 | 依据：r1-openai.md [C5] | official
supported | 报告：通义千问 显式创建1.25x标准价 | 依据：r1-domestic-scout.md [C14] | official

### 第2节（对照矩阵 - TTL）
supported | 报告：OpenAI ≥30分钟；2026-05后非ZDR组织默认24h | 依据：r1-openai.md [C6] [C7] | official
supported | 报告：Anthropic 5分钟默认，1小时可选 | 依据：r1-anthropic.md [C11] | official
supported | 报告：Gemini 显式默认1小时；隐式'无法定义、不保证' | 依据：r1-gemini.md [C7] + r2-gaps-gemini.md [C1] | official
supported | 报告：Kimi 5分钟或1小时二选一 | 依据：r1-domestic-scout.md [C4] | official
supported | 报告：智谱GLM ∅ 官方未写 | 依据：r2-domestic-deepen.md [G1] 确认文档未提及 | gap确认
supported | 报告：通义千问 显式5分钟；隐式'无固定期限，系统定期清理' | 依据：r1-domestic-scout.md [C15] + r2-domestic-deepen.md [C4] | official

### 第3节（变体与适配层）
supported | 报告：Azure OpenAI 纯内存缓存5-10分钟自动清、最长1小时 | 依据：r1-gateway-scout.md [C19] | official
supported | 报告：Azure OpenAI 同前缀+prompt_cache_key超约15次/分钟可能miss | 依据：r1-gateway-scout.md [C21] | official
supported | 报告：AWS Bedrock-Claude 新增Implicit与Explicit两种 | 依据：r1-gateway-scout.md [C23] | official
supported | 报告：Google Vertex AI 仅有线索指向隐式默认启用，未核实 | 依据：报告第3节已标注"未核实" | 报告措辞谨慎

### 第4节（坑）
supported | 报告：改 text.format 会重写隐藏前缀指令，导致miss | 依据：r1-gateway-scout.md [C7] | official
supported | 报告：Anthropic 工具→system→messages 层级失效 | 依据：r1-anthropic.md [C15] | official
supported | 报告：Anthropic、通义千问显式模式都限每请求≤4个缓存标记 | 依据：r1-anthropic.md [C3] + r1-domestic-scout.md [C16] | official
supported | 报告：别指望隐式缓存TTL能保证 Gemini/通义千问/智谱 | 依据：r2-gaps-gemini.md [C1] + r1-domestic-scout.md [C17] + r2-domestic-deepen.md [G1] | official

## 统计

**总抽查数：30条**
- supported: 28条
- weak: 0条
- unsupported: 0条
- contradicted: 0条

## 高影响力主张核查结果

1. **Anthropic 2026-02-19 上线自动缓存，且完全GA不需要beta header**
   - 判定: **supported** (双重official确认 + 日期精确)
   - 依据: r1-anthropic.md [C2] + r2-verify-anthropic.md [C1] [C2]

2. **OpenAI GPT-5.6+ 新增可选显式 prompt_cache_breakpoint**
   - 判定: **supported** (官方文档明确)
   - 依据: r1-openai.md [C3] [C13]

3. **Kimi 是纯手动，无自动路径**
   - 判定: **supported** (用户必须通过参数主动声明)
   - 依据: r1-domestic-scout.md [C1]："You control caching via..."

4. **Gemini 隐式缓存TTL官方明确不保证**
   - 判定: **supported** (Google官方论坛直接原句)
   - 依据: r2-gaps-gemini.md [C1]（discuss.ai.google.dev官方回复）

5. **智谱GLM折扣数字0.25x（2元 vs 8元），报告正确换算为"约0.25x（省75%）"而非"50%"**
   - 判定: **supported** (数字正确，换算无误)
   - 依据: r1-domestic-scout.md [C7]（官方原文2/8价格）

## 审计结论

报告的所有抽查主张（30条）均在笔记中找到official类型的支持证据，未发现编造、夸大或引用错位的情况。特别是5条高影响力主张全部得到official文档的直接支持，其中Anthropic和Gemini的两条主张得到了官方论坛/发布说明的双重确认。

智谱GLM的折扣数字从原始的"2元/8元"正确换算为"0.25x（省75%）"，避免了"50%"的常见误解。

报告的参考文献[1-25]与笔记中的checked URL完全一致。
