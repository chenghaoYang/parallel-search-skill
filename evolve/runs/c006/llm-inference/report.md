# vLLM / SGLang / TensorRT-LLM / llama.cpp 对比

> 截至 2026-09-25，官方文档为准。

## 0. 一屏看懂

- **「llama.cpp 只能跑 CPU」过时**：后端 17 个——CUDA/HIP/Metal/Vulkan/SYCL/MUSA/CANN/RPC/WebGPU 等 [40]；GGUF-only 本地运行时。
- **「vLLM 不支持 GGUF」过时**：支持，但高度实验性、已迁出主仓为插件 `vllm-gguf-plugin` [12]；主力是 safetensors+FP8/AWQ [9][10]。
- **「TRT-LLM 先编译 engine 再跑」已作废**：v1.0 起 PyTorch 默认、v1.2 起 TensorRT 后端整体删除（trtllm-build 已删、HF 直载）[29][30]。现为「NVIDIA-only 的 PyTorch 推理框架」。
- **vLLM prefix caching ≠ RadixAttention**：目标相同、实现不同——vLLM 是定长 block 的 hash 匹配（默认 sha256）[6]；SGLang 是 radix tree、单 token 粒度（`--page-size=1`）+ LRU 驱逐 + cache-aware 路由 [17][18][21]。
- **TGI 已归档**（2026-03 维护模式），HF 荐改用 vLLM/SGLang/llama.cpp/MLX [56]。
- **Ollama ≠ 纯 llama.cpp 封装**：主后端仍是 llama.cpp，但新增 MLX engine（Apple silicon）[52][54]。
- **选型**：数据中心——vLLM=生态最宽、SGLang=前缀密集/agentic/PD 分离、TRT-LLM=NVFP4+Dynamo；本地/边缘=llama.cpp 系；Apple 另看 MLX。

## 1. Taxonomy

轴：**部署目标**（数据中心↔本地）× **栈绑定**（HF 权重↔GGUF↔厂商栈）。

| 家族 | 成员 | 为什么是一类 |
|---|---|---|
| Python serving 框架 | vLLM、SGLang | HF 权重直载 + OpenAI server + K8s 生态 |
| NVIDIA 栈引擎 | TensorRT-LLM | 仅 NVIDIA GPU，PyTorch 前端+NV 专有量化 [29][35] |
| 本地运行时 | llama.cpp | 纯 C/C++、GGUF-only、后端最多、被 Ollama 等封装 [40][42] |
| 封装/编排层 | Ollama、LocalAI、Dynamo、llm-d 等 | 不是引擎，包装或调度上面三类 [52][58][59] |

## 2. 对照矩阵

### 调度与缓存（D1/D2）

| | vLLM | SGLang | TensorRT-LLM | llama.cpp |
|---|---|---|---|---|
| continuous batching | ✅ decode 优先调度 [8] | ✅ + overlap scheduler 默认开 [18] | ✅ in-flight batching [31] | ✅ slots，`--cont-batching` 默认开 [41] |
| chunked prefill | 默认开 [8] | `--chunked-prefill-size`，可混批 [18] | 默认开 [31] | — |
| P/D 分离 | 实验性，2 实例 + NixlConnector 等 connector [11] | ✅ 正式，Mooncake/NIXL + router [19] | ✅ `trtllm-serve disaggregated`，NIXL/UCX [32] | 未合入（PR open）[47] |
| 前缀复用 | APC：hash 定长块，V1 默认开，跨请求共享 [6][7] | RadixAttention：radix tree、token 粒度、LRU 系驱逐 [17][18] | radix tree 块复用 + prioritized LRU，默认开 [33] | prompt caching + slot 相似度匹配 [41] |
| 多层缓存 | LMCache/OffloadingConnector 等 [11] | HiCache L1 HBM/L2 DRAM/L3 分布式 [20] | — | 磁盘/RAM prompt cache [41] |
| 路由层 | production-stack（官方 K8s 栈）[21v] | Model Gateway：cache_aware 默认 [21] | Dynamo [39] | — |

### 量化 / 硬件 / 输出 / 投机（D3–D6）

