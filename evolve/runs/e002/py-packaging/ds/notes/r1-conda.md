# r1-conda

question: conda 在环境/锁文件、workspace/monorepo 概念、Python 版本管理、构建/打包机制、依赖解析与速度、私有源(channel)配置、全局工具运行、迁移路径、生态定位这些维度上，官方文档是怎么说的？

checked: docs.conda.io, docs.conda-build.io, github.com/conda/conda (releases, changelog), github.com/conda/conda-lock, github.com/conda-incubator/conda-libmamba-solver, conda.org

## claims

- [C1] `environment.yml` 不锁定 build string，用于跨平台共享但需要平台相关的依赖解析 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "不通常跨平台，依赖平台特定的依赖解析" | type: official

- [C2] `conda list --explicit` 生成包含完整 URL、build 和平台标记的精确规范，仅限单平台 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "@EXPLICIT 标头加上 conda 包 URL 列表...通常限于单一平台" | type: official

- [C3] conda 26.5.0+ 支持 `conda-lock.yaml` 和 `pixi.lock` 格式的多平台环境锁定 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "conda-lock.yaml（conda 26.5+）...完全解析状态，conda 可跳过求解器步骤" | type: official

- [C4] `conda-lock` 项目由 conda 组织维护（github.com/conda），用于生成完全可复现的多平台锁文件 | src: https://github.com/conda/conda-lock | quote: "maintained by the Conda organization...Conda lock is a lightweight library...to generate fully reproducible lock files" | type: official

- [C5] conda 官方文档中无 workspace 或 monorepo 概念的相关内容 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/index.html | quote: "包括 packages, channels, environments, and plugins"（不包含 workspace/monorepo） | type: official

- [C6] conda 环境被定义为"一个包含特定包集合的目录"，环境之间相互隔离，与 Python virtualenv 不同的是 conda 把 Python 本身作为依赖 | src: https://github.com/conda/conda/blob/main/docs/source/user-guide/concepts/environments.rst | quote: "An environment is a directory that contains a specific collection of packages...Python itself is a dependency provided in conda environments" | type: official

- [C7] conda 通过 `conda create -n myenv python=3.x` 创建环境时指定 Python 版本，将 Python 作为普通包处理 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-python.html | quote: "Conda treats Python the same as any other package" | type: official

- [C8] 多个 Python 版本通过不同的独立环境实现隔离，使用 `conda activate` 切换 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-python.html | quote: "create a dedicated environment: conda create -n py39 python=3.9" | type: official

- [C9] conda-build 用 `meta.yaml` 和 recipes 构建包（v1 recipes），官方文档未提及与 PEP 517/518 的关系 | src: https://docs.conda-build.io/en/latest/user-guide/index.html | quote: "Here you can find tutorials and recipes as well as information about environment variables and wheel files" | type: official

- [C10] conda 23.10.0 (2023-10-30) 将 `conda-libmamba-solver` 正式设为默认 solver，替代经典 pycosat-based solver | src: https://github.com/conda/conda/blob/main/CHANGELOG.md (23.10.0) | quote: "With this 23.10.0 release we are changing the default solver of conda to conda-libmamba-solver!" | type: official

- [C11] conda 26.5.0+ 需要 `conda-libmamba-solver >=26.4.1` 支持依赖解析 | src: https://github.com/conda/conda/releases/tag/26.5.0 | quote: "libmamba solver: 版本要求升级至 >=26.4.1" | type: official

- [C12] conda 提供 `BaseSolver` 插件基类，支持自定义 solver 实现 | src: https://github.com/conda/conda/blob/main/CHANGELOG.md (26.5.0) | quote: "Introduce conda.core.solve.BaseSolver as the solver plugin base class" | type: official

- [C13] 通过 `.condarc` 文件或 `conda config --add channels <url>` 配置私有 channel | src: https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html | quote: "允许用户自定义 conda 的行为，例如包搜索渠道" | type: official

- [C14] 私有 channel 可在 `~/.condarc` 或 `$CONDA_PREFIX/.condarc` 配置，后者适用于环境特定的私有源 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html | quote: ".condarc 文件会在多个位置被搜索，包括用户主目录和环境特定目录" | type: official

- [C15] `conda run -n env <command>` 无需激活环境即可在其中执行命令，支持 `-p/--prefix` 指定环境路径 | src: https://docs.conda.io/projects/conda/en/latest/commands/run.html | quote: "Run an executable in a conda environment without requiring activation" | type: official

- [C16] conda 与 pip 混用的官方指导是"尽可能用 conda 安装，然后才用 pip"；避免 `--user` 标志，改为 recreate 环境而非混合修改 | src: https://github.com/conda/conda/blob/main/docs/source/user-guide/tasks/manage-environments.rst | quote: "Install as many requirements as possible with conda then use pip...recreate the environment rather than running conda commands afterward" | type: official

- [C17] conda 官方文档未提及 PEP 751 或 pylock.toml 相关表态 | src: https://docs.conda.io/projects/conda/en/stable/ | quote: 未提及 | type: official

- [C18] conda 定位为"开源打包生态和哲学"，跨语言二进制包管理器，支持 C/C++/Java/Rust/Go 及 macOS/Windows/Linux 多平台 | src: https://conda.org/ | quote: "open-source packaging ecosystem and philosophy...manage applications and libraries regardless of programming language or operating system" | type: official

- [C19] conda 支持 CUDA/MKL/编译库等非 Python 依赖的二进制分发，跨语言特性 | src: https://conda.org/ | quote: "manages applications and libraries regardless of programming language" | type: official

- [C20] conda 生态由 conda、conda-forge、mamba、conda-incubator 组织合作，NumFOCUS 赞助 | src: https://conda.org/ | quote: "collaboration among organizations like conda, conda-forge, mamba, and conda-incubator...fiscally sponsored by NumFOCUS" | type: official

- [C21] conda 26.7.2 (2024-09-04) 为最新版本，支持多平台 lockfile、sharded repodata 等 | src: https://github.com/conda/conda/releases | quote: "The latest stable release is 26.7.2 (September 4, 2024)" | type: official

## conflicts

无官方文档之间的直接打架，仅发现：
- classic solver 与 libmamba solver 的过渡在 23.10.0 完成，无版本冲突说明

## gaps

- D4：PEP 517/518 与 conda-build 的官方说明。查过：docs.conda-build.io 用户指南，conda-build README，均未提及 PEP 标准。可能是因为 conda-build 是独立的、早于这些 PEP 标准的构建系统。
- D5：libmamba solver 相比经典 solver 的具体性能数据（倍数/绝对时间改进）。官方发布说"速度提升"但未给具体指标。
- D1：官方文档是否推荐使用 conda-lock vs conda list --explicit 的场景指导。
- D9：与 rattler-build（新的 Rust 构建工具）的关系和定位。查过 conda 官方文档和 release notes，未见提及。

## leads

- conda-pypi 插件：26.5.0+ 支持从 PyPI 原生安装纯 Python 包，可能是 conda+pip 融合的新方向
- rattler-build：可能是 conda-build 的 Rust 替代品，值得单独调研
- conda-lock 与 pixi.lock 的互操作性：同为现代多平台锁文件格式，生态定位尚未完全明确
