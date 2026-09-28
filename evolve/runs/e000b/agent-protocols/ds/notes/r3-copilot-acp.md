# r3-copilot-acp
question: GitHub Copilot CLI 对 ACP（Zed 的 Agent Client Protocol）的支持状态到底是什么？文档说 "public preview"，但 issue #222 显示未实现、已关闭、无分配开发者、无里程碑——这两者矛盾吗？
checked: https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server, https://github.com/github/copilot-cli/issues/222, https://github.blog/changelog/2026-01-28-acp-support-in-copilot-cli-is-now-in-public-preview/, api.github.com/repos/github/copilot-cli/issues/222

## claims
- [C1] GitHub Copilot CLI 对 ACP 的支持自 2026-01-28 起处于 "public preview" 状态 | src: https://github.blog/changelog/2026-01-28-acp-support-in-copilot-cli-is-now-in-public-preview/ | quote: "GitHub Copilot CLI now implements the Agent Client Protocol (ACP), an industry-standard protocol for communication between AI agents and clients." | type: official
- [C2] docs.github.com 的 ACP server 参考文档记载支持为"in public preview and subject to change" | src: https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server | quote: "ACP support in GitHub Copilot CLI is in public preview and subject to change." | type: official
- [C3] GitHub issue #222（"ACP support for Copilot CLI"）以 "completed" 原因关闭于 2026-01-30 | src: https://github.com/github/copilot-cli/issues/222 | quote: "closed_at: 2026-01-30T21:13:45Z, state_reason: completed" | type: official
- [C4] issue #222 关闭时，@devm33（GitHub 官方）评论"We have now shipped the ACP support in Copilot CLI to public preview!"并指向了 blog changelog | src: https://github.com/github/copilot-cli/issues/222 | quote: "We have now shipped the ACP support in Copilot CLI to public preview! https://github.blog/changelog/2026-01-28-acp-support-in-copilot-cli-is-now-in-public-preview/" | type: official
- [C5] 初始 ACP 支持于 2026-01-12 发货，用户可用 `--acp` flag 试用 | src: https://github.com/github/copilot-cli/issues/222 | quote: "@devm33: We have shipped initial support for ACP. While we are still iterating to close known gaps before announcing and adding docs, if you want to try it out and give feedback in the meantime, you can run with the `--acp` flag." | type: official
- [C6] Copilot CLI ACP 支持的启动方式为 `copilot --acp`（stdio）或 `copilot --acp --port 8080`（TCP）| src: https://github.blog/changelog/2026-01-28-acp-support-in-copilot-cli-is-now-in-public-preview/ | quote: "Standard input/output: copilot --acp; TCP connection: copilot --acp --port 8080" | type: official
- [C7] issue #222 的关闭并非"未实现"，而是功能已完成的正常关闭；当初提出者（@bdf369）请求 ACP 支持，GitHub 开发者随后实现并在 public preview 发布后关闭 issue | src: https://github.com/github/copilot-cli/issues/222 | quote: "Issue type: Feature Request, state_reason: completed" | type: official

## conflicts
（无）文档和 issue 不矛盾。issue #222 是特性请求，已在功能实现后标记为 "completed" 并关闭；文档正确反映了当前状态。

## gaps
- docs.github.com 上的 ACP server 页面未明确标注"从 Copilot CLI 哪个版本开始支持 ACP"
- docs.github.com 页面本身无可见的"最后更新日期"（仅 HTTP header 显示当前日期）

## leads
- Copilot CLI ACP 支持在 2026-01-28 由 GitHub 正式发布到 public preview；2026-01-30 issue #222 被标记为 "completed" 关闭
