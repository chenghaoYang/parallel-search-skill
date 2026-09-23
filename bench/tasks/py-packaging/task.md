产出文档 帮用户了解现在 Python 的包管理/项目管理工具有什么不同，新项目该怎么选

seed keywords: uv. pip. Poetry. PDM. pixi / conda

some user aware variation: 听说 Python 终于有标准锁文件了（PEP 751，pylock.toml），uv 和 pip 是不是都已经支持？Poetry 2 是不是也改用标准的 [project] 表了？


起码先这 5 个，然后讲清楚它们在锁文件、workspace/monorepo、Python 版本管理、构建后端上的做法有什么不同


以及其他用户需要知道的问题（从老工具迁移、CI 缓存、私有源）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长
