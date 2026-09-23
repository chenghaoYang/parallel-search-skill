# taxonomy grid（v2，R2 收束后更新）

状态：✅ 一手+原文；⚠ 仅二手/部分；⚔ 冲突；❓ 缺口；∅ 官方未写（已定向查过）；— 不适用。

## 分类轴（v2：google-interactions 归 D 族但注明向 B 族收敛）

轴：**请求形状谱系 + 状态放哪端**。R2 发现：Google Interactions API 引入服务端状态（previous_interaction_id、store 默认开）与 typed steps，在「状态放哪端」上向 B 族（Responses）收敛；xAI 把 /v1/responses 设为 primary、chat 标 legacy，下游也开始向 B 迁移。

- **A. Chat Completions 谱系**：openai-chat（参照）、deepseek-chat、google-openai、qwen、moonshot-chat、mistral、groq/together/fireworks、vllm、ollama、openrouter
- **B. Responses 谱系**：openai-responses（参照）、xai-responses（primary）、deepseek-responses、vllm/ollama 的 /responses（stateless 子集）
- **C. Anthropic Messages 谱系**：anthropic-messages（参照）、zhipu-anthropic、deepseek-anthropic、qwen-anthropic（/apps/anthropic）、moonshot-anthropic（自称）
- **D. Google 自有谱系**：google-gc（legacy）、google-interactions（GA 推荐）

## 维度（D1–D11 不变）

## 网格（R3 + 终审后；v2 终态）

| 实体 \ 维度 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| openai-chat | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| openai-responses | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| anthropic-messages | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| google-gc | ✅ | ✅ | ✅ | ✅ | ⚠终止信号 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| google-interactions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| deepseek-chat | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| deepseek-responses | ✅ | — | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | ✅ | — |
| deepseek-anthropic | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | — | ✅ | ✅ | — |
| zhipu-anthropic | ✅ | ✅ | ∅零文档 | ∅零文档 | ∅零文档 | ✅ | ∅ | ∅ | ✅ | ✅ | ✅ |
| zhipu-responses(/api/v1) | ✅ | — | ✅(none/auto) | ✅(store默认false) | ✅(无[DONE]) | ✅ | ✅ | ✅(text\|json_object) | ✅ | — | — |
| zhipu-native | ✅ | — | — | — | — | — | — | — | — | — | — |
| qwen | ✅ | — | ✅(tools×stream已放开) | — | ⚠ | — | ✅ | ⚔json_schema范围 | ✅ | — | — |
| moonshot | ✅ | — | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | — | ✅(R3双面入口) |
| xai | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅(端点×模型两维裁决) | ✅ | ✅ | — | ✅ |
| mistral | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ⚠ | ✅ | ✅ |
| openrouter/vllm/ollama/groq/together/fireworks/litellm | ✅ | — | — | — | — | — | ⚠ | — | ⚠ | — | — |

剩余 ⚠/∅/⚔ 项已全部写入 report §5。终态：核心格 112 ✅，可文档解决的缺口为 0。

## R2 → R3 决策

R2 观察：① 智谱官方对 anthropic 端点逐项行为零文档（∅），无法再靠文档补；智谱 coding plan 的 /api/v1（responses 面）与 /api/coding/paas/v4 是 ❓ 且影响多协议面总表；② moonshot 自称 anthropic/responses 兼容但入口未核（❓）；③ 百炼 tools×stream 两页打架（⚔）；④ xAI penalties 三口径（⚔）。→ 动作：R3 派 2-3 个定向工人（zhipu-coding-faces、moonshot-faces+百炼裁决、xAI penalties 核验），随后终审 1 工人。→ 预计 spawn：3+1。
