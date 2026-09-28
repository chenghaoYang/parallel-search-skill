# r2-counter-sse
question: 反证/收紧「2026-07-28 中 HTTP+SSE 是 Deprecated 非 Removed；标准传输仅 stdio+Streamable HTTP；客户端仍 MUST 双 Accept；传输页不再要求兼容 2024-11-05 HTTP+SSE；SEP-2596 尚未 Final 故移除日未到」
checked: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | https://modelcontextprotocol.io/specification/2026-07-28/deprecated | https://modelcontextprotocol.io/specification | https://modelcontextprotocol.io/seps | https://modelcontextprotocol.io/seps/2596-spec-feature-lifecycle-and-deprecation | https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2596 (+api.github.com pulls/2596) | https://api.github.com/repos/modelcontextprotocol/specification/contents/schema | https://modelcontextprotocol.io/specification/2025-06-18/basic/transports | https://modelcontextprotocol.io/specification/draft/basic/transports | https://modelcontextprotocol.io/specification/draft/basic/transports/streamable-http

## claims
- [C1] SEP-2596 状态为 **Final**，推翻「尚未 Final」 | src: https://modelcontextprotocol.io/seps/2596-spec-feature-lifecycle-and-deprecation | quote: "**Status** | Final … This SEP has reached Final status" | type: official
- [C2] SEP 索引同列 Final（Summary: Final: 42；行内 badge "Final"） | src: https://modelcontextprotocol.io/seps | quote: "SEP-2596 … Specification Feature Lifecycle and Deprecation Policy … Final" | type: official
- [C3] PR #2596 已合并并打 "final" 标签（"SEP finalized."），merged_at=2026-05-18T18:09:21Z → 三个月宽限期约至 2026-08-18，早于今天（2026-09-24）：HTTP+SSE 已**具备**移除资格 | src: https://api.github.com/repos/modelcontextprotocol/modelcontextprotocol/pulls/2596 | quote: "\"merged_at\":\"2026-05-18T18:09:21Z\" … \"name\":\"final\",\"description\":\"SEP finalized.\"" | type: official
- [C4] 但移除不自动发生；HTTP+SSE 仍 Deprecated | src: https://modelcontextprotocol.io/specification/2026-07-28/deprecated | quote: "the actual removal is a Core Maintainer decision taken during release preparation and may happen later … No features have been removed under this policy yet." | type: official
- [C5] registry 行确认 HTTP+SSE：Deprecated in `2025-03-26`，迁移路径 Streamable HTTP | src: https://modelcontextprotocol.io/specification/2026-07-28/deprecated | quote: "HTTP+SSE transport | SEP-2596 | `2025-03-26` | Streamable HTTP | Three months after SEP-2596 reaches Final" | type: official
- [C6] 反证「传输页不再提兼容」：2026-07-28 streamable-http 页仍保留 "### HTTP+SSE Transport (2024-11-05)" 小节 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "Clients and servers can maintain backward compatibility with the deprecated HTTP+SSE transport (from protocol version 2024-11-05) as follows:" | type: official
- [C7] 该措辞 2025-06-18 即为可选级（"can maintain"，"wanting to"），从未是 MUST | src: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports | quote: "Clients and servers can maintain backwards compatibility with the deprecated HTTP+SSE transport … as follows:" | type: official
- [C8] 2026-07-28 标准传输仅两项 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | quote: "The binding pages specify the standard transports: 1. stdio … 2. Streamable HTTP" | type: official
- [C9] 客户端 MUST 双接受仍在 | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | quote: "The client **MUST** include an `Accept` header listing both `application/json` and `text/event-stream`" + "The client **MUST** support both." | type: official
- [C10] Warning 框：HTTP+SSE "has been deprecated since protocol version `2025-03-26` and is classified as Deprecated under the feature lifecycle policy (SEP-2596) … It is eligible for removal in a future revision" | src: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | type: official
- [C11] draft 版传输页与 streamable-http 页仍只列 stdio+Streamable HTTP 且仍含同一 HTTP+SSE 兼容小节 → 移除尚未落入 draft | src: https://modelcontextprotocol.io/specification/draft/basic/transports/streamable-http | quote: "Clients and servers can maintain backward compatibility with the deprecated HTTP+SSE transport" | type: official
- [C12] 无更新正式版：仓库 schema/ 目录仅 2024-11-05、2025-03-26、2025-06-18、2025-11-25、2026-07-28、draft；spec 首页以 schema/2026-07-28/schema.ts 为权威 | src: https://api.github.com/repos/modelcontextprotocol/specification/contents/schema + https://modelcontextprotocol.io/specification | quote: "based on the TypeScript schema in schema/2026-07-28/schema.ts" | type: official

## conflicts
- vs「SEP-2596 尚未 Final，所以移除日未到」：SEP-2596 = Final（C1/C2/C3，PR 2026-05-18 合并）。三个月宽限期约 2026-08-18 已届满——HTTP+SSE 现已 eligible for removal；仍为 Deprecated 的原因是移除须 Core Maintainer 在下次发版时执行（C4），而非 SEP 未 Final。
- vs「这一版传输页不再要求实现去兼容 2024-11-05 的 HTTP+SSE」：字面成立（两版均 "can maintain"，无 MUST，C7），但若暗示兼容指引被删除则错误——2026-07-28 乃至 draft 仍完整保留该小节（C6/C11）。建议改写为「兼容指引仍在，且自始为可选而非强制」。

## gaps
- SEP-2596 「reaches Final」的精确日期站点未单列，以 PR merge 2026-05-18 为代理；宽限届满日 ≈2026-08-18 为推算。
- 下一正式版发版时间未知，无法断言 HTTP+SSE 何时真正 Removed。

## leads
- 监视 https://modelcontextprotocol.io/specification/draft/deprecated 的 Removed 区与 draft changelog「Removed」标题，捕捉 HTTP+SSE 实际移除。
- PR #2596 属 milestone「2026-07-28-RC」（已关闭）。
