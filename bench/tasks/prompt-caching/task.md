产出文档 帮用户搞清楚各家大模型 API 的 prompt caching（上下文缓存）有什么不同

seed keywords: OpenAI prompt caching. Anthropic cache_control. Gemini context caching / implicit caching. DeepSeek 上下文硬盘缓存

some user aware variation: 听说 OpenAI 和 DeepSeek 是自动缓存、不用改代码，Anthropic 必须手动打 cache_control 断点——现在还是这样吗？命中之后各家怎么计费、缓存能活多久好像也都不一样


起码先这 4 家，然后国内其他厂（Kimi、智谱、通义千问）和 OpenRouter 这类网关在缓存上有什么不同


以及其他用户需要知道的问题（怎么确认命中了、哪些改动会让缓存失效）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长
