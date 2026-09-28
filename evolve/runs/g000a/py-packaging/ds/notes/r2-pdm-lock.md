# r2-pdm-lock
question: PDM 锁文件页上「只支持导出 requirements.txt」和「pdm export -f pylock」是不是同一页的两段？lock.format、导出、workspace 各自的 Added in / Experimental 版本号原文是什么？
checked: https://pdm-project.org/en/latest/usage/lockfile/, https://pdm-project.org/en/latest/usage/workspace/

## claims
- [C1] latest 锁文件页 H2「Export locked packages to alternative formats」首段写目前只支持 requirements.txt。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "You can export the pdm.lock file to other formats, which will simplify the CI flow or image building process. At present, only the requirements.txt format is supported." | type: official
- [C2] 同一 H2、同一 URL 的后段（不是另一个标题或另一页）写可导出 pylock.toml；该段在独立 Tip 之后。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "Additionally, PDM supports exporting to pylock.toml format as defined by PEP 751. The following command will convert your lock file to a PEP 751 compatible format:" | type: official
- [C3] 该后段代码块命令是 pdm export -f pylock -o pylock.toml。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "pdm export -f pylock -o pylock.toml" | type: official
- [C4] 导出的版本标签原文是紧挨 pylock 段之前的 Tip「Added in 2.24.0.」，没有「Added in version」；该 Tip 只有这一句，不包住 requirements.txt-only 首段，导出段也无 Experimental。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "Added in 2.24.0." | type: official
- [C5] H2「Change lock file format」写两种锁格式，默认 pdm；pylock 默认文件名为 pylock.toml。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "PDM supports two lock file formats: pdm(default file name is pdm.lock) and pylock(default file name is pylock.toml). The default format is pdm." | type: official
- [C6] 该节 Tip 的版本原文是「Added in 2.25.0.」，不是「Added in version 2.25.0」。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "Added in 2.25.0." | type: official
- [C7] 同一 Tip 把 pylock 锁格式写成 experimental support，不是单独的 Experimental 警告标题。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "Added experimental support for the PEP 751 pylock file format." | type: official
- [C8] 同一 Tip 写 pylock 将在未来版本成为默认。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "It is set to become the default in a future version of PDM." | type: official
- [C9] 切换命令使用配置项 lock.format；本页没有给 lock.format 另写一条独立 Added in，2.25.0 挂在上一 Tip。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "pdm config lock.format pylock" | type: official
- [C10] workspace 页 H1「Workspaces」的 warning 标题是 Experimental，正文写行为仍可能变。 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "Workspace support is experimental. The configuration format and command behavior may change in future releases." | type: official
- [C11] workspace 的版本 Tip 原文是「Added in 2.28.0.」，没有「Added in version」。 | src: https://pdm-project.org/en/latest/usage/workspace/ | quote: "Added in 2.28.0." | type: official
- [C12] 结构判断：两段同时留在 latest 的同一 H2；requirements.txt-only 在 2.24.0 Tip 之前且无版本标签，pylock 导出在该 Tip 之后。像未改掉的开头，不是两个小节，页面也没删任一段。不把其中一句裁定为唯一现行行为。 | src: https://pdm-project.org/en/latest/usage/lockfile/ | quote: "At present, only the requirements.txt format is supported." | type: official

## conflicts
- 同一 URL 同一 H2「Export locked packages to alternative formats」自相矛盾，不裁决：https://pdm-project.org/en/latest/usage/lockfile/ 先写 "At present, only the requirements.txt format is supported."，同节在 Tip "Added in 2.24.0." 之后又写 "Additionally, PDM supports exporting to pylock.toml format as defined by PEP 751." 以及 "pdm export -f pylock -o pylock.toml"。两段都还在页面上。

## gaps
- 三处版本原文都是 "Added in 2.24.0." / "Added in 2.25.0." / "Added in 2.28.0."，页面没有字面 “Added in version”。
- 导出 pylock 段没有 Experimental；Experimental 标题只在 workspace。lock format 用的是 “Added experimental support” 句子，并带 "Added in 2.25.0."。
- lock.format 没有单独的 Added in 句。
- 两页正文和页脚没有 last-updated；HTML meta 只有 readthedocs-version-slug=latest。未打开 changelog，不能另证这三个号是否已发布。

## leads
- 未打开的 stable CLI（https://pdm-project.org/en/stable/reference/cli/）与中文锁文件页（https://pdm-project.org/zh-cn/latest/usage/lockfile）可能和这段英文 latest 不一致。
- 同锁文件页 Lock file freshness 另有 "Changed in 2.28.1."，与 D2/D3 无关。
- changelog（https://pdm-project.org/dev/changelog/）未打开，若要核对 2.24.0 导出、2.25.0 pylock、2.28.0 workspace 的发布说明需另开。
