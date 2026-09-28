# r3-anthropic-tools
question: 不用用户自己放 cache_control 时，Anthropic server tools 会不会仍写入 prompt cache？是否推翻「启用缓存必须放 cache_control」？
checked: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching ; https://platform.claude.com/docs/en/build-with-claude/prompt-caching

## claims
- [C1] 请求已启用缓存且 Claude 使用 server tool（web search / web fetch / code execution）时，API 自动在 server tool 结果上放缓存断点 | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching | quote: "the API automatically places a cache breakpoint on the server tool result before running the next iteration of the agentic loop" | type: official
- [C2] 该自动断点固定用默认 5 分钟 TTL，计入 cache_creation.ephemeral_5m_input_tokens，即使用户自己的 cache_control 全用 1h | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching | quote: "This automatic breakpoint always uses the default 5-minute TTL, independent of any TTL you set on your own `cache_control` markers." | type: official
- [C3] 关键限定：仅当请求里已有至少一个 cache_control 标记才发生；未启用缓存的请求不会得到自动断点——即不放 cache_control 就不会有 server tool 缓存写入 | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching | quote: "This behavior only applies when your request already has at least one `cache_control` marker. Requests without prompt caching do not receive the automatic breakpoint." | type: official
- [C4] 主指南交叉引用确认：使用 server tools 时可能看到未主动请求的 ephemeral_5m 写入 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "If you see `ephemeral_5m_input_tokens` writes you didn't request while using server tools such as web search" | type: official
- [C5] 结论：不推翻「必须放 cache_control」。D1 例外只是：已启用缓存的请求内，server tool 会产生用户未显式放置的 5m 写入，用户无需改代码即可获得这部分缓存 | src: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching | quote: "This lets later iterations within the same request read the growing prefix from cache instead of reprocessing it." | type: official

## conflicts
- 无

## gaps
- 自动断点是否占用请求 4 个断点上限，页内未说明。
- 顶层 automatic caching（top-level cache_control）是否同样触发 server tool 自动断点未逐字说明（按「at least one cache_control marker」推断涵盖）。

## leads
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools
- https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics
