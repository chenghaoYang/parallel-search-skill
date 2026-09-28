# r1-node-pkg-tooling
question: Node.js 自带/官方支持的包管理现状——npm 是否随 Node 一起分发、package.json/node_modules 的解析规则、corepack（用来免安装启用 yarn/pnpm）现在是什么状态（是否默认启用、是否已经从核心移出或计划移出、当前版本行为）；以及 Node.js 内置工具链：node:test 测试运行器的能力范围、`node --run <script>` 执行 package.json scripts、`--watch` 监听模式；Node 官方是否自带打包器（bundler）、代码格式化器、linter
checked: https://nodejs.org/api/packages.html,https://nodejs.org/api/cli.html,https://nodejs.org/api/test.html,https://nodejs.org/en/blog,https://github.com/nodejs/corepack,https://nodejs.org/en/blog/release/v24.21.0,https://nodejs.org/en/blog/release/v26.10.0,https://nodejs.org/en/download,https://nodejs.org/en/learn

## claims
- [C1] npm 随 Node.js 分发 | src: https://nodejs.org/en/download | quote: "npm is included with Node.js distributions" | type: official
- [C2] npm 在 v24.21.0 (LTS) 版本中随 Node.js 发布 | src: https://nodejs.org/en/blog/release/v24.21.0 | quote: "Release Date: September 8, 2026" | type: official
- [C3] 模块系统：.js 文件类型由最近父 package.json 的 "type" 字段决定 | src: https://nodejs.org/api/packages.html | quote: "'type': 'module' → ES modules; 'type': 'commonjs' or missing → CommonJS" | type: official
- [C4] .mjs 文件始终使用 ES modules | src: https://nodejs.org/api/packages.html | quote: "'.mjs' → Always ES modules" | type: official
- [C5] .cjs 文件始终使用 CommonJS | src: https://nodejs.org/api/packages.html | quote: "'.cjs' → Always CommonJS" | type: official
- [C6] Corepack 随 Node.js 14.19.0 到 24.x 版本分发 | src: https://github.com/nodejs/corepack | quote: "The tool comes bundled with Node.js versions 14.19.0 through 24.x" | type: official
- [C7] Corepack 在 v24.21.0 中更新到版本 0.36.0 | src: https://nodejs.org/en/blog/release/v24.21.0 | quote: "Corepack: Updated to 0.36.0" | type: official
- [C8] Corepack 不是默认启用的，需要用户运行 `corepack enable` | src: https://github.com/nodejs/corepack | quote: "Users can activate it by running `corepack enable`, which installs required binaries for Yarn and pnpm" | type: official
- [C9] node:test 测试运行器从 v18.0.0 开始可用，v20.0.0 稳定 | src: https://nodejs.org/api/test.html | quote: "available since v18.0.0 and stable as of v20.0.0" | type: official
- [C10] node:test 支持同步和异步测试 | src: https://nodejs.org/api/test.html | quote: "test('synchronous passing test', () => {...}); test('asynchronous passing test', async () => {...})" | type: official
- [C11] node:test 支持子测试（subtests） | src: https://nodejs.org/api/test.html | quote: "test('parent test', async (t) => { await t.test('subtest 1', () => {...}) })" | type: official
- [C12] node:test 支持跳过测试、TODO 测试、仅运行特定测试、期望失败 | src: https://nodejs.org/api/test.html | quote: "test('skipped test', { skip: true }, () => {}); test('todo test', { todo: true }, () => {})" | type: official
- [C13] node:test 支持 mock 函数和 mock 计时器 | src: https://nodejs.org/api/test.html | quote: "t.mock.fn(); t.mock.timers.enable(...)" | type: official
- [C14] node:test 支持快照测试 | src: https://nodejs.org/api/test.html | quote: "t.assert.snapshot({ value: 1 })" | type: official
- [C15] node:test 默认使用进程隔离 | src: https://nodejs.org/api/test.html | quote: "Process isolation (default): Each test file runs in a separate child process" | type: official
- [C16] node:test 支持测试标签过滤 (v26.2.0+) | src: https://nodejs.org/api/test.html | quote: "describe('database', { tags: ['db'] }, () => {...})" | type: official
- [C17] node:test 支持内置 Reporter：spec、tap、dot、junit、lcov | src: https://nodejs.org/api/test.html | quote: "'spec' - Human-readable (default); 'tap' - TAP format; 'dot' - Compact format; 'junit' - jUnit XML; 'lcov' - Code coverage" | type: official
- [C18] node:test 支持代码覆盖率选项 `--experimental-test-coverage` | src: https://nodejs.org/api/test.html | quote: "node --test --experimental-test-coverage" | type: official
- [C19] `node --run <script>` 用于执行 package.json 中定义的脚本 | src: https://nodejs.org/api/cli.html | quote: "node --run <script-name>" | type: official
- [C20] `node --run` 是 npm run 的轻量级替代 | src: https://nodejs.org/api/cli.html | quote: "Executes npm-style scripts from package.json without requiring npm" | type: official
- [C21] `--watch` 标志启用文件监听，文件改变时自动重启 | src: https://nodejs.org/api/cli.html | quote: "node --watch script.js" 或 "node --watch --run dev"" | type: official
- [C22] `--watch` 支持 `--watch-path`、`--watch-kill-signal`、`--watch-preserve-output` 选项 | src: https://nodejs.org/api/cli.html | quote: "--watch-path: Specify which paths to watch; --watch-kill-signal: Set the signal used to kill the process; --watch-preserve-output: Preserve console output between restarts" | type: official
- [C23] Node.js 没有官方打包器 | src: https://nodejs.org/en/learn | quote: "学习资源中列出的官方工具不包括 bundler" | type: official
- [C24] Node.js 没有官方代码格式化器 | src: https://nodejs.org/en/learn | quote: "学习资源中列出的官方工具不包括 formatter" | type: official
- [C25] Node.js 没有官方 linter | src: https://nodejs.org/en/learn | quote: "学习资源中列出的官方工具不包括 linter" | type: official
- [C26] package.json 中 `"exports"` 字段定义公开 API | src: https://nodejs.org/api/packages.html | quote: "'exports': './index.js'" | type: official
- [C27] 条件导出支持 `"import"`、`"require"`、`"node"`、`"default"` | src: https://nodejs.org/api/packages.html | quote: "'import': './index-module.js', 'require': './index-require.cjs', 'default': './index.js'" | type: official
- [C28] package.json 支持 `"imports"` 用于内部包导入映射 | src: https://nodejs.org/api/packages.html | quote: "'imports': {'#dep': {...}}'" | type: official
- [C29] Node.js v26.10.0 (Current) 是最新发行版，2026年9月22日发布 | src: https://nodejs.org/en/blog/release/v26.10.0 | quote: "Released September 22, 2026" | type: official
- [C30] Corepack 在 Node 14.19.0 到 24.x 版本中提供 | src: https://github.com/nodejs/corepack | quote: "from versions 14.19.0 through 24.x" | type: official

## conflicts
- Corepack 版本号：GitHub README 未提及最新版本号，但 v24.21.0 发布说明显示 Corepack 0.36.0

## gaps
- npm 在 v26.10.0 中的具体版本号未找到
- 是否计划从 Node.js 核心移出 Corepack 的明确官方说法
- 是否有官方关于"不推荐内置打包器、格式化器、linter"的明确说法

## leads
- Corepack GitHub 项目中 25.x 版本不包含 Corepack，可能需要确认后续版本策略
- Node.js 官方工具链文档提到"Userland Migrations"，建议使用第三方工具（Axios、Chalk 等），暗示官方不提供这些工具
