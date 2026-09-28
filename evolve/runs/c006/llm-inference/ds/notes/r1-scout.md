# r1-scout
question: 用户在选择/使用 vLLM、SGLang、TensorRT-LLM、llama.cpp 时最常踩的坑、版本变化造成的过时认知、以及容易被漏掉的相关实体/维度（scout：重点产出 leads）
checked: https://github.com/vllm-project/vllm/issues/18571, https://github.com/vllm-project/vllm/releases/tag/v0.11.0, https://docs.vllm.ai/en/latest/usage/v1_guide/, https://docs.vllm.ai/en/latest/features/quantization/gguf/, https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html, https://docs.vllm.ai/en/latest/design/prefix_caching.html, https://docs.vllm.ai/en/stable/getting_started/installation/gpu/index.html, https://nvidia.github.io/TensorRT-LLM/latest/legacy/tensorrt-backend-removal.html, https://nvidia.github.io/TensorRT-LLM/_sources/release-notes.md.txt, https://sgl-project-sglang-93.mintlify.app/resources/migration-guide, https://github.com/sgl-project/sglang/releases/tag/v0.5.16, https://github.com/sgl-project/sglang/releases/tag/gateway-v0.3.0, https://github.com/sgl-project/sglang/issues/9710, https://github.com/ggml-org/llama.cpp/pull/7809, https://github.com/ggml-org/llama.cpp/commit/d2fcd91cf96b46f4485ce46b4e3a32bf0df37715, https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md, https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md, raw READMEs of all four repos, gh api licenses

