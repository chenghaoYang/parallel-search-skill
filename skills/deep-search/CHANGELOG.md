# deep-search changelog

## v1.2-dev（2026-09-24 起，evolve/ 自进化循环收下的改动）

- **e002 边界主张先反证**（Claude Code dev 臂 +0.50，2/3 题胜；doubts +15、accuracy +9；单次花费反而低 11%）：
  否定、排他、强制、全称、时间边界类主张进「一屏看懂」或疑点结论前，先用自己的笔记找反例，找不到再派反证简报；
  工人写这类主张前重取页面、版本起点查 changelog 最早条目；终审不许把「没找到来源」改写成否定句。
  起因：A/A 判决里约六成硬错是这类主张，grid 里标 ✅ 却从没被核验过。

## v1.1（2026-09-23，bench 第一轮之后）

按 bench 里看到的现象改，不改流程：

- harness.md：加 Kimi Code、Grok Build 两节；写明各外层「等一批」的正确方式；Claude Code headless 下不许用 ScheduleWakeup /
  CronCreate 等待（cc-opus-opus 第 1 次因此丢了 10 个工人）；Perplexity 的配额回退、研究模式不可用、「产出文档」变成生成文件。
- worker.md / research-worker.md：`src` 必须是完整 URL（Sonnet 工人常写相对路径）；每个工人约 20–25 次工具调用，
  大文件只 grep 需要的段落（Opus 工人整份下载规范逐段核对，R1 用了 40 分钟以上、笔记超长）。
- SKILL.md：观察表加一行「与常识或旧版本相反、影响大的主张 → 先复核」。
- notes_lint.py：标出超过 8000 字符的笔记。
- harness.md（Grok）：记下 grok-4.7 主 agent 在等工人时自己抓网页（R1 88 次）。

## v1.0（2026-09-23）

bench 第一轮（cc-opus-sonnet、cc-opus-opus 重跑、grok-47-47、kimi-glm53-glm53flash）用的版本。
