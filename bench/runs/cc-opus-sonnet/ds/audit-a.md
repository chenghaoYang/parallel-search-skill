# audit-a：report.md §0/§1/§2 抽查

范围：report.md 第 5–81 行（§0 一屏看懂、§1 Taxonomy、§2 对照矩阵）。逐条核对 notes/ 与 2 次直接 WebFetch 复核（financeReason 枚举数、extended-thinking 4.7+ 原句、Interactions 端点）。

## §0 一屏看懂

supported | `input` item 数组→`output` item 数组，推理、工具调用、工具结果都是独立 item | r1-openai-responses.md[C3] | —
supported | Assistants API 已于 2026-08-26 下线 [2] | r1-openai-responses.md[C26] | —
weak | Google 称 generateContent 为 legacy（仍完全支持）[23] | r1-gemini-generatecontent.md conflicts 节：quote "While it is now considered legacy, the original generateContent API remains fully supported." 中"it"指代不清，笔记本身标为歧义未裁决 | 建议加"（原句 it 指代有歧义，非明确陈述）"或改弱语气
supported | 推荐新项目用 2026-06 GA 的 Interactions API（服务端状态）[23] | r1-gemini-generatecontent.md[C35]；r2-gemini-interactions.md[C21] | —
supported | Responses 家族已有厂商中立规范 Open Responses（2026-01-15）[9][26] | r2-open-responses.md[C1][C3] | —
supported | Anthropic 的 `thinking` 带 `signature`，须原样按序回传，否则 400 | r1-anthropic-messages.md[C23] | —
supported | Gemini 缺签名返回 `MISSING_THOUGHT_SIGNATURE` | r1-gemini-generatecontent.md[C23] | —
supported | Opus 4.6 之后发布的 Claude 模型，temperature 只接受 1.0、top_p 只接受 ≥0.99、top_k 任何值都 400 | r2-verify-ref.md[C11][C12][C13]（对 R1 的一手升级复核） | —
supported | 4.6+ 禁预填 | r1-anthropic-messages.md[C8]（quote: "Claude 4.6+ 与 Mythos Preview 不支持预填，返回 400"），citation [18]=api/errors 对应 | —
supported | 4.7+ 禁 `thinking.type:"enabled"` | r1-scout.md[C18] + WebFetch 直接核对 https://platform.claude.com/docs/en/build-with-claude/extended-thinking：quote "Claude 4.7 and later models do not support it and reject requests that use it, returning a 400 error." | —
supported | DeepSeek…Responses 入口（2026-08-13，官方称专为 Codex 适配） | r2-deepseek-responses.md[C31]（quote: "...is specifically adapted for Codex."） | —
supported | 智谱默认 `store=false`（§0-3，指智谱 Responses `/api/v1`） | r2-zhipu-anthropic.md[C15] | 建议行文注明这是智谱 Responses 端点而非 §0-6 的 Anthropic 兼容端点，避免读者混淆两个不同入口

## §1 Taxonomy

supported | Items｜OpenAI `/v1/responses`…状态列＝可选服务端状态 | r1-openai-responses.md[C4]（store 缺省 true 但可 store:false） | —
supported | Blocks｜Anthropic `/v1/messages`…状态列＝无状态 | r1-anthropic-messages.md[C10] | —
supported | Steps｜Gemini `/v1beta/interactions`…状态列＝服务端状态 | WebFetch 直接核对 https://ai.google.dev/api/interactions-api：quote "post https://generativelanguage.googleapis.com/v1beta/interactions"；状态见 r2-gemini-interactions.md[C21] | —
weak | Chat｜OpenAI `/v1/chat/completions`…状态列＝无状态 | r1-openai-chat.md gaps："未找到'Chat Completions 是 stateless'的官方原句；D3 结论从 store/GET 系列端点行为反推" | 建议标注为推断结论，非直接引用
weak | Parts｜Gemini `:generateContent`…状态列＝无状态＋缓存资源 | r1-gemini-generatecontent.md 无直接"generateContent 无状态"原句，同上反推逻辑 | 同上，建议加"（推断）"

## §2 对照矩阵

