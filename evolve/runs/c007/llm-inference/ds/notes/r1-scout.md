# r1-scout
question: vLLM/SGLang/TRT-LLM/llama.cpp 选型常踩的坑 + 对比可能漏掉的实体/维度
checked: docs.vllm.ai/en/latest/usage/v1_guide/, docs.vllm.ai/en/latest/contributing/deprecation_policy.html, docs.vllm.ai/en/latest/features/quantization/gguf.html, github.com/vllm-project/vllm, github.com/NVIDIA/TensorRT-LLM, nvidia.github.io/TensorRT-LLM/quick-start-guide.html, nvidia.github.io/TensorRT-LLM/_sources/release-notes.md.txt, nvidia.github.io/TensorRT-LLM/latest/legacy/tensorrt-backend-removal.html, docs.sglang.io/, github.com/sgl-project/sglang, raw.githubusercontent.com/sgl-project/sglang/main/python/pyproject.toml, github.com/ggml-org/llama.cpp, github.com/ggml-org/llama.cpp/pull/13460, /pull/13012, /pull/15434, github.com/huggingface/text-generation-inference(+LICENSE)

## claims
- [C1] vLLM V0 engine 已完全废弃，V1 迁移指南列出移除特性 | src: https://docs.vllm.ai/en/latest/usage/v1_guide/ | quote: "We have fully deprecated V0. Please read RFC #18571 for more details." | type: official
- [C2] V1 移除：best_of、per-request logits processors（改为启动时全局）、GPU<>CPU KV swap、request-level structured output backend | src: https://docs.vllm.ai/en/latest/usage/v1_guide/ | quote: "best_of: This feature has been removed due to limited usage." | type: official
- [C3] V1 行为差异坑：chunked prefill 默认开启、CUDA graph 占更多显存、logprobs 语义改为 raw | src: https://docs.vllm.ai/en/latest/usage/v1_guide/ | quote: "Chunked prefill is enabled by default whenever possible, unlike in V0" ; "CUDA graph capture takes up more memory in V1 than in V0." | type: official
- [C4] vLLM 废弃政策：分阶段，绑定 minor(Y) release，patch release 不得移除 | src: https://docs.vllm.ai/en/latest/contributing/deprecation_policy.html | quote: "No Removals in Patch Releases" | type: official
- [C5] vLLM 可跑 GGUF 但高度实验性，且已迁出为独立插件 vllm-gguf-plugin | src: https://docs.vllm.ai/en/latest/features/quantization/gguf.html | quote: "GGUF support in vLLM is highly experimental and under-optimized at the moment" ; "GGUF support has migrated to OOT vllm-gguf-plugin" | type: official
- [C6] vLLM 非 NVIDIA-only：README 列 NVIDIA/AMD/Intel GPU + x86/ARM/PowerPC CPU，TPU/Gaudi/Ascend 走插件 | src: https://github.com/vllm-project/vllm | quote: "Support for NVIDIA GPUs, AMD GPUs, Intel GPUs, and x86/ARM/PowerPC CPUs." | type: official
- [C7] vLLM 许可证 Apache-2.0（仓库 sidebar） | src: https://github.com/vllm-project/vllm | quote: "Apache-2.0 license" | type: official
- [C8] TRT-LLM 1.0 起 PyTorch 成为默认后端（breaking） | src: https://nvidia.github.io/TensorRT-LLM/_sources/release-notes.md.txt | quote: "BREAKING CHANGE Promote PyTorch to be the default LLM backend" ; "Change default backend to PyTorch in trtllm-serve" | type: official
- [C9] TRT-LLM 1.2 起 TensorRT engine 后端整体移除：trtllm-build/trtllm-refit/trtllm-prune、convert_checkpoint.py、--backend tensorrt 全删，tensorrt pip 依赖移除 | src: https://nvidia.github.io/TensorRT-LLM/_sources/release-notes.md.txt | quote: "[BREAKING CHANGE] TensorRT backend removed. PyTorch is now the sole execution backend." | type: official
- [C10] 迁移后无 engine-build/checkpoint 转换步骤，HF checkpoint 直接加载 | src: https://nvidia.github.io/TensorRT-LLM/latest/legacy/tensorrt-backend-removal.html | quote: "There is no separate checkpoint-conversion or engine-build step." | type: official
- [C11] TRT-LLM 弃用只给 3 个月迁移期 | src: https://github.com/NVIDIA/TensorRT-LLM | quote: "TensorRT LLM provides a 3-month migration period after deprecation." | type: official
- [C12] TRT-LLM 仅支持 NVIDIA GPU（README 无任何非 NVIDIA 表述） | src: https://github.com/NVIDIA/TensorRT-LLM | quote: "to perform inference efficiently on NVIDIA GPUs" | type: official
- [C13] TRT-LLM 现入口为 Python LLM API + trtllm-serve（OpenAI 兼容），并经 NVIDIA Dynamo/Triton 集成 | src: https://nvidia.github.io/TensorRT-LLM/quick-start-guide.html | quote: "You can use the `trtllm-serve` command to start an OpenAI compatible server to interact with a model." | type: official
- [C14] llama.cpp 只加载 GGUF，safetensors 必须先 convert（"llama.cpp 直接跑 HF safetensors" 是误传） | src: https://github.com/ggml-org/llama.cpp/blob/fa0b8a70a8d686cd11bad1579080d546d681a53e/README.md | quote: "requires the model to be stored in the GGUF file format. Models in other data formats can be converted to GGUF using the `convert_*.py` Python scripts" | type: official
- [C15] GGUF 有文件版本 V1/V2/V3，V1 支持只到 2023-11 | src: https://github.com/ggml-org/llama.cpp/blob/6c8dcaa7/src/llama-model-loader.cpp | quote: "GGUF V1 (support until nov 2023)" ; "GGUF V3 (latest)" | type: official
- [C16] llama.cpp 多模态 breaking：PR#13460(2025-05-13) 删除 libllava 与 clip-quantize-cli；llava/gemma3/minicpmv CLI 合并为 llama-mtmd-cli（PR#13012） | src: https://github.com/ggml-org/llama.cpp/pull/13460 | quote: "mtmd : remove libllava, remove clip-quantize-cli (⚠️ breaking change)" | type: official
- [C17] llama.cpp PR#15434(2025-08-30 合并) 起 flash attention 变三态（on/off/auto，默认 auto）且默认开 FA+全量 GPU layers——旧行为假设失效 | src: https://github.com/ggml-org/llama.cpp/pull/15434 | quote: "This PR updates the llama.cpp defaults to use FlashAttention and the maximum number of GPU layers by default." | type: official
- [C18] 量化 V cache（-ctv）需要 flash_attn：FA 被强制关闭（Grok 硬编码、Vulkan runtime）时硬报错；AUTO 会自动开 | src: https://dev.to/dreamdeck/v-cache-quantization-requires-flashattn-the-llamacpp-error-that-quietly-halves-your-context-1kdb | quote: "quantized V cache requires flash_attn to be enabled" | type: secondary
- [C19] llama.cpp 常用 flag 已弃用：--mlock/--mmap→--load-mode，--defrag-thold DEPRECATED；server 未设 -np 时自动 n_parallel=4+kv_unified | src: https://manpages.debian.org/unstable/llama.cpp-tools-extra/llama-mtmd-cli.1.en.html | quote: "--mlock DEPRECATED in favor of `--load-mode`" ; "--defrag-thold N KV cache defragmentation threshold (DEPRECATED)" | type: secondary
- [C20] KV cache 类型枚举：f32,f16,bf16,q8_0,q4_0,q4_1,iq4_nl,q5_0,q5_1（-ctk/-ctv，draft 另有 -ctkd/-ctvd） | src: https://github.com/ggml-org/llama.cpp/pull/13782 | quote: "allowed values: f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1 (default: f16)" | type: official
- [C21] llama.cpp MIT 许可证；后端横跨 CUDA/HIP/Metal/Vulkan/SYCL/CANN/OpenCL/RPC 等，支持 CPU+GPU 混合 | src: https://github.com/ggml-org/llama.cpp | quote: "MIT license" ; "CPU+GPU hybrid inference to partially accelerate models larger than the total VRAM capacity" | type: official
- [C22] SGLang 依赖几乎全 exact pin：sglang-kernel==0.4.7、flashinfer_python[cu13]==0.6.18、torch==2.13.0、transformers==5.12.1、xgrammar==0.2.7，requires-python>=3.10——共享环境/自行升级 torch 易炸 | src: https://raw.githubusercontent.com/sgl-project/sglang/main/python/pyproject.toml | quote: "\"sglang-kernel==0.4.7\"" ; "\"torch==2.13.0\"" ; "\"flashinfer_python[cu13]==0.6.18\"" | type: official
- [C23] SGLang 非 NVIDIA-only：官方称覆盖 NVIDIA/AMD/Intel Xeon/TPU/Ascend NPU/MUSA | src: https://docs.sglang.io/ | quote: "Native support across ... including NVIDIA, AMD, Intel Xeon, Google TPU, Ascend NPU, and Moore Threads MUSA accelerators." | type: official
- [C24] SGLang 特性面：multi-LoRA batching、FP4/FP8/INT4/AWQ/GPTQ、spec decoding、TP/PP/EP/DP、prefill-decode 分离；Apache-2.0 | src: https://github.com/sgl-project/sglang | quote: "multi-LoRA batching" ; "quantization (FP4/FP8/INT4/AWQ/GPTQ)" ; "Apache-2.0 license" | type: official
- [C25] HF TGI 仓库 2026-03-21 已被归档只读，LICENSE 现为 Apache-2.0——选型时 TGI 已是死项目 | src: https://github.com/huggingface/text-generation-inference/blob/main/LICENSE | quote: "archived by the owner on Mar 21, 2026" | type: official

