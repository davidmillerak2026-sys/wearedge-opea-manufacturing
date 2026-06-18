# 不是让大模型替厂长做决定：OpenAI 制造业 AI 的正确控制边界

本公开技术分享记录 WearEdge Pro 面向 OpenAI 原生能力的升级架构，并明确区分：

1. 仓库当前已经验证的 OPEA、RAG、确定性评估、守护规则和 OpenAI-compatible 适配边界；
2. 下一阶段计划加入的 OpenAI Responses、图像理解、严格函数工具和结构化输出。

## 核心观点

制造业真正需要的不是万能聊天机器人，而是把现场图片、操作员描述和设备信号转换成有来源、有合同、有边界、有人负责的行动。

WearEdge Pro 把现场决策拆成五条隔离路线：

| 路线 | 决策目标 | 企业系统目标 |
| --- | --- | --- |
| `maintenance` | 设备状态是否需要维护升级 | `maintenance_work_order` |
| `iqc` | 缺陷证据是否需要隔离或质量复核 | `qms_quality_event` |
| `changeover` | 换型证据是否达到人工签核条件 | `changeover_checklist` |
| `wi` | 应引用哪一版已发布作业指导书 | `wi_reference` |
| `hazard` | 是否需要停工、整改或 EHS 上报 | `ehs_case` |

每条路线拥有独立知识、目标系统、责任人、人类门槛和禁止性声明。维护智能体不能授予安全许可；质量智能体不能放行批次；换型智能体不能批准复机；EHS 智能体不能凭一张图断言事故最终根因。

## OpenAI 应该位于哪里

```text
M400 图片 / 操作员语音或文本 / 设备信号
  -> 边缘脱敏、压缩与资产身份确认
  -> WearEdge Gateway
  -> 五路线注册表与严格请求合同
  -> TEI / Qdrant 路线专属知识检索
  -> OpenAI Responses API
       - 图像与文本理解
       - 基于来源的解释
       - 严格工具选择
       - 结构化行动草案
  -> 确定性工业评估器
  -> 守护规则与禁止性声明
  -> 人类审批
  -> CMMS / QMS / MES / WI / EHS
  -> 审计与评估记录
```

OpenAI 可以负责：

- 理解第一视角图像与操作员语言；
- 根据检索到的已发布知识解释证据；
- 从最小权限工具集合中选择候选动作；
- 输出满足固定 JSON 合同的行动草案。

OpenAI 不应负责：

- 修改工业阈值；
- 跳过缺失确认；
- 授予复机、质量放行、安全许可或最终处置；
- 在身份、来源或知识修订不明确时继续执行。

因此，正确的控制原则是：

> OpenAI 负责理解与编排，确定性工业规则负责裁决，人类负责授权。

## 为什么确定性评估器必须保留

当前代码已经把关键工业检查写成可测试逻辑：维护路线检查振动、温度、润滑周期和 PLC 报警；IQC 比较检测置信度与质量计划阈值；换型检查清线、标签卷、配方和首件；WI 检查设备身份、发布版本、护罩和报警；Hazard 检查运动部件、通道和 PPE。

模型可以解释这些信号，但不能私自改变它们。生产系统应采用双层判定：

1. 模型识别证据、提取字段、提出候选工具；
2. 服务端重新验证身份、来源修订、阈值、权限、必填证据和审批状态。

冲突或缺失时 fail closed，进入人工复核。

## 当前实现与 OpenAI 路线的边界

静态仓库核验确认：

- 当前默认模型路径是确定性模板；
- `llm_adapter.py` 支持 OpenAI-compatible `/v1/chat/completions`；
- 运行时未依赖官方 OpenAI SDK；
- 当前仓库没有经本次核验确认的真实 OpenAI 模型端点生产基准；
- 已有本地 Gemma 和 DeepSeek-compatible 端点记录不能等同于 OpenAI 模型证据。

因此，准确表述是：

> WearEdge Pro 已有 OpenAI-compatible 模型边界，并具备升级为 OpenAI 原生制造业推理与工具层的清晰路径。

## 评估数字如何正确解读

仓库的轻量路线评估记录 15/15 用例通过。确定性小型公开夹具的 300-call 基准记录约 249.6 calls/s、平均约 3.99 ms、p95 约 6.14 ms；另有 1、5、10 请求均无失败的小规模官方 OPEA GenAIEval `chatqnafixed` 兼容运行。

这些数据验证的是公开夹具、确定性代码路径和 API 合同，不是 OpenAI 推理延迟、完整图像吞吐、工厂 SLA 或安全认证。

引入 OpenAI 后，应分别测量边缘采集、检索、模型、工具、规则、审批、成本、失败和恢复时间。

## 生产化必须补齐的能力

- 登录、RBAC、工厂/租户隔离和最小权限服务身份；
- 严格 Pydantic 请求合同、大小限制、超时、重试、熔断和幂等；
- Qdrant 与嵌入服务内网隔离；
- 图像脱敏、数据分类、保留周期和地区策略；
- 输入证据、来源修订、模型/提示版本、工具、规则、审批和写入结果的不可抵赖审计；
- strict function schemas、Structured Outputs 和服务端二次校验；
- 漏报、误报、错误路线、错误工具、越权声明、拒答、低质量图像和提示注入评估；
- 明确降级状态，不在生产中静默掩盖模型或向量库故障。

## 完整材料

- 中文长文：[`public/openai-centered-manufacturing-ai-zh.md`](../blob/main/public/openai-centered-manufacturing-ai-zh.md)
- English article: [`public/openai-centered-manufacturing-ai-en.md`](../blob/main/public/openai-centered-manufacturing-ai-en.md)
- 仓库核验：[`docs/repository-verification-2026-06-18.md`](../blob/main/docs/repository-verification-2026-06-18.md)
- OpenAI 原生集成蓝图：[`docs/openai-native-integration-blueprint.md`](../blob/main/docs/openai-native-integration-blueprint.md)
- 20 平台发布包：[`docs/20-platform-publication-pack-2026-06-18.md`](../blob/main/docs/20-platform-publication-pack-2026-06-18.md)
- 发布台账：[`docs/20-platform-publication-status-2026-06-18.md`](../blob/main/docs/20-platform-publication-status-2026-06-18.md)

## 讨论邀请

欢迎围绕以下问题提出可执行反馈：

- 五条路线的隔离是否足够清晰；
- 哪些条件必须 fail closed；
- OpenAI 工具应该如何最小化权限；
- 哪些指标能够证明工业价值而不是只证明模型流畅；
- 如何设计维护、质量、换型、WI 和 EHS 的独立发布门槛。

这不是让大模型替厂长做决定，而是让工厂更快看见问题、更完整保留证据、更一致执行流程，并在关键授权点上主动停下来。
