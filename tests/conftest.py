"""pytest 全局 fixture 与钩子 🧩.

集中管理浏览器上下文、失败截图 Allure 集成等企业级测试基建。
"""

from __future__ import annotations

from collections.abc import Iterator

import allure
import pytest
from config.settings import settings
from playwright.sync_api import Browser, BrowserContext, Page
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def browser_context(browser: Browser) -> Iterator[BrowserContext]:
    """创建并返回浏览器上下文（session 级）。

    统一设置视口，测试结束后自动关闭浏览器上下文。
    """
    context = browser.new_context(
        viewport={
            "width": settings.viewport_width,
            "height": settings.viewport_height,
        },
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context: BrowserContext) -> Iterator[Page]:
    """提供每个用例独立的页面（function 级），并应用全局超时。"""
    logger.info("🌱 为用例创建新页面")
    current_page = browser_context.new_page()
    current_page.set_default_timeout(settings.timeout)
    yield current_page
    current_page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用例失败时，把当前页面截图附加到 Allure 报告。"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        _attach_failure_screenshot(item)


def _attach_failure_screenshot(item) -> None:
    """尝试从 fixture 获取 page 并截图，失败不影响用例结果。"""
    try:
        page: Page | None = item.funcargs.get("page")
        if page is not None:
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name=f"失败截图-{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )
            logger.error("❌ 用例失败，已捕获截图: %s", item.name)
    except Exception:  # noqa: BLE001 - 截图失败不应污染原始用例结果
        logger.warning("⚠️ 失败截图捕获失败: %s", item.name)
