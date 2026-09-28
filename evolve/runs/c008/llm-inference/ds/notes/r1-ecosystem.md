# r1-ecosystem
question: Ollama、MLX、TGI 与 vLLM/SGLang/TensorRT-LLM/llama.cpp 的关系：Ollama 底层是不是 llama.cpp、TGI 维护状态、MLX 定位、Ollama 最近是否换引擎。
checked: https://github.com/ollama/ollama, https://raw.githubusercontent.com/ollama/ollama/main/README.md, https://github.com/huggingface/text-generation-inference, https://raw.githubusercontent.com/huggingface/text-generation-inference/main/README.md, https://github.com/ml-explore/mlx-lm, https://raw.githubusercontent.com/ml-explore/mlx-lm/main/README.md, https://raw.githubusercontent.com/ml-explore/mlx-lm/main/mlx_lm/SERVER.md, https://ollama.com/blog, https://ollama.com/blog/mlx, https://ollama.com/blog/multimodal-models, https://ollama.com/blog/improved-performance-and-model-support-with-gguf, https://docs.ollama.com/faq, gh api repos/huggingface/text-generation-inference

## claims
- [C1] Ollama README 的 "Supported backends" 一节只列了 llama.cpp（截至本次抓取）。 | src: https://raw.githubusercontent.com/ollama/ollama/main/README.md | quote: "## Supported backends - [llama.cpp](https://github.com/ggml-org/llama.cpp) project founded by Georgi Gerganov." | type: official
- [C2] Ollama 官方博客承认此前模型支持一直依赖 llama.cpp（2025-05-15 博文）。 | src: https://ollama.com/blog/multimodal-models | quote: "Ollama has so far relied on the ggml-org/llama.cpp project for model support." | type: official
- [C3] 2025-05-15 Ollama 发布自研新引擎，首发用于多模态模型（Llama 4 / Gemma 3 / Qwen 2.5 VL）；纯文本模型仍由 llama.cpp 支持。 | src: https://ollama.com/blog/multimodal-models | quote: "We set out to support a new engine that makes multimodal models first-class citizens" / "Today, ggml/llama.cpp offers first-class support for text-only models." | type: official
- [C4] 2026-03-30 Ollama 宣布在 Apple silicon 上改由 MLX 驱动（preview），发布版本为 Ollama 0.19。 | src: https://ollama.com/blog/mlx | quote: "Today, we're previewing the fastest way to run Ollama on Apple silicon, powered by MLX, Apple's machine learning framework." / "Download Ollama 0.19" | type: official
- [C5] 2026-06-05 Ollama 0.30 通过 llama.cpp 增加 GGUF 模型兼容，定位是"增强"而非替代 Apple silicon 上的 MLX 引擎。 | src: https://ollama.com/blog/improved-performance-and-model-support-with-gguf | quote: "Ollama 0.30 is now available with improved performance and GGUF model compatibility through llama.cpp. This augments Ollama's MLX engine on Apple silicon" | type: official
- [C6] Ollama 0.30 在 NVIDIA 硬件上提速最高 20%，优化来自 NVIDIA 与 llama.cpp 社区的贡献。 | src: https://ollama.com/blog/improved-performance-and-model-support-with-gguf | quote: "performance on NVIDIA hardware is now up to 20% faster, leveraging optimizations contributed by the NVIDIA and llama.cpp" | type: official
- [C7] TGI GitHub 仓库已被归档（API: archived=true，最后 push 2026-03-21T11:34:22Z），页面横幅显示 "archived by the owner on Mar 21, 2026... read-only"。 | src: https://github.com/huggingface/text-generation-inference | quote: "This repository was archived by the owner on Mar 21, 2026. It is now read-only." | type: official
- [C8] TGI README 顶部 CAUTION：项目进入 maintenance mode，只接受小修、文档和轻量维护 PR。 | src: https://raw.githubusercontent.com/huggingface/text-generation-inference/main/README.md | quote: "text-generation-inference is now in maintenance mode. Going forward, we will accept pull requests for minor bug fixes, documentation improvements and lightweight maintenance tasks." | type: official
- [C9] TGI README 明确推荐改用 vLLM、SGLang，本地引擎推荐 llama.cpp 或 MLX——即 HF 官方已把 TGI 用户导向这四者。 | src: https://raw.githubusercontent.com/huggingface/text-generation-inference/main/README.md | quote: "which we contribute to and recommend using going forward: [vllm](...), [SGLang](...), as well as local engines with inter-compatibility such as llama.cpp or MLX." | type: official
- [C10] TGI 自我定位是 Rust/Python/gRPC serving toolkit，曾在 HF 生产环境支撑 Hugging Chat、Inference API、Inference Endpoints。 | src: https://raw.githubusercontent.com/huggingface/text-generation-inference/main/README.md | quote: "A Rust, Python and gRPC server for text generation inference. Used in production at Hugging Face to power Hugging Chat, the Inference API and Inference Endpoints." | type: official
- [C11] mlx-lm 官方定位：Apple silicon 上基于 MLX 做文本生成与微调的 Python 包。 | src: https://raw.githubusercontent.com/ml-explore/mlx-lm/main/README.md | quote: "MLX LM is a Python package for generating text and fine-tuning large language models on Apple silicon with MLX." | type: official
- [C12] mlx-lm 支持通过 mx.distributed 做分布式推理与微调。 | src: https://raw.githubusercontent.com/ml-explore/mlx-lm/main/README.md | quote: "Distributed inference and fine-tuning with `mx.distributed`" | type: official
- [C13] mlx_lm.server 提供类 OpenAI chat API 的 HTTP 服务，默认起在 localhost:8080。 | src: https://raw.githubusercontent.com/ml-explore/mlx-lm/main/mlx_lm/SERVER.md | quote: "The HTTP API is intended to be similar to the OpenAI chat API." / "start a text generation server on port 8080 of the localhost" | type: official
- [C14] 官方明确 mlx_lm.server 不适合生产环境（只有基础安全检查）。 | src: https://raw.githubusercontent.com/ml-explore/mlx-lm/main/mlx_lm/SERVER.md | quote: "The MLX LM server is not recommended for production as it only implements basic security checks." | type: official
- [C15] Ollama 0.19 MLX preview 官方数据：prefill 1810 vs 0.18 的 1154 tokens/s，decode 112 vs 58 tokens/s；int4 量化下可到 1851/134 tokens/s。 | src: https://ollama.com/blog/mlx | quote: "Prefill performance ... 1810 Ollama 0.19 1154 Ollama 0.18 ... Decode performance ... 112 Ollama 0.19 58 Ollama 0.18" | type: official

