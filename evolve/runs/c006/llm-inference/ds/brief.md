# Brief: vLLM / SGLang / TensorRT-LLM / llama.cpp 对比调研

## 读者与目标
要给服务选推理引擎的工程师。5 分钟内建立「四个引擎分属不同家族、各自适合什么场景」的认知，再按需查矩阵细节。

## 范围内
- 四个主实体：vLLM、SGLang、TensorRT-LLM、llama.cpp
- 周边实体（关系层面）：Ollama、MLX、TGI、LMDeploy 等（只讲关系与定位，不展开）
- 维度：调度与吞吐（continuous batching、prefill/decode 分离）、KV cache 与前缀复用、量化格式、硬件后端、结构化输出、投机解码、生产部署形态

## 用户点名的疑点（成稿必须有明确结论）
1. llama.cpp 只能跑 CPU？（预期：否，有 CUDA/Metal/Vulkan 等后端）
2. vLLM 不支持 GGUF？（预期：部分支持，实验性）
3. TensorRT-LLM 是先把模型编译成 TensorRT engine 再跑？（预期：曾是，现在有 PyTorch backend）
4. vLLM prefix caching 和 SGLang RadixAttention 是不是一回事？（预期：思想同源，实现/语义不同）

## 范围外
- 训练框架、量化工具本身（AWQ/GPTQ 怎么做）
- 各引擎性能 benchmark 数值对比（无统一口径，只讲定位差异）
- API 级教程

## 完成标准
- budget 9000 字符（含来源节），写到 ds/report.md 和 ./report.md
- 每个疑点有结论；矩阵核心格 ✅/∅；坑一节有可操作事实
- rounds=3, workers=6/轮
