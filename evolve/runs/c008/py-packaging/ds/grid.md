# Grid v1 — 实体 × 维度（R1 收束后）

## 分类轴
①装什么包：PyPI wheel（PEP 标准系）vs conda 预编译跨语言包
②管多宽：安装器（pip）vs 项目管理器（uv/Poetry/PDM）vs conda 工作区（pixi）
→ 家族：PyPI 安装器 / PyPI 项目管理器 / conda 工作区。解释力强：锁格式、构建后端、解释器管理差异都落在轴上。

## 状态矩阵
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| uv | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(仅pip→uv; 其他∅) | ✅ | ✅ | ✅ |
| pip | — | ✅ | — | — | — | ✅ | — | ✅ | ✅ | ✅ |
| Poetry | ✅ | ✅ | ∅(无官方,issue open) | ✅(2.1实验) | ✅ | ✅ | ✅(无req导入) | ✅ | ✅ | ✅(723 ∅) |
| PDM | ✅ | ✅ | ✅(2.28实验) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pixi | ✅ | ✅ | ✅(模型不同) | ✅ | ✅(preview) | ✅ | ✅ | ✅ | ✅ | ✅ |
| PEP751标准 | — | ✅Final | — | — | — | — | — | — | — | — |

## R1 遗留缺口（R2 候选）
- poetry.lock 是否官方承诺跨平台（❓未取到原句）
- 「pip lock 仅当前平台 vs PEP751 多环境」需在成稿写清（已写进第 5 节）
- 私有源 dependency confusion：pip 侧无官方表述（只有 uv/Poetry 官方）→ 反证点
- 边界主张待反证：uv「项目接口仍只用 uv.lock」、Poetry「无官方 workspace」、Poetry「无官方 requirements.txt 导入」、pixi「无 workspace members」
- 次要：uv_build 首版、PDM 默认切 venv 版本、pixi.lock version 字段
