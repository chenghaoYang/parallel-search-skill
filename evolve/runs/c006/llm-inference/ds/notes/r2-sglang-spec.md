# r2-sglang-spec
question: SGLang `--speculative-algorithm` 的合法取值到底是哪些（裁决两官方页冲突）
checked: https://docs.sglang.io/docs/advanced_features/server_arguments.md, https://docs.sglang.io/docs/advanced_features/speculative_decoding.md, https://raw.githubusercontent.com/sgl-project/sglang/v0.5.20/python/sglang/srt/speculative/spec_info.py, https://raw.githubusercontent.com/sgl-project/sglang/v0.5.20/python/sglang/srt/speculative/spec_registry.py, https://raw.githubusercontent.com/sgl-project/sglang/v0.5.20/python/sglang/srt/arg_groups/fields/spec.py, https://raw.githubusercontent.com/sgl-project/sglang/v0.5.19/python/sglang/srt/server_args.py, https://raw.githubusercontent.com/sgl-project/sglang/v0.5.19/python/sglang/srt/speculative/spec_info.py, https://github.com/sgl-project/sglang/releases/tag/v0.5.20

## claims
- [C1] server_arguments.md 的 `--speculative-algorithm` Options 列只列 5 个值：`EAGLE`, `EAGLE3`, `NEXTN`, `STANDALONE`, `NGRAM` | src: https://docs.sglang.io/docs/advanced_features/server_arguments.md | quote: "`EAGLE`, `EAGLE3`, `NEXTN`, `STANDALONE`, `NGRAM`" | type: official
- [C2] speculative_decoding.md 列出 7 个值：`UNO`, `DFLASH`, `EAGLE`, `EAGLE3`, `STANDALONE`, `NGRAM`, `NEXTN`（注明 NEXTN 是 EAGLE 别名） | src: https://docs.sglang.io/docs/advanced_features/speculative_decoding.md | quote: "Algorithm to use: `UNO`, `DFLASH`, `EAGLE`, `EAGLE3`, `STANDALONE`, `NGRAM`, `NEXTN` (alias of `EAGLE`)" | type: official
- [C3] v0.5.20 源码 SpeculativeAlgorithm 枚举成员为 DFLASH, UNO, DSPARK, EAGLE, EAGLE3, FROZEN_KV_MTP, STANDALONE, NGRAM, NONE | src: https://raw.githubusercontent.com/sgl-project/sglang/v0.5.20/python/sglang/srt/speculative/spec_info.py | quote: "DFLASH = auto()\n    UNO = auto()\n    DSPARK = auto()\n    EAGLE = auto()\n    EAGLE3 = auto()\n    FROZEN_KV_MTP = auto()\n    STANDALONE = auto()\n    NGRAM = auto()\n    NONE = auto()" | type: official
- [C4] v0.5.20 CLI 帮助文本声明 builtins 为 EAGLE, EAGLE3, NEXTN, STANDALONE, NGRAM, DFLASH, DSPARK, UNO，且接受插件注册名 | src: https://raw.githubusercontent.com/sgl-project/sglang/v0.5.20/python/sglang/srt/arg_groups/fields/spec.py | quote: "Speculative algorithm. Builtins: EAGLE, EAGLE3, NEXTN, STANDALONE, NGRAM, DFLASH, DSPARK, UNO. Or any name registered via `SpeculativeAlgorithm.register`." | type: official
- [C5] NEXTN 不是独立枚举成员，而是保留别名，from_string 把 NEXTN 映射到 EAGLE | src: https://raw.githubusercontent.com/sgl-project/sglang/v0.5.20/python/sglang/srt/speculative/spec_registry.py | quote: "_RESERVED_ALIASES = frozenset({\"NEXTN\"})"（上方注释："to a builtin (e.g. NEXTN -> EAGLE)"） | type: official
- [C6] MTP 不是 --speculative-algorithm 的枚举值；MTP 通过 EAGLE 实现（文档示例用 EAGLE + num-steps 1 + topk 1） | src: https://docs.sglang.io/docs/advanced_features/speculative_decoding.md | quote: "We support MTP (Multi-Token Prediction) in SGLang by using speculative decoding"（示例 launch 用 --speculative-algorithm EAGLE） | type: official
- [C7] UNO 在 v0.5.20（2026-09-18 发布）才加入：v0.5.19 的 help 文本 builtins 为 "EAGLE, EAGLE3, NEXTN, STANDALONE, NGRAM, DFLASH, DSPARK"（无 UNO），v0.5.19 枚举亦无 UNO 成员 | src: https://raw.githubusercontent.com/sgl-project/sglang/v0.5.19/python/sglang/srt/server_args.py | quote: "Speculative algorithm. Builtins: EAGLE, EAGLE3, NEXTN, STANDALONE, NGRAM, DFLASH, DSPARK." | type: official
- [C8] v0.5.20 release notes 明确收录 "Add native UNO serving support" (#37667)，同版含多条 DFlash V2 / DSpark 条目 | src: https://github.com/sgl-project/sglang/releases/tag/v0.5.20 | quote: "[Speculative Decoding] Add native UNO serving support: #37667" | type: official
- [C9] speculative_decoding.md 同样不完整：未提 DSPARK、FROZEN_KV_MTP（v0.5.20 代码中已是合法 builtin/枚举值） | src: https://docs.sglang.io/docs/advanced_features/speculative_decoding.md | quote: "speculative decoding options, including EAGLE-2/EAGLE-3, MTP, UNO, DFLASH, classic draft-model decoding, and an NGRAM-based variant" | type: official
- [C10] argparse 层面无固定 choices 白名单：from_string 先查枚举成员名，再查保留别名，再查 SpeculativeAlgorithm.register 的插件注册表，未命中抛 ValueError | src: https://raw.githubusercontent.com/sgl-project/sglang/v0.5.20/python/sglang/srt/speculative/spec_info.py | quote: "return cls[upper] ... if upper in _RESERVED_ALIASES: return cls.EAGLE ... raise ValueError(f\"Unknown speculative algorithm name: {name}\")" | type: official

## conflicts
- 裁决：两页都滞后于代码，但方向相反。speculative_decoding.md 更接近正确——UNO、DFLASH 在 v0.5.20 代码中确为合法取值（UNO 自 v0.5.20 起，DFLASH 更早）；server_arguments.md 的 5 值枚举已过时（漏 DFLASH、DSPARK、UNO，FROZEN_KV_MTP 亦未列）。v0.5.20 事实集合 = {EAGLE, EAGLE3, STANDALONE, NGRAM, DFLASH, DSPARK, UNO, FROZEN_KV_MTP} + 别名 NEXTN→EAGLE + 插件注册名；NONE 为内部值。grid.md 填：合法 builtin 为 EAGLE/EAGLE3/NEXTN(=EAGLE)/STANDALONE/NGRAM/DFLASH/DSPARK/UNO（v0.5.20），文档两页不一致以代码为准。

## gaps
- FROZEN_KV_MTP 是否对用户公开/可用（枚举接受该字符串，但代码内有 FIXME："Remove FROZEN_KV_MTP here once we have established support for it in the scheduler"），未见文档说明。
- 未逐版定位 DFLASH/DSPARK 各自首次出现的 release（v0.5.19 已在，早于本轮核查范围）。

## leads
- server_arguments.md 疑为自动生成的参数表，其 Options 列滞后于 spec.py help 文本，类似错位可能波及其他参数。
