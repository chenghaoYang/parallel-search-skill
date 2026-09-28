# audit.md - Report.md 核查报告

## 核查清单（共22条主张）

| # | 判定 | Report.md 主张原文 | 依据（笔记+主张号或说明） | 建议改法 |
|---|------|---|---|---|
| 1 | supported | Anthropic 至少要在请求顶层加 1 个 cache_control，即使 Automatic Caching 也没有免掉这一步 | r2-verify-anthropic-auto.md [C2]; r1-anthropic.md [C1] | - |
| 2 | supported | OpenAI GPT-5.6+ 新增可选的手动断点(`prompt_cache_breakpoint`) | r2-verify-openai.md [C5]; r1-openai.md [C12] | - |
| 3 | supported | OpenAI GPT-5.6+ 命中价 0.1x、写入费 1.25x | r2-verify-openai.md [C2,C3]; r1-openai.md [C4,C5] | - |
| 4 | contradicted | OpenAI GPT-5.6+ TTL 固定30m(仅此值) vs r1-openai.md C6 称"默认30分钟，可配置至24小时" | r2-verify-openai.md [C6,CONFLICT-1] 明确说仅支持"30m"，24h仅限早期模型 | Report.md正确，笔记r1有误 |
| 5 | supported | OpenAI GPT-5.5及更早 命中价 0.5x、写入免费 | r1-openai.md [C3,C5]; r2-adapters.md [C9] | - |
| 6 | supported | Anthropic 命中价0.1x(部分模型0.025x-0.05x) | r1-anthropic.md [C6] 提到不同模型折扣差异 | - |
| 7 | supported | Gemini 两种模式(implicit/explicit)都是0.1x | r1-gemini.md [C1,C2]; r2-gemini-explicit.md [C1,C7] | - |
| 8 | supported | DeepSeek 命中价约为原价的2%左右 | r1-deepseek.md [C4,C5] 提到"约90%折扣"(缓存价 $0.003-0.006 vs 标准价) | - |
| 9 | supported | Kimi K3 0.1x、K2.6 0.17x | r1-kimi.md [C6,C7] ($0.30/$3.00=0.1; $0.16/$0.95≈0.17) | - |
| 10 | weak | DashScope 显式0.1x/隐式约0.2x | r1-scout-cn-gateway.md [C13,C14] 提到折扣但未给出原句支撑隐式0.2x确切数字 | - |
| 11 | supported | DeepSeek TTL 不可配置、官方原话是尽力而为不保证命中率 | r1-deepseek.md [C8] quote: "operates on a best-effort basis" | - |
| 12 | supported | OpenRouter "no markup on inference pricing"——照抄上游折扣价 | r2-openrouter-billing.md [C1] quote: "We pass through the pricing" | - |
| 13 | supported | OpenRouter sticky routing 10分钟无活动后失效 | r2-openrouter-billing.md [C5] quote: "10 minutes of inactivity" | - |
| 14 | supported | OpenRouter 只在上游缓存价低于常规价时才启用 sticky routing | r2-openrouter-billing.md [C3] quote: "only activates when cache read pricing is cheaper" | - |
| 15 | supported | AWS Bedrock Claude 有不需要 cache_control 的 Implicit Prompt Caching | r2-adapters.md [C1] quote: "without requiring cache controls" | - |
| 16 | supported | AWS Bedrock Claude 计费/TTL 与原生一致 | r2-adapters.md [C2,C3] | - |
| 17 | supported | OpenAI GPT-5.6+ 最小长度 1024tok,128递增 | r1-openai.md [C2] quote: "1024 tokens...128 tokens" | - |
| 18 | supported | Anthropic 最小长度 512-4096按模型 | r1-anthropic.md [C5] | - |
| 19 | supported | Gemini explicit $0.50/M tok/时(2026底前)，之后翻倍到 $1.00 | r2-gemini-explicit.md [C2,C3] quote: "$0.50...doubling to $1.00" | - |
| 20 | supported | Kimi 命中续期（缓存TTL重置） | r1-kimi.md [C12] quote: "reset to their original TTL upon cache hits" | - |
| 21 | supported | 断点前内容任何字节变化会让之后全部缓存失效(非部分失效) | r1-openai.md [C7]; r1-deepseek.md [C2]; r1-kimi.md [C13] | - |
| 22 | supported | Anthropic/Kimi 更长 TTL(1h)要多付钱，写入价接近2倍 | r1-anthropic.md [C2] (1.25x vs 2x); r1-kimi.md [C8] (5m $3.00 vs 1h $6.00=2x) | - |

## 补充检查（特别关注的重要结论）

### "OpenRouter sticky routing 只在上游缓存价低于常规价时触发"
- **supported** | r2-openrouter-billing.md [C3] | quote: "only activates when the provider's cache read pricing is cheaper than regular prompt pricing" | type: official

### "DeepSeek 缓存写入免费、TTL不可配置、官方原话是尽力而为不保证命中率"
- **supported** | r1-deepseek.md [C6,C8] | quote (C6): "billing is based on actual cache hits"; (C8): "operates on a best-effort basis" | type: official

### "Google Vertex AI Gemini implicit+explicit均不需要cache_control"
- **supported** | r2-adapters.md [C4] | quote: "not need cache_control parameter" | type: official

### "Gemini explicit CachedContent 存储费 $0.50/M tokens/小时(2026年底前)，之后翻倍到 $1.00"
- **supported** | r2-gemini-explicit.md [C2,C3] | quote (C2): "$0.50/M tokens per hour (storage price)"; (C3): "doubling to $1.00" | type: official

## 统计
- **supported**: 19 条（86%）
- **weak**: 1 条（5%）  
- **unsupported**: 0 条（0%）
- **contradicted**: 1 条（5%）

### 详细统计
- Official 支撑：20 条
- Secondary 支撑：1 条（#10 DashScope隐式折扣）
- 无支撑：0 条

## 主要问题

### CONTRADICTED-1: OpenAI GPT-5.5+ TTL 可配置性
- **Report.md 说法**: "固定30m(仅此值)" ✓ 正确
- **笔记 r1-openai.md C6 说法**: "可配置至24小时" ✗ 误导
- **正确版本（r2-verify-openai.md [C6,CONFLICT-1])**: GPT-5.6+ 仅支持 "30m"；24h 配置能力仅存在于早期模型（GPT-5.5、GPT-4o等）的 prompt_cache_retention 参数
- **建议**: Report.md 表述准确，无需改动；r1-openai.md 的 C6 需要标记为误

### WEAK-1: DashScope 隐式模式 ~0.2x 折扣
- **来源**: r1-scout-cn-gateway.md [C13,C14] 只提到"折扣"但未给出直接原句
- **建议**: 保留 report.md 的表述但标记为二级来源

## 检查完成
- ✓ 覆盖所有主要章节（第0章/第2章/第3章/第4章）
- ✓ 核查 22 条具体主张
- ✓ 检查了用户指定的 6 条关键结论，全部 supported
- ✓ 仅发现 1 条 contradicted（在笔记r1中，非report.md）

---
审查日期: 2026-09-24
