# Taxonomy 网格

状态：`✅` 一手来源 + 原文摘录；`⚠` 只有二手；`⚔` 来源冲突；`❓` 缺口；`∅` 官方未写（已定向查过）；`—` 不适用。

## 分类轴（v0，R1 后保留）

轴 1「项目真相放在哪一层」仍解释锁文件名、元数据表、workspace、构建后端的差异：

- 安装器：pip。官方写明不管项目、不管解释器。
- PyPI 项目管理器：uv、Poetry、PDM。都读 `[project]`，各自另有一把项目锁。
- conda 工作区：pixi。必填的是 `[workspace]` 的 channels / platforms，不是 PyPI 项目表。conda 本体仍是空行。

轴 2「依赖宇宙」：pip / uv / Poetry / PDM 锁的是 index、VCS、path、url。pixi 同时锁 conda channel 与 PyPI（PyPI 解析写明使用内置 uv）。

R1 没有出现轴 1 解释不了、又反复出现的差异。`pyver` 仍是独立列（谁下载 CPython），不另立家族。

未升格（只在 scout leads）：hatch、pip-tools、pipenv 待 R2 用窄简报决定是否进入「变体」而非新家族。rye 只作 uv 的迁移来源。mamba 不单列。

## 维度

| 维度 | 这一列回答什么问题 |
|---|---|
| lock | 锁文件叫什么、读/写 `pylock.toml`（PEP 751）吗、从哪一版起、用什么命令 |
| meta | 项目元数据写在哪个表 |
| workspace | monorepo 怎么声明成员、路径依赖怎么写 |
| pyver | 谁安装 CPython、钉版本的文件或字段叫什么 |
| build | 默认 `build-backend` 字符串是什么、能不能换成别的 |
| sources | 依赖从哪些宇宙进入锁 |
| migrate | 官方从哪些旧工具导入、命令名是什么 |
| ci | 官方点名的缓存目录或环境变量是什么 |
| index | 私有源的配置键和凭据环境变量叫什么 |

## 网格

| 实体 | lock | meta | workspace | pyver | build | sources | migrate | ci | index |
|---|---|---|---|---|---|---|---|---|---|
| uv | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pip | ✅ | ✅ | ∅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Poetry | ✅ | ✅ | ∅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PDM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pixi | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| conda | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

pixi 的 `lock` 为 ⚔：文件名 `pixi.lock` 一致；文档示例写 `version: 6`，changelog 写 0.68.0 起为 v7。

Poetry / pip 的 workspace 为 ∅：工人定向查过命令列表与相关页，没有 workspace 功能名。这是边界主张，反证前不写进「一屏看懂」。

Poetry 是否**读取**已有 `pylock.toml` 仍是 lock 格里的缺口，不单独占状态：导出语句已有一手来源，读取没有原句。

PDM `lock` 不标 ⚔：`lock.format=pylock` 与 2.25.0 release 一致；冲突只在 export 页「只支持 requirements.txt」与同页 pylock 导出两句并存，记在成稿第 5 节。

PDM `pyver` 不标 ⚔：`.pdm-python` / `pdm python` 有原句；只有 `.python-version` 的「Added in 2.23.0」和 release notes 对不上。
