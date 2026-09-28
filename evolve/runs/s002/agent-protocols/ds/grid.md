# Taxonomy 网格 v2

v1→v2：主轴仍是对话两端，辅轴仍是工作单元。新增观察：缩写 ACP 跨接缝，不能当家族。报告里的「商业」一行是厂商协议（Agentic Commerce Protocol、UCP），不给它们开 D1–D9 空行。AGNTCY 的 Agent Connect Protocol 只进疑点，不进实体表（规范仓已归档，细节未展开）。

IBM ACP 仍是 A2A 的同层前身，不是在营的第二套互操作协议。

## 实体 × 维度

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| A2A | ✅ | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ |
| ACP-IBM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚔ |
| ACP-Zed | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| AG-UI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

D3 MCP：HTTP+SSE 传输 = Deprecated，不是 Removed。SEP-2596 页为 Final。兼容旧端点的小节仍在，原文 can maintain。`Accept` 仍须同时列出 JSON 与 `text/event-stream`。

D5 ACP-IBM：生产文档有 Basic/Bearer/JWT。OpenAPI 是否写 securitySchemes 仍是 grep，不是原句。正文未再展开。

D6 A2A：规范站 1.0.0；GitHub release v1.0.1（2026-05-26）写了 spec 修复。

D6 ACP-Zed：v2 草案公告日 2026-07-20 仍在笔记里，这一稿正文为了长度没有展开。

D9 ACP-IBM：合并公告与归档 vs 未更新的对比页。

D9 MCP：自定位有原句。规范未点名另外四个名字。

## 厂商 × 协议

| 厂商 | MCP | A2A | ACP-IBM | ACP-Zed | AG-UI | 自家变体 |
|---|---|---|---|---|---|---|
| OpenAI | ✅ | ✅ | ∅ | ∅ | ∅ | ✅ |
| Anthropic | ✅ | ∅ | ∅ | ∅ | ∅ | ✅ |
| Google | ✅ | ✅ | ∅ | ∅ | ✅ | ✅ |
| Microsoft | ✅ | ✅ | ∅ | ∅ | ✅ | ✅ |

∅ = 已查的开发文档枢纽没有出现该全名，不是「全公司不支持」。OpenAI 的 A2A 格是 SDK 维护者写明不放进核心 SDK，不是全产品扫描。

## 用户疑点

| 疑点 | 状态 | 结论槽 |
|---|---|---|
| IBM ACP 与 Zed ACP 是否同一协议 | ✅ | 全名、两端、仓库都不同。反证未找到等同页。另外还有 AGNTCY Agent Connect Protocol 与 OpenAI Agentic Commerce Protocol。 |
| MCP 的 SSE 传输是否已废弃 | ✅ | HTTP+SSE 传输 Deprecated，SSE 帧仍是 Streamable HTTP 的必需响应。SEP-2596 = Final。尚未 Removed。 |

状态：✅ 一手+原句；⚠ 只有二手；⚔ 来源冲突；❓ 缺口；∅ 官方未写（已定向查过）；— 不适用。
