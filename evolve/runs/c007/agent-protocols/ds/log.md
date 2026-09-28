# log

## R0
框架：主分类轴=协议连接哪两端（agent↔tool / agent↔agent / client↔agent / agent↔UI），
10 维度 D1–D10 + 大厂立场子表 + 疑点判定格。
R1 计划（6 spawn）：mcp-core, a2a, acp-dual, ag-ui, vendors, scout。

待查：
- 分层组合说法（AG-UI→A2A→MCP 三层栈）官方出处
- MCP 治理：是否仍 Anthropic 独有 vs 基金会
- A2A 是否 1.0 GA

## R1 收束
6/6 工人返回，133 claims（131 official）。两大疑点均已判定：两个 ACP 非同一协议且实为 3–4 个缩写撞车；MCP HTTP+SSE 确已废弃（2025-03-26 起）。
taxonomy v0→v1：分类轴成立，新增 F5 交易家族；周边协议收敛为消歧内容。
report.r1 = 8235 chars（预算 9000），grid 89%。
R1 观察：一屏看懂含 3 条否定主张（Anthropic/OpenAI 未支持 A2A、AG-UI spec 不定义鉴权、Zed ACP 无鉴权）未反证；AGNTCY ACP 现状、MCP Apps spec 状态、SEP-2596 状态是缺口 → 动作：R2 派 4 个反证/定向工人 → 预计 spawn：4

## R2 收束
4/4 返回，54 claims。反证结果：「Zed ACP 无鉴权」被推翻（v1 有 authenticate/authMethods/logout，v2 草案 auth/login）；「Anthropic 未表态」被推翻一半（官方 A2A webinar + AG-UI quickstart，但无产品级声明）；「AG-UI 不定义鉴权」「OpenAI 未见 A2A/AG-UI」成立。
新增：AGNTCY ACP 2026-04 静默归档（第 4 个 ACP 也死了）；MCP Apps=SEP-1865 Final；SEP-2596 Final→SSE 移除窗口已到；Registry=preview。
report.r2 = 8980 chars（压缩了 ~750）。grid ∅ 格经反证后改判。
R2 观察：核心格子已 ✅/∅，边界主张已反证并修正 → 动作：终审，派 4 个核验工人按域回原页核对一屏/疑点/坑主张 → 预计 spawn：4

## R3 终审
4 核验工人回原页，32 判定项：29 confirmed / 1 wrong / 2 走样（已按原句改正：MAF×AG-UI 措辞、Foundry GA 页 MCP 半句、Apps SDK 页措辞、ACP repo URL 迁移）。audit.md 已汇总。
report.r3 = ≤9000 chars，已同步到 ./report.md。流程结束。
