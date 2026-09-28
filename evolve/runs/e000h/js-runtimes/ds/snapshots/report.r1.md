# Node.js / Deno 2 / Bun：2026 年怎么选

> 截至 2026-09-24。面向已用 Node、评估要不要上 Deno 2/Bun 的开发者：先看"一屏看懂"，再查矩阵和坑。

## 0. 一屏看懂

1. **"原生支持 TypeScript"三家含义不同**。Node.js 纯类型剥离，不检查类型，对 enum、带运行时代码的 namespace、参数属性、装饰器、.tsx 直接**报错**，须外接 tsc/tsx 才算完整支持[2][4]；Deno/Bun 剥离同样不检查类型[12][27]，但对这几类语法是否报错本轮未查到一手确认，是当前最大空白（见第 5 节）。
2. **Deno 2 确实能直接用 npm 包和 package.json**，官方称"full Node and npm backwards compatibility"[16]；但默认安装行为在 2.0 反转，是最容易踩的迁移坑（详见第 3 节）。
3. **权限模型三条不同的路**：Node 默认不设防，传 `--permission` 才 opt-in 变"默认拒绝"，Stable since v23.5.0[5][6]；Deno **无需 flag**，运行时内建默认拒绝文件/网络/环境变量/子进程[17]；Bun **无运行时权限系统**，仅装包阶段有"信任依赖"机制控制 postinstall[35]。
4. **内置工具链：Deno 最全，Bun 次之，Node 最少**（详见 D4）。Deno 自带 test/fmt/lint/compile/bundle[20-24]；Bun 自带 test/build/run 但无格式化器与 linter[32-34]；Node 仅 `node:test`+`--watch`，无官方打包器/格式化器/linter[7][8]。
5. **Node API 兼容，Bun 数字更具体**：Bun 称通过 99% Node 测试套件、Node-API 98%[30][31]；Deno 2.8 通过 75%+ Node 自身测试套件[14]。
6. **部署平台，Bun 文档最详细**：Vercel/Docker/Lambda/Railway/Render/Cloud Run/DigitalOcean 均有官方指南[37-41]；Deno Deploy 2.0 重写，98%+ npm 兼容(二手)，仍 beta、1GB/512MB 上限[25][26]；Node 无"平台支持列表"——它是默认基线。

## 1. Taxonomy

**分类轴**：默认安全姿态 × 对 Node/npm 生态的兼容策略——这条轴能解释 D1~D6 里大多数差异的根源。

| 家族 | 默认安全姿态 | 生态策略 |
|---|---|---|
| Node.js（基线） | 不设防；`--permission` 后才 opt-in 变默认拒绝 | 自己即生态 |
| Deno 2（沙箱优先） | 运行时内建默认拒绝，无需任何 flag | 2.0 起从"另起炉灶"转向高兼容，但安全默认值未变 |
| Bun（速度优先） | 无运行时权限系统 | 从第一天起就高兼容 |

**维度**：D1 TS 执行模型（怎么跑/是否检查类型）· D2 包管理与 npm 兼容默认行为 · D3 权限模型粒度与默认值 · D4 内置工具链覆盖面 · D5 对 `node:` 模块/原生插件兼容度 · D6 主流平台官方支持现状。

## 2. 对照矩阵

### D1 TypeScript 执行模型
| | Node.js | Deno 2 | Bun |
|---|---|---|---|
| 运行方式 | 类型剥离(Amaro/SWC)，默认开启于 v22.18/v23.6，Stable v25.2+[2][3] | 剥离类型直接交给 V8，无需 tsc/config[12] | 剥离全部 TS 语法后等同 JS loader[27] |
| 类型检查 | 不检查，需另跑 `tsc --noEmit`[1] | `deno check` 内置，默认 strict，等价 `tsc --noEmit`[12] | 不检查，编辑器类型靠 `@types/bun`[27] |
| tsconfig | 剥离时**忽略** tsconfig（不解析 paths/target）[2] | 自动发现并处理已有 tsconfig.json[13] | ❓ 未查 |
| enum/namespace/装饰器/参数属性 | **直接报错**；v26 移除了曾用于转换它们的 `--experimental-transform-types`[2][4] | ❓ 待核实（R2） | ❓ 待核实（R2） |
| .tsx | 不支持[2] | ❓ 未查到一手确认 | ❓ 未查到一手确认 |

