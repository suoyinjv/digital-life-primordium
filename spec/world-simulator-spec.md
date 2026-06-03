# 世界模拟器 - 规格说明

## 概述

世界模拟器（World Simulator）维护数字孪生环境，负责对外部世界状态的建模、推演和路径优选。它接收来自认知引擎的预测请求，在内部仿真环境中执行"what-if"推演，并返回优选路径和预期结果。数字孪生通过多源感知数据持续更新，确保与真实世界保持同步。

## 核心数据结构

### 世界状态（WorldState）
```
WorldState {
  timestamp: float64
  entities: Map<EntityID, EntityState>
  relationships: RelationGraph
  environment: EnvironmentParams
  confidence: float64            // 对当前状态的置信度
}
```

### 推演节点（SimulationNode）
```
SimulationNode {
  state: WorldState
  parent: NodeID | null
  children: NodeID[]
  action: Action | null
  reward: float64
  cumulative_reward: float64
  visit_count: uint64
  depth: uint16
}
```

### 推演树（SimulationTree）
```
SimulationTree {
  root: NodeID
  nodes: Map<NodeID, SimulationNode>
  horizon: uint16           // 推演时间步数上限
  branching_factor: uint8   // 每层最大分支数
  strategy: SearchStrategy  // MCTS / A* / Greedy
}
```

### 路径优选结果（PathResult）
```
PathResult {
  optimal_path: Action[]
  expected_outcome: WorldState[]
  confidence_scores: float64[]
  alternative_paths: Action[][]
  computation_cost: float64 // 毫秒
}
```

## 接口定义

```
interface WorldSimulator {
  sync(source: SensorFeed) -> void                    // 同步数字孪生
  simulate(actions: Action[], horizon: uint16) -> SimulationTrace
  search(state: WorldState, goal: Goal) -> PathResult  // 路径优选
  predict(state: WorldState, action: Action) -> WorldState
  get_current_state() -> WorldState
  fork() -> WorldSimulator  // 创建分支模拟器用于并行推演
}
```

## 状态机 / 行为约束

世界模拟器的状态转移：

```
SYNCING -> IDLE -> SIMULATING -> SEARCHING -> EVALUATING -> IDLE
                   |                              |
                   v                              v
              BRANCHING                      BACKPROPAGATING
```

**约束条件**：
1. **推演深度**：单次推演 horizon 上限为 100 时间步，防止无限展开
2. **分支因子**：MCTS 模式下 branching_factor ≤ 8，A* 模式下 ≤ 4
3. **实时性**：单次 search 调用必须在 200ms 内返回结果（含推演）
4. **数字孪生同步**：sync 操作必须处理传感器延迟抖动（±20%），采用时间戳对齐策略
5. **路径优选算法**：默认使用 MCTS（蒙特卡洛树搜索），当 time_budget < 50ms 时降级为贪婪策略
6. **推演一致性**：同一初始状态下相同 action 序列的推演结果必须可复现（确定性随机种子）
