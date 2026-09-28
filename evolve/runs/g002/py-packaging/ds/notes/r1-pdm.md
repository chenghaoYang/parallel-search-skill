# r1-pdm
question: PDM 在清单、锁文件（含是否读写 PEP 751 pylock.toml）、workspace、CPython、构建后端、依赖组、迁入、CI 缓存、私有源上的官方做法是什么？
checked: https://pdm-project.org/latest/usage/lockfile/, https://pdm-project.org/latest/usage/lock-targets/, https://pdm-project.org/latest/usage/dependency/, https://pdm-project.org/latest/usage/project/, https://pdm-project.org/latest/usage/config/, https://pdm-project.org/latest/usage/venv/, https://pdm-project.org/latest/usage/pep582/, https://pdm-project.org/latest/usage/workspace/, https://pdm-project.org/latest/usage/advanced/, https://pdm-project.org/latest/reference/pep621/, https://pdm-project.org/latest/reference/build/, https://pdm-project.org/latest/reference/configuration/, https://pdm-project.org/latest/reference/cli/, https://github.com/pdm-project/pdm/blob/main/CHANGELOG.md

## claims
- [C1] D1 元数据在 pyproject.toml 的 [project]，规范 PEP 621、631、639。 | src: https://pdm-project.org/latest/reference/pep621/ | quote: "The project metadata are stored in the pyproject.toml." | type: official
- [C2] D1 [tool.pdm].distribution=true 时当库。 | src: https://pdm-project.org/latest/usage/project/ | quote: "PDM will treat the project as a library." | type: official
- [C4] D1 非元数据在 [tool.pdm.resolution]，如 allow-prereleases。 | src: https://pdm-project.org/latest/usage/config/ | quote: "setting allow-prereleases to true in [tool.pdm.resolution] table" | type: official
- [C5] D9 [[tool.pdm.source]] type 默认 index，或 find_links。 | src: https://pdm-project.org/latest/usage/config/ | quote: "index or find_links, default to index" | type: official
- [C6] D1 pdm config --local 写在项目根 pdm.toml。 | src: https://pdm-project.org/latest/usage/config/ | quote: "Any local configurations will be stored in pdm.toml under the project root directory." | type: official
- [C7] D2 默认锁 pdm.lock，含包文件名与 hashes。 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "The file names and hashes of the packages" | type: official
- [C8] D2 格式 pdm（pdm.lock）或 pylock（pylock.toml），默认 pdm。切换 pdm config lock.format pylock（2.25.0 实验）。 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "default file name is `pdm.lock`) and `pylock`" | type: official
- [C9] D2 导出另命令 pdm export -f pylock -o pylock.toml（Added in 2.24.0）。 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "exporting to pylock.toml format as defined by PEP 751." | type: official
- [C10] D2 最早 opt-in pylock 锁格式：changelog v2.25.0（2025-06-13）。导出更早，v2.24.0。 | src: https://github.com/pdm-project/pdm/blob/main/CHANGELOG.md | quote: "make it opt-in by config." | type: official
- [C11] D2 另选锁：-L/--lockfile 或 PDM_LOCKFILE。组记在 metadata.groups。 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "the -L/--lockfile option or the PDM_LOCKFILE environment variable" | type: official
- [C12] D2 默认锁覆盖 requires-python 内全部平台（Added in 2.17.0）。 | src: https://pdm-project.org/latest/usage/lock-targets/ | quote: "works on all platforms within the Python versions specified by requires-python" | type: official
- [C13] D2 默认 cross-platform；该策略旗标 Deprecated in 2.17.0。 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "By default, the generated lockfile is cross-platform" | type: official
- [C14] D2 URL 里的环境变量在锁文件中不展开。 | src: https://pdm-project.org/latest/reference/pep621/ | quote: "kept untouched in the lock file." | type: official
- [C16] D3 键 [tool.pdm.workspace].members（路径或 glob）。Added in 2.28.0。changelog 最早 v2.28.0（2026-06-23）。 | src: https://pdm-project.org/latest/usage/workspace/ | quote: "direct paths and glob patterns." | type: official
- [C17] D3 成员互相按包名依赖时，从 checkout 以 editable 解析。 | src: https://pdm-project.org/latest/usage/workspace/ | quote: "PDM resolves it from the workspace checkout as an editable package." | type: official
- [C18] D3 共享根环境与根锁。install/lock/sync/outdated/info 必须在根上跑。 | src: https://pdm-project.org/latest/usage/workspace/ | quote: "Workspace members share the workspace root's environment and lock file." | type: official
- [C19] D4 默认 virtualenv，不是 PEP 582。python.use_venv False 才改 __pypackages__。 | src: https://pdm-project.org/latest/usage/venv/ | quote: "By default pdm is configured to use virtual environment instead of PEP 582." | type: official
- [C20] D4 解释器不是 venv 时，依赖装进项目根 __pypackages__。 | src: https://pdm-project.org/latest/usage/project/ | quote: "__pypackages__ will be created in the project root and dependencies will be installed into it." | type: official
- [C21] D4 pdm python install 装 CPython（示例 3.9.8，Added in 2.13.0）。python.install_root 默认 ~/.local/share/pdm/python。 | src: https://pdm-project.org/latest/usage/project/ | quote: "with the `pdm python install` command." | type: official
- [C22] D4 路径钉在 .pdm-python。2.23.0 起可读 .python-version 或 PDM_PYTHON_VERSION。范围在 requires-python。 | src: https://pdm-project.org/latest/usage/project/ | quote: "The interpreter path will be stored in .pdm-python" | type: official
- [C23] D5 项目页称默认后端 pdm-backend。构建页不强制；其代码块 build-backend 为 pdm.backend。poetry-core 不支持。 | src: https://pdm-project.org/latest/reference/build/ | quote: "PDM does not force you to use a specific build backend." | type: official
- [C24] D5 存在 pdm build 与 pdm publish。 | src: https://pdm-project.org/latest/reference/cli/ | quote: "Build and publish the project to PyPI" | type: official
- [C25] D6 仅 -d/--dev 时写入 [dependency-groups] 的 dev 组（Added in 1.5.0）。 | src: https://pdm-project.org/latest/usage/dependency/ | quote: "dev group under [dependency-groups] by default." | type: official
- [C26] D6 v2.20.0（2024-10-31）起默认写入 [dependency-groups]（PEP 735）。 | src: https://github.com/pdm-project/pdm/blob/main/CHANGELOG.md | quote: "dev dependencies will be written to [dependency-groups] table." | type: official
- [C27] D7 import 支持 Pipfile、Poetry、Flit、requirements.txt、setup.py。 | src: https://pdm-project.org/latest/usage/project/ | quote: "PDM provides `import` command" | type: official
- [C28] D7 import 位置参数 filename。changelog v0.6.0 原文命令是 pmd import。 | src: https://pdm-project.org/latest/reference/cli/ | quote: "Import project metadata from other formats" | type: official
- [C29] D8 CI 点名 Action pdm-project/setup-pdm，示例为 @v4。 | src: https://pdm-project.org/latest/usage/advanced/ | quote: "there is pdm-project/setup-pdm to make this process easier." | type: official
- [C30] D8 cache_dir 默认 ~/.cache/pdm，环境变量 PDM_CACHE_DIR。 | src: https://pdm-project.org/latest/reference/configuration/ | quote: "The root directory of cached files ~/.cache/pdm PDM_CACHE_DIR" | type: official
- [C31] D9 name=pypi 的 source 替换默认索引。凭证用 pypi.<name>.username/password。 | src: https://pdm-project.org/latest/usage/config/ | quote: "set the source name to pypi and that source will replace it." | type: official
- [C32] D9 URL 与凭证分开存。keyring 索引服务名 pdm-pypi-<name>。 | src: https://pdm-project.org/latest/usage/config/ | quote: "The service name will be pdm-pypi-<name> for an index" | type: official

