# Taxonomy grid v1

v0→v1：分类轴不变（连接边界）。F2 内部增加状态注记「页面称已并入」，不新开家族。A2UI / UTCP / ANP / MCP Apps 仍是 leads，本轮不升格。厂商网格保持 ❓，scout 不进成稿。

## 分类轴

**这条协议接的是哪两个角色？**

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| F1 宿主 ↔ 工具与上下文 | MCP | 模型宿主接工具、资源、提示词 |
| F2 智能体 ↔ 智能体 | A2A；ACP-IBM（仓库称已并入 A2A） | 把任务交给另一个不透明的 agent |
| F3 客户端 ↔ 智能体进程 | ACP-Zed | 编辑器驱动 coding agent |
| F4 智能体 ↔ 用户界面 | AG-UI | 把运行过程投影成前端事件 |
| F5 厂商采纳 | V-OpenAI、V-Anthropic、V-Google、V-Microsoft | 不是新边界 |

轴仍解释得了主差异：能合并的是 F2 里的 IBM ACP→A2A；Zed ACP 留在 F3，所以同名不是同协议。

## 维度

协议 P：D1 边界（谁和谁）· D2 对象（线上原名）· D3 传输 · D4 状态放在哪 · D5 发现 · D6 鉴权 · D7 版本与弃用 · D8 治理 · D9 和相邻协议的关系。

厂商 V：V1 官方点名支持谁 · V2 自家变体 · V3 产品里的传输/鉴权限制 · V4 治理角色。

## 网格 P

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| MCP | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| A2A | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ACP-IBM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ⚔ |
| ACP-Zed | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| AG-UI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

格注（不升成 ⚔ 的原因：反方没有 quote）：

- MCP D3/D4/D7：废弃起点、`initialize` 删除、header 全名，部分只有 changelog 概括句，R2 反证。
- MCP D9：✅ 只覆盖「spec 写灵感来自 LSP」。站内是否提到 A2A 仍是 ❓（索引未见，未逐页）。
- A2A D2/D4：方法全表、TaskState 全表主张写了，quote 只盖住一部分。
- A2A D7：站上 Latest 1.0.0 有 quote；笔记称 GitHub 有 v1.0.1，但 quote 未含该 tag，不标 ⚔。
- ACP-IBM D7：openapi `0.2.0` 与 tag `v1.0.3` 都有 quote。
- ACP-IBM D8：✅ 覆盖 2025-03 推出与 LF AI & Data。新闻稿「April 29, 2025」没有进 quote。
- ACP-IBM D9：banner/讨论帖写并入 A2A，首页正文仍用现在时。
- ACP-Zed D3：✅ 覆盖 stdio 与 Streamable HTTP draft。Intro 的 HTTP/WebSocket 句没有 quote。
- AG-UI D2：✅ 覆盖 spec 1.0 的 31 个事件。「约 16」写在 conflicts，没有 quote。

## 网格 V

| 实体 | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| V-OpenAI | ❓ | ❓ | ❓ | ❓ |
| V-Anthropic | ❓ | ❓ | ❓ | ❓ |
| V-Google | ❓ | ❓ | ❓ | ❓ |
| V-Microsoft | ❓ | ❓ | ❓ | ❓ |

## 待反证再留在「一屏看懂」的边界主张

1. HTTP+SSE **传输**自 2025-03-26 起 deprecated，且其后版本没有把它加回标准传输。
2. 2026-07-28 删除 `initialize` 握手，且没有更晚的规范把它加回来。
3. 两个 ACP 没有官方页把它们说成同一个协议；IBM ACP 并入 A2A 之后没有官方页宣布恢复独立开发。
4. AG-UI 规范「defines no credential」没有被另一页的标准鉴权方案打脸。
