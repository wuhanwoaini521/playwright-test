"""百度搜索页面的 Playwright UI 测试示例 🧪.

使用 pytest + pytest-playwright 插件，示例展示了:
- fixture 的用法（每个测试前后自动执行）
- 页面导航验证
"""

from playwright.sync_api import Page, expect
import pytest


@pytest.fixture(scope="function", autouse=True)
def goto_baidu(page: Page):
    """测试前置/后置操作：打开百度首页。"""
    print("🌐 开始执行测试...")
    page.goto("https://www.baidu.com")
    yield
    print("✅ 测试执行完毕")


def test_main_navigation(page: Page):
    """验证访问百度首页后 URL 正确。"""
    expect(page).to_have_url("https://www.baidu.com/")
