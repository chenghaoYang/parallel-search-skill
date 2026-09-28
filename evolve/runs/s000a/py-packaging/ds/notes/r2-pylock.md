# r2-pylock
question: 复核 pip 与 uv 对 PEP 751 pylock.toml 的支持到底到哪一步，版本号必须出现在你自己摘的原句或紧挨着的标题里。
checked: https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://docs.astral.sh/uv/concepts/projects/layout/, https://github.com/astral-sh/uv/blob/main/changelogs/0.6.x.md, https://github.com/astral-sh/uv/blob/main/changelogs/0.11.x.md, https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md, https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.7.x.md (+ curl raw: changelogs/0.8.x.md, 0.9.x.md, 0.10.x.md)

## claims
- [C1] pip.lock: `pip lock` 命令加入于 pip 25.1，标题 "## 25.1 (2025-04-26)"，标注 experimental | src: https://pip.pypa.io/en/stable/news/ | quote: "Add a new, *experimental*, `pip lock` command, implementing PEP 751." | type: official
- [C2] pip.lock: pip 26.1 起可实验性以 `-r pylock.toml` 读取需求，标题 "## 26.1 (2026-04-26)" | src: https://pip.pypa.io/en/stable/news/ | quote: "Add experimental support to read requirements from standardized pylock.toml files ( `-r pylock.toml`)." | type: official
- [C3] pip.lock: pip 26.2 继续完善 pylock 读取（--only-final、冲突报错等），标题 "## 26.2 (2026-07-29)" | src: https://pip.pypa.io/en/stable/news/ | quote: "Add support for `pylock.toml` `upload-time` field, so `--uploaded-prior-to` works with `-r pylock.toml`." | type: official
- [C4] pip.lock: 文档页今天仍标 EXPERIMENTAL（站点横幅 "pip documentation v26.2.1"） | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "EXPERIMENTAL - Lock packages and their dependencies from:" | type: official
- [C5] pip.lock: `pip lock` 默认输出文件名是 pylock.toml | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "Lock file name (default=pylock.toml). Use - for stdout." | type: official
- [C6] pip.lock: pip 生成的 pylock.toml 只对当前 Python 版本和平台保证有效 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The generated lock file is only guaranteed to be valid for the current python version and platform." | type: official
- [C7] pip.lock: `pip lock -r` 接受 requirements.txt 或 pylock.toml，读取侧仍标 experimental | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The file or URL can be in pip’s requirements.txt format, or pylock.toml format. pylock.toml support is experimental." | type: official
- [C8] uv.lock: uv 0.6.15 引入 pylock.toml，措辞为 preliminary（标题 "## 0.6.15"） | src: https://github.com/astral-sh/uv/blob/main/changelogs/0.6.x.md | quote: "This release includes preliminary support for the `pylock.toml` file format, as standardized in PEP 751." | type: official
- [C9] uv.lock: 0.6.15 支持面 = `uv export -o pylock.toml`、`uv pip compile -o pylock.toml`、安装侧如下 | src: https://github.com/astral-sh/uv/blob/main/changelogs/0.6.x.md | quote: "To install from a `pylock.toml` file, run: `uv pip sync pylock.toml` or `uv pip install -r pylock.toml`" | type: official
- [C10] uv.lock: uv 文档页（页脚日期 July 21, 2026）称 pylock.toml 支持为 export target + uv pip CLI，无 preliminary 字样 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "However, uv supports `pylock.toml` as an export target and in the `uv pip` CLI." | type: official
- [C11] uv.lock: uv.lock 仍是项目接口的锁格式，不会被 pylock.toml 取代 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "Some of uv's functionality cannot be expressed in the `pylock.toml` format; as such, uv will continue to use the `uv.lock` format within the project interface." | type: official
- [C12] uv.lock: uv 0.7.0 起拒绝把任意 .toml 当 requirements.txt，PEP 751 文件须用标准命名（标题 "## 0.7.0"，Breaking changes） | src: https://raw.githubusercontent.com/astral-sh/uv/main/changelogs/0.7.x.md | quote: "Reject non-PEP 751 TOML files in install, compile, and export commands" | type: official
- [C13] uv.lock: uv 0.11.13 修复安装 pylock.toml 时的哈希校验（标题 "## 0.11.13 / Released on 2026-05-10"，Bug fixes） | src: https://github.com/astral-sh/uv/blob/main/changelogs/0.11.x.md | quote: "Respect `--require-hashes` when installing from `pylock.toml` files" | type: official
- [C14] uv.lock: uv 0.11.22 增加 pylock.toml 合规校验（标题 "## 0.11.22 / Released on 2026-06-18"） | src: https://github.com/astral-sh/uv/blob/main/changelogs/0.11.x.md | quote: "Validate that the environment satisfies the `packages.requires-python` of a `pylock.toml`" | type: official
- [C15] uv.lock: uv 0.12.0 把严格校验 pylock.toml 列为 breaking change（标题 "## 0.12.0 / Released on 2026-07-28"） | src: https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md | quote: "uv now validates additional requirements from the `pylock.toml` specification" | type: official
- [C16] uv.lock: 0.12.0 同条注明不可关闭这些校验 | src: https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md | quote: "You cannot opt out of these checks. Regenerate malformed lockfiles, rename invalid filenames, and either correct or remove an incorrect optional `size` value." | type: official
- [C17] uv.lock: 新的 pylock 校验在 0.12.17 仍归入 "### Preview features"（标题 "## 0.12.17 / Released on 2026-09-18"） | src: https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md | quote: "Reject `pylock.toml` files whose wheel filenames do not match their declared package names or versions" | type: official
- [C18] uv 最新 changelog 版本为 0.12.18（标题 "## 0.12.18"） | src: https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md | quote: "Released on 2026-09-22." | type: official

## conflicts
- uv 文档页（2026-07-21）把 pylock.toml 支持陈述为既定功能、无 preview 标记："uv supports `pylock.toml` as an export target and in the `uv pip` CLI."（https://docs.astral.sh/uv/concepts/projects/layout/）；但 changelog 仍把部分新 pylock 校验归入 "### Preview features"：0.12.11 "Generate missing artifact hashes when exporting `pylock.toml` files to ensure they conform to PEP 751"、0.12.17 wheel 文件名拒绝（https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md）。官方没有一条声明 pylock 支持已脱离 preview/preliminary。

## gaps
- uv 无任何 changelog/文档明确写 "pylock.toml support is stable / no longer preliminary"；"preliminary" 仅出现在 0.6.15 引言，之后既不重复也不撤销。
- pip 侧未见移除 `pip lock` EXPERIMENTAL 标记的时间表；截至 docs v26.2.1 仍为 experimental。
- uv 0.8.x–0.10.x changelogs 中约 6 条 pylock 条目（如 0.9.19 "Support remote `pylock.toml` files"）仅以 curl+grep 核对，未逐条经 web_fetch 正文摘录。

## leads
- pip 26.2 有 pylock 安全修复："Reject a package `path` in a `pylock.toml` fetched from a URL when it resolves outside the lock file’s own location"（news 页，可佐证 pip 侧成熟度）。
- uv 文档另有 "Exporting lockfiles" 概念页（concepts/projects 下），可能列全部导出格式矩阵。
