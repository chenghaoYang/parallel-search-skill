# r1-deno-ts-npm
question: Deno 2 如何原生执行 .ts 文件（类型检查程度如何、tsconfig.json 支持范围）？更重要的是：Deno 2 对 npm 包、package.json、node_modules 目录的支持现状具体是什么——`npm:` specifier 怎么用、是否会直接读取项目里的 package.json 的 dependencies 并像 Node 一样跑、是否默认在磁盘上生成 node_modules 目录（还是走全局缓存）、这和 Deno 1.x 的路线（URL import、无 node_modules）比有什么变化、是否需要额外配置（如 deno.json 里的字段）才能启用这些兼容行为？和 JSR（Deno 自己的注册表）是什么关系？
checked: https://docs.deno.com/runtime/fundamentals/node/, https://docs.deno.com/runtime/fundamentals/typescript/, https://docs.deno.com/runtime/reference/deno_json/, https://docs.deno.com/runtime/reference/ts_config_migration/, https://docs.deno.com/runtime/fundamentals/workspaces/, https://docs.deno.com/runtime/manual/node/npm_specifiers/, https://docs.deno.com/examples/npm/, https://deno.com/blog/v2.0, https://deno.com/blog/v2.0-release-candidate, https://deno.com/blog/jsr_open_beta

