# 日志

参数：rounds=3 workers=6 budget=9000 dir=./ds worker-model=swe-2-shim

## R0

观察：用户要的是选型认知，不是工具手册。种子里的 pip / uv / Poetry / PDM 同属 PyPI，pixi / conda 是另一生态；若只做一张功能对照表，会把「安装器」和「环境管理器」比成同类。

决策：taxonomy v0 用三轴。轴 A 解析生态、轴 B 管到哪一层，用来分家族；轴 C（PEP 621 / 517 / 751）只解释家族内部差异。conda 先占一行但 R1 不派专员，留给 scout 判断是否值得 R2 立项。维度 10 个，覆盖点名的锁、workspace、Python 版本、构建后端，加上迁移、CI 缓存、私有源。

spawn：0

字数：尚无成稿。
