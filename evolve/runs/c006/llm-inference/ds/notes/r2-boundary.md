# r2-boundary
question: 对 4 条边界主张做反证（vLLM V1 medusa/lookahead 移除、llama.cpp 直载 safetensors、Ollama MLX 文档、llama.cpp server P/D 分离）
checked: https://github.com/vllm-project/vllm (git tree + vllm/config/speculative.py + vllm/v1/spec_decode/), https://github.com/vllm-project/vllm/releases/tag/v0.9.0 (+v0.9.1/v0.10.0/v0.11.0 bodies), https://docs.vllm.ai/en/latest/features/speculative_decoding/, https://github.com/ggml-org/llama.cpp (tree + src/llama-model-loader.cpp + PR #9916/#27058/#25675/#27004 + issue #21266 + tools/server/README.md), https://docs.ollama.com/ , https://docs.ollama.com/llms.txt , https://docs.ollama.com/gpu.md , https://github.com/ollama/ollama (tree + README + mlx/)

## claims
- [C1] vLLM main 的 SpeculativeMethod Literal 含 "medusa"（不含 "lookahead"）；合法值还有 ngram/draft_model/suffix/EagleModelTypes/NgramGPUTypes | src: https://github.com/vllm-project/vllm/blob/main/vllm/config/speculative.py | quote: "SpeculativeMethod = Literal[\"ngram\", \"medusa\", ... \"draft_model\", \"suffix\", ... EagleModelTypes, NgramGPUTypes]" | type: official
- [C2] vllm/v1/spec_decode/medusa.py 在 main 存在，含 V1 proposer 实现 | src: https://github.com/vllm-project/vllm/blob/main/vllm/v1/spec_decode/medusa.py | quote: "class MedusaProposer: \"\"\"Medusa proposer class for generating token sequences.\"\"\"" | type: official
- [C3] vLLM v0.9.0 release notes 明示 V1 支持 Medusa | src: https://github.com/vllm-project/vllm/releases/tag/v0.9.0 | quote: "[Model] vLLM v1 supports Medusa by @skylee-01 in https://github.com/vllm-project/vllm/pull/17956" | type: official
- [C4] v1/spec_decode 目录无 lookahead proposer（仅 tests/v1/spec_decode/test_dflash_lookahead.py，属 dflash）；docs spec decoding 页列出 EAGLE/MTP/draft/PARD/MLP/n-gram/suffix 等，未列 medusa/lookahead | src: https://docs.vllm.ai/en/latest/features/speculative_decoding/ | quote: "Model-based methods such as EAGLE, MTP, draft models, PARD and MLP provide the best latency reduction" | type: official
- [C5] llama.cpp src/llama-model-loader.cpp 只识别 GGUF 格式版本 | src: https://github.com/ggml-org/llama.cpp/blob/master/src/llama-model-loader.cpp | quote: "case GGUF_FILE_VERSION_V3: return \"GGUF V3 (latest)\"" | type: official
- [C6] llama.cpp PR #9916 "consolidated.safetensors" 自 2024-10-16 起 open、merged_at=null；repo tree 无任何 safetensors 路径 | src: https://github.com/ggml-org/llama.cpp/pull/9916 | quote: "state: open, title: consolidated.safetensors" | type: official
- [C7] docs.ollama.com 全部页面索引（llms.txt）、landing、gpu.md 均无 MLX；gpu.md 对 Apple 仅提 Metal | src: https://docs.ollama.com/gpu.md | quote: "Ollama supports GPU acceleration on Apple devices via the Metal API." | type: official
- [C8] ollama/ollama main 存在完整 mlx/ Go 包（array.go、compile.go、gated_delta.go、generator/、MLX_VERSION、cmake/mlx、.github/scripts/prepare_mlx_darwin.sh）；README 未提 mlx | src: https://github.com/ollama/ollama/tree/main/mlx | quote: "mlx/act.go, mlx/compile.go, mlx/generator, MLX_VERSION, cmake/mlx/CMakeLists.txt" | type: official
- [C9] llama.cpp server P/D 分离未合并：PR #27058 "server: add disaggregated prompt prefill over RPC" state=open merged_at=null；前作 PR #25675 closed(unmerged) 2026-08-14；PR #27004 (HTTP state handoff) 亦 open；issue #21266 open；master tree 与 server README 无 disaggreg/prefill 字样 | src: https://github.com/ggml-org/llama.cpp/pull/27058 | quote: "{\"closed_at\":null,\"merged_at\":null,\"state\":\"open\",\"title\":\"server: add disaggregated prompt prefill over RPC\"}" | type: official

## conflicts
- r1-vllm 主张「V1 已移除 Medusa」被 C1/C2/C3 推翻：medusa 是合法 SpeculativeMethod 且有 V1 proposer，v0.9.0 明文 "vLLM v1 supports Medusa"。但「lookahead 已移除」部分成立（C1 列表无 lookahead，v1 无 proposer 文件）——主张应改为仅 lookahead 被移除。

## gaps
- lookahead 移除的确切版本/changelog 明文未找到（已查 v0.9.0–v0.11.0 release notes 与 main 代码）。
- Ollama -mlx tag 覆盖模型范围、是否计划替代 llama.cpp 后端：docs.ollama.com 完全无说明，repo 内未见文档。
- llama.cpp docs/models.md 原句未本轮复查（沿用 r1 摘录）。

## leads
- ollama/ollama repo 的 mlx/ 包是 blog 之外的一手证据，可深挖 generator/ 推断支持模型族。
- vLLM dflash/dspark 等新 spec decode 方法（tests/v1/e2e）超出本题范围。
