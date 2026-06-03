# 认知引擎 - 规格说明

## 概述

认知引擎（Cognitive Engine）是数字生命体的核心推理中枢，由因果推理器（Causal Reasoner）和世界模拟器的认知层共同构成。它负责将感知输入转化为结构化因果模型，并驱动决策生成。认知引擎遵循 **预测编码-因果追溯** 双循环架构，在感知-行动闭环中持续更新内部因果图。

## 核心数据结构

### 因果图（CausalGraph）
```
CausalGraph {
  nodes: Map<EntityID, CausalNode>
  edges: Map<EdgeID, CausalEdge>
  version: uint64
  timestamp: float64
}
```
- `CausalNode`：每个实体包含属性集、状态向量、置信度分数
- `CausalEdge`：有向边，标记因果关系类型（cause / enable / inhibit / correlate）及权重

### 认知状态（CognitiveState）
```
CognitiveState {
  belief: Map<PropositionID, Belief>
  intention: IntentionStack
  attention: AttentionMask
  uncertainty: float64
}
```

### 推理记录（InferenceRecord）
```
InferenceRecord {
  input_signals: Signal[]
  activated_nodes: NodeID[]
  inferred_edges: EdgeID[]
  prediction: Prediction
  prediction_error: float64
  timestamp: float64
}
```

## 接口定义

### 因果推理器接口
```
interface CausalReasoner {
  infer(signals: Signal[], context: Context) -> InferenceResult
  update_graph(feedback: Feedback) -> void
  query(query: CausalQuery) -> CausalAnswer
  get_belief_state() -> CognitiveState
}
```

### 认知层接口（对接世界模拟器）
```
interface CognitiveLayer {
  perceive(state: WorldState) -> Perception
  predict(action: Action) -> ExpectedOutcome
  reconcile(actual: WorldState, expected: ExpectedOutcome) -> Delta
  consolidate() -> void  // 将短期推理沉淀为长期因果知识
}
```

## 状态机 / 行为约束

认知引擎的状态转移如下：

```
IDLE -> PERCEIVING -> REASONING -> PREDICTING -> ACTING -> RECONCILING -> IDLE
                      |                                     |
                      v                                     v
                   UPDATING_GRAPH                      LEARNING
```

**约束条件**：
1. 每轮推理最多触发 3 次因果回溯（防止无限循环）
2. 因果图节点数上限为 10,000，超出触发遗忘/压缩策略
3. 认知状态中的不确定性（uncertainty）超过阈值 0.7 时，引擎必须切换到探索模式（而非利用模式）
4. 认知层 reconcile 必须在收到实际世界状态后 50ms 内完成
