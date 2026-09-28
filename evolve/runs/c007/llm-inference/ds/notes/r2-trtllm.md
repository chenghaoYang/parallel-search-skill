# r2-trtllm
question: 裁决 speculative-decoding 页 "The PyTorch backend supports only `Eagle3`" 冲突；v1.0.0 发布日期；Medusa/lookahead/SmoothQuant 在 1.x release notes 的 removed/deprecated 条目；仓库 LICENSE。
checked: https://nvidia.github.io/TensorRT-LLM/features/speculative-decoding.html, https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0, https://api.github.com/repos/NVIDIA/TensorRT-LLM/releases/tags/v1.0.0, https://nvidia.github.io/TensorRT-LLM/latest/release-notes.html, https://github.com/NVIDIA/TensorRT-LLM, https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/LICENSE, https://github.com/NVIDIA/TensorRT-LLM/releases.atom

## claims

### D6 冲突裁决：Eagle3 句的位置与语义
- [C1] "The PyTorch backend supports only `Eagle3`." 位于 "Usage with `trtllm-bench` and `trtllm-serve`" 小节（讲用 `--config config.yaml` 传 speculative 配置），以 blockquote Note 形式紧跟在 decoding_type 取值列表之后，不在任何算法专属小节内。 | src: https://nvidia.github.io/TensorRT-LLM/features/speculative-decoding.html | quote: "The PyTorch backend supports only `Eagle3`." | type: official
- [C2] 该 Note 的完整后续句表明其限定范围是 EAGLE 家族/checkpoint 版本，而非全部 speculative 类型：`Eagle` 是 `Eagle3` 的兼容别名，EAGLE v1/v2 checkpoint 不兼容。 | src: https://nvidia.github.io/TensorRT-LLM/features/speculative-decoding.html | quote: "`decoding_type: Eagle` is accepted as a backward-compatible alias for `Eagle3`, but EAGLE (v1/v2) draft checkpoints are incompatible." | type: official
- [C3] 同一小节把 7 个 decoding_type 列为该 YAML 配置的可用选项，紧跟 Note 之前：MTP、Eagle3、NGram、DraftTarget、PARD、DFlash、SA。 | src: https://nvidia.github.io/TensorRT-LLM/features/speculative-decoding.html | quote: "An additional `decoding_type` option is used to specify the type of speculation to use. The available options are:" | type: official
- [C4] 同页还有非 decoding_type 的 UserProvidedDecodingConfig；SA 可作 standalone（SADecodingConfig）或增强 MTP/Eagle3/PARD；MTP 支持 DeepSeek 及 Qwen3 MoE、Step-3.x 等原生 MTP 模块。 | src: https://nvidia.github.io/TensorRT-LLM/features/speculative-decoding.html | quote: "MTP is supported by DeepSeek models and other architectures that ship native MTP modules" | type: official
- [C5] 裁决：该句按字面读与正上方的 7 项列表矛盾，但按其自身后续句（Eagle 别名 + v1/v2 checkpoint 不兼容）应读作「EAGLE 家族中只支持 Eagle3（EAGLE v1/v2 checkpoint 不可用）」，不是「PyTorch 后端只支持 Eagle3 这一种 spec decoding」。页面无第二处限制 PyTorch 后端 decoding_type 的句子；措辞位置不佳，属文档歧义而非旧路径限定。 | src: https://nvidia.github.io/TensorRT-LLM/features/speculative-decoding.html | quote: "The PyTorch backend supports only `Eagle3`." | type: official

### v1.0.0 发布日期
- [C6] v1.0.0 发布于 2025-09-24T12:53:50Z（GitHub API published_at；created_at 2025-09-23，updated_at 2025-10-17），作者 zongfeijing，name "v1.0.0"，非 prerelease。 | src: https://api.github.com/repos/NVIDIA/TensorRT-LLM/releases/tags/v1.0.0 | quote: "\"published_at\": \"2025-09-24T12:53:50Z\"" | type: official
- [C7] tag 页显示 "released this 24 Sep 12:53"（页面不显示年份），标题 "TensorRT LLM Release 1.0"。 | src: https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0 | quote: "released this 24 Sep 12:53" | type: official
- [C8] v1.0.0 highlights：PyTorch 架构转正为默认；breaking change 为 "Promote PyTorch to be the default LLM backend"。 | src: https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0 | quote: "the PyTorch-based architecture is now stable and the default experience, and the LLM API is now stable" | type: official

