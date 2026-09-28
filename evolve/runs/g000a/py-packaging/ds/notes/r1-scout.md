# r1-scout
question: 在 uv/pip/Poetry/PDM/pixi 这张对照表之外，用户开新项目时还会撞上哪些官方仍在维护的工具或坑？conda、hatch、pip-tools、rye 今天还是不是独立选项？
checked: https://docs.conda.io/projects/conda/en/latest/index.html, https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html, https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html, https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html, https://pixi.prefix.dev/latest/conda_ecosystem/, https://hatch.pypa.io/latest/, https://hatch.pypa.io/latest/config/build/, https://hatch.pypa.io/latest/history/hatch/, https://raw.githubusercontent.com/jazzband/pip-tools/main/README.md, https://pypi.org/pypi/pip-tools/json, https://github.com/astral-sh/rye, https://rye.astral.sh/guide/uv/, https://docs.astral.sh/uv/concepts/projects/layout/, https://docs.astral.sh/uv/concepts/projects/sync/, https://docs.astral.sh/uv/concepts/authentication/http/

## claims
- [C1] conda 仍是现行的包、依赖与环境管理器。 | src: https://docs.conda.io/projects/conda/en/latest/index.html | quote: "Conda provides package, dependency, and environment management for any language." | type: official
- [C2] conda 26.5 起有锁文件支持；未把 pixi 写成替代品。 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "Lockfile support is available in conda 26.5 and later." | type: official
- [C3] conda 原生支持 conda-lock.yaml 与 pixi.lock。 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "Conda supports conda-lock.yaml and pixi.lock natively" | type: official
- [C4] Pixi 自称不是 drop-in；同表称 conda 为 original package manager。 | src: https://pixi.prefix.dev/latest/conda_ecosystem/ | quote: "Not a drop-in replacement — it rethinks the workflow." | type: official
- [C5] Hatch 官方定义为现行项目管理器。 | src: https://hatch.pypa.io/latest/ | quote: "Hatch is a modern, extensible Python project manager." | type: official
- [C6] Hatchling 是标准构建后端，并且是 Hatch 的依赖。页脚 May 31, 2026。 | src: https://hatch.pypa.io/latest/config/build/ | quote: "Hatchling is a standards-compliant build backend and is a dependency of Hatch itself." | type: official
- [C7] Hatch 最新已发布 changelog 条目为 1.18.1（2026-09-16）。 | src: https://hatch.pypa.io/latest/history/hatch/ | quote: "1.18.1 - 2026-09-16" | type: official
- [C8] pip-tools 7.6.1（sdist 2026-08-12T00:04:08，未 yanked）；仓库 jazzband/pip-tools，不是 pypa。 | src: https://pypi.org/pypi/pip-tools/json | quote: "Development Status :: 5 - Production/Stable" | type: official
- [C9] README 仍支持 requirements.in→requirements.txt，输入也可是 pyproject.toml/setup.cfg/setup.py。 | src: https://raw.githubusercontent.com/jazzband/pip-tools/main/README.md | quote: "compile a requirements.txt file from your dependencies, specified in either pyproject.toml, setup.cfg, setup.py, or requirements.in." | type: official
- [C10] 新项目推荐的输入是 pyproject.toml，不是 requirements.in。 | src: https://raw.githubusercontent.com/jazzband/pip-tools/main/README.md | quote: "The pyproject.toml file is the latest standard for configuring packages and applications, and is recommended for new projects." | type: official
- [C11] Rye 不再开发，无后续更新（含安全更新）。 | src: https://github.com/astral-sh/rye | quote: "While Rye will continue to be available, no further updates are planned, including security updates." | type: official
- [C12] 官方要求改用同一维护者的继任项目 uv。 | src: https://github.com/astral-sh/rye | quote: "Rye is no longer developed. We encourage all users to use uv, the successor project from the same maintainers, which is actively maintained and much more widely used." | type: official
- [C13] rye 仓库 2026-02-05 归档只读。 | src: https://github.com/astral-sh/rye | quote: "This repository was archived by the owner on Feb 5, 2026. It is now read-only." | type: official
- [C14] 用过 pip 后 conda 不知道这些改动。 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html | quote: "Once pip has been used, conda will be unaware of the changes." | type: official
- [C15] 不要在全局同时配 defaults 与 conda-forge。 | src: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html | quote: "Mixing these channels in your global configuration can result in mixed-channel environments with incompatible packages" | type: official
- [C16] 必须按每个目标 Python 环境分别跑 pip-compile。 | src: https://raw.githubusercontent.com/jazzband/pip-tools/main/README.md | quote: "users must execute pip-compile on each Python environment separately" | type: official
- [C17] uv.lock 默认跨平台，应提交版本库。页脚 July 21, 2026。 | src: https://docs.astral.sh/uv/concepts/projects/layout/ | quote: "uv.lock is a universal or cross-platform lockfile" | type: official
- [C18] uv sync 默认 exact，会删除锁外的包。页脚 August 5, 2026。 | src: https://docs.astral.sh/uv/concepts/projects/sync/ | quote: "exact syncing by default, which means it will remove any packages that are not present in the lockfile." | type: official
- [C19] uv add 不把 index 凭证写入 pyproject.toml 或 uv.lock。 | src: https://docs.astral.sh/uv/concepts/authentication/http/ | quote: "When using uv add, uv will not persist index credentials to the pyproject.toml or uv.lock." | type: official
- [C20] direct URL 的账密会被 uv 写入。 | src: https://docs.astral.sh/uv/concepts/authentication/http/ | quote: "However, uv will persist credentials for direct URLs" | type: official

