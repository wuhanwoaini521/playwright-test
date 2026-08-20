"""pytest 自定义标记 🔖.

集中声明测试标记，避免使用未注册标记时的警告。
"""

from __future__ import annotations


def pytest_configure(config) -> None:
    """注册自定义标记。"""
    config.addinivalue_line("markers", "smoke: 冒烟测试，快速验证核心主链路")
    config.addinivalue_line("markers", "regression: 回归测试，覆盖完整功能")
    config.addinivalue_line("markers", "slow: 慢速测试（标记后可单独跳过或分片）")
