产出文档 帮用户了解现在 Python 的包管理/项目管理工具有什么不同，新项目该怎么选

seed keywords: uv. pip. Poetry. PDM. pixi / conda

some user aware variation: 听说 Python 终于有标准锁文件了（PEP 751，pylock.toml），uv 和 pip 是不是都已经支持？Poetry 2 是不是也改用标准的 [project] 表了？


起码先这 5 个，然后讲清楚它们在锁文件、workspace/monorepo、Python 版本管理、构建后端上的做法有什么不同


以及其他用户需要知道的问题（从老工具迁移、CI 缓存、私有源）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长

---
外层说明（Grok Build，benchmark 固定设置）：
- 用 deep-search skill 完成上面的任务：先完整读取 .claude/skills/deep-search/SKILL.md（按需读 references/），严格按它执行。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。
- 参数：--rounds 3 --workers 6 --budget 9000。
- 工人用 spawn_subagent 派出，每次调用都必须显式传 model="swe-2-shim"（外层固定的工人模型）。这个外层没有 research-worker 类型：把 .claude/skills/deep-search/agents/research-worker.md 的正文（工人规则和笔记格式）整段放进每份简报。一轮的所有工人在同一条消息里并行派出，再用一次 get_command_or_subagent_output 等全部返回后收束；不要用 sleep 或定时唤醒来等。
- 检索：工人用 web_search 找页面，再用 web_fetch 打开一手页面取原句。本次运行没有 pplx-safe。
- 当前目录之外的文件与本任务无关，不要读。
