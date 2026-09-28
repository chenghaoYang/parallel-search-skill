# Brief（R0）

## 任务
产出一份文档，帮助「要开新 Python 项目、需要在几分钟内选定包管理/项目管理工具」的读者，快速建立认知并能对照选择。

## 读者
中级以上 Python 开发者，可能刚好从 pip/requirements.txt 或旧版 Poetry 迁移过来。5 分钟内要能回答：
1. 我该用哪个工具？
2. 它们在锁文件、workspace/monorepo、Python 版本管理、构建后端上到底差在哪？
3. PEP 751（pylock.toml）现在是什么状态，uv/pip 是否已支持？Poetry 2 是否已改用标准 `[project]` 表？
4. 迁移、CI 缓存、私有源这些运维细节要注意什么？

## 范围内
- 工具（至少 5 个，来自 seed）：uv、pip（+ pip-tools）、Poetry（v1 → v2）、PDM、pixi、conda（+ conda-lock）。
- 标准/PEP：PEP 621（`[project]` 表）、PEP 517/518（构建后端接口）、PEP 751（`pylock.toml` 标准锁文件）。
- 维度：锁文件格式与标准化程度、workspace/monorepo、Python 版本管理、构建后端、虚拟环境管理、非 Python 依赖、私有源/认证、CI 缓存、从旧工具迁移。
- 候选新增行（视 R1 leads 决定是否单列）：Hatch（PEP621 原生 + 构建后端 hatchling）、pip-tools 单独成节还是并入 pip。

## 范围外
- 与 Python 无关的通用构建系统（Bazel/Nix 等）细节。
- PyPI 发布/twine 等发布机制本身。
- resolver 算法内部实现细节（只需知道解析器种类与速度定性）。
- conda 里非 Python 包（R、C 库）生态的深入介绍，只需说明「能管理」这一事实。

## 用户点名的疑点（成稿必须给出明确结论）
- Q1: PEP 751 / `pylock.toml` 是否已定稿？uv、pip 是否已支持？
- Q2: Poetry 2 是否已改用标准 `[project]` 表（而非 `[tool.poetry]` 自定义表）？

## 完成标准
- 0 节「一屏看懂」能独立回答 Q1、Q2 和「新项目怎么选」。
- 对照矩阵覆盖 5 个 seed 工具在全部维度上的取值，不用「详见来源」糊弄。
- 成稿 ≤ 9000 字符（含来源节），每轮收束后重写而非追加。

## 外层参数
rounds=3, workers≤6/轮, budget=9000 字符, dir=./ds, 终稿另存 ./report.md（相对主工作目录）。
工人：subagent_type="research-worker"（不传 model）。检索：WebSearch 找页 + WebFetch 开一手页。无 pplx-safe。
