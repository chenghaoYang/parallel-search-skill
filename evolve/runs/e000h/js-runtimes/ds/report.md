# Node.js / Deno 2 / Bun：2026 年怎么选

> 截至 2026-09-24。面向已用 Node、评估要不要上 Deno 2/Bun 的开发者。

## 0. 一屏看懂

1. **"原生支持 TypeScript"三家差距比想象中大**。Node 纯类型剥离，不检查类型，对 enum、带运行时代码的 namespace、参数属性、装饰器直接**报错**，须外接 tsc/tsx[2][4]。Deno 官方原话"enums and namespaces with runtime values work without flags"，enum 被 SWC 转译成 IIFE 正常执行[13][28]；Bun 支持 enum 内联/namespace 合并(v1.1.18+)，及 NestJS/TypeORM 依赖的 legacy decorators(v1.0.3+)、TC39 新装饰器(v1.3.10+)[44-46]。结论：Deno/Bun 接近"完整"TS 支持，Node 仅剥离可擦除语法——装饰器密集的框架代码在 Node 原生执行下跑不动。
2. **Deno 2 确实能直接用 npm 包和 package.json**，官方称"full Node and npm backwards compatibility"[17]；但默认安装行为在 2.0 反转，是最容易踩的迁移坑（第 3 节）。
3. **权限模型三条不同的路**：Node 默认不设防，传 `--permission` 才 opt-in 变"默认拒绝"[5][6]；Deno **无需 flag**，运行时内建默认拒绝文件/网络/环境变量/子进程[18]；Bun **无运行时权限系统**——官方立场是"静态分析后从二进制去掉不需要的能力，比运行时检查更安全"[47]；`Bun.Security` 只是装包阶段供应链扫描器，与运行时权限无关[48]。
4. **内置工具链：Deno 最全，Bun 次之，Node 最少**（详见 D4）。Deno 自带 test/fmt/lint/compile/bundle[21-25]；Bun 自带 test/build/run 但无格式化器与 linter[35-37]；Node 仅 `node:test`+`--watch`，无打包器/格式化器/linter[7][8][12]。
5. **Node API 兼容，Bun 数字更具体**：Bun 称通过 99% Node 测试套件、Node-API 98%[32][33]；Deno 2.8 通过 75%+ Node 自身测试套件[15]。
6. **部署平台，Bun 文档最详细**：Vercel/Docker/Lambda/Railway/Render/Cloud Run/DigitalOcean 均有官方指南[39-43]；Deno Deploy 2.0 重写，98%+ npm 兼容(二手)，仍 beta、1GB/512MB 上限[26][27]；Node 无专门部署指南页——它是默认基线，不是缺口。

## 1. Taxonomy

**分类轴**：默认安全姿态 × 对 Node/npm 生态的兼容策略——同一条轴也解释了 TS 支持深度差异：Deno/Bun 从第一天追求"像 JS 一样用 TS"，Node 是后加的最小化剥离。

| 家族 | 默认安全姿态 | 生态策略 |
|---|---|---|
| Node.js（基线） | 不设防；`--permission` 后才 opt-in 变默认拒绝 | 自己即生态 |
| Deno 2（沙箱优先） | 运行时内建默认拒绝，无需 flag | 2.0 起转向高兼容，安全默认值未变 |
| Bun（速度优先） | 无运行时权限系统，靠编译期精简替代 | 第一天起就高兼容 |

**维度**：D1 TS 执行模型 · D2 包管理/npm · D3 权限模型 · D4 内置工具链 · D5 `node:`/原生插件兼容 · D6 平台支持。

## 2. 对照矩阵

### D1 TypeScript 执行模型
| | Node.js | Deno 2 | Bun |
|---|---|---|---|
| 运行方式 | 类型剥离(Amaro/SWC)，默认开启于 v22.18/v23.6[2][3] | 剥离类型交给 V8，同时用 SWC 完整转译[13] | 剥离/转译全部 TS 语法[29] |
| 类型检查 | 不检查，需另跑 `tsc --noEmit`[1] | `deno check` 内置，默认 strict[13] | 不检查，编辑器类型靠 `@types/bun`[29] |
| enum/namespace(运行时)/参数属性 | **直接报错**；v26 移除了曾用于转换它们的 flag[2][4] | ✅ 官方"work without flags"，enum→IIFE[13][28] | ✅ enum 内联、namespace 合并自 v1.1.18[44] |
| legacy/TC39 装饰器 | **直接报错**，非原生 JS 语法[2] | ❓ 未查到官方明确声明 | ✅ legacy(v1.0.3+，NestJS 必需)+TC39(v1.3.10+)[45][46] |
| .tsx | 不支持[2] | ❓ 未查到一手确认 | ❓ 未查到一手确认 |

