# 网格

状态：✅ 有一手来源 + 原文摘录；⚠ 只有二手来源；⚔ 来源冲突；❓ 缺口；∅ 官方未写（已定向查过）；— 不适用。

截至 2026-09-24。R1 收束后的状态。

## 分类轴 v1

v0 → v1：轴不变。包宇宙（PyPI vs conda）仍解释锁里记录什么、私有源是 index 还是 channel、Python 是不是 conda 包。职责（只安装 vs 拥有项目）仍解释 workspace 与谁下载 CPython。

改动的是家族成员，不是轴。Poetry 2.0 已能读写 `[project]`，`[tool.poetry]` 降为仍可用的旧表，不再单独成「自有清单」家族。证据：`r1-poetry` C2、C3、C4。

Hatch 可能是「权威锁就是 pylock」的项目管理器，与 uv / Poetry / PDM 的自家锁不同。scout 不进成稿，Hatch 本轮不入格。R2 用窄简报核对后再决定加不加一行。

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| PyPI 安装器 | pip | 消费清单或锁，不写项目 |
| PyPI 项目管理器 | uv、Poetry、PDM | 拥有 `[project]`、锁和环境 |
| conda 栈求解器 | pixi；conda 行仍空 | 主宇宙是 conda 包，PyPI 后装 |

## 维度

| 列 | 这一列回答什么问题 |
|---|---|
| D1 清单 | 依赖和项目元数据写在哪个文件、哪张表？是不是 PEP 621 的 `[project]`？ |
| D2 锁 | 锁文件叫什么？是不是 PEP 751 `pylock.toml`？能生成、能安装、还是两者？有没有 hash？一份锁跨不跨平台？ |
| D3 workspace | 多包仓库怎么声明成员？成员如何互相依赖？锁是仓库一份还是每包一份？ |
| D4 Python | 工具能否下载并钉住 CPython？钉在哪个字段？和 `requires-python` 什么关系？ |
| D5 构建后端 | 默认 `[build-system].build-backend` 是哪个字符串？能不能换？工具是否负责 build / publish？ |
| D6 依赖组 | 开发依赖、可选依赖的字段名是什么？解析器看 PyPI、conda channel，还是两者？ |
| D7 迁移 | 从 requirements.txt / Poetry / Pipfile / conda 环境迁入的官方命令是什么？ |
| D8 CI | 官方让 CI 缓存哪个目录，或用哪个官方 Action / 环境变量？ |
| D9 私有源 | 私有 index 或 channel 的配置键、凭证环境变量是什么？凭证会不会进锁文件？ |

## 实体 × 维度

| 实体 | 家族 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|---|
| uv | PyPI 项目管理器 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pip | PyPI 安装器 | ✅ | ✅ | ∅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Poetry | PyPI 项目管理器 | ✅ | ✅ | ❓ | ⚔ | ✅ | ⚔ | ∅ | ✅ | ✅ |
| PDM | PyPI 项目管理器 | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pixi | conda 栈求解器 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ |
| conda | conda 栈求解器（待实体复核） | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

pip.D3：user guide、workflow、pip lock、pip install 均无 workspace，标 ∅。Poetry.D3 只确认「打开过的页没有」，还没做全站反证，保持 ❓。Poetry.D7：CLI 参考无 import，标 ∅。

不在表内、但会影响第 0 节用词的边界（R2 反证，不单列格子）：Poetry 2.3.0 之后能否用 pylock 替换 `poetry.lock`；`poetry new` 模板是否只有 `[project]`；uv 0.6.15 之后项目接口是否仍拒绝把 pylock 当 `uv.lock`；pip 安装 pylock 时是否跳过 resolver。

## 疑点 → 格子

- Q-pylock → `uv.D2` ✅、`pip.D2` ✅。结论已写入成稿，时间边界待 R2 反证。
- Q-poetry-project → `poetry.D1` ✅。模板原文摘录不足，待 R2。
