# r2-pip-pylock-verify
question: pip 是否已经官方支持"从 pylock.toml 安装"（即 `pip install -r pylock.toml` 或等价能力）？具体从哪个 pip 版本开始、命令语法是什么、是否仍是实验性。
checked: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst, https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/cli/pip_install/, https://pip.pypa.io/en/stable/reference/requirements-file-format/, https://www.infoworld.com/article/3951671/

## claims
- [C1] pip 26.1（2026-04-26 发布）添加了对从标准化 pylock.toml 文件读取需求的实验性支持，命令为 `pip install -r pylock.toml`，仍标记为 experimental | src: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst | quote: "Add experimental support to read requirements from standardized pylock.toml files (``-r pylock.toml``)" | type: official
- [C2] pip 26.2（2026-07-29 发布）进一步增强 pylock.toml 支持，添加对 upload-time 字段的支持，使 `--uploaded-prior-to` 可与 `pip install -r pylock.toml` 配合使用 | src: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst | quote: "Add support for ``pylock.toml`` ``upload-time`` field, so ``--uploaded-prior-to`` works with ``-r pylock.toml``" | type: official
- [C3] pip 26.2 版本中新增对 `--only-final` 标志的支持，可在使用 `pip install -r pylock.toml` 时生效 | src: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst | quote: "Honor ``--only-final`` when sourcing requirements with ``-r pylock.toml``" | type: official

## conflicts
- 无官方冲突。InfoWorld 文章（https://www.infoworld.com/article/3951671/）提到"No tools currently support pylock.toml generation"，但这是指锁文件**生成**功能（如 pip lock 命令），而非**安装/读取**功能（`pip install -r pylock.toml`）。NEWS.rst 中关于安装读取支持的表述清晰明确。

## gaps
- 无法从 pip.pypa.io/en/stable/cli/pip_install/ 的 WebFetch 结果中获取 -r / --requirement 参数的完整官方文档原句（该页面仅通过 WebFetch 返回了通用介绍，未返回参数详细说明部分）

## leads
- pip 25.1 版本（2025-04-26）添加了实验性 `pip lock` 命令（实现 PEP 751），这是生成锁文件的能力，与本轮核验的"从 pylock.toml 安装"是不同的维度
- 可进一步查阅 pip issue #13876（在 NEWS.rst 中提及）了解设计细节
