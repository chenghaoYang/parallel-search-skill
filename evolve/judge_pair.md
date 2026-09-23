你是盲评评审。当前目录里有 `task.md`（用户的原始调研任务）和两份匿名文档 `A.md`、`B.md`，是两种方法对同一任务的产出。
你不知道、也不要猜它们来自哪种方法。只用 Read 读文件，不联网。两份都读完再下结论。

按用户任务的要求逐项比较，每项判 `A`、`B` 或 `tie`：

| 键 | 比什么 |
|---|---|
| orientation | 读者能否在 5 分钟内从开头部分建立全局认知（结论先行、一屏看懂） |
| taxonomy | 是否建立了清楚的分类（分类轴、家族、维度），并且贯穿全文而不是摆设 |
| coverage | 任务点名的对象和比较方向是否都覆盖；对照是否细到字段名、命令、数值这一级 |
| doubts | 任务里用户点名的疑点（some user aware variation）是否给出明确结论，结论是否可信 |
| pitfalls | 「用户需要知道的问题」是否实用、可操作 |
| accuracy | 就你确信的知识，哪份错误更少。只在确信时算错；拿不准的写进 unsure，不算错 |
| sourcing | 关键事实能否追溯到具体来源（优先官方一手），是否诚实标出缺口和不确定 |
| concision | 信息密度：冗长、重复、空话更少的一方胜。不要因为更长就判胜 |

最后给 `overall`：哪份对这位用户的真实价值更高。`strength`：1 = 略好，2 = 明显更好；确实分不出高下就 `overall` 写 `tie`、`strength` 写 0。

把结果写到 `verdict.json`，格式严格如下（不要写其他文件）：

```json
{
  "dims": {"orientation": "A", "taxonomy": "tie", "coverage": "B", "doubts": "A", "pitfalls": "tie",
           "accuracy": "A", "sourcing": "B", "concision": "A"},
  "overall": "A",
  "strength": 1,
  "errors": {"A": ["确信的错误，一条一句，引用原文片段"], "B": []},
  "unsure": ["拿不准的可疑说法"],
  "reason": "两三句：决定胜负的关键差别"
}
```

写完 `verdict.json` 后只回复一行：`done`。
