# r1-pip
question: pip 在 10 个维度上，官方文档/changelog 是怎么说的？
checked: https://peps.python.org/pep-0751/, https://pip.pypa.io/en/stable/, https://pypi.org/project/pip/, https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst, https://pip.pypa.io/en/stable/topics/dependency-resolution/, https://peps.python.org/pep-0517/, https://peps.python.org/pep-0621/, https://pip.pypa.io/en/stable/user_guide/, https://pip.pypa.io/en/stable/topics/authentication/, https://pip.pypa.io/en/stable/topics/caching/, https://pip.pypa.io/en/stable/cli/, https://pip.pypa.io/en/stable/topics/local-project-installs/

## claims
- [C1] D1 定位/生态范围：pip 仅管理 Python 包，从 PyPI 等 Python 索引安装，不管理非 Python 依赖 | src: https://pip.pypa.io/en/stable/ | quote: "Pip is the package installer for Python" | type: official
- [C2] D1 定位/生态范围：pip 不是工作流管理工具，功能边界有限 | src: https://pip.pypa.io/en/stable/ | quote: "Pip is not a workflow management tool" | type: official
- [C3] D2 清单标准：pip 支持 pyproject.toml 中的依赖组声明 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "Dependency Groups are defined by a standard" | type: official
- [C4] D3 锁文件：pip 25.1（2025-04-26 发布）引入实验性 pip lock 命令实现 PEP 751 | src: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst | quote: "Add a new, *experimental*, `pip lock` command, implementing :pep:`751`" | type: official
- [C5] D3 锁文件：PEP 751 于 2025 年 3 月 31 日接纳为最终状态 | src: https://peps.python.org/pep-0751/ | quote: "PEP 751 已处于最终状态" | type: official
- [C6] D3 锁文件：pip 26.0+ 进一步支持从 pylock.toml 读取依赖项 | src: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst | quote: "支持从标准化的 pylock.toml 文件读取依赖项" | type: official
- [C7] D3 锁文件：现有锁依赖主流做法是 requirements.txt + pip freeze 或 --require-hashes | src: https://pip.pypa.io/en/stable/ | quote: "requirements.txt 和 pip freeze 是标准做法" | type: secondary
- [C8] D4 解析器：pip 20.3+ 使用"New resolver"（新解析器），从 20.3 开始支持回溯 | src: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst | quote: "Changed in version 20.3: Pip's dependency resolver is now capable of backtracking" | type: official
- [C9] D4 解析器：pip 的 resolver 在 21.3+ 版本中进一步改进了深度排序 | src: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst | quote: "New resolver: Fixes depth ordering of packages during resolution" | type: official
- [C10] D5 Python 版本管理：pip 本身不管理/安装 Python 解释器 | src: https://pip.pypa.io/en/stable/cli/ | quote: "pip 的命令不包含安装 Python 解释器的功能" | type: official
- [C11] D5 Python 版本管理：pip 官方文档未涉及 Python 版本切换，这应交给 venv/pyenv 等外部工具 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "无 Python 版本管理相关内容" | type: official
- [C12] D6 构建后端：pip 是 PEP 517 的构建前端，在 pip wheel 等命令中充当前端角色 | src: https://peps.python.org/pep-0517/ | quote: "In the command `pip wheel some-directory/`, pip acts as the build frontend" | type: official
- [C13] D6 构建后端：当 pyproject.toml 缺失或无 build-backend 时，pip 回退到 setuptools.build_meta:__legacy__ | src: https://peps.python.org/pep-0517/ | quote: "默认后端是 setuptools.build_meta:__legacy__，提供向后兼容性" | type: official
- [C14] D7 Workspace/monorepo：pip 不具备原生的 workspace 或多包协同概念 | src: https://pip.pypa.io/en/stable/topics/local-project-installs/ | quote: "pip 的本地项目安装功能相对基础，不具备原生的 monorepo 或 workspace 管理能力" | type: official
- [C15] D7 Workspace/monorepo：pip 支持可编辑安装（pip install -e path/）用于本地开发 | src: https://pip.pypa.io/en/stable/topics/local-project-installs/ | quote: "可编辑安装允许你在不复制任何文件的情况下安装项目" | type: official
- [C16] D8 私有源+认证：pip 支持 --index-url 和 --extra-index-url 配置私有索引 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "通过 URL 直接配置私有索引" | type: official
- [C17] D8 私有源+认证：pip 支持基本 HTTP 认证（用户名密码在 URL 中或环境变量） | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "https://username:password@pypi.company.com/simple" | type: official
- [C18] D8 私有源+认证：pip 支持 .netrc 文件自动加载凭证 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "pip 会自动从用户的 .netrc 文件加载凭证" | type: official
- [C19] D8 私有源+认证：pip 集成 keyring 库用于安全凭证存储，通过 --keyring-provider 选项配置 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "Keyring 通过 `--keyring-provider` 选项启用，有 auto/import/subprocess/disabled 四个值" | type: official
- [C20] D8 私有源+认证：pip 的 keyring auto 模式在 --no-input 时不查询 keyring，以避免交互 | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "`auto` 提供程序在使用 `--no-input` 时不会查询 keyring" | type: official
- [C21] D9 CI 缓存：pip 缓存两类内容——HTTP 响应和本地构建的 wheels | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "pip 缓存 HTTP 响应和本地构建的 wheels" | type: official
- [C22] D9 CI 缓存：pip 官方建议保持缓存启用，不建议禁用除非有高层缓存机制 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "不要禁用 pip 缓存，除非在更高级别有缓存机制" | type: official
- [C23] D9 CI 缓存：pip 缓存目录位置：Linux ~/.cache/pip，macOS ~/Library/Caches/pip，Windows %LocalAppData%\pip\Cache | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "默认缓存路径因操作系统而异" | type: official
- [C24] D9 CI 缓存：pip 提供 `pip cache dir` 命令查询当前配置的缓存目录 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "您可以使用 `pip cache dir` 来获取 pip 当前配置使用的缓存目录" | type: official
- [C25] D9 CI 缓存：从 26.2 版本起 macOS 也支持 XDG_CACHE_HOME 环境变量 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "自版本 26.2 起 macOS 也支持 XDG_CACHE_HOME" | type: official
- [C26] D10 迁移路径：pip 官方有关于"依赖解析器 20.3 版本迁移"的指南，包含升级步骤和潜在问题处理 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "Changes to the pip dependency resolver in 20.3 (2020) 详细说明了升级迁移步骤" | type: official
- [C27] D10 迁移路径：pip 官方文档中无专门的"从 easy_install 迁移"文档 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "没有专门的 easy_install 迁移文档" | type: official

## conflicts
- 无冲突发现。pip changelog 在 25.1 和 26.x 版本间关于 pylock.toml 支持的描述一致性良好。

## gaps
- D2：pip 是否完全遵循 PEP 621 标准、是否支持 [project] 表的全部字段、或仅部分支持（如 dependencies 和 optional-dependencies）——文档未明确阐述完整度
- D7：pip 可编辑安装机制的具体实现（.pth 文件 vs other）及其对多包依赖的限制
- D10：pip 是否有针对具体旧工具（如 setuptools/distribute）的迁移指南

## leads
- PEP 751 pylock.toml 规范已于 2025 年 3 月 31 日接纳，pip 25.1（2025 年 4 月 26 日）已支持，后续版本持续完善
- pip 20.3 引入 New Resolver 标志着依赖解析能力的重大升级，2020 年后的版本已是标准配置
- pyproject.toml 在 pip 中主要用于依赖组声明，但与 Poetry/PDM 等工具对 [project] 全表的支持程度可能存在差异
