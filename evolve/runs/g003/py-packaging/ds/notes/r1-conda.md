# r1-conda
question: conda 官方文档里，环境规格文件、锁、Python 版本、前缀、channel/私有源、CI 缓存、以及它和 pyproject.toml / PEP 517 的边界各是什么？conda 有没有 workspace？
checked: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt, https://docs.conda.io/projects/conda/en/stable/commands/create.html, https://docs.conda.io/projects/conda/en/stable/_sources/dev-guide/plugins/environment_specifiers.rst.txt, https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/environments.html, https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html, https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/pip-interoperability.html, https://docs.conda.io/projects/conda/en/stable/_sources/dev-guide/plugins/index.rst.txt, https://docs.conda.io/projects/conda/en/stable/_sources/dev-guide/api/conda/env/specs/yaml_file/index.rst.txt, https://github.com/conda/conda/releases/tag/26.5.0

## claims
- [C1] D1：`environment.yml` 在 stable `conda create` 页是安装时求解的 environment spec，不是该页 lockfile。settings 页标 conda 26.7.2。 | src: https://docs.conda.io/projects/conda/en/stable/commands/create.html | quote: "Create from an environment spec (solved at install time)" | type: official
- [C2] D1：同页 lockfile 不求解；示例 `explicit.txt`。Lockfiles 只列 `explicit: explicit.txt`。 | src: https://docs.conda.io/projects/conda/en/stable/commands/create.html | quote: "Create from a lockfile (no solve, exact reproduction)" | type: official
- [C3] D1：用户指南：锁支持自 conda 26.5。lockfile 含精确包、版本、build、channel。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "Lockfile support is available in conda 26.5 and later." | type: official
- [C4] D1：同页写原生支持 `conda-lock.yaml` 与 `pixi.lock`。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "Conda supports ``conda-lock.yaml`` and ``pixi.lock`` natively" | type: official
- [C5] D1：`@EXPLICIT` 不调用 solver，由 `conda list --explicit` 得到；包 URL 可带 MD5/SHA256。通常不跨平台。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "``@EXPLICIT`` lockfiles allow you to (re)create environments without invoking the solver." | type: official
- [C6] D1：按选定包安装时 solver 会再下载传递依赖。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "This will download and install numerous additional packages to solve for dependencies." | type: official
- [C7] D1：CEP 22 的 freeze 是禁止修改的 marker（`EnvironmentIsFrozenError`），不是包 URL 锁。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "The environment is marked as frozen." | type: official
- [C8] D1：26.5.0（2026-05-15）文件名写作 `conda-lock.yml` 与 `pixi.lock`。 | src: https://github.com/conda/conda/releases/tag/26.5.0 | quote: "multi-platform environment specifiers (``conda-lock.yml``, ``pixi.lock``)." | type: official
- [C9] D2：specifier 页写原生从 YAML 与 explicit 创建环境；后文把 `environment.yml`、`requirements.txt` 称为 single-platform specs。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/dev-guide/plugins/environment_specifiers.rst.txt | quote: "Currently, conda natively supports creating environments from" | type: official
- [C10] D2：`conda create --format` 无 pyproject.toml。可选 cep-24, environment-yaml, env.yml, environment.yml, explicit, requirements.txt, requirements, reqs。 | src: https://docs.conda.io/projects/conda/en/stable/commands/create.html | quote: "Possible choices: cep-24, environment-yaml, env.yml, environment.yml, explicit, requirements.txt, requirements, reqs" | type: official
- [C11] D2：`YamlFileSpec` 把 pyproject.toml 列在环境定义文件举例里，未写 `[project]`。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/dev-guide/api/conda/env/specs/yaml_file/index.rst.txt | quote: "(environment.yml, requirements.txt, pyproject.toml, etc.)" | type: official
- [C12] D4：环境文件依赖名 `python`，例 `python=3.9`；`*` 放开补丁。单包用 `channel::package`，如 `conda-forge::numpy`。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "use the `channel::package` syntax in `dependencies:`" | type: official
- [C13] D4：该 Python 是环境提供的依赖，独立于系统 Python。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/environments.html | quote: "Python itself is a dependency provided in conda environments" | type: official
- [C14] D5：`dependencies` 下有 `pip:`（例 `Flask-Testing`）。pip 之后 conda 不知道这些变化。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "Once pip has been used, conda will be unaware of the changes." | type: official
- [C15] D5：页 “Improving interoperability with pip”。4.6.0 的 `prefix_data_interoperability` 已弃用；现用 `conda-pypi`。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/pip-interoperability.html | quote: "Conda now supports pip-installed packages using the ``conda-pypi`` package." | type: official
- [C16] D5：插件打包示例的 build-backend 是 setuptools，不是 conda。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/dev-guide/plugins/index.rst.txt | quote: "build-backend = \"setuptools.build_meta\"" | type: official
- [C17] D6：`-p/--prefix` 是环境目录全路径。`--prefix ./envs` 可放在项目子目录。 | src: https://docs.conda.io/projects/conda/en/stable/commands/create.html | quote: "Full path to environment location (i.e. prefix)." | type: official
- [C18] D6：环境是装了包的目录。根下 `/envs` 是额外环境的系统位置。示例 `/home/username/miniconda/envs/myenv`。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/environments.html | quote: "The system location for additional conda environments to be created." | type: official
- [C19] D6：`.condarc` 键 `envs_dirs`。`CONDA_ENVS_PATH` 覆盖它（settings，conda 26.7.2）。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html | quote: "The ``CONDA_ENVS_PATH`` environment variable overwrites the ``envs_dirs`` setting" | type: official
- [C20] D7：小节标题 “Using pip in an environment”。`requirements.txt` 见 C10，是 environment spec，不是单独迁移标题。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "Using pip in an environment" | type: official
- [C21] D8：包缓存键 `pkgs_dirs`。未设时除 root 的 `envs` 用 `root_dir/pkgs` 外，用 `envs/pkgs`。`CONDA_PKGS_DIRS` 覆盖该键（26.7.2）。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html | quote: "The ``CONDA_PKGS_DIRS`` environment variable overwrites the ``pkgs_dirs`` setting" | type: official
- [C22] D8：根下 `/pkgs` 也称 `PKGS_DIR`，放已解压、待链接的包。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/environments.html | quote: "Also referred to as PKGS_DIR." | type: official
- [C23] D9：环境文件键 `channels`。`nodefaults` 入该列表即排除默认 channel。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "adding ``nodefaults`` to the channels list." | type: official
- [C24] D9：`.condarc` 键 `channels` 覆盖默认。默认 `channel_alias` 为 https://conda.anaconda.org 。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html | quote: "The default ``channel_alias`` is https://conda.anaconda.org ." | type: official
- [C25] D9：键 `add_anaconda_token` 把 token 加到 channel URL（默认 True；须 anaconda-client 已登录）。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html | quote: "automatically add the token to the channel URLs." | type: official
- [C26] D9：`channel_settings` 自 23.3.0，给单个 channel 加配置，现用于认证 handler。 | src: https://docs.conda.io/projects/conda/en/stable/user-guide/configuration/settings.html | quote: "Added in version 23.3.0." | type: official
- [C27] D10：手写规格是 `environment.yml` 的 `dependencies` 列表，可含 `channels`、`pip:` 与 `variables`。 | src: https://docs.conda.io/projects/conda/en/stable/_sources/user-guide/tasks/manage-environments.rst.txt | quote: "You can create an environment file (``environment.yml``) manually" | type: official
- [C28] D10：26.5.0 起 MatchSpec 可解析可选依赖组；同版约束里的 PyPI extras 例为 `dask[array]`。 | src: https://github.com/conda/conda/releases/tag/26.5.0 | quote: "optional dependency groups, and variant flags in ``MatchSpec`` expressions" | type: official

