# r2-google
question: Google Gemini Enterprise 文档里提到的「A2UI」和 CopilotKit 主导的「AG-UI」是什么关系——A2UI 是基于/兼容 AG-UI 的产品层，还是完全独立的另一套规范（有没有自己的事件格式/spec）？Google 对 ACP-Zed（Zed 的 Agent Client Protocol）有没有自己的官方表态（不只是 Zed 一侧说"Gemini CLI 是参考实现"）？
checked: developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/, github.com/google/A2UI, a2ui.org, developers.googleblog.com/a2ui-v0-9-generative-ui/, developers.googleblog.com/gemini-cli-is-now-integrated-into-zed/, github.com/google-gemini/gemini-cli, docs.cloud.google.com/gemini/enterprise/docs/a2ui-agents/register-and-manage-an-a2ui-agent

## claims
- [C1] A2UI 是 Google 开源项目，有独立的 GitHub 仓库 https://github.com/google/A2UI，采用 Apache 2.0 许可证 | src: https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/ | quote: "GitHub Access...available at github.com/google/A2UI...licensed under Apache 2.0" | type: official

- [C2] A2UI 有自己的协议规范和事件格式，采用声明式 JSON 格式，消息类型包括 createSurface, updateComponents, updateDataModel, deleteSurface | src: https://a2ui.org/ | quote: "protocol...four message types: createSurface, updateComponents, updateDataModel, and deleteSurface" | type: official

- [C3] A2UI 当前生产版本为 v0.9.1，v1.0 是候选发布版，v0.8 是遗留版本 | src: https://github.com/google/A2UI | quote: "v0.9.1 is the current production release...v1.0 is a release candidate" | type: official

- [C4] A2UI 支持多种传输方式：A2A Protocol、AG UI framework、MCP、Websockets、REST 等，不依赖于特定传输层 | src: https://developers.googleblog.com/a2ui-v0-9-generative-ui/ | quote: "A2UI over MCP, Websockets, REST, AG UI, A2A, or whatever you want" | type: official

- [C5] A2UI 与 AG-UI 是独立的、互补的两层规范，而非基于关系：A2UI 定义 UI 意图（what），AG-UI 是集成层（how） | src: https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/ | quote: "A2UI is...complementary to AG UI...AG-UI functions as an integration layer" | type: official

- [C6] Gemini CLI 在 github.com/google-gemini/gemini-cli 仓库中，支持 ACP 模式，使用 --acp 标志启动 | src: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/acp-mode.md | quote: "ACP is an open protocol that standardizes how AI coding agents communicate with code editors" | type: official

- [C7] Google 在 Developers Blog 上正式宣布 Gemini CLI 与 Zed 集成，Google 主动与 Zed 合作引入 Gemini CLI，而非 Zed 单方面实现 | src: https://developers.googleblog.com/gemini-cli-is-now-integrated-into-zed/ | quote: "Google integrated Gemini CLI directly into the Zed code editor...Google reached out to discuss bringing the Gemini CLI" | type: official

- [C8] Gemini CLI 是 ACP 兼容代理，在 ACP 代理注册表中列出，供 Zed 等编辑器发现 | src: https://github.com/google-gemini/gemini-cli | quote: "ACP-compatible agent...found in the ACP Agent Registry" | type: official

- [C9] A2UI 在 Gemini Enterprise 中通过 A2UI Protocol 与 A2A Protocol 配合使用，用于构建自定义代理 UI | src: https://docs.cloud.google.com/gemini/enterprise/docs/a2ui-agents/register-and-manage-an-a2ui-agent | quote: "using A2UI...and A2A Protocol for communication" | type: official

## conflicts
无

## gaps
- A2UI 规范文档的具体 HTTP endpoint 细节未从官方 GitHub 获取（WebFetch 返回 404）
- Google 对"Gemini CLI 是否为 ACP-Zed 的参考实现"这一说法的明确否定或确认未获得直接原文

## leads
- A2UI 官方规范文档可能在 https://github.com/google/A2UI/blob/main/specification/0.9/docs/a2ui_protocol.md，后续可通过 GitHub API 或 raw.githubusercontent.com 访问
- Gemini CLI 在 https://zed.dev/acp 上被列为正式的 ACP 代理实现
