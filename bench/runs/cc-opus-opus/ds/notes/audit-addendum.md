# audit-addendum
question: 终审工人（audit-a / audit-b）回原页核对时取得、但原笔记缺失或摘错的原句；由主 agent 从 audit-a.md / audit-b.md 转录，不含新调研。
checked: https://api-docs.deepseek.com/guides/anthropic_api, https://platform.minimax.io/docs/api-reference/responses-create, https://github.com/betmoar/cc-proxy-plugin/issues/67, https://developers.openai.com/api/docs/guides/migrate-to-responses, https://api-docs.deepseek.com/updates

## claims
- [C1] DeepSeek Anthropic 兼容层 tool_choice 表另有 none 一行，标 Fully Supported（纠正 r1-deepseek C29 的遗漏；audit-b 回原页核对） | src: https://api-docs.deepseek.com/guides/anthropic_api | quote: "Fully Supported" | type: official
- [C2] MiniMax Responses：M3 的 reasoning 默认 none，即关闭推理（audit-b 回原页核对） | src: https://platform.minimax.io/docs/api-reference/responses-create | quote: "For MiniMax-M3, the default is `none`, which disables reasoning." | type: official
- [C3] 智谱（Z.ai）返回的 server_tool_use 回灌 Anthropic 官方 API 时报 400（id 须匹配 srvtoolu_ 前缀；audit-b 回原页核对） | src: https://github.com/betmoar/cc-proxy-plugin/issues/67 | quote: "API Error: 400 messages.799.content.1.server_tool_use.id: String should match pattern '^srvtoolu_[a-zA-Z0-9_]+$'" | type: secondary
- [C4] OpenAI Responses 缓存利用率 40–80% 为内部测试结果（补全 r1-openai-responses C21 原句；audit-a 回原页核对） | src: https://developers.openai.com/api/docs/guides/migrate-to-responses | quote: "Results in lower costs due to improved cache utilization (40% to 80% improvement when compared to Chat Completions in internal tests)." | type: official

## conflicts
- r1-deepseek C29 只摘了 "Supported (disable_parallel_tool_use is ignored)"，未含 none 行；以本笔记 C1 为准。

## gaps
- audit-a：updates 页 2026-04-24 公告为将来时 "will be discontinued in three months (2026-07-24)"，其后无"已停用"确认条目 → 成稿改为"按公告于 2026-07-24 停用"。

## leads
- 无
