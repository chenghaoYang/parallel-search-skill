# Grid v1

## 分类轴（v1，R1 收束后微调）
- 轴 A：部署目标 —— 数据中心 serving ↔ 本地/嵌入式运行时。
- 轴 B：栈与格式绑定 —— HF 权重直载 ↔ 自有格式（GGUF）↔ 厂商栈绑定（NVIDIA-only）。
- 变更理由：TRT-LLM 已不再是「编译为 engine」，原「运行形态」轴失效；差异本质是硬件栈绑定。

## 状态网格（R1 收束后）
| 实体 | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|---|
| vLLM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(Medusa/lookahead 去留❓) | ✅ |
| SGLang | ✅ | ✅ | ✅ | ✅(各后端成熟度⚠) | ✅ | ⚔(枚举冲突) | ✅ |
| TensorRT-LLM | ✅ | ✅ | ⚔(INT8 口径) | ✅ | ✅ | ✅(移除版本❓) | ✅ |
| llama.cpp | ✅ | ✅ | ✅(safetensors 间接) | ✅ | ✅ | ✅ | ✅ |
| 周边 | — | — | — | — | — | — | ✅ |

## R2 候选缺口
- ⚔ SGLang spec 枚举：server_arguments vs spec 文档（UNO/DFLASH）
- ❓ TRT-LLM Medusa/Lookahead 移除版本、INT8 现状
- ❓ llama.cpp P/D 分离 PR 状态（已确认 open，够用了）、各后端成熟度
- 边界主张反证：「TRT-LLM 仅 NVIDIA」「llama.cpp 仅 GGUF」「vLLM 不支持 Windows」均有官方原句，强度够；「Ollama MLX engine 仅部分模型」未证
