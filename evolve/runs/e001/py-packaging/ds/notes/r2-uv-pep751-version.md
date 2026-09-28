# r2-uv-pep751-version
question: uv 最早在哪个版本、哪一天，开始支持 PEP 751 的 `pylock.toml`（无论是 export 还是 import/install 方向）？
checked: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md, https://github.com/astral-sh/uv/releases

## claims
- [C1] v0.12.0 (2026-07-28) 是 uv CHANGELOG 中首次明确提及 `pylock.toml` 支持的版本，包含对 PEP 751 规范的验证 | src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "Reject invalid `pylock.toml` files and artifacts...uv now validates additional requirements from the pylock.toml specification" | type: official
- [C2] v0.12.11 (2026-09-08) 添加了导出 `pylock.toml` 文件时生成缺失哈希值的功能 | src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "Generate missing artifact hashes when exporting pylock.toml files to ensure they conform to PEP 751" | type: official
- [C3] v0.6.x CHANGELOG 部分不包含任何关于 pylock.toml 或 PEP 751 的提及 | src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "[v0.6.x section has no pylock-related entries]" | type: official
- [C4] v0.11.x 版本中也未提及 `pylock.toml` 或 PEP 751 支持 | src: https://github.com/astral-sh/uv/blob/main/CHANGELOG.md | quote: "[v0.11.x section has no pylock-related entries]" | type: official

## conflicts
- WebSearch 索引提到 v0.6.15 (2025年4月) 支持 PEP 751，但官方 CHANGELOG.md 中 v0.6.x 部分完全无关 pylock/PEP 751 的记录；CHANGELOG 中最早的验证是 v0.12.0 (2026-07-28)

## gaps
- 无法从 CHANGELOG 判断 v0.12.0 之前是否存在实验性/隐藏的 pylock 支持（需查阅 GitHub Releases 详细页面或 PR 历史）

## leads
- v0.12.0 breaking changes 明确指出拒绝无效的 pylock.toml，说明此时对 PEP 751 的支持已成熟到需要严格校验；v0.12.11 的导出功能是后续增强
