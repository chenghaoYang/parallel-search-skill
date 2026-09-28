产出文档 帮用户理清 agent 时代各种「协议」分别管什么、有什么不同

seed keywords: MCP (Model Context Protocol). A2A (Agent2Agent). ACP. AG-UI

some user aware variation: 网上说的 ACP 好像有两个，一个 IBM 的 Agent Communication Protocol，一个 Zed 的 Agent Client Protocol，是不是一回事？还有人说 MCP 的 SSE 传输已经废弃了


起码先把这 4 个讲清楚，然后 OpenAI、Anthropic、Google、微软这些大厂各自支持哪些协议、有没有自家变体


以及其他用户需要知道的问题（鉴权、版本、谁在治理、怎么选）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长

---
外层说明（Grok Build，benchmark 固定设置）：
- 用 deep-search skill 完成上面的任务：先完整读取 .claude/skills/deep-search/SKILL.md（按需读 references/），严格按它执行。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。
- 参数：--rounds 3 --workers 6 --budget 9000。
- 工人用 spawn_subagent 派出，每次调用都必须显式传 model="grok-4.7"（外层固定的工人模型）。这个外层没有 research-worker 类型：把 .claude/skills/deep-search/agents/research-worker.md 的正文（工人规则和笔记格式）整段放进每份简报。一轮的所有工人在同一条消息里并行派出，再用一次 get_command_or_subagent_output 等全部返回后收束；不要用 sleep 或定时唤醒来等。
- 检索：工人用 web_search 找页面，再用 web_fetch 打开一手页面取原句。本次运行没有 pplx-safe。
- 当前目录之外的文件与本任务无关，不要读。
