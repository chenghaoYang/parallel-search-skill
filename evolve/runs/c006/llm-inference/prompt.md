/deep-search 产出文档 帮用户搞清楚 vLLM、SGLang、TensorRT-LLM、llama.cpp 这几个 LLM 推理引擎现在有什么不同

seed keywords: vLLM PagedAttention. SGLang RadixAttention. TensorRT-LLM PyTorch backend. llama.cpp GGUF

some user aware variation: 听说 llama.cpp 只能跑 CPU、vLLM 不支持 GGUF、TensorRT-LLM 是先把模型编译成 TensorRT engine 再跑——现在还是这样吗？另外 vLLM 和 SGLang 的前缀缓存（prefix caching / RadixAttention）是不是就是一回事


起码先这 4 个，然后说清它们在调度与吞吐（continuous batching、prefill/decode 分离）、KV cache 与前缀复用、量化格式支持、硬件后端（CUDA/ROCm/CPU/Metal）、结构化输出与投机解码、生产部署形态上的差异


以及其他用户需要知道的问题（怎么选、版本踩坑、和 Ollama/MLX/TGI 这类周边项目的关系）


大规模并行调研，一个turn指一次spawn，需要多次

不允许仅扩展而不收束，最终文档应该详细但快速建立认知和对比，帮助用户了解细节，以及额外可能需要知道的相关scope下的任何信息。希望建立taxonomy

不停的refine，根据observation做出下一步best next action

不允许文章越来越长

---
外层说明（Claude Code，benchmark 固定设置）：
- 参数：--rounds 3 --workers 6 --budget 9000。
- skill 目录是 .claude/skills/deep-search。工作目录用 ./ds（dir=./ds）。最终文档同时写到 ./report.md。
- 工人用 subagent_type "research-worker"（模型已由外层固定，不要传 model）。
- 检索：工人用 WebSearch 找页面，再用 WebFetch 打开一手页面取原句。本次运行没有 pplx-safe。
- 当前目录之外的文件与本任务无关，不要读。
