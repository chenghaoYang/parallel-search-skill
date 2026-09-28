# r1-conda
question: conda 官方文档 + conda-lock 项目文档在下列方面怎么说：(D2) conda 本身有没有官方锁文件机制（`environment.yml` 是不是锁文件还是仅声明式依赖），conda-lock 产出的锁文件是什么格式、是否官方推荐；(D4) `conda create -n env python=3.x` 这种方式怎么管理 Python 版本，conda 是否把 Python 本身当作一个可安装的包版本管理；(D5) conda 的环境管理机制（`conda env`，环境存放位置，`activate`/`deactivate`）；(D8) conda 能否管理非 Python 二进制依赖（这是 conda 最核心的卖点，找官方原句，例如 CUDA、MKL、编译器工具链等例子）；(D9) 私有 channel 怎么配置认证（例如 anaconda.org 私有 channel、token）；(D10) 官方 GitHub Actions 缓存方案（例如 `conda-incubator/setup-miniconda` 的 cache 用法，或官方文档提到的缓存 `pkgs` 目录做法）；(D11) 官方有没有「从 conda 迁移到 pixi」或「从 pip/venv 迁移到 conda」这类指南。

checked: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html, https://github.com/conda/conda-lock, https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-python.html, https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/packages.html, https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html, https://github.com/conda-incubator/setup-miniconda/blob/main/README.md, https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/pip-interoperability.html, https://docs.conda.io/projects/conda/en/latest/

## claims

### D2: Lock file mechanism
- [C1] `environment.yml` 是声明式依赖描述，仅指定所需包名和版本，conda 在创建环境时调用 solver 解决依赖冲突，不保证重现性 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Installing one program at a time can lead to dependency conflicts. Installing all the programs at the same time avoids dependency conflicts." | type: official
- [C2] conda 26.5+ 官方新增原生导出锁文件能力，使用 `conda export --name my-env --file conda-lock.yaml` 生成跨平台精确锁文件 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Modern conda supports multi-platform lock files (available in conda 26.5+). These capture exact packages, versions, builds, and channels needed to recreate environments precisely" | type: official
- [C3] conda-lock 是由 conda 官方组织维护的社区工具，产出 `conda-lock.yml` 格式锁文件 | src: https://github.com/conda/conda-lock | quote: "Conda lock is a lightweight library that can be used to generate fully reproducible lock files for conda environments" | type: official
- [C4] conda-lock 生成的锁文件通过 `@EXPLICIT` 格式在重建环境时绕过 solver，直接安装指定的精确包版本 | src: https://docs.conda.io/projects/conda/en/stable/commands/export.html | quote: "@EXPLICIT lockfiles allow you to (re)create environments without invoking the solver" | type: official
- [C5] conda-lock 支持多平台输出格式：统一 `conda-lock.yml` 或平台专用 explicit locks | src: https://github.com/conda/conda-lock | quote: "platform-specific explicit locks named like `conda-{platform}.lock`" | type: official

### D4: Python version management
- [C6] conda 把 Python 本身当作可安装包进行版本管理："Conda treats Python the same as any other package, so it is easy to manage and update multiple installations" | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-python.html | quote: "Conda treats Python the same as any other package, so it is easy to manage and update multiple installations" | type: official
- [C7] `conda create -n myenv python=3.9` 通过版本指示符指定 Python 小版本，每个版本在独立环境中安装 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-python.html | quote: "To create an environment with a particular Python version, use: conda create -n myenv python=3.9" | type: official
- [C8] conda 目前支持 Python 3.10, 3.11, 3.12, 3.13, 3.14，可用 `conda search --full-name python` 查看所有可用版本 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-python.html | quote: "Conda supports Python 3.10, 3.11, 3.12, 3.13, and 3.14" | type: official
- [C9] 更新 Python 版本用 `conda update python` 升级到最新发布版或 `conda install python=3.10` 钉死小版本 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-python.html | quote: "You can update to the latest Python release using `conda update python`, which upgrades to the newest major release" | type: official

### D5: Environment management
- [C10] conda 默认环境存储路径为 `/envs/`，可用 `--prefix` 标志指定自定义位置 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "By default, conda stores environments in `/envs/`. You can also specify custom locations using the `--prefix` flag" | type: official
- [C11] 激活环境执行两项关键操作：向系统 PATH 添加条目、执行环境激活脚本设置必要的环境变量 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Activation performs two critical functions: it adds entries to the system PATH and runs activation scripts that set necessary environment variables" | type: official
- [C12] 激活：`conda activate myenv`，停用：`conda deactivate` | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "To activate: `conda activate myenv`. To deactivate: `conda deactivate`" | type: official
- [C13] 对于不明确激活的命令执行，可用 `conda run` 在环境中执行命令而无需激活 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "You can also use `conda run` to execute commands in an environment without explicitly activating it" | type: official

