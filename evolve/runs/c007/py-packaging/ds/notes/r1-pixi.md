# r1-pixi
question: pixi 与 conda 在 D1–D8 维度上的现状（仅 pixi.sh/pixi.prefix.dev 官方文档、docs.conda.io、github.com/prefix-dev）
checked: https://pixi.prefix.dev/latest/, https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html, https://pixi.prefix.dev/latest/reference/pixi_manifest/, https://pixi.prefix.dev/latest/workspace/lock_file/, https://pixi.prefix.dev/latest/concepts/conda_pypi/, https://pixi.prefix.dev/latest/workspace/multi_environment/, https://pixi.prefix.dev/latest/build/getting_started/, https://pixi.prefix.dev/latest/deployment/authentication/, https://pixi.prefix.dev/latest/switching_from/conda/, https://pixi.prefix.dev/latest/integration/ci/github_actions/, https://pixi.prefix.dev/latest/python/tutorial/, https://pixi.prefix.dev/latest/python/pyproject_toml/, https://pixi.prefix.dev/latest/python/pytorch/, https://pixi.prefix.dev/latest/reference/cli/pixi/init/, https://docs.conda.io/en/latest/, https://conda-forge.org/, https://github.com/prefix-dev/pixi, https://github.com/prefix-dev/rattler-build, https://github.com/prefix-dev/pixi/issues/1172, https://raw.githubusercontent.com/prefix-dev/pixi/main/pixi.lock

## claims

### D1 定位
- [C1] pixi 自我定位是「建立在 conda 生态之上的跨平台多语言包管理器+工作流工具」 | src: https://github.com/prefix-dev/pixi | quote: "a cross-platform, multi-language package manager and workflow tool built on the foundation of the conda ecosystem" | type: official
- [C2] 文档首页定位 | src: https://pixi.prefix.dev/latest/ | quote: "a fast, modern, and reproducible package management tool for developers of all backgrounds" | type: official
- [C3] pixi 与 conda 理念差异：conda 管环境，pixi 管 workspace（含 manifest、pixi.lock、.pixi 目录） | src: https://pixi.prefix.dev/latest/switching_from/conda/ | quote: "`Conda` and `mamba` focus on managing environments, while `pixi` emphasizes workspaces." | type: official
- [C4] 两种 manifest 写法：pixi.toml 是 workspace manifest；也支持 pyproject.toml，结构相同 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "The `pixi.toml` is the workspace manifest… We also support the `pyproject.toml` file. It has the same structure as the `pixi.toml` file." | type: official

### D2 锁文件
- [C5] pixi.lock 为 YAML、带版本号、向后不向前兼容 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "The lock file also has a version number… Pixi is backward compatible with the lock file, but not forward compatible." | type: official
- [C6] 实际 pixi.lock 为 YAML、当前 version: 7（文档示例仍写 version: 6） | src: https://raw.githubusercontent.com/prefix-dev/pixi/main/pixi.lock | quote: "version: 7\nplatforms:\n- name: linux-64" | type: official
- [C7] 锁文件覆盖 conda+pypi 两种包、按所有 environment×platform 求解 | src: https://pixi.prefix.dev/latest/workspace/lock_file/ | quote: "the versions in the lock file are compatible with the requirements in the manifest file, for both `conda` and `pypi` packages." | type: official
- [C8] conda 26.5+ 已原生支持锁文件（含 conda-lock.yaml 与 pixi.lock） | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "Conda supports `conda-lock.yaml` and `pixi.lock` natively… Lockfile support is available in conda 26.5 and later." | type: official
- [C9] PEP 751 交叉：issue #3889 请求导出 pylock.toml；维护者称 conda 依赖无法用 pylock 表达，pixi.lock 仍为主锁 | src: https://github.com/prefix-dev/pixi/issues/3889 | quote: "we would never be able to capture \"everything\" as the conda dependencies can not be properly represented in the `pylock.toml` file… The primary lockfile for pixi will probably have to continue to be `pixi.lock`" | type: official
- [C10] conda-lock 是独立项目（github.com/conda/conda-lock），pixi.lock 当初选 YAML 部分为兼容它 | src: https://github.com/prefix-dev/pixi/issues/1172 | quote: "the main reason YAML has been chosen for `pixi.lock` was to stay compatible with conda-lock" | type: official

### D3 元数据
- [C11] pyproject.toml 中 pixi 表前缀 tool.pixi；[project] 的 requires-python→conda python 依赖、dependencies→pypi-dependencies、optional-dependencies/dependency-groups→同名 feature | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "Pixi understands that field and automatically adds the version to the dependencies… automatically adds the dependencies to the workspace as `[pypi-dependencies]`" | type: official
- [C12] [tool.pixi.workspace] 必填 channels、name、platforms | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "The minimally required information in the `workspace` table is: channels, name, platforms" | type: official

### D4 workspace/monorepo
- [C13] feature=可复用片段，environment 由 feature 组合而成，定义在 [environments] 表 | src: https://pixi.prefix.dev/latest/workspace/multi_environment/ | quote: "reusable parts that can be shared between environments… Environments are defined in the `pixi.toml` under the `[environments]` table." | type: official
- [C14] 顶层表=隐式 default feature；支持 solve-group、no-default-feature；面向大型多场景工作区 | src: https://pixi.prefix.dev/latest/workspace/multi_environment/ | quote: "This prepares `pixi` for use in large workspaces with multiple use-cases, multiple developers and different CI needs." | type: official

