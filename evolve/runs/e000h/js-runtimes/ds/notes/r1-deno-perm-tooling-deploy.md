# r1-deno-perm-tooling-deploy

question: Deno 的权限模型现状是怎样的——是否默认拒绝所有系统访问（文件、网络、环境变量、子进程）、`--allow-*` / `-A` 各自控制什么粒度、是否可以用配置文件声明权限？Deno 内置工具链的具体命令和能力：`deno test`、`deno fmt`、`deno lint`、`deno compile`（编译成单文件可执行程序）、`deno bundle`（是否还存在，官方是否已弃用/移除）？Deno Deploy 这个官方部署平台目前对 Deno 2 的支持现状——是否支持 npm 包、Node API 兼容程度如何、是否有已知限制？

checked: https://docs.deno.com/runtime/fundamentals/security, https://docs.deno.com/runtime/reference/cli/test, https://docs.deno.com/runtime/reference/cli/fmt, https://docs.deno.com/runtime/reference/cli/lint, https://docs.deno.com/runtime/reference/cli/compile, https://docs.deno.com/runtime/reference/cli/bundle, https://deno.com/deploy, https://docs.deno.com/deploy, https://docs.deno.com/runtime/fundamentals/node, https://deno.com/blog/v2.0, https://docs.deno.com/runtime/reference/cli/run, https://docs.deno.com/runtime/reference/permissions, https://docs.deno.com/runtime/reference/deno_json, https://docs.deno.com/deploy/pricing_and_limits

## claims

### 权限模型——默认拒绝
- [C1] Deno 默认拒绝所有系统访问。"Code executing in a Deno runtime has no access to read or write arbitrary files on the file system, to make network requests or open network listeners, to access environment variables, or to spawn subprocesses." | src: https://docs.deno.com/runtime/fundamentals/security | quote: "Code executing in a Deno runtime has no access to read or write arbitrary files on the file system, to make network requests or open network listeners, to access environment variables, or to spawn subprocesses." | type: official

- [C2] Deno 2 保持"安全第一"设计原则，未改变默认安全姿态。"Despite adding Node compatibility, Deno retains its core principles: native TypeScript support, web standards compliance, batteries-included tooling, and secure-by-default execution" | src: https://deno.com/blog/v2.0 | quote: "secure-by-default execution" | type: official

### 权限模型——--allow-* 标志粒度
- [C3] --allow-read 可作用域限制到指定路径。"--allow-read and --allow-write control disk access. Both accept optional path lists like --allow-read=foo.txt,bar.txt to restrict to specific files or directories." | src: https://docs.deno.com/runtime/reference/permissions | quote: "--allow-read...accept optional path lists like --allow-read=foo.txt,bar.txt to restrict to specific files or directories" | type: official

- [C4] --allow-write 可作用域限制到指定路径。同上。| src: https://docs.deno.com/runtime/reference/permissions | quote: "--allow-write control disk access...to restrict to specific files or directories" | type: official

- [C5] --allow-net 可作用域限制到特定主机。"--allow-net grants network access, optionally scoped to hosts: --allow-net=github.com,*.example.com:8080" | src: https://docs.deno.com/runtime/reference/permissions | quote: "--allow-net grants network access, optionally scoped to hosts: --allow-net=github.com,*.example.com:8080" | type: official

- [C6] --allow-env 可作用域限制到特定环境变量。"--allow-env permits reading/writing env vars, with support for wildcard scoping like --allow-env=\"AWS_*\"" | src: https://docs.deno.com/runtime/reference/permissions | quote: "--allow-env...with support for wildcard scoping like --allow-env=\"AWS_*\"" | type: official

- [C7] --allow-sys 可作用域限制到特定 API。"--allow-sys provides OS details (uptime, memory, hostname), optionally limited to specific APIs: --allow-sys=\"systemMemoryInfo,osRelease\"" | src: https://docs.deno.com/runtime/reference/permissions | quote: "--allow-sys...optionally limited to specific APIs: --allow-sys=\"systemMemoryInfo,osRelease\"" | type: official

- [C8] --allow-run 可作用域限制到特定程序。"--allow-run spawns child processes, optionally restricted to specific programs" | src: https://docs.deno.com/runtime/reference/permissions | quote: "--allow-run spawns child processes, optionally restricted to specific programs" | type: official

- [C9] --allow-ffi 可限制到特定路径。"--allow-ffi loads and executes native libraries from specific paths" | src: https://docs.deno.com/runtime/reference/permissions | quote: "--allow-ffi loads and executes native libraries from specific paths" | type: official

### 权限模型——-A 和 deny 标志
- [C10] -A flag (--allow-all) 禁用所有沙箱。"--allow-all (-A) to disable the sandbox entirely, equivalent to running untrusted code in Node.js." | src: https://docs.deno.com/runtime/reference/permissions | quote: "--allow-all (-A) to disable the sandbox entirely" | type: official

