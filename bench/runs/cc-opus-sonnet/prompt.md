/deep-search 产出文档 帮用户了解llm时代有关api 请求协议上的不同

seed keywords: chat completions.  Responses messages. Google genre atecontent协议

some user aware variation: deepseek 官方的response协议或许跟openai 官方释放docs中有很多不同


起码先4个主流，然后下游其他模型厂适配有什么不同，例如智谱的message对比Anthropic官方的不同


以及其他用户需要知道的问题


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长

---
外层说明（Claude Code，benchmark 固定设置）：
- skill 目录是 .claude/skills/deep-search。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。
- 工人用 subagent_type "research-worker"（模型已由外层固定，不要传 model）。
- 检索走 Perplexity：在每份简报里写明工人用 `.claude/skills/deep-search/scripts/pplx-safe search "<query>" --json --timeout 180` 检索（每个工人最多 4 次），再用 WebFetch 打开引用里的一手页面取原句。本次运行没有 WebSearch。
- 当前目录之外的文件与本任务无关，不要读。
