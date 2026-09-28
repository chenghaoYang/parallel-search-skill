# r2-pixi-workspace
question: pixi 的「workspace」概念到底是不是传统意义上的 monorepo（一个仓库里放多个可以互相引用依赖的独立子包/子项目），还是仅仅是"项目清单根节点"的改名？pixi 官方是否提及 PEP 751 或 pylock.toml？构建可分发 Python wheel/sdist 时 pixi 官方推荐什么构建后端？
checked: https://pixi.prefix.dev/dev/build/workspace/, https://pixi.prefix.dev/latest/python/pyproject_toml/, https://pixi.prefix.dev/dev/first_workspace/, https://github.com/prefix-dev/pixi (GitHub search for pylock/PEP 751)

## claims
- [C1] pixi workspace 是真正的 monorepo，支持一个仓库内多个独立子包在不同目录，每个有自己的 pixi.toml | src: https://pixi.prefix.dev/dev/build/workspace/ | quote: "Pixi enables developers to manage multiple packages within a single workspace" with structure: root pixi.toml, subdirectories (packages/cpp_math/, src/python_rich/) each with own pixi.toml | type: official
- [C2] pixi workspace 中子包可互相引用为源依赖（source dependencies），通过路径或 `{ workspace = true }` 语法 | src: https://pixi.prefix.dev/dev/build/workspace/ | quote: "Packages declare dependencies on workspace members using path-based references or the { workspace = true } syntax for shared dependency pools" | type: official
- [C3] 只有根 manifest 需要 [workspace] 表，子包可只包含 [package] 表 | src: https://pixi.prefix.dev/dev/build/workspace/ | quote: "Only the root manifest needs a [workspace] section. Member packages can omit this, containing only their [package] section." | type: official
- [C4] pixi publish 能发现并自动依赖顺序构建多个子包，确保源依赖也被发布 | src: https://pixi.prefix.dev/dev/build/workspace/ | quote: "pixi publish command discovers enabled packages, builds them in dependency order, and ensures all source dependencies are also published" | type: official
- [C5] pixi 官方 pyproject.toml 文档未提及 PEP 751 或 pylock.toml | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: 文档列举 [build-system] 配置但未提 PEP 751 | type: official
- [C6] pixi 对 [build-system] 的默认行为：若无 [build-system]，默认 setuptools；pixi init --format pyproject 默认 hatchling | src: https://pixi.prefix.dev/latest/python/pyproject_toml/ | quote: "If omitted, Pixi defaults to setuptools. Using hatchling is recommended: build-backend = 'hatchling.build' with requires = ['hatchling']" | type: official
- [C7] pixi 也支持 pixi-build-python 作为构建后端选项 | src: https://pixi.sh/dev/build/workspace/ (搜索结果提及 pixi-build-backends) | quote: "pixi-build-python - Pixi Build Backends" | type: secondary

## conflicts
无冲突发现。

## gaps
- GitHub 搜索未直接返回 pixi 团队对 PEP 751 的官方立场（issue/discussion/roadmap），只能确认官方文档中无提及，无法判断是有意不支持还是尚未规划

## leads
- pixi 文档对 workspace 和 monorepo 并未特别强调"monorepo"一词，但实现上完全符合定义，值得考虑在 deep-search 最终报告中特别标注术语对齐
- pixi-build-backends 项目可能有专属构建工具，但未在主文档中重点宣传
