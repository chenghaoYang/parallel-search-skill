# audit — report.md 主张抽查（对照 notes/）

笔记别名：pip=r1-pip-pep751, uv=r1-uv, poe=r1-poetry, pdm=r1-pdm, pixi=r1-pixi, scout=r1-scout, pip2=r2-pip-check, pixi2=r2-pixi-check, poe2=r2-poetry-check, uv2=r2-uv-check

格式：判定 | 主张原文 | 依据 | 建议改法

## 头部版本号
- supported | "uv 0.12.19 / pip 26.2.1 / Poetry 2.5.1 / PDM 2.29.2 / pixi 0.81.0" | uv2 C1（0.12.19, 2026-09-24）; pip2 C10（26.2.1, 2026-08-04）; poe2 C14（2.5.1, 2026-09-20）; pdm C1（v2.29.2, 2026-09-17）; pixi2 C9（v0.81.0, 2026-09-15） | —

## 0. 一屏看懂
- supported | "PEP 751 已 Final（2025-03-31，文件名 pylock.toml/pylock.<name>.toml，多环境设计）" | pip C1（Status: Final, Resolution 31-Mar-2025）/C2（命名正则）/C3（environments 键） | —
- supported | "没有一家拿它当默认锁：pip 25.1 起实验性 pip lock、26.1 起 pip install -r pylock.toml（仅保证当前平台）" | pip C5（25.1 experimental pip lock）/C6（26.1 -r pylock.toml）/C8（"only guaranteed…current python version and platform"）; pip2 C5 | —
- supported | "uv 0.6.15 起可导出/uv pip 读 pylock.toml，项目主锁仍是专有 uv.lock" | uv C5（0.6.15 preliminary）/C6（project interface 继续用 uv.lock）/C3（"specific to uv"） | —
- supported | "PDM 2.25 起可 lock.format=\"pylock\" 实验启用" | pdm C6（2.25.0 experimental, `pdm config lock.format pylock`） | —
- supported | "Poetry 仅插件导出" | poe C11（2.3.0 起 poetry-plugin-export 导 pylock.toml）; scout C9 | 可补"2.3.0 起"版本号
- supported | "Poetry 2 确认改用标准 [project] 表（PEP 621）；[tool.poetry] 只剩 package-mode、requires-poetry 等专有配置；^x.y caret 不能写进 project.dependencies" | poe C1（2.0.0 PEP 621）/C4（字段弃用）/C5（保留字段含 packages/group 依赖/requires-plugins）/C18（"Not supported in project.dependencies"） | "只剩"略窄：tool.poetry 还留 packages/include/exclude 与 group 依赖，"等"字可盖，可不改
- supported | "uv 原生 workspace（members glob、单一锁、成员 editable）；PDM 2.28 起实验性；Poetry 无内置；pixi 是多 environment 模型而非包 workspace" | uv C8/C9; pdm C9（2.28.0 experimental）; poe2 C1（7 页 0 命中）/C2（#2270 OPEN 2020）; pixi2 C1（[workspace] 无 members 字段）/C2 | —
- supported | "uv uv python install、PDM pdm python install 用 python-build-standalone；Poetry 2.1 起实验 poetry python install；pixi 自动装 conda 包解释器；pip 不管" | uv C11; pdm C11; poe C17（2.1.0 experimental, Python Standalone Builds）; pixi C12; pip C14（"Pip is the package installer"） | —

