/deep-search 产出文档 帮用户了解 Node.js、Deno、Bun 这几个 JavaScript 运行时现在有什么不同

seed keywords: Node.js. Deno 2. Bun. TypeScript

some user aware variation: 听说 Node 现在也能直接跑 .ts 文件了，是不是和 Deno、Bun 一样完整支持 TypeScript？Deno 2 是不是已经能直接用 npm 包和 package.json 了？


起码先这 3 个，然后说清它们在 TypeScript 支持、包管理与 npm 兼容、权限/安全模型、内置工具链（测试、打包、格式化）上的差异


以及其他用户需要知道的问题（迁移、部署平台支持、兼容性坑）


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
