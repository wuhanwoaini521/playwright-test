"""pytest 便捷命令行入口 🚀.

允许通过 ``pw-test`` 直接运行测试套件。
"""

from __future__ import annotations

import sys


def main() -> None:
    """作为 console script 入口，透传参数给 pytest。"""
    import pytest

    args = sys.argv[1:] if len(sys.argv) > 1 else []
    raise SystemExit(pytest.main(args))


if __name__ == "__main__":
    main()
