# py-packaging 任务 — 用户疑点参考答案（人工核对用）

对应 task.md 里 "some user aware variation" 这一行提出的疑点。

## 1. PEP 751 / pylock.toml 是不是已经是标准锁文件格式？

是。PEP 751 已于 2025-03-31 定案，状态为 **Final**，是 Python 官方标准（不是草案）。它规定锁文件必须命名为 `pylock.toml`，或匹配 `pylock.<name>.toml`（例如 `pylock.dev.toml`）。

来源：https://peps.python.org/pep-0751/

## 2. uv 是不是已经支持 PEP 751 / pylock.toml？

支持，但是"导出格式"而不是"替换 uv.lock"。uv 自 0.6.15 起可以把项目的 `uv.lock` 导出成 `pylock.toml`（`uv export --format pylock.toml`），也支持反向的 `uv pip install -r pylock.toml` / `uv pip sync pylock.toml`。项目级别仍然使用 uv 自己的 `uv.lock`，因为 pylock.toml 目前固定的结构表达不了 uv 的一些能力（例如任意入口点、跨平台解析），Astral 并未计划让它取代 uv.lock。

来源：https://docs.astral.sh/uv/concepts/projects/export/ （背景讨论：https://github.com/astral-sh/uv/issues/12584 ）

## 3. pip 是不是已经支持 PEP 751 / pylock.toml？

支持，但两个方向都还标 **experimental**。pip 25.1（2025-04-26）加入实验性的 `pip lock` 命令，按 PEP 751 生成 `pylock.toml`；pip 26.1（2026-04-26）加入实验性的 `-r pylock.toml` 读取安装支持；26.2 又继续给它补哈希校验、`upload-time` 字段等功能。方向明确，但截至今天（2026-09-24）官方文档仍未去掉 experimental 标签。

来源：https://pip.pypa.io/en/stable/news/

## 4. Poetry 2 是不是也改用标准的 [project] 表了？

是，但是可选升级，不是强制迁移。Poetry 2.0 开始支持在 `pyproject.toml` 里使用 PEP 621 定义的标准 `[project]` 表，可以用它替换 `tool.poetry` 里的许多字段；但 Poetry 特有的能力仍然只能写在 `[tool.poetry]`，两者可以混用，旧项目继续只用 `[tool.poetry]` 也完全没问题（不会被强制迁移）。

来源：https://python-poetry.org/blog/announcing-poetry-2.0.0/

## 补充：锁文件标准化不只是 uv/pip 的事

PDM 2.24.0 也加入了实验性的 pylock.toml 导出支持（默认仍是 `pdm.lock`，可用 `pdm config lock.format pylock` 切换；官方文档说未来版本可能把 pylock 设为默认）。也就是说，目前 uv、pip、PDM 三个工具都已经能"产出"符合 PEP 751 的 pylock.toml，但没有一个工具已经把它设为默认/唯一锁文件——都是并行选项。

来源：https://pdm-project.org/en/latest/usage/lockfile/
