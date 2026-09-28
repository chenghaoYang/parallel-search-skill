# r3-conda-plugin
question: conda 26.5 的 lockfile 支持是安装 conda 之后就有，还是必须再装 conda-lockfiles 插件？
checked: https://github.com/conda/conda/releases/tag/26.5.0 ; https://github.com/conda/conda-lockfiles ; https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html ; https://github.com/conda/conda/blob/26.5.0/recipe/meta.yaml ; https://github.com/conda/conda/blob/26.5.x/pyproject.toml

## claims
- [C1] conda 26.5.0 的 conda 包 recipe 把 conda-lockfiles 列为硬 run 依赖，归类在"捆绑插件"注释下——装/升级 conda conda-package 会自动带入插件。 | src: https://github.com/conda/conda/blob/26.5.0/recipe/meta.yaml | quote: "# Plugins to bundle with conda - conda-libmamba-solver >=26.4.1 - conda-lockfiles >=0.2.0 - conda-self >=0.2.0" | type: official
- [C2] 同一版本 pyproject.toml 的 pip dependencies 里没有 conda-lockfiles——pip 装的 conda 不自带该插件。 | src: https://github.com/conda/conda/blob/26.5.x/pyproject.toml | quote: "# Disabled due to conda-libmamba-solver not being available on PyPI" | type: official
- [C3] 插件 README 仍写必须手动装到 base。 | src: https://github.com/conda/conda-lockfiles | quote: "conda-lockfiles is a conda plugin and must be installed in the base environment: conda install --name base conda-forge::conda-lockfiles" | type: official
- [C4] 用户指南只说升级到 conda>=26.5 即可，未提装插件。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Lockfile support is available in conda 26.5 and later. Use the following command to update: conda install --name base \"conda>=26.5\"" | type: official
- [C5] 用户指南用"natively"描述支持。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Conda supports conda-lock.yaml and pixi.lock natively" | type: official
- [C6] 26.5.0 release notes 无"bundled/default install"类散文声明；conda-lockfiles 仅出现在 docs 条目。 | src: https://github.com/conda/conda/releases/tag/26.5.0 | quote: "Add information on conda-lockfiles to Managing environments page. (#16086)" | type: official
- [C7] release notes 暗示格式支持由已装插件驱动。 | src: https://github.com/conda/conda/releases/tag/26.5.0 | quote: "driven dynamically by the installed environment specifier and exporter plugins" | type: official

## conflicts
- 同一插件两种官方说法并存：recipe 把 conda-lockfiles>=0.2.0 当 conda 26.5.0 的捆绑 run 依赖（docs 称 "natively"），但插件 README 仍写 "must be installed in the base environment"。两者分别对 conda 包安装与 pip/非捆绑安装成立，官方未在散文中挑明。

## gaps
- release notes 与用户指南均无一句话明说"插件随 conda 26.5 默认安装"；bundled 结论只来自 recipe 注释，非散文。
- Miniforge/Anaconda 等发行版是否随包预装未核实。
- conda-lockfiles 自身版本发布节奏（>=0.2.0 对应哪个插件版本）未查。

## leads
- https://conda-incubator.github.io/conda-lockfiles/getting-started/ （README 指向的插件文档，超出本次允许域名）
- PR conda/conda#16086（docs 改动来源）与 conda-lockfiles recipe/ 目录
