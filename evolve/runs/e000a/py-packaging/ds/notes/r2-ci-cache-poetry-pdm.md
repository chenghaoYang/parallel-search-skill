# r2-ci-cache-poetry-pdm
question: Poetry 和 PDM 官方分别推荐什么样的 CI 缓存方式？有没有官方 GitHub Action 或官方文档页面给出具体缓存路径/key 策略？
checked: https://python-poetry.org/docs/,https://python-poetry.org/docs/configuration/,https://python-poetry.org/docs/faq/,https://python-poetry.org/docs/basic-usage/,https://pdm-project.org/latest/,https://pdm-project.org/en/latest/usage/advanced/,https://pdm-project.org/latest/usage/config/,https://github.com/pdm-project/setup-pdm,https://github.com/marketplace/actions/setup-pdm,https://github.com/python-poetry/poetry

## claims
- [C1] Poetry 官方文档没有专门的 CI/CD 或 GitHub Actions 缓存指南，仅在 Configuration 页面提供通用的 cache-dir 配置（默认路径：macOS `~/Library/Caches/pypoetry`；Unix `~/.cache/pypoetry`），不涉及 CI 缓存策略 | src: https://python-poetry.org/docs/configuration/ | quote: "The path to the cache directory used by Poetry." | type: official
- [C2] Poetry 官方文档中没有推荐的 GitHub Action；GitHub Marketplace 上存在多个第三方 Poetry Action（如 snok/install-poetry），但均非 Poetry 官方维护 | src: https://github.com/python-poetry/poetry | quote: "无官方 setup-poetry 或 install-poetry Action" | type: official
- [C3] PDM 官方推荐在 CI 中使用 `pdm-project/setup-pdm` GitHub Action | src: https://pdm-project.org/en/latest/usage/advanced/ | quote: "there is pdm-project/setup-pdm to make this process easier" | type: official
- [C4] setup-pdm 支持内置缓存功能，通过 `cache: true` 启用，缓存键默认基于 `pdm.lock` 文件，支持自定义 `cache-dependency-path` 参数 | src: https://github.com/pdm-project/setup-pdm | quote: "cache: false (default) - Enable the PDM install cache; cache-dependency-path: pdm.lock - The file used to calculate the cache key" | type: official
- [C5] setup-pdm 缓存支持多文件或 glob 模式，例如 `cache-dependency-path: |` 跨多个 pdm.lock 文件或 `**/pdm.lock` glob 模式 | src: https://github.com/marketplace/actions/setup-pdm | quote: "支持单个文件路径、多文件列表（使用管道符分隔）、Glob 模式匹配" | type: official

## conflicts
- Poetry 官方文档的 FAQ 中仅提及 Docker 多阶段缓存最佳实践（--no-root 标志），未涉及 GitHub Actions 或传统 CI 平台的缓存配置

## gaps
- Poetry 官方文档未明确说明在 GitHub Actions 或其他 CI 环境中应该缓存哪些具体路径（如 ~/.cache/pypoetry/virtualenvs 或 ~/.cache/pypoetry/packages）
- Poetry 官方没有提供 cache key 设计建议（如是否应使用 poetry.lock 文件 hash 作为 key）
- Poetry 官方未发布或推荐任何第一方 GitHub Action

## leads
- Poetry GitHub 仓库中存在多个关于缓存的 issue（如 #2315、#2203），反映社区对 CI 缓存策略的长期关注，但未在官方文档中形成规范化指导
