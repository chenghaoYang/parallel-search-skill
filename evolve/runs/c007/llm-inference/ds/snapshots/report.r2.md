# vLLM / SGLang / TensorRT-LLM / llama.cpp：四个 LLM 推理引擎现在的差别

> 截至 2026-09（vLLM v0.30 / TRT-LLM 1.3.0rc / llama.cpp b11170）。

## 0. 一屏看懂

- **「llama.cpp 只能跑 CPU」已过时**：README 列 16 后端（CUDA/HIP/Metal/Vulkan/SYCL…）[17]。
- **「vLLM 不支持 GGUF」半过时**：能跑单 .gguf 文件，但已迁出主仓为 OOT 插件 `vllm-gguf-plugin`（仅 CUDA/ROCm），官方称 "highly experimental and under-optimized" [5][52]。
- **「TRT-LLM 先编译 engine 再跑」已过时**：v1.0 起 PyTorch 为默认后端，v1.2 删除整个 TensorRT 后端（trtllm-build/convert_checkpoint 全废），HF checkpoint 直载 [11][12]。
- **vLLM prefix caching ≠ SGLang RadixAttention**：目标相同（跨请求复用前缀 KV），数据结构不同——vLLM 是整块 hash 表+LRU [4]，SGLang 是 token 粒度 radix tree+LRU 逐叶 [9]；TRT-LLM 也用 radix search tree [14]，反更接近 SGLang。
- 三家 serving 引擎机制已趋同（continuous batching、chunked prefill、分页 KV、PD 分离、xgrammar、EAGLE3 类投机），分化点在**硬件覆盖**与**生态位**：TRT-LLM 仅 NVIDIA [15]；vLLM 主仓 CUDA/ROCm/XPU/CPU、其余加速器走插件 [7]；SGLang 覆盖 NVIDIA/AMD/Xeon/TPU/Ascend [8]。
- Ollama 不再等于 llama.cpp：2025-05 起有自有 Go+GGML 引擎，2026-03 起 Apple silicon 走 MLX 引擎，llama.cpp 退居 GGUF 兼容层 [19][20]。
- TGI 已归档（已只读），HF 官方推荐迁往 vLLM/SGLang/llama.cpp/MLX [22]。

## 1. Taxonomy

分类轴：运行基底 × 目标场景 × 模型工件。

- **PyTorch 数据中心引擎**：vLLM、SGLang、TRT-LLM——PyTorch 动态图 + HF safetensors 直载，竞争点是集群吞吐与分布式编排。
- **自包含本地运行时**：llama.cpp——C/C++ 库（libllama 是主产物 [18]）+ GGUF 专属格式，竞争点是跨硬件便携与低资源。
- **编排层（不是引擎）**：Dynamo、llm-d——架在引擎之上做多节点 PD 分离/路由 [23][24]。

许可证：vLLM/SGLang/TRT-LLM 为 Apache-2.0，llama.cpp 为 MIT [54][8][55][17]。

维度：D1 调度吞吐 / D2 KV 与前缀复用 / D3 量化 / D4 硬件 / D5 结构化输出 / D6 投机解码 / D7 部署形态 / D8 覆盖。

## 2. 对照矩阵

### D1 调度与吞吐

| | continuous batching | chunked prefill | PD 分离 |
|---|---|---|---|
| vLLM | ✅；V1 调度优先 decode [1][2] | 默认尽可能开 [2] | ✅ 9 种 KV connector（NIXL/Mooncake/LMCache…）；官方注明不提升吞吐 [3] |
| SGLang | ✅ [8] | `--chunked-prefill-size`，-1 关 [25] | ✅ Mooncake/NIXL 传输+router [10] |
| TRT-LLM | ✅ 官方名 in-flight batching [13] | chunked context，需 FMHA paged KV [13] | ✅ Disaggregated Serving，NIXL，ctx/gen 双服务 [16] |
| llama.cpp | ✅ `--cont-batching` 默认开；`--parallel` 多 slot [26] | 无同名 flag；共享 batch 内按 `--ubatch-size`(512) 分块 [27] | ∅ 未合入（issue #21266 open）[28] |

### D2 KV cache 与前缀复用

| | 机制 | 结构/粒度 | 分层 |
|---|---|---|---|
| vLLM | PagedAttention + Automatic Prefix Caching | 整块 hash→block ID + LRU free queue，只存整块 [4] | OffloadingConnector/LMCache/FlexKV 卸 CPU [3] |
| SGLang | RadixAttention | radix tree，token 粒度 page+LRU 逐叶子；`lpm` 调度促命中 [9][29] | HiCache：GPU L1/host L2/L3（Mooncake/3FS/NIXL）[30] |
| TRT-LLM | paged KV + block reuse | radix search tree+prioritized LRU，partial reuse 默认开 [14] | host_cache_size 卸 host [14] |
| llama.cpp | prompt caching（`--cache-prompt` 默认开） | 最长公共前缀 + `--cache-reuse` KV shifting；slot 相似度阈值 | `--slot-save-path` 落盘；`-ctk/-ctv` KV 量化 [26] |

