# journal（autoresearch/sep24）

每个实验一段：观察 → 假设 → 结果 → 为什么收/弃 → 学到什么。提案者读这里，避免重复试同一个想法。

## 设置

- 被改对象：`skills/deep-search/`（起点 v1.1，skill_chars 见 e000a）。
- dev 臂：Claude Code，Sonnet 主 → Haiku 工人，WebSearch + WebFetch，`--rounds 3 --workers 6 --budget 9000`，60 分钟 / $20 上限。
- 开发任务：prompt-caching、agent-protocols、py-packaging。留出：js-runtimes（dev 臂）、api-protocol（flagship 臂）。
- 评审：Opus + Grok 盲评对打，两种顺序。
