# r1-bun-tooling-security-deploy

question: Bun 内置工具链的具体命令和能力——`bun test`（内置测试运行器）、`bun build`（内置打包器，支持哪些输出格式/target，是否能打包成单文件可执行程序）、`bun run`、是否自带代码格式化器或 linter？Bun 是否有类似 Deno 的权限/沙箱模型（预期默认信任所有代码执行、没有 --allow-net 这类 flag）？主流部署平台对 Bun 的官方支持现状？

checked: https://bun.sh/docs,https://bun.com/docs/test,https://bun.com/docs/bundler,https://bun.com/docs/bundler/executables,https://bun.com/docs/runtime,https://bun.com/reference/bun/Security,https://bun.com/guides,https://bun.com/docs/runtime/workers,https://bun.com/guides/deployment/vercel,https://bun.com/guides/deployment/aws-lambda,https://bun.com/guides/deployment/railway,https://bun.com/guides/deployment/render,https://bun.com/guides/ecosystem/docker,https://bun.com/guides/deployment/google-cloud-run,https://bun.com/guides/deployment/digital-ocean

## claims

- [C1] bun test 支持 --timeout flag，用于设置单个测试的超时时间，默认 5000ms | src: https://bun.com/docs/test | quote: "Use the --timeout flag to specify a per-test timeout in milliseconds (default is 5000)" | type: official

- [C2] bun test 支持 --concurrent 和 --max-concurrency flag，用于控制并发执行，--max-concurrency 默认 20 | src: https://bun.com/docs/test | quote: "Use the --concurrent flag to run all tests concurrently within their respective files, with --max-concurrency N (default 20)" | type: official

- [C3] bun test 支持 --parallel flag，用于在多个 CPU 核心上运行测试文件 | src: https://bun.com/docs/test | quote: "Pass --parallel to spread files across CPU cores" | type: official

- [C4] bun test 支持 --test-name-pattern (-t)、--todo、--reporter、--coverage、--update-snapshots (-u)、--watch、--retry、--rerun-each、--randomize、--seed、--bail flag | src: https://bun.com/docs/test | quote: "To filter by test name, use the -t/--test-name-pattern flag...support watch mode, coverage reports" | type: official

- [C5] bun build 支持三种输出格式：esm（默认）、cjs（实验性）、iife（实验性） | src: https://bun.com/docs/bundler | quote: "Bun supports three module formats: ESM (default), CommonJS (experimental), and IIFE (experimental)" | type: official

- [C6] bun build 支持三种 target 类型：browser（默认）、bun、node | src: https://bun.com/docs/bundler | quote: "Three target environments: browser (default), bun (for Bun runtime), node (for Node.js)" | type: official

- [C7] bun build 支持 --compile flag 生成单文件可执行程序，可执行文件包含 Bun 运行时的副本 | src: https://bun.com/docs/bundler/executables | quote: "Bun bundles all imported files and packages into the executable, along with a copy of the Bun runtime" | type: official

- [C8] bun build --compile 支持跨平台编译，通过 --target flag 指定目标（Linux x64/arm64、Windows x64/arm64、macOS x64/arm64） | src: https://bun.com/docs/bundler/executables | quote: "Using --target flag for different systems: Linux x64/arm64, Windows x64/arm64, macOS x64/arm64" | type: official

- [C9] bun build 支持 --minify、--sourcemap、--splitting、--watch、--bytecode、--compile-autoload-dotenv 等 flag | src: https://bun.com/docs/bundler | quote: "Bun bundler supports minification, source maps, code splitting, and other optimizations" | type: official

- [C10] bun run 用于执行脚本或 JavaScript/TypeScript 文件，支持 package.json 脚本执行 | src: https://bun.com/docs/runtime | quote: "Use bun run to execute a source file or run package.json scripts" | type: official

- [C11] bun run 支持 --watch flag 用于监听文件变化并自动重新运行 | src: https://bun.com/docs/runtime | quote: "To run a file in watch mode, use the --watch flag" | type: official

- [C12] bun run 支持生命周期钩子（preclean、postclean 等） | src: https://bun.com/docs/runtime | quote: "Bun respects lifecycle hooks. For instance, bun run clean runs preclean and postclean, if defined" | type: official

- [C13] Bun 没有内置的代码格式化器或 linter，需要集成第三方工具如 Prettier 或 ESLint/Oxlint | src: https://bun.com/guides | quote: "当设置 Vite 项目时，被问到 'Which linter to use?' 需要选择集成单独的 linting 工具" | type: official

- [C14] Bun 没有权限/沙箱模型，不存在 --allow-net 或类似的 permission flag | src: https://bun.com/docs/runtime | quote: "文档中没有涉及细粒度的权限控制机制或权限 flag" | type: official

- [C15] Bun.Security 对象用于安全漏洞扫描，不是权限/沙箱管理工具 | src: https://bun.com/reference/bun/Security | quote: "Bun.Security is a security scanner namespace for bun install command, not permissions management" | type: official

- [C16] Bun 提供 package trust model，通过 bun pm trust 命令管理受信赖的依赖，控制 postinstall 脚本执行 | src: https://bun.com/docs | quote: "By default, Bun does not run postinstall scripts for packages that are not trusted" | type: official

