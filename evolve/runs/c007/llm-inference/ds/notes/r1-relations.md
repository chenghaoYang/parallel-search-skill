# r1-relations
question: Ollama、MLX、TGI 这三个周边项目与 vLLM/SGLang/TensorRT-LLM/llama.cpp 的关系现在是什么？
checked: github.com/ollama/ollama, raw.githubusercontent.com/ollama/ollama/main/README.md, ollama.com/blog, ollama.com/blog/mlx, ollama.com/blog/improved-performance-and-model-support-with-gguf, ollama.com/blog/multimodal-models, docs.ollama.com/faq, github.com/huggingface/text-generation-inference (+raw README), github.com/ml-explore/mlx-lm (+raw README + mlx_lm/{utils,gguf,tokenizer_utils,convert}.py), raw.githubusercontent.com/ml-explore/mlx/main/README.md, github.com/ai-dynamo/dynamo, github.com/llm-d/llm-d

## claims
- [C1] Ollama README 设「Supported backends」一节，只列出 llama.cpp（链向 ggml-org/llama.cpp）；vLLM 在 README 中零提及。 | src: https://github.com/ollama/ollama | quote: "## Supported backends — [llama.cpp](https://github.com/ggml-org/llama.cpp) project founded by Georgi Gerganov." | type: official
- [C2] Ollama 官方承认历史上模型支持依赖 llama.cpp（2025-05-15 博客）。 | src: https://ollama.com/blog/multimodal-models | quote: "Ollama has so far relied on the ggml-org/llama.cpp project for model support" | type: official
- [C3] 2025-05-15 起 Ollama 有自有新引擎，在 Go 中直接调用 GGML 做推理图（多模态模型首批支持）。 | src: https://ollama.com/blog/multimodal-models | quote: "Ollama now supports multimodal models via Ollama's new engine" / "Being able to access GGML directly from Go has given a portable way to design custom inference graphs" | type: official
- [C4] 2026-03-30 起 Ollama 在 Apple silicon 上构建于 Apple MLX 框架之上（preview，Ollama 0.19）。 | src: https://ollama.com/blog/mlx | quote: "Ollama on Apple silicon is now built on top of Apple's machine learning framework, MLX" | type: official
- [C5] Ollama 0.30（2026-06-05）经 llama.cpp 提供 GGUF 兼容，官方明确它是对 MLX 引擎的补充而非替代。 | src: https://ollama.com/blog/improved-performance-and-model-support-with-gguf | quote: "Ollama 0.30 is now available with improved performance and GGUF model compatibility through llama.cpp." / "This augments Ollama's MLX engine on Apple silicon" | type: official
- [C6] ollama/ollama 仓库顶层同时存在 llama/、LLAMA_CPP_VERSION 与 mlx/、mlxrunner/、MLX_VERSION——多引擎并存（2026-09 抓取）。 | src: https://github.com/ollama/ollama | quote: "LLAMA_CPP_VERSION, MLX_C_VERSION, MLX_VERSION, llama, mlx, mlxrunner" | type: official
- [C7] 未发现 Ollama×vLLM 官方集成或对比：Ollama README、docs FAQ、官方博客均不提 vLLM。 | src: https://docs.ollama.com/faq | quote: "no mention of llama.cpp, vLLM, GGUF, or MLX" (page scan) | type: official
- [C8] MLX 是 Apple 官方的 Apple silicon 机器学习 array 框架（ml-explore 组织）。 | src: https://raw.githubusercontent.com/ml-explore/mlx/main/README.md | quote: "MLX is an array framework for machine learning on Apple silicon" | type: official
- [C9] mlx-lm 定位：在 Apple silicon 上用 MLX 生成文本与微调 LLM 的 Python 包，与 llama.cpp 相互独立（README 不提 llama.cpp/GGUF）。 | src: https://github.com/ml-explore/mlx-lm | quote: "MLX LM is a Python package for generating text and fine-tuning large language models on Apple silicon with MLX." | type: official
- [C10] mlx-lm 走 HF Hub 生态：加载 MLX 格式模型，mlx-community 提供预量化模型，convert 工具把 HF 模型量化转 MLX 格式。 | src: https://raw.githubusercontent.com/ml-explore/mlx-lm/main/README.md | quote: "You can specify any MLX-compatible model with the --model flag" | type: official
- [C11] mlx-lm 权重加载只认 safetensors（`model*.safetensors`，缺失报 "No safetensors found"）；仓库内 gguf.py 仅为拷贝自 llama.cpp convert.py 的 tokenizer 词表解析工具，未接入主加载路径。 | src: https://raw.githubusercontent.com/ml-explore/mlx-lm/main/mlx_lm/utils.py | quote: "weight_files = glob.glob(str(model_path / \"model*.safetensors\"))" | type: official
- [C12] TGI 已进维护模式，只接受小修/文档/轻量维护 PR。 | src: https://github.com/huggingface/text-generation-inference | quote: "text-generation-inference is now in maintenance mode. Going forward, we will accept pull requests for minor bug fixes, documentation improvements and lightweight maintenance tasks." | type: official
- [C13] HF 官方在 TGI README 推荐转向：vLLM、SGLang，及本地引擎 llama.cpp、MLX。 | src: https://github.com/huggingface/text-generation-inference | quote: "we contribute to and recommend using going forward: [vllm], [SGLang], as well as local engines with inter-compatibility such as llama.cpp or MLX." | type: official
- [C14] TGI 仓库被 owner 于 2026-03-21 archive，只读。 | src: https://github.com/huggingface/text-generation-inference | quote: "This repository was archived by the owner on Mar 21, 2026. It is now read-only." | type: official
- [C15] NVIDIA Dynamo 是 vLLM/SGLang/TRT-LLM 之上的编排层而非替代，三者为支持的后端。 | src: https://github.com/ai-dynamo/dynamo | quote: "Dynamo is the orchestration layer above inference engines" / "it doesn't replace SGLang, TensorRT-LLM, or vLLM, it turns them into a coordinated multi-node inference system." | type: official
- [C16] llm-d 是 vLLM 等 model server 之上的 Kubernetes 编排/优化层。 | src: https://github.com/llm-d/llm-d | quote: "llm-d provides state-of-the-art orchestration and optimizations above model servers" / "integrating industry-standard open technologies like vLLM and Kubernetes" | type: official
- [C17] 「本地跑模型用 Ollama = 用了 llama.cpp」准确版本：2025-05 前成立；此后 Ollama 有自有 Go+GGML 引擎、Apple silicon 上 MLX 引擎（2026-03 preview 起），llama.cpp 退居 GGUF 兼容层——该说法现已过时（综合 C2–C5）。 | src: https://ollama.com/blog/multimodal-models | quote: "Ollama has so far relied on the ggml-org/llama.cpp project for model support" | type: official

