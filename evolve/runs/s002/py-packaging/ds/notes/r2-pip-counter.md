# r2-pip-counter
question: 只找反例。pip 文档里「pip lock / pip install -r pylock.toml 仍是 EXPERIMENTAL，写自 25.1、读自 26.1，产物只保证当前平台」有没有被更晚的 news 或现行 CLI 页改口？顺带看有没有 pip sync 或 workspace 命令。
checked: https://pip.pypa.io/en/stable/news/, https://pip.pypa.io/en/stable/cli/pip_lock/, https://pip.pypa.io/en/latest/cli/pip_lock/, https://pip.pypa.io/en/latest/cli/pip_install/, https://pip.pypa.io/en/latest/news/, https://github.com/pypa/pip/releases

## claims
- [C1] 现行 stable 文档（v26.2.1）pip lock 页仍标 EXPERIMENTAL，未改口 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "EXPERIMENTAL - Lock packages and their dependencies from:" | type: official
- [C2] 现行 stable 文档 pip lock 页仍写产物只保证当前 python 版本与平台 | src: https://pip.pypa.io/en/stable/cli/pip_lock/ | quote: "The generated lock file is only guaranteed to be valid for the current python version and platform." | type: official
- [C3] 开发版文档（v26.3.dev0，即 main 分支）pip lock 页同样仍是 EXPERIMENTAL + 同一句平台保证，未改口 | src: https://pip.pypa.io/en/latest/cli/pip_lock/ | quote: "EXPERIMENTAL - Lock packages and their dependencies from:" | type: official
- [C4] 开发版 pip install 页 -r 选项仍写 pylock.toml experimental | src: https://pip.pypa.io/en/latest/cli/pip_install/ | quote: "The file or URL can be in pip’s requirements.txt format, or pylock.toml format. pylock.toml support is experimental." | type: official
- [C5] pip lock 的 -r 选项（dev 页）同样注明 pylock.toml experimental，即 lock 命令也能读 pylock.toml 但仍标实验性 | src: https://pip.pypa.io/en/latest/cli/pip_lock/ | quote: "Install from the given requirements file. The file or URL can be in pip’s requirements.txt format, or pylock.toml format. pylock.toml support is experimental." | type: official
- [C6] 26.2 之后唯一已发布版本是 26.2.1 (2026-08-04)，changelog 只有一条 keyring bug fix，无 lock/pylock 条目 | src: https://pip.pypa.io/en/stable/news/ | quote: "26.2.1 (2026-08-04) ... Reallow keyring installed in a (non-activated) virtual environment to be be used via the `import` provider method while installing build dependencies. (#14227)" | type: official
- [C7] latest news 页含未发布段 "Not yet released (2026-09-21)"（未来 26.3）：1 个 feature（wheel console scripts 加速）+ 7 个 bug fix + vendored 升级，无任何 lock/pylock/sync/workspace 条目 | src: https://pip.pypa.io/en/latest/news/ | quote: "Not yet released (2026-09-21) ... Speed up installing a wheel with console scripts by not resolving every `PATH` entry. (#14235)" | type: official
- [C8] 26.2 (2026-07-29) 的 pylock 条目全是增量改进而非转正：Honor --only-final、upload-time 字段、更好报错、远程 path 安全修复 | src: https://pip.pypa.io/en/stable/news/ | quote: "Add support for `pylock.toml` `upload-time` field, so `--uploaded-prior-to` works with `-r pylock.toml`. (#14168)" | type: official
- [C9] stable 与 latest 两版文档的命令列表完全相同：pip, install, uninstall, inspect, list, show, freeze, check, lock, download, wheel, hash, search, index, cache, config, debug —— 无 pip sync、无 workspace 命令 | src: https://pip.pypa.io/en/latest/cli/pip_install/ | quote: "Commands: pip / pip install / pip uninstall / pip inspect / pip list / pip show / pip freeze / pip check / pip lock / pip download / pip wheel / pip hash / pip search / pip index / pip cache / pip config / pip debug" | type: official
- [C10] pip lock 没有 --platform/--python-version/--abi/--implementation 选项（pip install 页有，lock 页 Options 列表中没有），与「只保证当前平台」一致，未出现多平台锁改口 | src: https://pip.pypa.io/en/latest/cli/pip_lock/ | quote: "Options: -o, --output / -r, --requirement / --requirements-from-script / -c, --constraint / --build-constraint / --no-deps / --only-deps / -e, --editable / --src / --ignore-requires-python / --no-build-isolation / --check-build-dependencies / -C, --config-settings / --require-hashes / --no-require-hashes / --progress-bar / --group / --no-clean / index options" | type: official
- [C11] 全量 changelog 中最早 pylock 读条目仍是 26.1 (#13876)，最早 lock 写条目仍是 25.1 (#13213)；grep 全文无更早读支持、无 "pip sync"、无 "workspace" | src: https://pip.pypa.io/en/stable/news/ | quote: "Add experimental support to read requirements from standardized pylock.toml files ( `-r pylock.toml`). (#13876)" | type: official
- [C12] github.com/pypa/pip 不使用 GitHub Releases（页面显示 "There aren’t any releases here"），release notes 唯一载体是 pip.pypa.io changelog | src: https://github.com/pypa/pip/releases | quote: "There aren’t any releases here" | type: official

## conflicts
- 无。R1 的 A–D 四条与现行 stable(v26.2.1)/latest(v26.3.dev0) 页面及全部更晚 news 完全一致，未找到任何反例。

## gaps
- 未找到反例。最新已发布 news 条目：26.2.1 (2026-08-04)；latest 文档另有未发布段 "Not yet released (2026-09-21)"（对应 26.3.dev0），亦无 lock/pylock 改口。打开过的 URL 见 checked。
- 未逐条核对 GitHub 上 main 分支 news/ 目录的 towncrier 片段（latest news 页 2026-09-21 已编译进未发布条目，覆盖该来源）。

## leads
- pip lock 的 -r 也能读 pylock.toml（C5），即「读 pylock.toml」不只属于 pip install；写大题时注意归属。
- 26.2 起 -r pylock.toml 已支持 --only-final / --uploaded-prior-to（#13950、#14168），读路径功能在增强但仍是 experimental。
