#!/usr/bin/env python3
"""hello_dlp.py — DLP概念演示示例

当前阶段（Phase 0），DLP尚无实际可运行的实现。
本示例演示了DLP的模块化架构和使用方式（纯概念性）。
"""

import sys
import os

# 添加源码路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from digital_life_primordium import DigitalLifePrimordium
except ImportError:
    # Phase 0: 所有模块均为占位符，导入失败是预期的
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     Digital Life Primordium — Phase 0 (概念预研)       ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║                                                        ║")
    print("║  本项目的所有模块目前均为概念占位符。                    ║")
    print("║  请从以下路径开始阅读：                                 ║")
    print("║                                                        ║")
    print("║  whitepaper/research-proposal.md   — 完整研究计划书    ║")
    print("║  ARCHITECTURE.md                   — 架构总览          ║")
    print("║  docs/                             — 模块化技术文档    ║")
    print("║  spec/                             — 架构规格说明      ║")
    print("║                                                        ║")
    print("║  欢迎通过 Issues 提交讨论或贡献。                       ║")
    print("║                                                        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    sys.exit(0)

# 如果导入成功（Phase 1+），创建并激活DLP
dlp = DigitalLifePrimordium(name="DLP-Demo")
print(f"DLP实例已创建: {dlp.name}")
print(f"状态: {dlp.status}")
print("正在激活...")
dlp.activate()
print("DLP已激活。")
print()
print("感知-推理-行动循环已启动。等待输入...")
