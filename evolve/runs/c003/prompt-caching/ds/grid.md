# grid — taxonomy v0

## 分类轴（家族划分依据）
缓存键从哪来：
- F1 自动前缀缓存：服务方按请求前缀自动匹配命中，用户零改动（OpenAI、DeepSeek、Gemini implicit）
- F2 请求内手动断点：用户在消息里打标记（Anthropic cache_control）
- F3 显式缓存资源对象：先 create 一个服务端 cache 再引用（Gemini cachedContents、Kimi /caching）
- F4 网关透传：行为取决于上游 provider（OpenRouter）

## 维度（每列回答一个问题）
- D1 机制：自动 / 手动断点 / 显式对象？要不要改代码
- D2 写法：具体字段名/参数（cache_control、prompt_cache_key、cached_content…）
- D3 门槛：最小可缓存 token 数
- D4 确认命中：响应里哪个字段；是否保证命中
- D5 计费：写入溢价、读取折扣、存储费
- D6 TTL：默认寿命、滚动续期、可配置范围
- D7 失效：哪些改动/条件让缓存失效（前缀、tools、system、model、图像…）
- D8 隔离/范围：org 级？绑 model？路由亲和（same machine）？
- D9 支持范围：哪些模型、是否兼容 stream/tools/vision/batch

## 网格（状态：✅⚠⚔❓∅—）
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| OpenAI | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Anthropic | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Gemini (explicit) | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Gemini (implicit) | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| DeepSeek | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Kimi/Moonshot | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 智谱 GLM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 通义千问/DashScope | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| OpenRouter | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| （补充：xAI/Bedrock/Azure/其他） | — | — | — | — | — | — | — | — | — |

## 备注
- 最后一条「补充」行由 scout leads 决定是否升格为正式行。
