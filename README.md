# Personal skills

个人维护的 skills 仓库。模块结构相关能力既可独立使用，也可通过 `module-structure` 组合使用。

## Paper Lookup

[paper-lookup](research/paper-lookup/SKILL.md) 提供 18 个学术 API 的调用说明及检索辅助脚本，存放于 `research/paper-lookup/`，由本仓库维护。上游仓库、路径和基准 commit 保留在 skill 的 metadata 中，更新采用审查后选择性合并。上游 MIT 许可证保留于 [LICENSE.md](research/paper-lookup/LICENSE.md)。

## Module Structure：独立能力与组合入口

**`cohesion-locality` 和 `modularity-review` 是两个可以独立安装、独立使用的 skill；`module-structure` 是它们的组合入口，帮助 agent 判断当前需要哪种分析，以及是否需要衔接下一步。**

| 目录 | 职责 | 使用方式 |
| --- | --- | --- |
| [`cohesion-locality/`](cohesion-locality/SKILL.md) | 设计新代码的职责与归属，也审查既有代码的拆分、合并或保持完整；依据内聚性、变化原因和局部性作决定。 | 可以独立使用，回答“哪些代码应该放一起”。 |
| [`modularity-review/`](modularity-review/SKILL.md) | 优化公开接口、信息隐藏、依赖和测试边界，按用户要求审查、设计或实现。 | 可以独立使用，处理接口与结构复杂度。 |
| [`module-structure/`](module-structure/SKILL.md) | 选择分析起点，说明何时组合两个 skill；不管理各 skill 的工作流程。 | 不确定该用哪个，或任务需要两种视角时使用。 |

这里的“组合调用”由同一 main agent 按需使用对应 skill，不要求每次把两个 skill 都执行一遍。审查可按责任范围并行分派 subagent，main 核验证据并汇总；设计仍由当前 agent 完整运用原则。

## 安装组合

- **只需要边界判断：** 安装完整的 `cohesion-locality/`。
- **只需要模块复杂度审查或优化：** 安装完整的 `modularity-review/`。
- **需要统一入口和组合流程：** 一起安装 `module-structure/`、`cohesion-locality/`、`modularity-review/`，推荐保持同一仓库版本。

保留所选目录中的参考文件等资源。组合安装时保留三个目录的同级关系，方便相互定位。当前没有自动安装依赖的包管理机制；只安装 `module-structure` 不会自动带上另外两个 skill。

独立安装时，在自身职责内完成任务即可。若后续工作需要未安装的另一项能力，应说明缺少哪项支持，并根据已有证据继续可完成的部分；不要声称已经调用不存在的 skill，也不要仅因组合入口未安装而停止本职工作。

## 组合入口如何判断

- 用户只问是否拆分、合并或保持完整：用 `cohesion-locality`，回答完成即可结束。
- 用户审查接口泄漏、浅层封装或依赖问题：用 `modularity-review`；只有发现边界不清楚时才补充边界判断。
- 用户既要判断边界又要优化设计或实现：先得到边界结论，再带着结论继续所需的设计或实现。

组合入口只负责选择与组合，不强制固定流水线。`cohesion-locality` 交付归属与拆合结论、证据、约束和未决问题；`modularity-review` 消费这些结论，自行选择工作模式，只在影响建议的归属问题仍不清楚时补充边界分析。两个技能都能直接继续用户原任务，无需返回组合入口读取规则。审查不会因为发现需要改代码而自动转为实现；已有实现授权也不会因分析步骤改变而丢失。

这三个目录保留独立 skill 入口，不计划仅为组合使用而把两个下游 skill 降为内部参考文件。

## 并行审查

手动触发且审查范围不明确时，main 先询问未提交改动、最近一次/指定提交范围或 PR、某个项目/模块等目标；确认缺失的项目、路径和版本范围后再开始。已有明确范围直接沿用，只问缺失信息，不让 subagent 重复询问。设计请求仍按设计处理，不弹出审查范围选择。

Main 先读取项目根与目标目录适用的 `AGENTS.md`、相关架构/ADR 和项目 skill，再决定审查安排；不能只转交自己未读的路径。项目要求的专项审查单独分派一位 reviewer，例如医疗 reviewer 在干净上下文中读取项目医疗 skill 和规范、覆盖全部医疗维度。跨技能复用同一次专项安排，main 核验证据并统一汇总；不传整个会话，分派与报告遵守项目隐私规则。

按责任范围、共享合同与风险决定是否分派，不以行数或固定人数作为门槛。每位 reviewer 完整读取所用技能的原则，独立检查分配区域，并可沿调用和数据关系读取邻接代码。main 负责核验证据、处理分歧和语义去重，补查跨区状态、事务、生命周期与依赖；失败或未覆盖区域显式说明。审查期间不自动修改代码，也不按发现数量打质量分。

组合审查只保留一个 main，reviewer 不递归分派。具体流程由各技能自己的审查参考承接：内聚判断见[并行审查](cohesion-locality/references/review-checklist.md#parallel-review)，接口与依赖见[并行审查](modularity-review/references/review-report.md#parallel-review)。独立安装时不依赖组合入口或共享协议文件。

## 维护与验证

选择与组合规则维护在 `module-structure`，边界判断与结论维护在 `cohesion-locality`，边界结论的使用、公开接口分析与模式维护在 `modularity-review`。各入口保留独立使用所需的任务范围约束，不新增共享协议文件。修改职责或组合规则时，核对三个入口的选择条件、结论交付与使用方式及范围约束是否一致。修改后运行[回归检查](module-structure/evals/README.md)，分别报告数据一致性检查与真实 agent 行为回归。回归需要覆盖独立完成、直接组合、经入口选择、任务范围保持和缺少可选 skill 的情况。

`modularity-review` 的来源和 full fork 说明见[来源记录](modularity-review/README.md)，许可证见 [LICENSE](modularity-review/LICENSE)。

## 指令设计原则

以原则和可调整的默认方法引导 agent，而不是要求每次走固定流程、填满报告字段或达到设计方案数量。允许提出假设、反证和探索性方案，结论中区分事实、推断与探索建议。硬约束集中在用户授权、安全与行为契约、适用的项目硬规则，以及证据和验证结果的真实性。

内聚判断的代码案例及评估方式见 [cohesion-locality/evals](cohesion-locality/evals/README.md)，用于检查误报、漏报、证据质量和探索空间；不按措辞或固定文件布局判分。

## Skill 内部的按需加载

`cohesion-locality` 触发后完整读取 `SKILL.md` 中的共同词汇、核心原则和任务边界，设计与审查都适用。详细参考分别补充单元边界、归属与局部性、审查方法；规则来源与详细判断在参考中保留，核心原则不依赖按需读取才能获得。较长示例独立放在 `references/examples.md`，只有拿不准或具体对照有帮助时才读取。并行分派的执行细节仅在审查需要分派时加载。精简入口时保留有用信息，避免仅为减少行数而丢失判断依据。

这是 skill 内部的文档路由，与 `module-structure` 组合两个独立 skill 的路由不同；参考文件没有独立触发入口，也不要求每次全部加载。

完整原则是设计与审查的共同基础，参考按当前问题读取，不设文件数量目标；清单和案例不作为设计前置步骤。内聚检查决定规则、状态和生命周期的归属；公开接口形状、泄漏和依赖方向继续由 `modularity-review` 深化。

后续真实行为评估使用实际项目的提交及其上下文进行；当前合成案例作为补充材料，不作为真实项目效果的证明。评估时固定项目基线和 skill 版本，保留原始审查输出，并在审查完成后对照提交与测试证据判断误报、漏报和建议质量。
