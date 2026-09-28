# Grid v2（R2 收束后）

## 分类轴（沿用，R1+R2 数据进一步验证）
默认安全姿态 + 对 Node/npm 生态的兼容策略。R2 新增验证：TS 支持深度也呼应这条轴的精神——Deno/Bun 从第一天起就想"像用 JS 一样用 TS"（完整 transpile），Node 是后加的、保守的、最小化维护成本的剥离。

## 网格（实体 × 维度）—— R2 后状态
| 实体 | D1 TS 执行模型 | D2 包管理/npm | D3 权限模型 | D4 内置工具链 | D5 Node API 兼容 | D6 部署平台 |
|---|---|---|---|---|---|---|
| Node.js | ✅ 全部确认，含 enum/namespace/decorator/参数属性均报错 | ✅ | ✅ | ✅（"无内置工具"结论缺硬反面引用，已知情，降级为推断性表述） | — | ❓ 确认官方无部署专页，非缺口而是"不适用" |
| Deno 2 | ✅ enum/namespace(运行时值)/参数属性官方原话"work without flags"；❓ legacy decorator 是否需配置未明确 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Bun | ✅ enum(v1.1.18+)/namespace(v1.1.18+)/legacy decorator(v1.0.3+)/TC39 decorator(v1.3.10+) 均确认支持；❓ 参数属性无官方明确声明（推断支持） | ✅ | ✅ 补齐设计哲学引用（GitHub Discussion #725） | ✅ | ✅ | ✅ |

## 用户点名疑点 —— 最终结论
| 疑点 | 结论 |
|---|---|
| Node .ts 支持是否等同 Deno/Bun | **否，且差距明确**：Node 是纯类型剥离，对 enum/namespace(带运行时代码)/参数属性/装饰器直接报错；Deno 官方原话确认 enum/namespace/参数属性"work without flags"（真转译，如 enum→IIFE）；Bun 官方确认 enum/namespace/legacy decorators(NestJS/TypeORM 所需)/TC39 装饰器均支持。Deno、Bun 的 TS 支持明显比 Node "更完整"，尤其是装饰器密集的框架代码。 |
| Deno 2 是否已支持 npm 包 + package.json | **是，但默认安装行为在 2.0 反转**（1.x 自动建 node_modules，2.x 默认 manual，需显式 `deno install`）。R1 已定论，R2 未变。 |

## 遗留小缺口（不再派工人，写入成稿"未决"）
- Deno legacy decorator（experimentalDecorators）运行时行为未在官方文档中找到明确声明。
- Bun 参数属性无官方明确声明（正反皆无），按"无不支持清单"推断支持，标二手推断。
- Deno 文档里"declare namespace"与"namespaces with runtime values"两处表述是否指向同一结论存在阅读歧义，未做代码实测，只依赖文档。
- Node.js"无内置 bundler/formatter/linter"结论缺乏官方直接反面声明，结论维持但引用降级。
- Node.js 部署平台维度确认officially无此类页面，判定为"不适用于对比"而非缺口。

## R2 → R3 决策
观察：核心 6×3=18 格中，16 格 ✅，2 格仍是有理由的 ❓（Deno decorator、Bun 参数属性），且这 2 格已尝试查证但官方确实未写，继续派工人边际收益低。两个用户点名疑点都已有精确结论。网格已经从 R1 的 84% resolved 提升到接近饱和，且 R1→R2 变化的边际信息量在下降。
判断：满足"核心格子都是 ✅/∅ + 上一轮几乎打完所有能打的缺口"的收尾条件。
动作：进入终审——派 1 个审稿工人核对 report.md 与 notes/ 的一致性（抽查 ≥20 条具体主张），而不是再扩一轮。
预计 spawn：1（终审）。
