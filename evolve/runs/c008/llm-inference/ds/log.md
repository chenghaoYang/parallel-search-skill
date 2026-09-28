# log

## R0
- taxonomy v0：分类轴 = 部署目标×运行栈，三家族（A 数据中心 serving / B 本地便携运行时 / C 封装分发层）；维度 D1–D7。
- 四条疑点登记为 Q1–Q4。
- R1 计划：按来源边界 4 工人（每引擎一工人填全行）+ 1 周边关系 + 1 scout。共 6 spawn。

## R1
- spawn：r1-vllm, r1-sglang, r1-trtllm, r1-llamacpp, r1-ecosystem, r1-scout（6/6 上限）
- 等批中。
- r1-ecosystem 返回：15 claims 全 official。要点：TGI 已归档/维护态，官方推荐 vLLM/SGLang/llama.cpp/MLX；Ollama 2026-03 起 Apple silicon 用 MLX 引擎（README 未更新，冲突 1）；Ollama↔llama.cpp 关系有官方句。