### D8: Non-Python binary dependencies
- [C14] conda 包含系统级库、Python 或其他模块、可执行程序等多种内容，不限于 Python | src: https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/packages.html | quote: "system-level libraries. Python or other modules. executable programs and other components" | type: official
- [C15] 数据科学库和工具由 conda 分发，使用优化的硬件特定库（如 Intel 的 MKL 或 NVIDIA 的 CUDA）以加速性能 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/data-science.html | quote: "Data science libraries and tools provided by Conda are built using optimized, hardware-specific libraries such as Intel's MKL or NVIDIA's CUDA, which speed up performance" | type: official
- [C16] conda 通过 MKL 跟踪特性实现 BLAS 库选择，MKL 无任何 track_features 关联，使其为默认选项 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/pkg-specs.html | quote: "the MKL package is chosen over OpenBLAS because MKL does not have any track_features associated with it" | type: official
- [C17] CUDA 工具链和 CuPy 等 CUDA 加速库通过 conda-forge 作为原生 conda 包提供 | src: https://github.com/conda-forge/cudatoolkit-feedstock | quote: "cudatoolkit-feedstock: A conda-smithy repository for cudatoolkit" | type: secondary
- [C18] Conda-build 提供特殊 jinja2 函数 `compiler()` 便于在多平台动态指定编译器包 | src: https://docs.conda.io/projects/conda-build/en/latest/resources/compiler-tools.html | quote: "Conda-build 3 defines a special jinja2 function, compiler(), to make it easy to specify compiler packages dynamically on many platforms" | type: official

### D9: Private channel authentication
- [C19] `add_anaconda_token` 配置与 anaconda-client 联动，自动将私有 token 嵌入 anaconda.org 私有 channel 的访问 URL | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html | quote: "add_anaconda_token setting used in conjunction with the anaconda command-line client" | type: official
- [C20] conda 支持在 channel URL 中通过环境变量展开嵌入凭证，例如 `https://${USERNAME}:${PASSWORD}@my.private.conda.channel` | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html | quote: "expands environment variables in a subset of configuration settings including channels and custom multichannels" | type: official
- [C21] `channel_settings` 配置允许为单个 channel 定义额外选项并通过 Auth Handlers 插件系统注册自定义认证处理器 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html | quote: "channel_settings configuration allows defining extra configuration options for individual channels" | type: official
- [C22] conda 支持 channel 的白名单/黑名单机制，黑名单优先于白名单，若 channel 同时出现在两个列表中则被拒绝 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html | quote: "the denylist takes precedence over the allowlist. If a channel is in both lists, it is denied" | type: official

### D10: GitHub Actions caching
- [C23] setup-miniconda GitHub Action 默认缓存目录为 `~/conda_pkgs_dir` | src: https://github.com/conda-incubator/setup-miniconda/blob/main/README.md | quote: "uses `~/conda_pkgs_dir` as the default cache path for conda packages" | type: official
- [C24] 使用 `actions/cache@v5` 结合 `~/conda_pkgs_dir` 路径和基于 `environment.yml` 内容哈希的 key 进行缓存 | src: https://github.com/conda-incubator/setup-miniconda/blob/main/README.md | quote: "key: ${{ runner.os }}-conda-${{ hashFiles('environment.yml') }}" | type: official
- [C25] 缓存正常运作的前提条件：必须将 setup-miniconda 的 `use-only-tar-bz2` 选项设为 `true` | src: https://github.com/conda-incubator/setup-miniconda/blob/main/README.md | quote: "For caching to work properly, you will need to set the `use-only-tar-bz2` option to `true`" | type: official
- [C26] 可通过 setup-miniconda 的 `pkgs-dirs` 选项自定义缓存目录位置（例如 Windows 上的 D: 盘可改善解压性能） | src: https://github.com/conda-incubator/setup-miniconda/blob/main/README.md | quote: "You may also set conda's package directories (`pkgs_dirs`) config value using the `pkgs-dirs` option" | type: official

### D11: Migration guides
- [C27] conda 官方文档中讨论了 pip-conda 互操作性，现已弃用旧的 `prefix_data_interoperability` 配置，转而推荐使用 `conda-pypi` 包 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/pip-interoperability.html | quote: "Conda now supports pip-installed packages using the `conda-pypi` package" | type: official
- [C28] conda 与 pipenv/Poetry 的本质区别在于后者基于 Python 内置 venv，而 conda 有独立的低层次虚环境概念，其中 Python 本身作为依赖 | src: https://docs.conda.io/projects/conda/en/4.14.x/user-guide/concepts/environments.html | quote: "Pipenv and Poetry are based around Python's built-in venv library, whereas conda has its own notion of virtual environments that is lower-level (Python itself is a dependency provided in conda environments)" | type: official
- [C29] 官方建议混合使用 conda 和 pip 时，应先用 conda 安装尽可能多的包，仅在最后阶段用 pip 补充 conda 无法提供的包 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/pip-interoperability.html | quote: "When combining conda and pip, it is best to use an isolated conda environment. Only after conda has been used to install as many packages as possible should pip be used" | type: official

## conflicts

## gaps
- D11: 未找到官方「从 pip/venv 迁移至 conda」的独立指南文档，仅有互操作性讨论
- D2: 官方文档未显式说明 conda-lock 是否被官方推荐（仅列举为可用工具）
- D8: 未找到 CUDA 本身作为官方推荐 conda 包的官方文档原句，仅在 conda-forge 生态中存在

## leads
- conda 26.5+ 原生锁文件支持是最近新功能，值得确认是否将取代 conda-lock
- conda-lock 与 pixi 对比时需明确：pixi 原生内置 lock，conda 需要第三方工具或官方新功能
- 建议查阅 conda-lock 完整文档 (readthedocs 或 GitHub) 以获得维护方、推荐用法、版本历史信息

