# r2-verify-ref
question: 核验4条参照协议冲突/高影响主张(OAI-Resp D8、D6、ANT-Msg D1、D9),只看一手来源,逐条给判定与原句。
checked: https://github.com/openai/openai-openapi/blob/master/openapi.yaml, https://github.com/openai/openai-python/blob/main/src/openai/_streaming.py, https://developers.openai.com/api/docs/guides/streaming-responses, https://developers.openai.com/api/docs/guides/reasoning, https://platform.claude.com/docs/en/api/overview, https://platform.claude.com/docs/en/api/messages, https://platform.claude.com/docs/en/about-claude/models/migration-guide

## claims
- [C1] [D8]R1判定:正确,证据可升级为schema级。`ResponseStreamEvent`(anyOf 60成员,按type判别)末位非DoneEvent,紧接discriminator | src: https://github.com/openai/openai-openapi/blob/master/openapi.yaml | quote: "- $ref: \"#/components/schemas/ResponseCustomToolCallInputDoneEvent\" ... discriminator: propertyName: type" | type: official
- [C2] [D8]字面`data:"[DONE]"`的`DoneEvent`只被Assistants专用(beta)的`AssistantStreamEvent`引用,不在Responses联合里 | src: https://github.com/openai/openai-openapi/blob/master/openapi.yaml | quote: "oneOf: - $ref: \"#/components/schemas/ErrorEvent\" - $ref: \"#/components/schemas/DoneEvent\" x-oaiMeta: name: Assistant stream events beta: true" | type: official
- [C3] [D8]DoneEvent字段定义:data恒为字符串"[DONE]";此定义只服务Assistants(见C2)不服务Responses | src: https://github.com/openai/openai-openapi/blob/master/openapi.yaml | quote: "data: type: string enum: - \"[DONE]\" ... description: Occurs when a stream ends." | type: official
- [C4] [D8]官方streaming指南(.md全文检索DONE零命中)的关键事件清单不含[DONE] | src: https://developers.openai.com/api/docs/guides/streaming-responses | quote: "response.created - response.output_text.delta - response.completed - error" | type: official
- [C5] [D8]secondary佐证:openai-python通用SSE解码器(Completions/Assistants/Responses共用)仍对字面[DONE]特判并break,属防御性兼容非服务端实证 | src: https://github.com/openai/openai-python/blob/main/src/openai/_streaming.py | quote: "if sse.data.startswith(\"[DONE]\"): break" | type: official
- [C6] [D6]R1判定:需补限定条件。指南"默认带encrypted_content"限定在stateless mode(store=false或组织启用ZDR) | src: https://developers.openai.com/api/docs/guides/reasoning | quote: "When you create a response in stateless mode, reasoning items in the response's output array include an encrypted_content property by default." | type: official
- [C7] [D6]guide把include里reasoning.encrypted_content定性为legacy、非必需,示例store:false不传include也返回该字段,化解R1"两处关系不明"疑问 | src: https://developers.openai.com/api/docs/guides/reasoning | quote: "The API still accepts the legacy reasoning.encrypted_content value in include for compatibility, but doesn't require it." | type: official
- [C8] [D6]残留点:openapi.yaml对该字段措辞不限store条件(比guide更绝对),store=true默认场景是否也默认带此字段未见明说 | src: https://github.com/openai/openai-openapi/blob/master/openapi.yaml | quote: "This is populated by default for reasoning items returned by `POST /v1/responses` and WebSocket `response.create` requests." | type: official
- [C9] [D1]R1判定:正确。Authorization为必填(除非改设x-api-key),值是Bearer token,token即API key本身 | src: https://platform.claude.com/docs/en/api/overview | quote: "`Bearer <token>`, where `<token>` is your API key or a short-lived access token obtained from `POST /v1/oauth/token`" | type: official
- [C10] [D1]R1判定:正确。x-api-key行逐字确认为Authorization的legacy fallback且非必填,与R1摘录一致 | src: https://platform.claude.com/docs/en/api/overview | quote: "Your API key from Console. Legacy fallback for `Authorization`, still supported" | type: official
- [C11] [D9]R1判定:范围"Opus4.6后发布模型"正确,机制需修正——非笼统忽略,是deprecated+仅接受一个兼容值(1.0)其余报400 | src: https://platform.claude.com/docs/en/api/messages | quote: "Deprecated. Models released after Claude Opus 4.6 do not support setting temperature. A value of 1.0 will be accepted for backwards compatibility, all other values will be rejected with a 400 error." | type: official
- [C12] [D9]top_p同构,但兼容阈值是">=0.99"区间而非单值,R1原笔记未区分 | src: https://platform.claude.com/docs/en/api/messages | quote: "Deprecated. Models released after Claude Opus 4.6 do not support setting top_p. A value >= 0.99 will be accepted for backwards compatibility, all other values will be rejected with a 400 error." | type: official
- [C13] [D9]top_k与前两者不同:无任何兼容值,任何取值都被拒绝,R1笔记未区分此细节 | src: https://platform.claude.com/docs/en/api/messages | quote: "Deprecated. Models released after Claude Opus 4.6 do not accept top_k; any value will be rejected with a 400 error." | type: official
- [C14] [D9]未见独立迁移指南页收录此弃用;索引页只列各模型专属迁移页,不含采样参数变更 | src: https://platform.claude.com/docs/en/about-claude/models/migration-guide | quote: "Guides for migrating to the latest Claude models from previous Claude versions" | type: official

## conflicts
- [D6] openapi.yaml字段描述("populated by default...",不限store)与reasoning指南(限定stateless/store=false/ZDR)范围不一致,两页未互引,store=true默认场景行为不确定。见C6、C8。

## gaps
- [D6] store=true(默认非ZDR)时reasoning item是否也默认带encrypted_content,两一手页面均未明说。
- [D9] 未见一手页把三参数弃用整理成独立迁移公告,权威原句只在api/messages参数表;已查migration-guide索引页及opus-5-5专属迁移页均未提及。
- [D8] developers.openai.com的streaming-events参考页(astro站,.md后缀404)两次WebFetch均"未找到",改用openapi.yaml schema佐证。

## leads
- openai-openapi里Assistants专用DoneEvent(beta)仍保留,与迁移指南"Assistants已2026-08-26 sunset"是否矛盾,值得单独核verify。
- platform.claude.com与developers.openai.com文档页URL加`.md`可直接拿原始Markdown(含完整参数表),比WebFetch更稳定,建议后续工人优先尝试。
- pplx线索(未一手核实):采样参数弃用似从Claude Opus 4.7起对后续新模型生效,可作追问"具体分界模型"起点。
