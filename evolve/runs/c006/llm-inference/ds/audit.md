# 终审判定（1 核验工人，§0 全部主张 + llama.cpp GGUF）

V1 llama.cpp 17 后端 — confirmed（页面实列 17 个）
V2 vLLM GGUF 实验性+OOT 插件 — confirmed
V3 TRT-LLM TensorRT 后端移除 — 走样：removal 页无版本号；「v1.2 起」由 [30] release notes 支撑（"[BREAKING] TensorRT backend removed. PyTorch is now the sole execution backend."），成稿双引 [29][30]，保留
V4 vLLM APC hash 块/sha256 — confirmed
V5 SGLang radix tree/LRU — confirmed
V6 TGI 归档+官方推荐 — confirmed
V7 Ollama llama.cpp+MLX — confirmed
V8 llama.cpp GGUF-only — confirmed

未逐条核验：矩阵中次级事实（量化清单逐项、部署 flag 细节）——均有一手笔记 quote 支撑，未回原页重查。
