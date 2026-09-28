# Grid v1（R1 后更新）

## 分类轴（v0→v1 改动：见 log.md R1）
- Axis A 触发机制：零改动自动命中 vs 至少声明一处（一个字段起）才生效 vs 全手动多断点
- Axis B 写入/未命中是否有溢价：首次写入（cache miss）本身要不要比不缓存更贵——这条轴比「内存/磁盘」更能解释各家计费差异，v1 用它替换 v0 的存储介质轴（存储介质多数厂商不公开，∅ 太多，解释力弱）

## 维度（列）
D1 触发方式｜D2 最小可缓存长度｜D3 粒度/断点｜D4 命中读取计费｜D5 写入/存储计费｜D6 TTL｜D7 命中确认字段｜D8 失效条件｜D9 适用范围｜D10 存储介质/隔离

## 状态网格（R1 后）
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| OpenAI | ✅ | ✅ | ✅ | ✅ | ✅(需查是否仅GPT-5.6+适用) | ✅ | ✅ | ✅ | ⚠Chat Completions未确认 | ✅ |
| Anthropic | ✅**需R2复核**(反常识：新增自动模式) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini | ✅ | ✅ | ✅ | ⚔explicit✅90%，implicit仅Vertex二手90% | ⚔explicit✅，implicit仅Vertex二手称免费 | ⚔explicit✅1h，implicit仅Vertex二手≤24h | ✅ | ✅ | ✅ | ✅ |
| DeepSeek | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(区间"数小时到数天"不精确) | ✅ | ✅ | ⚠仅2款模型确认 | ✅ |
| Kimi | ✅ | ✅ | ⚠断点数上限未披露 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ∅官方未披露 |
| 智谱GLM | ✅ | ✅ | ✅ | ✅ | ✅(限时免费) | ∅官方未给数字 | ✅ | ❓仅"异步生效"未给具体规则 | ✅ | ∅官方未披露 |
| 通义千问 | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠explicit✅5min，implicit❓无数字 | ✅ | ✅ | ✅（需注明含第三方托管模型） | ✅ |
| OpenRouter | ✅ | ∅网关层不适用 | ∅网关层不适用 | ⚠仅二手 | ⚠仅二手 | ✅（转述上游） | ✅ | ∅网关层不适用 | ✅ | ∅网关层不适用 |

## R2 完成情况（4/4 返回，18 条主张全 official，2 冲突，8 缺口）
- Anthropic D1：✅ 复核通过——「自动缓存」真实存在，2026-02-19 上线（源：anthropic-sdk-python commit），官方原文明确「仍需显式加 cache_control，不是不加任何参数就全自动」。反常识主张已验证，非零改动。
- OpenAI D9：✅ 缺口已填——Chat Completions 经 `prompt_cache_options` 参数确认支持 gpt-5.6+；但官方指南页与 API reference 覆盖面不一致（指南只讲 Responses/Agents），记入未决。
- OpenAI D5：✅ 确认 1.25x 写入溢价对 implicit/explicit 两种模式都适用，非仅显式。
- DashScope implicit D6：✅ 官方原文「无固定有效期，系统按使用频率清理」——不是缺口，是官方给出的设计说明（无固定数字是事实本身）。
- 智谱 D6、Gemini implicit D4：∅ 二次核实仍未给数字，确认为官方沉默而非上一轮漏查。
- OpenRouter D4/D5：⚔ 升级——官方 https://openrouter.ai/docs/features/prompt-caching 确实列出分供应商倍率表（如 Anthropic 写 1.25x），但无「不加价」声明，且部分倍率（OpenAI 读取 0.25x–0.5x）比该厂商官网直连价（0.1x）更贵，无法排除加成，只能确认「官方给了表，没给保证」。
- Kimi D10：∅ 二次核实仍未披露存储介质。

## 决策：进入终审，不再开 R3
核心矩阵格子已 ✅/∅，用户点名的疑点（自动/手动、计费、TTL）在 R2 都完成了反证/核实，OpenRouter 加价问题也升级为有官方一手依据的结论。剩余缺口（DeepSeek 完整模型列表、Kimi 断点概念是否存在等）不影响核心结论，边际价值低于终审校对。按 rounds=3 硬上限和「核心格子解决+边界主张已反证」双重停止条件，跳过 R3 扩展，直接派终审工人。

## R1 完成情况
6/6 工人返回，92 条主张（official 90 / secondary 2），4 处冲突，24 个缺口，15 条线索。r1-cn-a 笔记因子标号格式（`[C1-Kimi-D1]`）没被 lint 脚本解析，人工确认笔记完整无误（20 条 claims），不重派。

## R2 计划（针对性，非普查）
- r2-verify-anthropic：核实 Anthropic「自动缓存」是否真实存在、上线时间、是否仍需加一个 cache_control 字段（区分「零改动」vs「一个字段起效」）。对应 [C1][C2] 及 gaps 里的发布时间。
- r2-openai-gaps：Chat Completions 是否支持 prompt caching；写入 1.25x 是否也适用于默认自动模式而非仅显式断点；域名 developers.openai.com 是否为当前官方文档域。对应 D9 gap、[C8][C9]。
- r2-ttl-gaps：DashScope 隐式缓存 TTL 精确值；智谱 GLM TTL 是否有数字；Gemini API（非 Vertex）官方是否给出 implicit caching 折扣数字。对应 D6/D4 的 ❓⚔ 格。
- r2-openrouter-kimi：OpenRouter 官方文档（非三方博客）是否明确「不加价、原样转发」；Kimi 存储介质、断点上限官方是否披露。对应 D4/D5/D10 的 ⚠∅ 格。
