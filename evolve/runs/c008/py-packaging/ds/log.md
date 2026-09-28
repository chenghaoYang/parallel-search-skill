# log

## R1（6 spawn：uv/pip+PEP751/poetry/pdm/pixi/scout）
- 3 个工人遇 429 限流中断，SendMessage 续跑全部成功，无重派浪费。
- 结果：177 主张（174 official），0 缺 src/quote，6 conflicts（均非实质冲突）。
- taxonomy v0→v1：确认两轴（装什么包 × 管多宽），三家族。轴解释力强，不换。
- 收束：写 report 8825 字符（预算 9000），压缩手段=去来源标题+矩阵紧缩。
- roundstat：grid 48/48 resolved（3 ∅）。

## R1 观察 → R2 决策
- 进一屏的边界主张需反证：①uv「项目接口只用 uv.lock」（uv 已到 0.12+，需查 changelog 是否变化）②Poetry「无官方 workspace」③Poetry「无官方 req.txt 导入」④pixi「无 members 式 workspace」⑤「没有工具默认 pylock」。
- 缺口：poetry.lock 跨平台官方表述；pip 侧 dependency confusion 官方原句；pip lock 跨平台选项；PDM lock --platform；pixi build 转正版本。
- → 动作：4 个定向反证/补漏简报（uv、poetry+pdm-lock、pixi、pip-confusion+spec页）。预计 spawn：4。

## R2（4 spawn：uv-check/poetry-check/pixi-check/pip-check）
- 全部一次成功。50 条新主张，全 official。
- 反证结果：uv「项目锁=uv.lock」成立（仅 --with-requirements 临时读 pylock）；「无默认 pylock 工具」成立；Poetry 无 workspace/无 req.txt 导入成立（issue #2270 open）；pixi 无 members 字段成立（模型=成员各自 manifest+workspace.dependencies）；pip 依赖混淆有官方原句（Warning 框）。
- 补漏：pip 26.2.1/uv 0.12.19/Poetry 2.5.1/pixi 0.81.0 版本快照；uv_build 0.5 引入/0.6.5 独立包/0.7.19 stable；pdm.lock --platform 跨平台；pixi.lock v7（文档示例过时）。
- 收束：改动净 +173 后压回 8998。手段=矩阵单元换措辞+来源节已极简。
- R2 观察：核心格子全部 ✅/∅，进一屏的边界主张均已反证 → 终审后停。

## R3 终审（1 spawn）
- 52 条抽查：49 supported / 2 weak / 1 unsupported / 0 contradicted。
- 修正：pip D5 删「PEP 517 frontend」（无笔记支撑）；setup-python 缓存保留并自标二手；pip-tools 有 pip 官方定位兜底。
- 终稿 8998→~8970 字符 ≤9000，写 ./ds/report.md 与 ./report.md。
