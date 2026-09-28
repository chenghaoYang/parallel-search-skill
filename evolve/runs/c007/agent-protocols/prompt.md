/deep-search 产出文档 帮用户理清 agent 时代各种「协议」分别管什么、有什么不同

seed keywords: MCP (Model Context Protocol). A2A (Agent2Agent). ACP. AG-UI

some user aware variation: 网上说的 ACP 好像有两个，一个 IBM 的 Agent Communication Protocol，一个 Zed 的 Agent Client Protocol，是不是一回事？还有人说 MCP 的 SSE 传输已经废弃了


起码先把这 4 个讲清楚，然后 OpenAI、Anthropic、Google、微软这些大厂各自支持哪些协议、有没有自家变体


以及其他用户需要知道的问题（鉴权、版本、谁在治理、怎么选）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长

---
外层说明（Claude Code，benchmark 固定设置）：
- 参数：--rounds 3 --workers 6 --budget 9000。
- skill 目录是 .claude/skills/deep-search。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。
- 工人用 subagent_type "research-worker"（模型已由外层固定，不要传 model）。
- 检索：工人用 WebSearch 找页面，再用 WebFetch 打开一手页面取原句。本次运行没有 pplx-safe。
- 当前目录之外的文件与本任务无关，不要读。
