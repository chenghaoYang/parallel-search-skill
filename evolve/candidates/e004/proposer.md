model: grok-4.7
minutes: 14.4
leak_terms: []

等待窗口改成先把缺口写入 `log.md` 的 `待查：`，再一次等整批或结束回合；主 agent 要开的页面留给下一轮工人，并删掉「自己抓更全 / 禁用 web_fetch」。

改了 `evolve/candidates/e004/skill/SKILL.md` 和 `references/harness.md`。假设在 `evolve/candidates/e004/hypothesis.md`。工人搜索和终审回原页没改。

预期更多运行在时限内做完下一轮和终审，coverage、doubts、accuracy 上升。`lead_web` 可能降不多：现有计数把工人抓页算进了父会话。
