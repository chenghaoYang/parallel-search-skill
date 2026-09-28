# Taxonomy 网格 v2

R2 收束后。状态：✅ 一手+原句；⚠ 只有二手；⚔ 冲突；❓ 缺口；∅ 官方未写（已定向查过）；— 不适用。

## 分类轴

轴 1 保留：安装器（pip）/ 项目经理（uv、Poetry、PDM）/ 环境经理（pixi、conda）。conda 行已用官方文档填上，不再悬空。

轴 2 保留，并且现在能写成一句：pip 的实验锁就是 pylock；uv 与 Poetry 的日常锁是自有格式，pylock 只导出；PDM 可用 `lock.format` 切到 pylock；conda / pixi 用另一套锁。

`workspace` 继续按「多包是否共享一把锁」理解。pixi 的 `[workspace]` 是清单根（必填 `channels`、`platforms`），不是 uv 的 `members`。

## 维度

| 维度 | 这一列回答什么 |
|---|---|
| lock | 锁文件叫什么、能否读/写/安装 PEP 751 `pylock.toml` |
| meta | 依赖和项目元数据写在哪个表 |
| workspace | 多包是否共享一把锁，成员怎么声明 |
| pyver | 谁安装、谁钉死 Python |
| backend | 默认构建后端是谁 |
| index | 私有源 / channel 的配置键和凭证 |
| cicache | CI 该缓存哪个目录、哪个环境变量 |
| migrate | 官方迁入路径 |

## 实体 × 维度

| 实体 | 家族 | lock | meta | workspace | pyver | backend | index | cicache | migrate |
|---|---|---|---|---|---|---|---|---|---|
| pip | 安装器 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| uv | 项目经理 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Poetry | 项目经理 | ✅ | ✅ | ∅ | ⚔ | ✅ | ✅ | ✅ | ✅ |
| PDM | 项目经理 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pixi | 环境经理 | ✅ | ✅ | ✅ | ✅ | ⚔ | ✅ | ✅ | ✅ |
| conda | 环境经理 | ⚔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

⚔ 的三格：Poetry 的 pyver（不替你装 vs 2.1.0 实验命令）；pixi 的 backend（迁移页说还没做 vs `pixi publish`，且 `pixi-build` 是 preview）；conda 的 lock（“natively” vs 插件必须装进 base）。

未进格子：pip 25.1 / 26.1、uv 0.6.15 的数字不在摘录字符串里，只在工人报告的标题上。`pdm install` 读取现成 pylock 仍无原句。
