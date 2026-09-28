# r1-ecosystem
question: Ollama、MLX、TGI、LMDeploy、NVIDIA Dynamo、llm-d 与 vLLM/SGLang/TensorRT-LLM/llama.cpp 的关系和定位
checked: https://github.com/ollama/ollama, https://docs.ollama.com/import, https://docs.ollama.com/faq, https://ollama.com/blog/mlx-performance, https://github.com/ml-explore/mlx, https://github.com/ml-explore/mlx-lm, https://github.com/huggingface/text-generation-inference, https://github.com/InternLM/lmdeploy, https://github.com/ai-dynamo/dynamo, https://github.com/llm-d/llm-d, https://github.com/abetlen/llama-cpp-python, https://github.com/OpenNMT/CTranslate2, https://github.com/mlc-ai/mlc-llm, https://github.com/mudler/LocalAI, https://www.linkedin.com/posts/ollama_ollama-is-now-powered-by-mlx-on-apple-silicon-activity-7444864522856697857-1UQa

## claims
- [C1] Ollama README 的 "Supported backends" 只列一个后端：llama.cpp | src: https://github.com/ollama/ollama | quote: "llama.cpp project founded by Georgi Gerganov." | type: official
- [C2] Ollama 在后端之上封装 REST API、CLI、模型库（ollama.com/library）、桌面安装包 | src: https://github.com/ollama/ollama | quote: "Ollama has a REST API for running and managing models." | type: official
- [C3] Ollama 通过 Modelfile FROM 导入 GGUF 单文件/分片模型，也支持 Safetensors 目录 | src: https://docs.ollama.com/import | quote: "To import a single-file GGUF model, create a `Modelfile` containing: `FROM /path/to/file.gguf`" | type: official
- [C4] Ollama 导入时不再量化，需先用 llama.cpp 的 llama-quantize 预量化 | src: https://docs.ollama.com/import | quote: "Ollama does not quantize GGUF models during import." / "Prepare and quantize them first with a GGUF tool such as llama.cpp's `llama-quantize`." | type: official
- [C5] Ollama 已新增自研 MLX engine 跑在 Apple silicon 上（llama.cpp 之外第二引擎），用 `-mlx` tag 调用；repo 内有 mlx/mlxrunner 目录和 MLX_VERSION 文件 | src: https://ollama.com/blog/mlx-performance | quote: "Ollama's MLX engine has been updated to deliver its highest performance on Apple Silicon yet."（博文日期 2026-06-11，命令 `ollama run gemma4:12b-mlx`） | type: official
- [C6] MLX engine 于 2026-03-30 以 preview 发布（Ollama 官方 LinkedIn） | src: https://www.linkedin.com/posts/ollama_ollama-is-now-powered-by-mlx-on-apple-silicon-activity-7444864522856697857-1UQa | quote: "Today, we're previewing the fastest way to run Ollama on Apple silicon, powered by MLX, Apple's machine learning framework." | type: official
- [C7] MLX 是 Apple 机器学习研究团队出品的 Apple silicon 数组框架 | src: https://github.com/ml-explore/mlx | quote: "MLX is an array framework for machine learning on Apple silicon, brought to you by Apple machine learning research." | type: official
- [C8] mlx-lm 是基于 MLX 的 Apple silicon LLM 推理+微调 Python 包，带 HF Hub 集成 | src: https://github.com/ml-explore/mlx-lm | quote: "MLX LM is a Python package for generating text and fine-tuning large language models on Apple silicon with MLX." | type: official
- [C9] mlx-lm README 全页未提及 llama.cpp——两者是独立生态（C/Python vs MLX），在 Apple silicon 本地推理层面互为替代方案 | src: https://github.com/ml-explore/mlx-lm | quote: （页面无 llama.cpp 字样；已二次确认） | type: official
- [C10] TGI 是 Hugging Face 的 Rust/Python/gRPC 推理 server | src: https://github.com/huggingface/text-generation-inference | quote: "A Rust, Python and gRPC server for text generation inference" / "Used in production at Hugging Face to power Hugging Chat, the Inference API and Inference Endpoints." | type: official
- [C11] TGI repo 2026-03-21 被 archive，进入 maintenance mode，只收 minor fixes | src: https://github.com/huggingface/text-generation-inference | quote: "This repository was archived by the owner on Mar 21, 2026. It is now read-only." / "text-generation-inference is now in maintenance mode." | type: official
- [C12] HF 官方推荐用户改用 vLLM、SGLang、llama.cpp、MLX | src: https://github.com/huggingface/text-generation-inference | quote: "This approach is now adopted by downstream inference engines, which we contribute to and recommend using going forward" | type: official
- [C13] TGI 不依赖 vLLM，但其 Paged Attention 链接指向 vllm-project/vllm（借鉴该机制） | src: https://github.com/huggingface/text-generation-inference | quote: "Optimized transformers code for inference using Flash Attention and Paged Attention" | type: official
- [C14] LMDeploy 由 InternLM 组织下 MMRazor 和 MMDeploy 团队（OpenMMLab 系）开发 | src: https://github.com/InternLM/lmdeploy | quote: "developed by the MMRazor and MMDeploy teams" | type: official
- [C15] LMDeploy 定位是 LLM 压缩/部署/serving 工具箱，自带两个引擎 TurboMind（极致性能）和 PyTorch（低门槛） | src: https://github.com/InternLM/lmdeploy | quote: "a toolkit for compressing, deploying, and serving LLM" / "LMDeploy has developed two inference engines - TurboMind and PyTorch" | type: official
- [C16] LMDeploy 与 vLLM 是同级竞品，README 拿 vLLM 做性能对比基准；未提及 SGLang | src: https://github.com/InternLM/lmdeploy | quote: "LMDeploy delivers up to 1.8x higher request throughput than vLLM" | type: official
- [C17] NVIDIA Dynamo 是数据中心级分布式推理 serving 框架（ai-dynamo org），构建在引擎之上而非替代 | src: https://github.com/ai-dynamo/dynamo | quote: "the orchestration layer above inference engines — it doesn't replace SGLang, TensorRT-LLM, or vLLM" | type: official
- [C18] Dynamo 支持三个后端：SGLang、TensorRT-LLM、vLLM（prefill/decode 分离、KV-aware 路由等）；页面未提 llama.cpp | src: https://github.com/ai-dynamo/dynamo | quote: "Built in Rust for performance, Python for extensibility" + 后端矩阵含三引擎 | type: official
- [C19] llm-d 是 Kubernetes 上的分布式推理 serving 栈，跑在 model server 之上 | src: https://github.com/llm-d/llm-d | quote: "a high-performance distributed inference serving stack optimized for production deployments on Kubernetes" | type: official
- [C20] llm-d 明确以 vLLM/SGLang 为下层 model server | src: https://github.com/llm-d/llm-d | quote: "Model servers like vLLM and SGLang handle efficiently running large language models on accelerators." / "llm-d provides state-of-the-art orchestration and optimizations above model servers." | type: official
- [C21] llm-d 是 CNCF sandbox 项目，由 Red Hat、Google Cloud、IBM Research、CoreWeave、NVIDIA 共同发起 | src: https://github.com/llm-d/llm-d | quote: "founded by Red Hat, Google Cloud, IBM Research, CoreWeave, and NVIDIA" | type: official
- [C22] llama-cpp-python = llama.cpp 的 Python 绑定（abetlen），带 OpenAI 兼容 API | src: https://github.com/abetlen/llama-cpp-python | quote: "Simple Python bindings for @ggerganov's llama.cpp library." | type: official
- [C23] CTranslate2 是 OpenNMT 出品的 C++/Python Transformer 推理引擎（非 GGUF 系） | src: https://github.com/OpenNMT/CTranslate2 | quote: "CTranslate2 is a C++ and Python library for efficient inference with Transformer models." | type: official
- [C24] MLC-LLM 是 mlc-ai 组织（Apache TVM 血统）的编译式多端部署引擎 | src: https://github.com/mlc-ai/mlc-llm | quote: "Universal LLM Deployment Engine with ML Compilation" | type: official
- [C25] LocalAI 是 OpenAI 兼容的本地 AI 引擎，本身不实现推理，按需拉取后端镜像包装 llama.cpp、vLLM、MLX 等 60+ 后端 | src: https://github.com/mudler/LocalAI | quote: "Each backend wraps a best-in-class engine (llama.cpp, vLLM, whisper.cpp, stable-diffusion, MLX...)" | type: official

## conflicts
- 无（一手来源间未发现矛盾）

## gaps
- Ollama MLX engine 是否仅限 preview 模型集（-mlx tag 模型覆盖范围）、是否计划替代 llama.cpp 默认后端——官方页面未说明
- Dynamo 的 NVIDIA 归属在 README 无单句直述（仅 ai-dynamo org 与 NVIDIA 品牌推断）；llm-d 同理（founded by 列表含 NVIDIA）
- TGI 自哪一版/日期起停止功能开发仅有 archive 日期（2026-03-21），未查到更早 maintenance 公告

## leads
- Ollama 0.19 + MLX engine 意味着「Ollama=llama.cpp 封装」的说法自 2026-03 起已不完整，成稿应写成「llama.cpp 为主 + 新增 MLX 引擎（Apple silicon）」
- Dynamo 与 llm-d 定位高度重叠（K8s 分布式 serving 编排 + P/D 分离 + KV 路由），NVIDIA 同时是 llm-d 发起方——两者竞争/分工关系可深挖
- TGI archive 后 HF 生态位由 vLLM/SGLang 接管，成稿「周边项目」节可把 TGI 标为 legacy
