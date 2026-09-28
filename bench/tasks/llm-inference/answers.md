# llm-inference 任务参考答案

给人工检查者用的简明答案，对应 task.md 里用户提出的疑问。核实日期：2026-09-24。

## 1. "llama.cpp 只能跑 CPU" —— 现在还是这样吗？

**不是，这是误解。** llama.cpp 的默认构建确实是可移植 CPU 版（这大概是误解来源），但它有一整套 GPU/加速器后端：NVIDIA 走 CUDA（`-DGGML_CUDA=ON`）、AMD 走 HIP/ROCm（`-DGGML_HIP=ON`）、跨厂商走 Vulkan（`-DGGML_VULKAN=ON`）、Intel 走 SYCL；macOS 上 Metal 默认启用（"On MacOS, Metal is enabled by default"）。GPU 支持是"层卸载"模式，用 `-ngl`/`--n-gpu-layers` 控制放多少层到 GPU；要完全禁用 GPU 用 `--device none`（`-ngl 0` 不保证零 GPU 计算）。
来源：https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md

## 2. "vLLM 不支持 GGUF" —— 现在还是这样吗？

**半对。** vLLM 现在能跑 GGUF，但已从主线迁到独立插件 `vllm-gguf-plugin`，官方原话是 "highly experimental and under-optimized"，可能与其他特性冲突。典型用法 `vllm serve unsloth/Qwen3-0.6B-GGUF:Q4_K_M --tokenizer Qwen/Qwen3-0.6B`（官方建议 tokenizer 用原始 HF 模型的）。结论：GGUF 在 vLLM 里是实验性次要路径，生产 GPU 服务仍应选 AWQ/GPTQ/FP8 等成熟量化；GGUF 的主场是 llama.cpp（要求模型必须是 GGUF，其他格式用 `convert_*.py` 转换）。SGLang 侧：量化文档的兼容性表已把 `gguf` 标为 NVIDIA/Ascend 可用，但在线量化列表里仍写着"will soon support"，稳妥说法是其 GGUF 支持不如 llama.cpp 成熟。
来源：https://docs.vllm.ai/en/latest/features/quantization/gguf/ ；https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md ；https://docs.sglang.io/docs/advanced_features/quantization.md

## 3. "TensorRT-LLM 是先把模型编译成 TensorRT engine 再跑" —— 现在还是这样吗？

**已经过时。** TensorRT-LLM 1.0 把 PyTorch 架构转正为默认；1.2 直接删除了 TensorRT 后端——官方原话 "PyTorch is now the sole execution backend"，`LLM(backend="tensorrt")` 会抛 ValueError，`trtllm-build`/`trtllm-refit`/`trtllm-prune`、逐模型的 `convert_checkpoint.py`、`tensorrt` pip 依赖全部移除。现在的部署形态是 `trtllm-serve` + PyTorch 工作流。它仍是 NVIDIA-only（"inference efficiently on NVIDIA GPUs"），不像 vLLM 有 ROCm/XPU/CPU/Apple Silicon 插件路径。Windows 支持在 0.18.0 已弃用。
来源：https://nvidia.github.io/TensorRT-LLM/release-notes.html ；https://github.com/NVIDIA/TensorRT-LLM

## 4. "vLLM 和 SGLang 的前缀缓存是一回事" —— 对吗？

**目标相同、机制不同。** 两者都做跨请求的前缀 KV 复用，但索引结构不一样：

- **vLLM（Automatic Prefix Caching）**：按"链式 block 哈希"存全局哈希表，官方明确 "We only cache full blocks"——前缀尾部不满一个 block 的部分要重算。V1 时代已默认开启（`enable_prefix_caching: bool = True`），还支持 `cache_salt` 做租户隔离。
- **SGLang（RadixAttention）**：用 radix tree 直接按 token 序列做最长前缀匹配，分叉（branch）是一等公民——同一系统 prompt 派生出的多轮对话/agent 轨迹天然共享树干。官方定义 "a novel technique for automatic KV cache reuse during runtime"。

粗略记法：vLLM 是 block 哈希复用，SGLang 是树索引最长前缀复用；分支多、前缀层级深的负载（多轮、agent、共享文档多问）里 RadixAttention 结构更占优。
来源：https://docs.vllm.ai/en/latest/design/prefix_caching/ ；https://lmsys.org/blog/2024-01-17-sglang/ ；https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py

## 5. 调度与吞吐：continuous batching 和 PD 分离各家什么状态？

