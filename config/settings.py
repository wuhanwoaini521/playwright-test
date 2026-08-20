"""全局配置管理 ⚙️.

企业级多环境配置：所有参数可通过环境变量覆盖，便于本地开发与 CI 无缝切换。

可用环境变量（前缀 ``PW_``）：
- ``PW_BASE_URL``         被测环境基础地址，默认 ``https://www.baidu.com``
- ``PW_HEADLESS``         是否无头模式，默认 ``true``
- ``PW_TIMEOUT``          全局操作超时（毫秒），默认 ``30000``
- ``PW_VIEWPORT_WIDTH``   视口宽度，默认 ``1920``
- ``PW_VIEWPORT_HEIGHT``  视口高度，默认 ``1080``
- ``PW_RETRIES``          失败重试次数，默认 ``0``
- ``PW_TRACING``          是否开启 trace 录制，默认 ``off``
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


def _env(name: str, default: str) -> str:
    """读取环境变量，缺失时返回默认值。"""
    return os.getenv(name, default)


def _env_bool(name: str, default: bool) -> bool:
    """读取布尔型环境变量。"""
    return _env(name, "true" if default else "false").strip().lower() in ("1", "true", "yes", "on")


def _env_int(name: str, default: int) -> int:
    """读取整型环境变量。"""
    try:
        return int(_env(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    """Playwright 测试框架全局配置（不可变对象）。"""

    # 被测环境基础地址
    base_url: str = field(default_factory=lambda: _env("PW_BASE_URL", "https://www.baidu.com"))
    # 是否无头模式
    headless: bool = field(default_factory=lambda: _env_bool("PW_HEADLESS", True))
    # 全局操作超时（毫秒）
    timeout: int = field(default_factory=lambda: _env_int("PW_TIMEOUT", 30000))
    # 浏览器视口
    viewport_width: int = field(default_factory=lambda: _env_int("PW_VIEWPORT_WIDTH", 1920))
    viewport_height: int = field(default_factory=lambda: _env_int("PW_VIEWPORT_HEIGHT", 1080))
    # 失败重试次数
    retries: int = field(default_factory=lambda: _env_int("PW_RETRIES", 0))
    # trace 录制模式: off / on / retain-on-failure
    tracing: str = field(default_factory=lambda: _env("PW_TRACING", "retain-on-failure"))


# 模块级单例，供各层直接导入使用
settings = Settings()
