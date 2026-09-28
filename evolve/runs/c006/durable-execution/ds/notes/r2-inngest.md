# r2-inngest
question: (a) Inngest 官网 "each step completes exactly once" 准确原句与语境；(b) 自托管二进制是否剔除/门控 SSO/RBAC/audit 等企业功能。
checked: https://www.inngest.com/docs/examples/durable-endpoints, https://www.inngest.com/docs/self-hosting, https://www.inngest.com/pricing, https://github.com/inngest/inngest (Makefile, .goreleaser.yml, pkg/devserver/devserver.go, ui/apps/dev-server-ui/src/hooks/useFeatureFlags.ts, ui/apps/dashboard/src/components/Billing/Plans/utils.tsx, issues #4470/#4731)

## claims
- [C1] durable-endpoints 页第二段原句："use step.run() inline to get automatic retries and memoization for each step. This is useful when you want your endpoint to orchestrate multiple operations (like booking a flight, processing a payment, and sending a confirmation) and guarantee that each step completes exactly once, even if the handler crashes or restarts partway through." 语境：`inngest.endpoint()` 包裹现有 API route。 | src: https://www.inngest.com/docs/examples/durable-endpoints | quote: "guarantee that each step completes exactly once, even if the handler crashes or restarts partway through." | type: official
- [C2] 同页解释机制为 memoization + 跳过已完成 step，非外部副作用语义："Each step.run() call is memoized: if the handler is re-executed (due to a retry or crash recovery), completed steps are skipped and their previous results are reused." | src: https://www.inngest.com/docs/examples/durable-endpoints | quote: "completed steps are skipped and their previous results are reused" | type: official
- [C3] 崩溃示例场景：handler 在 enrich-data 完成、process 未完成时崩溃，重跑时第一步返回缓存结果；原文 "No duplicate work, no lost progress." | src: https://www.inngest.com/docs/examples/durable-endpoints | quote: "The first step returns its cached result instantly, and execution picks up at the second step. No duplicate work, no lost progress." | type: official
- [C4] 每步独立重试不重跑前序步骤："each step retries on its own without re-running previous steps"；"If the hotel booking fails, it retries independently while the flight and car rental results are preserved." | src: https://www.inngest.com/docs/examples/durable-endpoints | quote: "each step retries on its own without re-running previous steps" | type: official
- [C5] 判定（D9）：该 "exactly once" 指 step 完成结果的 memoization（完成过的 step 绝不重跑、复用缓存结果），即 durable execution 内部语义；页面未提及幂等性要求或对外部副作用（扣款/预订中途崩溃）的 exactly-once 保证，尽管示例把 payment/booking 包进 step.run()。 | src: https://www.inngest.com/docs/examples/durable-endpoints | quote: "guarantee that each step completes exactly once, even if the handler crashes or restarts partway through." | type: official
- [C6] Pricing 页 Enterprise 档安全功能原文 "SAML, RBAC, audit trails"（dashboard 代码 utils.tsx L177 为 "SAML, RBAC, and audit trails"），另有 "Trace and log exports"、"Datadog and advanced observability"、"90 day trace history"、"HIPAA included"、"Dedicated Slack channel"。 | src: https://www.inngest.com/pricing | quote: "SAML, RBAC, audit trails" | type: official
- [C7] Pricing FAQ：self-host 无专属功能清单，只定位 Cloud 增值。"Can I self-host Inngest? Yes. Inngest is open-source and can be self-hosted." Cloud 提供 "managed infrastructure, observability, and reliability"。 | src: https://www.inngest.com/pricing | quote: "Yes. Inngest is open-source and can be self-hosted." | type: official
- [C8] Self-hosting 文档页完全不提 SSO/RBAC/audit/功能差异；仅支持层面："Inngest's support team does not guarantee direct support for self-hosted instances." 及 "If you require dedicated support or service guarantees for self-hosting, please contact us to explore enterprise options." | src: https://www.inngest.com/docs/self-hosting | quote: "Inngest's support team does not guarantee direct support for self-hosted instances." | type: official
- [C9] 发布二进制只打包 dev-server-ui 而非 cloud dashboard：Makefile `build-ui` 构建 `ui/apps/dev-server-ui` 并拷至 `pkg/devserver/static/`；`.goreleaser.yml` L7 在构建前执行 `make build-ui`。SAML/RBAC/audit 所在的 `ui/apps/dashboard`（含 Billing/Plans）不进二进制。 | src: https://github.com/inngest/inngest/blob/main/Makefile | quote: "cd ui/apps/dev-server-ui && pnpm build\ncp -r ./ui/apps/dev-server-ui/dist/* ./pkg/devserver/static/" | type: official
- [C10] dev-server UI 无任何用户认证代码：dev-server-ui 内搜不到 login/auth 实现；`pkg/devserver/devserver.go` 唯一 authentication 命中是 Redis Sentinel 注释。issue #4470 用户原话："there is not even a basic auth for that dashboard"。 | src: https://github.com/inngest/inngest/issues/4470 | quote: "there is not even a basic auth for that dashboard" | type: secondary
- [C11] 自托管 UI 存在服务端 feature flag 门控机制：dev-server-ui 从 `/dev` 端点拉取 `FEATURE_CEL_SEARCH`、`FEATURE_EVENTS` 布尔 flag（useFeatureFlags.ts）。 | src: https://github.com/inngest/inngest/blob/main/ui/apps/dev-server-ui/src/hooks/useFeatureFlags.ts | quote: "FEATURE_CEL_SEARCH?: boolean; FEATURE_EVENTS?: boolean;" | type: official
- [C12] issue #4731（2026-08-11，OPEN，无官方回复）：v1.19.4 自托管 dashboard 的 runs CEL 搜索框被锁，此前可用；社区猜测 "the ui is gating on a cloud-only flag"。是刻意门控还是回归未定。 | src: https://github.com/inngest/inngest/issues/4731 | quote: "Earlier versions used to allow search using CEL expressions. Now it shows this" | type: secondary
- [C13] issue #4470（2026-06-18，OPEN）：自托管 dashboard 侧栏锁死显示 "Development" 环境；社区成员查证 goreleaser/Makefile 确认打包的是 dev-server-ui，与 cloud `dashboard` 是两个应用。 | src: https://github.com/inngest/inngest/issues/4470 | quote: "So `dev-server-ui` are completely different from `dashboard`" | type: secondary

## conflicts
- 无直接冲突。定价页写 "SAML, RBAC, audit trails"，dashboard 代码写 "SAML, RBAC, and audit trails"——同一功能的措辞差异，非实质冲突。

## gaps
- 无官方页面给出「self-hosted vs Cloud 功能对照表」；"SAML/RBAC/audit 属 Cloud/Enterprise" 的结论由定价页 + 代码架构（dashboard 不入二进制、dev-server-ui 无认证）推出，非官方明文声明。
- FEATURE_CEL_SEARCH 在自托管端被锁是回归还是刻意门控：上游 issue 无 maintainer 回复；可查 v1.19.x changelog/release notes 确认。
- durable-endpoints 页未说明 exactly-once 是否覆盖 step 内部外部副作用（如扣款后崩溃）；未出现 idempotent/side-effect 字样。

## leads
- 查 inngest repo CHANGELOG/release notes v1.18→v1.19 间 FEATURE_CEL_SEARCH 相关提交，确认搜索门控是否刻意。
- `ui/apps/dashboard` 在 repo 内但不随二进制发布——cloud 控制面；`@inngest/components` 共享组件里的 flag 名可枚举更多被门控功能。
