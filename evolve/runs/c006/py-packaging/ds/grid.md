# grid v1：实体 × 维度（R1 收束后）

状态：✅一手+摘录 ⚠二手 ⚔冲突 ❓缺口 ∅官方未写 —不适用

## 分类轴
- 轴1 生态：纯 PyPI（uv/pip/Poetry/PDM）vs conda 跨语言（pixi）
- 轴2 职责边界：只装包(pip) → 管项目+环境(Poetry/PDM/uv) → 管解释器(uv/PDM/pixi，Poetry 2.1 实验)
- 轴3 PEP 标准采用：621 [project] / 735 dep-groups / 751 pylock.toml 的三层支持（导出/消费/主锁）

## 网格

| 实体 | D1锁 | D2声明 | D3ws | D4py | D5build | D6env | D7迁移 | D8CI | D9私有源 |
|---|---|---|---|---|---|---|---|---|---|
| uv | ✅ uv.lock universal；pylock 导出+安装 | ✅ PEP621+735 | ✅ tool.uv.workspace | ✅ uv python install | ✅ uv_build 纯py | ✅ .venv | ✅ add -r + migrate-to-uv | ✅ setup-uv | ✅ index/netrc/keyring |
| pip | ✅ pip lock 25.1 实验；-r pylock 26.1 | —（消费 PEP735） | — | — | —（委托 PEP517） | ✅ 不建 venv | — | ✅ setup-python | ✅ URL/netrc/keyring |
| Poetry | ✅ poetry.lock 2.1；pylock 仅插件导出 | ✅ 2.0 起 [project] 默认 | ∅ issue#2270 | ✅ 2.1 实验 poetry python | ✅ poetry-core | ✅ venv 可配置 | ∅ 无导入器 | ⚠ 仅自用样例 | ✅ source+http-basic |
| PDM | ✅ pdm.lock/pylock 双格式（2.25 实验） | ✅ PEP621+735 | ✅ 2.28 实验 | ✅ 2.13 pdm python | ✅ pdm-backend | ✅ venv 默认/582 opt-in | ✅ pdm import 5 源 | ✅ setup-pdm@v4 | ✅ source+keyring 插件 |
| pixi | ✅ pixi.lock YAML v6（conda+pypi） | ✅ pixi.toml/[tool.pixi] | ✅ 多 package | ✅ python 是 conda 包 | ✅ pixi-build-* | ✅ .pixi/envs | ✅ pixi import 2 格式 | ✅ setup-pixi | ✅ auth login/keyring |

## 遗留 ❓/边界主张（待 R2 反证）
- ∅ 格：Poetry workspace（issue 佐证）、Poetry 导入器（cli 枚举佐证）、pixi PEP751（open issue 佐证）→ 反证必要性中低
- uv 主锁不能是 pylock：issue #12584 佐证（无 arbitrary entrypoints）
- Dependabot/Renovate pylock 支持 ❓
- 锁文件跨平台语义差异（uv.lock universal vs pdm.lock 策略 vs poetry.lock markers）→ 已有部分主张，够写一句
