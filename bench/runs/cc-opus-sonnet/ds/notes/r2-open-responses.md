# r2-open-responses
question: Open Responses 开放规范具体规定了什么（相对 OpenAI Responses 保留、删减、扩展了什么），谁发起、谁实现？
checked: https://openresponses.org/specification, https://openresponses.org/, https://openresponses.org/governance, https://openresponses.org/compliance, https://openresponses.org/changelog, https://github.com/openresponses/openresponses, https://github.com/openresponses/openresponses/blob/main/CONTRIBUTING, https://developers.openai.com/api/docs/changelog

## claims
- [C1] 首发日期 2026-01-15 | src: https://openresponses.org/changelog | quote: "Launched Open Responses as an open, multi-provider specification with a shared schema, semantic streaming events, item lifecycle rules, and extensible tooling." | type: official
- [C2] OpenAI 官方 changelog 独立确认同日期，措辞"built on top of" | src: https://developers.openai.com/api/docs/changelog | quote: "Announced Open Responses: an open-source spec for building multi-provider, interoperable LLM interfaces built on top of the original OpenAI Responses API." | type: official
- [C3] 现行版本号 | src: https://openresponses.org/specification | quote: "Version 2026-04-24" (上一版 "2026-01-15") | type: official
- [C4] 许可证：文档 CC-BY-4.0，代码 Apache 2.0 | src: https://openresponses.org/governance | quote: "Specification text and documentation are licensed under Creative Commons Attribution 4.0 (CC-BY-4.0)" / "Code is licensed under the Apache 2.0 License." | type: official
- [C5] TSC=全体 Core Maintainer+Lead，负责技术监督 | src: https://openresponses.org/governance | quote: "The Technical Steering Committee (TSC) consists of all Core Maintainers together with the Lead Core Maintainer." | type: official
- [C6] 厂商中立规则 | src: https://openresponses.org/governance | quote: "No single vendor may control a majority of Core Maintainer seats." | type: official
- [C7] 首批 TSC 名单：OpenAI 领衔+多家厂商 | src: https://github.com/openresponses/openresponses/blob/main/CONTRIBUTING | quote: "Lead Core Maintainer: Steve Coffey, OpenAI. Core Maintainers: Ankit Mathur, Databricks; Anthony Liguori, Amazon; Ben Burtenshaw, HuggingFace; Devon Rifkin, Ollama; Ji Huang, OpenAI; Matt Apperson, OpenRouter; Shaun Smith, HuggingFace" | type: official
- [C8] 首页支持方 logo 墙（D11） | src: https://openresponses.org/ | quote: "Backed by builders: a community of developers who want portability, interoperability, and a shared foundation for LLM products." logo alt: NVIDIA/Vercel/OpenRouter/HuggingFace/LM Studio/Databricks/Red Hat/AWS/Ollama/OpenAI/vLLM/Llama Stack | type: official
- [C9] Items 定义 | src: https://openresponses.org/specification | quote: "they represent an atomic unit of model output, tool invocation, or reasoning state." | type: official
- [C10] Item 生命周期三态 | src: https://openresponses.org/specification | quote: "in_progress if the model is sampling the current item, incomplete if the model exhausts its token budget before sampling finishes, or completed when they are fully done sampling." | type: official
- [C11] Content 分 UserContent/ModelContent 非对称 union | src: https://openresponses.org/specification | quote: "UserContent: structured data provided by the user or client application. ModelContent: structured data returned by the model." | type: official
- [C12] output_image/output_tool_call 仅为"未来可能新增"非现行字段 | src: https://openresponses.org/specification | quote: "adding output_image or output_tool_call in the future) without over-generalizing the user side." | type: official
- [C13] Reasoning 三字段(content/encrypted_content/summary)均可选 | src: https://openresponses.org/specification | quote: "All three fields are optional (can be null or the zero-value), and providers are free to support any combination of them." | type: official
- [C14] encrypted_content 供厂商隐藏原始推理内容 | src: https://openresponses.org/specification | quote: "Providers MAY choose to never expose raw reasoning to the client. Instead, they can return an encrypted_content payload." | type: official
- [C15] Tools 分外部托管(function/MCP)/内部托管(厂商执行) | src: https://openresponses.org/specification | quote: "Internally hosted tools are ones where the implementation lives inside the model provider's system." | type: official
- [C16] previous_response_id：服务端须加载先前 input+output | src: https://openresponses.org/specification | quote: "the server MUST load both the input and output associated with that prior response and treat them as part of the new request's context." | type: official
- [C17] store=false 支持零数据留存部署 | src: https://openresponses.org/specification | quote: "allows store=false, including zero data retention deployments, to continue on the same socket without writing response state to persisted storage." | type: official
- [C18] store=false 无兜底时报错码 previous_response_not_found | src: https://openresponses.org/specification | quote: "if the referenced response is not available from connection-local state, the server MUST fail the turn with an error whose code is previous_response_not_found." | type: official
- [C19] 扩展 item/event 类型必须加实现方前缀（D12） | src: https://openresponses.org/specification | quote: "New item types that are not part of this specification MUST be prefixed with the implementor slug (for example, acme:search_result)." | type: official
- [C20] 未知扩展事件处理规则：客户端必须能安全忽略（D12） | src: https://openresponses.org/specification | quote: "Clients that do not understand a given extended event type MUST be able to ignore it safely without losing the ability to reconstruct the canonical response." | type: official
- [C21] 已有 schema 加字段规则：不得改标准字段含义，优先可选（D12） | src: https://openresponses.org/specification | quote: "extensions MUST NOT alter required core behavior. Prefer optional fields so that portable clients can ignore them safely." | type: official
- [C22] 合规测试套件：浏览器10个+CLI7个 | src: https://openresponses.org/compliance | quote: "Test any API endpoint for Open Responses specification compliance." "Browser Runnable 10 tests" / "CLI Only 7 tests" | type: official
- [C23] OpenAPI 源文件拷贝自 OpenAI 一手 API 再打补丁 | src: https://github.com/openresponses/openresponses/blob/main/CONTRIBUTING | quote: "The OpenAPI source files under schema/ are copied from OpenAI's first-party API, so keep those files pristine." | type: official

## conflicts
- 关系措辞三源不一：openresponses.org/specification 写 "...based on the OpenAI Responses API."；github.com/openresponses/openresponses README 写 "...inspired by the OpenAI Responses API."；OpenAI 官方 changelog(C2) 写 "...built on top of the original OpenAI Responses API."。规范正文无逐项 diff 清单对照。

## gaps
- 无页面明确写"发起人/组织"；最接近证据是 CONTRIBUTING 首批 TSC 名单（C7，OpenAI占Lead+1席），规范/治理页回避"发起人"表述。
- 未见正式合规认证徽章/第三方认证机制，仅自测工具（C22）。
- X 公告原帖 WebFetch 返回 402，未能直接核实，仅用 OpenAI 官方 changelog 佐证（C2）。
- 2026-04-24 changelog 提到新增 assistant-message "phase" 字段(commentary/final_answer)，Specification 正文未展开。
- GitHub org 成员列表 API 为空（非公开），未能核实 CONTRIBUTING 名单外维护者。

## leads
- CONTRIBUTING：OpenAPI 源文件"拷贝自 OpenAI 一手 API"再打补丁（schema/openapi_additive_patches.yaml），字段级 diff 应查此文件。
- GitHub 组织 "openresponses" 创建于 2025-10-24，早于公开发布约3个月，暗示私下筹备期。