| | vLLM | SGLang | TensorRT-LLM | llama.cpp |
|---|---|---|---|---|
| 模型格式 | safetensors；GGUF 实验插件 [12] | safetensors；GGUF 表列支持 [22] | HF checkpoint 直载 [29] | **仅 GGUF**，须 convert [42] |
| 量化 | FP8/MXFP4/NVFP4/INT4/GPTQ/AWQ 等 [9][10] | 22 种含 NVFP4/GGUF/modelopt [22] | FP8/NVFP4/MXFP4/AWQ/GPTQ 按 SM 代划分 [34] | Q4_K_M/IQ*/TQ/MXFP4/NVFP4，1.5–8bit [40][43] |
| 硬件 | CUDA/ROCm/XPU；CPU x86/ARM/s390x；TPU、Metal 走 OOT 插件 [13][14] | NV/AMD GPU、Xeon(AMX)、TPU(JAX)、Ascend、MUSA [16] | **仅 NVIDIA**（Ampere–Blackwell）[35] | 17 后端最广（WebGPU/Hexagon/RPC）[40] |
| 结构化输出 | xgrammar、guidance；JSON/regex/EBNF [16v] | xgrammar(默认)/outlines/llguidance [23] | xgrammar、llguidance [36] | GBNF + JSON Schema 子集 [44] |
| 投机解码 | EAGLE(3)/Medusa/MTP/draft/PARD/N-gram/Suffix [17v][61] | EAGLE(3)/STANDALONE/NGRAM/DFLASH/DSPARK/UNO；MTP 走 EAGLE [24][63] | DraftTarget/Eagle3/NGram/MTP/PARD/DFlash/SA [37] | draft/eagle3/dflash/mtp/ngram `--spec-type` [45] |

### 部署形态（D7）

| | server | 兼容 API | 分布式 | 上层生态 |
|---|---|---|---|---|
| vLLM | `vllm serve`，Docker `vllm/vllm-openai` [20v] | OpenAI + Anthropic + gRPC [10] | TP/PP/DP/EP/CP，Ray 多机 [23v] | K8s：Helm/Dynamo/llm-d/KServe 等 13 项 [21v] |
| SGLang | `sglang.launch_server`，`sgl.Engine` 离线 [25] | OpenAI | TP/PP/DP/EP，多机、LWS on K8s [34s] | Model Gateway（Rust）[21] |
| TRT-LLM | `trtllm-serve`（`--backend` 已废） | OpenAI [38] | TP/PP/EP，disagg 编排 [32] | Dynamo、Triton [39] |
| llama.cpp | `llama-server`/cli | OpenAI + Anthropic [41] | `--split-mode`、RPC 多机 [41] | Ollama/llama-cpp-python 等 [52] |

## 3. 周边项目关系

| 项目 | 关系 |
|---|---|
| Ollama | 封装：llama.cpp 主后端 + 新 MLX engine；registry/CLI [52][54] |
| MLX / mlx-lm | Apple 自研框架，与 llama.cpp 无代码关系，Apple silicon 替代方案 [55] |
| TGI | HF server，2026-03 归档，荐 vLLM/SGLang/llama.cpp/MLX [56] |
| LMDeploy | OpenMMLab 竞品，TurboMind+PyTorch 双引擎 [57] |
| Dynamo / llm-d | 编排层：Dynamo 跨三引擎（PD 分离、KV 路由）；llm-d=CNCF K8s 栈，下层 vLLM/SGLang [58][59] |

## 4. 坑

- **vLLM V1 迁移**：v0.8 起 V1 默认、v0.11 删光 V0；`best_of`、prompt adapter 等被砍 [1v][3v][4v]；v0.11.0 `--async-scheduling` 有乱码 bug [1v]；Windows 仅 WSL [15]。
- **TRT-LLM 版本剧变**：1.0 换默认后端、1.2 删 TensorRT 路径且 CLI>YAML 优先级反转 [30]；Medusa/Lookahead 残留到 ~1.3.0rc26 才删（release notes 无明文）[62]。
- **SGLang flag 漂移**：v0.5.16 起多个 flag 无别名改名，旧命令直接报错；env 前缀 `SGL_`→`SGLANG_`、超时单位 ms→s [27][28]。
- **llama.cpp 默认值漂移**（教程失效重灾区）：二进制改名 `llama-*` [48]、context shift 默认关（超长 prompt 报错而非截断）[50]；无 semver，按 build 号发布。
- **GGUF 互通错觉**：vLLM/SGLang 跑 GGUF 只是兼容运行，没有 llama.cpp 量化生态（imatrix/IQ/K-quants）；深度需求回 llama.cpp 系 [12][22][43]。

## 5. 未决与置信度

- SGLang spec 枚举两文档页都滞后：v0.5.20 代码合法值含 DFLASH/DSPARK/UNO（NEXTN=EAGLE 别名），以代码为准 [63]。
- TRT-LLM INT8/INT4 不在 1.3 quantization 矩阵（旧 support-matrix 的 Blackwell 行仅 v1.0.0 文档有）[34]。
- 未逐页核：llama.cpp 后端成熟度、SGLang 结构化输出×radix 交互、Ollama MLX 覆盖面。

