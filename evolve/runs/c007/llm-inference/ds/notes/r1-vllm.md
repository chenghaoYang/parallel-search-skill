# r1-vllm
question: vLLM 当前（2025–2026 最新稳定版/当前文档）在 D1–D8 维度的官方事实
checked: https://docs.vllm.ai/en/latest/, https://docs.vllm.ai/en/stable/, https://docs.vllm.ai/en/latest/features/quantization/, https://docs.vllm.ai/en/latest/features/quantization/gguf.html, https://docs.vllm.ai/en/stable/features/quantization/gguf.html, https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html, https://docs.vllm.ai/en/latest/design/prefix_caching/, https://docs.vllm.ai/en/latest/features/speculative_decoding/, https://docs.vllm.ai/en/latest/features/structured_outputs.html, https://docs.vllm.ai/en/latest/features/disagg_prefill.html, https://docs.vllm.ai/en/latest/getting_started/installation/, https://docs.vllm.ai/en/latest/configuration/engine_args.html, https://docs.vllm.ai/en/latest/configuration/optimization.html, https://docs.vllm.ai/en/latest/models/supported_models.html, https://github.com/vllm-project/vllm/releases, https://github.com/vllm-project/vllm/releases/tag/v0.11.0, https://github.com/vllm-project/production-stack, https://github.com/llm-d/llm-d, https://github.com/vllm-project/vllm-neuron, https://docs.vllm.ai/en/v0.12.0/getting_started/installation/, https://raw.githubusercontent.com/vllm-project/vllm/main/vllm/config/cache.py

注：latest 文档现为 dev preview（页脚 2026-04-09）；stable 页脚 2026-06-12；GitHub 最新 release 为 v0.30.0（2026-09-22）。

