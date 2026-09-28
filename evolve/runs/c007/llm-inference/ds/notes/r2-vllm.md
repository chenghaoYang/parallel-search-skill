# r2-vllm
question: 补 vLLM 三个格子级事实：vllm-gguf-plugin 仓库现状（状态/量化类型/硬件/安装用法）、Medusa 投机解码在 vLLM 的去向（release notes 有无 remove/deprecate）、enable_prefix_caching 默认值（stable 源码原句）
checked: https://docs.vllm.ai/en/latest/features/quantization/gguf.html, https://github.com/vllm-project/vllm-gguf-plugin, https://raw.githubusercontent.com/vllm-project/vllm-gguf-plugin/main/README.md, https://api.github.com/repos/vllm-project/vllm/releases (pages 1-3, 106 releases), https://docs.vllm.ai/en/latest/search/search_index.json, https://raw.githubusercontent.com/vllm-project/vllm/v0.11.0/vllm/config/cache.py, https://raw.githubusercontent.com/vllm-project/vllm/v0.13.0/vllm/config/cache.py, https://raw.githubusercontent.com/vllm-project/vllm/v0.30.0/vllm/config/cache.py

## claims
- [C1] vLLM 官方 GGUF 文档页将 GGUF 支持标注为高度实验性 | src: https://docs.vllm.ai/en/latest/features/quantization/gguf.html | quote: "Please note that GGUF support in vLLM is highly experimental and under-optimized at the moment, it might be incompatible with other features." | type: official
- [C2] GGUF 支持已从 vLLM 主仓库迁出到独立插件仓库 github.com/vllm-project/vllm-gguf-plugin | src: https://docs.vllm.ai/en/latest/features/quantization/gguf.html | quote: "GGUF support has migrated to OOT vllm-gguf-plugin . Make sure you have GGUF plugin installed before serving a GGUF model." | type: official
- [C3] 文档页安装方式为一行 pip 命令，用法是 repo_id:quant_type 格式 | src: https://docs.vllm.ai/en/latest/features/quantization/gguf.html | quote: "uv pip install vllm-gguf-plugin ... vllm serve unsloth/Qwen3-0.6B-GGUF:Q4_K_M --tokenizer Qwen/Qwen3-0.6B" | type: official
- [C4] 插件 README 自述定位为 in-tree 支持废弃后的 out-of-tree 插件，README 正文未自称 experimental | src: https://raw.githubusercontent.com/vllm-project/vllm-gguf-plugin/main/README.md | quote: "This plugin provides out-of-tree GGUF quantization support for vLLM after in-tree support deprecation ([vllm-project/vllm#39583])" | type: official
- [C5] 插件硬件前提只有 CUDA 或 ROCm 工具链（即 NVIDIA/AMD GPU） | src: https://raw.githubusercontent.com/vllm-project/vllm-gguf-plugin/main/README.md | quote: "### Prerequisites\n\n- CUDA toolkit or ROCm toolkit" | type: official
- [C6] README 测试覆盖的 GGUF 量化类型：Q6_K、Q8_0、IQ4_XS、Q4_K_M、Q4_0、UD-IQ2_XXS；VLM 为 Q4_0/Q4_K_M/UD-IQ2_XXS backbone + F16/BF16 projector；明确说兼容性不限于此列表 | src: https://raw.githubusercontent.com/vllm-project/vllm-gguf-plugin/main/README.md | quote: "The plugin uses vLLM's model implementations and a generic GGUF weight adapter, so model compatibility is broader than a fixed allowlist." | type: official
- [C7] 源码安装插件需关闭 build isolation，使 CUDA 扩展针对 vLLM 运行时所用 PyTorch 编译 | src: https://raw.githubusercontent.com/vllm-project/vllm-gguf-plugin/main/README.md | quote: "uv pip install -e . --no-build-isolation ... Disabling build isolation ensures that the CUDA extension is compiled against the same PyTorch installation used by vLLM at runtime." | type: official
- [C8] v0.9.0 release notes 记录 V1 引擎新增 Medusa 支持（PR #17956），非移除 | src: https://github.com/vllm-project/vllm/releases/tag/v0.9.0 | quote: "[Model] vLLM v1 supports Medusa by @skylee-01 in https://github.com/vllm-project/vllm/pull/17956" | type: official
- [C9] v0.13.0 release notes 仍在改进 Medusa，说明当时未移除 | src: https://github.com/vllm-project/vllm/releases/tag/v0.13.0 | quote: "**Speculative decoding**: Medusa GPU-CPU sync avoidance (#29723), async spec-decode improvements (#29624)." | type: official
- [C10] 当前（latest）文档 engine args / cli serve 的 --spec-method 枚举仍含 medusa，即该方法仍受支持，只是没有独立 feature 页 | src: https://docs.vllm.ai/en/latest/configuration/engine_args/ | quote: "longcat_flash_mtp, medusa, mimo_mtp, mimo_v2_mtp, minimax_m3_mtp, mlp_speculator, mtp" | type: official
- [C11] v0.11.0 源码中 enable_prefix_caching 为 Optional[bool] = None，docstring 说明 V1 默认启用 | src: https://raw.githubusercontent.com/vllm-project/vllm/v0.11.0/vllm/config/cache.py | quote: "enable_prefix_caching: Optional[bool] = None\n\"\"\"Whether to enable prefix caching. Enabled by default for V1.\"\"\"" | type: official
- [C12] 当前最新 release v0.30.0（2026-09-22）中默认值已改为显式 True；v0.13.0 同样为 bool = True | src: https://raw.githubusercontent.com/vllm-project/vllm/v0.30.0/vllm/config/cache.py | quote: "enable_prefix_caching: bool = True\n\"\"\"Whether to enable prefix caching.\"\"\"" | type: official

## conflicts
- 无文档间矛盾。注意版本演化：v0.11.0 用 None 哨兵值（"Enabled by default for V1"），v0.13.0/v0.30.0 改为显式 `bool = True`——同一事实的不同写法，非冲突。

## gaps
- 文档 GGUF 页本身未列支持的量化类型/硬件清单；该信息只存在于插件 README 的 "Tested model coverage" 表（C6）。
- Medusa 为何没有独立 feature 文档页：未找到官方说明；release notes（106 个 release 全量 grep "medusa"，v0.0.x–v0.30.0）无任何 remove/deprecate 条目。

## leads
- in-tree GGUF 废弃的追踪 issue：vllm-project/vllm#39583（README 引用）。
- 插件 README 还记录了 GGUF + MTP 投机解码用法（--speculative-config '{"method":"mtp",...}'），说明插件已接入 V1 spec decode。
