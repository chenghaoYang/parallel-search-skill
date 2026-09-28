# grid: 实体 × 维度

## 分类轴（taxonomy 骨架）
机制三家族：
- **A 自动前缀缓存**：服务端自动按前缀命中，零代码改动。预期：OpenAI、DeepSeek、Gemini implicit、Qwen?
- **B 显式断点**：请求里打 cache_control 断点标记前缀边界。预期：Anthropic（OpenRouter 透传）
- **C 显式缓存对象**：先调 API 创建 cache 资源拿到 cache_id，后续请求引用。预期：Gemini explicit、Kimi

## 维度（列，彼此正交）
- D1 机制家族+启用方式：要不要改代码/打标记/建对象？
- D2 计费-读：命中部分按什么价？（cached token 单价/折扣）
- D3 计费-写/存：写入是否溢价？有无按时长/容量存储费？
- D4 TTL：缓存存活多久、是否滚动续期？
- D5 门槛与约束：最小 token 数、适用模型、prefix 对齐粒度
- D6 命中观测：响应里哪个字段确认命中（usage.* 原名）
- D7 失效条件：哪些请求改动会 miss（system/tools/参数）
- D8 作用域：缓存按什么隔离（org/model/显式 id/地区）

## 网格（状态：❓待查）
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 |
|---|---|---|---|---|---|---|---|---|
| OpenAI | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Anthropic | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Gemini implicit | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Gemini explicit | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| DeepSeek | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Kimi | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 智谱 GLM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Qwen | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| OpenRouter | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