### D3–D6 速查

| | D3 量化 | D4 硬件 | D5 结构化输出 | D6 投机解码 |
|---|---|---|---|---|
| vLLM | AWQ/GPTQ/FP8/INT4/NVFP4/compressed-tensors/bnb… [6]；GGUF 仅实验插件 [5] | CUDA/ROCm/XPU/CPU 主仓；TPU/Ascend/Gaudi 插件 [7] | xgrammar 或 guidance，默认 auto [31] | eagle3/medusa/mtp/draft_model/ngram/suffix/dflash…（`--spec-method` 枚举）[32][53] |
| SGLang | fp8/awq(_marlin)/gptq_marlin/mxfp4/nvfp4/modelopt/gguf(NVIDIA+Ascend)… [33] | NVIDIA/AMD/Xeon/TPU/Ascend/Jetson/Metal [8] | JSON schema/regex/EBNF；XGrammar 默认，另 Outlines/llguidance [34] | EAGLE3(荐)/EAGLE/NEXTN/STANDALONE/NGRAM/DFLASH；MTP 经此 [35] |
| TRT-LLM | NVFP4/MXFP4/FP8 多粒度/W4A16+W4A8 GPTQ+AWQ，按 SM 受限 [36] | 仅 NVIDIA（Ampere→Blackwell）[15] | XGrammar / LLGuidance [37] | MTP/Eagle3(EAGLE 家族仅此；`Eagle` 为别名)/NGram/DraftTarget/PARD/DFlash/SA [38] |
| llama.cpp | 仅 GGUF：K/I/TQ quants+imatrix；不读 safetensors（PR#17580 被拒）[39] | 16 后端+CPU/GPU 混合推理 [17] | GBNF 语法+JSON schema 子集+Jinja [40] | `--model-draft`+`--spec-type`：eagle3/mtp/dflash/ngram 系 10 种 [41] |

### D7 部署形态 / D8 覆盖

- vLLM：`vllm serve`（OpenAI+Anthropic Messages+gRPC）、离线 LLM API；K8s 走 Production Stack / llm-d；200+ HF 架构 [1][42][24]。
- SGLang：`sglang.launch_server` OpenAI 兼容；Model Gateway（Rust，cache_aware 默认）路由+PD 负载；可作 Dynamo 后端；K8s 用 LWS；另有前端 DSL [10][43][23]。
- TRT-LLM：`trtllm-serve` OpenAI 兼容 + Python LLM API；Triton backend 已并入主仓；Dynamo 为其分布式编排层 [44][45]。
- llama.cpp：libllama 为主产物；`llama-server` OpenAI+Anthropic 兼容+web UI+多模型 router；`-hf` 拉 HF GGUF [18][26]。

## 3. 周边关系

- **Ollama**：多引擎——自有 Go+GGML 引擎（2025-05）、Apple silicon MLX 引擎（2026-03 preview）、llama.cpp 只做 GGUF 兼容（0.30 起）[19][20][21]；与 vLLM 无集成。
- **MLX / mlx-lm**：Apple 官方框架，独立生态，只读 safetensors MLX 格式 [46]。
- **TGI**：已归档只读，HF 推荐迁往 vLLM/SGLang/llama.cpp/MLX [22]。
- **Dynamo / llm-d**：编排层，Dynamo 编排三家引擎，llm-d 是 vLLM 之上的 K8s 栈 [23][24]。

## 4. 坑

- **TRT-LLM 老教程全死**：1.2 删 engine 后端与 trtllm-build/convert_checkpoint；弃用只给 3 个月迁移期 [12][47]。
- **vLLM V0→V1 行为差**：V0 完全移除；best_of/逐请求 logits processor/KV swap 没了；chunked prefill 默认开、CUDA graph 更吃显存、logprobs 语义变 [48]。
- **llama.cpp 默认值漂移**：FA 默认 auto+全量 GPU offload（PR#15434）；量化 V cache 需 FA，强关即报错；llava→mtmd 是 breaking（PR#13460）[49][50]。
- **SGLang 依赖全 exact pin**：torch/transformers/flashinfer/xgrammar 钉死，共享环境易炸 [51]。
- **vLLM GGUF 勿上生产**：实验性 OOT 插件，tokenizer 转换慢不稳，建议用基座 tokenizer [5]。