## 2. 对照矩阵 — 表 1
- supported | uv D2 "uv.lock：universal 跨平台、uv 专有；pylock 仅导出/uv pip/uv run --with-requirements" | uv C3/C6/C7; uv2 C7（--with-requirements 接受 pylock.toml）/C8 | —
- supported | uv D3 "[tool.uv.workspace] members glob、共享锁、成员 editable" | uv C8（members required+exclude optional, globs）/C9（single lockfile, editable） | —
- supported | uv D5 "自带 uv_build（0.5 引入/0.7.19 stable，仅纯 Python；0.12 起 uv init 默认）；可作任意后端 frontend" | uv2 C11（0.5.0 experimental）/C13（0.7.19 stable）/C15（0.12.0 init 默认）; uv C14（only pure Python）/C16（frontend） | —
- supported | uv D6 "自动建 .venv，uv sync 精确同步" | uv C17/C18（exact, 删多余包） | —
- supported | pip D2 "pip lock→pylock.toml（实验、仅当前平台）；可复现路径=req.txt ==+--hash+wheelhouse" | pip C8/C10/C12; pip2 C5（无 --platform 类选项） | —
- unsupported | pip D5 "—（PEP 517 frontend）" | 10 份笔记均无 pip×PEP 517 条目 | 低风险细节；补 pip 官方文档一手来源或删去括号
- supported | pip D6 "靠 stdlib venv" | pip C15 | —
- supported | Poetry D1 "2.0 起 [project]；package-mode=false 纯依赖管理" | poe C1/C38（不装项目本体） | —
- supported | Poetry D2 "poetry.lock（v2.1，专有）；pylock 仅插件导出" | poe C9（locker.py _VERSION="2.1"）/C11 | —
- supported | Poetry D3 "无内置（issue #2270 open 自 2020）；path develop=true 仅本地开发" | poe2 C2（OPEN, 2020-04-05）/C3; poe C13 | —
- supported | Poetry D4 "2.1 起实验 poetry python install（Python Standalone）；或 poetry env use" | poe C17/C15 | —
- supported | Poetry D5 "默认 poetry-core；2.1 起后端无关" | poe C20/C21（2.1.0 build-system agnostic） | —
- supported | Poetry D6 "{cache-dir}/virtualenvs 或已有 .venv" | poe C24 | —
- supported | PDM D1 "[project] PEP 621；库标 distribution=true" | pdm C2/C3 | —
- supported | PDM D2 "pdm.lock 默认跨平台（--platform 可锁非当前平台）；lock.format=pylock 实验（2.25）" | poe2 C11（"the generated lockfile is cross-platform"）/C10（--platform=linux 等）; pdm C5/C6 | —
- supported | PDM D3 "实验（2.28）：[tool.pdm.workspace] members glob、共享锁" | pdm C9 | —
- supported | PDM D4 "pdm python install（pbs，2.13）；路径存 .pdm-python" | pdm C11（v2.13.0, python-build-standalone）/C12 | —
- supported | PDM D5 "不强制（默认 pdm-backend；不支持 poetry-core）" | pdm C13（"not supported because it does not support reading PEP 621"） | —
- supported | PDM D6 "默认 .venv；python.use_venv=false 切 PEP 582 __pypackages__" | pdm C15/C16/C17 | —
- supported | pixi D1 "pixi.toml 或 pyproject [tool.pixi]（TOML 1.1 语法坑）" | pixi C1/C2（"most Python tooling only reads TOML 1.0"） | —
- supported | pixi D2 "pixi.lock（格式 v7）：全 environment×platform 一把锁，conda+PyPI 同锁" | pixi2 C7（v0.68.0 bump v7）/C8（rattler LATEST=V7）; pixi C6/C7 | §5 已注明文档示例滞后写 6，处理得当
- supported | pixi D3 "成员包各自 manifest，根 [workspace.dependencies] path 引用、workspace=true 继承（环境表 0.73 起免 preview）" | pixi C11; pixi2 C2/C4（v0.73.0 环境表免 preview） | —
- supported | pixi D4 "解释器=conda 包自动装" | pixi C12 | —
- supported | pixi D5 "pixi build→conda 包（仍 preview）" | pixi C14; pixi2 C5（changelog 无转正条目） | —
- supported | pixi D6 ".pixi/envs/ 每环境一目录" | pixi C17 | —

## 2. 对照矩阵 — 表 2
- supported | uv D7 "仅 pip→project 指南：uv add -r req.in，-c 保留已锁版本" | uv C20; scout C11 | —
- supported | uv D8 "setup-uv enable-cache(auto)；uv cache prune --ci" | scout C16（auto 规则）/C18/C21 | —
- supported | uv D9 "[[tool.uv.index]] default/explicit/first-match；index pin 防依赖混淆" | uv C23/C24/C10; scout C26/C28 | —
- supported | uv D10 "PEP 735✅（dev 组默认装）、723✅、668 break-system-packages" | uv C26/C27/C28 | —
- weak | pip D8 "setup-python cache:'pip' 缓存 pip 目录（二手）" | pip C18（type: secondary, setup-python README） | 报告已自标"二手"；升级需直接引 README 原句为 official
- supported | pip D9 "--index-url/--extra-index-url；netrc/keyring" | pip C19/C20 | —
- supported | pip D10 "PEP 668（23.0 起）；735 --group（25.1）" | pip C22（23.0 实现）/C23（25.1 --group） | —
- supported | Poetry D7 "无官方 req.txt 导入；1→2 手动改 pyproject + config --migrate" | poe2 C4（28 命令无 import）/C5/C6; poe C27 | —
- supported | Poetry D8 "pipx 装+固定版本；cache-dir ~/Library/Caches/pypoetry 等" | poe C29/C30/C31 | —
- supported | Poetry D9 "[[tool.poetry.source]] primary/supplemental/explicit；配 primary 关隐式 PyPI" | poe C32; scout C30 | —
- supported | Poetry D10 "PEP 735（2.2）；723 无官方支持" | poe C35（2.2.0）; poe2 C8（7 页+history grep "PEP 723" 0 命中，已验证否定） | —
- supported | PDM D7 "pdm import 5 格式：Pipfile/Poetry/Flit 段、req.txt、setup.py" | pdm C18 | —
- supported | PDM D8 "setup-pdm@v4 内置 cache（key=./pdm.lock）；集中 wheel 缓存可选" | pdm C19/C20 | —
- supported | PDM D9 "[[tool.pdm.source]]+include/exclude_packages；keyring" | pdm C21/C22 | —
- supported | PDM D10 "735（2.20）、723（2.16）、实验 use_uv" | pdm C23（2.20.0）/C24（2.16.0）/C25（2.19.0） | —
- supported | pixi D7 "pixi init --import environment.yml（仅 conda-env）" | pixi C19 | —
- supported | pixi D8 "setup-pixi 见 pixi.lock 自动缓存" | pixi C20; scout C24 | —
- supported | pixi D9 "私有 channel：bearer/conda-token/basic/S3；[pypi-options]" | pixi C21/C4 | —
- supported | pixi D10 "pypi-deps 用 uv 解析库，conda 优先" | pixi C23（"Pixi uses the uv library"）/C22 | —

