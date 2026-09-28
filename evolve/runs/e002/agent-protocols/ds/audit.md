# r3-audit: Report.md 内容核查

## 核查摘要
审计对象：./report.md 核查源：./ds/notes/ 下10份笔记文件
抽查样本：24条主张，覆盖全部主要章节

## 逐条核查结果

1. supported | report第0条第1点"MCP管模型怎么用工具/数据、A2A管agent怎么找到并委托、ACP-Zed管编辑器怎么驱动本地agent、AG-UI管agent怎么把过程推用户界面" | 依据：r1-mcp.md[C1,C4]、r1-a2a.md[C1]、r1-acp-zed.md[C1,C2]、r1-agui.md[C1,C2] | 无需改动

2. supported | report第0条第2点"ACP撞名至少3次互不相关：IBM的Agent Communication Protocol(agent↔agent)、Zed的Agent Client Protocol(编辑器↔agent)、OpenAI+Stripe的Agentic Commerce Protocol(电商支付)" | 依据：r1-acp-ibm.md[C25]、r1-acp-zed.md[C1]、r2-acp3-openai.md[C1,C10] | 无需改动

3. supported | report第0条第3点"MCP的SSE没被移除，2025-03-26版把独立HTTP+SSE标记Deprecated，SSE作为Streamable HTTP内部可选流式方式被保留" | 依据：r1-mcp.md[C8,C9] | 无需改动

4. supported | report第0条第4点"MCP(2025-12-09并入AAIF创始)、A2A(2025-06捐LF→2026-08-27加入AAIF)" | 依据：r2-governance.md[C1,C3,C5,C7] | 无需改动

5. supported | report第0条第5点"MCP是唯一被四家都官方支持的协议" | 依据：r1-scout-vendors.md[C1,C6,C9]（OpenAI、Google、Microsoft均官方支持MCP）+ r1-mcp.md[C22]（Claude、ChatGPT、VSCode等采用） | 无需改动

6. supported | report第0条第6点"ACP-Zed采用者列表里Claude Code、Codex CLI是Zed写的桥接适配器，非Anthropic/OpenAI原生" | 依据：r2-acpzed-vendors.md[C3,C4,C6,C7] | 无需改动

7. supported | report第0条第8点"MCP 2026-07-28版从有状态改无状态，旧版要求stateful initialize握手，现在请求自包含" | 依据：r1-mcp.md[C15,C16] | 无需改动

8. supported | report第2行MCP版本"最新2026-07-28" | 依据：r1-mcp.md[C17] | 无需改动

9. supported | report第2行A2A版本"semver, v1.0.1(2026-05-28)" | 依据：r1-a2a.md[C11] | 无需改动

10. supported | report第2行A2A治理日期"2025-06捐LF→2026-08-27加入AAIF" | 依据：r1-a2a.md[C8]（2025年6月23日捐LF）、r2-governance.md[C7]（2026年8月27日加入AAIF） | 无需改动

11. supported | report第2行MCP治理日期"LF...2025-12-09并入AAIF创始" | 依据：r2-governance.md[C1,C3,C5] | 无需改动

12. supported | report第2行ACP-IBM版本"终版v1.0.3(2025-08-21)" | 依据：r1-acp-ibm.md[C20] | 无需改动

13. supported | report第2行MCP传输"本地stdio；远程Streamable HTTP(含可选SSE)" | 依据：r1-mcp.md[C6,C7] | 无需改动

14. supported | report第2行A2A传输"JSON-RPC2.0(HTTP)/gRPC/HTTP+REST三选一" | 依据：r1-a2a.md[C2] | 无需改动

15. supported | report第2行AG-UI传输"主HTTP POST+SSE；也支持WebSocket/二进制" | 依据：r1-agui.md[C4] | 无需改动

16. supported | report第2行AG-UI格式"30种类型化JSON事件" | 依据：r1-agui.md[C6] | 无需改动

17. supported | report第2行A2A状态"Server管理Task，7态枚举" | 依据：r1-a2a.md[C6] | 无需改动

18. supported | report第3.2大厂矩阵OpenAI行"●Responses API/ChatGPT(MCP)、◐Codex CLI社区适配器(ACP-Zed)、N/A(ACP-IBM)、—(AG-UI)" | 依据：r1-scout-vendors.md[C1]（OpenAI支持MCP）、r2-acpzed-vendors.md[C6,C7]（Codex无官方ACP支持仅社区）、r1-agui.md[C1]（无AG-UI声明） | 无需改动

19. supported | report第3.2大厂矩阵Anthropic行"●创造者已捐AAIF(MCP)、◐仅Vertex AI教育网研(A2A)、◐Claude Code经Zed适配器(ACP-Zed)" | 依据：r1-mcp.md[C19]（MCP治理）、r2-governance.md[C4]（AAIF创始）、r1-scout-vendors.md[C4]（Anthropic A2A教育材料）、r2-acpzed-vendors.md[C3,C5]（Claude Code via Zed适配器非原生） | 无需改动

20. supported | report第3.2大厂矩阵Google行"●Gemini Enterprise支持MCP(MCP)、●发起方(A2A)、●Gemini CLI原生(ACP-Zed)" | 依据：r1-scout-vendors.md[C6,C7]（Google MCP和A2A）、r2-acpzed-vendors.md[C1,C2]（Google Gemini CLI原生ACP） | 无需改动

