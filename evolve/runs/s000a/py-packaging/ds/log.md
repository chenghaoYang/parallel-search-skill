# 轮次日志

## R0

观察：用户要选型，不是功能清单。点名疑点是 PEP 751（uv 与 pip）和 Poetry 2 的 `[project]`。种子里 pixi/conda 是一对，但职责可能不同。

决策：taxonomy v0 用两条轴。轴 1 = 拥有哪一层（安装器 / 项目经理 / 环境经理）。轴 2 = 清单与锁是否靠 PEP 621 / PEP 751。维度 8 个：lock、meta、workspace、pyver、backend、index、cicache、migrate。conda 单独成行但 R1 不派专工。

R1 计划（6 个工人，按来源边界）：pip（含 PEP 751 文本）、uv、Poetry、PDM、pixi 各填自己那一行；scout 只交 leads（坑、未列入的实体和维度）。

→ 动作：spawn R1 → 预计 spawn：6

## R1

结果：6/6 返回。lint：136 claims，全部 official，0 缺 src/quote。超长：r1-pdm 9426、r1-poetry 10178、r1-uv 10970。冲突 8，gaps 23，leads 21。摘录撑不住的半句没有写进成稿。

taxonomy v0→v1：轴 1、轴 2 保留。`workspace` 收紧为「多包是否共享一把锁」，因为 pixi 的 `[workspace]` 是清单根。PEP 735 并进 meta，不加列。Hatch、Pipenv、Rye、pip-tools、conda-lock 不升格成行。

成稿：`snapshots/report.r1.md` 8989（预算 9000）。为了塞进 Q1/Q2 的形态，删掉 package-mode、cyclonedx 导出格式，以及 Poetry「CI 必须钉版本」的重复句。roundstat：✅ 34、⚔ 3、❓ 10、∅ 1，resolved 35/48（73%）。

R1 观察：conda 行几乎是空的，lock 还和 pixi 对比表打架，这是种子里的另一半。pip/uv 的 pylock、Poetry 2 的 `[project]` 已有官方原句，但小版本号不在摘录里，又和「pip 不锁、Poetry 只有 tool.poetry」的旧认知相反，所以没写进第 0 节。PDM 的成员键、pixi 的成员键和 channel 键仍空着。

→ 动作：只复核这些洞 → 预计 spawn：5
（r2-pylock、r2-poetry、r2-conda、r2-pdm、r2-pixi）

## R2

结果：5/5。lint：100 claims，全 official，1 条缺 quote（r2-pixi C5，未采用）。r2-conda 超长 10075。

新增并写进成稿：Poetry 弃用键名单、2.3.0 导出 pylock、`poetry python install` 为 2.1.0 experimental；PDM `lock.format pylock`（2.25.0，将来默认）与 `[tool.pdm.workspace].members`（2.28.0）；pixi 必填 `channels`/`platforms`、无 members、`index-url`；conda 26.5 的 lockfile 命令。第 0 节因此写上 Q1/Q2 的形态。

为了不比 R1 更长，删掉：Hatch/Pipenv/Rye 变体句、package-mode 的解释、PDM 安装器自身的四套 Python 要求、若干重复的坑。

R2 观察：主矩阵除 3 个 ⚔ 外都有原句。剩下真正影响选型结论的洞只有两处：pip/uv 的小版本号仍不在摘录字符串里；conda「natively」和「必须装插件」还没人用发布说明判哪句是安装后的默认状态。

→ 动作：两份更窄的复核 → 预计 spawn：2
（r3-versions、r3-conda-plugin）

roundstat：report.r1.md 8989，report.r2.md 8980（短 9）。grid：✅ 44、⚔ 3、❓ 0、∅ 1，resolved 45/48（94%）。