## claims
- [C1] vLLM v0.11.0 完全移除 V0 引擎代码 | src: https://github.com/vllm-project/vllm/releases/tag/v0.11.0 | quote: "This release completes the removal of V0 engine. ... V1 is the only engine in the codebase now." | type: official
- [C2] V1 自 v0.8.0 起为默认引擎；V0 自 v0.9.0 冻结 | src: https://github.com/vllm-project/vllm/issues/18571 | quote: "vLLM V1 has been the default engine since version v0.8.0" | type: official
- [C3] V1 永久砍掉 prompt adapter、V100 GPU、per-request structured output backend | src: https://github.com/vllm-project/vllm/issues/18571 | quote: "Features Permanently Dropped ... Prompt adapter / V100 support / Per-request structured outputs backend" | type: official
- [C4] V1 移除 best_of、per-request logits processors、GPU↔CPU KV swapping | src: https://docs.vllm.ai/en/latest/usage/v1_guide/ | quote: "best_of: This feature has been removed due to limited usage." / "vLLM V1 no longer requires KV cache swapping" | type: official
- [C5] V1 中 Whisper 已被原生支持（encoder-decoder 曾列为暂停支持） | src: https://docs.vllm.ai/en/latest/usage/v1_guide/ | quote: "Whisper is supported natively." | type: official
- [C6] v0.11.0 起默认 CUDA graph 模式为 FULL_AND_PIECEWISE；且该版 --async-scheduling 有已知乱码 bug | src: https://github.com/vllm-project/vllm/releases/tag/v0.11.0 | quote: "--async-scheduling will produce gibberish output in some cases such as preemption" | type: official
- [C7] vLLM 的 GGUF 支持是实验性的且已迁出主仓为插件 | src: https://docs.vllm.ai/en/latest/features/quantization/gguf/ | quote: "GGUF support in vLLM is highly experimental and under-optimized" / "GGUF support has migrated to OOT vllm-gguf-plugin" | type: official
- [C8] vLLM V1 prefix caching 是 hash-based（按 KV block 哈希），不是 radix tree | src: https://docs.vllm.ai/en/latest/design/prefix_caching.html | quote: "vLLM chooses a hash-based approach ... we hash each kv-cache block by the tokens in the block and the tokens in the prefix" | type: official
- [C9] vLLM 不原生支持 Windows，官方只给 WSL 或社区 fork | src: https://docs.vllm.ai/en/stable/getting_started/installation/gpu/index.html | quote: "vLLM does not support Windows natively. To run vLLM on Windows, you can use the Windows Subsystem for Linux (WSL)" | type: official
- [C10] vLLM 特性面（README）：量化含 GGUF、multi-LoRA、TP/PP/DP/EP/CP 五种并行 | src: https://raw.githubusercontent.com/vllm-project/vllm/main/README.md | quote: "Quantization: FP8, MXFP8/MXFP4, NVFP4, INT8, INT4, GPTQ/AWQ, GGUF..." / "Tensor, pipeline, data, expert, and context parallelism" | type: official
- [C11] TRT-LLM 1.0：PyTorch 成为默认后端（breaking） | src: https://nvidia.github.io/TensorRT-LLM/_sources/release-notes.md.txt | quote: "BREAKING CHANGE Promote PyTorch to be the default LLM backend" | type: official
- [C12] TRT-LLM 1.2：TensorRT 后端整体移除，trtllm-build/refit/prune CLI 删除，HF ckpt 直读 | src: https://nvidia.github.io/TensorRT-LLM/latest/legacy/tensorrt-backend-removal.html | quote: "The TensorRT engine backend has been removed. PyTorch is now the sole execution backend" / "No engine-build step — HuggingFace checkpoints load directly" | type: official
- [C13] TRT-LLM 1.2 反转了 CLI 与 YAML 配置的优先级 | src: https://nvidia.github.io/TensorRT-LLM/_sources/release-notes.md.txt | quote: "explicit CLI flags now take precedence over values in --config / --extra_llm_api_options YAML files" | type: official
- [C14] TRT-LLM README 定位：PyTorch-native 架构 + 高层 Python LLM API | src: https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/README.md | quote: "Architected on PyTorch" / "TensorRT LLM provides a high-level Python LLM API" | type: official
- [C15] TRT-LLM LICENSE 是 Apache-2.0 但含其他项目衍生代码，GitHub 判定为 Other | src: https://github.com/NVIDIA/TensorRT-LLM/blob/main/LICENSE | quote: "This project is licensed under the Apache 2.0 license ... portions of code that are based on or derived from other open source projects, which may have different licenses" | type: official
- [C16] SGLang 环境变量前缀 SGL_ → SGLANG_，旧前缀仅告警 | src: https://sgl-project-sglang-93.mintlify.app/resources/migration-guide | quote: "All `SGL_` prefixed environment variables are deprecated in favor of `SGLANG_`" | type: official
- [C17] SGLang 超时环境变量单位从毫秒改为秒 | src: 同上 | quote: "Timeout environment variables have changed from milliseconds to seconds" | type: official
- [C18] SGLang v0.4.0：FlashInfer 成默认 attention 后端 + RadixAttention cache 行为变化 | src: 同上 | quote: "FlashInfer becomes the default attention backend" / "Changes to RadixAttention cache behavior" | type: official
- [C19] SGLang v0.5.16 有多个无别名直接改名的 CLI flag，旧命令直接报错 | src: https://github.com/sgl-project/sglang/releases/tag/v0.5.16 | quote: "--enable-deepep-waterfill is renamed to --enable-waterfill with no deprecated alias, so existing launch commands fail" | type: official
- [C20] SGLang v0.5.16 移除 QServe W4A8 与 FBGEMM FP8；NVFP4 GEMM 只能走 FlashInfer | src: 同上 | quote: "the experimental QServe (QoQ) W4A8 and FBGEMM FP8 paths are gone ... NVFP4 GEMM now requires FlashInfer" | type: official
- [C21] SGLang README 定位与硬件面 | src: https://raw.githubusercontent.com/sgl-project/sglang/main/README.md | quote: "SGLang is a high-performance serving framework for large language models and multimodal models." / "Runs on NVIDIA GPUs ..., AMD GPUs (MI355/MI300), Intel Xeon CPUs, Google TPUs, Ascend NPUs" | type: official
- [C22] SGLang 有新实体 Model Gateway（Rust/Go），v0.3.0 含 metrics 架构与 UUID worker 等 breaking | src: https://github.com/sgl-project/sglang/releases/tag/gateway-v0.3.0 | quote: "Metric names and structure have changed. ... Workers are now identified by UUIDs instead of endpoints" | type: official
- [C23] llama.cpp 2024-06 把二进制全部改名加 llama- 前缀，旧教程大面积失效 | src: https://github.com/ggml-org/llama.cpp/pull/7809 + issue/8397 | quote: "`main` → `llama-cli`" / "the existing tutorials all say to run `./main` and `./server`" | type: official
- [C24] llama.cpp Makefile 构建已废弃须用 CMake；LLAMA_* 构建变量废弃改 GGML_* | src: https://github.com/ggml-org/llama.cpp/blob/master/Makefile | quote: "$(error The Makefile build is deprecated. Use the CMake build instead." / "LLAMA_CUBLAS is removed. Use GGML_CUDA instead." | type: official
- [C25] llama.cpp context shift 默认值从启用翻转为禁用（#15416），超长 prompt 现在报错而非静默截断 | src: https://github.com/ggml-org/llama.cpp/commit/d2fcd91cf96b46f4485ce46b4e3a32bf0df37715 | quote: "server : disable context shift by default ... bool ctx_shift = false" | type: official
- [C26] llama.cpp 当前默认值已变：ctx 0=读模型、--jinja 默认开、-fa auto、-ngl auto | src: https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md | quote: "size of the prompt context (default: 0, 0 = loaded from model)" / "default: 'auto'" | type: official
- [C27] llama.cpp 定位与覆盖面：纯 C/C++、CUDA/Metal/HIP/SYCL/Vulkan/CANN/Hexagon、CPU+GPU 混合、OpenAI 兼容 server、VLM | src: https://raw.githubusercontent.com/ggml-org/llama.cpp/master/README.md | quote: "Plain C/C++ implementation without any dependencies" / "Launch OpenAI-compatible API server" / "CPU+GPU hybrid inference" | type: official
- [C28] 许可证：vLLM Apache-2.0、SGLang Apache-2.0、llama.cpp MIT、TRT-LLM Apache-2.0(GitHub 标 Other) | src: gh api repos/{...}.license | quote: spdx_id: Apache-2.0 / Apache-2.0 / MIT / NOASSERTION(Other) | type: official
- [C29] llama.cpp Windows 原生支持（MSVC/clang、arm64） | src: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md | quote: "Building for Windows (x86, x64 and arm64) with MSVC or clang as compilers" | type: official
- [C30] SGLang DeepGEMM 升级曾造成 sgl-kernel 接口不兼容的突发 break | src: https://github.com/sgl-project/sglang/issues/9710 | quote: "After sgl-kernel 0.3.7, DeepGEMM's JIT has been changed to C++ JIT ... not compatible with previous versions" | type: official

