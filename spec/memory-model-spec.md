# 记忆模型 - 规格说明

## 概述

记忆模型采用 **认知拓扑流形（Cognitive Topological Manifold）** 作为核心数据结构，将记忆表征为高维空间中的连续流形。记忆不再是无序的键值对存储，而是在拓扑空间中通过邻近关系、路径连接和曲率度量自然组织。该模型支持联想回忆、经验泛化和遗忘压缩三大核心操作。

## 核心数据结构

### 记忆节点（MemoryNode）
```
MemoryNode {
  id: UUID
  embedding: Vector<float64, D>  // D 维嵌入向量
  content: MemoryContent
  timestamp: float64
  importance: float64           // [0, 1]
  access_count: uint64
  last_access: float64
  decay_rate: float64           // 遗忘衰减率
}
```

### 记忆流形（MemoryManifold）
```
MemoryManifold {
  nodes: Map<UUID, MemoryNode>
  adjacency: SparseMatrix<float64>  // 节点间相似度/距离
  metric: MetricType                // 可选：欧氏 / 余弦 / 双曲
  curvature: float64                // 流形曲率参数
  dimension: uint8                  // 嵌入维度
}
```

### 遗忘因子（ForgetFactor）
```
ForgetFactor {
  base_decay: float64     // 基准衰减率 0.001
  importance_decay: float64  // 重要性加权
  time_decay: float64        // 时间指数衰减
  consolidation_boost: float64  // 巩固增益
}
```

## 接口定义

```
interface MemoryModel {
  store(content: MemoryContent, context: Context) -> UUID
  recall(query: Vector<float64>, k: uint8) -> MemoryRecord[]
  associate(source_id: UUID, relation: RelationType, target_id: UUID) -> void
  forget(node_id: UUID) -> void
  consolidate() -> void  // 记忆巩固：重复回忆节点提升重要性
  compress(threshold: float64) -> uint64  // 压缩低重要性节点，返回移除数
  get_manifold_snapshot() -> MemoryManifold
}
```

## 状态机 / 行为约束

记忆模型的生命周期：

```
FORMATION -> CONSOLIDATION -> STORAGE -> RETRIEVAL
                  |                         |
                  v                         v
             REINFORCEMENT             DECAY -> EVICTION
```

**约束条件**：
1. **遗忘机制**：每个记忆节点按指数衰减 `importance(t) = importance_0 * e^(-decay_rate * t)`，当 importance < 0.05 时标记为可回收
2. **巩固阈值**：同一记忆节点在 24 小时内被访问 ≥ 3 次，触发 consolidation_boost，衰减率减半
3. **流形维度约束**：嵌入维度 D 固定为 128，变更需重新构建整个流形
4. **最大容量**：流形节点上限 50,000，超出时触发 compress(threshold=0.1)
5. **联想距离**：recall 操作仅返回 k 个节点中距离 ≤ 0.85 的节点（余弦距离），超出视为无关记忆
