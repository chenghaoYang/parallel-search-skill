# r2-pip-check
question: pip 侧四个缺口：A) 官方对 --extra-index-url dependency confusion 的表述/防护建议；B) pip lock 能否跨平台/解释器锁；C) packaging.python.org 是否有 pylock.toml spec 页；D) pip 最新版本与日期
checked: https://pip.pypa.io/en/stable/cli/pip_lock/, https://packaging.python.org/en/latest/specifications/pylock-toml/, https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/topics/secure-installs/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/search.html?q=dependency+confusion

## claims
- [C1] pip 官方文档明确把 --extra-index-url 装私有包称为 dependency confusion 风险（pip_install 页 Examples 下 Warning 框） | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "Using the `--extra-index-url` option to search for packages which are not in the main repository (for example, private packages) is unsafe. This is a class of security issue known as dependency confusion: an attacker can publish a package with the same name to a public index, which may then be chosen instead of your private package." | type: official
- [C2] pip 对多个 index 无优先级，全部检查后选「best」版本匹配 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "There is no priority in the locations that are searched. Rather they are all checked, and the “best” match for the requirements (in terms of version number - see the specification for details) is selected." | type: official
- [C3] pip_install 的 --extra-index-url 选项描述本身无安全提示，仅说「same rules as --index-url」 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "Extra URLs of package indexes to use in addition to --index-url. Should follow the same rules as --index-url." | type: official
- [C4] secure-installs 主题页不提 dependency confusion/index 风险，只讲 hash 校验 | src: https://pip.pypa.io/en/stable/topics/secure-installs/ | quote: "does not perform any checks to protect against remote tampering and involves running arbitrary code from distributions"（缓解为 --require-hashes / --only-binary :all:） | type: official
- [C5] pip lock 选项列表中不存在 --python-version/--platform/--implementation/--abi/--target 等跨解释器选项（doc v26.2.1 全量选项已核对） | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The generated lock file is only guaranteed to be valid for the current python version and platform." | type: official
- [C6] pip lock 有 --index-url/--extra-index-url/--find-links/--no-index、-r/-c/-e/--group、--require-hashes、--pre、--only-binary/--no-binary、-o（默认 pylock.toml）等选项 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "-o, --output <path> — Lock file name (default=pylock.toml). Use - for stdout." | type: official
- [C7] packaging.python.org 已有 pylock.toml 独立 spec 页，源自 PEP 751 | src: https://packaging.python.org/en/latest/specifications/pylock-toml/ | quote: "The pylock.toml file format is for specifying dependencies to enable reproducible installation in a Python environment. ... This specification was originally defined in PEP 751." | type: official
- [C8] pylock.toml 必填字段 lock-version = "1.0"；可选 requires-python、environments（环境 marker 数组，实现多环境锁）、extras、packages 表 | src: https://packaging.python.org/en/latest/specifications/pylock-toml/ | quote: "lock-version ... Required? : yes ... only valid value until future updates to the standard change it – as \"1.0\"." / "environments ... A list of Environment Markers for which the lock file is considered compatible with." | type: official
- [C9] pylock.toml spec 历史：2025-04 经 PEP 751 批准初版；2026-03 澄清文件名优先级 | src: https://packaging.python.org/en/latest/specifications/pylock-toml/ | quote: "April 2025: Initial version, approved via PEP 751 . March 2026: Clarify file name precedence for archives, sdists, and wheels." | type: official
- [C10] pip 最新版本 26.2.1，发布日期 2026-08-04（news 页顶部） | src: https://pip.pypa.io/en/stable/news/ | quote: "26.2.1 (2026-08-04)" | type: official

## conflicts
- 无。

## gaps
- pip_install 的 Warning 框给出风险表述，但是否附带具体防护建议（如用代理型私有 index、锁文件 hash）未在抓取文本中出现；github.com/pypa/pip issues 未单独核查（官方文档已有明确立场，够用）。
- pip lock 实验性状态/「非当前平台锁」是否有 roadmap：仅核对了选项列表原文，未查 pypa/pip issue。

## leads
- pylock.toml 的 environments 字段（marker 数组）是 pylock 多环境锁的机制——pip lock 不跨平台是 pip 实现限制，非格式限制，成稿可区分二者。
