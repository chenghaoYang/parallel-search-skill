# r2-dbos
question: DBOS (a) Java SDK GA or preview/beta; (b) Postgres 最低版本; (c) DBOS Cloud 公开单价或已下线; (d) Conductor license/是否开源
checked: https://docs.dbos.dev/, https://docs.dbos.dev/java/programming-guide, https://docs.dbos.dev/faq, https://dbos.dev/pricing, https://github.com/dbos-inc/dbos-transact-java, https://github.com/dbos-inc/dbos-transact-java/releases, https://github.com/orgs/dbos-inc/repositories?page=1&2, https://www.dbos.dev/conductor-license, https://repo1.maven.org/maven2/dev/dbos/transact/maven-metadata.xml, https://raw.githubusercontent.com/dbos-inc/dbos-ctl/main/supported-databases.json, github.com/dbos-inc/dbos-docs (cloned, grepped)

## claims
- [C1] Java SDK 已越过 1.0：Maven Central 上 dev.dbos:transact 存在正式版 1.0.0，latest/release 为 1.1.0-m43（里程碑版），元数据 lastUpdated=20260924 | src: https://repo1.maven.org/maven2/dev/dbos/transact/maven-metadata.xml | quote: "<latest>1.1.0-m43</latest> <release>1.1.0-m43</release> ... <version>1.0.0</version>" | type: official
- [C2] GitHub releases 中 dbos-transact-java 1.0.0 带 "Latest" 徽标，发布于 07-01（2026）；0.8.0 说明预告 1.0 起采用 "standard SemVer deprecation policy"。无任何 beta/preview 字样 | src: https://github.com/dbos-inc/dbos-transact-java/releases | quote: "1.0.0 ... Latest" | type: official
- [C3] Java 文档（programming-guide）未标注 GA/beta/preview，仍钉在 implementation("dev.dbos:transact:0.9.0")（落后于已发 1.0.x） | src: https://docs.dbos.dev/java/programming-guide | quote: "implementation(\"dev.dbos:transact:0.9.0\")" | type: official
- [C4] Java SDK 环境要求：Gradle 8+；建议 Java 21，最低 Java 17 | src: https://github.com/dbos-inc/dbos-docs/blob/main/docs/java/prompting.md | quote: "Gradle 8 or later should be suggested. Java 21 should be suggested, but any Java 17 or later can be used if the user requests that." | type: official
- [C5] Postgres 版本：docs 无显式最低版本要求，quickstart 仅说 "DBOS requires a Postgres database"；docker 示例用 postgres:17，k8s/Conductor 自托管示例用 postgres:16 | src: https://github.com/dbos-inc/dbos-docs/blob/main/docs/quickstart.md | quote: "DBOS requires a Postgres database. ... docker run -d --name dbos-postgres ... postgres:17" | type: official
- [C6] 官方支持矩阵（dbos-ctl 仓库 supported-databases.json，CLI 使用）：Postgres 14/15/16/17/18，18 标记 latest → 最低支持版本为 Postgres 14；另列 CockroachDB 25.2/25.4/26.2 | src: https://raw.githubusercontent.com/dbos-inc/dbos-ctl/main/supported-databases.json | quote: "{ \"engine\": \"postgres\",  \"version\": \"14\",   \"image\": \"postgres:14\" } ... { \"engine\": \"postgres\",  \"version\": \"18\",   \"image\": \"postgres:18\",  \"latest\": true }" | type: official
- [C7] DBOS Cloud 仍在运营（docs 现维护 dbos-cloud 章节）："DBOS Cloud is a serverless platform for durably executed applications"，托管+自动扩缩，计费模式为 "Applications are charged only for the CPU time they actually consume" | src: https://github.com/dbos-inc/dbos-docs/blob/main/docs/production/dbos-cloud/deploying-to-cloud.md | quote: "DBOS Cloud is a serverless platform for durably executed applications. ... Applications are charged only for the CPU time they actually consume." | type: official
- [C8] dbos.dev/pricing 公开的是订阅档而非 Cloud 单价：Pro "$99/month"（2 seats/3 apps/1M checkpoints，超额 $50/百万）、Teams "$499/month"（10 seats/10 apps/10M checkpoints，超额 $40/百万）、Enterprise "Custom"；Cloud 计算本身 "Contact sales"，无 per-CPU/per-exec 公开单价 | src: https://dbos.dev/pricing | quote: "DBOS Pro — $99/month ... Extra checkpoints - $50 per million ... DBOS Teams — $499/month ... More cost-effective than AWS Lambda" | type: official
- [C9] Conductor 是专有闭源软件：自托管文档 "Self-hosted Conductor is released under a proprietary license and requires a license key"；许可证页明确被许可方 "no right or license to access or possess Software source code"（Conductor Software License, updated Dec 2025） | src: https://www.dbos.dev/conductor-license | quote: "Self-hosted Conductor is released under a proprietary license and requires a license key" (docs/production/hosting-conductor.md) | type: official
- [C10] Conductor 许可细节：开发/测试（"Test/Development Mode"）免费、dev key 可自取（console.dbos.dev/settings/license-key）但限 1 executor/app；生产/商用需付费 key（contact sales）；启动时向 cloud.dbos.dev 验证 license（可付费买免回连 key） | src: https://github.com/dbos-inc/dbos-docs/blob/main/docs/production/hosting-conductor-with-kubernetes.md | quote: "Conductor validates its license key against https://cloud.dbos.dev at startup and exits if it cannot reach it" | type: official
- [C11] dbos-inc org 33 个仓库中无 conductor/dbos-conductor 源码仓（逐页核对两页），佐证闭源 | src: https://github.com/orgs/dbos-inc/repositories | quote: "No — there is no repository named conductor or dbos-conductor" | type: official

## conflicts
- Java 文档钉 0.9.0（C3）vs Maven Central/GitHub 已发 1.0.0/1.1.0-m43（C1/C2）——文档滞后，非版本冲突。
- pricing 页 FAQ 曾提 "self-hosting Conductor with a free license" 可连 1 executor（docs/faq.md），与 hosting 文档的 dev key 限 1 executor 一致；但"free license"措辞与"proprietary license"并存——免费的是开发模式使用权，不是开源。

## gaps
- 无任何 docs 页面明示 Postgres 最低版本；14+ 下限来自 dbos-ctl 的 supported-databases.json（CLI 支持矩阵），非 requirements 文档。查过：docs 全库 grep（version/1x/or later 均无果）、faq、quickstart、4 个 SDK README、dbos-transact-py 源码与 pyproject。
- DBOS Cloud 的 CPU 时间单价（$/vCPU·s 之类）未公开，pricing 页仅订阅档+"Contact sales"。

## leads
- DBOS 官方支持 CockroachDB 作 system DB（docs/integrations/cockroachdb.md、dbosctl --cockroach、supported-databases.json）。
- docs 仓库含各语言 prompting.md（给 AI 助手的生成提示）。
- Conductor 有 "call-home" license 校验；air-gapped 需付费免回连 key。
