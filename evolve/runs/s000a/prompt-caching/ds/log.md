# log

参数：rounds=3，workers≤6，budget=9000 字符。工作目录 `./ds`。工人模型 `swe-2-shim`。无 pplx-safe。主 agent 不搜网页。

## R0

- 读者要在几分钟内分清触发方式、计费、寿命、观测、失效。点名疑点见 `brief.md`。
- taxonomy v0 分类轴：边界由谁划定 × 形态（隐式前缀 / 请求内断点 / 独立资源 / 网关）。维度 D1–D8，见 `grid.md`。
- 核心 9 行（含 Gemini 拆成 implicit/explicit）。变体 3 行（Azure、Vertex、Bedrock）默认不进主矩阵。
- R1 不填国内厂和 OpenRouter：先由 scout 收回官方 URL，避免工人在错文档站上耗预算。
- 动作：派 4 个文档站工人 + 2 个 scout。预计 spawn：6。

## R1

- spawn 6（openai、anthropic、gemini、deepseek、scout-pitfalls、scout-others），全部返回。lint：144 条主张，全是 official，0 条缺 src/quote。`r1-gemini.md`、`r1-scout-others.md` 超过 8000 字符，仍能解析。
- taxonomy v0→v1：分类轴保留。取消「一家只占一个家族」。OpenAI 默认 I、GPT-5.6+ 可选 II；Gemini 是 I+III；Anthropic 仍是 II，但标记有顶层和块级两种放法。命中是否计入限流不新开维度。
- 网格：四家核心行大多 ✅。⚔ 四格：OpenAI D2（回看窗口个数）、Anthropic D1 与 D4（2025-08 快照对现行页）、DeepSeek D3（新闻页 64 token 对现行 prefix unit）。∅：Gemini implicit 的 D4、D7，explicit 的 D3。国内四行保持 ❓。scout 笔记不进成稿。
- 字数：首稿 9921，删掉和第 2 节重复的坑、压短未决后 8979。快照 `snapshots/report.r1.md`。roundstat：resolved 36/96（38%）。变体行拉低了填充率，核心四家（32 格）里已决的是 ✅+∅。
- 观察：读者那句「Anthropic 必须手动打断点」对不上现行页，OpenAI 5.6 的写入计价也对不上旧记忆。这两条有原句，但按规则还没做复核，所以一屏只写了「仍要 cache_control」和「5.6 价格不当全线结论」。成稿最大的洞是四家国内/网关仍是 ❓；scout 已经给了官方 URL。DeepSeek 价目数字的原句没带上表格单元格，Gemini implicit 折扣仍空，这两件比国内四家窄，留给下一轮以后。
- 动作：R2 不重查四家全量。2 个复核简报（Anthropic 启用方式；OpenAI 5.6 的计价和 TTL 原句）+ 4 个定向摘录（Kimi、智谱、百炼、OpenRouter），每家只填自己那一行。预计 spawn：6。

## R2

- spawn 6，全部返回。lint：144 条主张。OpenRouter 多数 claim 把 src 写在文首声明而不是每一行，收束时按该声明引用 `openrouter.ai/docs/features/prompt-caching`，不把它转述的上游价写进厂商行。
- 复核结果：Anthropic 顶层 `cache_control` 与 2025-08 快照的差别是版本差（release notes：automatic caching 2026-02-19；1 小时 TTL 2025-08-13 起不用 beta）。D1/D4 从 ⚔ 改为 ✅。OpenAI 5.6 的 1.25×、0.1×、`"30m"`，以及「复用刷新且不再收写入费」都有原句，升入一屏。
- 新增进成稿：Kimi（Chat 与 Messages 默认相反）、智谱、百炼隐式/显式/Session、OpenRouter 粘性路由与标记互译。Kimi 旧 `/v1/caching` 实测 404，不进现行家族。
- 为了塞进这些行，删了：OpenAI 逐项失效的重复叙述、Gemini 分型号存储价的展开、和第 2 节重复的 TPM 坑、以及只出现在 scout 笔记里的「Anthropic 第一次响应开始后才可命中」。
- 字数：8979 → 8799（-180）。快照 `snapshots/report.r2.md`。
- 观察：用户点名的四家国内/网关已经进矩阵，但三处计费还不能当最终数。DeepSeek 美元价的原句没有单元格；Kimi 价表原句是没有表头的 JSON；Gemini 隐式折扣仍是 ∅。Anthropic「完全不传 cache_control 会不会缓存」被 server tools 一句搅浑，还没打开那一页。智谱 50% 对 25%、OpenRouter 对百炼/Gemini 的转述，两边原句都在，再派工人也不会变成一个数。
- 动作：R3 只打这四个洞，每个工人只开指定页。预计 spawn：4。不复核已经 ✅ 的触发方式。

## R3

- spawn 4（deepseek 价、kimi 表头、anthropic server tools、gemini implicit 折扣），全部返回。
- 收进成稿：DeepSeek 美元/人民币价的表头原句已对齐，D5 改为 ✅；现行指南没有 64，D3 改为 ✅（无具体 token 数）。Kimi K3 列为 5 分钟写入 ¥20、1 小时 ¥40、命中 ¥2、未命中 ¥20。1/10 只是 k3 的例子。Anthropic：不放 `cache_control` 时 server tools 也不写缓存；放了之后 web search 会额外写一笔 5 分钟。Gemini 隐式折扣现行文档仍无百分比，博客 75% 不进矩阵。
- 为了不超上一版字数，删了 taxonomy 里的元说明、Azure/Vertex 一句、以及未决里已经核对完的「价目原句缺数字」。
- 字数：8799 → 8797。快照 `snapshots/report.r3.md`。
- 观察：三轮扩展用完。核心行里还开着的是冲突而不是没查：OpenAI 回看窗口、智谱 50% 对定价页、OpenRouter 转述和厂商页不一致。这些已经把两边原句放进第 5 节，再派调研工人不会合成一个数。
- 动作：终审。1 个审稿工人对照笔记抽查 ≥20 条，不新开调研题。预计 spawn：1。
