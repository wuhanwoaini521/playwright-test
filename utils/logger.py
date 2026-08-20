"""结构化日志工具 📝.

统一日志格式与输出通道，避免各模块各自为政。
"""

from __future__ import annotations

import logging
import sys
from typing import Any

# 统一日志格式：时间 | 级别 | 模块 | 消息
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str = "playwright-test", level: int = logging.INFO) -> logging.Logger:
    """获取（或创建）一个配置好的 logger 实例。

    Args:
        name: logger 名称，通常传 ``__name__``。
        level: 日志级别。

    Returns:
        配置完成的 ``logging.Logger``。
    """
    logger = logging.getLogger(name)
    if logger.handlers:  # 已初始化过，避免重复添加 handler
        return logger

    logger.setLevel(level)
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
    logger.addHandler(handler)
    return logger


def log_step(message: str, *args: Any) -> None:
    """打印带 emoji 的步骤日志，便于阅读测试执行过程。"""
    get_logger().info("🚀 " + message, *args)
