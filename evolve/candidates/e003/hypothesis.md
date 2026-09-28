# e003 — 自洽改稿留住 [n] 和完整 URL

在 e002 上重试 e001 的成稿自洽检查。e001 的好处留着（一屏/坑对矩阵、重算条数和数字），改稿时不再把引用换掉。

## 证据

e001 的 sourcing −15 全部来自两题，每题 8/8 票把 sourcing 判给基线。prompt-caching 的 sourcing 是 +1，而且是唯一一次自洽之后没有改稿的运行。

**py-packaging（task score −0.875，sourcing −8，accuracy −6，doubts 0）。** `report.md` 的「一屏看懂」7 条从第一份快照起就没有 `[n]`：`ds/snapshots/report.r1.md`、`report.r2.md`、`report.r3-final.md` 和终稿都是 0 个 `[n]`，句末是 `[§1]` `[§2]` `[§3]` `[§4]`。同题基线的一屏是 e000a 15 个 `[n]`、e000b 16 个。终审确实改了概括句（`ds/log.md`：§0 第 2 条「只支持导出」与 §3、笔记 C8 不一致，改成和矩阵一致），改完的句子仍以 `[§3]` 结尾。收尾自查只核对「每个来源编号是否在正文出现过」，把缺的 `[17]` 补进矩阵行，一屏仍然是 0。判决理由点的就是这个：

- `judge/py-packaging/py-packaging__e000a-py-packaging__grok-yx.json`（sourcing −1，判给 DN5X）：「DN5X 一屏里就有选型法则，引用也更细」。
- `judge/py-packaging/py-packaging__e000a-py-packaging__claude-xy.json`（sourcing −1，判给 WQ54）：「关键说法逐格标了来源」。
- `judge/py-packaging/py-packaging__e000b-py-packaging__claude-yx.json`（sourcing −1，判给 BP8N）：「逐条标了一手来源」。

旧规则「其他地方只引用那一节」把 `[§k]` 当成了引用。e001 的「核对 [n]」被做成了「编号至少出现一次」，不是「被改的那句带着该格的 [n]」。

**agent-protocols（sourcing −8，但 doubts +8、accuracy +4，整题仍 +0.375）。** URL 是在 R2 整篇重写时丢的，不是终审抽查时丢的。`ds/snapshots/report.r1.md` 来源节 1304 字、18 个 `https://`；`report.r2.md` 1507 字、0 个 `https://`，地址收成 `modelcontextprotocol.io/.../{changelog, basic/authorization}` 和带 `...` 的无协议路径。当时成稿 6955 字，离 9000 还有约 2000 字，不是预算裁的。终稿（7165 字，来源节 1538 字）维持 0 个 `https://`，`meta.json` 的 `urls: 0`、`traceable: 0.0`。唯一 `[n]` 10 个，e000a 是 38、e000b 是 31（45 个 `https://`，traceable 1.0）。来源节字数是涨的，所以「来源节不许缩」这条长度约束抓不住。

- `judge/agent-protocols/agent-protocols__e000a-agent-protocols__claude-yx.json`（sourcing −1，判给 X8GC）：X8GC「逐条挂了约 40 条具体来源」；e001 这份「来源按厂商打包，难以逐条追溯」。
- `judge/agent-protocols/agent-protocols__e000b-agent-protocols__claude-xy.json`（整题 e001 胜，sourcing 仍 −1，判给 KXF5）：KXF5「来源是完整的一手 URL」。
- `judge/agent-protocols/agent-protocols__e000b-agent-protocols__grok-xy.json`（同样整题胜、sourcing −1）：对方「一手链接和证据分级更容易核对」。

**prompt-caching（+0.75，sourcing +1，doubts +6，accuracy +6，traceable 1.0）。** `ds/log.md`：自洽对照 0 处不一致，10 个来源编号的域名都对，正文不改。一屏仍有 14 个 `[n]`，来源节 12 个 `https://`。自洽检查在没改写出处时是赚的；e001 的 doubts +14、accuracy +4 主要来自这一题和 agent-protocols，py-packaging 的 accuracy −6 把总账拉平。

和 journal 里那句「改概括时保留 [n]、来源节不许缩」的差别：编号「至少出现一次」和「来源节不要变短」这两条，e001 的两份失败成稿都能通过。要守的是被改的那句自己的 `[n]`，以及来源节里的地址仍是笔记 `src` 的完整 `https://`。底座换成已含 e002 的 skill：py-packaging 一屏里被判错的「只有」「不支持」是边界主张，e002 要求它们进一屏之前先反证，自洽改稿不容易再把未反证的否定句抄进开头。

## 假设

终审仍做一屏/坑对矩阵、重算条数和数字。改概括句时必须带上该格原来的 `[n]`，`[§k]` 不算来源；来源节的 URL 不许去掉协议、不许用花括号或省略号合并。每次收束已经要跑的 `roundstat.py` 若看到一屏 0 个 `[n]` 或来源节 0 个 `https://`，先补再交。这样 doubts/accuracy 沿 prompt-caching 那次走，sourcing 和 traceable 不再出现 e001 那两题的整题 −8。

## 改动

只动候选副本（相对当前 skill，`.md` 字符 +529，约 +3.6%）。

- `SKILL.md` 终审：审稿工人同时做自洽对照；改句留下该格 `[n]`，不许缩写或删掉来源节 URL；`roundstat.py` 的 `cite:` 要先补完再交。
- `references/converge.md`：删掉「其他地方只引用那一节」这条例外；引用节要求来源地址是完整 `https://`，一屏不能只标 `[§k]`；审稿标准加一条自洽（工人不改稿），改稿段写明带着 `[n]`、不缩写 URL。
- `scripts/roundstat.py`：成稿一屏没有 `[n]`，或来源节没有 `https://`，打出 `cite:`。退出码仍是 0。用 e001/e002 的终稿对过：只对 e001 的 py-packaging（一屏）和 agent-protocols（URL）报警，prompt-caching 和 e002 的 py-packaging 不报。

## 预期

- sourcing 不再整题 −8；traceable 靠近 e002 的 0.97，而不是 e001 的 0.62。
- doubts、accuracy 沿 prompt-caching（查了、没改出处）和 agent-protocols（doubts +8、accuracy +4）的方向，不要再被一份无 `[n]` 的一屏拖成 py-packaging 的 accuracy −6。
- 不加 spawn。`len_ok` 仍须全过。

## 风险

- 自洽会把矩阵里已经写错、但两边一致的数字抄进一屏。留住 `[n]` 并不纠正笔记本身。e002 只拦住边界主张，拦不住一个查错了的版本号。
- e002 的成稿已经顶到 8999 字。不许缩写 URL 之后，超预算只能删整句。可能伤 coverage，或把 concision 从 e001 的 +6 拉回来。
- `cite:` 只是打印，不改变退出码。主 agent 可以忽视。规则写了「先补再交」，但是否照做要看运行日志里有没有 `cite:` 以及补完后的一屏 `[n]` 数和来源节 `https://` 数。
