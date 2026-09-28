# brief：LLM 推理引擎横向对比（vLLM / SGLang / TensorRT-LLM / llama.cpp）

## 读者与目标
有技术背景、要给项目选推理引擎或纠正过时印象的用户。5 分钟建立认知：四个引擎现在（2026-09）各自的定位、能力边界、怎么选。

## 范围内
- 核心实体：vLLM、SGLang、TensorRT-LLM、llama.cpp
- 周边关系实体：Ollama、MLX、TGI（只讲与核心四者的关系/定位，不做同等深度）
- 维度：调度与吞吐（continuous batching、chunked prefill、prefill/decode 分离）、KV cache 与前缀复用、量化与模型格式、硬件后端（CUDA/ROCm/CPU/Metal/TPU）、结构化输出与投机解码、生产部署形态、选型与版本坑

## 范围外
训练框架；云托管服务（Bedrock/Vertex）；单机 benchmark 数字横评（除非官方文档写了）

## 用户点名疑点（成稿必须给结论）
1. llama.cpp 只能跑 CPU？（预期：否，有 CUDA/Metal/Vulkan/ROCm/SYCL 后端——需一手来源）
2. vLLM 不支持 GGUF？（预期：有实验性 GGUF 支持——需一手来源）
3. TensorRT-LLM 仍要先把模型编译成 TRT engine？（预期：PyTorch backend 已成默认/主推路径——需一手来源与版本起点）
4. vLLM prefix caching 与 SGLang RadixAttention 是不是一回事？（预期：目标相同、机制不同——hash 块复用 vs radix tree）

## 参数
rounds=3, workers=6, budget=9000 chars, dir=./ds, 成稿同时写 ./report.md

## 完成标准
- grid 核心格子 ✅/∅，冲突有裁决或进未决
- 四条疑点各有一句明确结论+来源
- report.md ≤ 9000 字符，含来源节
