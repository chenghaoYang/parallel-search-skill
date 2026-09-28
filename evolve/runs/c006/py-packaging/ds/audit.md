# 终审判定汇总（41 条）

## verify-pip（6 条）
V1–V6 全部 confirmed：PEP 751 Final/文件名、pip 25.1 `pip lock`、26.1 `-r pylock.toml`、锁文件单平台限制、scope 自述、认证三方式、setup-python cache。

## verify-uv（10 条）
V1–V8 confirmed。V9 无反例（uv 主锁不能是 pylock，issue #12584）。V10 无反例（迁移指南仅 pip→uv）。
修正：direct URL 依赖（`pkg @ https://user:pass@…`）的凭据会持久化——「凭据不写入」有例外，已改进 §4。

## verify-pixi（10 条）
V1–V3、V5–V8 confirmed。V4 走样：页面未提 `pixi add python=3.x`，已删该细节。V9 走样：「pip: 段进 [pypi-dependencies]」不在所引页，已删。V10 无反例：#3474/#3889 仍 open，repo 无 pylock 命中，最新 v0.81.0（2026-09-15）。

## verify-poetry-pdm（11 条）
V1–V5、V8–V11 confirmed。V6 无反例（无 workspace）。V7 无反例（无导入器）。
小注：Poetry `keyring.enabled 默认 true` 是行为描述而非字面 default 表——成稿表述已兼容（未声称字面默认值）。

## 未覆盖
矩阵其余格子（Poetry/PDM 私有源细节、pixi auth 细节）走自查：均已追到笔记 [C#]。未逐条核验项已在 §5 声明。