## conflicts
- TRT-LLM 旧版本化文档（mintlify 版"backends"页）仍把 TensorRT backend 标为 "Legacy - Maintained for compatibility"（https://nvidia-tensorrt-llm-50.mintlify.app/concepts/backends），而 latest 文档/1.2 release notes 称已完全移除——看旧教程/旧文档会被误导。

## gaps
- SGLang 安装页迁移：docs.sglang.ai→docs.sglang.io 301 后 /start/install.html 与 /get-started/install 均 404，安装期的 sgl-kernel/flashinfer 版本对齐警告（若有）未取到。
- vLLM V1 页面未见 VLLM_USE_V1 之类的 V0 逃生开关原句，无法确认残留回退路径。
- llama.cpp 具体哪个 build 号开始不再读 GGUF V1 / 各 backend 的 KV 量化支持差异（Metal 混合量化问题 #21450 仅 secondary 提及）。
- TRT-LLM Supported Hardware 页未取，具体 GPU arch 支持矩阵未核。
- TGI 历史上是否曾短暂改非 Apache 许可证未核（现 LICENSE 为 Apache-2.0）。

## leads
- 实体漏项：NVIDIA Dynamo（TRT-LLM README 已把它当部署入口）、llm-d、vLLM production-stack、AIBrix（K8s/PD 分离编排层）、KServe；LMDeploy、MLC-LLM、ExLlamaV3+TabbyAPI（单人量化服）；Ollama/LM Studio 等 vendored llama.cpp 版本滞后数月是真实坑源；Modular MAX（商业闭源对照项）。
- 维度漏项：许可证+项目活性（Apache-2.0×3/MIT/TGI 已归档/MAX 专有）；模型格式门槛（GGUF-only vs safetensors 直载 vs 免 build）；依赖 pin 与环境冲突（SGLang exact pin + cu13 wheel）；分布式 TP/PP/EP 与 PD 分离 + K8s 生态；LoRA；多模态（llama.cpp 走 mtmd）；structured output 后端（xgrammar/outlines/llguidance 均被 pin）；OpenAI 兼容面差异；CPU/边缘 vs 数据中心定位。