## conflicts
- create.html 的 Lockfiles 只有 `explicit.txt`，`environment.yml` 是 solved at install time。manage-environments.rst 写 26.5 起支持锁，名 `conda-lock.yaml` 与 `pixi.lock`。specifier 页与 26.5.0 notes 写作 `conda-lock.yml`。未裁决。
- specifier 页开头只列 YAML 与 explicit；后文又有 `requirements.txt`。create.html 把 `requirements.txt` 放在 Environment specs。
- yaml_file 举例含 `pyproject.toml`；`--format` 与 “natively supports” 都没有。不能当成会读 `[project]`。
- lock 三义：create.html `--no-lock` 是 “updating index (repodata.json) cache”；`@EXPLICIT`/conda-lock 是环境锁；CEP 22 是 freeze。

## gaps
- D2：create、specifiers、yaml_file 已打开。无读取 `[project]` 的原句。
- D3：环境页与 plugins index 无 workspace/monorepo。搜 “workspace” 无功能页。不写成“没有 workspace”。
- D4：已打开页无 pyenv。
- D5：无原句说 conda 是或不是 PEP 517 build-backend。`pip:` extras 写法未给出。
- D7：无“从 requirements.txt/pip 迁到 conda”专页标题。
- D8：无已打开页点名 CI 缓存目录。
- D10：环境文件页无分组键；MatchSpec 可选组没有写进 environment.yml 的句子。

## leads
- conda-lockfiles：https://conda-incubator.github.io/conda-lockfiles/getting-started/ （指南外链）。
- pixi.lock 被点名为可读锁；pixi 未查。mamba/micromamba 未写成 conda 的做法；`--solver` 有 `libmamba`。
- conda-pypi：https://conda.github.io/conda-pypi/ （未打开）。conda-build 的 PEP 517 不属于环境规格。
