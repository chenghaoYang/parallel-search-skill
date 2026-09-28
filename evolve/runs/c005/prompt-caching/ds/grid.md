# grid — taxonomy v0

## 分类轴（把实体分成家族的依据）
**A. 缓存指令谁给**：隐式自动（provider 自己匹配前缀，不用改代码）vs 显式断点（请求里标 cache_control/cachePoint）vs 显式缓存对象（先建 cache 资源再引用）。
**B. 缓存存活模型**：固定 TTL（到期即死）vs 用量驱动/LRU（无承诺 TTL）vs 用户管理对象（显式建/删/续）。

预期家族：
- F1 自动前缀缓存：OpenAI、DeepSeek、Gemini implicit
- F2 显式断点：Anthropic
- F3 显式缓存对象：Gemini explicit、Kimi（？待核实）
- F4 透传网关：OpenRouter（策略取决于上游）

## 维度（每列回答一个问题）
- D1 机制与开关：要改代码吗？用什么字段/端点/header？
- D2 门槛与粒度：最小可缓存 tokens？块大小？
- D3 计费：写入溢价？命中读取折扣（相对原价）？存储费？
- D4 生命周期：TTL？续期规则？
- D5 确认命中：响应里哪个 usage 字段？
- D6 失效条件：什么改动打掉缓存？
- D7 作用域/隔离：缓存按什么边界隔离（org/model/workspace）？
- D8 模型覆盖：哪些模型支持？
- D9 约束：断点上限、beta header、地区/端点限制。

## 网格（行=实体 × D1..D9）

| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| OpenAI | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Anthropic | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Gemini explicit | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Gemini implicit | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| DeepSeek | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Kimi/Moonshot | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 智谱 GLM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| 通义千问 DashScope | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| OpenRouter | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
