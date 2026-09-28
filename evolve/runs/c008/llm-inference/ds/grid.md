# grid v0

状态：✅ 一手来源+摘录 | ⚠ 仅二手 | ⚔ 冲突 | ❓ 缺口 | ∅ 官方未写 | — 不适用

## 分类轴
轴 = 「部署目标 × 运行栈」：
- A 家族「数据中心 GPU serving 框架」：vLLM、SGLang、TensorRT-LLM —— 为高并发多用户 serving 设计，Python 服务形态，假设 GPU 集群
- B 家族「本地/边缘便携运行时」：llama.cpp（+MLX 同类）—— 单用户/低并发，C/C++ 直写 kernel，跨全硬件
- C 家族「封装/分发层」：Ollama（封装 llama.cpp）、TGI（HF 的 serving 栈，与 A 家族同层）—— 不是新引擎，是包装或竞品

## 维度（每列回答什么）
- D1 定位与治理：谁维护、它自我定位是什么
- D2 调度与吞吐：有没有 continuous batching / chunked prefill / prefill-decode 分离（disaggregated serving）
- D3 KV cache 与前缀复用：机制名、粒度、是否跨请求共享前缀
- D4 量化与模型格式：GGUF/GPTQ/AWQ/FP8/INT4/safetensors 各支持到什么程度
- D5 硬件后端：CUDA / ROCm / CPU / Metal / TPU / 其他
- D6 结构化输出与投机解码：guided decoding(xgrammar/outlines)、speculative decoding(EAGLE/MTP/n-gram)
- D7 生产部署形态：server 命令、OpenAI 兼容 API、k8s/分布式方案（Dynamo、llm-d、trtllm-serve 等）

## 网格
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|---|
| vLLM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| SGLang | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| TensorRT-LLM | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| llama.cpp | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| Ollama/MLX/TGI（关系行） | ❓ | — | — | — | — | — | ❓ |

## 疑点格子（必须结论）
- Q1 llama.cpp D5：「只能 CPU」真伪
- Q2 vLLM D4：GGUF 支持状态
- Q3 TRT-LLM D1/D7：TRT engine 编译路径 vs PyTorch backend 现状（版本起点）
- Q4 vLLM D3 vs SGLang D3：prefix caching 与 RadixAttention 机制差异
