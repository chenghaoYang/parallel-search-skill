# r1-trtllm
question: TensorRT-LLM 当前版（docs commit fca831e, 更新 2026-09-21, 分支 1.3.0rc）D1–D8 官方事实 + 「编译成 TensorRT engine」是否仍成立
checked: github.com/NVIDIA/TensorRT-LLM, nvidia.github.io/TensorRT-LLM/ (+ features/quantization, speculative-decoding, disagg-serving, kvcache, guided-decoding, paged-attention-ifb-scheduler, supported-hardware, models/supported-models, legacy/tensorrt-backend-removal, llm-api/index, latest/release-notes), github releases/tag/v1.0.0 + ?page=2, github.com/triton-inference-server/tensorrtllm_backend

## claims
- [C1] 关键疑点结论：TRT engine 编译流程已移除。v1.0 起 PyTorch 为默认稳定后端："the PyTorch-based architecture is now stable and the default experience"；"BREAKING CHANGE Promote PyTorch to be the default LLM backend"；"Change default backend to PyTorch in trtllm-serve" | src: https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0 | quote: "TensorRT LLM 1.0 brings 2 major changes: the PyTorch-based architecture is now stable and the default experience, and the LLM API is now stable." | type: official
- [C2] Release 1.2 彻底移除 TensorRT 后端：trtllm-build/trtllm-refit/trtllm-prune CLI、`--backend tensorrt`、convert_checkpoint.py 全删，tensorrt pip 依赖不再安装 | src: https://nvidia.github.io/TensorRT-LLM/latest/release-notes.html | quote: "[BREAKING CHANGE] TensorRT backend removed. PyTorch is now the sole execution backend. `LLM(backend=\"tensorrt\")` now raises a `ValueError`" | type: official
- [C3] 迁移指南确认无 engine-build 步骤 | src: https://nvidia.github.io/TensorRT-LLM/legacy/tensorrt-backend-removal.html | quote: "No engine-build step — HuggingFace checkpoints load directly"; "`--backend pytorch` is the default, so no engine is needed" | type: official
- [C4] README 定位：PyTorch 原生架构 | src: https://github.com/NVIDIA/TensorRT-LLM | quote: "Architected on PyTorch, TensorRT LLM provides a high-level Python LLM API" | type: official
- [C5] D1 调度官方名 in-flight batching = continuous batching | src: https://nvidia.github.io/TensorRT-LLM/features/paged-attention-ifb-scheduler.html | quote: "in-flight batching of requests (also known as continuous batching or iteration-level batching)" | type: official
- [C6] chunked context（即 chunked prefill）把 context 切块与 decode 同批；需开 FMHA paged KV cache；非末块须为 KV block size 整数倍 | src: 同 C5 | quote: "this feature splits the context into several chunks"; "the FMHA paged kv-cache also needs to be enabled" | type: official
- [C7] 分离式服务官方名 "Disaggregated Serving"："Disaggregated LLM serving, in which the context and generation phases are run on different GPUs"；KV 传输用 NIXL backend（cache_transceiver_config），trtllm-serve 起 ctx/gen 双服务 + disaggregated orchestrator | src: https://nvidia.github.io/TensorRT-LLM/features/disagg-serving.html | type: official
- [C8] 另有 Overlap Scheduler 特性页（features/overlap-scheduler.html）；1.0rc2 notes："overlap scheduler support to overlap prepare inputs and model forward" | src: https://nvidia.github.io/TensorRT-LLM/ | type: official
- [C9] paged KV cache："The paged KV cache decomposes the KV cache into blocks that are distributed to the different requests by a cache manager"；块为"a pool of blocks that can hold KV state for a fixed number of tokens"，token 数须为 >1 的 2 的幂 | src: https://nvidia.github.io/TensorRT-LLM/features/paged-attention-ifb-scheduler.html ; https://nvidia.github.io/TensorRT-LLM/features/kvcache.html | type: official
- [C10] 前缀复用：填满的块存入 radix search tree 供后续请求复用；enable_block_reuse 与 enable_partial_reuse 默认开 | src: https://nvidia.github.io/TensorRT-LLM/features/kvcache.html | quote: "Blocks containing KV state computed for previous requests are stored in a radix search tree as soon as they are filled." | type: official
- [C11] 淘汰策略 prioritized LRU："The core eviction scheme is prioritized LRU"；优先级 0–100；可 host 内存 offload（host_cache_size）| src: 同 C10 | type: official
- [C12] D3 量化清单：NVFP4、MXFP4、FP8 per-tensor / block-scaling / rowwise / KV-cache、W4A16+W4A8 GPTQ、W4A16+W4A8 AWQ | src: https://nvidia.github.io/TensorRT-LLM/features/quantization.html | quote: "The default PyTorch backend supports FP4 and FP8 quantization on the latest Blackwell and Hopper GPUs." | type: official
- [C13] 量化按架构受限：Hopper 无 NVFP4/MXFP4；sm120（消费级 Blackwell）仅 NVFP4/MXFP4/FP8 per-tensor/FP8 KV；Ampere 仅 FP8 KV + W4A16 AWQ/GPTQ；NVFP4 KV 需配 FP8 权重且经 ModelOpt 离线量化 | src: 同 C12 | type: official
- [C14] D4 硬件仅 NVIDIA："TensorRT LLM supports the full spectrum of NVIDIA GPU architectures:" Blackwell B200/GB200/B300/GB300/DGX Spark；Hopper H100/H200/GH200；Ada L20/L40/L40S；Ampere A100。该页未提任何非 NVIDIA 硬件（已直接核对）| src: https://nvidia.github.io/TensorRT-LLM/supported-hardware.html | type: official
- [C15] D5 guided decoding 两后端："TensorRT LLM supports two grammar backends:" XGrammar（JSON schema/regex/EBNF/structural tag）与 LLGuidance（JSON schema/regex/EBNF）；"Structural tag is supported by `xgrammar` backend only." 线上 trtllm-serve 用 guided_decoding_backend+response_format，线下 GuidedDecodingParams(json=…) | src: https://nvidia.github.io/TensorRT-LLM/features/guided-decoding.html | type: official
- [C16] D6 投机解码 decoding_type：MTP、Eagle3、NGram、DraftTarget、PARD、DFlash（含 DFlash 2）、SA（Suffix Automaton，可作 enhancer）、UserProvidedDecodingConfig | src: https://nvidia.github.io/TensorRT-LLM/features/speculative-decoding.html | type: official
- [C17] Medusa 与 lookahead 在当前 spec-decoding 特性页全文不存在（已二次直问核对）；历史 notes 曾有 "seamless lookahead decoding"（pre-1.0 条目）与 Medusa（TRT 时代）| src: 同 C16 ; https://nvidia.github.io/TensorRT-LLM/1.0.0rc2/release-notes.html | type: official
- [C18] D7：trtllm-serve = OpenAI 兼容 serving CLI（另有 trtllm-bench/trtllm-eval）；Triton backend 源码已迁入主仓 triton_backend/ 目录，容器 nvcr.io/nvidia/tritonserver:25.12-trtllm-python-py3 | src: https://github.com/triton-inference-server/tensorrtllm_backend | quote: "the Triton backend source code and test have been moved to TensorRT-LLM" | type: official
- [C19] Dynamo 关系 | src: https://github.com/NVIDIA/TensorRT-LLM | quote: "A datacenter scale distributed inference serving framework that works seamlessly with TensorRT LLM." | type: official
- [C20] LLM API："a high-level Python API…uses a PyTorch-native and modular backend"，入口 LLM/AsyncLLM；Python API 索引无 Executor 类（C++ executor API 仍在 1.2 release notes 中被提及）| src: https://nvidia.github.io/TensorRT-LLM/llm-api/index.html | type: official
- [C21] D8 模型覆盖（PyTorch backend 矩阵）：Llama/Llama4、Qwen2/3/3-MoE/3Next/3.5-MoE、Gemma3/4、GLM-4.5~4.7/GLM-5.x、GPT-OSS、Phi-4、Mistral/Mixtral、Nemotron、Kimi K2/K3、MiniMax M2/M3、Hunyuan、EXAONE、Granite、Seed-OSS 等；编码-解码含 T5/BART/Whisper | src: https://nvidia.github.io/TensorRT-LLM/models/supported-models.html | type: official
- [C22] MoE 与多模态均有专门矩阵（VILA、LlavaNext、Qwen2/2.5/3-VL、Gemma3/4、Llama4、Mistral3、Phi4MM、MiniCPM 等）；视觉生成 Beta：FLUX.1/2、Wan 2.1/2.2、Qwen-Image、Cosmos3 | src: 同 C21 | type: official
- [C23] DeepSeek：V2/V3(+Kimi-K2)/V3.2/V4 架构在列；"DeepSeek-V4 is only supported on Blackwell GPUs (`SM100+`)"；README 提 DeepSeek FP4 | src: 同 C21 | type: official
- [C24] 版本基线：docs "Last updated on September 21, 2026", commit fca831e；README badge 1.3.0rc29；v1.3.0rc28 发布于 2026-09-23；release notes 注明 "as of TensorRT-LLM 1.3 (2026-09)"；v1.3.0rc28 另 "Remove deprecated TensorRT serve, evaluation, benchmark, and stress paths (BREAKING)" | src: https://nvidia.github.io/TensorRT-LLM/ ; https://github.com/NVIDIA/TensorRT-LLM/releases | type: official

