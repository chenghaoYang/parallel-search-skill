# Brief（R0）

## 任务
产出一份中文文档，帮读者理清「agent 时代」各种互操作「协议」分别管什么、彼此有什么不同。

## 读者
想做技术选型或只是想搞清楚现状的工程师/技术决策者。有工程背景，但不一定读过任何一份协议 spec。

## 成稿目标
5 分钟内建立：这些协议各自连接什么两端、谁治理、鉴权/传输怎么做、四大厂各自支持什么、遇到时该怎么选。之后能按需查表格细节。

## 范围内
- MCP（Model Context Protocol，Anthropic 起源）
- A2A（Agent2Agent，Google 起源）
- ACP ×2：IBM/BeeAI 的 Agent Communication Protocol；Zed 的 Agent Client Protocol
- AG-UI（Agent-User Interaction Protocol）
- 大厂支持面：OpenAI、Anthropic、Google、Microsoft 对上述协议的官方支持情况 + 是否有自家变体/专有协议
- 鉴权机制、版本/spec 演进、治理归属（谁拥有/谁维护/是否已捐赠给基金会）、选型建议
- scout 授权发现范围内其他相关协议（如 ANP、AGNTCY 等），按重要性决定收入正文还是只留「未决」一笔

## 范围外
- 框架/SDK 本身的用法教程（LangChain、AutoGen、Semantic Kernel……）——除非直接是「协议支持」的证据
- 代码示例、定价、部署教程
- 与 agent 协议无关的通用安全议题

## 用户点名疑点（成稿必须给出明确结论，哪怕结论是「官方没写」）
1. IBM 的 Agent Communication Protocol 和 Zed 的 Agent Client Protocol 是不是一回事？
2. MCP 的 SSE 传输是否已经「废弃」？如果是，哪个版本、替代方案是什么？

## 完成标准
- 「0 一屏看懂」单独就能回答上面两个疑点 + 5 个协议各连什么 + 四大厂站队
- 正文每个具体事实可追溯到 notes/ 里的一条 [C#]
- 成稿 ≤ 9000 字符（含来源节），每轮收束都检查
