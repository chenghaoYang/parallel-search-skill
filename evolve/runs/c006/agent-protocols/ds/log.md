# log

R0：定框架。分类轴 =「协议连接哪两端」→ 4 家族（模型↔工具、agent↔agent、客户端↔agent、UI↔agent）。8 个维度（连接面/治理/传输/抽象/鉴权/版本/大厂支持/实现）。疑点：两个 ACP 是否一回事；MCP SSE 是否废弃。

R1 计划（6 spawn）：
- r1-mcp：modelcontextprotocol.io 全维度，重点 SSE 废弃、OAuth、版本时间线
- r1-a2a：a2a 官方站 + github，全维度
- r1-acp2：两个 ACP 对比（IBM agentcommunicationprotocol.dev / BeeAI + Zed agentclientprotocol.com），回答疑点 1
- r1-agui：ag-ui.com / CopilotKit docs
- r1-vendors：OpenAI/Anthropic/Google/MS 各自支持哪些协议、自家变体（Apps SDK、Copilot Studio、ADK 等）
- r1-scout：范围内漏掉的协议/坑（ANP、MCP-UI、AGENTS.md、A2A 合并 ACP 史、其他「ACP」同名物），只产 leads

R1 已发出 6 spawn，等整批完成通知。

## R1 收束
- 6 工人全返回，123 claims（122 official）。lint 见上。grid 37/40 ✅。
- taxonomy v0→v1：分类轴不变（连接哪两端）；新增家族「商务/支付」（OpenAI/Stripe ACP、AP2、UCP、x402）与「非协议约定」（AGENTS.md、Skills、NLWeb）——scout 发现 ACP 同名物共 4 个，是最大新信息。
- 疑点结论：①两个 ACP 不是一回事（实际有 4 个）；②SSE 废弃=HTTP+SSE 传输被 Streamable HTTP 取代，SSE 机制仍在。
- report v1 = 8983 字符（预算 9000）。
- R1 观察：核心格子基本 ✅；剩余风险集中在 6 条边界主张（grid B1–B6）→ 动作：R2 定向反证/补全 5 spawn。

## R2 收束
- 5 工人全返回，71 claims（全 official）。裁决：B1 维持并强化（AG-UI spec 明文"defines no credential"；WS 无 normative binding 但有 schema flag）；B2 维持（adapter 迁至 agentclientprotocol org、远程传输仍 draft RFD、wire v1）；B3 全填（Apps SDK built on MCP 拿到 openai.com 原句；A2A 不内建有 2026-08 更新表态；AG-UI 官方拒绝）；B4 填（HTTP+SSE 具备移除资格≈2026-08 但尚未移除；版本号=最后破坏性变更日）；B5 推翻（Anthropic 有 A2A webinar + AG-UI quickstart PR）；B6 填（Foundry A2A v1.0 GA 有限制、Copilot Studio 2026-04 GA、Windows ODR）。
- taxonomy 不变；矩阵按新证据更新（Anthropic/OpenAI 行改正）。
- report v2 = 8916 字符。变化：新增 OpenAI/Anthropic 细粒度表态、微软 GA 细节、deprecated 移除时间表；删除：Plugins 行、Interactions API、维度图例行。
- R2 观察：核心格全 ✅；进一屏/疑点的边界主张均已反证 → 动作：终审（2 核验工人回原页核对一屏+疑点+坑的关键事实），然后停。
