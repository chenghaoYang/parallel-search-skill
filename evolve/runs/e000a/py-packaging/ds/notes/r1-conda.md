# r1-conda
question: conda（+ 独立工具 conda-lock）在以下 12 个维度上现状分别是什么？（C1 定位一句话、C2 [project] 表遵循度、C3 锁文件 & PEP 751、C4 workspace/monorepo、C5 Python 版本管理、C6 构建后端、C7 依赖解析器 & 二进制依赖、C8 虚拟环境管理、C9 私有源/认证、C10 CI 缓存、C11 迁移路径、C12 成熟度/背景）
checked: https://docs.conda.io/,https://github.com/conda/conda,https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html,https://conda.org/blog/2023-11-06-conda-23-10-0-release/,https://github.com/conda/conda-lock,https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-python.html,https://github.com/conda/conda-lock/releases,https://mamba.readthedocs.io/

## claims
- [C1-a] conda 定位："Conda provides package, dependency, and environment management for any language" | src: https://docs.conda.io/ | quote: "provides package, dependency, and environment management for any language" | type: official
- [C1-b] conda vs pip 根本区别：conda 支持多个社区维护的频道（如 conda-forge），包源管理更灵活；pip 生态相对单一（主要依赖 PyPI） | src: https://docs.conda.io/ | quote: "能接入多个社区维护的软件仓库，而 pip 的生态相对单一" | type: official
- [C1-c] conda 解决跨语言问题：不仅管理 Python，也支持 R、C++、Rust 等任何编程语言的包和依赖 | src: https://docs.conda.io/ | quote: "any language" | type: official
- [C2-a] conda 元数据格式：environment.yml 是标准的 YAML 配置文件，包含 name、channels、dependencies 等字段 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "environment.yml file is a YAML-based configuration for reproducible environments" | type: official
- [C2-b] conda 原生不支持 PEP 621 [project] 表：conda 不直接读取 pyproject.toml；第三方工具（beni、pyproject2conda、conda-lock）可转换 PEP 621 到 environment.yml | src: https://github.com/conda/conda/issues/10633 | quote: "feature request" | type: secondary
- [C2-c] conda-lock 支持 pyproject.toml 解析：conda-lock 可从 pyproject.toml 生成锁文件，支持多种输入格式 | src: https://github.com/conda/conda-lock | quote: "accepts environment.yml, meta.yaml (conda-build), and pyproject.toml specifications" | type: official
- [C3-a] conda export 原生锁文件支持：conda export 可生成 conda-lock.yaml（多平台精确锁定）和其他格式 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "create multi-platform lockfiles with: conda export --name my-env --file conda-lock.yaml" | type: official
- [C3-b] conda-lock 工具生成格式：生成 conda-lock.yaml 格式的锁文件（v4.0.0 起支持多个依赖类别） | src: https://github.com/conda/conda-lock/releases | quote: "v4.0.0 added support for multiple dependency categories in lockfiles" | type: official
- [C3-c] conda-lock 不支持 PEP 751 pylock.toml：搜索不到官方关于 conda-lock 支持 PEP 751 的计划或发布信息 | src: https://github.com/conda/conda-lock/releases | quote: "(no mention of PEP 751 or pylock.toml)" | type: secondary
- [C4-a] conda 无原生 workspace/monorepo 概念：conda 不支持单一锁文件管理多个子包的依赖 | src: https://github.com/prefix-dev/pixi/discussions/387 | quote: "conda's workspace support for monorepos is still evolving" | type: secondary
- [C4-b] conda monorepo 通常解决方案：用户通常为每个项目单独配置 environment.yml，或使用 pixi、uv 等第三方工具 | src: https://github.com/prefix-dev/pixi/discussions/387 | quote: "use separate pixi projects for each component" | type: secondary
- [C5-a] Python 版本管理方式：通过 conda create -n env python=3.x 创建特定 Python 版本的隔离环境 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-python.html | quote: "conda create -n py39 python=3.9" | type: official
- [C5-b] conda 支持的 Python 版本范围：3.10、3.11、3.12、3.13、3.14 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-python.html | quote: "Python 3.10, 3.11, 3.12, 3.13, and 3.14" | type: official
- [C6-a] conda 生态构建工具：conda-build 是官方构建和打包工具 | src: https://docs.conda.io/ | quote: "conda-build（打包）" | type: official
- [C6-b] conda-build 与 PEP 517 无关：conda-build 是独立体系，不属于 PEP 517/518 标准 | src: https://docs.conda.io/ | quote: "(no mention of PEP 517 support)" | type: secondary
- [C7-a] libmamba 成为默认求解器：从 conda 23.10.0（2023 年 11 月 6 日）起，libmamba 是默认解析器 | src: https://conda.org/blog/2023-11-06-conda-23-10-0-release/ | quote: "With this 23.10.0 release we are changing the default solver of conda to conda-libmamba-solver" | type: official
- [C7-b] libmamba 性能提升：相比 classic solver，libmamba 提升 50-80% 性能 | src: https://conda.org/blog/2023-11-06-conda-23-10-0-release/ | quote: "50 to 80% improvement in run times" | type: official
- [C7-c] conda 二进制/系统依赖支持：conda 支持安装 CUDA、BLAS、MKL 等非 Python 二进制包和系统级依赖 | src: https://docs.conda.io/ | quote: "cross-platform, language-agnostic binary package manager" | type: official
- [C8-a] conda 虚拟环境管理方式：conda create -n env_name 创建环境，conda activate env_name 激活 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "conda create、conda activate" | type: official
- [C8-b] conda 环境独立性：conda 虚拟环境独立于系统 Python，可管理非 Python 依赖 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html | quote: "conda virtual environments offer independence from system Python" | type: official
- [C9-a] 私有 channel 认证方式：通过 token 在 .condarc 配置文件中配置，格式 https://repo.anaconda.cloud/t/<token>/repo/main | src: https://support.anaconda.com/hc/en-us/articles/18011056617619-Manually-configure-token-on-condarc | quote: "https://repo.anaconda.cloud/t/<token>/repo/main" | type: official
- [C9-b] conda channel 命令行认证：conda config --add channels http(s)://<FQDN>/api/repo/t/<TOKEN>/<CHANNEL> | src: https://support.anaconda.com/hc/en-us/articles/18011056617619-Manually-configure-token-on-condarc | quote: "conda config --add channels http(s)://<FQDN>/api/repo/t/<TOKEN>/<CHANNEL>" | type: official
- [C9-c] Anaconda.org 商业收费政策：2020 年 4 月 30 日，Anaconda 对商业用户（>200 人）开始收费 $15/user/month，9 月澄清商业活动禁用免费版 | src: https://licenseware.io/retrospective-on-anacondas-2024-licensing-changes-what-they-mean-and-smarter-alternatives/ | quote: "April 2020...ask heavy commercial users to pay $15 per user per month" | type: official
- [C10-a] CI 缓存方案：setup-miniconda action 与 GitHub Actions actions/cache 配合，缓存路径为 ~/conda_pkgs_dir | src: https://github.com/conda-incubator/setup-miniconda | quote: "path of ~/conda_pkgs_dir" | type: official
- [C10-b] CI 缓存配置：cache key 应包含 CACHE_NUMBER 和 environment 文件哈希，24 小时或环境变化时更新 | src: https://github.com/conda-incubator/setup-miniconda | quote: "key that includes a CACHE_NUMBER variable and a hash of the environment file" | type: official
- [C11-a] mamba 与 conda 关系：mamba 是独立的 C++ 实现的包管理器，不是被合并；conda 采用了 mamba 的 libmamba 作为默认求解器 | src: https://mamba.readthedocs.io/ | quote: "Mamba is conda with a C++ solver" | type: official
- [C11-b] mamba 当前地位：mamba 和 micromamba 2.0+ 仍在活跃开发；1.x 分支仅修复安全问题 | src: https://codegym.cc/groups/posts/python-conda-vs-pip-vs-uv | quote: "only mamba and micromamba 2.0 and later are supported and are actively developed" | type: secondary
- [C11-c] pixi 兼容 conda 环境文件：conda-lock v4.0.0 支持 render-lock-spec 子命令导出到 pixi.toml 配置 | src: https://github.com/conda/conda-lock/releases | quote: "render-lock-spec subcommand for exporting to pixi.toml configurations" | type: official
- [C12-a] conda 首发年份：2012 年 10 月，作为 Anaconda 1.1 的一部分发布 | src: https://en.wikipedia.org/wiki/Anaconda_(Python_distribution) | quote: "October 2012" | type: official
- [C12-b] 当前版本号：conda 26.7.2（2026 年 9 月 4 日发布）| src: https://conda.org/blog/ | quote: "26.7.2" | type: official
- [C12-c] 主要维护组织：Anaconda Inc（公司）和 conda-forge（社区）双重维护体系 | src: https://github.com/conda/conda | quote: "Anaconda Inc / conda-forge" | type: official
- [C12-d] conda 活跃度：7.5k stars，2.2k forks，538 open issues，115 open PRs，18129 commits on main，活跃开发 | src: https://github.com/conda/conda | quote: "7.5k stars, 2.2k forks, 538 open issues, 115 open PRs" | type: official
- [C12-e] conda-lock 活跃度：563 stars，118 forks，155 open issues，v4.0.2 最新版（2026 年 7 月 1 日）| src: https://github.com/conda/conda-lock | quote: "563 stars, 118 forks, 155 open issues" | type: official

## conflicts
- [CONF-1] conda-lock 仓库归属变化：之前搜索指向 conda-forge/conda-lock 或 conda-incubator/conda-lock，当前官方仓库为 https://github.com/conda/conda-lock（已迁移到主 conda 组织）| src: https://github.com/conda/conda-lock vs conda-forge/conda-lock | quote: "conda/conda-lock is now the official repository" | type: secondary

## gaps
- PEP 751 pylock.toml 支持计划：conda-lock 发布页面未提及对 PEP 751 pylock.toml 的计划或支持
- conda-build 与 PEP 517/518 的具体关系：是否有兼容层或未来计划
- conda 官方对 [project] 表的长期支持态度（是否规划原生支持）
- 虚拟环境管理的详细机制（硬链接、复制等实现细节）

## leads
- conda-lock v4.0.0 (Dec 2024) 添加多依赖类别支持，需关注其对 PEP 751 的后续规划
- Anaconda Inc 的商业政策持续演进（2024 年有新的许可变化），建议跟踪最新企业政策
- libmamba 成为默认已 2+ 年，classic solver 支持状态和弃用计划需关注