### D2 包管理与 npm 兼容
| | Node.js | Deno 2 | Bun |
|---|---|---|---|
| 包管理器 | npm 随分发[11] | 内置（`deno install` 等）[16] | 内置 `bun install`，官方称比 npm 快 25 倍[29] |
| package.json | 标准 exports/imports[10] | 原生理解 dependencies/scripts(`deno task`)/type 字段[14] | 完整支持标准字段[29] |
| node_modules 默认行为 | 标准 | **manual**：2.x 起需显式 `deno install`，1.x 是自动创建[15] | 默认生成 |
| lockfile | package-lock.json | 内部锁定（本轮未细查） | `bun.lock`（文本 JSONC，v1.2 起默认，取代二进制 `bun.lockb`，旧项目仍受支持）[28] |
| 无 node_modules 时 | 不适用 | 走全局缓存，不落地 node_modules（"none" 模式，默认）[14] | 不适用（总会用 node_modules） |
| Yarn/pnpm | Corepack，需 `corepack enable`，非默认开启[9] | 不适用（用 `npm:`/`jsr:` specifier） | 自动从 yarn.lock/pnpm-lock.yaml 迁移[28] |

### D3 权限模型
| | Node.js | Deno 2 | Bun |
|---|---|---|---|
| 默认行为 | 允许一切，除非传 `--permission`[5] | **拒绝**文件/网络/环境变量/子进程访问[17] | 允许一切，无权限系统[35] |
| 状态 | Stable since v23.5.0[6] | 自 1.0 起就是核心设计[17] | 不适用（无此设计） |
| 粒度 | `--allow-fs-read/write=path` 等，路径级[5] | `--allow-net/read/write/env/sys/run/ffi`，可精确到域名/路径/变量名[18] | 无运行时权限 flag；仅 `bun pm trust` 控制 postinstall 脚本[35] |
| 一键放行 | 无（需逐项开） | `-A`，官方称等价于"在 Node.js 里跑不受信任的代码"[18] | 不适用 |
| 配置文件声明 | 不支持 | 2.5+ 可在 deno.json 声明 allow/deny/ignore[19] | 不适用 |

### D4 内置工具链
| | Node.js | Deno 2 | Bun |
|---|---|---|---|
| 测试 | `node:test`（v18+，Stable v20+），mock/快照/覆盖率/多种 reporter[7] | `deno test`：filter/watch/parallel/coverage/retry/shuffle，4 种 reporter[20] | `bun test`：并发(默认 20)/coverage/watch/retry/snapshot[32] |
| 打包 | 无官方 bundler[8] | `deno bundle`（**仍实验性**，官方称不能替代 Vite/webpack）[24] | `bun build`：esm/cjs/iife 格式，browser/bun/node 三种 target[33] |
| 编译为可执行文件 | 无 | `deno compile`（内嵌 denort，跨平台 `--target`，2.8+ 自动识别框架）[23] | `bun build --compile`（内嵌 Bun 运行时，跨平台）[34] |
| 格式化 | 无官方 formatter[8] | `deno fmt`：25+ 文件类型，2.0 新增 HTML/CSS/YAML[21] | 无内置，需自接 Prettier[35] |
| Lint | 无官方 linter[8] | `deno lint`：100+ 规则，`--fix`，2.0 新增 Node 专属规则[22] | 无内置，需自接 ESLint/Oxlint[35] |
| 脚本执行 | `node --run <script>`[8] | `deno task` | `bun run`，支持生命周期钩子[35] |

### D5 Node API 兼容层
| | Deno 2 | Bun |
|---|---|---|
| 官方兼容度说法 | 2.8+ 通过 Node 自身测试套件 75%+，覆盖近乎所有 `node:` 模块[14] | 通过 Node 测试套件 99%；Node-API（原生插件）98%[30][31] |
| 已知限制 | 部分 API 仅 partial；带原生插件的包需本地 node_modules[14] | crypto 缺 ed448/x448/secp256k1（BoringSSL 非 OpenSSL 后端）；`node:sea` 未实现，用 `bun build --compile` 替代[30] |

### D6 部署平台
| 平台 | Deno 2 | Bun |
|---|---|---|
| 自家平台 | Deno Deploy：2.0 完全重写，支持 Deno+Node 应用；1GB 部署/512MB 内存上限，beta 期不保正常运行时间[25][26] | 无自家平台 |
| Vercel | ❓ 未查 | 官方 Runtime 公测，`vercel.json` 配 `bunVersion`；不支持自动 source map/bytecode 缓存[37] |
| Docker | ❓ 未查 | 官方镜像 `oven/bun`：debian/slim/distroless/alpine，x64+arm64[38] |
| Serverless/容器 | ❓ 未查 | AWS Lambda（经 Docker+adapter）、Google Cloud Run、DigitalOcean 均经 Docker[39] |
| PaaS | ❓ 未查 | Railway（零配置自动部署）、Render（原生支持，但 Runtime 字段仍选"Node"）[40][41] |
| Node.js | 无专门"平台支持"文档——是几乎所有平台的默认基线运行时，不构成决策差异点 | — |

## 3. 变体与适配层

**Deno 1→2 的 npm 兼容路线反转**：1.x 靠 URL import + 不落地 node_modules 是卖点；2.0 为"无缝跑现有 Node 应用"引入 package.json/node_modules 支持[16]，但默认安装行为比 1.x 更保守（`manual` 而非自动）[15]——能力变强，但默认动作变少，迁移时容易误判为"装不上包"。

