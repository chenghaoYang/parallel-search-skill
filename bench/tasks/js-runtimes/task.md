产出文档 帮用户了解 Node.js、Deno、Bun 这几个 JavaScript 运行时现在有什么不同

seed keywords: Node.js. Deno 2. Bun. TypeScript

some user aware variation: 听说 Node 现在也能直接跑 .ts 文件了，是不是和 Deno、Bun 一样完整支持 TypeScript？Deno 2 是不是已经能直接用 npm 包和 package.json 了？


起码先这 3 个，然后说清它们在 TypeScript 支持、包管理与 npm 兼容、权限/安全模型、内置工具链（测试、打包、格式化）上的差异


以及其他用户需要知道的问题（迁移、部署平台支持、兼容性坑）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长
