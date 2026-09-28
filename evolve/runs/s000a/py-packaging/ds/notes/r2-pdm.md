# r2-pdm
question: PDM 的 workspace 成员键、锁格式切换命令、私有源表名，上一轮主张写了但摘录没包含，请用原句补上或否定。
checked: https://pdm-project.org/latest/usage/lockfile/ ; https://pdm-project.org/en/latest/usage/workspace/ ; https://pdm-project.org/latest/usage/config/

## claims
- [C1] PDM 支持 pdm 与 pylock 两种锁格式，默认 pdm | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "PDM supports two lock file formats: `pdm`(default file name is `pdm.lock`) and `pylock`(default file name is `pylock.toml`). The default format is `pdm`." | type: official
- [C2] 切换锁格式的命令为 `pdm config lock.format pylock` | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "You can switch to the `pylock` format with `pdm config` command: `pdm config lock.format pylock`" | type: official
- [C3] pylock（PEP 751）支持于 2.25.0 加入，标记为 experimental | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "Added in 2.25.0. Added experimental support for the PEP 751 pylock file format." | type: official
- [C4] pylock 将在未来版本成为默认格式 | src: https://pdm-project.org/latest/usage/lockfile/ | quote: "It is set to become the default in a future version of PDM." | type: official
- [C5] workspace 成员配置在根项目 pyproject.toml 的 `[tool.pdm.workspace]` 表，键为 `members` | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "Workspace members are configured in the root project's `pyproject.toml`: `[tool.pdm.workspace] members = [\"packages/foo\", \"packages/bar\", \"tools/*\"]`" | type: official
- [C6] `members` 接受直接路径与 glob，成员须为含 pyproject.toml 的目录 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "The `members` list accepts direct paths and glob patterns. Each matched member must be a directory with a `pyproject.toml` file." | type: official
- [C7] `pdm add <path>` 会把成员路径写入 `[tool.pdm.workspace].members` | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "If `packages/foo` is under the project root and contains a `pyproject.toml`, PDM also adds it to `[tool.pdm.workspace].members`." | type: official
- [C8] workspace 功能标记为 experimental | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "Workspace support is experimental. The configuration format and command behavior may change in future releases." | type: official
- [C9] workspace 支持加入版本为 2.28.0 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "Added in 2.28.0." | type: official
- [C10] 私有源表名为 `[[tool.pdm.source]]`，示例含 name/url/verify_ssl 键 | src: https://pdm-project.org/latest/usage/config/ | quote: "`[[tool.pdm.source]] name = \"private\" url = \"https://private.pypi.org/simple\" verify_ssl = true`" | type: official
- [C11] `[[tool.pdm.source]]` 可用键含 url、verify_ssl、username、password、type | src: https://pdm-project.org/latest/usage/config/ | quote: "`url`: The URL of the index `verify_ssl`: (Optional)Whether to verify SSL certificates, default to true `username`: (Optional)The username for the index `password`: (Optional)The password for the index `type`: (Optional) index or find_links, default to index" | type: official

## conflicts
- 无。三处上一轮主张（`pdm config lock.format pylock`、2.25.0、「将来成为默认」）均在 lockfile 页找到原句，全部成立。

## gaps
- lockfile 页未明说 `pdm install` / `pdm sync` 能读取已有的 pylock.toml（导入侧）。页上仅有：格式切换命令、`pdm install --lockfile my-lockfile.lock`（-L/PDM_LOCKFILE 指定其他锁文件，示例为 .lock）、以及导出侧 `pdm export -f pylock -o pylock.toml`（Added in 2.24.0）。pylock.toml 作为输入被 install/sync 直接读取无原句支撑。

## leads
- CLI 参考页或有 pylock 读取细节：https://pdm-project.org/en/latest/reference/cli/ （#install/#sync/#lock）
- lock.format 配置项说明：https://pdm-project.org/en/latest/reference/configuration/
- PEP 751 pylock-toml 规范：https://packaging.python.org/en/latest/specifications/pylock-toml/#pylock-toml-spec
