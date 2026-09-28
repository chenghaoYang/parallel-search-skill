# grid v1

## 分类轴（不变，解释力足够）
- 轴1 生态：PyPA/PyPI 系（uv、pip、Poetry、PDM；wheel+venv）vs conda 系（pixi、conda；多语言二进制+prefix）
- 轴2 定位层：纯安装器（pip）vs 全项目管理器（uv、Poetry、PDM、pixi）vs 环境层（conda）

## 状态矩阵（R1 后）
| | D1定位 | D2锁 | D3元数据 | D4ws | D5解释器 | D6构建 | D7环境 | D8操作 |
|uv|✅|✅|✅|✅|✅|✅|✅|✅|
|pip|✅|✅|—|—|✅|—|✅|✅|
|Poetry|✅|✅|✅|✅|✅|✅|✅|✅|
|PDM|✅|✅|✅|✅|✅|✅|✅|✅|
|pixi|✅|✅|✅|✅|✅|✅|✅|✅|
|conda|✅|✅|—|—|✅|⚠|✅|⚠|

## 已知缺口/边界（R2 后）
- Poetry 读 pylock：✅ 反证完成——code search 零命中+CLI 文档无，确认仅导出
- uv export pylock：✅ 不 gated；preview `pylock` 仅安装侧
- setup-uv 默认 glob：✅ 逐字确认 7 项，无 pylock.toml
- Dependabot #12094 OPEN 零命中；Renovate #35704「PR welcome」、manager 列表无 pylock ✅
- hatch 1.17 确认（hatch.pypa.io history + locker 页）
- conda 26.5：✅ 双向（conda export 生成 / create+install 消费；只锁 conda 包）
- pixi #3889：✅ 仍 open
- 残余：uv_build 默认化版本、pip 位置参数装 pylock、pixi per-env Python 无字面句（有 feature 示例）
