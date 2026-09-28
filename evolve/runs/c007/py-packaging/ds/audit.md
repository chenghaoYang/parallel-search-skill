# 终审核验汇总（52 项）

## v-conda（9 项）
8 confirmed；V1 走样：pixi.lock 文档页示例为 version: 6（version:7 来自仓库实物）→ 成稿已删版本号。

## v-pdm（8 项）
全 confirmed；V3/V5/V6 附加细节未在引用页核对（workspace members 语法、pdm-backend PEP 清单、.venv 位置）——来自上轮官方 docs 笔记，保留。

## v-pip / v-uv / v-poetry / v-eco
429 限流后 SendMessage 续跑；结果见下（待补）。

## 终稿状态
预算耗尽提前收稿：v-pip/v-uv/v-poetry/v-eco 共 35 项未回判定。这些主张全部经过 R2 一手反证轮或来自 R1 官方文档摘录（159/161 claims 为 official），风险集中在版本号细节，已在 §5 标注。v-conda 走样项已修复。
v-uv 后补：9/9，V9 走样（「尚未编写」指迁移指南整体非专指 Poetry）→ 已改稿。
