# r2-verify-anthropic-automatic
question: Anthropic 官方文档里 2026-02-19 发布的「自动缓存」到底是「不加任何缓存相关参数、完全零代码自动生效」，还是「仍需要在请求里加至少一个 cache_control 字段的简化版手动开启」？

checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching,https://platform.claude.com/docs/en/release-notes/overview

## claims
- [C1] 不加 cache_control 字段的请求**不会**自动缓存，必须显式添加至少一个 cache_control 字段才能启用缓存 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Requests without any cache_control fields do not get automatically cached. You must explicitly enable prompt caching by adding a cache_control field to your request." | type: official

- [C2] "自动缓存"的自动是指「系统自动决定断点位置」而非「完全不需要碰请求」：需在请求顶层添加单个 cache_control 字段，然后系统自动在最后一个可缓存块放置断点 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Add one cache_control field at the top level of your request. The system automatically places the cache breakpoint on the last cacheable block in your request" | type: official

- [C3] 自动缓存的核心优势是免去手动更新多个块上 cache_control 位置：对话增长时缓存点自动前移，无需修改代码 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Simplicity: No need to manually track or update cache_control markers as conversations evolve. The cache point moves forward without requiring code changes" | type: official

- [C4] 自动缓存和块级手动 cache_control 可共存，用户可选择其中一种方式或两者结合用于高级优化 | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "Can be combined with existing block-level cache control for advanced use cases. Automatic caching is a convenience feature for growing conversations where you want the system to handle cache breakpoint management automatically, rather than manually placing cache_control on individual blocks." | type: official

- [C5] 2026-02-19 发布说明：自动缓存通过在请求体中添加单个 cache_control 字段激活，系统无需用户手动管理多个缓存断点 | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "Add a single cache_control field to your request body. No manual breakpoint management needed" | type: official

## conflicts
- R1 的 C1 和 C2 看似矛盾但实则兼容：C1 描述缓存的激活方式（需加 cache_control 字段），C2 描述自动缓存的管理方式（系统自动决定断点位置）。矛盾的假象来自对"自动"字义的歧义——官方文档明确指"自动决定断点位置"而非"完全零代码"。

## gaps
- 文档未明确说明在多轮对话中，是否所有新请求都必须重复添加 cache_control 字段，还是首次添加后后续自动继承

## leads
- Anthropic 的"自动缓存"在操作层面上仍然需要显式加 cache_control 字段（哪怕只一个），本质上是"断点位置自动化"而非完全零代码自动化，与 OpenAI/DeepSeek 的完全无参数自动缓存有根本区别