## conflicts
- 锁页 “only the requirements.txt format is supported.” 与后文 pylock 导出、CLI 的 requirements.txt or pylock.toml 并存。https://pdm-project.org/latest/usage/lockfile/ https://pdm-project.org/latest/reference/cli/
- 最低 Python：项目页 3.9 and above；changelog v2.27.0 to 3.10；CI 页 Python < 3.7。https://pdm-project.org/latest/usage/project/ https://github.com/pdm-project/pdm/blob/main/CHANGELOG.md https://pdm-project.org/latest/usage/advanced/
- cross_platform Deprecated in 2.17.0，同页仍默认 cross-platform；lock-targets 仍默认全平台。https://pdm-project.org/latest/usage/lockfile/ https://pdm-project.org/latest/usage/lock-targets/

## gaps
- hash 算法名未写。无 pylock import 子命令（只有 lock.format 与 export -f pylock）。
- CI 未点名 actions/cache path/key。install.cache 在 $(pdm config cache_dir)/packages。
- dependency 页未写是否仍读 [tool.pdm.dev-dependencies]（changelog v2.22.4 还有该表）。import -f 枚举未列出。

## leads
- 须提交 pyproject.toml，应提交 pdm.lock 与 pdm.toml，勿提交 .pdm-python。https://pdm-project.org/latest/usage/project/
- 另一 monorepo 用 dependency-groups 的 file:// 与单一 pdm.lock，未写废弃 workspace。https://pdm-project.org/latest/usage/advanced/
