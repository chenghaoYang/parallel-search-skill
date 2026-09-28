# r2-pip-pylock
question: pip 从哪个版本起能生成 pylock.toml、从哪个版本起能用 -r 读取？这些能力在现行文档里是否仍标实验性？安装时是否跳过依赖解析？依赖解析页是否仍指向 pip-tools？
checked: https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/topics/dependency-resolution/, https://peps.python.org/pep-0751/

## claims
- [C1] 生成锁文件的 `pip lock` 写在 changelog 标题 25.1 (2025-04-26) 的 Features 下，原文称 experimental，并实现 PEP 751。 | src: https://pip.pypa.io/en/stable/news/ | quote: "25.1 (2025-04-26) Add a new, experimental, pip lock command, implementing PEP 751." | type: official
- [C2] 用 `-r` 读取 pylock.toml 写在 changelog 标题 26.1 (2026-04-26) 的 Features 下，原文称 experimental。 | src: https://pip.pypa.io/en/stable/news/ | quote: "26.1 (2026-04-26) Add experimental support to read requirements from standardized pylock.toml files (-r pylock.toml)." | type: official
- [C3] 现行 stable changelog 页眉为 pip documentation v26.2.1，第一条版本标题是 26.2.1 (2026-08-04)。 | src: https://pip.pypa.io/en/stable/news/ | quote: "pip documentation v26.2.1 26.2.1 (2026-08-04)" | type: official
- [C4] v26.2.1 的 pip lock 页仍把该命令标为 EXPERIMENTAL。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "pip documentation v26.2.1 EXPERIMENTAL - Lock packages and their dependencies from:" | type: official
- [C5] v26.2.1 的 `-o/--output` 默认锁文件名是 pylock.toml。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "pip documentation v26.2.1 Lock file name (default=pylock.toml)." | type: official
- [C6] v26.2.1 写明生成的锁文件只保证对当前 Python 版本和平台有效。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "pip documentation v26.2.1 The generated lock file is only guaranteed to be valid for the current python version and platform." | type: official
- [C7] v26.2.1 的 pip lock `-r` 仍写 pylock.toml support is experimental。 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "pip documentation v26.2.1 pylock.toml support is experimental." | type: official
- [C8] v26.2.1 的 pip install `-r` 仍写 pylock.toml support is experimental。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "pip documentation v26.2.1 pylock.toml support is experimental." | type: official
- [C9] v26.2.1 依赖解析页仍写用 pip-tools 创建 lockfile。 | src: https://pip.pypa.io/en/stable/topics/dependency-resolution/ | quote: "pip documentation v26.2.1 During deployment, you can create a lockfile stating the exact package and version number for each dependency of that package. You can create this with pip-tools." | type: official
- [C10] 同页紧接着说该 lockfile 做法可在部署时不做 dependency resolution；该段主语是 pip-tools，不是 pylock.toml。 | src: https://pip.pypa.io/en/stable/topics/dependency-resolution/ | quote: "pip documentation v26.2.1 This means the “work” is done once during development process, and thus will avoid performing dependency resolution during deployment." | type: official
- [C11] PEP 751 的 Status 仍为 Final。 | src: https://peps.python.org/pep-0751/ | quote: "Status: Final" | type: official
- [C12] PEP 751 仍自称 historical document，并指向 PyPA 上的 pylock.toml Specification。 | src: https://peps.python.org/pep-0751/ | quote: "This PEP is a historical document. The up-to-date, canonical spec, pylock.toml Specification, is maintained on the PyPA specs page." | type: official
- [C13] PEP 751 Abstract 仍写：消费该文件的 installer 应能在安装时不经 dependency resolution 算出要安装的内容。 | src: https://peps.python.org/pep-0751/ | quote: "Installers consuming the file should be able to calculate what to install without the need for dependency resolution at install-time." | type: official
- [C14] PEP 751 Rationale 仍写格式设计为安装时不需要 resolver。 | src: https://peps.python.org/pep-0751/ | quote: "The file format is also designed to not require a resolver at install time." | type: official
- [C15] v26.2.1 的 pip install 总述仍把 Resolve dependencies 列为安装阶段，未写 pylock.toml 例外。 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "pip documentation v26.2.1 Resolve dependencies. What will be installed is determined here." | type: official

## conflicts
- 安装时是否跳过依赖解析：PEP 751 写 installer 不必在 install-time 做 dependency resolution（C13，https://peps.python.org/pep-0751/ quote: "Installers consuming the file should be able to calculate what to install without the need for dependency resolution at install-time."）；现行 pip install 仍把解析列为一般阶段（C15，https://pip.pypa.io/en/stable/cli/pip_install/ quote: "Resolve dependencies. What will be installed is determined here."），且未声明 `-r pylock.toml` 跳过解析。不裁决。

## gaps
- 已打开的 pip lock / pip install 页没有写 `pip install -r pylock.toml` 会跳过依赖解析。C10 的 avoid performing dependency resolution during deployment 属于 “Use constraint files or lockfiles” 中的 pip-tools，页面没有把该句接到 pylock.toml 或 `pip lock`。
- pip_lock 页眉只有 “pip documentation v26.2.1”，没有日期；2026-08-04 只出现在 news 标题 “26.2.1 (2026-08-04)”。

## leads
- PEP 751 把现行规范指到 PyPA pylock.toml Specification（https://packaging.python.org/en/latest/specifications/pylock-toml/）；该页不在本次来源政策内，未打开。
- stable 依赖解析页只点名 pip-tools，没有提到 `pip lock` 或 pylock.toml。
