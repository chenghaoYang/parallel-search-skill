# r1-bun-ts-npm-nodeapi
question: Bun 如何原生执行 .ts 文件——是否做类型检查还是只做 transpile/strip types（用的什么机制，是否要求安装 typescript 包）？Bun 自带的包管理器细节：`bun install`、对 package.json 的支持、lockfile 格式（bun.lock 还是 bun.lockb，是文本格式还是二进制，最近是否有格式变化）、workspaces 支持、和 npm registry 的兼容程度？Bun 对 Node.js 内置模块/API 的兼容矩阵——官方给出的 node: 兼容模块清单或兼容度说法、原生插件（N-API/Node-API addon）支持现状？
checked: https://bun.sh/docs/runtime/typescript,https://bun.sh/docs/cli/install,https://bun.sh/docs/pm/lockfile,https://bun.sh/docs/runtime/nodejs-compat,https://bun.sh/docs/runtime/node-api,https://bun.sh/blog/bun-lock-text-lockfile,https://bun.sh/docs/runtime/transpiler,https://bun.sh/docs/typescript,https://bun.sh/docs/install/registries,https://bun.sh/docs/pm/workspaces,https://bun.sh/docs/runtime

## claims
- [C1] Bun TypeScript loader 不执行类型检查：Bun 的 TypeScript loader "strips out all TypeScript syntax" 后与 JS loader 行为相同，"Bun does not perform typechecking" | src: https://bun.sh/docs/runtime/typescript | quote: "Bun's TypeScript loader strips out all TypeScript syntax and then behaves identically to the JS loader. Bun does not perform typechecking." | type: official
- [C2] 不需要安装 typescript 包：Bun 内置 TypeScript 支持，可直接运行 .ts 文件而无需单独安装 typescript | src: https://bun.sh/docs/runtime/typescript | quote: "Bun natively supports TypeScript files" | type: official
- [C3] 类型定义需 @types/bun：编辑器中引用 Bun 全局需安装 `@types/bun` 作为开发依赖 | src: https://bun.sh/docs/typescript | quote: "To get TypeScript definitions for Bun's built-in APIs, install @types/bun" | type: official
- [C4] `bun install` 命令安装依赖：`bun install` 比 npm 快约 25 倍，安装所有 dependencies、devDependencies、optionalDependencies、peerDependencies | src: https://bun.sh/docs/cli/install | quote: "bun install is Bun's fast package manager command designed as a dramatically faster replacement for npm, yarn, and pnpm. It's up to 25x faster than npm install." | type: official
- [C5] bun.lock 为文本格式 JSONC：Bun v1.2 将默认 lockfile 从二进制改为文本格式 bun.lock，格式为 JSONC（如 tsconfig.json） | src: https://bun.sh/docs/pm/lockfile | quote: "Bun v1.2 changed the default to text-based bun.lock format" | type: official
- [C6] 二进制格式 bun.lockb 仍支持：binary lockfile `bun.lockb` 仍会继续支持 | src: https://bun.sh/docs/pm/lockfile | quote: "For existing projects with a bun.lockb file, Bun will continue to support the binary lockfile, without migration to the new lockfile" | type: official
- [C7] v1.1.39 引入文本 lockfile：Bun v1.1.39（2024年12月17日）引入了可用 `bun install --save-text-lockfile` 启用的 bun.lock | src: https://bun.sh/blog/bun-lock-text-lockfile | quote: "The text-based lockfile bun.lock was introduced in Bun v1.1.39 (December 17, 2024)" | type: official
- [C8] 文本 lockfile 性能优化：缓存状态下 bun.lock 比 bun.lockb "30% faster" | src: https://bun.sh/blog/bun-lock-text-lockfile | quote: "Cached bun install with the text-based lockfile is 30% faster compared to the binary bun.lockb format (v1.1.38)" | type: official
- [C9] 完整 package.json 支持：Bun 支持标准 package.json 字段包括 dependencies、devDependencies、optionalDependencies、peerDependencies、workspaces、overrides | src: https://bun.sh/docs/cli/install | quote: "Bun fully supports standard package.json fields" | type: official
- [C10] 自动 lockfile 迁移：运行 `bun install` 时，Bun 自动从 yarn.lock (v1)、package-lock.json (npm v2/3/4)、pnpm-lock.yaml 迁移 | src: https://bun.sh/docs/pm/lockfile | quote: "When running bun install in a project without bun.lock, Bun automatically migrates from yarn.lock, package-lock.json, pnpm-lock.yaml" | type: official
- [C11] Workspace 支持 glob 语法：`package.json` 中 workspaces 支持完整 glob 语法包括负模式 | src: https://bun.sh/docs/pm/workspaces | quote: "Bun supports full glob syntax, including negative patterns" | type: official
- [C12] Workspace 依赖协议：引用其他包使用 `workspace:` 协议，发布时被替换为实际版本 | src: https://bun.sh/docs/pm/workspaces | quote: "Reference other packages using the workspace: protocol" | type: official
- [C13] npm registry 兼容性：Bun 从 npm 的 .npmrc 读取配置，可用相同配置给 npm 和 Bun；默认从 npm 官方 registry (https://registry.npmjs.org/) 解析包 | src: https://bun.sh/docs/install/registries | quote: "Bun reads npm registry configuration from .npmrc" | type: official
- [C14] 作用域 registry 支持：在 bunfig.toml 的 [install.scopes] 可配置特定组织使用不同 npm registry | src: https://bun.sh/docs/install/registries | quote: "Configure private registries for specific organizations using the [install.scopes] section" | type: official
- [C15] 99% Node.js 测试套件兼容：Bun 通过 99% 的 Node.js 测试套件，每次发布前运行数千项测试 | src: https://bun.sh/docs/runtime/nodejs-compat | quote: "99% of Node.js's test suite passes" | type: official
- [C16] Node.js 模块分类状态：官方文档列举 node: 模块为完全实现（🟢）、部分实现（🟡）、未实现（🔴）三种状态 | src: https://bun.sh/docs/runtime/nodejs-compat | quote: "Bun supports most Node.js APIs with three status levels: 🟢 Fully implemented, 🟡 Partially implemented, 🔴 Not implemented" | type: official
- [C17] 完全实现模块清单：node:assert、node:buffer、node:console、node:dgram、node:dns、node:events、node:fs、node:http、node:os、node:path、node:querystring、node:readline、node:stream、node:timers、node:tty、node:url、node:zlib、node:http2、node:vm 等 | src: https://bun.sh/docs/runtime/nodejs-compat | quote: "Fully Implemented: node:assert, node:buffer, node:console, node:dgram, node:dns, node:events, node:fs, node:http, node:os, node:path, node:stream, node:timers, node:url, node:zlib, node:http2, node:vm" | type: official
- [C18] 部分实现模块：node:crypto（缺 ed448、x448、secp256k1 等）、node:https（缺 SNICallback）、node:worker_threads（缺 resourceLimits）、node:cluster、node:tls、node:test | src: https://bun.sh/docs/runtime/nodejs-compat | quote: "Partially Implemented: node:crypto - Missing ed448, x448, secp256k1; node:https - Missing SNICallback; node:worker_threads - Missing resourceLimits" | type: official
- [C19] 未实现模块：node:sea（Single Executable Applications），用 `bun build --compile` 替代 | src: https://bun.sh/docs/runtime/nodejs-compat | quote: "Not Implemented: node:sea - Use bun build --compile for executables instead" | type: official
- [C20] Node-API 95% 兼容：Bun 从零实现 Node-API 接口，大多数现有 Node-API 扩展开箱可用 | src: https://bun.sh/docs/runtime/node-api | quote: "Bun implements this interface from scratch, meaning most existing Node-API extensions work with Bun out of the box" | type: official
- [C21] Node-API 98% 测试套件：Bun v1.2.5 通过 Node 的 js-native-api 测试套件 98% | src: https://bun.sh/docs/runtime/nodejs-compat | quote: "Bun v1.2.5 passes 98% of Node's js-native-api test suite" | type: official
- [C22] .node 文件加载方式：通过 `require()` 或 `process.dlopen()` 加载 .node 文件（Node-API 模块） | src: https://bun.sh/docs/runtime/node-api | quote: "You can load .node files (Node-API modules) using require() or process.dlopen()" | type: official
- [C23] 全局对象兼容性：完全实现 AbortController、Blob、Buffer、console、fetch、process、require()、URL、URLSearchParams、WebSocket 等 | src: https://bun.sh/docs/runtime/nodejs-compat | quote: "Fully Supported: AbortController, Blob, Buffer, fetch, process, require(), URL, URLSearchParams, WebSocket" | type: official
- [C24] 内置 BoringSSL：node:crypto 后端使用 BoringSSL（非 OpenSSL），缺 ML-KEM-512、Ed448、X448、secp256k1 等算法 | src: https://bun.sh/docs/runtime/nodejs-compat | quote: "Backed by BoringSSL (not OpenSSL). Missing ML-KEM-512, Ed448, X448, secp256k1" | type: official
- [C25] Bun 测试优先 node:test：官方建议用 `bun:test` 代替 `node:test`，后者部分实现 | src: https://bun.sh/docs/runtime/nodejs-compat | quote: "Use bun:test instead of node:test for full feature support" | type: official

## conflicts
- 无冲突发现

## gaps
- 尚未找到 Bun 对特定 npm package 可安装性的定量阈值说法（如"支持 98% 的 npm 包"）
- npm registry 认证方式（如 npm token、bearer token 等）的完整支持清单未找到
- Workspace 中 peerDependencies 的具体处理逻辑（是否允许多版本共存）

## leads
- Bun 官方博客中关于 bun.lock 文本格式的详细性能对比：https://bun.sh/blog/bun-lock-text-lockfile
- Node.js 完整兼容矩阵页（包含每个模块的详细进度）：https://bun.sh/docs/runtime/nodejs-compat
- 从 npm/yarn/pnpm 迁移指南：https://bun.sh/guides/install/from-npm-install-to-bun-install
