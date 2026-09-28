# r2-verify-anthropic
question: 1) 现在（2026年）使用Claude的prompt caching/cache_control功能，是否仍需要在请求里带anthropic-beta之类的beta header？还是已经完全GA、不需要任何特殊header？2) Anthropic的prompt cache存储在服务端的介质是内存还是磁盘（或未公开）？
checked: https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/api/messages/create, https://platform.claude.com/docs/en/release-notes/overview, https://platform.claude.com/docs/en/api/beta-headers, https://claude.com/blog/token-saving-updates

## claims
- [C1] Prompt caching 已完全GA，不需要任何特殊header。 | src: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | quote: "Prompt caching is available on all active Claude models with no special headers required." | type: official
- [C2] 自动缓存（automatic caching）2026年2月19日推出时，未要求任何beta header。 | src: https://platform.claude.com/docs/en/release-notes/overview | quote: "Automatic Caching (February 19, 2026)" [发布说明中无提及beta header要求] | type: official
- [C3] Beta headers页面列出所有需要anthropic-beta header的功能，prompt caching未被列出。 | src: https://platform.claude.com/docs/en/api/beta-headers | quote: "The following examples show the same request with cURL, the `ant` CLI, and the SDKs, using the [context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing) beta as the example" [仅列举managed-agents、mcp-tunnels、agent-memory需要特定beta header，prompt caching不在其中] | type: official
- [C4] Messages API reference中关于Headers的部分只列出可选的anthropic-workspace-id和anthropic-user-profile-id，未提及cache_control需要任何header。 | src: https://platform.claude.com/docs/en/api/messages/create | quote: "anthropic-workspace-id (optional): Select workspace for multi-workspace credentials; anthropic-user-profile-id (optional): Attribute request to specific user (requires beta header)" | type: official

## conflicts
- 无直接冲突。上一轮C23主张引用的原句"Place cache_control directly on individual content blocks for fine-grained control over exactly what gets cached"确实是官方原文，但该引用无法支持"不需要额外开通或特殊请求头"的结论——该原句仅讲cache_control的位置。现在找到的新原句"Prompt caching is available on all active Claude models with no special headers required"才是正确的支持证据。

## gaps
- D1 存储介质官方文档：Anthropic官方文档（platform.claude.com、docs.anthropic.com）中未明确说明prompt cache的存储介质是内存、磁盘还是其他。第三方技术文章提到KV cache在GPU HBM/VRAM中，5分钟缓存可能在GPU内存，1小时缓存可能在node-local NVMe，但无官方原句支持。

## leads
- 第三方分析提到缓存存储策略可能分层：5分钟TTL用GPU HBM，1小时TTL用NVMe，但这需要官方澄清
- Claude Code engineering team提到"build our entire harness around prompt caching"并将cache miss视为生产事故，表明缓存对性能至关重要