## 5. 未决与置信度

- TRT-LLM spec 页 "PyTorch backend supports only Eagle3" 实指 EAGLE 家族（v1/v2 checkpoint 不兼容），非限制全部 spec 类型 [38]。v1.0.0 日期 2025-09-24（取自 GitHub API）[11]。
- Medusa/lookahead/SmoothQuant 在 1.x release notes 无移除条目——随 TRT 后端消失；vLLM 的 medusa 仍在 `--spec-method` 枚举中，仅无独立文档页 [12][53]。
- SGLang radix cache 默认开仅间接证据；llama.cpp 无 "chunked prefill" 命名特性（实为 ubatch 分块）、llguidance 后端文档未核。
- 时效风险：docs.vllm.ai latest 为 dev preview；旧版 TRT-LLM mintlify 文档仍标 TensorRT 后端 "Legacy"。

## 来源

[1] https://docs.vllm.ai/en/latest/
[2] https://docs.vllm.ai/en/latest/configuration/optimization.html
[3] https://docs.vllm.ai/en/latest/features/disagg_prefill.html
[4] https://docs.vllm.ai/en/latest/design/prefix_caching/
[5] https://docs.vllm.ai/en/latest/features/quantization/gguf.html
[6] https://docs.vllm.ai/en/latest/features/quantization/
[7] https://docs.vllm.ai/en/latest/getting_started/installation/
[8] https://github.com/sgl-project/sglang
[9] https://lmsys.org/blog/2024-01-17-sglang/
[10] https://docs.sglang.io/docs/advanced_features/pd_disaggregation.md
[11] https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0
[12] https://nvidia.github.io/TensorRT-LLM/latest/release-notes.html
[13] https://nvidia.github.io/TensorRT-LLM/features/paged-attention-ifb-scheduler.html
[14] https://nvidia.github.io/TensorRT-LLM/features/kvcache.html
[15] https://nvidia.github.io/TensorRT-LLM/supported-hardware.html
[16] https://nvidia.github.io/TensorRT-LLM/features/disagg-serving.html
[17] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/README.md
[18] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/docs/build.md
[19] https://ollama.com/blog/multimodal-models
[20] https://ollama.com/blog/mlx
[21] https://ollama.com/blog/improved-performance-and-model-support-with-gguf
[22] https://github.com/huggingface/text-generation-inference
[23] https://github.com/ai-dynamo/dynamo
[24] https://github.com/llm-d/llm-d
[25] https://docs.sglang.io/docs/advanced_features/server_arguments.md
[26] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md
[27] https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README-dev.md
[28] https://github.com/ggml-org/llama.cpp/issues/21266
[29] https://docs.sglang.io/docs/advanced_features/radix_eviction_policy.md
[30] https://docs.sglang.io/docs/advanced_features/hicache_design.md
[31] https://docs.vllm.ai/en/latest/features/structured_outputs.html
[32] https://docs.vllm.ai/en/latest/features/speculative_decoding/
[33] https://docs.sglang.io/docs/advanced_features/quantization.md
[34] https://docs.sglang.io/docs/advanced_features/structured_outputs.md
[35] https://docs.sglang.io/docs/advanced_features/speculative_decoding.md
[36] https://nvidia.github.io/TensorRT-LLM/features/quantization.html
[37] https://nvidia.github.io/TensorRT-LLM/features/guided-decoding.html
[38] https://nvidia.github.io/TensorRT-LLM/features/speculative-decoding.html
[39] https://github.com/ggml-org/llama.cpp/pull/17580
[40] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md
[41] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/docs/speculative.md
[42] https://github.com/vllm-project/production-stack
[43] https://docs.sglang.io/docs/advanced_features/sgl_model_gateway.md
[44] https://nvidia.github.io/TensorRT-LLM/quick-start-guide.html
[45] https://github.com/triton-inference-server/tensorrtllm_backend
[46] https://github.com/ml-explore/mlx-lm
[47] https://github.com/NVIDIA/TensorRT-LLM
[48] https://docs.vllm.ai/en/latest/usage/v1_guide/
[49] https://github.com/ggml-org/llama.cpp/pull/15434
[50] https://github.com/ggml-org/llama.cpp/pull/13460
[51] https://raw.githubusercontent.com/sgl-project/sglang/main/python/pyproject.toml
[52] https://raw.githubusercontent.com/vllm-project/vllm-gguf-plugin/main/README.md
[53] https://docs.vllm.ai/en/latest/configuration/engine_args/
[54] https://github.com/vllm-project/vllm
[55] https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/LICENSE
