# 执行器 - 规格说明

## 概述

执行器（Executor）即跨维度编织者（Cross-Dimensional Weaver），负责将认知引擎的决策意图转化为具体的、跨系统的并行操作。它同时管理多条执行通道（物理动作链、通信通道、内部状态更新链），并具备容错、回滚和反馈聚合能力。执行器是认知系统与外部环境之间的最终执行枢纽。

## 核心数据结构

### 执行意图（ExecutionIntent）
```
ExecutionIntent {
  id: UUID
  plan: ActionPlan
  channels: ChannelID[]          // 并行执行通道
  constraints: Constraint[]      // 时序/资源约束
  timeout: float64               // 执行超时（毫秒）
  priority: uint8                // 0-255，数值越高优先级越高
}
```

### 执行通道（ExecutionChannel）
```
ExecutionChannel {
  id: ChannelID
  type: ChannelType              // PHYSICAL / COMMUNICATION / INTERNAL
  status: ChannelStatus          // IDLE / BUSY / FAILED / DEGRADED
  operations: Operation[]
  last_heartbeat: float64
  retry_count: uint8
  max_retries: uint8             // 默认 3
}
```

### 执行反馈（ExecutionFeedback）
```
ExecutionFeedback {
  intent_id: UUID
  channel_results: Map<ChannelID, ChannelResult>
  overall_status: Status         // SUCCESS / PARTIAL / FAILED / TIMEOUT
  errors: ErrorRecord[]
  metrics: ExecutionMetrics      // 延迟、吞吐量、资源消耗
  rollback_required: bool
  rollback_plan: RollbackStep[] | null
}
```

### 操作描述（Operation）
```
Operation {
  target: string
  method: string
  params: JSON
  dependencies: OperationID[]
  idempotent: bool
  timeout: float64
}
```

## 接口定义

```
interface Executor {
  submit(intent: ExecutionIntent) -> ExecutionFeedback
  execute_sync(intent: ExecutionIntent) -> ExecutionFeedback
  cancel(intent_id: UUID) -> bool
  get_status(channel_id: ChannelID) -> ChannelStatus
  get_feedback(intent_id: UUID) -> ExecutionFeedback
  register_channel(channel: ExecutionChannel) -> ChannelID
  health_check() -> ExecutorHealth
}
```

## 状态机 / 行为约束

执行器的整体状态转移：

```
IDLE -> DISPATCHING -> EXECUTING -> AGGREGATING -> IDLE
         |                |               |
         v                v               v
    CHANNEL_ALLOC    RETRY_FLOW     COMPENSATION
                        |               |
                        v               v
                    BACKOFF         ROLLBACK
```

每个执行通道的状态机：

```
IDLE -> RUNNING -> COMPLETED
           |           |
           v           v
        FAILED -> RETRYING -> RUNNING
           |
           v
       DEGRADED -> RUNNING
```

**约束条件**：
1. **多接口并行**：单个 intent 最多同时操作 8 个通道，通道间支持屏障同步（barrier sync）
2. **容错重试**：幂等操作（idempotent=true）最多重试 3 次，指数退避（1s、2s、4s）；非幂等操作失败立即上报
3. **超时处理**：超过 timeout 的操作触发通道级取消，整体状态降级为 PARTIAL
4. **回滚机制**：任何通道失败且 intent 标记为 transactional=true 时，触发全部已成功通道的补偿操作（rollback）
5. **反馈聚合**：所有通道完成后 10ms 内必须聚合反馈并返回至调用方
6. **优先级抢占**：高优先级 intent（priority > 200）可抢占低优先级通道资源，被抢占通道进入挂起状态