## 3. 变体与适配层
- weak | "pip-tools：第三方，给 pip 补 .in→全 pin requirements.txt 锁工作流" | pip C11（official："a package that builds upon pip…workflow"）+C13（type: secondary，pip-compile/pip-sync 细节） | 核心有 official 兜底；如需全 official 可引 jazzband/pip-tools repo
- supported | "poetry-plugin-export：2.0 起 export 变插件；导 requirements.txt / pylock.toml" | scout C2/C9; poe C11 | —
- supported | "Hatch/hatchling：PyPA 项目管理器+后端，uv_build 之外的纯 Python 后端选项" | scout C31; uv C14（扩展模块建议换 hatchling） | —
- supported | "pipenv 仍维护；pyenv 只切解释器；pipx 隔离装 CLI" | scout C15（PyPI 2026.8.0, 2026-08-20）/C32/C33 | —
- supported | "conda/mamba/miniforge：原版/C++ drop-in/conda-forge 专用安装器；pixi 是 Rust 重写、非 drop-in" | pixi C25; scout C34/C35 | —
- supported | "rye：2026-02 归档停更，官方指 uv 继任" | scout C10（2026-02-05 archived） | —

## 4. 需要知道的坑
- supported | 坑1 "pip 官方警告 --extra-index-url 装私有包是 dependency confusion 风险（各 index 无优先级、取 best 匹配）" | pip2 C1（Warning 框原句）/C2（"no priority…best match"） | —
- supported | 坑1 "uv first-match+explicit/index pin、Poetry explicit、PDM include/exclude_packages 才是防护" | uv C23/C24/C10; scout C26/C29; pdm C22 | —
- supported | 坑2 "Poetry 1→2：shell/export 变插件、lock 默认 --no-update、prefer-active-python 反转为 use-poetry-python、弃 3.8、读不了 <1.1 的 lock" | scout C1/C2/C3/C6/C7; poe C12/C10 | —
- supported | 坑3 "平台专属 req.txt 不能直接当 uv -c（markers 冲突），先 uv pip compile --python-platform … --no-strip-markers" | scout C12 | —
- supported | 坑4 "PEP 668：报 externally-managed 是设计行为，用 venv/pipx，勿 --break-system-packages" | pip C22（EXTERNALLY-MANAGED, 导向 venv）; uv C28 | "勿"为编辑性建议，与 PEP 668 导向一致，可保留
- supported | 坑5 "uv 缓存不感知 flat index 同文件名替换，要 --refresh；CI 末尾 uv cache prune --ci" | scout C22/C21 | —
- supported | 坑6 "pixi 混装时 conda 优先且钉住 PyPI 解，冲突加 [constraints]" | pixi C22/C23 | —

## 5. 未决与置信度
- supported | "poetry.lock 跨平台官方仅 FAQ 暗示；PDM 默认切 venv 的版本未确认" | poe2 C7+gaps（7 页 grep 0 命中已记录）; pdm gaps | —
- supported | "pixi build 与 package 表 workspace 依赖仍 preview；pixi.lock 已 v7 但文档示例仍写 6" | pixi2 C3/C5/C6/C7（conflicts 节已记文档滞后） | —
- supported | "pip lock 仅当前平台：PEP 751 格式支持多环境，pip 实现未到" | pip2 C5/C8; pip C3/C8 | —
- supported | "setup-python 缓存为二手来源" | pip C18 type=secondary，与正文标注一致 | —

## 计数
- supported: 49
- weak: 2（pip D8 setup-python 缓存[已自标二手]；pip-tools 工作流细节）
- unsupported: 1（pip D5 "PEP 517 frontend" 括号注）
- contradicted: 0
- 合计抽查：52 条