## claims
- [C1] 最新 release 为 v0.30.0（2026-09-22），v0.29.0（2026-09-09）等 | src: https://github.com/vllm-project/vllm/releases | quote: "v0.30.0 (Latest) … released … September 22" | type: official
- [C2] V0 engine 已在 v0.11.0（2025-10-02）完全移除，V1 是唯一引擎 | src: https://github.com/vllm-project/vllm/releases/tag/v0.11.0 | quote: "This release completes the removal of V0 engine. … V1 is the only engine in the codebase now." | type: official
- [C3] v0.29.0 起 Model Runner V2 为所有模型默认；MRV1 计划 v0.32 移除 | src: https://github.com/vllm-project/vllm/releases | quote: "Model Runner V2 is now the default for all models … we are considering Model Runner V1 deprecated and are targeting v0.32 for its removal." | type: official
- [D1] [C4] 官方特性列 continuous batching、chunked prefill、prefix caching | src: https://docs.vllm.ai/en/latest/ | quote: "Continuous batching of incoming requests, chunked prefill, prefix caching" | type: official
- [C5] V1 中 chunked prefill 尽可能默认开启，调度优先 decode | src: https://docs.vllm.ai/en/latest/configuration/optimization.html | quote: "In V1, chunked prefill is enabled by default whenever possible." / "the scheduling policy prioritizes decode requests." | type: official
- [C6] P/D 分离：prefill/decode 跑在不同实例，connector 传 KV；明确不提升吞吐 | src: https://docs.vllm.ai/en/latest/features/disagg_prefill.html | quote: "Disaggregated prefilling put prefill and decode phase of LLM inference inside different vLLM instances." / "Disaggregated prefill DOES NOT improve throughput." | type: official
- [C7] KV connector 列 9 种：ExampleConnector、LMCacheConnectorV1(+MP)、NixlConnector、MooncakeConnector、MoRIIOConnector(仅ROCm)、MultiConnector、OffloadingConnector、FlexKVConnectorV1 | src: https://docs.vllm.ai/en/latest/features/disagg_prefill.html | quote: "Connector allows kv consumer to retrieve the KV caches of a batch of request from kv producer." | type: official
- [D2] [C8] KV 内存管理用 PagedAttention | src: https://docs.vllm.ai/en/latest/ | quote: "Efficient management of attention key and value memory with PagedAttention" | type: official
- [C9] APC 跨请求复用 KV | src: https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html | quote: "caches the KV cache of existing queries, so that a new query can directly reuse the KV cache" | type: official
- [C10] APC 实现是 hash-based（非 radix tree）：block hash → block ID 映射 + LRU 双向链 free queue；按整块 token hash | src: https://docs.vllm.ai/en/latest/design/prefix_caching/ | quote: "vLLM chooses a hash-based approach." / "we hash each kv-cache block by the tokens in the block and the tokens in the prefix before the block." / "Mapping from hash key to block IDs" | type: official
- [C11] 只缓存整块；示例 block size 16/4；LRU 逐出 | src: https://docs.vllm.ai/en/latest/design/prefix_caching/ | quote: "We only cache full blocks." / "Pop the block from the head of the free queue. This is the LRU block to be evicted" | type: official
- [C12] prefix caching 默认开启（main 分支代码） | src: https://raw.githubusercontent.com/vllm-project/vllm/main/vllm/config/cache.py | quote: "enable_prefix_caching: bool = True" | type: official
- [C13] KV offloading 分层：OffloadingConnector 可卸载到 CPU（cpu_bytes_to_use 配置），另有 FlexKV、LMCache | src: https://docs.vllm.ai/en/latest/features/disagg_prefill.html | quote: "OffloadingConnector — CPU offload configured via \"kv_connector_extra_config\":{\"block_size\": 64, \"cpu_bytes_to_use\": 1000000000}" | type: official
- [D3] [C14] 量化格式官方列表：AutoAWQ、BitsAndBytes、GPTQModel、Intel Neural Compressor、LLM Compressor(FP8 W8A8/INT4 W4A16/INT8 W4A8/INT8 W8A8)、NVIDIA Model Optimizer、Online Quantization、AMD Quark、Quantized KV Cache、TorchAO、FP8 ViT Enc Attn | src: https://docs.vllm.ai/en/latest/features/quantization/ | quote: "The following are the supported quantization formats for vLLM:" | type: official
- [C15] 首页另列 MXFP8/MXFP4、NVFP4、GGUF、compressed-tensors | src: https://docs.vllm.ai/en/stable/ | quote: "Quantization: FP8, MXFP8/MXFP4, NVFP4, INT8, INT4, GPTQ/AWQ, GGUF, compressed-tensors, ModelOpt, TorchAO" | type: official
- [C16] GGUF 支持存在但「高度实验性」，且已迁出主仓为 OOT 插件 vllm-gguf-plugin（latest 与 stable 文档一致） | src: https://docs.vllm.ai/en/latest/features/quantization/gguf.html | quote: "GGUF support in vLLM is highly experimental and under-optimized at the moment, it might be incompatible with other features" / "GGUF support has migrated to OOT vllm-gguf-plugin" | type: official
- [C17] 支持单 .gguf 文件加载与 repo_id:quant_type 形式 | src: https://docs.vllm.ai/en/latest/features/quantization/gguf.html | quote: "you can download and use a local GGUF file" （例：vllm serve ./Qwen3-0.6B-Q4_K_M.gguf --tokenizer Qwen/Qwen3-0.6B） | type: official
- [C18] GGUF 硬件表：NVIDIA Volta–Hopper + AMD GPU 支持；tokenizer 转换慢且不稳定，建议用基座模型 tokenizer | src: https://docs.vllm.ai/en/latest/features/quantization/ | quote: "GGUF – Volta→Hopper plus AMD GPU" ; src2: gguf.html | quote2: "the tokenizer conversion from GGUF is time-consuming and unstable" | type: official
- [D4] [C19] 主仓原生 GPU：NVIDIA CUDA、AMD ROCm、Intel XPU；CPU：x86、ARM AArch64、Apple silicon、IBM Z；Apple Silicon GPU 经 vLLM-Metal | src: https://docs.vllm.ai/en/latest/getting_started/installation/ | quote: "vLLM supports the following hardware platforms" (GPU: CUDA/ROCm/XPU/Apple Silicon via vLLM-Metal) | type: official
- [C20] 其余加速器均为仓外插件 | src: https://docs.vllm.ai/en/latest/getting_started/installation/ | quote: "vLLM supports third-party hardware plugins that live outside the main vllm repository." | type: official
- [C21] 插件表（v0.12.0 文档）：Google TPU=tpu-inference、Ascend=vllm-ascend、Intel Gaudi=vllm-gaudi、MetaX=vLLM-metax、Rebellions=vllm-rbln、IBM Spyre=vllm-spyre、Cambricon=vllm-mlu | src: https://docs.vllm.ai/en/v0.12.0/getting_started/installation/ | quote: "The backends below live outside the main vllm repository and follow the Hardware-Pluggable RFC." | type: official
- [C22] AWS Neuron 为社区维护插件 vllm-neuron，Beta | src: https://github.com/vllm-project/vllm-neuron | quote: "Community maintained hardware plugin for vLLM on AWS Neuron … vLLM Neuron Plugin (Beta) … the recommended serving solution for large language models on AWS Trainium" | type: official
- [D5] [C23] 结构化输出后端为 xgrammar 或 guidance | src: https://docs.vllm.ai/en/latest/features/structured_outputs.html | quote: "vLLM supports the generation of structured outputs using xgrammar or guidance as backends" | type: official
- [C24] 默认后端 auto | src: https://docs.vllm.ai/en/latest/features/structured_outputs.html | quote: "The default backend is auto, which will try to choose an appropriate backend based on the details of the request." | type: official
- [C25] guided_decoding_backend 字段 v0.12.0 移除；改 --structured-outputs-config.backend | src: https://docs.vllm.ai/en/latest/features/structured_outputs.html | quote: "guided_decoding_backend -> Remove this field from your request" | type: official
- [D6] [C26] spec decode 方法：EAGLE、MTP、draft model、PARD、MLP speculator、n-gram、suffix、custom proposer(experimental)、dynamic、adaptive verification(DSpark) | src: https://docs.vllm.ai/en/latest/features/speculative_decoding/ | quote: "Model-based methods such as EAGLE, MTP, draft models, PARD and MLP provide the best latency reduction" | type: official
- [C27] method 取值 | src: https://docs.vllm.ai/en/latest/features/speculative_decoding/ | quote: "Common values include `draft_model`, `ngram`, `suffix`, `mtp`, `eagle3`, and `dflash`"（另有 custom_class experimental） | type: official
- [C28] Medusa 未出现在该页（两次定向核查均无）；首页列 "n-gram, suffix, EAGLE, DFlash" | src: https://docs.vllm.ai/en/latest/features/speculative_decoding/ | quote: 页面无 "Medusa" 字样 | type: official
- [D7] [C29] `vllm serve` 提供 OpenAI 兼容 + Anthropic Messages + gRPC；离线 LLM API | src: https://docs.vllm.ai/en/latest/ | quote: "OpenAI-compatible API server, plus Anthropic Messages API and gRPC support" | type: official
- [C30] Production Stack：K8s 参考部署（Helm：serving engine+router+Prometheus/Grafana） | src: https://github.com/vllm-project/production-stack | quote: "vLLM's reference system for K8S-native cluster-wide deployment" / "Directs requests to appropriate backends based on routing keys or session IDs to maximize KV cache reuse" | type: official
- [C31] llm-d：CNCF sandbox 分布式推理栈，用 P/D 分离 + wide EP + prefix-cache 感知路由 + KV 分层卸载；vLLM/SGLang 作 model server；v0.7（2026-05） | src: https://github.com/llm-d/llm-d | quote: "a high-performance distributed inference serving stack optimized for production deployments on Kubernetes" | type: official
- [D8] [C32] 支持 200+ HF 架构；MoE、hybrid/state-space、多模态、embedding、reward | src: https://docs.vllm.ai/en/latest/ | quote: "vLLM seamlessly supports 200+ model architectures on HuggingFace" | type: official
- [C33] 默认从 HF Hub 加载，按 config.json architectures 字段判定支持 | src: https://docs.vllm.ai/en/latest/models/supported_models.html | quote: "If the \"architectures\" field contains a model architecture listed below, then it should be natively supported." | type: official
- [C34] DeepSeek 原生架构：DeepseekV3ForCausalLM(V3/R1/V3.1)、DeepseekV32ForCausalLM(V3.2)、DeepseekV4ForCausalLM(V4-Flash/Pro) 及多模态变体 | src: https://docs.vllm.ai/en/latest/models/supported_models.html | quote: "Native architectures include DeepseekForCausalLM, DeepseekV2ForCausalLM, DeepseekV3ForCausalLM … DeepseekV32ForCausalLM (V3.2), and DeepseekV4ForCausalLM (V4-Flash/Pro)." | type: official

