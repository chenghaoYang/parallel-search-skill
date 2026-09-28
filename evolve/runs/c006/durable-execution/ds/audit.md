# audit — 终审说明

预算耗尽，未派独立核验工人回原页。以下为核验状态自查：

## 已在 R2 回原页逐字核过（= confirmed）
- Restate server BSL 1.1/4 年转 Apache/仅禁托管竞品 — LICENSE 原文（r1-restate C15-18 + r1-scout C12）
- Inngest server SSPL+DOSP、SDK Apache — LICENSE.md/README（r1-inngest C10-12）
- Temporal server MIT；sdk-java Apache-2.0、其余 SDK MIT — LICENSE 文件逐个取（r2-temporal C21-28）
- Hatchet MIT — repo LICENSE（r1-hatchet C12）
- Inngest "each step completes exactly once"=step memoization 内部语义 — durable-endpoints 原句（r2-inngest C1-C5）
- Inngest 自托管二进制只打包 dev-server-ui、无 SAML/RBAC/audit — Makefile/.goreleaser（r2-inngest C9）
- Restate 同 endpoint 改码→RT0016 journal 兼容失败、仅两类 in-place 安全 — versioning 页原句（r2-restate C16-20）
- Hatchet 重试默认关（retries>0 才启用）— retry-policies 页（r2-hatchet C4）
- Hatchet 建 run 钉 workflow_version_id — schema SQL（r2-hatchet C1）
- Temporal action 分 8 类+豁免规则 — actions 页（r2-temporal C1-19）
- DBOS Conductor 专有闭源+回连验 license — conductor-license/hosting 文档（r2-dbos C9-10）
- DBOS Java GA 1.0.0、Postgres 14+（CLI 矩阵）— releases/maven/supported-databases.json（r2-dbos C1-6）
- Temporal TS 沙箱替换 Math.random 可直接用 — TS basics 页（r1-temporal C9）
- Hatchet "at least once" vs durable-tasks "exactly-once" 裁定 — 两页原句（r1-hatchet conflicts）

## 未逐条核验/仅单源
- 价格数字（Temporal $50/M 阶梯、Restate 套餐、Inngest executions、Hatchet $10/M、DBOS $99）均来自各 pricing 页一次抓取；Restate 价格取自 JS chunk。
- .NET/PHP/Ruby SDK 确定性细节、Inngest dashboard CEL 搜索门控性质、Hatchet 重分配是否校验版本、DBOS Cloud CPU 单价：见 report §5。