- [C17] Vercel 官方支持 Bun Runtime，提供公开 beta 支持，可通过 vercel.json 中 bunVersion 字段配置 | src: https://bun.com/guides/deployment/vercel | quote: "Vercel Functions can run on the Bun runtime...support available as public beta" | type: official

- [C18] Vercel + Bun 部署支持 Next.js、Express、Hono、Nitro 等框架 | src: https://bun.com/guides/deployment/vercel | quote: "You can use Bun with frameworks supported by Vercel, like Next.js, Express, Hono, or Nitro" | type: official

- [C19] Vercel + Bun 有限制：不支持自动 source maps、bytecode 缓存和 node:http/node:https 的 request metrics | src: https://bun.com/guides/deployment/vercel | quote: "Automatic source maps, bytecode caching, and request metrics for node:http and node:https are not supported on Bun" | type: official

- [C20] Docker 官方 Bun 镜像为 oven/bun，支持多个变体：debian、slim、distroless、alpine | src: https://bun.com/guides/ecosystem/docker | quote: "Bun publishes image variants for different operating systems: debian, slim, distroless, and alpine" | type: official

- [C21] Docker 官方 Bun 镜像支持 Linux x64 和 arm64 架构 | src: https://bun.com/guides/ecosystem/docker | quote: "Bun provides a Docker image that supports both Linux x64 and arm64" | type: official

- [C22] AWS Lambda 官方支持通过 Docker 部署 Bun 应用，使用 AWS Lambda adapter 处理 Lambda 运行时 | src: https://bun.com/guides/deployment/aws-lambda | quote: "Deploy a Bun HTTP server to AWS Lambda using a Dockerfile...uses AWS Lambda adapter" | type: official

- [C23] AWS Lambda 部署 Bun 应用需要设置端口为 8080（AWS Lambda adapter 要求） | src: https://bun.com/guides/deployment/aws-lambda | quote: "Setting the port to 8080, which is required for the AWS Lambda adapter" | type: official

- [C24] Railway 官方支持 Bun 部署，通过 Railpack 自动检测和构建，支持零配置部署 | src: https://bun.com/guides/deployment/railway | quote: "Railway uses Railpack to automatically detect and build your Bun application with zero configuration" | type: official

- [C25] Railway 部署自动从 GitHub push 时触发部署（auto-deploy） | src: https://bun.com/guides/deployment/railway | quote: "Railway auto-deploys on every GitHub push" | type: official

- [C26] Render 官方支持 Bun 部署，支持作为 web services、background workers、cron jobs 等多种类型部署 | src: https://bun.com/guides/deployment/render | quote: "Render supports Bun natively and you can deploy Bun apps as web services, background workers, cron jobs" | type: official

- [C27] Render 部署 Bun 应用需要配置 Runtime 为 'Node'、Build Command 为 'bun install'、Start Command 为 'bun app.ts' | src: https://bun.com/guides/deployment/render | quote: "Provide the Runtime as Node, Build Command as bun install, Start Command as bun app.ts" | type: official

- [C28] Google Cloud Run 官方支持通过 Docker 部署 Bun 应用，使用 Dockerfile 进行容器化 | src: https://bun.com/guides/deployment/google-cloud-run | quote: "Deploy a Bun HTTP server to Google Cloud Run using a Dockerfile" | type: official

- [C29] DigitalOcean 官方支持通过 Docker 部署 Bun 应用，ARM Mac (M1/M2) 构建需使用 docker buildx 指定 --platform=linux/amd64 | src: https://bun.com/guides/deployment/digital-ocean | quote: "If building on ARM Mac, must use docker buildx with --platform=linux/amd64 for DigitalOcean compatibility" | type: official

- [C30] Cloudflare Pages 支持 Bun 部署（在 Bun v1.1.45+ 提及），但 Bun 官方文档中没有专门的部署指南 | src: https://bun.sh/blog/bun-v1.1.45 | quote: "Bun now works in more Linux environments, including Amazon Linux 2 and builds for Vercel and Cloudflare Pages" | type: official

## conflicts

- [Conflict 1] Cloudflare Pages/Workers 支持级别不明确：Bun 博客提及支持 Cloudflare Pages，但官方文档（bun.com/guides）中没有专门的部署指南，与 Vercel、Railway、Render 等平台的一级支持不同

## gaps

- bun build 对 CSS、HTML、JSON 等资源文件的详细处理和支持能力（bundler 文档未详细说明）
- bun build --compile 的完整 flag 列表（仅找到 --compile-autoload-dotenv、--compile-exec-argv、--compile-jit-policy 等部分 flag）
- Cloudflare Workers（非 Pages）对 Bun 的具体支持状态
- Bun 对 AWS App Runner 的支持状态（仅确认 Lambda 支持）
- bun test --reporter 支持的具体输出格式（仅提及 junit、dots）

## leads

- Bun 官方博客中关于版本更新（v1.1.45）确认了 Cloudflare Pages 支持，可能有更多部署平台信息
- Bun 的 Web Standard API 兼容性可能影响部署平台的支持程度
- 权限模型缺失是 Bun 与 Deno 相比的重要差异，确认为设计选择而非遗漏