## conflicts
- Ollama README 的 "Supported backends" 仍只列 llama.cpp（C1），与 2026-03-30 博客"powered by MLX"（C4）口径不一致——README 明显滞后于引擎变更；仓库内已存在 mlx/、mlxrunner/、MLX_VERSION 文件（github.com/ollama/ollama 目录列表）。
- 表述粒度差异：C3 说新引擎直接走 GGML tensor library（Go 侧），C5 说 GGUF 兼容"through llama.cpp"——GGML、llama.cpp、Ollama 自研层三者边界在官方文中并不完全统一，主文档引用时建议并列两条原句。

## gaps
- docs.ollama.com/faq 页面为 JS 渲染，curl 未抓到 llama.cpp/MLX 相关原句；旧版 repo docs/faq.md 已 404。FAQ 中"Ollama 与 llama.cpp 关系"的经典句子未拿到当前版本原句。
- Ollama 0.19 之后（0.30+）在非 Apple 平台默认引擎是 MLX 还是 llama.cpp，官方未逐平台明说（C5 只说 MLX 是 Apple silicon 引擎、llama.cpp 负责 GGUF 兼容）。
- TGI README 未给出 maintenance mode 的起始日期；归档日 2026-03-21 来自 GitHub API/UI，非 README 文字。

## leads
- Ollama 2026-06-29 博文 "Faster Gemma 4 on MLX with multi-token prediction"（ollama.com/blog/faster-gemma-4-mlx-mtp）：Ollama 0.31 起 MLX 引擎支持 MTP，coding agent 场景最高提速 90%——如主文档需要性能论据可用。
- Ollama 2026-08-10 博文提到 MLX 引擎新增 DFlash 与图像输入支持（ollama.com/blog/muse-glimmer），说明 MLX 引擎仍在快速迭代。