## conflicts
- Rye 停更日：https://rye.astral.sh/guide/uv/ 页顶 "Rye is no longer developed as of February 2025."；https://github.com/astral-sh/rye "archived by the owner on Feb 5, 2026"。README 不写 2025-02。未裁决。
- 迁移指南仍写 "As of July 2025, uv does not yet have a task runner."（uv 0.8.0）。现行 uv 未核对。

## gaps
- docs.conda.io 无「停用 conda、改用 pixi」。mamba 官方站未打开。
- 无 pypa/pip-tools。packaging.python.org 是否推荐 .in 路径未打开。
- authenticated-channels 正文未读：https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/authenticated-channels.html
- Hatch「只用 build system」与 uv#5903 现状未打开。

## leads
- conda: 仍是与 pixi 并列的独立现行工具。conda>=26.5 原生读 pixi.lock；Pixi 自称 not a drop-in。 | https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
- hatch: 项目管理器，不只是构建后端。hatchling 是 build-backend。1.17.0（2026-05-31）有 env lock→pylock.toml；1.18.1（2026-09-16）仍发版。 | https://hatch.pypa.io/latest/history/hatch/
- pip-tools: 仍维护，仓库是 jazzband 不是 pypa；7.6.1（2026-08-12）。.in→txt 仍支持，新项目推荐输入是 pyproject.toml。 | https://raw.githubusercontent.com/jazzband/pip-tools/main/README.md
- rye: 不是现行选项。successor=uv，无安全更新；2026-02-05 archived。[tool.rye] 改名 [tool.uv]；requirements.lock 换 uv.lock。指南停在 uv 0.8/2025-07。 | https://rye.astral.sh/guide/uv/
- 坑: conda 先 pip 再 conda 难再改 | pip 之后 conda 不知道改动，应重建；勿在 root pip，勿 --user | https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
- 坑: 纯 Python wheel 仍被 pip 进 conda | 2026 改口：优先 conda install + conda-pypi，pip 只是 fallback | https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html
- 坑: defaults 与 conda-forge 同时进 .condarc | 混频道会不兼容；channel::pkg 可造成 ABI 不兼容 | https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html
- 坑: 一份 requirements.txt 换 OS/Python 就错 | 须按环境分别 pip-compile，并提交如 macos-py3.10-requirements.txt | https://raw.githubusercontent.com/jazzband/pip-tools/main/README.md
- 坑: CI 不提交锁则机器间漂移 | uv 要求提交 uv.lock；pip-tools 要求同时提交 .in 与 .txt | https://docs.astral.sh/uv/concepts/projects/layout/
- 坑: uv sync 删手工包，uv run 留下 | sync 默认 exact（--inexact 保留）；uv run 默认 inexact（--exact 删除） | https://docs.astral.sh/uv/concepts/projects/sync/
- 坑: 私有源账密进仓库 | index 凭证不进 pyproject/uv.lock；direct URL user:pass 会写入。conda 私有频道页未读 | https://docs.astral.sh/uv/concepts/authentication/http/
- 维度: 锁是否默认跨平台 | uv.lock 默认 universal；pip-compile 默认单环境；conda explicit 通常单平台，conda>=26.5 的 conda-lock.yaml/pixi.lock 须重复 --platform。 | https://docs.astral.sh/uv/concepts/projects/layout/
- 维度: sync 会不会删多余包 | uv sync 默认删、uv run 默认不删；pip-sync 会 uninstall 但不卸 pip/setuptools/pip-tools；conda 仅 env update --prune 才删。 | https://docs.astral.sh/uv/concepts/projects/sync/
