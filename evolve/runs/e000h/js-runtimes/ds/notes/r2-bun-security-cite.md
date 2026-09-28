# r2-bun-security-cite
question: 为"Bun 没有类似 Deno 的运行时权限/沙箱模型（没有 --allow-net 这类 flag）"这个结论找到一条真正的官方页面原句引用或明确的设计说明；同时理清 `Bun.Security` 这个 API 具体是做什么的——它是依赖安装阶段的供应链安全扫描器，还是运行时权限控制？
checked: https://github.com/oven-sh/bun/discussions/725,https://bun.sh/docs/pm/security-scanner-api,https://bun.com/reference/bun/Security,https://bun.sh/blog/bun-v1.3,https://github.com/oven-sh/bun/issues/6617,https://github.com/oven-sh/bun/issues/25929

## claims

- [C1] Bun 的官方设计立场是用"binary dead code elimination based on statically analyzing what features/native modules are used"而非运行时权限检查来实现安全，表示不采用 Deno 式的权限模型 | src: https://github.com/oven-sh/bun/discussions/725 | quote: "Instead of checking if a feature is allowed at runtime, it is safer to just not have potentially unsafe or undesired code in the binary to begin with" | type: official

- [C2] Bun Security Scanner API 是在"package installation"（包安装）阶段运行的供应链安全工具，不是运行时权限系统 | src: https://bun.sh/docs/pm/security-scanner-api | quote: "Security scanners analyze packages during bun install, bun add, and other package operations to detect known CVEs, malicious packages, and license compliance issues" | type: official

- [C3] Bun Security Scanner 的扫描结果包含两个严重级别：fatal（立即停止安装）和 warn（交互式终端中提示继续；CI 中立即退出） | src: https://bun.sh/docs/pm/security-scanner-api | quote: "fatal: installation stops immediately with non-zero exit code; warn: in interactive terminals prompts to continue, in CI exits immediately" | type: official

- [C4] Bun 1.3 发布的 Security Scanner API 是与 Socket 合作推出的官方扫描器 @socketsecurity/bun-security-scanner，用于依赖包的前置安全扫描 | src: https://bun.sh/blog/bun-v1.3 | quote: "Bun is launching with Socket and their official security scanner: @socketsecurity/bun-security-scanner" | type: official

- [C5] Bun.Security 对象定义了 Scanner 接口（含 version 和 scan 方法）、Package 接口（name、version、requestedRange、tarball）、Advisory 接口（package、level、description、url），专用于包安装前的安全建议声明 | src: https://bun.com/reference/bun/Security | quote: "Bun.Security defines Scanner with version and scan() method, Package with name/version/requestedRange/tarball, Advisory with package/level/description/url for pre-install security recommendations" | type: official

- [C6] 权限系统是 Bun 社区开放 feature request（Issue #6617 等），但仍未实现；相比之下 Deno 2 已内建默认拒绝权限模型、Node.js 有 --permission flag | src: https://github.com/oven-sh/bun/issues/6617 | quote: "open enhancement request for sandboxing capabilities similar to Deno, labeled as feature request with no assigned developer" | type: official

## conflicts

- 无直接冲突。但值得注意的是：GitHub Issue #25929（"Bun as secure sandbox runtime"）被关闭为重复 Issue #6617，说明权限系统请求已存在，但官方暂未改变设计立场

## gaps

- 无法找到 Bun 官方文档中的明确否定性声明（如"Bun does not have a permissions system"）——官方倾向于通过 GitHub 讨论阐明设计哲学，而非在文档中直接说"我们没有 X"
- Bun 对于未来是否会实现权限系统的官方路线图说明（GitHub 中 Jarred-Sumner 提及"might explore runtime permission checks in the future"，但无具体承诺）

## leads

- GitHub Discussion #725 提供了权限模型设计哲学的最权威官方解释，可作为"为什么 Bun 选择不采用权限模型"的佐证
- Bun 官方博客（v1.3 发布说明）中关于 Security Scanner API 的描述清晰界定了这个工具仅限于"包安装阶段"，与运行时权限完全无关