### D2 包管理与 npm 兼容
| | Node.js | Deno 2 | Bun |
|---|---|---|---|
| 包管理器 | npm 随分发[11] | 内置 `deno install`[17] | 内置 `bun install`，称比 npm 快 25 倍[31] |
| package.json | 标准 exports/imports[10] | 原生理解 deps/scripts(`deno task`)/type[15] | 完整支持标准字段[31] |
| node_modules 默认行为 | 标准 | **manual**：2.x 需显式 `deno install`，1.x 自动创建[16] | 默认生成 |
| lockfile | package-lock.json | 内部锁定（未细查） | `bun.lock`(文本 JSONC，v1.2 起默认，取代二进制 `bun.lockb`)[30] |
| Yarn/pnpm | Corepack，需 `corepack enable`[9] | 不适用(`npm:`/`jsr:` specifier) | 自动迁移 yarn.lock/pnpm-lock.yaml[30] |

### D3 权限模型
| | Node.js | Deno 2 | Bun |
|---|---|---|---|
| 默认行为 | 允许一切，除非传 `--permission`[5] | **拒绝**文件/网络/环境变量/子进程[18] | 允许一切，无运行时权限系统[47] |
| 设计立场 | Stable v23.5.0+，opt-in enforce[6] | 自 1.0 起核心设计[18] | 编译期精简替代运行时检查[47]；沙箱功能请求未实现(#6617) |
| 粒度 | `--allow-fs-read/write=path` 路径级[5] | `--allow-net/read/write/env/sys/run/ffi`，域名/路径级[19] | 仅 `bun pm trust` 控制 postinstall；`Bun.Security` 是装包期扫描器，非权限系统[48] |
| 一键放行/配置声明 | 无 | `-A`（等价 Node 无沙箱）；2.5+ 可在 deno.json 声明[19][20] | 不适用 |

### D4 内置工具链
| | Node.js | Deno 2 | Bun |
|---|---|---|---|
| 测试 | `node:test`(v18+，Stable v20+)，mock/快照/覆盖率[7] | `deno test`：filter/watch/parallel/coverage[21] | `bun test`：并发/coverage/watch/snapshot[34] |
| 打包/编译 | 无官方 bundler[8][12] | `deno bundle`(实验性)；`deno compile` 跨平台单文件[24][25] | `bun build`：esm/cjs/iife；`--compile` 跨平台单文件[35][36] |
| 格式化/Lint | 无[8][12] | `deno fmt`(25+ 类型)；`deno lint`(100+ 规则)[22][23] | 无内置，需自接 Prettier/ESLint[37] |
| 脚本执行 | `node --run <script>`[8] | `deno task` | `bun run`，支持生命周期钩子[37] |

### D5 Node API 兼容层
| | Deno 2 | Bun |
|---|---|---|
| 官方兼容度 | 2.8+ 通过 75%+ Node 测试套件[15] | 通过 99% Node 测试套件；Node-API 98%[32][33] |
| 已知限制 | 部分 API partial；原生插件需本地 node_modules[15] | crypto 缺 ed448/x448/secp256k1(BoringSSL)；`node:sea` 未实现，用 `--compile` 替代[32] |

### D6 部署平台
| 平台 | Deno 2 | Bun |
|---|---|---|
| 自家平台 | Deno Deploy：2.0 重写；1GB 部署/512MB 内存上限，beta 不保运行时间[26][27] | 无 |
| Vercel/Docker/Serverless/PaaS | ❓ 本轮未查 | Vercel(公测)、Docker(`oven/bun`)、AWS Lambda、Cloud Run、DigitalOcean(均经 Docker)、Railway(零配置)、Render(选 Runtime="Node")[39-43] |
| Node.js | 无专门"平台支持"页——默认基线，不构成决策差异点 | — |

## 3. 变体与适配层

**Deno 1→2 的 npm 兼容路线反转**：1.x 靠 URL import + 不落地 node_modules 是卖点；2.0 为"无缝跑现有 Node 应用"引入 package.json/node_modules 支持[17]，但默认安装行为比 1.x 更保守（`manual` 而非自动）[16]——能力变强，默认动作变少，容易误判为"装不上包"。

**Bun 的 lockfile 格式反转**：二进制 `bun.lockb` → v1.1.39 引入文本 `bun.lock`(JSONC) → v1.2 起默认文本格式，旧项目不强制迁移[30]。

## 4. 用户需要知道的坑

1. **"Node 也能跑 .ts 了"不等于"Node 支持 TypeScript"**：项目里一旦用了 enum、namespace、参数属性或装饰器（NestJS/TypeORM/Angular 常见），Node 直接报错退出，须走 tsc/tsx/esbuild；同样代码在 Deno、Bun 上可原生跑[2][4][45]。
2. **Deno 2 项目"装不上包"通常是 `nodeModulesDir` 默认值变了**：从 1.x 迁移的项目依赖自动生成的 node_modules，需在 deno.json 加 `"nodeModulesDir":"auto"` 或跑 `deno install`[16]。
3. **Corepack 不是默认开启的**：内置了也要先手动 `corepack enable` 才能用 yarn/pnpm[9]。
4. **Deno 的 `-A` 官方原话："等价于在 Node.js 里跑不受信任的代码"**：全局 `-A` 等于放弃 Deno 核心卖点，仅建议调试用[19]。
5. **Render 部署 Bun 时 Runtime 字段要选"Node"**：不是选错，Render 没有单独 Bun 分类，Build/Start Command 手动填[43]。
6. **Bun 在 Cloudflare 只有 Pages 被提及、无独立部署指南**：和 Vercel/Railway/Render 不是一个层级，先自己跑通一次。

## 5. 未决与置信度

- Deno 对 legacy decorators 的运行时处理未在官方文档找到明确声明（enum/namespace/参数属性已明确支持，装饰器单独存疑）；文档中"namespaces with runtime values work without flags"与"declare namespace is supported"两处表述存在阅读歧义，未做代码实测，按更完整的前者为准。
- Bun 对参数属性无官方明确声明，按"无不支持清单"推断为支持。
- Node.js"无内置 bundler/formatter/linter"缺乏官方直接反面声明，结论维持但引用降级为推断性。
- Deno "98%+ npm 包兼容"表述偏营销，标二手；Deno Deploy 是否原生支持 `npm:` specifier 未专门确认。
- Node.js、Deno 在 Vercel/Docker/Lambda 等平台的支持现状本轮未查（Bun 已查全），不作为对比依据。
- Bun 权限模型的社区请求（issue #6617/#25929）仍开放未实现，不代表官方路线图。

## 来源
[1] Run TypeScript natively — https://nodejs.org/learn/typescript/run-natively
[2] Modules: TypeScript — https://nodejs.org/api/typescript.html
[3] v22.18.0 Release — https://nodejs.org/en/blog/release/v22.18.0
[4] v26.0.0 Release — https://nodejs.org/en/blog/release/v26.0.0
[5] Permissions — https://nodejs.org/api/permissions.html
[6] v23.5.0 Release — https://nodejs.org/en/blog/release/v23.5.0
[7] Test runner — https://nodejs.org/api/test.html
[8] Command-line API — https://nodejs.org/api/cli.html
[9] Corepack (GitHub) — https://github.com/nodejs/corepack
[10] Packages — https://nodejs.org/api/packages.html
[11] Download page — https://nodejs.org/en/download
[12] Publishing a package — https://nodejs.org/learn/modules/publishing-a-package
[13] TypeScript — https://docs.deno.com/runtime/fundamentals/typescript/
[14] tsconfig migration — https://docs.deno.com/runtime/reference/ts_config_migration/
[15] Node & npm compatibility — https://docs.deno.com/runtime/fundamentals/node/
[16] Migration guide 1.x→2.x — https://docs.deno.com/runtime/reference/migration_guide/
[17] Announcing Deno 2 — https://deno.com/blog/v2.0
[18] Security — https://docs.deno.com/runtime/fundamentals/security
[19] Permissions reference — https://docs.deno.com/runtime/reference/permissions
[20] deno.json reference — https://docs.deno.com/runtime/reference/deno_json
[21] CLI: test — https://docs.deno.com/runtime/reference/cli/test
[22] CLI: fmt — https://docs.deno.com/runtime/reference/cli/fmt
[23] CLI: lint — https://docs.deno.com/runtime/reference/cli/lint
[24] CLI: compile — https://docs.deno.com/runtime/reference/cli/compile
[25] CLI: bundle — https://docs.deno.com/runtime/reference/cli/bundle
[26] Deno Deploy docs — https://docs.deno.com/deploy
[27] Deploy pricing & limits — https://docs.deno.com/deploy/pricing_and_limits
[28] CLI: transpile — https://docs.deno.com/runtime/reference/cli/transpile/
[29] TypeScript — https://bun.sh/docs/runtime/typescript
[30] Lockfile — https://bun.sh/docs/pm/lockfile
[31] bun install — https://bun.sh/docs/cli/install
[32] Node.js compatibility — https://bun.sh/docs/runtime/nodejs-compat
[33] Node-API — https://bun.sh/docs/runtime/node-api
[34] Test runner — https://bun.com/docs/test
[35] Bundler — https://bun.com/docs/bundler
[36] Single-file executables — https://bun.com/docs/bundler/executables
[37] Runtime — https://bun.com/docs/runtime
[38] Bun.Security reference — https://bun.com/reference/bun/Security
[39] Deploy to Vercel — https://bun.com/guides/deployment/vercel
[40] Docker — https://bun.com/guides/ecosystem/docker
[41] AWS Lambda — https://bun.com/guides/deployment/aws-lambda
[42] Railway — https://bun.com/guides/deployment/railway
[43] Render — https://bun.com/guides/deployment/render
[44] Bun v1.1.18 blog — https://bun.com/blog/bun-v1.1.18
[45] Bun v1.0.3 blog — https://bun.com/blog/bun-v1.0.3
[46] Bun v1.3.10 blog — https://bun.com/blog/bun-v1.3.10
[47] GitHub Discussion #725 — https://github.com/oven-sh/bun/discussions/725
[48] Security Scanner API — https://bun.sh/docs/pm/security-scanner-api
