# log

R0：brief + grid v0（轴1 生态 PyPA vs conda；轴2 定位层 installer/manager/env；维度 D1–D8）。

R1 spawn 6：r1-uv, r1-pip, r1-poetry, r1-pdm, r1-pixi, r1-scout。
待查（R2 候选）：
- hatch/hatchling 是否值得单列一行
- rye 归档状态（若死则只在文内一句话）
- PEP 751 各工具支持粒度：install vs export vs generate

R1 收束：161 claims（159 official）；grid 41✅/2⚠；taxonomy v0 保留（两轴解释力够）。report.r1 = 8995 字。
R1 观察：核心格全满；剩 5 条边界主张未反证（Poetry 读 pylock ∅、uv export preview-gating、setup-uv 默认 glob、Dependabot/Renovate 不支持 pylock、pixi #3889/conda 26.5）→ 动作：R2 派 2 个窄工人做反证+补缺口 → 预计 spawn：2

R2 收束：2 工人返回，14+14 claims 全 official；5 条边界主张全 confirmed（Poetry 仅导出、uv export 不 gated、setup-uv glob 无 pylock、dependabot/renovate 未支持、hatch 1.17 属实）。新增 conda 26.5 双向锁、#3889 open、conda-build→rattler 委托。删 §5 已决项，压散文。report.r2 = 8996 字。
R2 观察：核心格全 ✅/∅，无 ⚔，疑点结论已反证 → 动作：终审（6 个核验工人按域回原页）→ 预计 spawn：6
终审：6 核验工人派出；v-pip/v-uv/v-poetry 撞 429 后用 SendMessage 续跑。v-conda 已回：8 confirmed、1 走样（pixi.lock version 7→文档页为 6，已改稿去掉版本号）。