## claims
- [C1] Deno 原生执行 .ts 文件无需编译器或配置，`deno run main.ts` 直接运行 | src: https://docs.deno.com/runtime/fundamentals/typescript/ | quote: "Run `.ts` files directly. No `tsc`, no build step, no config." | type: official
- [C2] 执行时 Deno 去掉类型信息转为 JS 后交给 V8，不做类型检查 | src: https://docs.deno.com/runtime/fundamentals/typescript/ | quote: "Deno strips the types and hands the resulting JavaScript to V8. This is fast, happens in-process, and is cached, but it does not look at whether the types are correct." | type: official
- [C3] `deno check` 提供完整类型检查，等价于 `tsc --noEmit`，默认启用严格模式 | src: https://docs.deno.com/runtime/fundamentals/typescript/ | quote: "Deno also ships the type checker: deno check plays the role of tsc --noEmit, with strict mode on by default." | type: official
- [C4] Deno 自动检测并使用现有 tsconfig.json 文件，无需配置 | src: https://docs.deno.com/runtime/reference/ts_config_migration/ | quote: "existing `tsconfig.json` files from Node.js workspaces work out-of-the-box. Deno automatically discovers and processes them" | type: official
- [C5] 通过 `npm:` 前缀导入 npm 包，格式为 `npm:[@scope]/[package]@[version]` | src: https://docs.deno.com/runtime/manual/node/npm_specifiers/ | quote: "The npm specifier format in Deno follows this pattern: `npm:[@][/]`" | type: official
- [C6] npm 包导入示例：`import * as emoji from "npm:node-emoji"` | src: https://docs.deno.com/runtime/fundamentals/node/ | quote: "Import npm packages directly: import * as emoji from \"npm:node-emoji\"" | type: official
- [C7] Deno 默认不创建本地 node_modules，改用全局缓存（"none" 模式） | src: https://docs.deno.com/runtime/fundamentals/node/ | quote: "Deno instead resolves npm packages from a central global cache and does not create a `node_modules` directory." | type: official
- [C8] 使用全局缓存时项目目录保持清洁，npm 包在首次运行时下载并存入全局缓存 | src: https://docs.deno.com/runtime/manual/node/npm_specifiers/ | quote: "Deno downloads the package on first run and stores it in a global cache, so your project directory stays clean." | type: official
- [C9] Deno 理解 package.json 文件，支持其中的 dependencies、scripts（via `deno task`）和 `type` 字段 | src: https://docs.deno.com/runtime/fundamentals/node/ | quote: "Deno understands `package.json` files, respecting dependencies, scripts (via `deno task`), the `type` field" | type: official
- [C10] nodeModulesDir 有三种模式：`"none"`（默认，全局缓存）、`"auto"`（自动创建本地目录）、`"manual"`（用户手动维护） | src: https://docs.deno.com/runtime/fundamentals/node/ | quote: "Three modes are available: None (default): Uses global cache; keeps projects clean. Auto: Creates local `node_modules` when needed. Manual: Requires explicit `deno install` step." | type: official
- [C11] Deno 1.x 默认行为：package.json 存在时自动创建 node_modules | src: https://docs.deno.com/runtime/reference/migration_guide/ | quote: "In Deno 1.x: When a `package.json` file existed, npm packages were automatically installed into `node_modules`." | type: official
- [C12] Deno 2.x 关键变化：npm 包不再自动安装，推荐使用 `deno install` | src: https://docs.deno.com/runtime/reference/migration_guide/ | quote: "In Deno 2.x: npm packages are no longer installed by default when there is a package.json and instead running `deno install` is recommended." | type: official
- [C13] Deno 2.x 默认 nodeModulesDir 从 Deno 1.x 的 `true` 改为 `"manual"` | src: https://docs.deno.com/runtime/reference/migration_guide/ | quote: "Default behavior with package.json: Deno 1.x default: `true` (auto-installing). Deno 2.x default: `manual` (requires explicit user management)" | type: official
- [C14] 保持 Deno 1.x 行为需在 deno.json 中设置 `"nodeModulesDir": "auto"` | src: https://docs.deno.com/runtime/reference/migration_guide/ | quote: "To preserve automatic dependency installation, add this to your `deno.json`: {\"nodeModulesDir\": \"auto\"}" | type: official
- [C15] `preferPackageJson` 设为 true 时，`deno add`、`deno install <pkg>`、`deno remove` 命令改为写入 package.json | src: https://docs.deno.com/runtime/reference/deno_json/ | quote: "With this enabled, `deno add`, `deno install <pkg>`, and `deno remove` write to `package.json`, creating one if it does not exist." | type: official
- [C16] `jsrDepsInNodeModules` 启用时，JSR 依赖通过 JSR 的 npm 兼容注册表安装，`jsr:@david/dax` 被改写为 `npm:@jsr/david__dax` | src: https://docs.deno.com/runtime/reference/deno_json/ | quote: "Each `jsr:` specifier is rewritten to its npm form (`jsr:@david/dax` becomes `npm:@jsr/david__dax`, served from `https://npm.jsr.io`) and installed into `node_modules`" | type: official
- [C17] JSR（JavaScript Registry）是 TypeScript 原生、ESM 专有的现代包注册表 | src: https://deno.com/blog/jsr_open_beta | quote: "JSR is a \"TypeScript-first ESM package registry\" designed to complement rather than replace npm." | type: official
- [C18] JSR 支持发布 TypeScript 源代码无需编译步骤，自动生成 .d.ts、JS 转译和 API 文档 | src: https://deno.com/blog/jsr_open_beta | quote: "JSR accepts TypeScript source code directly—no build step required from authors. The platform automatically generates: .d.ts type declaration files, JavaScript transpilation for Node environments, API documentation" | type: official
- [C19] JSR 设计用于跨运行时支持，包括 Deno、Node、Bun 等 | src: https://deno.com/blog/jsr_open_beta | quote: "Multi-runtime support: works with Deno, Node, and other modern runtimes." | type: official
- [C20] Deno 2.0 发布公告称实现"full Node and npm backwards compatibility" | src: https://deno.com/blog/v2.0 | quote: "Deno 2 combines the simplicity, security, and performance of Deno 1 with full Node and npm backwards compatibility." | type: official
- [C21] Deno 2 无 package.json 和 node_modules 时，npm 包安装在全局缓存中 | src: https://deno.com/blog/v2.0 | quote: "Without `package.json` and the `node_modules` directory, Deno will install your package in the global cache." | type: official
- [C22] Deno 2 支持 package.json、node_modules 和 npm workspaces | src: https://deno.com/blog/v2.0 | quote: "seamlessly runs existing Node applications, supporting `package.json`, `node_modules`, and npm workspaces" | type: official
- [C23] `deno install` 命令比 npm 冷缓存快 15%，热缓存快 90% | src: https://deno.com/blog/v2.0 | quote: "Package Management: Three new commands streamline dependency handling—`deno install` (15% faster than npm with cold cache, 90% faster with hot cache)" | type: official

## conflicts
- Deno 1.x vs 2.x node_modules 默认行为完全相反：1.x 当 package.json 存在时自动创建 node_modules，2.x 默认改为 "manual"（不自动创建），用户需显式 `deno install` 或配置 `nodeModulesDir: "auto"`

## gaps
- tsconfig.json 中具体哪些选项 Deno 支持、哪些不支持（已知不支持 target、outDir 等，但具体列表未完全获取）
- `deno check` 的 strict 模式具体默认启用的规则有哪些
- npm 包在全局缓存中的具体位置和管理方式
- Deno 2 中 bare imports（如 `import "chalk"`）是否完全支持

## leads
- Deno 1.x→2.x 最重要的变化：node_modules 策略从自动创建改为需要显式 `deno install` 或设置 `nodeModulesDir: "auto"`，这影响现有 package.json 项目的迁移路径
- JSR 与 npm 互补：JSR 用于 TypeScript 原生包，npm 用于传统 JavaScript 包，两者在 Deno 中可以通过 `jsrDepsInNodeModules` 共存于本地 node_modules
