# Taxonomy grid

版本：v1（R1 收束）
状态只出现在矩阵单元格里。图例：✅ 一手来源加原句；⚠ 只有二手；⚔ 来源冲突；❓ 缺口；∅ 官方未写（已定向查过）；— 不适用。

## 分类轴

| 轴 | 这一轴回答什么 | v1 |
|---|---|---|
| A1 生态谱系 | 包从哪个宇宙解析，锁文件跟谁走？ | PyPI/PyPA：pip、uv、Poetry、PDM。Conda/prefix：pixi 与 conda（conda 本轮只有 scout，矩阵仍空） |
| A2 职责宽度 | 它替你管到哪一层？ | 安装器：pip。项目管理器：uv、Poetry、PDM。conda 包 + PyPI + 解释器：pixi |

v0→v1：轴不换。两条轴仍解释「包从哪来」和「管到哪一层」。scout 提出的「锁是否跨平台」收进 D2 的单元格，不新开列。「sync 会不会删多余包」先不进网格，等非 scout 笔记再决定是否写入坑。新增 conda 行。hatch、pip-tools、rye 不进矩阵。

## 维度

| ID | 维度 | 这一列回答什么问题 |
|---|---|---|
| D1 | 元数据 | 项目名、版本、依赖写在哪个文件的哪张表？ |
| D2 | 锁文件 | 锁文件叫什么、锁定范围是否跨平台、能否读/写 `pylock.toml`？ |
| D3 | workspace | monorepo 的成员和内部依赖用哪个字段声明？ |
| D4 | Python | 谁安装、固定、切换 CPython？配置键或命令叫什么？ |
| D5 | 构建后端 | 默认 `[build-system]` 的 `build-backend` 是谁？ |
| D6 | 环境 | 依赖装进哪种环境、默认路径是什么？ |
| D7 | 依赖组 | dev / 可选依赖用哪套字段？ |
| D8 | 私有源 | 额外 index / channel / 凭证的字段和环境变量叫什么？ |
| D9 | CI 缓存 | 官方让 CI 缓存哪个目录、哪个环境变量？ |
| D10 | 迁移 | 官方从旧工具迁入的命令或文档入口叫什么？ |

## 矩阵

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| uv | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pip | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Poetry | ⚔ | ⚔ | ∅ | ⚔ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ |
| PDM | ✅ | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pixi | ✅ | ✅ | ❓ | ✅ | ⚔ | ✅ | ✅ | ✅ | ⚔ | ✅ |
| conda | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

依据（不是状态）：uv D2 同页既写跨工具安装是 future，又写出现行 `uv pip sync`。pip D2 为实验性读写，且依赖解析页仍指向 pip-tools；安装时是否跳过解析未写。Poetry D1 为 2.0 可用 `[project]` 与 FAQ 仍允许只写 `tools.poetry`。Poetry D3 定向查过无特性页。Poetry D4 为 `env use` 有原句，`poetry python install` 有原句，对向的「不安装解释器」没有摘进 quote。pixi D3 没有成员字段原句。pixi D5 为构建教程与 Poetry 迁移页相反。pixi D9 为缓存目录两页不一致。conda 整行留到复核，scout 不直接进成稿。

## 未进矩阵

| 实体 | 处理 |
|---|---|
| hatch | scout：仍是项目管理器，hatchling 是后端。R2 不派，除非锁文件结论还缺一个 PyPA 参照 |
| pip-tools | scout：仓库在 jazzband，仍能编译 requirements。pip 自己的文档仍提到它，冲突写在第 5 节 |
| rye | scout：已停更，继任是 uv。不占一行 |
