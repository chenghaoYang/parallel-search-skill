# r2-ts-runtime-features
question: Deno 2 和 Bun 的运行时在遇到 TypeScript 的 enum、带运行时代码的 namespace、参数属性（parameter properties）、legacy/experimental decorators 这几类"non-erasable"语法时，具体行为是什么——是像 Node.js 那样直接报错拒绝运行，还是像完整的 TypeScript 编译器一样把它们转换（transpile）成等价 JS 代码后正常执行？
checked: https://docs.deno.com/runtime/fundamentals/typescript/,https://docs.deno.com/runtime/reference/ts_config_migration/,https://bun.com/docs/runtime/typescript,https://bun.com/docs/runtime/transpiler,https://bun.com/blog/bun-v1.1.18,https://bun.com/blog/bun-v1.0.3,https://bun.com/blog/bun-v1.3.10,https://docs.deno.com/runtime/reference/cli/transpile/

## claims
- [C1] Deno 2 支持 enum（无需 flag）：官方文档明确说"Full TypeScript language support: Features like enums...work without flags" | src: https://docs.deno.com/runtime/fundamentals/typescript/ | quote: "Full TypeScript language support: Features like enums and namespaces with runtime values work without flags" | type: official
- [C2] Deno 2 支持 parameter properties（无需 flag）：官方文档同上明确列举 | src: https://docs.deno.com/runtime/fundamentals/typescript/ | quote: "Full TypeScript language support...parameter properties work without flags" | type: official
- [C3] Deno 2 仅支持 declare namespace，不支持 runtime namespace：根据文档总结，只有"declare namespace"被支持，runtime namespace 是 legacy TypeScript 语法不被支持 | src: https://docs.deno.com/runtime/fundamentals/typescript/ | quote: "declare namespace is supported" | type: official
- [C4] Deno 2 使用 SWC 作为 transpiler 来处理 TypeScript：Deno 的运行时编译管道采用 SWC 编译器，它会把 enum 转换成 IIFE 构造函数 | src: https://docs.deno.com/runtime/reference/cli/transpile/ | quote: "using Deno.transpileOnly() with an enum, the enum would be rewritten to an IIFE" | type: official
- [C5] Deno 2 decorators 需要在配置中启用：JSX transform、decorators、target 等 emit 设置来自 deno.json（或 tsconfig.json）的 compilerOptions | src: https://docs.deno.com/runtime/fundamentals/typescript/ | quote: "emit settings come from compilerOptions in your deno.json" | type: official
- [C6] Bun 支持 enum 并在 v1.1.18+ 支持内联优化：Bun 的 transpiler 支持 TypeScript enum 值内联，这在 Bun 的 runtime、bun build、bun test 中默认启用 | src: https://bun.com/blog/bun-v1.1.18 | quote: "Bun's optimizing transpiler now supports inlining TypeScript enum values...Enabled by default in Bun's runtime" | type: official
- [C7] Bun 支持 namespace 并在 v1.1.18+ 修复 namespace merging：duplicate namespace 声明现在正确地被合并成单个共享声明 | src: https://bun.com/blog/bun-v1.1.18 | quote: "TypeScript Namespace Merging: Duplicate namespace declarations are now properly merged" | type: official
- [C8] Bun v1.0.3+ 支持 emitDecoratorMetadata（legacy/experimental decorators）：此功能启用通过 reflect-metadata 为 decorators 生成元数据，对 NestJS/TypeORM 支持至关重要 | src: https://bun.com/blog/bun-v1.0.3 | quote: "emitDecoratorMetadata...enables the generation of metadata for decorators via reflect-metadata. The addition of emitDecoratorMetadata dramatically improves Nest.js support" | type: official
- [C9] Bun v1.3.10+ 完整支持 TC39 stage-3 ES decorators：包括 accessor 关键字、decorator metadata via Symbol.metadata、正确的评估顺序 | src: https://bun.com/blog/bun-v1.3.10 | quote: "Bun now supports modern (non-legacy) TypeScript decorators...accessor keyword, decorator metadata via Symbol.metadata" | type: official
- [C10] Bun 的 transpiler API 支持 TypeScript 代码转换：Bun.Transpiler 的 transformSync/transform 方法将 TypeScript 代码转换为 vanilla JavaScript | src: https://bun.com/docs/runtime/transpiler | quote: "The transpiler does not resolve modules or execute the code. The result is a string of vanilla JavaScript code." | type: official

## conflicts
- Deno 文档对"namespace with runtime values support"的说法与 R1 结论冲突：R1 说"only declare namespace is supported"，但官方文档 C1 引用中同时说"namespaces with runtime values work without flags"。需要直接测试或查找更具体的 issue/PR 来确认 Deno 是否真的支持 namespace 生成的运行时代码（即 IIFE）还是只支持类型声明。

## gaps
- parameter properties 在 Bun 中的支持情况未找到官方明确说明（无"不支持"清单，推断为默认支持）
- Deno 2 对 legacy decorators（experimentalDecorators: true）的具体运行时支持情况（是转译还是报错）未在官方文档中找到明确说法
- Bun 对 parameter properties 的官方立场（支持或不支持）未显式陈述

## leads
- Deno GitHub Issue #12102 (swc-project/swc) 提到"TypeScript enum transform does not fold namespace member access"，可能提供 Deno 中 namespace 运行时行为的线索
- 直接在 Deno 2 和 Bun 中执行测试代码（enum、namespace、parameter properties、decorators）来验证运行时行为，而不依赖文档推理
- Bun 的 bunfig.toml 文档或 tsconfig 支持情况可能有关于 TypeScript 特性支持的更多细节
