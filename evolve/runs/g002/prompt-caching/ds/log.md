# log

参数：rounds=3 workers=6 budget=9000 dir=./ds worker-model=grok-4.7。无 pplx-safe。主 agent 不搜网页。

## R0

观察：用户疑点集中在「还要不要改代码、命中怎么计费、活多久、怎么确认、什么会失效」。四家是核心，Kimi / 智谱 / 通义 / OpenRouter 是第二圈。Gemini 的 implicit 与 explicit 不是同一机制，网格拆成两行。

决策：taxonomy v0 用轴 A（控制点）做主家族、轴 B（钱记在哪）做第二分族。R1 按官方文档站拆 4 个实体工人（Gemini 两行归一个文档站）+ 2 个 scout。不在 R1 填国内厂和网关，避免一个工人跨多个文档站。

→ 动作：R1 铺开 → 预计 spawn：6

## R1

spawn：6（openai、anthropic、gemini、deepseek、scout-pitfalls、scout-cn），全部返回。lint：6 份笔记、146 条主张，全部 official，0 条缺 src/quote。

taxonomy v0→v1：主轴改成「默认就缓存 / 请求里要有缓存字段 / 先创建资源」，并单列计费结构与介质。新增 D10 隔离与并发。通义拆成隐式、显式两行（官方写互斥），格子仍是 ❓，scout 原句不计入已填。原因写在 grid.md 文首。

成稿从头重写。roundstat：budget 9000；report.r1.md 与 report.md 8762；grid ✅ 34、⚔ 10、❓ 56、resolved 34/100。随后只改了家族表里 Gemini implicit 的措辞：一页写不承诺、另一页写命中就返利，不能写成已裁的「不承诺」。快照会按改后的正文重拷。

新增进正文的是四家的字段名、倍率、TTL 和失效条件。国内厂与 OpenRouter 只在第 5 节留文档 URL。删掉的是 scout 里没有原句的 Bedrock 400，以及 DeepSeek 模型新闻里的 SSD 体积（不是 API TTL）。

观察：第 0 节被两组 ⚔ 挡住。Anthropic「没有 cache_control 就不缓存」对上 thinking 小节的 without explicit markers。OpenAI「默认开启」对上「没放显式断点则不缓存」，以及 `ttl=30m` 对上 retention 只支持 `24h`。Gemini 的折扣承诺也是 ⚔，第 0 节没有把它写成结论。用户点名的 Kimi、智谱、通义、OpenRouter 仍全是 ❓。DeepSeek 的 64 token 是 2024 公告对现行指南，先留在未决。

→ 动作：R2 填四行空格子，并反证 OpenAI D1/D7 与 Anthropic D1/D7。Gemini 的写价、TTL、字段名留到 R3。
→ 预计 spawn：6