## conflicts
- vLLM RFC #18571（2025-06）把 encoder-decoder 模型列为"temporarily discontinued"，而当前 v1_guide 写 "Whisper is supported natively"——旧说法仍在社区流传，属已解决的冲突。
- TRT-LLM README badge 标 "Apache 2"，GitHub license API 却报 NOASSERTION/Other（LICENSE 含第三方衍生代码条款），两口径不一致。
- vLLM V1 prefix caching 官方设计文档明确 hash-based、未提 radix tree；而社区常把"prefix caching=RadixAttention"套到 vLLM 头上（待核验为误解）。

## gaps
- vLLM V1 的 gpu_memory_utilization 语义变化与多模型 OOM 抱怨（issue #18571 评论串、#14992）只拿到截断文本，未确认原句。
- SGLang 官方文档正式域名（mintlify 预览域命中）与 OS 支持矩阵（Windows/macOS）未核。
- llama.cpp 最低 CUDA compute capability 未在 build.md 写明；--embeddings flag 现状未核。
- llama.cpp 各默认值翻转（-ngl auto、-fa auto、jinja on、ctx=0）的具体 build 号未定位。
- SGLang "agentic workload" 的官方定位原句未找到强出处（仅 README 高亮条目）。

## leads
- 简报：vLLM V1 迁移坑清单——gpu_memory_utilization 语义、多模型同卡 OOM（issue #18571/#14992 评论）、CUDA graph 占显存变大、logprobs 语义四模式、prompt logprobs 禁 prefix cache。
- 简报：SGLang 每版 breaking flag 改名目录（v0.5.x 无别名改名会直接 unrecognized arguments）+ 官方文档域名与 SGL_/SGLANG_、ms→s 迁移。
- 简报：llama.cpp 默认值漂移编年——逐 build 定位 -ngl auto、-fa auto、--jinja 默认开、ctx=0、ctx_shift off 的引入版本；这是"过时教程"重灾区。
- 简报：llama.cpp 量化生态——legacy quants（Q4_0/IQ*）弃用状态、GGUF v3 与旧 GGML 文件支持、imatrix/kt-quants 现状。
- 维度：五引擎能力矩阵——多模态（vLLM VLM/SGLang VLM/TRT-LLM multimodal/llama.cpp mtmd）、embedding/rerank/pooling 端点、LoRA 热加载（vLLM multi-LoRA、llama.cpp --lora 多个+server 热换）、结构化输出后端（xgrammar/llguidance/outlines）、投机解码。
- 维度：并行/分布式命名差异——vLLM TP/PP/DP/EP/CP、SGLang DP attention+PD 分离、TRT-LLM wide-EP、llama.cpp --split-mode/RPC 多机。
- 维度：serving 生态配套——vLLM llm-d/NIXL、SGLang Model Gateway/router（新实体，gateway-v0.3.0 已独立发版）、TRT-LLM trtllm-serve+Dynamo、Ollama 与 llama.cpp 的关系。
- 维度：OS/部署矩阵——llama.cpp Windows/macOS 原生、vLLM 仅 Linux（WSL/社区 fork）、SGLang 与 TRT-LLM 的 Windows/macOS 状态待查；ARM/x86、Docker、pip 可用性。
- 简报：许可证与商用——四引擎均宽松但 TRT-LLM LICENSE 夹带第三方条款（GitHub 判 Other）；模型 license（Llama 社区协议）与引擎 license 正交，常被混淆。
- 简报：高频抱怨源量化——vLLM 冷启动/torch.compile 时长、TRT-LLM 每版 BREAKING CHANGE 密度（release-notes.md.txt 可统计）、llama.cpp 无 semver 按 build 号发布导致的"教程失效"。
- 误解候选（待核验）：「vLLM 不支持 embedding/rerank 模型」（v0.11.0 已扩 pooling/BERT NER）；「SGLang 只是 RadixAttention」；「llama.cpp 无并发 serving」（llama-server cont batching）；「TRT-LLM 闭源/只能用 TensorRT engine」。
