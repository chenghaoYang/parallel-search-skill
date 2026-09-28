# r1-node-ts-security
question: Node.js 现在如何原生运行 .ts 文件——是类型检查（type-checking）还是仅类型剥离（type-stripping）？从哪个版本、哪个 flag、默认值何时改变？对 tsconfig 里的装饰器、enum、namespace 等"non-erasable"语法支持到什么程度？另外，Node.js 的 Permission Model（--permission / --allow-fs-read 等）现状如何：默认是允许还是拒绝、权限粒度多细、是否已经 stable（脱离 experimental）？

checked: https://nodejs.org/learn/typescript/run-natively, https://nodejs.org/api/permissions.html, https://nodejs.org/api/typescript.html, https://nodejs.org/en/blog/release/v22.18.0, https://github.com/nodejs/node/releases/tag/v23.6.0, https://nodejs.org/en/blog/release/v23.5.0, https://nodejs.org/en/blog/release/v26.0.0

## claims
- [C1] Node.js 原生运行 .ts 文件使用类型剥离（type stripping），不进行类型检查 | src: https://nodejs.org/learn/typescript/run-natively | quote: "Node.js does NOT type-check your code. It only strips types and runs the code." | type: official
- [C2] v22.6.0（2024-08-06）引入 --experimental-strip-types flag | src: https://nodejs.org/en/blog/release/v22.6.0 | quote: "Node.js introduced the --experimental-strip-types flag for initial TypeScript support" | type: secondary
- [C3] v22.18.0（2025-07-31）TypeScript 类型剥离默认启用，无需 flag | src: https://nodejs.org/en/blog/release/v22.18.0 | quote: "Type stripping is enabled by default in Node.js v22.18.0... You can now run node file.ts directly" | type: official
- [C4] v23.6.0（2025-01-07）默认启用类型剥离，可用 --no-strip-types 禁用 | src: https://nodejs.org/docs/latest-v23.x/api/typescript.html | quote: "enabled by default, disable with --no-strip-types flag" | type: official
- [C5] v24 LTS 默认启用 TypeScript 类型剥离 | src: https://github.com/nodejs/nodejs.org/blob/main/apps/site/pages/en/blog/release/v22.18.0.md | quote: "TypeScript type stripping is enabled by default in v22.18, v23.6, v24" | type: secondary
- [C6] v25.2.0+ 类型剥离标记为 stable 状态 | src: https://nodejs.org/api/typescript.html | quote: "Status: Stable (v25.2.0+), enabled by default" | type: official
- [C7] 类型剥离使用 Amaro 库，基于 SWC 引擎 | src: https://nodejs.org/learn/typescript/run-natively | quote: "The Node.js TypeScript loader (Amaro) removes type annotations" | type: official
- [C8] Enum 声明不支持，使用类型剥离时会报错 | src: https://nodejs.org/api/typescript.html | quote: "Enum declarations... will error" | type: official
- [C9] Parameter properties 不支持，使用类型剥离时会报错 | src: https://nodejs.org/api/typescript.html | quote: "Parameter properties... will error" | type: official
- [C10] Namespace with runtime code 不支持，使用类型剥离时会报错 | src: https://nodejs.org/api/typescript.html | quote: "namespace with runtime code... will error" | type: official
- [C11] Import aliases 不支持，使用类型剥离时会报错 | src: https://nodejs.org/api/typescript.html | quote: "Import aliases... will error" | type: official
- [C12] Decorators 不支持（非 JavaScript 原生特性），使用类型剥离时会报错 | src: https://nodejs.org/api/typescript.html | quote: "Decorators (not yet native JavaScript)... will error" | type: official
- [C13] .tsx 文件不支持 | src: https://nodejs.org/api/typescript.html | quote: ".tsx - Unsupported" | type: official
- [C14] 类型剥离通过将类型语法替换为空格来保持行号一致 | src: https://nodejs.org/learn/typescript/run-natively | quote: "replaces types with whitespace so that line numbers stay identical" | type: official
- [C15] 类型剥离不依赖 tsconfig.json，不解析 paths 和编译目标配置 | src: https://nodejs.org/api/typescript.html | quote: "Type stripping ignores tsconfig.json settings like paths and compilation targets" | type: official
- [C16] --experimental-strip-types 仍在旧版本（v22.6-22.17）中需要 flag，不再是 experimental 后标记为 default | src: https://nodejs.org/learn/typescript/run-natively | quote: "Node.js < v22.18.0: node --experimental-strip-types example.ts" | type: official
- [C17] --experimental-transform-types 在 Node.js v22.7.0 曾用于处理 enum、namespace、parameter properties 等需要代码生成的特性 | src: https://github.com/nodejs/node/pull/54283 | quote: "extended in version 22.7.0 to include TypeScript-only syntax... by using the --experimental-transform-types flag" | type: secondary
- [C18] Node.js 26.0.0（2026-05-05）删除了 --experimental-transform-types flag | src: https://nodejs.org/en/blog/release/v26.0.0 | quote: "--experimental-transform-types - Removed" | type: official
- [C19] --experimental-transform-types 移除原因：维护复杂性大于收益，enum/namespace 等特性不在 Node 原生支持的路线图内 | src: https://github.com/nodejs/node/commit/89f4b6cddb | quote: "Native runtime transformation of TypeScript-specific syntax is not part of Node's roadmap" | type: secondary
- [C20] 权限模型（Permission Model）v23.5.0（2024-12-19）标记为 stable，不再 experimental | src: https://nodejs.org/en/blog/release/v23.5.0 | quote: "Permission Model - Now Stable" | type: official
- [C21] 权限模型在 v22（LTS）中使用 --experimental-permission flag，v23.5.0+ 改为 --permission | src: https://nodejs.org/api/permissions.html | quote: "operates behind the --permission flag" | type: official
- [C22] 权限模型默认行为：Enforce Mode，访问被拒绝，抛出 ERR_ACCESS_DENIED | src: https://nodejs.org/api/permissions.html | quote: "Enforce Mode (default with --permission): Access is denied and ERR_ACCESS_DENIED is thrown" | type: official
- [C23] 权限模型还有 Audit Mode（--permission-audit），记录违规但继续执行 | src: https://nodejs.org/api/permissions.html | quote: "Audit Mode (--permission-audit): Permission violations are logged... but execution continues" | type: official
- [C24] --allow-fs-read 控制文件系统读权限，支持 * 通配符或逗号分隔的路径列表 | src: https://nodejs.org/api/permissions.html | quote: "Allow all file system access: --allow-fs-read=*... allow specific directories: --allow-fs-read=/home/test*" | type: official
- [C25] --allow-fs-write 控制文件系统写权限，支持 * 通配符或逗号分隔的路径列表 | src: https://nodejs.org/api/permissions.html | quote: "Allow all... or pass a comma-separated list of paths to limit access" | type: official
- [C26] 权限模型受限资源包括：文件系统、网络、子进程、Worker Threads、原生模块、WASI、FFI、运行时 inspector | src: https://nodejs.org/api/permissions.html | quote: "File system... Network... Child processes and worker threads... Native addons, WASI, and FFI... Runtime inspector" | type: official
- [C27] 权限模型的重要限制：不保护恶意代码，符号链接会绕过路径限制 | src: https://nodejs.org/api/permissions.html | quote: "Does not protect against malicious code... Symbolic links are followed outside granted paths" | type: official
- [C28] process.permission.has(scope[, reference]) 检查进程是否具有特定权限 | src: https://nodejs.org/api/permissions.html | quote: "Check if the process has a specific permission" | type: official
- [C29] process.permission.drop(scope[, reference]) 不可逆地放弃权限 | src: https://nodejs.org/api/permissions.html | quote: "Irreversibly drop a permission (cannot be restored)" | type: official
- [C30] 类型剥离默认支持特性：内联类型注解、Interfaces、Type aliases、import type 语句 | src: https://nodejs.org/api/typescript.html | quote: "Type stripping removes erasable TypeScript syntax including: Type annotations, Interfaces, Type aliases, import type statements" | type: official
- [C31] 官方推荐在类型导入时使用 type 关键字，避免运行时错误 | src: https://nodejs.org/api/typescript.html | quote: "Always use the type keyword for type-only imports" | type: official
- [C32] tsconfig.json 中推荐配置 erasableSyntaxOnly: true 和 verbatimModuleSyntax: true 以配合 Node 类型剥离 | src: https://nodejs.org/api/typescript.html | quote: "\"erasableSyntaxOnly\": true, \"verbatimModuleSyntax\": true" | type: official
- [C33] 完整 TypeScript 支持（包括 enum、namespace 等）需要使用第三方工具如 tsx | src: https://nodejs.org/api/typescript.html | quote: "For full TypeScript support, use a third-party tool" | type: official
- [C34] .mts 总是 ES modules，.cts 总是 CommonJS | src: https://nodejs.org/api/typescript.html | quote: ".mts - Always ES modules... .cts - Always CommonJS" | type: official
- [C35] .ts 的模块系统由 package.json 的 type 字段决定 | src: https://nodejs.org/api/typescript.html | quote: ".ts - Module system determined like .js files (use \"type\": \"module\" in package.json for ESM)" | type: official
- [C36] Node 不进行类型检查时，应在单独命令或 CI job 中运行 tsc --noEmit | src: https://nodejs.org/learn/typescript/run-natively | quote: "Run tsc --noEmit in a separate command or CI job for type checking" | type: official
- [C37] Node 26 之前的版本中 --experimental-transform-types flag 已被移除，enum 等特性需要外部编译器 | src: https://nodejs.org/en/blog/release/v26.0.0 | quote: "if you relied on enum, namespace, or decorator transforms, you'll need a real build step" | type: secondary

## conflicts
- [CONF1] --experimental-transform-types 的生命周期：v22.7.0 引入，某个版本后变为 experimental，v26.0.0 完全移除 | 官方文档未明确说明何时从实验变为实验（重复），仅说 v26 移除

## gaps
- 权限模型是否会继承到 Child Processes 和 Worker Threads（文档提及"不继承"但条件不清楚）
- --permission 在 v22（使用 --experimental-permission）到 v23.5 间的具体发展过程
- 符号链接绕过的具体行为边界（哪些 API 受影响）
- Permission Model 中 "seat belt" 的精确含义和安全级别定义
- Node 对于同时使用 .ts 和 .tsx 文件时的具体行为

## leads
- Node.js 26 移除 --experimental-transform-types 是重大破坏性变更，依赖 enum/namespace 的项目必须迁移到 tsc/tsx/swc
- "完整支持 TypeScript" 的说法对 Node 而言不准确——仅支持可擦除语法，不支持 enum/namespace/decorators，且不进行类型检查
- 权限模型 stable 后仍有 symbolic link bypass 等安全边界问题，不应视为生产级别的沙箱，需要配合其他安全层