- [C11] -A 不推荐用于生产。"is not recommended and should only be used for testing." | src: https://docs.deno.com/runtime/reference/cli/run | quote: "is not recommended and should only be used for testing" | type: official

- [C12] Deny 标志优先于 allow 标志。"Deny flags (--deny-*) take precedence over allow flags. For example...allow all reads but deny access to secrets: --allow-read=./ --deny-write=./secrets" | src: https://docs.deno.com/runtime/reference/permissions | quote: "Deny flags (--deny-*) take precedence over allow flags" | type: official

### 权限模型——配置文件支持
- [C13] Deno 2.5+ 支持在 deno.json 中声明权限。"Deno 2.5+ allows you to store permission sets directly in your config file." | src: https://docs.deno.com/runtime/reference/deno_json | quote: "Deno 2.5+ allows you to store permission sets directly in your config file" | type: official

- [C14] deno.json 支持 allow、deny、ignore 三层控制。"allow: Grant access...deny: Explicitly block access, even if allowed elsewhere...ignore: Silently ignore requests" | src: https://docs.deno.com/runtime/reference/deno_json | quote: "allow: Grant access...deny: Explicitly block access...ignore: Silently ignore requests" | type: official

### 内置工具链——deno test
- [C15] deno test 支持过滤、Watch 模式、并行执行。"Use --filter...--watch flag automatically reruns tests...--parallel, which defaults to your system's CPU count" | src: https://docs.deno.com/runtime/reference/cli/test | quote: "--filter...--watch...--parallel" | type: official

- [C16] deno test 支持覆盖率、重试、shuffle。"Collect coverage data with --coverage...Use --retry...and --shuffle to randomize test order" | src: https://docs.deno.com/runtime/reference/cli/test | quote: "--coverage...--retry...--shuffle" | type: official

- [C17] deno test 支持多种输出格式（pretty、dot、junit、tap）。"Choose from four reporters—pretty (default), dot, junit, or tap" | src: https://docs.deno.com/runtime/reference/cli/test | quote: "Choose from four reporters—pretty (default), dot, junit, or tap" | type: official

### 内置工具链——deno fmt
- [C18] deno fmt 支持 25+ 文件类型。"The formatter handles 25+ file types" | src: https://docs.deno.com/runtime/reference/cli/fmt | quote: "The formatter handles 25+ file types" | type: official

- [C19] Deno 2 升级：deno fmt 新增 HTML、CSS、YAML 支持。"deno fmt now formats \"HTML, CSS, and YAML\"" | src: https://deno.com/blog/v2.0 | quote: "deno fmt now formats \"HTML, CSS, and YAML\"" | type: official

- [C20] deno fmt 支持 deno.json 配置。"Users can customize formatting through deno.json settings like useTabs, lineWidth, indentWidth, semiColons, singleQuote, and proseWrap" | src: https://docs.deno.com/runtime/reference/cli/fmt | quote: "deno.json settings like useTabs, lineWidth, indentWidth" | type: official

### 内置工具链——deno lint
- [C21] deno lint 包含 100+ 规则。"The linter offers over 100 rules" | src: https://docs.deno.com/runtime/reference/cli/lint | quote: "The linter offers over 100 rules" | type: official

- [C22] deno lint 支持自动修复。"Auto-fixing: Repair certain violations automatically with --fix" | src: https://docs.deno.com/runtime/reference/cli/lint | quote: "--fix" | type: official

- [C23] Deno 2 升级：deno lint 新增 Node 特定规则。"deno lint includes Node-specific rules" | src: https://deno.com/blog/v2.0 | quote: "deno lint includes Node-specific rules" | type: official

### 内置工具链——deno compile
- [C24] deno compile 生成单文件可执行程序，包含精简 Deno 运行时。"Deno compile embeds your program into denort...a stripped build of Deno that contains only what's needed to run a compiled program" | src: https://docs.deno.com/runtime/reference/cli/compile | quote: "Deno compile embeds your program into denort" | type: official

- [C25] deno compile 支持跨平台编译。"Developers can target different operating systems and architectures using the --target flag, including Windows ARM64, macOS Silicon, and Linux variants—all from any host platform." | src: https://docs.deno.com/runtime/reference/cli/compile | quote: "Developers can target different operating systems and architectures using the --target flag" | type: official

- [C26] deno compile 支持框架自动检测（Deno 2.8+）。"Starting with Deno 2.8, the compiler automatically detects web frameworks like Next.js, Astro, Fresh, React Router, SvelteKit" | src: https://docs.deno.com/runtime/reference/cli/compile | quote: "Starting with Deno 2.8, the compiler automatically detects web frameworks" | type: official

