产出文档 帮用户了解llm时代有关api 请求协议上的不同

seed keywords: chat completions.  Responses messages. Google genre atecontent协议

some user aware variation: deepseek 官方的response协议或许跟openai 官方释放docs中有很多不同


起码先4个主流，然后下游其他模型厂适配有什么不同，例如智谱的message对比Anthropic官方的不同


以及其他用户需要知道的问题


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长

---
外层说明（Grok Build，benchmark 固定设置）：
- 用 deep-search skill 完成上面的任务：先完整读取 .claude/skills/deep-search/SKILL.md（按需读 references/），严格按它执行。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。
- 工人用 spawn_subagent 派出，每次调用都必须显式传 model="grok-4.7"（外层固定的工人模型）。这个外层没有 research-worker 类型：把 .claude/skills/deep-search/agents/research-worker.md 的正文（工人规则和笔记格式）整段放进每份简报。一轮的所有工人在同一条消息里并行派出，再用一次 get_command_or_subagent_output 等全部返回后收束；不要用 sleep 或定时唤醒来等。
- 检索走 Perplexity：在每份简报里写明工人用 `.claude/skills/deep-search/scripts/pplx-safe search "<query>" --json --timeout 180` 检索（每个工人最多 4 次），再用 web_fetch 或 curl 打开引用里的一手页面取原句。不要用内置的网页搜索工具。
- 当前目录之外的文件与本任务无关，不要读。
