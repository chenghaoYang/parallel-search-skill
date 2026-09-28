# r2-license
question: 反证三条「自托管/许可证无限制」边界主张 + 补 Restate 官方定价数字（Restate×D3 / Inngest 自托管缺口 / Temporal cloud 独占）
checked: https://restate.dev/pricing (via https://r.jina.ai/https://restate.dev/pricing 镜像), https://www.inngest.com/docs/self-hosting, https://www.inngest.com/docs/platform/monitor/insights, https://docs.temporal.io/cloud, https://docs.temporal.io/cloud/manage-access/saml, https://docs.temporal.io/cloud/audit-logs, https://docs.temporal.io/evaluate, https://docs.temporal.io/evaluate/cloud, https://docs.temporal.io/security, https://docs.restate.dev/cloud/getting-started, https://docs.restate.dev/byoc/overview, https://docs.restate.dev/cloud/connecting-services(搜索快照), https://docs.restate.dev/server/monitoring/tracing(搜索快照)

## claims
- [C1] Restate Cloud Free 档 $0：含 100k actions、10 actions/s（burst 100/s）、1 GB Virtual Object 存储、1 天 history retention、社区支持 | src: https://restate.dev/pricing | quote: "100k actions … 10 actions/sec … 1 GB … 1-day … Community (Discord / Slack)" | type: official
- [C2] Starter 档 "$75 per month"（Most popular）："5M actions"、超量 "$25 / million"、50 actions/s（burst 500/s）、5 GB、3 天 retention、SLA "99.9%" | src: https://restate.dev/pricing | quote: "$75 per month … 5M actions … $25 / million … 99.9%" | type: official
- [C3] Business 档 "$300 per month"："20M actions"、200 actions/s（burst 1,000/s）、20 GB、7 天 retention、"Email (Business Hours)"；付费加购 "HIPAA BAA + $300"、"Multi-AZ redundancy + $200" | src: https://restate.dev/pricing | quote: "$300 per month … 20M actions … HIPAA BAA + $300 … Multi-AZ redundancy + $200" | type: official
- [C4] Premium 档 "$1,000 per month"："50M actions"、超量 "$15 / million"、500 actions/s（burst 2,000/s）、50 GB、30 天 retention、"Dedicated Slack Channel (Business hours, 2h response)"、"99.9% (99.99% multi-AZ)"、Multi-AZ "+ $500" | src: https://restate.dev/pricing | quote: "$1,000 per month … 50M actions … $15 / million" | type: official
- [C5] Enterprise 档 "Custom"：吞吐 "Up to 100,000s actions/sec"、"Enterprise Support (P0 24/7, 30 min response)"、"99.99%"；存储超量统一 "$0.5 per added GB/month" | src: https://restate.dev/pricing | quote: "Custom volume, dedicated support, security & legal review … Up to 100,000s actions/sec" | type: official
- [C6] Restate Cloud 计费单位：每次调用计 2 actions + 中间步骤，负载每 64KiB 计 1 action | src: https://restate.dev/pricing | quote: "Durable actions are the basic unit of accounting in Restate Cloud … one action per started 64KiB of data" | type: official
- [C7] 定价页对比表存在以下行：Client-side Encryption、OTEL exports、SAML SSO / SCIM、Security review MSA legal redlining（各档勾选未渲染，归属档位未确认） | src: https://restate.dev/pricing | quote: "Client-side Encryption … OTEL exports … SAML SSO / SCIM" | type: official
- [C8] Restate BYOC：环境创建/更新/扩缩由 Restate 控制面托管 —— 控制面属 Cloud/BYOC 专属，自托管无 | src: https://docs.restate.dev/byoc/overview | quote: "Environment creation, updates, and scaling are managed by Restate's control plane." | type: official
- [C9] Restate 环境日志仅经 Cloud console 提供 | src: https://docs.restate.dev/byoc/overview | quote: "Authenticated customers can access environment logs through the Restate Cloud console." | type: official
- [C10] 自托管 Restate 支持 OTLP trace 导出（`tracing-endpoint` 配置项，otlp+http/https scheme，Jaeger 4317/4318）—— 即 server 本身无 OTEL 阉割 | src: https://docs.restate.dev/server/monitoring/tracing | quote: "Exporting traces to OTLP-compatible systems (e.g. Jaeger) … Set up the OTLP exporter by pointing the configuration entry `tracing-endpoint`" | type: official
- [C11] Client-side encryption 为 SDK 侧功能（`JournalValueCodec`），文档自述"only available in the TypeScript SDK"，非 Cloud 专属功能 | src: https://docs.restate.dev/cloud/connecting-services | quote: "You need to implement a `JournalValueCodec` … Currently, this feature is only available in the TypeScript SDK." | type: official
- [C12] Inngest 自托管默认 SQLite「不支持单节点以外扩缩」，多节点需自配 Postgres | src: https://www.inngest.com/docs/self-hosting | quote: "This is convenient for zero-dependency deployments, but does not support scaling beyond a single node." | type: official
- [C13] Inngest 自托管无内置数据保留：不会自动删 Postgres 旧行，retention 仅列 roadmap | src: https://www.inngest.com/docs/self-hosting | quote: "The Inngest server does not automatically delete old database rows within Postgres for events, runs, or traces." | type: official
- [C14] Inngest 自托管 metrics 默认仅一个 gauge，更多需实验 flag | src: https://www.inngest.com/docs/self-hosting | quote: "By default it emits a single gauge, `inngest_queue_depth`." | type: official
- [C15] Inngest 自托管诊断工具仍为 alpha | src: https://www.inngest.com/docs/self-hosting | quote: "`inngest alpha doctor` and `inngest alpha debug` - currently in alpha." | type: official
- [C16] Inngest 官方不保证自托管支持 | src: https://www.inngest.com/docs/self-hosting | quote: "Inngest's support team does not guarantee direct support for self-hosted instances." | type: official
- [C17] Inngest 自托管默认关闭 app sync 轮询（cloud 侧持续同步函数配置） | src: https://www.inngest.com/docs/self-hosting | quote: "Disable app sync polling to check for new functions or updated configurations" | type: official
- [C18] Inngest 外部数据库支持未完成 | src: https://www.inngest.com/docs/self-hosting | quote: "Inngest can be configured to use external services for the queue and state store, and soon, the database." | type: official
- [C19] Temporal 官方明示 Audit Logs 为 Cloud 功能 | src: https://docs.temporal.io/cloud/audit-logs | quote: "Audit Logs is a feature of Temporal Cloud" | type: official
- [C20] Temporal SAML 文档仅面向 Cloud 账户（未提自托管可用） | src: https://docs.temporal.io/cloud/manage-access/saml | quote: "SAML is included on all Temporal Cloud plans. … To authenticate the users of your Temporal Cloud account" | type: official
- [C21] Temporal Cloud 独占控制面功能集：tcld CLI、Cloud Ops API、Terraform provider、cell-based 架构跨 AZ/区域/云 HA、99.9%/99.99% SLA、PrivateLink/PSC、mTLS 证书+API key 认证 | src: https://docs.temporal.io/evaluate/cloud | quote: "Cloud Ops API … Programmatic access for custom tooling and automation … Replicate across cloud providers (AWS ↔️ GCP)" | type: official
- [C22] Temporal 官方称自托管应用可零改码迁 Cloud（兼容性表述，非功能对等承诺） | src: https://docs.temporal.io/evaluate/cloud | quote: "applications built for a self-hosted Temporal Service run on Temporal Cloud without code changes" | type: official

