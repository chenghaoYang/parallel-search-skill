# grid v1（R1 收束后）

## 分类轴（沿用 v0，能解释差异）
A. 运行基底：PyTorch 动态图（vLLM、SGLang、TRT-LLM 现唯一后端）vs 自包含 C/C++（llama.cpp）。TRT engine AOT 路径已死（v1.2 移除）
B. 目标场景：数据中心 serving（vLLM/SGLang/TRT-LLM）vs 本地/边缘（llama.cpp）
C. 模型工件：HF safetensors 直载（vLLM/SGLang/TRT-LLM）vs GGUF 专属（llama.cpp；vLLM 仅实验插件）

## 网格状态
| 实体 | D1 调度 | D2 KV/前缀 | D3 量化 | D4 硬件 | D5 结构化 | D6 投机 | D7 部署 | D8 覆盖 |
|---|---|---|---|---|---|---|---|---|
| vLLM | ✅ | ✅ hash块/LRU | ✅(GGUF=实验插件⚔已裁) | ✅ | ✅ xgrammar/guidance | ✅(Medusa❓) | ✅ | ✅ |
| SGLang | ✅ | ✅ radix树/LRU | ✅(gptq⚔→gptq_marlin) | ✅ | ✅ xgrammar默认 | ✅ | ✅ | ✅ |
| TRT-LLM | ✅ | ✅ radix树/prioritized-LRU | ✅ | ✅ NVIDIA-only | ✅ xgrammar/llguidance | ⚔ Eagle3-only 语境未裁 | ✅ | ✅ |
| llama.cpp | ✅(PD∅未合入) | ✅ prompt cache/KV shifting | ✅ GGUF-only | ✅ 16后端 | ✅ GBNF/JSON schema | ✅ --spec-type | ✅ | ✅ |
| 周边 | — | — | — | — | — | — | ✅ Ollama多引擎/TGI归档/Dynamo·llm-d 编排层 | — |

## R1 遗留 → R2 简报
- TRT-LLM⚔：spec 页 "PyTorch backend supports only Eagle3" 与多 decoding_type 并存 → 要上下文原句；另补 v1.0.0 日期、Medusa/lookahead/SmoothQuant 移除版本、LICENSE
- vLLM：vllm-gguf-plugin 细节（量化类型/硬件）；Medusa 移除出处；stable 版 enable_prefix_caching 默认
- SGLang：radix cache 默认开（--disable-radix-cache 语义）；chunked-prefill 默认；docs.sglang.io 新安装页 pin 警告；/v1/responses
- llama.cpp 次要 gap 不进 R2：llguidance 文档、RPC 细节 → §5 或一句带过
