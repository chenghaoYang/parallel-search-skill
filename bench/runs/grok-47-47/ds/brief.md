# R0 brief

读者：要在自己的客户端、网关或 SDK 里接多家大模型的工程师。他们见过 OpenAI Chat Completions，但分不清 Responses、Anthropic Messages、Gemini generateContent，也不知道「兼容 OpenAI / 兼容 Anthropic」的国内厂商改了哪些字段。

几分钟内要建立的认知：

1. 市面上的「聊天 API」不是一个协议，而是少数几种请求谱系。
2. 谱系差在：历史谁保存、内容是字符串还是块、系统指令放哪、工具结果怎么回传、流式事件长什么样、响应体叫什么。
3. 下游厂的「兼容」是有损适配：要能指出 DeepSeek 的响应相对 OpenAI 官方文档差在哪，以及智谱的 Messages 相对 Anthropic 官方差在哪。

成稿上限：20000 字符（含来源）。日期锚点：2026-09-23。工作目录：`./ds`。最终文档同时写到仓库根 `./report.md`。

## 范围内

- 请求与响应协议（HTTP 路径、header、JSON 字段、枚举、流式事件），不是模型能力榜、价格、上下文长度。
- 四个官方谱系：OpenAI Chat Completions、OpenAI Responses、Anthropic Messages、Google Gemini `generateContent`。
- 下游对上述谱系的有损适配。R0 先列入：DeepSeek、智谱、阿里云百炼 compatible-mode、Moonshot。其余由 scout 的 leads 决定是否进网格。
- 用户会踩的协议坑（换端点时静默丢字段、流式对不齐、工具消息角色不同）。

## 范围外

- 训练、微调、批处理文件格式、向量、图像专用 API（除非它就是上述聊天端点上的一个字段）。
- SDK 方法名对照（只在它暴露了协议字段差异时才记）。
- 各家模型质量、价格、速率限制数值（除非该限制改变了请求字段的合法性）。

## 种子词

chat completions；Responses；messages；Google generateContent。

## 用户点名、成稿必须给结论

1. DeepSeek 官方的 response（响应体，以及若有 `/responses` 或同名协议）相对 OpenAI 官方文档差在哪。结论可以是「官方写明的差异清单」或「官方没写」。
2. 智谱的 message 接口相对 Anthropic 官方 Messages 差在哪。
3. 至少四个主流谱系先讲清，再讲下游适配，而不是把所有厂商平铺成一张无家族的大表。

## 完成标准

- taxonomy 能解释矩阵里的大部分差异（分类轴写在 `grid.md`）。
- 每个具体事实能追到笔记主张；没有一手来源的进「未决」。
- 成稿按 `references/converge.md` 的骨架，且不超过 20000 字符。
- 至少两轮扩展；最后一轮是收束（含终审后的改稿）。