## conflicts
- 主张 A（Restate 自托管无阉割）：server binary 层面官方称"single binary that implements all features"（R1），且 OTEL 导出/client-side encryption 自托管可用（C10/C11）；但 Cloud 专属的管理面功能确实存在 —— 环境控制面、secure tunnels、Lambda assume-role 调用、Cloud console 日志、SAML SSO/SCIM（C7/C8/C9）。属"server 无阉割、管理面有边界"，部分削弱原主张的"无限制"读法。
- 主张 B（Inngest 仅四项 cloud-only）：docs/self-hosting 明列了更多缺口 —— 单节点上限（默认）、无 retention、metrics 默认残血、诊断 alpha、sync polling 默认关、外部 DB"soon"、无支持保证（C12–C18）。推翻"仅四项"的完整性。
- 主张 C（Temporal 无 cloud 独占对照）：官方无 OSS-vs-Cloud 对照表（evaluate/cloud/security 页均无），但 audit-logs/saml 页有"feature of Temporal Cloud / included on all Temporal Cloud plans"的归属表述（C19/C20），cloud 独占功能客观存在。

## gaps
- Inngest Insights 是否自托管可用：docs/platform/monitor/insights 全文未提 self-host/cloud-only，self-hosting 页也未提 Insights；realtime 自托管支持未查（self-hosting 页未提及）。
- Restate 定价页 SAML SSO/SCIM、OTEL exports、client-side encryption 各行的档位勾选未渲染，无法确认归属档位；未找到 "Compare Cloud/BYOC/self-hosted" 对照页（导航有此链接文本，目标页未定位）。
- Temporal SCIM 页面未单独核；"OSS 不支持 X"的逐字排除句在已查页（cloud、saml、audit-logs、evaluate、evaluate/cloud、security）均未出现。
- Inngest changelog/blog、github.com/inngest 仓库 feature flag 未查；Restate changelog 未查。

## leads
- github.com/inngest/inngest 源码目录可能暴露 license/feature gating（未查）。
- Temporal 自托管 SSO（JWT/OIDC via web UI config）文档未核，可能弱化 SAML cloud-only 结论。
- Restate cloud/connecting-services 的 secure tunnel + Lambda assume-role 是最具体的 Cloud 独占集成。