## 来源

[1v] https://github.com/vllm-project/vllm/releases/tag/v0.11.0 · [3v] https://github.com/vllm-project/vllm/issues/18571 · [4v] https://docs.vllm.ai/en/latest/usage/v1_guide/ · [6] https://docs.vllm.ai/en/latest/design/prefix_caching/ · [7] https://docs.vllm.ai/en/v0.10.2/configuration/engine_args.html · [8] https://docs.vllm.ai/en/latest/configuration/optimization.html · [9] https://docs.vllm.ai/en/latest/features/quantization/ · [10] https://github.com/vllm-project/vllm · [11] https://docs.vllm.ai/en/latest/features/disagg_prefill.html · [12] https://docs.vllm.ai/en/latest/features/quantization/gguf.html · [13] https://docs.vllm.ai/en/latest/getting_started/installation/ · [14] https://github.com/vllm-project/tpu-inference · [15] https://docs.vllm.ai/en/stable/getting_started/installation/gpu/index.html · [16v] https://docs.vllm.ai/en/latest/features/structured_outputs.html · [17v] https://docs.vllm.ai/en/latest/features/speculative_decoding/ · [20v] https://docs.vllm.ai/en/latest/deployment/docker.html · [21v] https://docs.vllm.ai/en/stable/deployment/k8s/ · [23v] https://docs.vllm.ai/en/stable/serving/parallelism_scaling/
[16] https://github.com/sgl-project/sglang · [17] https://lmsys.org/blog/2024-01-17-sglang/ · [18] https://docs.sglang.io/docs/advanced_features/server_arguments.md · [19] https://docs.sglang.io/docs/advanced_features/pd_disaggregation.md · [20] https://docs.sglang.io/docs/advanced_features/hicache_design.md · [21] https://docs.sglang.io/docs/advanced_features/sgl_model_gateway.md · [22] https://docs.sglang.io/docs/advanced_features/quantization.md · [23] https://docs.sglang.io/docs/advanced_features/structured_outputs.md · [24] https://docs.sglang.io/docs/advanced_features/speculative_decoding.md · [25] https://docs.sglang.io/docs/get-started/quickstart.md · [34s] https://docs.sglang.io/docs/references/multi_node_deployment/deploy_on_k8s.md · [27] https://sgl-project-sglang-93.mintlify.app/resources/migration-guide · [28] https://github.com/sgl-project/sglang/releases/tag/v0.5.16
[29] https://nvidia.github.io/TensorRT-LLM/legacy/tensorrt-backend-removal.html · [30] https://nvidia.github.io/TensorRT-LLM/release-notes.html · [31] https://nvidia.github.io/TensorRT-LLM/features/paged-attention-ifb-scheduler.html · [32] https://nvidia.github.io/TensorRT-LLM/features/disagg-serving.html · [33] https://nvidia.github.io/TensorRT-LLM/features/kvcache.html · [34] https://nvidia.github.io/TensorRT-LLM/features/quantization.html · [35] https://nvidia.github.io/TensorRT-LLM/supported-hardware.html · [36] https://nvidia.github.io/TensorRT-LLM/features/guided-decoding.html · [37] https://nvidia.github.io/TensorRT-LLM/features/speculative-decoding.html · [38] https://nvidia.github.io/TensorRT-LLM/commands/trtllm-serve/trtllm-serve.html · [39] https://github.com/NVIDIA/TensorRT-LLM
[40] https://github.com/ggml-org/llama.cpp · [41] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md · [42] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/docs/models.md · [43] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/include/llama.h · [44] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md · [45] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/docs/speculative.md · [47] https://api.github.com/repos/ggml-org/llama.cpp/pulls/27058 · [48] https://github.com/ggml-org/llama.cpp/pull/7809 · [50] https://github.com/ggml-org/llama.cpp/commit/d2fcd91cf96b46f4485ce46b4e3a32bf0df37715
[52] https://github.com/ollama/ollama · [54] https://ollama.com/blog/mlx-performance · [55] https://github.com/ml-explore/mlx-lm · [56] https://github.com/huggingface/text-generation-inference · [57] https://github.com/InternLM/lmdeploy · [58] https://github.com/ai-dynamo/dynamo · [59] https://github.com/llm-d/llm-d · [61] https://github.com/vllm-project/vllm/releases/tag/v0.9.0 · [62] https://github.com/NVIDIA/TensorRT-LLM/commit/23e5ff15f7 · [63] https://github.com/sgl-project/sglang/blob/v0.5.20/python/sglang/srt/speculative/spec_info.py
