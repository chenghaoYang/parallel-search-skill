# r2-gotchas
question: 为三个主题找具体的、有一手来源支撑的踩坑案例：(1)私有源解析顺序陷阱；(2)Poetry/PDM迁移到uv时lock文件不能直接互转；(3)CI缓存跨版本/OS导致wheel ABI不兼容
checked: https://docs.astral.sh/uv/concepts/indexes/, https://docs.astral.sh/uv/pip/compatibility/, https://github.com/astral-sh/uv/issues/1804, https://github.com/astral-sh/uv/issues/6425, https://docs.astral.sh/uv/concepts/cache/, https://pip.pypa.io/en/stable/topics/caching/, https://github.com/actions/setup-python/issues/432, https://github.com/astral-sh/uv/issues/9429, https://pixi.prefix.dev/v0.47.0/integration/ci/github_actions/

## claims
- [C1] uv默认`first-index`策略：停止在第一个包含该包的index，不跨index合并版本候选 | src: https://docs.astral.sh/uv/pip/compatibility/ | quote: "Search for each package across all indexes, limiting the candidate versions to those present in the first index that contains the package" | type: official
- [C2] pip默认`unsafe-best-match`策略：从所有index合并候选版本并选最优版本，易遭依赖混淆攻击 | src: https://docs.astral.sh/uv/pip/compatibility/ | quote: "uv prioritizes preventing dependency confusion attacks. By stopping at the first index containing a package, uv ensures internal packages are always installed from internal registries" | type: official
- [C3] uv提供`--index-strategy`选项支持配置：`first-index`(默认)、`unsafe-first-match`、`unsafe-best-match` | src: https://docs.astral.sh/uv/pip/compatibility/ | quote: "As of v0.1.39, uv offers three `--index-strategy` modes" | type: official
- [C4] uv在忘记给内部index加用户名密码时会悄悄fallback到PyPI，触发依赖混淆漏洞 | src: https://github.com/astral-sh/uv/issues/9429 | quote: "uv silently and happily ignored my internal package index URL, gave no warning, and installs example-component from pypi" | type: official
- [C5] uv不支持直接使用poetry.lock或Pipfile.lock进行安装，该feature request已被标记wontfix | src: https://github.com/astral-sh/uv/issues/1804 | quote: "该issue已被标记为wontfix（不会解决）并已关闭。这意味着uv开发团队决定不支持直接使用Poetry或Pipenv的锁文件进行安装。" | type: official
- [C6] Poetry到uv迁移时生成uv.lock需要特殊处理，不能自动从poetry.lock转换 | src: https://github.com/astral-sh/uv/issues/6425 | quote: "用户尝试从poetry.lock导出requirements.txt后运行uv lock，但没有按预期工作" | type: official
- [C7] GitHub Actions pip缓存在跨Ubuntu版本时失效：Ubuntu 20.04编译的wheel在Ubuntu 22.04不兼容 | src: https://github.com/actions/setup-python/issues/432 | quote: "A wheel compiled on Ubuntu 20.04 may be incompatible with Ubuntu 22.04" because compiled packages depend on specific shared library versions | type: official
- [C8] pip缓存设计假设包编译结果是确定性的，但可能缓存不兼容的wheel（如带optional C扩展的包） | src: https://pip.pypa.io/en/stable/topics/caching/ | quote: "pip assumes that the result of building a package from a package index is deterministic...pip may cache a pure Python wheel built in one environment and reuse it in another environment capable of building the C extensions" | type: official
- [C9] GitHub Actions setup-python的缓存key需要包含OS版本，仅有OS类型+Python版本不够 | src: https://github.com/actions/setup-python/issues/432 | quote: "The cache key format includes OS type and Python version but ignores OS release...ensure separate caches for Ubuntu 20.04 and Ubuntu 22.04" | type: official
- [C10] Pixi GitHub Actions缓存key结构为`<cache-key><conda-arch>-<hash>`，包含架构但未明确要求Python版本 | src: https://pixi.prefix.dev/v0.47.0/integration/ci/github_actions/ | quote: "The cache key structure follows: `<cache-key><conda-arch>-<hash>`" | type: official

## conflicts
- uv文档强调first-index防止依赖混淆，但issue #9429指出在忘记凭证时仍会fallback到PyPI造成混淆 | src1: https://docs.astral.sh/uv/pip/compatibility/ | src2: https://github.com/astral-sh/uv/issues/9429 | quote1: "By stopping at the first index containing a package, uv ensures internal packages are always installed from internal registries" | quote2: "uv silently and happily ignored my internal package index URL...installs example-component from pypi"

## gaps
- uv文档未明确说明当内部index返回401/403时的fallback行为是否必然（issue #12362提出改进建议，但未确认官方决定）
- pixi缓存文档未明确强调cache key需要包含Python版本以避免ABI不兼容
- pip官方缓存文档未提供跨操作系统版本缓存失效的具体预警或最佳实践建议

## leads
- uv issue #12362提出防止401/403时fallback到PyPI以完全阻止依赖混淆，可跟踪官方决策
- 检查pip-tools/poetry等工具对lock文件格式的互操作性说明（目前只确认uv不支持poetry.lock）
