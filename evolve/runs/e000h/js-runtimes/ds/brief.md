# Brief：Node.js / Deno 2 / Bun 对比

## 任务
产出一份文档，帮用户快速了解 Node.js、Deno 2、Bun 这三个 JavaScript/TypeScript 运行时现在（2026-09）有什么不同。

## 读者
会写 JS/TS、可能已经用惯 Node，正在评估要不要换/加用 Deno 或 Bun 的开发者。要在 5 分钟内建立对比认知，再按需查字段级细节。

## 范围内
- TypeScript 支持（怎么跑 .ts、是否类型检查、tsconfig 支持范围、版本时间线）
- 包管理与 npm 兼容（package.json、node_modules、lockfile、npm 生态兼容度）
- 权限/安全模型（默认允许 vs 默认拒绝、权限粒度、是否实验性）
- 内置工具链（测试、打包/编译、格式化、lint）
- 迁移路径（从 Node 迁移到 Deno/Bun 或反过来的阻力点）
- 部署平台支持（Vercel、Cloudflare、Deno Deploy、Docker 等对三者的支持现状）
- 兼容性坑（三者中"看起来兼容但其实有差异"的具体点）

## 范围外
- 底层引擎实现细节（V8/JSC 内部机制、GC 算法）不展开，只在能解释差异时提一句
- 性能基准测试数字（除非官方文档明确给出且与用户问题相关，避免仅二手 benchmark 博客）
- 历史八卦（除非直接解释当前设计决策，如 Deno 1→2 的路线转变）

## 种子词
Node.js、Deno 2、Bun、TypeScript

## 用户点名的疑点（成稿必须给出明确结论）
1. **Node 现在能直接跑 .ts 文件了，是不是和 Deno、Bun 一样"完整支持"TypeScript？**
   → 需要查清：Node 是类型剥离（type-stripping）还是类型检查；哪个版本起默认开启；对 tsconfig 高级特性（enum、namespace、装饰器等）的支持程度；与 Deno/Bun 的差异到底在哪。
2. **Deno 2 是不是已经能直接用 npm 包和 package.json 了？**
   → 需要查清：Deno 2 对 `npm:` specifier、`package.json`、`node_modules` 的支持范围和默认行为，与 Deno 1 的路线差异，是否需要额外配置。

## 完成标准
- 三个核心实体（Node.js、Deno 2、Bun）在 6 个核心维度上的状态都是 ✅ 或 ∅（官方未写），❓/⚠ 数量收敛到最少。
- 两个用户点名疑点在"一屏看懂"里有一句话结论。
- 成稿 ≤ 9000 字符（硬预算），含来源节。
- 每个具体事实可追溯到 notes/ 里的一条 claim。