## conflicts
- GGUF 定位矛盾：首页与硬件兼容表把 GGUF 列为受支持量化格式，但 quantization 索引页的「supported formats」列表不含 GGUF，GGUF 专页称其已迁至仓外 vllm-gguf-plugin 且 "highly experimental"。（两处 URL 见 C15/C16）
- 文档版本漂移：latest 为 dev preview（Apr 2026 页脚）、stable 页脚 Jun 2026，而代码已到 v0.30.0（Sep 2026）；插件表取自 v0.12.0 版文档，latest 页仅指向 vllm.ai 网站列表。

## gaps
- Medusa 是否被正式移除/未移植 V1：spec decode 页无，未查 release notes 逐版确认。
- enable_prefix_caching=True 默认值按 main 分支源码；stable 版默认值未逐版核；个别硬件/模型可能默认关。
- --structured-outputs-config.backend 的允许取值页面未枚举。
- Intel XPU、CPU 后端的成熟度分级文档未标注 experimental/production。
- bitsandbytes/NVFP4 等单页细节未逐一核查。

## leads
- Model Runner V2（v0.29 默认、v0.32 将移除 MRV1）是 V0/V1 叙事之后的新引擎轴。
- DFlash 投机解码为新方法；PARD/MLP speculator 为新列项。
- vllm-gguf-plugin 仓库可查 GGUF 量化类型覆盖范围。