### D1–D4
weak | Messages 鉴权："`anthropic-version: 2023-06-01` 必填"，该行仅标 [10][11] | r1-anthropic-messages.md[C2] 显示该事实原句出自 api/versioning（＝来源表 [12]），未见 [10]/[11] 页含此句 | 建议在该格补标 [12]
supported | Messages 鉴权："`Authorization: Bearer`，`x-api-key` 是 legacy fallback" | r1-anthropic-messages.md[C3]；r2-verify-ref.md[C9][C10]（一手复核确认） | —
supported | Responses 状态："`store` 缺省 true，至少 30 天；`previous_response_id` 与 `conversation` 互斥、不继承 `instructions`；Conversation 无 30 天 TTL [3]" | r1-openai-responses.md[C4][C5][C6] | —
unsupported | Responses 鉴权："同左"（沿用 Chat 的 Bearer/OpenAI-Organization） | r1-openai-responses.md 全篇无鉴权相关 claim，checked 列表也未含 authentication 页 | 建议补一条鉴权引用（如 api-reference/authentication）或删除隐含断言

### D5 工具
supported | Responses 声明："省略 strict 时尽量严格" | r1-openai-responses.md[C10] | —
supported | Messages 回传："user 消息里的 `tool_result{...}`，须排在最前 [14]" | r1-anthropic-messages.md[C18] | —
supported | Responses 托管工具："16 类，如 web_search、file_search、mcp" | r1-openai-responses.md[C9]（"16成员union"） | —
supported | Messages 托管工具举例："`web_search_20260209`" | r1-anthropic-messages.md[C20] | —

### D6 推理 · D7 JSON · D9 参数
supported | Responses 推理返回："`reasoning` item：summary＋`encrypted_content`（无状态模式默认返回）[5]" | r2-verify-ref.md[C6]（对 R1 未加限定的原句做出修正，成稿已采用修正版） | —
supported | Messages 回传："原样原序回传，改动即 400" | r1-anthropic-messages.md[C23] | —
supported | Responses 采样："temperature 0–2、top_p；无 stop/n/seed" | r1-openai-responses.md[C8][C20] | —

### D8 流式 · D10 停止/用量/缓存
supported | Responses 流式："带 `event:` 的语义事件…无 `[DONE]` [4]" | r2-verify-ref.md[C1]–[C4]（schema 级 + guide 级双重核实） | —
supported | Messages 流式："2023-06-01 起无 `[DONE]` [12][13]" | r1-anthropic-messages.md[C32] | —
contradicted | generateContent 停止："`finishReason` 19 项，含 SAFETY、RECITATION、MALFORMED_FUNCTION_CALL" | WebFetch+curl 直接核对 https://ai.google.dev/api/generate-content 的 FinishReason 枚举表：实际列出 21 个值（含 FINISH_REASON_UNSPECIFIED）/20 个（不含）；且笔记 r1-gemini-generatecontent.md[C33] 自己列出的名单逐个数也是 20 个，并非 19 | 改为"20 项"（不含 UNSPECIFIED）或"21 项"（含），并补列漏掉的 IMAGE_PROHIBITED_CONTENT/IMAGE_OTHER/IMAGE_RECITATION
supported | Messages 缓存："显式 `cache_control`…≤4 断点，最小 512–4096" | r1-anthropic-messages.md[C37] | —
supported | generateContent 缓存："隐式缓存（2.5+ 默认，最小 2048/4096）＋显式 `cachedContents` [22]" | r1-gemini-generatecontent.md[C12] | —
supported | Chat 缓存："自动前缀缓存（GPT-5.6+ ≥1,024 tokens）；`prompt_cache_key`；`prompt_cache_options.ttl` [6]" | r1-openai-chat.md[C27] | —

### Gemini 的两个入口
supported | Interactions 输入："`input`（字符串/Content/Step 数组）＋`system_instruction`；角色靠 `Step.type`" | r2-gemini-interactions.md[C2][C3][C4] | —
supported | Interactions 推理/JSON/参数："`generation_config`（参考页未列 temperature）" | r2-gemini-interactions.md[C17]（"全页0命中"temperature/top_p/top_k/candidate_count） | —
supported | Interactions 流式/状态："`store` 默认 true，`previous_interaction_id`，`background` [23]" | r2-gemini-interactions.md[C21][C22]；r1-gemini-generatecontent.md[C36] | —

## 计数
supported 31 / weak 4 / unsupported 1 / contradicted 1（共 37 条）
