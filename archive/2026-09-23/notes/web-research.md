> 归档于 2026-09-24。这是历史材料，不代表现行做法。
> 现行入口：仓库根 README.md。现行流程：skills/deep-search/SKILL.md。现行 bench：bench/README.md。

# 公开资料：大规模并行搜索 skill 与 harness

调研日：2026-09-23。下面只写打开过页面、或检索工具返回了对应页面摘录的内容。数字都标明出处和条件。没有打开到的并发数、token、胜率不写。Perplexity 官网多次被 Cloudflare 拦住，相关句子只来自检索摘录，并在第 5 节标出。

## 1. 可以借鉴的分工

这张表比的是公开研究/搜索系统，不是编码 harness。编码产品里 model、skill、harness 怎么拆，放在第 2 节。

| 系统 | 来源与页面上的时间 | 搜索并行方式 | skill/提示 与 harness/运行时 | 引用和停止 | 不适合照搬 |
| --- | --- | --- | --- | --- | --- |
| Anthropic Research（多 agent） | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)，Published Jun 13, 2025 | Orchestrator-worker。Lead 分析问题后并行派 subagent；文中为了速度写了两类并行：lead 一次拉起 3–5 个 subagent，而不是串行；每个 subagent 并行用 3 个以上工具。复杂查询上，这两类并行把研究时间最多砍掉 90%。Lead 目前同步等这一批 subagent 结束才能继续。 | 他们没有用 harness / skill 这两个词。Agent 被定义成「在循环里自主用工具的 LLM」。分工几乎全在提示里：lead 负责拆任务并写清目标、输出格式、工具和来源、边界；subagent 各自搜索、用 interleaved thinking 评估结果。提示里还写了力度：简单事实用 1 个 agent、3–10 次工具调用；直接比较用 2–4 个 subagent、各 10–15 次；复杂研究可以超过 10 个 subagent。早期失败是简单问题派出 50 个 subagent。 | 研究循环结束后，另有 CitationAgent 对着文档和报告标引用位置。Lead 自己判断信息够不够，不够就再派或改策略。计划写入 Memory，因为上下文超过 200,000 tokens 会被截断。内部研究评测：Opus 4 做 lead、Sonnet 4 做 subagent，比单 agent Opus 4 高 90.2%。BrowseComp 上，token 用量、工具调用次数、模型选择合起来解释 95% 的表现方差，其中 token 用量单独解释 80%。他们的数据里，agent 大约是聊天的 4 倍 token，多 agent 大约是聊天的 15 倍。改写工具描述后，后续 agent 的任务完成时间下降 40%（该工具被测了几十次）。 | 90.2%、4×/15×、3–5、90% 都是他们自己的内部用法或内部评测，不是公开基准上的通用定律。同步等待会被一个慢 subagent 堵住。需要共享上下文或步骤强依赖的任务，他们明确说不适合。编码任务的可并行部分通常少于研究。 |
| OpenAI Deep Research | [Introducing deep research](https://openai.com/index/introducing-deep-research/)，February 2, 2025。同页更新：2025-02-05、2025-02-25、2025-04-24、2025-07-17、2026-02-10 | 公开帖没有写 fan-out 的并发个数。写的是端到端强化学习训出来的多步轨迹：搜索、读文本/图片/PDF、用 Python、碰壁后改方向。2025-07-17 起，更深的浏览放到 ChatGPT agent 的视觉浏览器里；原来的 deep research 仍在工具菜单。 | 没有公开的 SKILL.md。产品行为在模型训练和 ChatGPT 运行时里，不在一份可移植 skill。2026-02-10 更新：可接任意 MCP 或 app，并可把网页搜索限制在受信任站点；可看进度、中途打断、用后续提示或新来源修正。 | 输出要有清晰引用，并引用来源里的具体句子或段落；侧边栏给出步骤和来源摘要。耗时「5 to 30 minutes」。Humanity's Last Exam：deep research（带 browsing + python tools）26.6%；对照表里 GPT-4o 3.3、Grok-2 3.8、Claude 3.5 Sonnet 4.3、Gemini Thinking 6.2、o1 9.1；带星号的文本子集：DeepSeek-R1 9.4、o3-mini medium 10.5、o3-mini high 13.0。GAIA：pass@1 的 Level 1/2/3/Avg 为 74.29 / 69.06 / 47.6 / 67.36；cons@64 为 78.66 / 73.21 / 58.03 / 72.57。脚注说 GAIA 答案在网上大量泄漏，他们屏蔽了若干网站才评。限额是产品配额，不是研究停止条件：上线时 Pro 最多每月 100 次；2025-04-24 起 Plus/Team/Enterprise/Edu 每月 25 次完整版、Pro 250、Free 5，超出后改走 o4-mini 轻量版。 | 「几百个网上来源」「研究分析师水平」是产品描述，不是实验计数。内部专家任务只有「浏览越多越好」的图，正文没有给出可引用的通过率数字。幻觉和权威性判断仍被列为限制。架构细节不公开，不能把它写成可复现的编排规格。 |
| Gemini Deep Research / Max | [Gemini API 文档](https://ai.google.dev/gemini-api/docs/deep-research)（打开时为 preview）；[博客](https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/)，Apr 21, 2026 | 文档把流程写成 Plan → Search → Read → Iterate → Output，延迟是分钟级，必须 `background=true`。没有写同时开多少个搜索 worker。两个 agent id：`deep-research-preview-04-2026`（速度）和 `deep-research-max-preview-04-2026`（更长 test-time compute）。博客说 Max 相对 2025 年 12 月预览「查阅明显更多来源」，但没有给出来源个数。 | 没有 skill 文件。范围、格式、语气写在当次 input 里。`collaborative_planning=true` 时先回计划，用户改完再把该开关关掉才执行。默认工具是 Google Search、URL Context、Code Execution；可加 MCP 和 File Search，也可以只开其中一部分，从而关掉网页。 | 文档要求对照响应里的 citations 核对来源。停止条件是 interaction 状态变成 `completed` 或 `failed`，客户端轮询或重连流。流式示例写明连接可能在 600 秒超时后断开，要用 `interaction_id` 和 `last_event_id` 续上。安全说明把上传文件和网页都当成不可信输入。 | 博客上的胜率图没有在正文里写出百分比，这里不转抄。agent id 和 Interactions API 是 2026-04 这一代预览，不能当成稳定协议。File Search 语料库怎么建、和网页结果怎么去重，文档没有规定。 |
| Perplexity Deep Research，以及 Computer 里的 Search as Code | 检索摘录，未打开完整 HTML：[Introducing Perplexity Deep Research](https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research)（摘录中的日期 Feb 14, 2025）；[What is Research mode?](https://www.perplexity.ai/help-center/en/articles/10738684-what-is-research-mode)；[Deep Research, now in Computer](https://www.perplexity.ai/hub/blog/deep-research-now-in-computer)（摘录日期 Jun 11, 2026）；[DRACO](https://research.perplexity.ai/articles/evaluating-deep-research-performance-in-the-wild-with-the-draco-benchmark)（摘录日期 2026-02-04） | 2025-02 帖：一次 Deep Research 做 dozens of searches、读 hundreds of sources，用搜索和代码迭代，边学边改计划，再写报告。帮助中心：大多数任务 under 3 minutes，生成回答大约 4 到 5 minutes。2026-06 Computer 帖把搜索写成程序：模型写代码，把问题拆成 hundreds or thousands of targeted retrievals，并行跑，不够就再试；进模型前用代码 dedupe、join、filter。 | DRACO 文把「Deep Research harness」说成 model agnostic：换更强的 agentic LLM 就重跑评测。帮助中心说 Research 模式自己选模型，用户不能指定。没有公开 SKILL.md。 | 产品描述是综合报告，不是单独的引用 agent。停止写在行为里：评估证据是否够、记下冲突，再合成。摘录里没有公开的并发上限或 token 预算。 | 「dozens / hundreds / thousands」是产品文案，不是带实验条件的计数。Cloudflare 挡住了正文页，不能把检索摘录扩写成架构图。DRACO 摘录只确认他们用了 harness 这个词，没有打开到榜单数字，所以这里不写胜率。 |
| xAI Grok DeepSearch | [Grok 3 Beta](https://x.ai/news/grok-3)，页面日期 Feb 19, 2025 | 帖子把 DeepSearch 写成第一个 agent：代码解释器和互联网，查询缺失上下文，处理互相冲突的事实和观点，最后给一份简短报告。没有写并行子 agent 或停止规则。 | 这是模型和产品功能，不是 skill。同页其他数字（AIME cons@64 93.3%、GPQA 84.6%、LiveCodeBench 79.4%、Chatbot Arena Elo 1402、1M context）是 Grok 3 / Think 的模型结果，不是 DeepSearch 的搜索实验。 | 公开描述停在「综合后给出报告」。没有引用格式、重试或预算。 | 不能把 Think 的数学/代码分数当成 DeepSearch 的研究质量。后文 API 文档里的 `grok-4.20-multi-agent` 用 `reasoning.effort` 控制协作 agent 数量，那是另一页、另一代模型，见第 3 节，不要和 2025-02 的 DeepSearch 混成一个系统。 |
| Manus Wide Research | [Introducing Wide Research](https://manus.im/blog/introducing-wide-research)，栏目标成 Thursday, July 31，配图路径含 `2025/07/31`；[帮助中心](https://help.manus.im/en/articles/11960169-what-is-wide-research)，页面写 March 17, 2026。配套运行时见 [Context Engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)，作者署 2025/7/18 | 面向「很多相似项」而不是一个开放问题。博客：每个 subagent 都是完整的通用 Manus，而不是预写死的 manager/coder 角色。帮助中心：只能自动触发；付费用户；同一时刻跑 20 个 subtask；每个 subtask 积分上限 50。 | 博客把 Wide Research 说成系统级并行机制和 agent 间协议，不是一份提示。2025-07-18 的上下文工程才是他们公开的运行时：循环、沙箱虚拟机、KV-cache、用文件系统当外部记忆、用 todo.md 把目标反复写进上下文末尾。平均输入输出 token 比大约 100:1；典型任务大约 50 次工具调用。Claude Sonnet 的缓存价被他们写成 cached 0.30 USD/MTok、未缓存 3 USD/MTok。 | 帮助中心的停止/预算是积分帽，不是证据标准。上下文帖要求失败轨迹留在上下文里，方便模型别再犯；压缩必须能还原（网页可以丢掉正文，但要留 URL；文件留路径）。 | 「把算力放大 100×」在博客里是他们问自己的问题，不是测量结果。20 路和 50 积分是 Manus 计费策略。全功能虚拟机 subagent 的成本结构不能当成轻量检索 worker 的默认。 |
| LangChain Open Deep Research | [博客](https://www.langchain.com/blog/open-deep-research)，July 16, 2025；[仓库 README](https://github.com/langchain-ai/open_deep_research)；打开时的 [configuration.py](https://github.com/langchain-ai/open_deep_research/blob/main/src/open_deep_research/configuration.py) | 三阶段：Scope（澄清 + 研究简报）、Research（supervisor 把独立子题派给隔离上下文的 subagent）、Write（所有研究结束后一次性写报告）。早期让 subagent 并行写章节，报告会散。打开时的配置默认：同时研究单元 5（允许 1–20），supervisor 反思迭代 6（1–10），单个 researcher 的工具循环 10（1–30）。网页正文在摘要前最长 50,000 字符。 | 提示在图的节点里，不在 SKILL.md。Supervisor 用简报判断还缺什么；subagent 只做子题，结束前再叫一次模型，把原始网页和失败的工具结果压成带引用的干净答案。用户自带模型、搜索 API 和 MCP。 | 停止由 supervisor 判断简报是否被覆盖，加上上面的迭代和工具次数上限。结构化输出失败最多重试 3 次。README 记录 Deep Research Bench：100 个博士级任务（英/中各 50，22 个领域），榜单用 Gemini 做 LLM-as-judge 的 RACE。他们列出的一次提交（commit `c0a160b`，摘要模型 gpt-4.1-nano，研究/压缩 gpt-4.1）RACE 0.4344，207,005,549 tokens，87.83 美元，当时榜上第 6、总分 0.4344（2025-08-02 的 README 更新）。同表 Defaults（`6532a41`）RACE 0.4309、58,015,332 tokens、45.98 美元；Claude Sonnet 4 研究模型那一行 0.4401、138,917,050 tokens、187.09 美元；GPT-5 研究模型那一行 0.4943、204,640,896 tokens。跑满 100 题大约 20–100 美元，视模型而定。 | 0.43 分是这一套模型配置在这个榜上的分数，不是「多 agent 研究」的通解。默认并发 5 是仓库滑块的默认值，README 写明并发高了会撞 rate limit。博客里的 15× token 是转述 Anthropic，不是他们自己的新测量。 |
| GPT Researcher | [README](https://github.com/assafelovic/gpt-researcher/blob/main/README.md)（打开时的 `main`） | Planner 生成研究问题，execution/crawler 按问题收集，publisher 过滤并汇总。README 把加速归于并行 agent，而不是同步跑完。Deep Research 是可配置深度和广度的树，分支并发。多 agent 示例受 STORM 启发：先浏览，编辑定大纲，再按大纲主题并行研究。 | 可以当成 Claude skill 安装（`npx skills add assafelovic/gpt-researcher`），那是把整套研究程序交给别的 agent 调，不是 Agent Skills 规范里的薄 SKILL.md。角色提示在 planner / crawler / publisher。MCP 通过 `RETRIEVER=tavily,mcp` 和网页检索混用。 | 报告带引用。README 的产品说法包括：聚合超过 20 个来源、报告可以超过 2,000 词、Deep Research 大约 5 分钟、用 `o3-mini` 且推理努力为 high 时大约 0.4 美元一次；多 agent 流程平均产出 5–6 页。这些是仓库自述，不是独立评测。本地文档用 `DOC_PATH`，前端选 “My Documents”，或 `report_source="local"`。 | 「站越多、高频事实越不可能全错」是 README 的假设，不是实验结果。没有公开的证据分级或跨本地/网页的去重协议。星数各镜像不一致，这里不引用。 |
| STORM / Co-STORM | 论文 [Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models](https://arxiv.org/abs/2402.14207)，Yijia Shao、Yucheng Jiang、Theodore A. Kanell、Peter Xu、Omar Khattab、Monica S. Lam；提交 2024-02-22，修订 2024-04-08；NAACL 2024。代码与流程：[stanford-oval/storm](https://github.com/stanford-oval/storm) | 不是「一项一个 agent」的宽并行。预写阶段：从相近题目归纳多种视角，再模拟「维基写作者问、领域专家基于互联网来源答」的对话，用追问更新理解，然后整理成大纲；写作阶段才根据大纲和参考文献成文。Co-STORM（README 指向 arXiv:2408.15232，EMNLP 2024）改成话语轮次：专家、主持人、人；主持人专门问检索里出现但还没被用到的信息。 | 模块化 LM，不是 skill。README 建议便宜模型做对话模拟和提问，更强模型做成文和润色。检索器可换 You.com、Bing、Serper、Tavily、向量库等。 | 文章带引用。论文相对 outline-driven RAG 基线：STORM 的文章被判断为组织得更好的绝对增幅 25%，覆盖更广的增幅 10%。评测集是他们建的 FreshWiki（近期高质量维基页）；也收集了有经验的维基编辑意见。编辑反馈指出的新问题包括来源偏见转移，以及把不相关事实过度关联。README 说 FreshWiki 是 2022-02 到 2023-09 编辑最多的页面里的 100 篇。停止点是管道开关：`do_research`、`do_generate_outline`、`do_generate_article`、`do_polish_article`，不是模型自己宣布证据足够。 | 25% / 10% 只相对于那一个大纲驱动 RAG 基线，评的是大纲和长文，不是问答准确率。系统写不出可直接发布的维基页。多视角对话是串行模拟，不能当成 Map-Reduce 宽搜索。 |

Claude Code、Codex、Factory Droid、Amp 的公开材料主要定义运行时，不定义一套研究算法，所以没有塞进上表。它们对「何时另开一个上下文」的说法见第 2、3 节。

## 2. Harness 在公开讨论里具体指什么

四层可以分开看，但公开文本并没有一份共同标准。有的作者把 skill 和工具算进 harness，有的把 skill 写成 harness 加载的数据。

**模型。** 厂商原文里，模型是会推理、会选下一步的那一部分。Anthropic 在 2025-06-13 的研究系统文里把单个 agent 定义成在循环中自主使用工具的 LLM，多 agent 就是多个这样的循环一起工作（[原文](https://www.anthropic.com/engineering/multi-agent-research-system)）。Amp 的 Thorsten Ball 在 2025-04-15 写：agent 是一个 LLM，加上能改上下文窗口之外状态的工具；他自己的最小实现是一个循环加足够的 token（[How to Build an Agent](https://ampcode.com/notes/how-to-build-an-agent)）。这篇文章没有使用 harness 这个词。xAI 在 2025-02-19 把 DeepSearch 描述成带代码解释器和互联网的模型侧 agent，同样没有拆 harness（[Grok 3](https://x.ai/news/grok-3)）。

**Skill。** 厂商原文是 Anthropic 工程博客，2025-10-16：skill 是带 `SKILL.md` 的目录，启动时只把 `name` 和 `description` 放进系统提示，判断相关后再读正文，更细的文件按需读；可执行脚本可以不把脚本或 PDF 读进上下文（[Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)）。同页更新写明 2025-12-18 把 Agent Skills 发布成开放标准。规范站 [agentskills.io/specification](https://agentskills.io/specification) 把渐进披露写成三档：元数据大约 100 tokens，启动时加载；`SKILL.md` 正文建议低于 5,000 tokens，并建议主文件少于 500 行；`scripts/`、`references/`、`assets/` 用到才读。必填字段只有 `name`（最多 64 字符，小写、数字、连字符，且必须等于目录名）和 `description`（最多 1,024 字符，要同时写做什么和何时用）。`allowed-tools` 标成实验字段。规范不管循环、沙箱、并发和重试。

Claude Code 文档把这层接进自己的运行时，并声明多出来的字段不是开放标准。[Extend Claude with skills](https://code.claude.com/docs/en/skills) 写：开放标准字段是 `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools`；`context: fork`、`agent`、`disable-model-invocation` 等是 Claude Code 扩展。`context: fork` 会另开一个 subagent，只把 skill 正文当任务，不继承当前对话；文档特别说，这和「fork 当前对话」不是一回事。没有具体任务、只有风格约定的 skill 不该这样跑，否则 subagent 没有可执行目标。skill 一旦加载，正文会跨回合留在上下文里。列表里的 `description` 加 `when_to_use` 在 1,536 字符处截断。

Factory 的厂商文档把边界写得更硬。[Custom droids](https://docs.factory.ai/harness/subagents)：「A custom droid is a runtime tool boundary and a separate agent. A skill is a discoverable instruction set.」要新上下文、换模型或强制工具策略时用 droid；要在当前会话里跑一个轻量流程时用 skill。Droid 的 subagent 不能再派 subagent（没有 Task 工具）。[Droid CLI 概览的检索摘录](https://docs.factory.ai/droid-cli/overview)把 MCP、hooks、plugins、skills、custom droids 都说成扩展 harness 的方式。TypeScript SDK 检索摘录写：SDK 跑的是驱动 CLI、桌面和网页的同一个 agent harness，负责上下文、工具执行、权限、流式、选模型和多步执行（[SDK 页](https://docs.factory.ai/sdk/typescript)）。这两句来自检索到的文档 Markdown，不是二手博客。

**Harness。** 这个词在 2026 年被几份文本收紧，但所指不完全一样。

Mitchell Hashimoto 在 2026-02-05 的个人博客里说，他还不知道有没有被行业接受的术语，他暂且把下面这件事叫 harness engineering：agent 每犯一次错，就花时间做一次工程，让它不能再犯。形式是改 `AGENTS.md`，或做真正可执行的校验工具。这是个人原文，不是哪家模型厂商的产品定义（[My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey)）。

六天后，OpenAI 的 Ryan Lopopolo 在 2026-02-11 用同一词描述另一件事：人不再手写代码，而是设计环境、写清意图、做反馈回路，让 Codex agent 可靠地干活。文中实验从 2025 年 8 月下旬的空仓库开始，大约五个月后仓库量级为一百万行；大约 1,500 个 PR 由最初三名工程师驱动，平均每名工程师每天 3.5 个 PR，后来团队到七人，吞吐还在升。他们把大约 100 行的 `AGENTS.md` 当目录，而不是百科；知识放在版本化的 `docs/`。单次 Codex 运行经常超过六小时。文中的「harness」更多是仓库里的约束、可观察性和反馈，不是搜索编排（[Harness engineering](https://openai.com/index/harness-engineering/)）。

更早的 2026-02-04，Celia Chen 把 Codex harness 定义成所有 Codex 表面底下的 agent loop 和逻辑。核心循环之外还有：线程的创建、恢复、分叉和持久化；配置和登录；在沙箱里执行 shell/文件，并把 MCP 和 skills 接到同一套策略上。App Server 用 JSON-RPC 把这个运行时暴露给 CLI、IDE 和桌面。这里 skill 是 harness 接进来的扩展，不是 harness 本身（[Unlocking the Codex harness](https://openai.com/index/unlocking-the-codex-harness/)）。

LangChain 的 Vivek Trivedy 在 2026-03-10 给出社区/厂商博客里最宽的一句：Agent = Model + Harness；「If you're not the model, you're the harness.」他列入 harness 的东西包括系统提示、工具、skills、MCP 及其描述、文件系统/沙箱/浏览器、子 agent 编排，以及压缩、续跑、lint 这类确定性钩子。同文把 skill 的渐进披露说成对抗 context rot 的 harness 机制。这是解释，不是 Anthropic 或 OpenAI 的原文；它把 skill 划进 harness（[The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)）。

论文侧，Paul Barbaste、Tristan Darrigol、Germain Vu、Tom Wiltberger（Inclusive Brains 与 Wavestone AI Lab）的 *Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents* 在 PDF 首页把日期写成 July 2026，arXiv 标识是 [2609.00006](https://arxiv.org/pdf/2609.00006)。检索到的摘要把 agent 定义成 model 加 harness：用循环、工具、上下文管理、安全控制、编排和扩展面把 LLM 接到世界上的运行时；并说 harness engineering 在 2026 年初被命名成一门学科。摘要还写，在他们钉到 2026 年 7 月版本的 11 个编码系统源码里，SKILL.md 的采用是 9/11，MCP 是 8/11。这是那次源码对照的计数，不是市场普查。正文里的星数是大约值，这里不引用。

Factory 文档首页把 “harness customization” 列成平台能力（[docs.factory.ai](https://docs.factory.ai/)）。[Missions](https://docs.factory.ai/docs/missions/overview) 没有定义这个词，但把「并行是否真的比串行更好」写成仍在测试的开放问题，并给了一个规划启发式：大约 1–500 个 feature 适合一个 Mission，超过 500 就拆开。这是功能粒度，不是搜索并发。

**工具。** 工具是循环里被点名执行的动作。Amp 文把工具定义和执行函数放在循环外面，模型只是发出调用。Anthropic 研究文把工具描述的质量当成和提示同级的杠杆：工具必须用途互斥，并举例 MCP 描述差会把 agent 带偏。Gemini Deep Research 把 Google Search、读 URL、代码执行、MCP、File Search 都做成可开关的工具，而不是写死在提示里。Factory 的 droid 用 frontmatter 的 `tools` 真正限制工具；skill 只是记下打算用什么。Claude Code 的 `allowed-tools` 只在触发该 skill 的这一回合里预批准，下一条用户消息就清掉。

所以，若把四层硬拆开：模型选择和推理；skill 是可发现、按需加载的流程和来源策略；工具是搜索、读页、读本地文件、代码执行这些动作；harness 是循环、并发和嵌套上限、上下文隔离、沙箱、权限、重试、持久化和压缩。这个拆法对齐 Factory 文档和 Agent Skills 规范，不对齐 LangChain 2026-03-10 那篇把 skill 算进 harness 的定义，也不完全对齐 OpenAI 把「把 skill 接进循环」算作 harness 职责的写法。Anthropic 的研究系统文和 Amp 的 2025-04 笔记则还没有使用这个词。

## 3. 并行搜索的机制清单

只列打开过或检索摘录里写明的机制。

**Query decomposition。** Anthropic 的 lead 把问题拆成带目标、输出格式、工具/来源和边界的子任务；边界写不清时，subagent 会做同一件事或做错年份（[2025-06-13](https://www.anthropic.com/engineering/multi-agent-research-system)）。他们要求先短而宽地搜，再收窄。STORM 认为直接让模型提问不够，所以先从相近文章抽出视角，再在模拟对话里追问（[论文摘要](https://arxiv.org/abs/2402.14207)；[仓库说明](https://github.com/stanford-oval/storm)）。LangChain 先把对话压成一份研究简报，supervisor 再决定哪些子题彼此独立（[2025-07-16](https://www.langchain.com/blog/open-deep-research)）。GPT Researcher 的 planner 生成一组问题，再交给 crawler（[README](https://github.com/assafelovic/gpt-researcher/blob/main/README.md)）。CoRAG（Chain-of-Retrieval Augmented Generation，Liang Wang、Haonan Chen、Nan Yang、Xiaolong Huang、Zhicheng Dou、Furu Wei；提交 2025-01-24，修订 2025-10-10）是单模型按状态改写查询，不是多 agent 拆题（[arXiv:2501.14342](https://arxiv.org/abs/2501.14342)）。另有一篇同名缩写的 *CoRAG: Collaborative Retrieval-Augmented Generation*（arXiv:2504.01883），不是这篇。

**Fan-out。** Anthropic 写明 lead 并行 3–5 个 subagent，subagent 再并行 3 个以上工具，复杂查询耗时最多降 90%（同上，内部系统，不是公开榜）。Manus 帮助中心写同时 20 个 subtask，每项最多 50 积分（[2026-03-17 页](https://help.manus.im/en/articles/11960169-what-is-wide-research)）。Open Deep Research 打开时的配置默认 5 个并发研究单元，滑块允许 1–20，并警告 rate limit（[configuration.py](https://github.com/langchain-ai/open_deep_research/blob/main/src/open_deep_research/configuration.py)）。Claude Code 文档写，自 v2.1.217 起，一个会话里已有 20 个 subagent 在跑时，再用 Agent 工具去派会失败，错误让模型不要重试；`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` 可改；ultracode 豁免。嵌套默认最多到主会话之下三层；v2.1.172–v2.1.216 曾默认五层且不能改，v2.1.217–v2.1.218 默认一层，v2.1.219 起默认三层（[Create custom subagents](https://code.claude.com/docs/en/sub-agents)）。Factory 的 subagent 不能再往下派；并行靠父级在同一回合发出多个 Task，或 `run_in_background: true` 后用 `TaskOutput` 收（[Custom droids](https://docs.factory.ai/harness/subagents)）。Perplexity Computer 的检索摘录写「成千上万步检索并行」，没有写 worker 上限（[2026-06-11 帖](https://www.perplexity.ai/hub/blog/deep-research-now-in-computer)）。xAI 文档检索摘录说 `grok-4.20-multi-agent` 的 `reasoning.effort` 控制的是协作 agent 数量（4 或 16），不是搜索 query 的数量（[Reasoning](https://x.ai/docs/developers/model-capabilities/text/reasoning)）。Factory Missions 页则写他们仍在测试并行是否优于串行（[Missions](https://docs.factory.ai/docs/missions/overview)）。

**Map-reduce。** Anthropic 把搜索的本质写成压缩：subagent 用自己的上下文探索，再把重要 token 交回 lead。附录建议大产物写入外部存储，只把轻量引用交回协调者，避免多层转述。LangChain 把 reduce 拆成两截：每个 subagent 先写成带引用的子题答案，supervisor 不再看原始网页；最终报告在研究全部结束后一次性写。他们试过并行写章节，结果互相不衔接，所以写作不并行。Manus Wide Research 是 map 到相似项、再由主 agent 收成表或报告；博客强调 subagent 是全功能实例，不是专用 reducer。STORM 的 reduce 是大纲，不是自由合并：先收集，再大纲，再成文。

**Dedup。** 公开文本里真正写成代码步骤的是 Perplexity Computer 摘录：检索结果进模型前做 dedupe、join、filter。Anthropic 用任务边界减少重复劳动，而不是写一个去重算法。STORM 的润色阶段可以选择去掉重复内容（仓库的 `do_polish_article` 说明）。Open Deep Research 用一次压缩调用丢掉无关网页和失败工具结果，这是降噪，不等于 URL 级去重。没有看到哪家公开了跨网页与本地附件的统一去重键。

**Rerank。** 这些研究系统的公开文几乎都不写经典检索的 rerank。Anthropic 用 LLM-as-judge 评来源质量，标准包括是不是优先用了一次来源，而不是二次转述；早期人工测试发现 agent 偏向 SEO 内容农场，后来把来源质量启发式写进提示。Gemini 博客说他们训练 agent 对照 SEC 文件和开放获取的同行评审期刊等来源，权衡互相冲突的证据，但没有写排序模型。Search-R1 和 DeepResearcher 优化的是「何时再搜」的轨迹，不是对一个固定候选集做 rerank。

**Citation compression。** Anthropic 把引用从研究循环里拆出，交给 CitationAgent。LangChain 要求 subagent 在返回前写一份详细、带有用来源的子题答案，否则原始页面会把 supervisor 撑爆。Gemini 把 citations 放在最终响应里，并告诉调用方用它们核对。OpenAI 写明可以引用来源中的具体句子或段落，也能引用用户上传文件。GPT Researcher 的步骤是对每个抓取结果做摘要并记下来源，再过滤汇总。这些都是「先压缩再引用」或「引用时再定位」，不是同一种算法。

**Budget。** Anthropic：简单/比较/复杂三档工具次数和 subagent 数；并报告多 agent 大约 15 倍于聊天的 token，所以只适合任务价值盖得过这笔开销的场合。Open Deep Research 用并发、supervisor 迭代和单 researcher 工具次数三道闸，外加网页字符上限。Claude Code 用 subagent 的 `maxTurns`（到顶后结果标成部分完成，可以续）、描述合计超过 15,000 tokens 就在启动时警告，以及默认 20 路并发。Manus 用每项 50 积分和同时 20 项；上下文工程帖把 KV-cache 命中率当成生产成本的主指标，并给出当时 Claude Sonnet 缓存与非缓存的 10 倍价差。OpenAI Deep Research 公开的是分钟数（5–30）和每月查询次数，不是 token 闸。Perplexity 2025 年帖和帮助中心给的是 2–4 分钟或大约 3–5 分钟，没有 token 预算。

**Judge / verifier。** Anthropic 的内部评测用一个 LLM 调用打 0.0–1.0 分并给出过/不过，维度是事实是否对得上来源、引用是否对得上断言、是否覆盖所问、来源质量、工具是否用得合理。他们说多评委并不比这一次调用更稳，且只在答案明确时最好用。人也要测，因为自动评测漏掉了来源偏见。Open Deep Research 的对外分数依赖 Deep Research Bench 的 Gemini judge。DeepResearcher（Yuxiang Zheng、Dayuan Fu、Xiangkun Hu、Xiaojie Cai、Lyumanshan Ye、Pengrui Lu、Pengfei Liu；提交 2025-04-04，v4 为 2025-04-17）写，端到端 RL 之后出现了制定计划、多源交叉验证、反思并改方向、找不到就不编的行为；相对 prompt engineering 基线最高多 28.9 分，相对 RAG 环境里的 RL agent 最高多 7.2 分（[arXiv:2504.03160](https://arxiv.org/abs/2504.03160)）。摘要没有在这句旁边写明这 28.9 / 7.2 是哪一个数据集上的绝对准确率差，所以这里只保留「up to」和对照类型。Search-R1（Bowen Jin 等；提交 2025-03-12，v5 为 2025-08-05）用结果奖励，而不是过程奖励；在七个问答数据集、同一设置下，相对多种 RAG 基线，Qwen2.5-7B 提高 41%，Qwen2.5-3B 提高 20%（[arXiv:2503.09516](https://arxiv.org/abs/2503.09516)）。训练稳定性来自遮住检索到的 token，不让那些 token 直接进策略梯度。这是单轨迹里的多轮搜索，不是并行 subagent。

**Source diversity。** STORM 用多视角提问对抗单一大纲。Anthropic 要求先宽后窄，并在发现 SEO 偏见后加入来源质量启发式。Gemini 博客把「查阅多样来源并对照冲突证据」写成相对 2025-12 预览的训练目标。Co-STORM 的主持人被规定去问「检索到了但还没进入对话」的信息。GPT Researcher 的使命陈述是用多站点降低单一来源偏差，并承认不能消除偏差。没有一份公开文档给出「至少 N 个独立域」这种可执行的多样性约束；Anthropic 的来源质量是提示启发式，Gemini 的多样性是模型行为描述。

**失败与重试。** Anthropic：工具失败要告诉模型，让它改策略；同时用确定性重试和检查点，因为不能每次从头跑。部署用 rainbow deployment，避免改代码打断已经跑到一半的 agent。Manus 要求把错误动作和报错留在上下文里，并警告不要在迭代中途增删工具定义，否则 KV-cache 失效，旧动作还会引用已经不存在的工具；他们改为在解码时遮住不允许的工具 token。Open Deep Research 对结构化输出最多重试 3 次。Gemini 的客户端要处理 `failed` 和流断开后的续传。Factory Missions 写长计划会累积错误，正确性策略仍是开放问题。

**本地语料和网页混在一起。** 这不是上表里的第十分支，但是公开设计和「群文件 + 网页」最接近的部分。

- GPT Researcher 把 `report_source` 分成网页和 `local`。本地目录由 `DOC_PATH` 指定，格式包括 PDF、纯文本、CSV、Excel、Markdown、PowerPoint、Word。网页加专用数据源时把 retriever 设成 `tavily,mcp`。两条通道的结果如何合并，README 没有写。
- STORM 仓库在 2024-07 的更新里加入 `VectorRM`，用来在用户提供的文档上做 grounding，和 You.com、Bing 等搜索引擎并列。检索器是运行时配置，视角和对话流程不变。
- Gemini Deep Research 默认同时有 Google Search、URL Context 和代码执行。File Search 指向已上传的 `file_search_store_names`；文档也可以作为多模态 input 直接传入。文档示例是「拿 2025 财年报告对照当前公开网页」。安全节写明：agent 会读你给的文件，恶意 PDF 可以藏指令；网页也不可信，要用返回的 citations 核对。可以把工具列表收成只有 File Search，从而不搜网页。
- OpenAI Deep Research 从 2025-02-02 起可以附上文件或表格；当时写「目前能访问公开网页和上传文件」，更专门的内部源留到以后。2026-02-10 的更新把这件事落到 MCP，以及把网页搜索限制在受信任站点。
- Claude 的项目帮助中心写：项目知识接近上下文窗口时自动改用 RAG，容量大约到原来的 10 倍；模型通过 project knowledge search tool 抽取，而不是把全部项目文件放进上下文。RAG 与网页搜索、extended thinking、Research 可以一起用。付费计划（Pro、Max、Team、Enterprise）。页面没有写激活阈值的 token 数，也没有写项目文件和网页结果冲突时听谁的（[RAG for projects](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)）。
- Anthropic 研究功能的工程文写，Research 可以搜网页、Google Workspace 和集成。工具选择启发式包括：只存在于 Slack 的内容不要去网页搜。这是来源边界写在提示里，不是索引层的 ACL。
- DeepResearcher 的摘要把「固定语料 RAG」和「真实网页」对立起来：前者假设需要的信息都在库里。Search-R1 仍是在检索增强的问答设置里训练。两者都没有描述附件如何成为证据。

没有看到一份公开规格同时规定：群文件的权限边界、附件是否算一次来源、以及网页结果与本地块冲突时的优先级。各家只是把「用户文件」和「网页」做成可开关的不同工具。

## 4. 对「一个 skill + 一个 harness」的设计含义

下面是根据上一节做的分工判断，不是新的实验结果，也不是这个仓库的实现规格。

1. **Skill 写流程和判定，harness 写不可违背的上限。** Agent Skills 规范只约束目录、frontmatter 和按需加载（[规范](https://agentskills.io/specification)）。Claude Code 和 Factory 都把「另开上下文、限制工具、换模型」放在 subagent/droid，而不是 skill 正文（[Claude skills](https://code.claude.com/docs/en/skills)，[Factory droids](https://docs.factory.ai/harness/subagents)）。因此一份并行搜索 skill 适合写：什么问题要拆、子任务说明必须包含哪些字段、先宽后窄、什么叫做来源不够、引用长什么样。并发 5 还是 20、失败是否重试、网页正文截到多少字符，公开系统是写在运行时配置里的（Anthropic 的提示启发式是例外，他们自己也说早期会派 50 个 subagent）。把上限只写在 prose 里，不能声称有强制力。

2. **「Skill 调用子 agent」有公开的触发条件，没有公开的研究专用阈值。** Claude Code：副作用是大段搜索结果、日志或文件，而且主会话不会再逐字引用时，用 subagent；要复用的流程留在主会话时用 skill。`context: fork` 只适合自洽的任务说明。Factory：要隔离上下文、换模型或强制工具策略时用 droid，否则用 skill，而且 droid 不能再派 droid。Anthropic 研究系统把「派 subagent」放在 lead 的提示里，并用 3–5 / 工具次数做启发式，那是他们的 Research 提示，不是 SKILL.md 标准。能说的是：搜索 skill 应该在说明里写出何时委托；真正的并发和嵌套深度要由 harness 拒绝超额调用。不能说存在一个被各家采纳的「超过 N 条来源就开子 agent」的标准。

3. **并行的单位是独立子问题或独立条目，不是报告章节。** Anthropic 和 LangChain 都把收益记在「子题各有一个上下文」上；LangChain 明确把并行写作撤掉了。Manus Wide Research 并行的是相似条目。Factory 仍把「并行是否更好」当成开放问题。所以「一个 skill + 一个 harness」可以规定：只有子任务互不依赖时才 fan-out；汇总和写最终答案留在单上下文。不能声称并行本身提高事实准确率。Anthropic 在 BrowseComp 上把大部分方差解释为 token 用量，而不是并行这个形式。

4. **子 agent 的返回值应该是压缩后的证据，不是页面。** 这一点 Anthropic（压缩是搜索的本质；大产物外置）、LangChain（子题答案而不是原始工具结果）、Manus（文件系统留 URL/路径，上下文可删正文）和 Perplexity Computer 摘录（进模型前 dedupe/join/filter）是一致的。Skill 可以规定返回字段：主张、来源 URL 或本地路径、摘录、缺口。去重和截断如果要可重复，就属于 harness，而不是再让模型做一次。各家没有公开同一种去重算法，不能把某一种说成行业做法。

5. **引用和「研究已经做完」最好分开。** Anthropic 用独立的 CitationAgent，并在评测里把事实准确和引用准确分成两项。OpenAI 要求引用到句子，同时承认仍会幻觉。Gemini 让调用方自己核对 citations。因此 skill 可以要求每条主张带可回溯位置；harness 可以在循环外再跑一次对齐，或者在没有可回溯位置时拒绝写入最终报告。不能说这样做就达到了 Anthropic 内部评测的 90.2%，那个数字绑着他们的模型、评测集和 2025-06 的系统。

6. **本地文件和网页是两种工具，skill 要写来源边界，harness 要保留来源类型。** GPT Researcher、STORM 的 VectorRM、Gemini 的 File Search 与 Google Search 开关、OpenAI 的上传文件和 2026-02 的可信站点限制、Claude 项目 RAG，都是「私有材料」和「公开网页」分开进入。Claude 的项目 RAG 在快满窗口时才从全量上下文切到检索，容量大约 10 倍，但是没有公开冲突规则。设计含义是：附件和群文件应以路径或库 id 进入证据，并带上通道标签；skill 写「只在网页找不到时再查本地」或反过来的策略。不能声称已有系统证明了某种优先级更准确。DeepResearcher 的论点只是：只在固定库上训练，学不会开放网页。

7. **预算要同时有软判断和硬停止。** 软判断是 Anthropic/LangChain/Perplexity 描述的「证据够不够」。硬停止是 Open Deep Research 的迭代和工具次数、Claude Code 的 `maxTurns` 和 20 路并发、Manus 的积分帽、Gemini 的异步任务状态。Skill 里写软判断；harness 在超额时返回部分结果而不是再开一轮。Anthropic 的 15 倍 token 是他们的用量观察，只能用来提醒多 agent 很贵，不能当成预算公式。

8. **失败要可见，重试要有界。** Manus 把错误留在上下文里；Anthropic 把工具失败告诉模型，并用检查点避免整段重来。两边都不是无限重试。Harness 适合做次数上限和断点续跑（Gemini 的流续传是同一类问题）。Skill 不适合假装搜索从不失败。

9. **已有系统做到的，和它们没做的。** 做到的是：问题分解、有限 fan-out、用隔离上下文做 map、返回前压缩、单独或事后引用、用配置表达预算、用 LLM judge 评开放式报告、把用户文件和网页分成不同工具。没做、因此不能声称的是：一个跨厂商的「并行搜索 skill」标准；把 skill 和 harness 划成互斥四层的唯一官方定义；本地群文件与网页的统一证据等级；可移植的最佳并发数；Search-R1 / DeepResearcher / CoRAG 那种训练方法可以被 SKILL.md 替代。那三篇是在改模型的搜索策略，不是在写运行时说明书。Amp 的 2025-04 笔记和 Anthropic 的 2025-06 研究文甚至还没有采用 harness 这个词。

## 5. 来源列表

### 厂商文档

- Anthropic，Jeremy Hadfield、Barry Zhang、Kenneth Lien、Florian Scholz、Jeremy Fox、Daniel Ford. *How we built our multi-agent research system*. 2025-06-13. https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic，Barry Zhang、Keith Lazuka、Mahesh Murag. *Equipping agents for the real world with Agent Skills*. 2025-10-16；页内更新写开放标准发布于 2025-12-18. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Agent Skills 规范（开放标准站）. https://agentskills.io/specification
- Claude Code. *Extend Claude with skills*. https://code.claude.com/docs/en/skills
- Claude Code. *Create custom subagents*. https://code.claude.com/docs/en/sub-agents
- Claude Help Center. *Retrieval augmented generation (RAG) for projects*. https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects
- OpenAI. *Introducing deep research*. 2025-02-02，页内更新至 2026-02-10. https://openai.com/index/introducing-deep-research/
- OpenAI，Celia Chen. *Unlocking the Codex harness: how we built the App Server*. 2026-02-04. https://openai.com/index/unlocking-the-codex-harness/
- OpenAI，Ryan Lopopolo. *Harness engineering: leveraging Codex in an agent-first world*. 2026-02-11. https://openai.com/index/harness-engineering/
- Google. *Gemini Deep Research agent*（Gemini API 文档，打开时为 preview）. https://ai.google.dev/gemini-api/docs/deep-research
- Google，Lukas Haas、Srinivas Tadepalli. *Deep Research Max: a step change for autonomous research agents*. 2026-04-21. https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/
- xAI. *Grok 3 Beta — The Age of Reasoning Agents*. 2025-02-19. https://x.ai/news/grok-3
- xAI 文档. *Reasoning*（检索摘录中的 `grok-4.20-multi-agent` 与 effort）. https://x.ai/docs/developers/model-capabilities/text/reasoning
- Manus. *Introducing Wide Research*. 栏目标 Thursday, July 31，配图目录为 2025/07/31. https://manus.im/blog/introducing-wide-research
- Manus Help Center. *What is Wide Research?* 页上日期 March 17, 2026. https://help.manus.im/en/articles/11960169-what-is-wide-research
- Manus，Yichao “Peak” Ji. *Context Engineering for AI Agents: Lessons from Building Manus*. 文内日期 2025/7/18. https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- Amp，Thorsten Ball. *How to Build an Agent*. 2025-04-15. https://ampcode.com/notes/how-to-build-an-agent
- Factory. 文档首页. https://docs.factory.ai/
- Factory. *Factory Missions*. https://docs.factory.ai/docs/missions/overview
- Factory. *Custom droids (subagents)*. https://docs.factory.ai/harness/subagents
- Factory. *Droid CLI* 与 *Droid TypeScript SDK*（检索到的文档摘录，未逐页打开全文）. https://docs.factory.ai/droid-cli/overview ；https://docs.factory.ai/sdk/typescript
- Perplexity（仅检索摘录，完整页被 Cloudflare 拦住）. https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research ；https://www.perplexity.ai/help-center/en/articles/10738684-what-is-research-mode ；https://www.perplexity.ai/hub/blog/deep-research-now-in-computer ；https://research.perplexity.ai/articles/evaluating-deep-research-performance-in-the-wild-with-the-draco-benchmark

### 论文

- Yijia Shao, Yucheng Jiang, Theodore A. Kanell, Peter Xu, Omar Khattab, Monica S. Lam. *Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models*（STORM）. 提交 2024-02-22，修订 2024-04-08. NAACL 2024. https://arxiv.org/abs/2402.14207
- Yucheng Jiang, Yijia Shao, Dekun Ma, Sina Semnani, Monica Lam. *Into the Unknown Unknowns: Engaged Human Learning through Participation in Language Model Agent Conversations*（Co-STORM）. EMNLP 2024. 题名和出处来自 STORM 仓库 README 的 BibTeX，本文没有打开论文 PDF，因此没有引用它的实验数字. https://arxiv.org/abs/2408.15232
- Liang Wang, Haonan Chen, Nan Yang, Xiaolong Huang, Zhicheng Dou, Furu Wei. *Chain-of-Retrieval Augmented Generation*（CoRAG）. 提交 2025-01-24，修订 2025-10-10. https://arxiv.org/abs/2501.14342
- Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon, Sercan Arik, Dong Wang, Hamed Zamani, Jiawei Han. *Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning*. 提交 2025-03-12，v5 为 2025-08-05. https://arxiv.org/abs/2503.09516
- Yuxiang Zheng, Dayuan Fu, Xiangkun Hu, Xiaojie Cai, Lyumanshan Ye, Pengrui Lu, Pengfei Liu. *DeepResearcher: Scaling Deep Research via Reinforcement Learning in Real-world Environments*. 提交 2025-04-04，v4 为 2025-04-17. https://arxiv.org/abs/2504.03160
- Paul Barbaste, Tristan Darrigol, Germain Vu, Tom Wiltberger. *Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents*. PDF 内署 July 2026；arXiv:2609.00006. 本文依据检索到的 PDF 摘要摘录，没有通读全文. https://arxiv.org/pdf/2609.00006

### 开源仓库

- https://github.com/stanford-oval/storm （打开了 README；2025-01 的 litellm、2024-09 的 Co-STORM、2024-07 的 VectorRM 都写在该 README）
- https://github.com/assafelovic/gpt-researcher （打开了 `main` README）
- https://github.com/langchain-ai/open_deep_research （打开了 README 和 `src/open_deep_research/configuration.py`）
- https://github.com/agentskills/agentskills （规范页指向的参考实现；本文引用的是规范站，不是仓库星数）

### 社区文章

- Mitchell Hashimoto. *My AI Adoption Journey*. 2026-02-05. https://mitchellh.com/writing/my-ai-adoption-journey （个人博客；文中写明他自己还不确定术语是否已被行业接受）
- Vivek Trivedy, LangChain. *The Anatomy of an Agent Harness*. 2026-03-10. https://www.langchain.com/blog/the-anatomy-of-an-agent-harness （厂商博客，但是「Agent = Model + Harness」这句的来源；不是模型实验室的产品定义）
- LangChain 团队. *Open Deep Research*. 2025-07-16. https://www.langchain.com/blog/open-deep-research

未当作事实来源：比较站和安全公司对 harness 的综述、Deep Research 横评里的「典型来源数 50–200」一类区间、Manus 文档营销页上未注明研究出处的「8–10 项就开始编造」。这些页面出现在检索结果里，但没有被用来支持结论。

---

使用的搜索通道：本机 Perplexity Pro 网页会话 `pplx-web`，模型 `kimik3thinking`。六次查询都返回了答案和 Citations。Citations 只当作线索，结论改以随后打开的原文为准。Perplexity 官网正文抓取失败后，改用环境里的网页检索摘录，没有中断。

查询列表：

1. `What is an agent harness in 2025-2026? How do Anthropic, OpenAI Codex, Claude Code, Amp, Factory, and Manus publicly define the split between model, skill, tool, and harness? Cite primary sources.`
2. `Anthropic multi-agent research system 2025 blog: orchestrator, subagents, parallel search, citation, token budget, how it works. Also OpenAI Deep Research architecture and stopping criteria. Primary URLs only.`
3. `STORM Stanford report generation, GPT Researcher architecture, LangChain LangGraph open deep research, query decomposition, parallel retrieval, citation. Official repos and papers.`
4. `Search-R1 DeepResearcher CoRAG agentic retrieval reinforcement learning papers 2024 2025 2026 arxiv titles authors mechanisms`（`--focus scholar`）
5. `Agent Skills open standard SKILL.md agentskills.io Claude skills when to spawn subagents parallel limits context budget official docs Anthropic Claude Code skills. Also Manus wide research, Google Gemini Deep Research, Perplexity deep research, xAI Grok deep research public descriptions.`
6. `Hybrid local corpus and web search for research agents: local index vs live search, attachments as evidence, source boundaries, dedup rerank citation compression. Public designs from LlamaIndex, LangChain, Anthropic, OpenAI file search, Perplexity spaces or collections.`

失败与降级：第 4 条第一次因输出目录尚未创建而没有写入文件，同一查询立刻重试成功，不是鉴权或连接失败。`web_fetch` 打不开 `https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research`、`https://www.perplexity.ai/hub/blog/deep-research-now-in-computer` 和 Research mode 帮助中心，返回 Cloudflare 的 “Just a moment...”。Amp 笔记和 Anthropic Skills 博客、两篇 OpenAI harness 文章的第一次抓取为空或失败，改用另一种打开方式后拿到正文。没有遇到 `AUTHENTICATION`、`CONNECT`、`HTTP` 或 `NO_BROWSER`。
