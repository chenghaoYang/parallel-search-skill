# r2-pip-pylock-install
question: pip 除了用 `pip lock` 命令生成 pylock.toml 之外，能不能反过来用 `pip install` 直接读取/消费一份 pylock.toml 来安装依赖？如果可以，是从哪个 pip 版本、哪天开始，用什么命令/参数？
checked: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst, https://pip.pypa.io/en/stable/cli/pip_install/

## claims
- [C1] pip 26.1 (2026-04-26) 添加实验性功能，支持通过 `-r pylock.toml` 从标准化的 pylock.toml 文件读取依赖 | src: https://raw.githubusercontent.com/pypa/pip/main/NEWS.rst | quote: "Add experimental support to read requirements from standardized pylock.toml files (``-r pylock.toml``)" | type: official | version: 26.1 | release_date: 2026-04-26
- [C2] pip install 的 `-r` 参数支持 pylock.toml 文件格式（除了传统的 requirements.txt），pylock.toml 支持处于实验阶段 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "The file or URL can be in pip's requirements.txt format, or pylock.toml format. pylock.toml support is experimental" | type: official
- [C3] 使用命令 `pip install -r pylock.toml` 或等效的 `python -m pip install -r pylock.toml` 可以从锁文件安装依赖 | src: https://pip.pypa.io/en/stable/cli/pip_install/ | quote: "Install from the given requirements file" | type: official

## conflicts
- 无

## gaps
- pip 26.1 及更新版本中 `-r pylock.toml` 与其他参数（如 `--only-binary`、`--prefer-binary` 等）的交互行为未在官方文档明确说明

## leads
- pip 26.2 后续版本添加了 pylock.toml 的更多支持，包括 `--only-final`、`--uploaded-prior-to` 等参数的适配