- [C27] deno compile 支持实验性 --bundle 选项优化二进制大小。"The experimental --bundle flag tree-shakes dependencies using esbuild, embedding only reachable code" | src: https://docs.deno.com/runtime/reference/cli/compile | quote: "The experimental --bundle flag tree-shakes dependencies using esbuild" | type: official

### 内置工具链——deno bundle
- [C28] deno bundle 仍存在但状态为实验性。"deno bundle is classified as **experimental**...is currently an experimental subcommand and is subject to changes." | src: https://docs.deno.com/runtime/reference/cli/bundle | quote: "deno bundle is currently an experimental subcommand and is subject to changes" | type: official

- [C29] deno bundle 不推荐替代复杂构建工具。"deno bundle should not be viewed as a replacement for complex or interactive build tools such as Vite or webpack." | src: https://docs.deno.com/runtime/reference/cli/bundle | quote: "deno bundle should not be viewed as a replacement for complex or interactive build tools such as Vite or webpack" | type: official

### Deno Deploy——Deno 2 支持
- [C30] Deno Deploy 完全重写，使用 Deno 2.0。"Deno Deploy represents a complete redesign from Deploy Classic, utilizing Deno 2.0 for significantly enhanced capabilities." | src: https://docs.deno.com/deploy | quote: "Deno Deploy represents a complete redesign...utilizing Deno 2.0" | type: official

- [C31] Deno Deploy 支持 Deno 和 Node.js 应用。"Full support for Deno and Node.js applications" | src: https://docs.deno.com/deploy | quote: "Full support for Deno and Node.js applications" | type: official

### Deno Deploy——npm 包支持
- [C32] Deno 2 支持 98%+ npm 包。"Deno 2.0 is production-ready, NPM-compatible, with support now covering 98%+ of npm packages." | src: https://docs.deno.com/runtime/fundamentals/node | quote: "98%+ of npm packages" | type: secondary

- [C33] Deno 2 支持 npm: 说明符导入 npm 包。"Packages can be imported using the npm: specifier: import * as emoji from \"npm:node-emoji\";" | src: https://docs.deno.com/runtime/fundamentals/node | quote: "import * as emoji from \"npm:node-emoji\"" | type: official

### Deno Deploy——Node API 兼容
- [C34] Deno 2.8+ 通过 75% Node 测试套件。"As of Deno 2.8, **over 75% of Node's own test suite passes** in Deno, covering nearly every node: module." | src: https://docs.deno.com/runtime/fundamentals/node | quote: "over 75% of Node's own test suite passes" | type: official

- [C35] Node API 有已知限制。"Some APIs are partial...Packages with native addons need a local node_modules directory...A few tools assume npm's exact on-disk layout" | src: https://docs.deno.com/runtime/fundamentals/node | quote: "Some APIs are partial...Packages with native addons need a local node_modules" | type: official

### Deno Deploy——已知限制
- [C36] Deno Deploy 单次部署大小限制 1GB。"The total size of all files within the deployment (source files and static files) **should not exceed 1 gigabyte**." | src: https://docs.deno.com/deploy/pricing_and_limits | quote: "should not exceed 1 gigabyte" | type: official

- [C37] Deno Deploy 内存限制 512MB。"Applications are restricted to a maximum of 512MB of memory allocation." | src: https://docs.deno.com/deploy/pricing_and_limits | quote: "maximum of 512MB of memory allocation" | type: official

- [C38] Deno Deploy HTTPS 出站需要 TLS 终止。"Direct connections to port 443 using Deno.connect are prohibited; developers must use Deno.connectTls instead for TLS connections." | src: https://docs.deno.com/deploy/pricing_and_limits | quote: "Direct connections to port 443 using Deno.connect are prohibited" | type: official

- [C39] Deno Deploy Beta 不提供正常运行时间保证。"During the public beta phase, no uptime guarantees are offered" | src: https://docs.deno.com/deploy/pricing_and_limits | quote: "no uptime guarantees are offered" | type: official

## conflicts
- C34 和 C35 之间的平衡性：Deno 2.8+ 通过 75% Node 测试，但仍有部分 API 不完整或需要 native 模块的 node_modules 目录。这不是矛盾而是正常的迁移现状。无冲突。

## gaps
- Deno Deploy 对具体 Node.js 内置模块的兼容程度百分比（只有 Deno 的 75% 总体数据）
- Deno Deploy 是否原生支持 npm: 说明符（只确认 Deno 运行时支持）
- deno.json 中 "permissions" 字段最早引入版本（仅知 2.5+）
- deno test 对 node:test 格式的支持细节
- 配置文件中是否可声明 -A (allow-all) 权限

## leads
- Deno Deploy Classic 退役日期 2026-07-20，需确认新版本 GA 日期和迁移限制
- deno compile 的 --engine 选项（V8 vs QuickJS）在 Deno Deploy 中的支持状态
- Deno Deploy 对原生扩展模块的限制（C-extensions/WASM）
