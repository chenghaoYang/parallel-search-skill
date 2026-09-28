# r2-pixi
question: pixi 的「workspace」是不是多包 monorepo，channel / PyPI index 的键名是什么，构建文档和 Poetry 迁移页是否互相矛盾？
checked: https://pixi.prefix.dev/latest/reference/pixi_manifest/ ; https://pixi.prefix.dev/latest/build/workspace/ ; https://pixi.prefix.dev/latest/build/backends/ ; https://pixi.prefix.dev/latest/switching_from/poetry/

## claims
- [C1] [workspace] 必填键是 channels + platforms；name 在最小示例里出现但官方标注 optional | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "The minimally required information in the `workspace` table is: [workspace] channels = [\"conda-forge\"] name = \"project-name\" platforms = [\"linux-64\"]" | type: official
- [C2] name 可选，缺省用目录名 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "### `name` (optional) The name of the workspace. If the name is not specified, the name of the directory that contains the workspace is used." | type: official
- [C3] channels 键 = conda channel 列表 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "This is a list that defines the channels used to fetch the packages from." | type: official
- [C4] platforms 键 = 求解平台列表 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "Defines the list of platforms that the workspace supports. Pixi solves the dependencies for all these platforms and puts them in the lock file (`pixi.lock`)." | type: official
- [C5] manifest 全文无 `members` 键、无 "monorepo" 一词；"member" 仅出现一次："re-anchored per consuming member"（指 path 依赖的消费方）。workspace 表键集合：channels, platforms, name, version, authors, description, license, license-file, readme, homepage, repository, documentation, conda-pypi-map, channel-priority, solve-strategy, requires-pixi, exclude-newer, build-variants, build-variants-files, dependencies, preview | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | type: official
- [C6] 多包 monorepo 靠 path source dependency，不是 members 列表；顶层 manifest 持有唯一 [workspace] 表 | src: https://pixi.prefix.dev/latest/build/workspace/ | quote: "we will show you how to integrate multiple Pixi packages into a single workspace" | type: official
- [C7] 子包 manifest 去掉 [workspace] 段 | src: https://pixi.prefix.dev/latest/build/workspace/ | quote: "We only want to use the `workspace` table of the top-level manifest. Therefore, we can remove the workspace section in the manifest of `cpp_math`." | type: official
- [C8] 多包/源码依赖是 pixi-build preview 功能 | src: https://pixi.prefix.dev/latest/build/workspace/ | quote: "`pixi-build` is a preview flag, and will change until it is stabilized." | type: official
- [C9] [workspace.dependencies] 池 + `{ workspace = true }` 继承；页面标题用 "members" 但是散文非键名 | src: https://pixi.prefix.dev/latest/build/workspace/ | quote: "A `[workspace.dependencies]` pool lets you declare those specs once and have each member opt in per entry with `{ workspace = true }`." | type: official
- [C10] pypi-options 键名：index-url、extra-index-urls、find-links、no-build-isolation、no-build、no-binary、index-strategy、prerelease-mode、skip-wheel-filename-check | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "`index-url`: replaces the main index url. `extra-index-urls`: adds an extra index url. `find-links`: similar to `--find-links` option in `pip`." | type: official
- [C11] index-url 默认 pypi.org/simple，每环境只能一个 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "If this is not set the default index used is `https://pypi.org/simple`. **Only one** `index-url` can be defined per environment." | type: official
- [C12] pypi-options 三个作用域 | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "`[workspace.pypi-options]`: the workspace base. ... `[pypi-options]` at the root of the manifest: shorthand for the default feature's options. ... `[feature.<name>.pypi-options]`: per-feature options" | type: official
- [C13] 单个 PyPI 包可用 `index` 键钉 index（pypi-dependencies 内） | src: https://pixi.prefix.dev/latest/reference/pixi_manifest/ | quote: "The index parameter allows you to specify the URL of a custom package index for the installation of a specific package." 例：torch = { version = "*", index = "https://download.pytorch.org/whl/cu118" } | type: official
- [C14] 构建后端键位置 [package.build.backend]，键为 channels/name/version | src: https://pixi.prefix.dev/latest/build/backends/ | quote: "[package.build.backend] channels = [\"https://prefix.dev/conda-forge\"] name = \"pixi-build-python\" version = \"0.*\"" | type: official
- [C15] 官方后端名单：pixi-build-cmake / pixi-build-python / pixi-build-rattler-build / pixi-build-ros / pixi-build-r / pixi-build-rust / pixi-build-mojo | src: https://pixi.prefix.dev/latest/build/backends/ | quote: "All backends are available through the [conda-forge](https://prefix.dev/channels/conda-forge) conda channel" | type: official
- [C16] pixi publish 存在且会遍历 workspace 树发布 | src: https://pixi.prefix.dev/latest/build/workspace/ | quote: "`pixi publish` walks the workspace directory tree, finds every package that opts in, and builds and uploads them in dependency order." | type: official
- [C17] 发布需 [package] 里 publish = true 显式 opt-in | src: https://pixi.prefix.dev/latest/build/workspace/ | quote: "To publish a workspace's packages, opt each of them in with `publish = true` in its `[package]` section" | type: official

## conflicts
- Poetry 迁移页说构建/发布「尚未实现」，build 文档却在讲 pixi publish 与 backends：
  - https://pixi.prefix.dev/latest/switching_from/poetry/ 表格两行原句: "Building a package | `poetry build` | We've yet to implement package building and publishing" 与 "Publishing a package | `poetry publish` | We've yet to implement package building and publishing"（该页未出现 preview / pixi-build 字样）
  - https://pixi.prefix.dev/latest/build/backends/ 原句: "When you build a package (for example via `pixi publish`), the build backends generate a complete rattler-build recipe that is stored in your project's build directory."（该句附近无 preview 字样；preview 门槛写在 build/workspace 页: "`pixi-build` is a preview flag"）
  - 即：迁移页似已过时；构建/发布能力存在但挂在 `preview = ["pixi-build"]` 之下。不裁决，仅并列。

## gaps
- 无 `members` 数组键的证据是「页面 absence」：manifest reference 的 workspace 表无此键、全页 0 次 "monorepo"、1 次 "member"（散文用法）。uv 式 members globs 不存在。
- backends 页本身未在该句旁标注 preview 要求；preview 关联来自 build/workspace 页与 manifest 的 build-variants/package.* 段落（"require the `pixi-build` preview flag"）。

## leads
- pixi publish CLI 完整行为: https://pixi.prefix.dev/latest/reference/cli/pixi/publish/ （未打开）
- workspace dependencies 细节: https://pixi.prefix.dev/latest/build/workspace_dependencies/ （未打开）
- 各后端页: https://pixi.prefix.dev/latest/build/backends/pixi-build-python/ 等（未打开）