## conflicts
- spec-decoding 页列出 MTP/NGram/DraftTarget/PARD/DFlash/SA 等多种 decoding_type，但同页有句 "The PyTorch backend supports only `Eagle3`"（语境不明，疑为某小节限定）；未裁决，列为存疑句。
- v1.0.0 release notes 同时含 "Add TensorRT-Engine Qwen3 (dense) model support"、"Add Qwen3 MoE support to TensorRT backend"——即 1.0 时 PyTorch 为默认但 TRT 后端仍在加新模型，直至 1.2 才整体移除（非矛盾，是时间线）。

## gaps
- v1.0.0 精确发布日期：GitHub tag 页只显示相对日期 "24 Sep"（依赖项 PyTorch 25.06/transformers 4.53 指向 2025 年中），年份未在页面上确认。
- SmoothQuant / INT8：当前量化矩阵未列出（页面仅描述性提及 INT8）；旧版曾有 SmoothQuant，何时移除未定位到具体 release 条目。
- Executor API：Python 索引无 Executor 类；C++ executor API 现状（是否仍公开支持）未查专门文档页。
- Medusa/lookahead 被移除的具体 release 版本未定位。

## leads
- AutoDeploy (Beta)：基于 PyTorch backend 的自动部署/编译路径（features/auto_deploy/），可视为 engine-build 的替代物。
- Wide Expert Parallelism (wide-EP)、Helix parallelism、sparse attention（Rocket/DeepSeek sparse）——D1–D8 之外的新特性轴。
- Triton backend 在 1.0 后走 LLM API + PyTorch（"Remove support for llmapi + TRT backend in Triton"）。