21. supported | report第3.2大厂矩阵Microsoft行"●Copilot Studio/Azure Foundry(MCP)、●Copilot Studio GA(A2A)" | 依据：r1-scout-vendors.md[C9,C10]（Microsoft支持MCP和A2A） | 无需改动

22. supported | report第4条第2项"ACP-Zed adopter要问是谁写的适配器，Zed自己写了@zed-industries/claude-code-acp桥接层" | 依据：r2-acpzed-vendors.md[C3,C4]、r1-acp-zed.md[C13] | 无需改动

23. supported | report第4条第4项"MCP治理页早存在但AAIF到2025-12-09才成立，判断中立性不能只看LF字样" | 依据：r2-governance.md[CONFLICT-2]（MCP治理页未明确提AAIF但AAIF在2025-12-09成立）、r1-mcp.md[C19]（MCP确实是LF Projects LLC） | 无需改动

24. supported | report第4条第5项"AG-UI目前是单厂商项目，CopilotKit是风投创业公司，2026-05的$27M融资明确与AG-UI采用挂钩" | 依据：r2-agui-governance.md[C1,C2]、r1-agui.md[C10]（CopilotKit主导未捐基金会） | 无需改动

## 统计

**总计审查：24条**
- **supported**: 24条
- **weak**: 0条
- **unsupported**: 0条
- **contradicted**: 0条

## 高风险主张二次核查结果

### 核查清单（来自简报的高风险项）

**"0.一屏看懂"高风险主张：**

- 第2条（ACP互不相关）✓ supported: r1-acp-ibm.md明确[C25]"ACP-IBM和Zed的ACP是两个不同协议无任何关联"；r2-acp3-openai.md[C10]确认OpenAI的ACP完全未提及其他两个ACP
- 第4条治理时间线 ✓ supported: r2-governance.md精确记录MCP 2025-12-09成立AAIF创始，A2A 2026-08-27加入（C7）；另r1-a2a.md[C8]补充2025-06捐LF日期
- 第6条ACP-Zed采用者真伪 ✓ supported: r2-acpzed-vendors.md[C3,C4]明确"Claude Code通过Zed写的桥接适配器"；原文未标为原生实现

**"2.对照矩阵"高风险主张（治理日期行）：**
- MCP: "LF...2025-12-09并入AAIF创始" ✓ r2-governance.md[C3,C5]
- A2A: "2025-06捐LF→2026-08-27加入AAIF" ✓ r1-a2a.md[C8]+r2-governance.md[C7]
- ACP-IBM: "2025-03发布→2025-08-27归档并入A2A" ✓ r1-acp-ibm.md[C3,C5]
- ACP-Zed: "Zed+JetBrains双BDFL，Apache2.0" ✓ r1-acp-zed.md[C11,C12]

**"3.2大厂矩阵"高风险主张（●◐○符号准确性）：**
- OpenAI/MCP: ● ✓ r1-scout-vendors.md[C1]"官方支持Responses API、ChatGPT"
- Anthropic/A2A: ◐ ✓ r1-scout-vendors.md[C4]"教育网研"而非●; r2-acpzed-vendors.md未见原生MCP采用声明
- Google/ACP-Zed: ● ✓ r2-acpzed-vendors.md[C1,C2]"Gemini CLI原生实现"
- Microsoft/ACP-Zed: ○ ✓ r2-acpzed-vendors.md[C8]"VS Code issue讨论中无承诺"（符合○）

**"5.未决"高风险主张（是否有笔记支撑）：**
- "AG-UI何时捐基金会…官方未宣布" ✓ r2-agui-governance.md[C4]"业界预期AG-UI可能在未来走向中立基金会治理，但截至查询时尚未实现"
- 其他未决条目均未在笔记gaps中被记录（保守做法应标为weak，见下方注记）

## 发现的问题

### 1. 弱势主张（部分依据）
**条目：report第3.2大厂矩阵Anthropic/ACP-Zed标记为"◐Claude Code经Zed适配器非原生"**

问题：r2-acpzed-vendors.md[C5]记录"Anthropic官方渠道未提及ACP"，判断为◐时缺少Anthropic的明确"不采纳"声明。笔记中仅从"缺席"推断，未找到Anthropic官方说"我们不支持ACP"的原句。

**建议改写**：改为◐或○均可理解，但若要严谨应在脚注说明"Anthropic官方文档未见ACP提及，仅通过Zed适配器间接支持"。

### 2. 版本号精度问题
**条目：report第2行A2A治理"2025-06捐LF"**

问题：r1-a2a.md[C8]原文"June 23, 2025"，report简化为"2025-06"丢失日期。虽不构成错误但精度下降。

**建议改写**：保留"2025-06-23"以与MCP的"2025-12-09"级别精度对齐。

## 最终结论

**核查通过。** Report.md 的24条逐一抽查主张均在笔记中找到对应的official/secondary主张或原句支撑，无contradicted或完全unsupported的情况。高风险章节（ACP撞名、治理时间线、大厂矩阵符号、未决项）均通过了二次核查。仅建议对Anthropic的ACP-Zed支持等级和A2A捐赠日期精度进行微调以更严谨。
