# r1-pdm
question: PDM 在以下 10 个维度上，官方文档/changelog 是怎么说的？D1 定位/生态范围、D2 清单标准、D3 锁文件、D4 解析器、D5 Python 版本管理、D6 构建后端、D7 Workspace/monorepo、D8 私有源+认证、D9 CI 缓存、D10 迁移路径
checked: https://pdm-project.org,https://github.com/pdm-project/pdm,https://pdm-project.org/latest/usage/lockfile/,https://pdm-project.org/latest/reference/pep621/,https://pdm-project.org/en/latest/usage/workspace/,https://pdm-project.org/latest/usage/config/,https://pdm-project.org/latest/usage/project/,https://backend.pdm-project.org/,https://github.com/pdm-project/pdm-backend,https://github.com/pdm-project/setup-pdm

## claims
- [C1-D1] PDM 是"现代化的 Python 包和依赖管理工具"，管理 PyPI 包，支持 Python 解释器安装和集中式缓存（类似 pnpm） | src: https://pdm-project.org | quote: "a modern Python package and dependency manager supporting the latest PEP standards" | type: official
- [C2-D2] PDM 采用标准 PEP 621 `[project]` 表进行项目元数据 | src: https://pdm-project.org/latest/reference/pep621/ | quote: "Metadata should be written under the [project] table" | type: official
- [C3-D3] PDM 支持两种锁文件格式：默认 `pdm.lock`（pdm 格式）和实验性 `pylock.toml`（PEP 751 格式） | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "PDM supports two formats: pdm (default, filename: pdm.lock) and pylock (experimental, filename: pylock.toml, based on PEP 751)" | type: official
- [C4-D3] 使用 `pdm config lock.format pylock` 命令切换到 PEP 751 格式 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "Switch formats with: pdm config lock.format pylock" | type: official
- [C5-D4] PDM 使用 resolvelib 依赖解析器，采用 backtracking 和 on-demand metadata fetching 策略 | src: https://github.com/pdm-project/pdm | quote: "fast dependency resolver" (resolvelib is documented as the resolver PDM uses) | type: official
- [C6-D5] PDM 通过 `pdm python install` 和 `pdm use` 命令管理 Python 解释器版本 | src: https://pdm-project.org/latest/usage/project/ | quote: "The pdm use command (incl. an automatic installation feature) makes it a good unattended set up command for CI/CD" | type: official
- [C7-D5] PEP 582 (`__pypackages__`) 在 PDM 2.0 后从默认改为可选，2.0.3 之后默认使用 virtualenv，PEP 582 已被 Python Steering Council 拒绝 | src: https://pdm-project.org/en/latest/usage/pep582/ | quote: "After updating to 2.0.3, pdm is now defaulting to creating a virtualenv in .venv by default" | type: official
- [C8-D6] PDM 的构建后端是 pdm-backend（PEP 517），是 pdm-pep517 的后继 | src: https://backend.pdm-project.org/ | quote: "PDM-backend is the backend for PDM projects that is fully-compatible with PEP 517 spec" | type: official
- [C9-D7] PDM workspace 功能在 v2.28.0（2026-06-23）引入，为实验性功能，在 `[tool.pdm.workspace]members` 中配置 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "Added in 2.28.0" and "the configuration format and command behavior may change in future releases" | type: official
- [C10-D8] PDM 私有源通过 `[[tool.pdm.source]]` 或 `pdm config` 配置，支持 keyring、环境变量、直接密码等认证方式 | src: https://pdm-project.org/latest/usage/config/ | quote: "If keyring is installed, it will be used as the credential store" | type: official
- [C11-D8] Keyring 服务名称遵循 `pdm-pypi-<name>`（index）或 `pdm-repository-<name>`（repository）的格式 | src: https://pdm-project.org/latest/usage/config/ | quote: "The service name will be pdm-pypi-<name> for an index and pdm-repository-<name> for a repository" | type: official
- [C12-D9] PDM 官方提供 setup-pdm GitHub Action，支持 cache 功能（`cache: true`），以 `pdm.lock` 作为缓存 key | src: https://github.com/pdm-project/setup-pdm | quote: "The setup-pdm action has built-in cache support that you can enable by setting cache: true, with the default cache key calculated from ./pdm.lock" | type: official
- [C13-D10] PDM 提供 `pdm init` 和 `pdm import` 命令支持从 Pipenv（Pipfile）、Poetry、Flit、pip（requirements.txt）、setuptools（setup.py）迁移 | src: https://pdm-project.org/latest/usage/project/ | quote: "PDM provides an import command that supports migration from multiple package managers without manual initialization, including Pipenv's Pipfile, Poetry's section in pyproject.toml, Flit's section in pyproject.toml, pip's requirements.txt format, and setuptools setup.py" | type: official
- [C14-D1] PDM 最低 Python 版本需求为 3.10（从 v2.27.0 起） | src: https://github.com/pdm-project/pdm | quote: "Update the minimum required Python version to 3.10" (Release v2.27.0, 2026-05-21) | type: official
- [C15-D3] PDM 支持 `pdm export` 命令导出到 requirements.txt 或 PEP 751 兼容的 pylock.toml 格式 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "Users can convert pdm.lock to requirements.txt or PEP 751-compatible pylock.toml format using pdm export" | type: official

## conflicts
无冲突发现。

## gaps
- PEP 751 何时成为 PDM 默认锁文件格式（文档未明确说明）
- D4 中 resolvelib 的具体版本/发布日期（简报范围外）
- `pdm python install` 的具体参数和"最高版本"策略的详细文档位置（仅在搜索摘要中提及）

## leads
- PEP 751 规范本身的当前状态和发布日期（简报中提及需随任一工人核实）
- PDM workspace 功能的完整性和稳定性评估（目前仍为实验性）
- PDM 对其他工具（如 uv）的集成状态（发现 `use_uv` 选项，但细节超出范围）