## conflicts
- Ollama README「Supported backends」只列 llama.cpp，而官方博客称 Apple silicon 上已「built on top of MLX」且有自有 Go 引擎——README 落后于多引擎现实（doc lag）。src: github.com/ollama/ollama vs ollama.com/blog/mlx
- C5 中 llama.cpp 被官方描述为「augments Ollama's MLX engine」——从唯一后端降级为兼容补充，与「Ollama 基于 llama.cpp」旧认知冲突。

## gaps
- MLX 引擎是否已转正为 Apple silicon 默认路径？2026-06 博客称 "Ollama's MLX engine" 无 preview 字样，未见 GA 公告。
- Ollama 按模型/平台选引擎（llama.cpp vs 自有 vs MLX）的路由规则无官方文档。
- Ollama×vLLM 无官方集成/对比的正面表述（仅确认多页缺席）。
- mlx-lm 的 gguf.py 未被 utils/tokenizer_utils/convert 引用，是否残留代码未确认。

## leads
- Ollama MLX 性能数据：ollama.com/blog/mlx-performance（2026-06-11）、ollama.com/blog/faster-gemma-4-mlx-mtp（2026-06-29）。
- TGI archive 日期（2026-03-21）可作 HF 生态转向 vLLM/SGLang 的时间锚点。
- Dynamo、llm-d 均为「引擎之上编排层」，§3 适配层素材可与引擎层对照。