### D5 Python 版本管理
- [C15] Python 解释器本身是 conda-forge 的 conda 包，随环境安装；版本由 requires-python 驱动 | src: https://pixi.prefix.dev/latest/python/tutorial/ | quote: "The Python interpreter is also installed into the environment… the Python interpreter version is read from the `requires-python` field… Pixi automatically manages/bootstraps the Python interpreter for you" | type: official

### D6 构建后端
- [C16] pixi build 仍为 preview，需 workspace.preview=["pixi-build"]；后端 pixi-build-python/cmake/rattler-build/ros/r/rust/mojo；pixi publish 产出 .conda 并上传 | src: https://pixi.prefix.dev/latest/build/getting_started/ | quote: "the build feature is still in preview… By specifying `package.build.backend` and `package.build.channels` you determine which backend is used" | type: official
- [C17] pixi-build-python 把 Python 包转成 conda 包 | src: https://pixi.prefix.dev/latest/build/getting_started/ | quote: "`hatchling` creates a Python package, and `pixi-build-python` turns the Python package into a conda package." | type: official
- [C18] rattler-build 是独立 Rust 工具，conda-build 的更快替代，吃 recipe.yaml | src: https://github.com/prefix-dev/rattler-build | quote: "a universal Conda package builder for Windows, macOS and Linux (like conda-build but faster)… does not have any dependencies on `conda-build` or Python" | type: official

### D7 环境模型
- [C19] conda 环境=带前缀的目录，可含非 Python 软件（官方示例 environment.yml 装 nodejs=16.13.*）；conda 跨语言 | src: https://docs.conda.io/en/latest/ | quote: "Conda provides package, dependency, and environment management for any language." | type: official
- [C20] conda 生态只装二进制包 | src: https://pixi.prefix.dev/latest/concepts/conda_pypi/ | quote: "a cross-platform, cross-language package ecosystem… it always installs binary packages" | type: official
- [C21] CUDA 走 conda 虚拟包机制：__cuda、cuda-version/cudatoolkit 是普通依赖，platform 上声明 cuda="12.0" | src: https://pixi.prefix.dev/latest/python/pytorch/ | quote: "The `cuda-version` package constraints the version of the `__cuda` virtual package and `cudatoolkit` package." | type: official
- [C22] pixi 无 base 环境；环境存于工作区 .pixi 目录 | src: https://pixi.prefix.dev/latest/switching_from/conda/ | quote: "Pixi does not have a base environment" | type: official
- [C23] pixi 能装 PyPI 包：conda-first 策略，[pypi-dependencies]，uv 作为库（非独立工具）做 PyPI 求解 | src: https://pixi.prefix.dev/latest/concepts/conda_pypi/ | quote: "Pixi can install packages from both ecosystems, but it uses a conda-first approach… Pixi uses the `uv` library to handle PyPI packages." | type: official
- [C24] conda 与 pypi 同时声明时优先 conda | src: https://pixi.prefix.dev/latest/concepts/conda_pypi/ | quote: "Pixi will install the conda package (and not the PyPI package) if both are available and specified as dependencies." | type: official

### D8 操作性
- [C25] setup-pixi GH Action：prefix-dev/setup-pixi@v0.10.0，cache:true 默认在有 pixi.lock 时启用并按 lock 哈希缓存 | src: https://pixi.prefix.dev/latest/integration/ci/github_actions/ | quote: "By default, project environment caching is enabled if a `pixi.lock` file is present… use the `pixi.lock` file to generate a hash" | type: official
- [C26] 私有 channel 认证：pixi auth login <host>；OAuth(prefix.dev)、--token(Bearer)、--conda-token(anaconda.org/quetz)、basic auth、S3；凭据存系统 keychain，fallback ~/.rattler/credentials.json，可用 RATTLER_AUTH_FILE；keyring/.netrc 仅用于 PyPI | src: https://pixi.prefix.dev/latest/deployment/authentication/ | quote: "You can authenticate Pixi with a server like prefix.dev, a private quetz instance, anaconda.org, or any S3-compatible bucket." | type: official
- [C27] 迁移：pixi init --import <ENVIRONMENT_FILE> 导入 environment.yml；反向 pixi workspace export conda-environment（--from-lockfile 出冻结版） | src: https://pixi.prefix.dev/latest/reference/cli/pixi/init/ | quote: "`--import (-i) <ENVIRONMENT_FILE>` — Environment.yml file to bootstrap the workspace" | type: official

## conflicts
- pixi.lock 序列化格式：官方文档+仓库实物为 YAML（version: 7，见 C5/C6）；但 mintlify 镜像 prefix-dev-pixi.mintlify.app 的搜索快照称其为 "custom TOML-based format"（未直接抓取该页，存疑）；issue #1172（YAML→TOML 提议）已关闭但评论不可见，无法确认是否采纳。
- 文档示例锁版本 `version: 6` vs 仓库实际 `version: 7`（文档滞后，非实质冲突）。

## gaps
- issue #3889（export pylock.toml）当前状态未确认：搜索快照显示讨论，未取到 open/closed。
- 「每个 environment 可各用不同 Python 版本」无直接原句；仅 feature 示例 [feature.py39] 暗示。
- conda-lock 项目当前活跃度未查（conda 26.5 已原生支持其格式）。
- pixi build GA 时间线未知，仅 "still in preview"。

## leads
- conda 26.5 原生支持 conda-lock.yaml/pixi.lock 是近期大变化，主文档 D2 值得单独强调。
- detached-environments 配置可模拟 conda 全局环境位置；pixi global ≈ pipx/condax。
- python-freethreading conda 包可装自由线程解释器；pixi 支持 PEP 723 脚本内嵌 manifest（--script）。
