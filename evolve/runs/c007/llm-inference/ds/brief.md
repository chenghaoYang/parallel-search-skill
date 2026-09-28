# brief：vLLM / SGLang / TensorRT-LLM / llama.cpp 现状对比

读者：知道 LLM 推理基本概念（prefill/decode、KV cache、量化）的工程师，要选型或更新旧认知。
目标：5–10 分钟建立 taxonomy + 差异认知；用户点名的旧说法必须给出明确裁决。

## 范围内
- 4 个主实体：vLLM、SGLang、TensorRT-LLM、llama.cpp
- 周边关系：Ollama、MLX、TGI、Dynamo/llm-d 等部署层（解释关系即可，不做全面对比）
- 维度：调度与吞吐（continuous batching、chunked prefill、PD 分离）、KV cache 与前缀复用、量化格式、硬件后端（CUDA/ROCm/CPU/Metal/TPU）、结构化输出、投机解码、生产部署形态、模型格式/架构覆盖

## 范围外
- 训练框架、云厂商托管服务（Bedrock 等）、具体 benchmark 跑分排名（只记官方声称时标出来源）

## 用户点名疑点（成稿必须裁决）
1. llama.cpp 只能跑 CPU？（旧认知；现 CUDA/ROCm/Metal/Vulkan/SYCL？）
2. vLLM 不支持 GGUF？（文档里 GGUF 支持现状、是否实验性）
3. TensorRT-LLM 必须先编译 TRT engine？（PyTorch backend 是否已是默认/官方推荐路径）
4. vLLM prefix caching 与 SGLang RadixAttention 是不是一回事？（数据结构、复用粒度、跨请求/多轮差异）

## 参数
rounds=3, workers=6, budget=9000 字符, dir=./ds, 终稿另写 ./report.md