- **四家都有 continuous batching**——包括 llama.cpp 的 `llama-server`（`--cont-batching` 默认 enabled，`--parallel N` 控槽位），不是只能串行。但 llama-server 的 KV 池是所有槽位共享的总预算（`--ctx-size`），高并发/长上下文下效率和尾延迟明显不如 vLLM 的 PagedAttention 调度；Red Hat 的对比测试里 64 并发时 vLLM 吞吐约为 llama.cpp 的 44 倍（注意：单一负载的数字，不能当普遍比例）。
- **vLLM**：continuous batching + chunked prefill 是 V1 核心；disaggregated prefill 官方支持但标为实验特性，prefill/decode 两个实例间用 `NixlConnector`（`--kv-transfer-config`，kv_role=kv_producer/kv_consumer）异步传 KV。
- **SGLang**：PD 分离是主打能力，prefill/decode 跑在不同进程，KV 传输引擎支持 Mooncake 和 NIXL；decode 侧 radix cache 还能让 prefill 只补 delta KV（agent 场景省重复 prefill）。
- **TensorRT-LLM**：也有 disaggregated serving 路径，但 NVIDIA-only。
来源：https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md ；https://docs.vllm.ai/en/latest/features/disagg_prefill/ ；https://docs.sglang.io/advanced_features/pd_disaggregation.html ；https://developers.redhat.com/articles/2026/06/15/llamacpp-vs-vllm-choosing-right-local-llm-inference-engine

## 6. 量化、结构化输出、投机解码的差异

- **量化**：llama.cpp = GGUF（Q4_K_M 等 K-quants/IQ-quants 最全）；vLLM/SGLang 主打 HF 格式的 AWQ/GPTQ/FP8/NVFP4 等 GPU 量化，SGLang 官方建议离线量化优于在线量化，已量化模型不要叠加 `--quantization`。
- **结构化输出**：vLLM 用 `structured_outputs`（json/regex/choice/grammar/structural_tag），xgrammar/guidance 后端，旧 `guided_*` 字段 v0.12.0 已移除；SGLang 用 `--grammar-backend`（xgrammar 等）。注意有未修的公开 bug：SGLang 上 EAGLE 投机解码 + JSON/regex 约束可能挂住/截断（issue #9187），要严格结构化输出+投机解码的组合目前 vLLM 更稳。
- **投机解码**：两家都支持 EAGLE 系；SGLang 用 `--speculative-algorithm` 可选 EAGLE/EAGLE3/NEXTN/STANDALONE/NGRAM/UNO/DFLASH；TensorRT-LLM 1.2 删掉了双模型投机路径，只留单模型/drafter 变体。
来源：https://docs.vllm.ai/en/latest/features/structured_outputs/ ；https://docs.sglang.io/docs/advanced_features/speculative_decoding.md ；https://docs.sglang.io/docs/advanced_features/quantization.md ；https://github.com/sgl-project/sglang/issues/9187 ；https://nvidia.github.io/TensorRT-LLM/release-notes.html

## 7. 版本踩坑与选型（其他需要知道的）

- **版本现状**：vLLM 最新 v0.30.0（2026-09-22，V1 引擎，Model Runner V2 自 v0.29 起默认）；SGLang 最新 v0.5.20（CUDA 12 制品已退役，v0.5.19 是最后一条带 CUDA 12 的线）；TensorRT-LLM 当前 1.2；llama.cpp 滚动发版。升级前务必看各家 release notes——这三家 2026 年都有破坏性变更（vLLM 删了 `g_idx`、SGLang 删了旧 prefill CP v1、TRT-LLM 删了整个 TensorRT 后端）。
- **选型速记**：本地/边缘/CPU/Mac/GGUF → llama.cpp（或基于它的 Ollama、LM Studio）；GPU 生产多租户 → vLLM（硬件面最广）或 SGLang（前缀复用/agent 流量强）；全 NVIDIA 标准化集群要 NVFP4 等厂商级优化 → TensorRT-LLM（但按 PyTorch 运行时评估，别再找 engine 编译流程）。
- **周边关系**：Ollama/LM Studio/llama-cpp-python 都是 llama.cpp 生态（GGUF）；MLX 是 Apple 的框架，vLLM 在 Apple Silicon 上靠社区 vLLM-Metal 插件（底层 MLX）；TGI 是 Hugging Face 的老 serving 栈，2026 年的对比里基本已不是新项目首选（本次未单独核实其维护状态，写文档时建议按"非主推"处理）。
- **PD 分离不是免费午餐**：vLLM 文档自己提醒 "Disaggregated prefill DOES NOT improve throughput"，它解决的是 TTFT/ITL 独立扩缩；Dynamo 管理下还有 prefill worker 不能调 sleep 的已知坑（NixlConnector 残留状态会让 pause_scheduler 失败）。
来源：https://github.com/vllm-project/vllm/releases ；https://github.com/sgl-project/sglang/releases ；https://docs.vllm.ai/en/latest/features/disagg_prefill/ ；https://docs.nvidia.com/dynamo/dev/reference/releases/known-issues
