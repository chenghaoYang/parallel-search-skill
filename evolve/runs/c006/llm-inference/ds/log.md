# Log

## R0
- 框架：4 核心实体 + 周边关系维度。分类轴 v0：A=运行形态（Python 服务端 / 编译引擎 / 本地运行时），B=模型表示（HF 权重 / GGUF / TRT engine）。
- R1 计划：4 个实体工人（各填自己一行 D1–D7）+ 1 个生态工人（D8 + 周边实体定位）+ 1 个 scout（坑/误区/漏列实体，只产 leads）。共 6 spawn。
- 决策依据：来源边界清晰（每个引擎一个官方文档站），实体工人各拿一整行效率最高。
R1 spawned: r1-vllm, r1-sglang, r1-trtllm, r1-llamacpp, r1-ecosystem, r1-scout
待查：SGLang spec 枚举冲突（--speculative-algorithm vs spec 文档 UNO/DFLASH）；vLLM Medusa/lookahead 是否被 V1 移除；llama.cpp safetensors 不能直载需原句

## R1 收束
- 观察：6 工人全返回，156 claims（153 official）。网格 84% 填充；冲突 3 处（SGLang spec 枚举、TRT-LLM INT8、vLLM APC 默认态已裁决）。
- taxonomy v0→v1：「编译引擎」轴失效（TRT-LLM 已 PyTorch-only），改为「栈与格式绑定」轴。
- 成稿 10576→9090 字：压缩散文、删 7 个次要来源（[19v][22v][26l][46][49][53][26]）。
- 决策：R2 派窄简报——①SGLang spec 枚举冲突裁决；②TRT-LLM Medusa/Lookahead 移除版本 + INT8 现状；③边界反证打包（llama.cpp safetensors 直载、Ollama MLX 覆盖面、vLLM Medusa/lookahead 在 V1 的状态）。预计 spawn：3。

## R2 收束
- 返回 3/3。修正：①SGLang spec 枚举——两文档页都滞后，v0.5.20 代码合法值含 DFLASH/DSPARK/UNO（NEXTN=EAGLE 别名，MTP 走 EAGLE）；②vLLM Medusa 仍在 V1（v0.9.0 起），仅 lookahead 移除；③TRT-LLM Medusa/Lookahead 残留到 ~1.3.0rc26（PR #18532）；④llama.cpp safetensors 直载确认不成立（loader 仅 GGUF，PR #9916 open）；⑤TRT-LLM INT8 不在 1.3 quantization 矩阵。
- 成稿 8992→8991：新增 3 来源 [61-63]，删 LocalAI 行并入，散文再压缩。
- 决策：核心格已 ✅/∅，疑点全有结论，边界主张已反证 → 终审（1 核验工人，§0 六主张）后停。

## 终审（R3）
- 1 核验工人回原页核 §0 八项：7 confirmed，1 走样（V3 版本号不在 removal 页，由 [30] 支撑，不改稿）。
- 终稿 8991 字 ≤ 9000；网格 27✅/1⚠/2⚔→已裁决写入 §5；引用一致（无 uncited/missing）。
- 停止：轮数预算用尽、核心格填满、边界主张已反证。
