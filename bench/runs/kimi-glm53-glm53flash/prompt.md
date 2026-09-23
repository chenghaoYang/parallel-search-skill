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
外层说明（Kimi Code，benchmark 固定设置）：
- 用 deep-search skill 完成上面的任务：先完整读取 .claude/skills/deep-search/SKILL.md（按需读 references/），严格按它执行。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。
- 工人用 subagent_type "research-worker"（模型由外层决定，不要传 model）。一轮的工人用一次 AgentSwarm（prompt_template 写 {{item}}，items 是各份完整简报）或同一步里多个前台 Agent 调用并行派出，等全部返回再收束；不要用后台任务、sleep 或定时唤醒来等。模型提供方限制并发：同时最多 3 个工人在跑，一轮工人多于 3 个就分批派，每批等返回后再派下一批。
- 检索走 Perplexity：在每份简报里写明工人用 `.claude/skills/deep-search/scripts/pplx-safe search "<query>" --json --timeout 180` 检索（每个工人最多 4 次），再用 FetchURL 或 curl 打开引用里的一手页面取原句。不要用内置的网页搜索工具。
- 当前目录之外的文件与本任务无关，不要读。
