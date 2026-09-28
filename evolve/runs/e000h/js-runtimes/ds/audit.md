# 终审结果 audit

## 检查过程

共抽查 31 条具体主张，覆盖 report.md 的第 0、2、3、4 节。

### 检查结果

| 判定 | 条号 | report.md 原文节选 | 依据笔记/[C#] | 建议 |
|---|---|---|---|---|
| supported | 1 | Node "纯类型剥离，不检查类型" | r1-node-ts-security [C1] | 无需改 |
| supported | 2 | Node "对 enum...直接报错" | r1-node-ts-security [C8] | 无需改 |
| supported | 3 | Node "对...namespace...直接报错" | r1-node-ts-security [C10] | 无需改 |
| supported | 4 | Node "对...参数属性...直接报错" | r1-node-ts-security [C9] | 无需改 |
| supported | 5 | Node "对...装饰器...直接报错" | r1-node-ts-security [C12] | 无需改 |
| supported | 6 | Deno "enums and namespaces with runtime values work without flags" | r2-ts-runtime-features [C1] | 无需改 |
| supported | 7 | Deno "enum 被 SWC 转译成 IIFE" | r2-ts-runtime-features [C4] | 无需改 |
| supported | 8 | Bun "enum 内联 v1.1.18+" | r2-ts-runtime-features [C6] / r1-bun-ts-npm-nodeapi [C4] | 无需改 |
| supported | 9 | Bun "namespace 合并 v1.1.18+" | r2-ts-runtime-features [C7] | 无需改 |
| supported | 10 | Bun "legacy decorators v1.0.3+" | r2-ts-runtime-features [C8] | 无需改 |
| supported | 11 | Bun "TC39 装饰器 v1.3.10+" | r2-ts-runtime-features [C9] | 无需改 |
| supported | 12 | Deno 2 "full Node and npm backwards compatibility" | r1-deno-ts-npm [C20] | 无需改 |
| supported | 13 | Deno 2 nodeModulesDir 默认值 "2.x 需显式 deno install" | r1-deno-ts-npm [C12-C13] | 无需改 |
| supported | 14 | Deno 1.x nodeModulesDir "1.x 自动创建" | r1-deno-ts-npm [C11] | 无需改 |
| supported | 15 | Node 权限 "传 --permission 才 opt-in 变默认拒绝" | r1-node-ts-security [C21] | 无需改 |
| supported | 16 | Deno "无需 flag，运行时内建默认拒绝" | r1-deno-perm-tooling-deploy [C1] | 无需改 |
| supported | 17 | Bun "无运行时权限系统" | r2-bun-security-cite [C1] | 无需改 |
| supported | 18 | Bun.Security "装包阶段供应链扫描器，与运行时权限无关" | r2-bun-security-cite [C2] | 无需改 |
| supported | 19 | Deno "自带 test/fmt/lint/compile/bundle" | r1-deno-perm-tooling-deploy [C15-C28] | 无需改 |
| supported | 20 | Bun "自带 test/build/run" | r1-bun-tooling-security-deploy [C1-C12] | 无需改 |
| supported | 21 | Bun "无格式化器与 linter" | r1-bun-tooling-security-deploy [C13] | 无需改 |
| supported | 22 | Node "仅 node:test+--watch，无打包器/格式化器/linter" | r1-node-pkg-tooling [C9-C25] | 无需改 |
| supported | 23 | Bun "通过 99% Node 测试套件" | r1-bun-ts-npm-nodeapi [C15] | 无需改 |
| supported | 24 | Bun "Node-API 98%" | r1-bun-ts-npm-nodeapi [C21] | 无需改 |
| supported | 25 | Deno "2.8 通过 75%+ Node 测试套件" | r1-deno-perm-tooling-deploy [C34] | 无需改 |
| supported | 26 | Deno Deploy "1GB/512MB 上限" | r1-deno-perm-tooling-deploy [C36-C37] | 无需改 |
| supported | 27 | Deno Deploy "beta 不保运行时间" | r1-deno-perm-tooling-deploy [C39] | 无需改 |
| supported | 28 | Node v22.18/v23.6 "类型剥离默认启用" | r1-node-ts-security [C3-C4] | 无需改 |
| supported | 29 | Bun lockfile "v1.2 起默认文本 bun.lock" | r1-bun-ts-npm-nodeapi [C5] | 无需改 |
| supported | 30 | Render 部署 Bun "Runtime 字段要选'Node'" | r1-bun-tooling-security-deploy [C27] | 无需改 |
| supported | 31 | Bun 在 Cloudflare "只有 Pages 被提及、无独立部署指南" | r1-bun-tooling-security-deploy [C30] + conflicts | 无需改 |

## 汇总

- **supported（有官方 type:official 或笔记记录支撑）**: 31 条
- **weak（只有 secondary 或部分支撑）**: 0 条
- **unsupported（笔记中找不到对应支撑）**: 0 条
- **contradicted（与笔记内容相反）**: 0 条

## 重点检查结果

### 重点检查 1：TypeScript non-erasable 语法支持（第 0 节第 1 条 + D1 矩阵）

**report.md 原文**："Node 纯类型剥离，不检查类型，对 enum、带运行时代码的 namespace、参数属性、装饰器直接报错，须外接 tsc/tsx。Deno 官方原话'enums and namespaces with runtime values work without flags'，enum 被 SWC 转译成 IIFE 正常执行；Bun 支持 enum 内联/namespace 合并(v1.1.18+)，及 NestJS/TypeORM 依赖的 legacy decorators(v1.0.3+)、TC39 新装饰器(v1.3.10+)"

**核对结果**：
- Node 报错：r1-node-ts-security [C8-C12] 均有官方 quote 支撑 ✓
- Deno 转译：r2-ts-runtime-features [C1, C4] 引用官方文档 + Deno.transpileOnly() 例子 ✓
- Bun 版本号：r2-ts-runtime-features [C6-C9] / r1-bun-ts-npm-nodeapi [C4] 均对应版本号 ✓

**判定**：supported，所有数字、版本号都能对应找到

### 重点检查 2：Deno 2 nodeModulesDir 默认值变化（第 0 节第 2 条 + D2 矩阵）

**report.md 原文**："Deno 2 确实能直接用 npm 包和 package.json，官方称'full Node and npm backwards compatibility'；但默认安装行为在 2.0 反转，是最容易踩的迁移坑…默认值从 Deno 1.x 的自动变成 2.x 的 manual"

**核对结果**：
- "full Node and npm backwards compatibility"：r1-deno-ts-npm [C20] 有原句 ✓
- Deno 1.x 行为：r1-deno-ts-npm [C11] "auto-installing" ✓
- Deno 2.x 默认行为：r1-deno-ts-npm [C12-C13] 明确说 2.x 默认 "manual" ✓
- D2 矩阵对应："manual：2.x 需显式 deno install，1.x 自动创建"完全与笔记一致 ✓

**判定**：supported，表述准确

## 未检出的关键风险

审查过程中未发现 report.md 与笔记间的矛盾或严重偏差。所有具体数字、版本号、引用都能在笔记中找到官方来源的支撑。

**唯一需要提请注意的地方**：report.md 第 5 节"未决与置信度"中已明确说明 Deno legacy decorators 支持"未在官方文档找到明确声明"，这与第 0 节、D1 矩阵中关于 TypeScript 语法支持的讨论保持一致。笔记 r2-ts-runtime-features.md 中也记录了同样的 gap，所以 report.md 的表述是谨慎且负责任的。

---

**审查完成日期**: 2026-09-24
**审查者**: deep-search audit worker