### Medusa / lookahead / SmoothQuant 的 removed/deprecated 条目
- [C9] release-notes.html 单页覆盖 1.3、1.2、1.1、1.0、0.21.0–0.11.0；其中 1.x 各节均无 Medusa/lookahead/SmoothQuant 的 removed/deprecated 条目（三者全页仅出现于 0.x 的 added/fixed 条目）。 | src: https://nvidia.github.io/TensorRT-LLM/latest/release-notes.html | quote: "Enabled Medusa for Qwen2 models."（0.15.0 Key Features） | type: official
- [C10] Medusa 最后出现：0.15.0 "Enabled Medusa for Qwen2 models." 与 0.16.0 LLM API additions "Medusa support."；1.x 无任何提及。 | src: https://nvidia.github.io/TensorRT-LLM/latest/release-notes.html | quote: "Medusa support." | type: official
- [C11] lookahead 最后出现：0.17.0 "Added runtime support for seamless lookahead decoding."（另 0.13.0 experimental、0.14.0 fix、0.16.0 API）；1.x 无任何提及。 | src: https://nvidia.github.io/TensorRT-LLM/latest/release-notes.html | quote: "Added runtime support for seamless lookahead decoding." | type: official
- [C12] SmoothQuant 最后出现：0.19.0 "Fixed a Llama-3.2 SmoothQuant convert checkpoint issue. (#2677)"（另 0.15.0 "Added TensorRT native support for INT8 Smooth Quantization."）；1.x 无任何提及。 | src: https://nvidia.github.io/TensorRT-LLM/latest/release-notes.html | quote: "Fixed a Llama-3.2 SmoothQuant convert checkpoint issue. (#2677)" | type: official
- [C13] 1.2 的 spec-decoding 相关 removed 条目是 "Two-model speculative decoding"（非 Medusa/lookahead）。 | src: https://nvidia.github.io/TensorRT-LLM/latest/release-notes.html | quote: "[BREAKING CHANGE] Two-model speculative decoding removed." | type: official
- [C14] 1.2 另有 "[BREAKING CHANGE] TensorRT backend removed."；1.3 TRITON MoE backend "is deprecated as of TensorRT-LLM 1.3 (2026-09)"。 | src: https://nvidia.github.io/TensorRT-LLM/latest/release-notes.html | quote: "[BREAKING CHANGE] TensorRT backend removed." | type: official

### LICENSE
- [C15] 许可证为 Apache 2.0：LICENSE 文件首行 "Copyright (c) 2011-2026 NVIDIA CORPORATION & AFFILIATES."，次段 "This project is licensed under the Apache 2.0 license"；README badge "license-Apache 2"。 | src: https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/LICENSE | quote: "This project is licensed under the Apache 2.0 license" | type: official

## conflicts
- D6（已裁决）：Note 字面（"supports only Eagle3"）与正上方 7 项 decoding_type 列表冲突；按 Note 第二句（Eagle 别名 / v1-v2 不兼容）应判为「EAGLE 家族内仅 Eagle3」，非全局限制。页面无其他 PyTorch 限制句。若成稿曾引用该句证明「PyTorch 后端仅支持 Eagle3 一种 spec decoding」，应改判为错误表述。

## gaps
- tag 页只显示 "24 Sep 12:53" 无年份；年份取自 API published_at（2025-09-24）。未能用第二处官方页面交叉验证年份。
- releases.atom 截断只到 v1.3.0rc28，未含 v1.0.0 条目。
- release-notes 页 0.11.0 节在页面末尾截断，更早版本未覆盖（但 1.x 已完整核对）。

## leads
- 1.2 "[BREAKING CHANGE] Two-model speculative decoding removed." —— 若成稿涉及 DraftTarget/two-model spec decoding 的版本演进需核对（当前 spec-decoding 页仍列 DraftTarget，可能指旧 two-model 实现路径）。
- 1.3 (2026-09) 起 TRITON MoE backend deprecated；1.2 TensorRT backend removed —— 支持「PyTorch 是唯一后端」的时间线，间接佐证 Eagle3 句不可能是全局限制。
