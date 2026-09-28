# r1-pip
question: pip 现状（D1 定位 / D2 锁文件与 PEP 751 pylock.toml / D5 Python 版本管理 / D7 环境模型 / D8 操作性）；重点：pip 是否已支持 pylock.toml
checked: https://peps.python.org/pep-0751/, https://pip.pypa.io/en/stable/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/topics/, https://pip.pypa.io/en/stable/topics/caching/, https://pip.pypa.io/en/stable/topics/workflow/, https://pip.pypa.io/en/stable/topics/authentication/, https://pip.pypa.io/en/stable/topics/python-option/, https://pip.pypa.io/en/stable/reference/requirements-file-format/, https://pip.pypa.io/en/stable/user_guide/, https://packaging.python.org/en/latest/specifications/pylock-toml/, https://github.com/pypa/pip/pull/13213

## claims
- [C1] pip 自我定位是纯安装器，不是项目管理器 | src: https://pip.pypa.io/en/stable/ | quote: "Pip is the package installer for Python." | type: official
- [C2] pip 官方 topic guide 明确「pip 不是工作流管理工具」，只管环境内已装的包 | src: https://pip.pypa.io/en/stable/topics/workflow/ | quote: "The core purpose of pip is to *manage the packages installed in your environment* ... there is no intention that pip will manage the workflow as a whole." | type: official
- [C3] 「管理 project」明确不在 pip 范围 | src: https://pip.pypa.io/en/stable/topics/workflow/ | quote: "Tasks like creating and managing environments, configuring and running development tasks ... managing the Python interpreter itself, and managing the overall \"project\", are not part of pip's scope." | type: official
- [C4] PEP 751（pylock.toml 锁文件格式）状态为 Final，2025-03-31 决议；作者 Brett Cannon，取代 PEP 665 | src: https://peps.python.org/pep-0751/ | quote: "Status: Final ... Resolution: 31-Mar-2025" | type: official
- [C5] PEP 751 正文已转为历史文档，canonical spec 在 packaging.python.org；spec 要求 lock-version="1.0" | src: https://packaging.python.org/en/latest/specifications/pylock-toml/ | quote: "This specification was originally defined in PEP 751 ... April 2025: Initial version, approved via PEP 751." | type: official
- [C6] pip 已支持 pylock.toml：`pip lock` 命令自 pip 25.1（2025-04-26）起存在，实验性 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add a new, *experimental*, `pip lock` command, implementing PEP 751." | type: official
- [C7] pip lock 实现 PR #13213「PEP 751 experimental `pip lock` command」已于 2025-04-16 合并进 25.1 milestone | src: https://github.com/pypa/pip/pull/13213 | quote: "merged_at 2025-04-16, milestone 25.1, state closed" | type: official
- [C8] `pip lock` 当前仍标注 EXPERIMENTAL；默认输出 pylock.toml（-o 可改）；锁只对当前 Python 版本与平台保证有效 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "EXPERIMENTAL - Lock packages and their dependencies ... Lock file name (default=pylock.toml) ... only guaranteed to be valid for the current python version and platform." | type: official
- [C9] `pip install` 从 pip 26.1（2026-04-26）起可用 `-r pylock.toml` 安装 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add experimental support to read requirements from standardized pylock.toml files" | type: official
- [C10] pip install 的 -r 选项文档确认接受 pylock.toml，且标注实验性 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "can be in pip's requirements.txt format, or pylock.toml format ... pylock.toml support is experimental." | type: official
- [C11] pip 26.2（2026-07-29）继续完善 pylock.toml：upload-time 字段、--only-final、冲突报错 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add support for `pylock.toml` `upload-time` field, so `--uploaded-prior-to` works with `-r pylock.toml`" | type: official
- [C12] requirements.txt 未被取代：PEP 751 明确不完全替代 requirements 文件；锁文件 multi-use vs requirements 文件 single-use | src: https://peps.python.org/pep-0751/ | quote: "This PEP does NOT fully replace requirements files ... This PEP supports multi-use lock files while requirements files are single-use." | type: official
- [C13] PEP 751 落地是各工具自愿决定，PEP 不强制 | src: https://peps.python.org/pep-0751/ | quote: "that will be a per-tool decision as to whether they choose to support this PEP" | type: official
- [C14] pylock.toml 支持仍在推进：pypa/pip 有 open issues #13952 "What's next for `-r pylock.toml`?"、#13953 "What's next for `pip lock`?"、#13961 `-c pylock.toml`、#13962 选 extras/dependency-groups | src: https://github.com/pypa/pip/issues/13952 | quote: "13952 [open] What's next for `-r pylock.toml` ? / 13953 [open] What's next for `pip lock` ?" | type: official
- [C15] pip 不管 Python 解释器本身的安装/管理（见 C3 同页）；`--python` 选项（自 22.3 起）只能指向已存在的解释器或 venv | src: https://pip.pypa.io/en/stable/topics/python-option/ | quote: "you can use the `--python` option to specify the interpreter you want to manage ... The path to a Python executable ... The path to a virtual environment" | type: official
- [C16] pip 环境模型：在「某个环境」内装包；创建/管理环境（venv 等）不在范围内（C3）；pip 用所在解释器运行 | src: https://pip.pypa.io/en/stable/user_guide/ | quote: "`python -m pip` executes pip using the Python interpreter you specified as python." | type: official
- [C17] 私有源：-i/--index-url 指定 PEP 503 simple 索引，默认 PyPI | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "Base URL of the Python Package Index (default https://pypi.org/simple)." | type: official
- [C18] --extra-index-url 追加索引；--no-index 只看 --find-links | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "Extra URLs of package indexes to use in addition to --index-url ... Ignore package index (only looking at --find-links URLs instead)." | type: official
- [C19] 私有源认证：URL 内嵌 basic auth 或 token-as-username | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "Pip supports basic HTTP-based authentication credentials ... https://username:password@pypi.company.com/simple" | type: official
- [C20] 认证还支持 .netrc 与 keyring（--keyring-provider auto/disabled/import/subprocess，可用 PIP_KEYRING_PROVIDER 配置） | src: https://pip.pypa.io/en/stable/topics/authentication/ | quote: "Pip supports loading credentials from a user's `.netrc` file ... `auto`, `disabled`, `import`, or `subprocess`" | type: official
- [C21] pip 缓存默认开启；`pip cache dir`（自 20.1）查目录；`pip cache info/list/remove/purge` 管理；`--no-cache-dir` 关闭；官方建议容器分层缓存等高层缓存场景才关闭 | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "Pip's caching behaviour is disabled by passing the `--no-cache-dir` option ... caching at a higher level (eg: layered caches in container builds)" | type: official
- [C22] 缓存含 HTTP 响应缓存 + 本地构建 wheel 缓存；目录默认 ~/.cache/pip（Linux）、~/Library/Caches/pip（macOS），尊重 XDG_CACHE_HOME | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "This cache functions like a web browser cache ... Pip attempts to use wheels from its local wheel cache whenever possible." | type: official
- [C23] 最新稳定版 pip 26.2.1（2026-08-04）；26.2 发布于 2026-07-29 | src: https://pip.pypa.io/en/stable/news/ | quote: "26.2.1 | 2026-08-04 ... 26.2 | 2026-07-29" | type: official

## conflicts
- 无实质冲突。注意表述差异：peps.python.org 上 PEP 751 标 Final，同时说明正文成为历史文档、canonical spec 移到 packaging.python.org（内容归属迁移，非状态矛盾）。

## gaps
- `pip install pylock.toml`（不带 -r 的位置参数）是否可用：文档未记载，文档化的入口只有 `-r pylock.toml`；未实测。
- `pip lock` / pylock.toml 支持何时摘掉 experimental：官方无时间表，仅 #13952/#13953 跟踪。
- pip requirements-file-format reference 页尚未提及 pylock.toml（文档滞后于实现）。
- pip 文档未找到「推荐使用 venv」的明确句子（user_guide 未含；packaging.python.org 教程未深入查）。

## leads
- pylock spec 把 uv/PDM/Poetry 列为设计 Inspiration（跨工具对比可用）。
- pip 26.2 起 macOS 缓存目录尊重 XDG_CACHE_HOME（CI 缓存路径细节）。
- `pip lock` 可锁 VCS/本地目录/sdist 来源（CLI 页 usage），跨工具锁能力对比可查。
