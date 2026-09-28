# r2-conda-verify
question: (a) conda 官方命令是否真的能生成"多平台"锁文件？(b) pixi 和 conda-lock 的官方 changelog/issue tracker 里对 PEP 751 / pylock.toml 的官方表态？(c) Anaconda 现行商业条款对免费版商业使用的限制原文？
checked: https://docs.conda.io/projects/conda/en/latest/commands/export.html,https://raw.githubusercontent.com/conda/conda/main/docs/source/user-guide/tasks/manage-environments.rst,https://github.com/prefix-dev/pixi/issues/3474,https://github.com/prefix-dev/pixi/issues/3889,https://github.com/conda/conda-lock/releases,https://github.com/conda/conda-lock/issues,https://www.anaconda.com/legal/terms-of-service,https://www.anaconda.com/pricing

## claims
- [C1] conda export 默认单平台，多平台需显式指定 --platform 参数 | src: https://docs.conda.io/projects/conda/en/latest/commands/export.html | quote: "For formats that support multi-platform output, repeat the flag to produce a single file covering every platform" | type: official
- [C2] conda export 多平台语法示例 | src: https://raw.githubusercontent.com/conda/conda/main/docs/source/user-guide/tasks/manage-environments.rst | quote: "conda export --name my-env --file conda-lock.yaml --platform linux-64 --platform osx-64 --platform win-64" | type: official
- [C3] R1 主张 [C3-a] 误读说明：R1 声称"conda export --name my-env --file conda-lock.yaml"能生成多平台锁文件，但官方文档证明缺少 --platform 参数时只能单平台导出；文件名不决定格式 | src: https://docs.conda.io/projects/conda/en/latest/commands/export.html | quote: "Explicit spec files are usually limited to a single platform, but lockfiles can support multiple platforms" | type: official
- [C4] pixi 官方 PEP 751 立场：开放 issue #3474 "PEP751 support" 标记为 needs-design，表明在探索/规划中 | src: https://github.com/prefix-dev/pixi/issues/3474 | quote: "issues/3474" | type: official
- [C5] pixi 官方 pylock.toml 立场：开放 issue #3889 "Support export to `pylock.toml`" 已分配给 @wolfv | src: https://github.com/prefix-dev/pixi/issues/3889 | quote: "issues/3889 assigned to @wolfv" | type: official
- [C6] conda-lock PEP 751 沉默确认：搜索 github.com/conda/conda-lock issues、releases、CHANGELOG 未见 "PEP 751"、"PEP-751"、"pylock" 任何提及 | src: https://github.com/conda/conda-lock/releases | quote: "(无搜索结果)" | type: official
- [C7] Anaconda 现行商业条款：>200 人员组织必须购买付费版 | src: https://www.anaconda.com/legal/terms-of-service | quote: "Users within organizations with 200+ employees/contractors (including Affiliates) require a paid Business license" | type: official
- [C8] Anaconda 免费版商业活动限制：禁止"embed the Platform or any Offering in any product or service provided to third parties without obtaining an additional Embedding license" | src: https://www.anaconda.com/legal/terms-of-service | quote: "build a competitive product or service" | type: official

## conflicts
- [CONFLICT-A] R1 主张 C3-a "conda export --name my-env --file conda-lock.yaml" 生成多平台锁文件不准确。官方文档明确说明：(1) 仅凭文件名 conda-lock.yaml 不能自动产生多平台格式，(2) 必须显式加 --platform 参数，(3) 不加参数时为当前平台单平台导出。R1 主张的引用来源 https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html 中的原句应该是"conda export --name my-env --file conda-lock.yaml --platform linux-64 --platform osx-64 --platform win-64"（包含多个 --platform 标志），而非 R1 引用的简略形式。

## gaps
- pixi issue #3474 完整讨论内容（仅通过 API 搜索确认标题存在）
- conda-lock 是否有 PEP-735 相关讨论（发现 issue #857 关于 PEP-735 但非 PEP-751）

## leads
- pixi 对 PEP 751 的态度从"开放讨论中"升级为具体 issue（#3889 分配给主维护者），表明有真实规划而非完全沉默
- Anaconda 商业条款与 conda-lock/pixi 的中立性形成对比：conda 生态（conda-lock、pixi）都在探索 PEP 751，但 Anaconda 官方政策专注商业订阅模式
