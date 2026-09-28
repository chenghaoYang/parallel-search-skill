# log

## R0 框架
- 分类轴：运行基底（PyTorch 动态图 / AOT engine / 自包含 C++）× 目标场景（数据中心 / 本地边缘）× 模型工件（HF / GGUF / TRT engine）
- 维度 D1–D8：调度吞吐、KV/前缀、量化、硬件、结构化输出、投机解码、部署形态、模型覆盖

## R1 扩展（spawn 6）
- r1-vllm / r1-sglang / r1-trtllm / r1-llamacpp：各填 D1–D8 全行，重点带回 GGUF、RadixAttention、PyTorch backend、GPU 后端的官方原句
- r1-relations：Ollama/MLX/TGI/Dynamo/llm-d 关系
- r1-scout：版本坑 + 漏项（只进 leads）
- 待查：许可证列（Apache/MIT）R1 简报没列，scout leads 若无则 R2 补一格
- 待查：vLLM prefix caching 是否已改为 radix/hash 树（V1 后实现细节）

## R1 收束
- 笔记 154 claims（official 152），矩阵 33/37 格填上
- 关键结论：4 个疑点全部有官方裁决；TRT-LLM 也用 radix tree（vLLM 才是 hash 派）
- ⚔×3：SGLang gptq（README 宣传 vs docs 已移除→取 docs gptq_marlin）；TRT-LLM "PyTorch only Eagle3" 语境不明；Ollama README vs 博客（doc lag，取博客）
- report.md 9663→8596（超 9000 预算，压来源标题）
- R2 观察：核心格子基本 ✅；剩 TRT-LLM D6 ⚔、GGUF 插件细节、版本起点若干 → 动作：2 个窄简报（trtllm 冲突裁决、vllm-gguf-plugin）→ 预计 spawn：2

## R2 收束（spawn 2）
- r2-trtllm：Eagle3 冲突裁决=仅指 EAGLE 家族（v1/v2 ckpt 不兼容），非全局限制；v1.0.0=2025-09-24；Medusa/lookahead/SmoothQuant 无 1.x 移除条目（随 TRT 后端消失）；LICENSE=Apache-2.0
- r2-vllm：GGUF 插件仅 CUDA/ROCm、测过 Q6_K/Q8_0/IQ4_XS/Q4_K_M/Q4_0/UD-IQ2_XXS；Medusa 仍在 --spec-method 枚举；prefix caching v0.13+ 显式默认 True
- report 8596→9000（=budget 上限）
- 终审：预算紧，1 个核验工人 × 10 条（一屏+疑点+坑 全量高影响主张）
