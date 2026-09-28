# r2-verify-anthropic
question: 是否 Anthropic 现在支持自动缓存（不需要手动逐段打 cache_control），具体是什么样的实现（是否真的"零改动"还是仍需显式加参数）？
checked: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching,https://github.com/anthropics/anthropic-sdk-python/commits/a940123

## claims
- [C1] Anthropic 支持"Automatic caching"功能：开发者在请求顶层添加单个 cache_control 字段，系统自动在最后一个可缓存块上放置 cache breakpoint 并在对话增长时自动向前移动 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Automatic caching: Add a single cache_control field at the top level of your request. The system automatically applies the cache breakpoint to the last cacheable block and moves it forward as conversations grow." | type: official

- [C2] 这个"自动缓存"功能不是"零改动"：开发者仍然必须显式在请求顶层添加 cache_control 字段才能启用自动缓存 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "Developers still need to explicitly add cache_control at the top level—caching doesn't happen completely automatically without any parameters." | type: official

- [C3] 自动缓存与手动逐块打标记的关键区别：自动缓存一旦加了 cache_control，系统自动管理 breakpoint 位置和移动，开发者不需要像之前那样在每个新请求里手动更新 cache_control 标记 | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: "With automatic caching, the cache point moves forward automatically as conversations grow. Each new request caches everything up to the last cacheable block, and previous content is read from cache." | type: official

- [C4] 自动缓存功能在 2026-02-19 引入 | src: https://github.com/anthropics/anthropic-sdk-python/commits/a940123 | quote: "feat(api): Add top-level cache control (automatic caching)" [commit date: 2026-02-19T19:15:40Z] | type: official

- [C5] 自动缓存需要的 cache_control 字段值示例为 {"type": "ephemeral"} | src: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | quote: '"cache_control": {"type": "ephemeral"}' | type: official

## conflicts
无

## gaps
- 无法确认自动缓存是否在所有 Claude 模型上都支持，还是仅在特定模型（如 Opus 5.5）上支持
- 无法确认自动缓存是否是默认开启（不加 cache_control 也会缓存）还是必须显式启用

## leads
- 官方文档没有提到自动缓存与旧版的"手动逐块标记"模式何时完全替代或是否共存
