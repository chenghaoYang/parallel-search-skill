# r2-openai
question: ①Apps SDK built on MCP 一手原句；②OpenAI 对 A2A 最新官方立场；③OpenAI 对 AG-UI / Zed ACP 有无官方表态
checked: https://developers.openai.com/apps-sdk/, https://developers.openai.com/plugins, https://openai.com/index/agentic-ai-foundation/, https://openai.com/index/introducing-apps-in-chatgpt/, https://github.com/openai/openai-apps-sdk-examples, https://github.com/openai/openai-agents-python/issues/472, https://github.com/openai/openai-agents-python/issues/1374, https://github.com/openai/openai-agents-python/issues/855, https://github.com/openai/openai-agents-js/issues/70, https://github.com/openai/codex/issues/11980, https://github.com/openai/codex (codex-rs dir listing)

## claims
- [C1] Apps SDK built on MCP（DevDay 公告，原文 2025-10-06，页面标注 Update on November 13, 2025）| src: https://openai.com/index/introducing-apps-in-chatgpt/ | quote: "The Apps SDK builds on the Model Context Protocol (MCP), the open standard that lets ChatGPT connect to external tools and data. It extends MCP so developers can design both the logic and interface of their apps." | type: official
- [C2] 同页另句："we're releasing as an open standard built on the Model Context Protocol (MCP)" | src: https://openai.com/index/introducing-apps-in-chatgpt/ | type: official
- [C3] AAIF 公告页确认 MCP 是 ChatGPT apps 的基础 | src: https://openai.com/index/agentic-ai-foundation/ | quote: "We've also been early adopters and core contributors to the Model Context Protocol (MCP), incorporating it as the foundation for connectors and apps in ChatGPT." | type: official
- [C4] 官方 examples 仓库 README（pushed 2026-04-15）：Apps SDK 内 MCP 同步 server/model/UI | src: https://github.com/openai/openai-apps-sdk-examples | quote: "Within the Apps SDK, MCP keeps the server, model, and UI in sync." | type: official
- [C5] developers.openai.com/apps-sdk/ 现已 301 重定向至 /plugins；新页 tagline | src: https://developers.openai.com/plugins | quote: "Build and publish plugins with skills, MCP servers, and optional UI." | type: official
- [C6] A2A 立场原话（维护者 seratch，2025-08-01，issue #472）| src: https://github.com/openai/openai-agents-python/issues/472 | quote: "We don't have immediate plans to add this feature, but we will continue to listen to the community's needs." | type: official
- [C7] A2A 最新立场（seratch 关闭 issue，2026-08-05）：不内建，建议与 a2a-sdk 显式组合 | src: https://github.com/openai/openai-agents-python/issues/472 | quote: "At this point, we do not plan to add an SDK-owned A2A abstraction to the OpenAI Agents SDK. The two SDKs can already be composed at a small, explicit boundary." | type: official
- [C8] AAIF 公告全文 grep 无任何 A2A/agent2agent 字样；OpenAI 捐给基金会的是 AGENTS.md（"we're contributing AGENTS.md … to the foundation"），三家联创各捐一项：OpenAI=AGENTS.md、Anthropic=MCP、Block=goose | src: https://openai.com/index/agentic-ai-foundation/ | quote: "the AAIF co-founders will each be contributing a project to the foundation: Anthropic's Model Context Protocol (MCP) and Block's goose." | type: official
- [C9] AAIF 联创名单（页面未提"白金"等级）| src: https://openai.com/index/agentic-ai-foundation/ | quote: "co-founding the Agentic AI Foundation (AAIF) under the Linux Foundation, alongside Anthropic and Block, and with the support of Google, Microsoft, AWS, Bloomberg, and Cloudflare." | type: official
- [C10] AG-UI 官方拒绝（python SDK，seratch 2025-09-22 关 issue）| src: https://github.com/openai/openai-agents-python/issues/855 | quote: "As mentioned in this thread, we don't have plans to add this. While we'll be closing this issue, sharing the demos available in different repos would be greatly appreciated." | type: official
- [C11] AG-UI 官方拒绝（js SDK，seratch 关 issue）| src: https://github.com/openai/openai-agents-js/issues/70 | quote: "Since we don't plan to work on this idea, let us close this issue. Thanks again for sharing this idea!" | type: official
- [C12] Zed ACP：openai/codex 无 ACP 代码（codex-rs 下无 acp/a2a crate，仅 codex-mcp、rmcp-client）；唯一相关 issue #11980（社区请求给 Codex 加 ACP session 管理）被维护者 etraut-openai 以票数不足关闭（2026-05-10）| src: https://github.com/openai/codex/issues/11980 | quote: "This feature request hasn't received enough upvotes, so I'm going to close it." | type: official
- [C13] Codex 的 ACP 适配器是第三方维护（Zed 官方仓库 zed-industries/codex-acp，issue 评论所列），非 OpenAI 出品 | src: https://github.com/openai/codex/issues/11980 | quote: "FYI, there are these existing adapter implementations: https://github.com/zed-industries/codex-acp https://github.com/cola-io/codex-acp" | type: official
- [C14] Apps SDK 正在泛化为跨平台 MCP Apps（与 Anthropic、MCP-UI 合作，2025-11 下旬）| src: https://openai.com/index/agentic-ai-foundation/ | quote: "we announced a collaboration with Anthropic and MCP-UI to extend the Apps SDK to all MCP developers through MCP Apps" | type: official

## conflicts
- 无实质冲突。#472 早期"暂不内建"（C6）与 2026-08-05 关单表态（C7）一致且后者更新——立场从未变：不内建 A2A，但官方认可用 a2a-sdk 在边界处组合。

## gaps
- "OpenAI 是 AAIF 白金成员"：openai.com 公告页未提会员等级，只列联创/支持方名单；等级信息需 aaif.io 或 Linux Foundation 新闻稿（超出本次来源政策）。
- developers.openai.com/apps-sdk/ 原页面内容已随重定向消失（改名 Plugins），旧版"built on MCP"文档措辞不可考；现存等价物为 /plugins 页（不再用 Apps SDK 一词）。
- openai.com 主站正文从未出现 "A2A" 一词（已 grep AAIF 页全文；为单页否定，非全站证明）。
- openai-agents-python#1374 为 #472 重复单，创建次日关闭，无新增信息。

## leads
- zed-industries/codex-acp：Zed 维护的 Codex↔ACP 适配器（第三方，可用于 ACP 生态格）。
- MCP Apps：blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps/ —— Apps SDK 规范进入 MCP 官方生态，跨 ChatGPT 之外复用。
- Apps SDK 文档已更名 Plugins（developers.openai.com/plugins），grid 措辞或需同步。
