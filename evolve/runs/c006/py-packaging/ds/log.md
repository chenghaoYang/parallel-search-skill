# log

## R0
- brief.md、grid.md v0 已写。分类轴：PyPI vs conda 生态；是否管解释器；PEP 标准兼容度。
- R1 计划：5 个实体各一工人（uv、pip+PEP751、Poetry、PDM、pixi）+ 1 scout（迁移/CI/私有源坑 + 遗漏实体）。
- spawn 数：6。

## R1 收束
- 6 工人全部返回，141 claims（135 official）。网格 39/40 填充。
- taxonomy v0 轴保留：生态/职责边界/PEP 采用层级，能解释矩阵差异，未换轴。
- 成稿 10630 → 压缩至 8932（来源节去标题留 URL、删 P2）。
- R1 观察：核心格子全 ✅/∅；风险点是进 §0 的边界主张（Poetry 无 workspace/无导入器、pixi 不支持 PEP751、uv 主锁不能是 pylock）→ 动作：终审核验批 4 工人，逐条回原页+反证 → 预计 spawn：4。

## 终审
- 4 核验工人回原页：38 confirmed / 2 走样 / 0 wrong；4 条反证均无反例（Poetry 无 workspace、无导入器；uv 主锁非 pylock；pixi 无 PEP751）。
- 修正：删 `pixi add python=3.x`、删「pip: 段进 pypi-dependencies」、补 direct-URL 凭据例外、§5 补 pixi 反证结论。
- 终稿 8932→约 9000 内，已写 ./report.md。
