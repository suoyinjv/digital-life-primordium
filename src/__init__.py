"""Digital Life Primordium — 主模块

DLP系统的顶层入口，协调认知引擎、记忆、世界模拟器和执行器的协作。
"""

from cognitive_engine import CognitiveEngine, create_engine
from memory import TopologicalMemory, create_memory
from world_simulator import WorldSimulator, create_simulator
from executor import Executor, create_executor


class DigitalLifePrimordium:
    """数字生命原基——DLP系统主类"""
    
    def __init__(
        self,
        name: str = "DLP-1",
        memory_dim: int = 256
    ):
        self.name = name
        self.cognitive_engine: CognitiveEngine = create_engine()
        self.memory: TopologicalMemory = create_memory(dim=memory_dim)
        self.simulator: WorldSimulator = create_simulator()
        self.executor: Executor = create_executor()
        self._is_active = False
    
    def activate(self) -> None:
        """激活DLP——启动感知-推理-行动循环"""
        self._is_active = True
        # TODO: 实现主循环
        pass
    
    def deactivate(self) -> None:
        """停用DLP"""
        self._is_active = False
    
    @property
    def status(self) -> dict:
        """DLP当前状态摘要"""
        return {
            "name": self.name,
            "active": self._is_active,
            "memory_entropy": self.memory.entropy if hasattr(self.memory, 'entropy') else None,
            "active_avatars": self.executor.active_avatar_count,
        }


def create_dlp(name: str = "DLP-1") -> DigitalLifePrimordium:
    """创建一个DLP实例"""
    return DigitalLifePrimordium(name=name)
