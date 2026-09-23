# js-runtimes 任务 · 用户疑问参考答案

供人工检查用的简短参考答案，对应 task.md 里 "some user aware variation" 那一行提到的两个疑问。核实日期：2026-09-24。

## 疑问 1：听说 Node 现在也能直接跑 .ts 文件了，是不是和 Deno、Bun 一样完整支持 TypeScript？

不算完全一样，三家现在的默认行为其实是"擦除类型 ≠ 检查类型"，但完整度和配套不同：

- **Node**：v22.6.0 起支持"类型擦除"（type stripping），只是把类型标注换成空白直接跑，**不检查类型**；v23.6.0/v22.18.0 起默认开启，v25.2.0/v24.12.0 转正为 Stable。但只认"可擦除语法"，enum/namespace 等需要生成新代码的语法不支持——曾经用来支持它们的实验性开关 `--experimental-transform-types` 在 v26.0.0 已被移除，官方文档建议要"完整支持所有语法"就装 tsx 之类第三方包。
- **Bun**：同样只转不查，`ts`/`tsx` loader "Strips out all TypeScript syntax... Bun does not perform typechecking"，官方说 bundler 不是用来替代 `tsc` 做类型检查的。
- **Deno**：把"执行"和"类型检查"当成两件独立的事——`deno run` 一样只擦除类型；但另外自带 `deno check`（相当于 `tsc --noEmit`，默认严格模式），`deno test`/`deno bench` 默认还会先类型检查。三者里只有 Deno 官方自带完整的类型检查器，Node 和 Bun 都要外部工具。

来源：
- https://nodejs.org/api/typescript.html
- https://bun.sh/docs/bundler/loaders ・ https://bun.sh/docs/bundler
- https://docs.deno.com/runtime/fundamentals/typescript/

## 疑问 2：Deno 2 是不是已经能直接用 npm 包和 package.json 了？

是的。Deno 2 可以用 `npm:` 前缀直接 `import`（如 `import chalk from "npm:chalk@5"`），也看得懂 `package.json`——一个典型 Node 项目搬进 Deno 通常就是"先装依赖、再运行"两条命令，很多 Node 代码不改就能跑。CommonJS 的 npm 包也支持，可以用 `node:module` 的 `createRequire` 在 ESM 里 `require()`。

细节上和 npm 不完全一样：**没有** `package.json` 时，Deno 默认从全局缓存解析依赖、不生成 `node_modules`；**一旦**项目里有 `package.json`，会切到需要 `node_modules` 的"手动"模式（可以配置 `nodeModulesDir: "auto"` 让它自动生成）。

来源：
- https://docs.deno.com/runtime/fundamentals/node/
