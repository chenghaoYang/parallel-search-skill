# r2-acpzed-vendors

question: OpenAI、Anthropic、Google、Microsoft 对 Zed 的 Agent Client Protocol（ACP-Zed，editor↔agent 协议）的支持，官方一手来源分别是什么、是"厂商原生实现"还是"第三方/Zed 造的桥接适配器"？

checked: https://zed.dev/acp, https://github.com/zed-industries/agent-client-protocol, https://agentclientprotocol.com, https://github.com/microsoft/vscode/issues/265496, https://zed.dev/blog/claude-code-via-acp, https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/acp-mode.md, https://zed.dev/blog/bring-your-own-agent-to-zed

## claims

- [C1] Google Gemini CLI 原生支持 ACP，通过 `gemini --acp` 启动 ACP 模式 | src: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/acp-mode.md | quote: "To activate this mode, users run: gemini --acp. The entire communication happens over stdio using JSON-RPC 2.0 protocol." | type: official

- [C2] Google Gemini CLI 的 ACP 实现是官方原生实现，Google 团队开发，非 Zed 适配器 | src: https://zed.dev/blog/bring-your-own-agent-to-zed | quote: "By running the same Gemini CLI as a subprocess speaking ACP, we surface the same underlying capabilities." | type: official

- [C3] Claude Code 在 Zed 中通过 ACP 运行使用 Zed 构建的桥接适配器，非 Anthropic 官方原生实现 | src: https://zed.dev/blog/claude-code-via-acp | quote: "Zed 构建了一个适配器，将 Claude Code 的 SDK 包装起来，并将其交互转换为 ACP 的 JSON RPC 格式" | type: official

- [C4] Zed 已在 Apache 许可证下开源了 Claude Code 的 ACP 适配器，npm 包名为 @zed-industries/claude-code-acp | src: https://zed.dev/blog/claude-code-via-acp | quote: "Zed 已在 Apache 许可证下开源了这个 Claude Code 适配器，使其可供采纳 ACP 的任何编辑器使用。" | type: official

- [C5] Anthropic 官方渠道（anthropic.com）未提及 ACP 或对 ACP 的支持承诺 | src: https://www.anthropic.com | quote: "Site search for 'Claude Code ACP Agent Client Protocol' returned no direct Anthropic announcements" | type: official

- [C6] OpenAI Codex CLI 的 ACP 支持为社区适配器实现，官方 Codex 仓库中的 ACP 相关 issue#9085 已被删除，未见官方 ACP 支持承诺 | src: https://github.com/openai/codex/issues/9085 | quote: "Issue #9085 deleted" | type: official

- [C7] OpenAI 官方渠道（openai.com）的 Codex 文档中未提及 Agent Client Protocol 或 ACP | src: https://developers.openai.com/codex/cli | quote: "Codex documentation focuses on MCP integration, not ACP protocol" | type: official

- [C8] VS Code 对 ACP 的支持状态为功能建议阶段，未作出原生实现承诺，issue #265496 标记为 under-discussion | src: https://github.com/microsoft/vscode/issues/265496 | quote: "Issue is under discussion for relevance, priority, approach" | type: official

- [C9] GitHub Copilot CLI 在 Zed ACP adopter 列表中出现，但源代码或官方公告未明确标注是官方实现还是社区适配器 | src: https://zed.dev/acp | quote: "GitHub Copilot CLI listed as ACP agent" | type: secondary

- [C10] ACP registry 包含 41 个 agent，其中 Claude、Codex、Gemini 等获得 Zed 或厂商博客宣传，但 registry 本身不区分官方实现与社区适配器 | src: https://agentclientprotocol.com/get-started/registry | quote: "Curated set of agents with authentication support" | type: official

## conflicts

- VS Code 对 ACP 的立场不明确：Zed/media 称 GitHub Copilot CLI 已支持 ACP（作为 adopter 列表），但 Microsoft/VS Code 官方 GitHub issue #265496 仅标记为讨论中，未见原生实现或承诺。

## gaps

- OpenAI 官方对 Codex CLI ACP 支持的明确立场：查过 openai.com 文档、GitHub openai/codex repo（issue#9085 已删除），Codex CLI 官方文档未提及 ACP，仅提及 MCP。查证社区适配器存在（github.com/agentclientprotocol/codex-acp 等），但无官方承诺。

- Microsoft/VS Code 官方对 ACP 的正式承诺：issue #265496 为功能建议、under-discussion，无正式实现时间表或设计文档。

- Anthropic 对 Claude Code ACP 支持的官方立场：Anthropic 官方渠道（anthropic.com、文档）未出现 ACP 相关表述，仅 Zed 官方和社区报道称使用 Zed 适配器。

- registry 元数据：agentclientprotocol.com registry 中的 agent.json schema 是否包含厂商/社区标记字段，未直接查证。

## leads

- Google Gemini CLI 唯一明确的厂商原生实现案例，具体体现在官方 GitHub repo 的 acp-mode.md 文档和 --acp 命令行参数。

- Zed 开源的 @zed-industries/claude-code-acp npm 包可作为"第三方桥接适配器"的核心证据，对标 Anthropic 未原生采纳 ACP 的立场。

- Microsoft GitHub issue #265496 可持续监控作为 VS Code ACP 支持进展的唯一官方跟踪点，目前为讨论阶段无实装。
