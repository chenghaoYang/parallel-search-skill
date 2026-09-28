# r2-conda-lock-verify
question: R1一个工人在docs.conda.io笔记里写了「conda 26.5+官方新增原生导出锁文件能力」，措辞"Modern conda supports..."与引文逐字是否相符，`conda export --name my-env --file conda-lock.yaml`是新能力还是旧命令换名；conda CHANGELOG 26.x 是否真有lock file功能的记录；conda-lock README如何描述自己与conda核心功能的关系。
checked: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html, https://github.com/conda/conda/blob/main/CHANGELOG.md, https://github.com/conda/conda-lock/blob/main/README.md

## claims
- [C1] conda 26.5版本（2026-05-15发布）在官方CHANGELOG中明确记录了多平台锁文件支持的增强功能 | src: https://github.com/conda/conda/blob/main/CHANGELOG.md | quote: "Add default-implemented `available_platforms` and `env_for(platform)` on `EnvironmentSpecBase` (**EXPERIMENTAL**) for multi-platform environment specifiers (`conda-lock.yml`, `pixi.lock`). (#15927)" | type: official | version: 26.5.0
- [C2] conda 26.5版本的CHANGELOG记录了对`conda export`等命令帮助文本的改写以突出锁文件工作流 | src: https://github.com/conda/conda/blob/main/CHANGELOG.md | quote: "Rewrite the help text for `conda create`, `conda export`, `conda env create`, and `conda env export` (already an alias of `conda export`) to make lockfile workflows discoverable." | type: official | version: 26.5.0
- [C3] conda官方文档明确说明锁文件支持从26.5版本开始可用 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Lockfile support is available in conda 26.5 and later." | type: official
- [C4] conda官方文档记录了`conda export --name my-env --file conda-lock.yaml`命令语法及其多平台扩展形式 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "conda export --name my-env --file conda-lock.yaml --platform linux-64 --platform osx-64 --platform win-64" | type: official
- [C5] 官方文档说锁文件格式为`conda-lock.yaml`和`pixi.lock`两种原生支持格式 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: "Conda supports `conda-lock.yaml` and `pixi.lock` natively" | type: official
- [C6] R1原笔记引用的"Modern conda supports multi-platform lock files (available in conda 26.5+)"这个措辞不出现在官方文档原文 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html | quote: 官方文档该段落的实际措辞是"Lockfile support is available in conda 26.5 and later"而非"Modern conda supports..." | type: official
- [C7] conda-lock 项目README未提及conda 26.5+的原生锁文件支持，仍将自己定位为"a lightweight library that can be used to generate fully reproducible lock files" | src: https://github.com/conda/conda-lock/blob/main/README.md | quote: "Conda lock is a lightweight library that can be used to generate fully reproducible lock files for conda environments." | type: official
- [C8] 26.5.0版CHANGELOG Docs部分明确记录了"Add information on conda-lockfiles to Managing environments page. (#16086)"——正是R1所引用的那个URL对应的PR改动 | src: https://github.com/conda/conda/blob/main/CHANGELOG.md | quote: "Add information on conda-lockfiles to Managing environments page. (#16086)" | type: official | version: 26.5.0

## conflicts
- R1原笔记的引文措辞"Modern conda supports multi-platform lock files (available in conda 26.5+)"与官方文档实际措辞"Lockfile support is available in conda 26.5 and later"不一致。前者用了"Modern conda supports..."这类似新闻稿的语气加内联版本号，而后者是典型的技术文档直述风格。这可能是R1工人在WebFetch结果中看到被AI模型改写/总结过的版本而不是原文。

## gaps
- 无法确认锁文件格式（conda-lock.yaml）是否与第三方conda-lock工具的输出格式完全兼容或只是名称相同。CHANGELOG提到"Add default-implemented `available_platforms` and `env_for(platform)` on `EnvironmentSpecBase` (**EXPERIMENTAL**)"标注为EXPERIMENTAL，说明该功能在26.5可能还在试验阶段。

## leads
- conda-lock项目没有更新其README来反映conda 26.5+的原生支持，这可能意味着两者的功能定位存在差异（conda原生可能更基础，conda-lock更高级）——应查conda-lock的issue/discussion来理解关系
- 官方文档在26.5版发布后新增了锁文件部分（PR #16086），值得查一下该PR的讨论过程
