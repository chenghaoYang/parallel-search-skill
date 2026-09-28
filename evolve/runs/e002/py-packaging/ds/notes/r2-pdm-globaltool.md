# r2-pdm-globaltool
question: PDM 有没有类似 uvx/pipx/pixi global 的「全局安装并隔离运行 CLI 工具」机制？
checked: https://pdm-project.org/latest/reference/cli/, https://raw.githubusercontent.com/pdm-project/pdm/main/src/pdm/cli/options.py, https://raw.githubusercontent.com/pdm-project/pdm/main/docs/usage/config.md, https://raw.githubusercontent.com/pdm-project/pdm/main/docs/index.md

## claims
- [C1] PDM 的 `-g/--global` 选项定义为"Use the global project, supply the project root with `-p` option" | src: https://raw.githubusercontent.com/pdm-project/pdm/main/src/pdm/cli/options.py | quote: "help='Use the global project, supply the project root with `-p` option'" | type: official
- [C2] PDM 使用 `-g/--global` 选项时指向的是全局项目配置文件路径 `<CONFIG_ROOT>/global-project/pdm.toml`，用于项目级依赖管理，不是隔离工具运行机制 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/docs/usage/config.md | quote: "If `-g/--global` option is used, the first item will be replaced by `<CONFIG_ROOT>/global-project/pdm.toml`." | type: official
- [C3] PDM CLI 完整命令集中不存在 `tool install`、`tool run` 或任何类似名称的用于隔离运行全局工具的命令 | src: https://pdm-project.org/latest/reference/cli/ | quote: "Commands available: add, build, cache, completion, config, export, fix, import, info, init, install, list, lock, new, outdated, publish, python/py, remove, run, search, self/plugin, show, sync, update, use, venv" | type: official
- [C4] PDM 官方文档在安装说明中提到 pipx 和 uv 作为安装 PDM 本身的工具（pipx install pdm、uv tool install pdm），而不是推荐用于全局工具隔离 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/docs/index.md | quote: "uv tool install pdm" and "pipx install pdm" listed under installation methods for PDM | type: official
- [C5] PDM 的全局项目功能与 pipx/uvx/pixi 的全局工具隔离机制在语义上完全不同：PDM `--global` 是使用全局项目配置文件进行依赖管理，不提供工具级别的隔离和运行 | src: https://raw.githubusercontent.com/pdm-project/pdm/main/src/pdm/project/core.py | quote: "global_project = Path(self.global_config['global_project.path']).expanduser()" (表示全局项目是一个配置路径，非隔离环境) | type: official

## conflicts
- 无

## gaps
- PDM 是否有官方文档明确说明为什么不采用 pipx 式的全局工具隔离机制
- PDM 社区是否讨论过添加 pipx 等价物功能的 feature request

## leads
- 检查 PDM GitHub issues 中是否有关于全局工具隔离功能的讨论（关键词：tool install、global isolation、pipx equivalent）
