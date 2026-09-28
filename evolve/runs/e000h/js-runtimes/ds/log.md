# Log

## R0（定框架，不 spawn）
- 写了 brief.md、grid.md v0。
- 分类轴：Node=参照系；Bun=速度+高兼容+默认信任；Deno 2=安全沙箱起家、2.0 起向 npm 生态妥协。
- 6 维度：D1 TS 执行模型、D2 包管理/npm、D3 权限模型、D4 内置工具链、D5 Node API 兼容层、D6 部署平台支持。
- 参数：rounds=3, workers=6/轮, budget=9000 字符。
- R1 计划：6 个工人，按实体+维度簇拆分（见 grid.md「R1 分工计划」）。不单独派 scout——工人简报里要求顺带记录迁移/部署/坑相关的 leads，省出的工人配额留到 R2 定向打缺口和覆盖坑/迁移/部署这个跨实体主题。

## R1（扩展，6 spawn）
- 6 个工人全部一次成功，无需重派。notes_lint：184 条主张（178 official / 6 secondary），0 条缺 src/quote，6 条"conflicts"经检查均非真实冲突（版本演进或自评过度谨慎），25 gaps，16 leads。3 份笔记超 8000 字符但内容有效未截断使用。
- grid v0 → v1：分类轴验证成立（默认安全姿态 + npm 生态兼容策略），未换轴。新增细分发现：Node 权限模型是"opt-in enforce"（不传 flag 完全不设防），Deno 是"内建默认拒绝"（无需 flag）——这个对比比 v0 预想的更锋利，写入分类轴描述。
- 首次收束 report.md：9000/9000 字符（压缩三轮：源列表去冗余前缀省约420字符，一屏看懂六条各去重后省约320字符），网格 84% resolved（16 ✅ / 3 ❓）。
- 观察：D1 维度里 Deno/Bun 对 enum/namespace/装饰器/参数属性的**运行时**处理（转换还是报错）完全空白——这恰好是用户疑点1"是否和 Node 一样完整支持TS"的最锋利差异点，Node 这边数据充分（32 official claims 精确到每个语法报错），但 Deno/Bun 对应数据是 R1 六份简报都没覆盖到的盲区。另观察：Node 部署平台（D6）为空但优先级低（Node 作为基线不构成决策差异），Node"无内置工具链三兄弟"与 Bun"无权限模型"两条结论的笔记 quote 字段是转述而非原句，违反笔记规范，需要补硬引用。
- 决策：R2 派 3 个更窄的工人（少于 R1 的 6，符合"每轮更少更窄"）：
  1. r2-ts-runtime-features：核实 Deno + Bun 运行时对 enum/namespace(带代码)/参数属性/legacy decorators 的处理——直接解决用户疑点1的精确结论，最高优先级。
  2. r2-node-cite-fix：补 Node"无官方打包器/格式化器/linter"的硬引用 + 顺带查 Node 官方是否有部署/容器相关表态（D6 低优先级但顺手做）。
  3. r2-bun-security-cite：补 Bun"无权限模型"的硬引用/设计说明，理清 Bun.Security 与权限管理的关系（避免用户误解）。
- 预计 spawn：3。

## R2（扩展，3 spawn）
- 3 个工人全部成功。notes_lint：17 条主张全 official，0 缺 src/quote，2 conflicts（均为文档内部表述张力，非跨源真冲突），7 gaps，6 leads。
- **关键突破**：r2-ts-runtime-features 找到 Deno 官方原话"enums and namespaces with runtime values work without flags"（enum→IIFE 由 SWC 转译）；Bun 官方 blog 确认 enum 内联/namespace 合并(v1.1.18+)、legacy decorators via emitDecoratorMetadata(v1.0.3+，NestJS 场景)、TC39 装饰器(v1.3.10+)。这把用户疑点1从"待核实"变成了有精确版本号和原话支撑的结论：Deno/Bun 是真转译，Node 是纯剥离+报错，差距比预想更大。
- r2-bun-security-cite 找到 Bun 创始人在 GitHub Discussion #725 的设计哲学原话（"静态分析后从二进制去掉不需要的能力，比运行时检查更安全"），补齐了 D3 的硬引用，也理清 Bun.Security 是供应链扫描器而非权限系统。
- r2-node-cite-fix 收益有限：Node 官方文档确实没有"我们不内置 bundler/formatter/linter"这种否定性声明（这类声明在任何厂商文档里都少见），结论维持但引用质量诚实地标注为"推断性"而非编造引用。D6 部署平台确认 nodejs.org 没有专门页面，判定为"不适用"而非缺口。
- grid v1 → v2：无需换轴（TS 支持深度的新发现进一步印证了分类轴：Deno/Bun 追求"像写 JS 一样写 TS"，Node 保守剥离）。
- 收束 report.md：重写后 10129 字符，超预算 1129，经 8 轮小幅压缩（源列表去括注、章节 3 删除次要历史段落、D1/D3/D4/D6 表格精简措辞、一屏看懂/坑/未决收紧）降到 8998/9000，未删除任何 P0 内容（taxonomy、核心矩阵、用户疑点结论）。已同步写入 ./report.md（outer）。
- 观察：核心 18 格中 16 ✅，剩 2 格（Deno legacy decorator 运行时行为、Bun 参数属性官方声明）是真实的"官方没写"，R1+R2 累计已用 6 次工具调用级别的查证尝试，继续派工人边际收益很低，且不违反"不许为了凑轮数派工人"。两个用户点名疑点都有精确、可引用原句支撑的结论。这符合"核心格子都是 ✅/∅ + 上一轮几乎打完缺口"的收尾信号。
- 决策：不再扩展，进入终审。派 1 个审稿工人核对 report.md 与全部 9 份 notes 的一致性。
- 预计 spawn：1（终审）。

## R3（终审，1 spawn）
- 审稿工人通读 report.md 全文 + 全部 9 份笔记，均匀抽查 31 条具体主张（覆盖第 0/2/3/4 节，含版本号、flag 名、API 名、百分比数字），重点复核用户两个点名疑点对应的段落。
- 结果：31/31 supported，0 weak/unsupported/contradicted。两个重点复核（TS 非可擦除语法支持、Deno nodeModulesDir 默认值反转）均"表述准确对应"，无需改稿。审稿并指出 report.md 第5节对 Deno legacy decorator 缺口的标注是"谨慎且负责任的"。
- 决策：不修改正文（无 contradicted/unsupported 需要处理），跳过"改稿"步骤直接进入最终确认。report.md 保持 8998/9000 字符，已同步到 ./report.md（outer）。
- 终止：三轮扩展+终审全部完成（R1 铺开 6 工人 → R2 定向打缺口 3 工人 → R3 审稿 1 工人，共 10 次 spawn），网格核心 18 格 16 ✅ + 2 个如实标注的官方空白，两个用户点名疑点均有精确、可引用原话的结论，成稿全程未破预算。停止扩展，任务完成。