**Bun 的 lockfile 格式反转**：早期二进制 `bun.lockb`（不可读、难 diff）→ v1.1.39 引入文本 `bun.lock`（JSONC）→ v1.2 起默认改为文本格式，旧项目的 `bun.lockb` 仍继续支持，不强制迁移[28]。

## 4. 用户需要知道的坑

1. **"Node 也能跑 .ts 了"不等于"Node 支持 TypeScript"**：项目里一旦用了 enum、namespace、参数属性或装饰器（NestJS/TypeORM/Angular 风格代码常见），Node 直接报错退出，必须走 tsc/tsx/esbuild 编译[2][4]。
2. **Deno 2 项目"装不上包"通常是 `nodeModulesDir` 默认值变了**：从 Deno 1.x 迁移来的项目若依赖自动生成的 node_modules，需在 deno.json 加 `"nodeModulesDir":"auto"` 或显式跑 `deno install`[15]。
3. **Corepack 不是默认开启的**：即使内置了 Corepack，用 yarn/pnpm 前必须先手动 `corepack enable`[9]。
4. **Deno 的 `-A` 官方原话是"等价于在 Node.js 里跑不受信任的代码"**：默认安全是 Deno 的核心卖点，全局 `-A` 等于放弃这个卖点，仅建议调试用[18]。
5. **Render 部署 Bun 时 Runtime 字段要选"Node"**：不是选错，是 Render 目前没有单独的 Bun 分类，Build/Start Command 手动填 `bun install`/`bun app.ts`[41]。
6. **Bun 在 Cloudflare 上只有 Pages 被提及、无独立部署指南**：和 Vercel/Railway/Render 不是一个层级，依赖前先自己跑通一次。

## 5. 未决与置信度

- **Deno/Bun 运行时对 enum、namespace(带运行时代码)、参数属性、装饰器的处理**——是像 Node 一样报错，还是转换执行——本轮未查到一手确认，是本文档当前最大空白，直接决定"三家 TS 支持谁更完整"这一用户最关心问题的精确结论。**R2 定向核实中。**
- Node.js 无官方打包器/格式化器/linter、Bun 无权限模型两条结论的引用偏转述而非页面原句；结论与社区共识一致，但引用质量待补强。
- Deno "98%+ npm 包兼容"表述来自官方域名但措辞偏营销，workers 标记为二手，谨慎对待；Deno Deploy 是否原生支持 `npm:` specifier 本轮未专门确认。
- Node.js、Deno 在 Vercel/Docker/Lambda 等第三方平台的官方支持现状本轮未查（Bun 已查全），暂不作为对比依据，避免"Bun 部署支持更好"的误导性结论。

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
[12] TypeScript — https://docs.deno.com/runtime/fundamentals/typescript/
[13] tsconfig migration — https://docs.deno.com/runtime/reference/ts_config_migration/
[14] Node & npm compatibility — https://docs.deno.com/runtime/fundamentals/node/
[15] Migration guide 1.x→2.x — https://docs.deno.com/runtime/reference/migration_guide/
[16] Announcing Deno 2 — https://deno.com/blog/v2.0
[17] Security — https://docs.deno.com/runtime/fundamentals/security
[18] Permissions reference — https://docs.deno.com/runtime/reference/permissions
[19] deno.json reference — https://docs.deno.com/runtime/reference/deno_json
[20] CLI: test — https://docs.deno.com/runtime/reference/cli/test
[21] CLI: fmt — https://docs.deno.com/runtime/reference/cli/fmt
[22] CLI: lint — https://docs.deno.com/runtime/reference/cli/lint
[23] CLI: compile — https://docs.deno.com/runtime/reference/cli/compile
[24] CLI: bundle — https://docs.deno.com/runtime/reference/cli/bundle
[25] Deno Deploy docs — https://docs.deno.com/deploy
[26] Deploy pricing & limits — https://docs.deno.com/deploy/pricing_and_limits
[27] TypeScript — https://bun.sh/docs/runtime/typescript
[28] Lockfile — https://bun.sh/docs/pm/lockfile
[29] bun install — https://bun.sh/docs/cli/install
[30] Node.js compatibility — https://bun.sh/docs/runtime/nodejs-compat
[31] Node-API — https://bun.sh/docs/runtime/node-api
[32] Test runner — https://bun.com/docs/test
[33] Bundler — https://bun.com/docs/bundler
[34] Single-file executables — https://bun.com/docs/bundler/executables
[35] Runtime — https://bun.com/docs/runtime
[36] Bun.Security — https://bun.com/reference/bun/Security
[37] Deploy to Vercel — https://bun.com/guides/deployment/vercel
[38] Docker — https://bun.com/guides/ecosystem/docker
[39] AWS Lambda — https://bun.com/guides/deployment/aws-lambda
[40] Railway — https://bun.com/guides/deployment/railway
[41] Render — https://bun.com/guides/deployment/render
