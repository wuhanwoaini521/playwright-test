"""页面对象基类 🏠.

封装 Playwright ``Page`` 的常用操作与断言，供各业务页面继承复用。
子类必须实现 ``search_loader`` 方法，返回用于确定页面已加载的定位符。
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from config.settings import settings
from playwright.sync_api import Locator, Page, expect
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage(ABC):
    """所有页面对象的基类，提供通用操作与显式等待。"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.__apply_timeout()

    def __apply_timeout(self) -> None:
        """对页面应用全局超时配置。"""
        self.page.set_default_timeout(settings.timeout)

    @abstractmethod
    def search_loader(self) -> Locator:
        """返回页面加载完成的标志元素定位符。子类必须实现。

        用于 `wait_for_ready` 辅助判断页面是否就绪。
        """

    def open(self, url: str | None = None) -> BasePage:
        """打开页面（默认打开配置中的 base_url），并等待页面加载。"""
        target = url or settings.base_url
        logger.info("🌐 打开页面: %s", target)
        self.page.goto(target, wait_until="domcontentloaded")
        self.wait_for_ready()
        return self

    def wait_for_ready(self, timeout: int | None = None) -> None:
        """等待页面主要资源加载完成。

        优先等待网络空闲；若始终不空闲（如页面长期轮询），则降级为
        DOM 加载完成即可，避免把动态加载动画误判为失败。
        """
        timeout = timeout or settings.timeout
        try:
            self.page.wait_for_load_state(state="networkidle", timeout=timeout)
        except Exception:  # noqa: BLE001 - 网络不空闲属常见情形，降级处理
            self.page.wait_for_load_state(state="domcontentloaded", timeout=timeout)

    def fill(self, locator: Locator, text: str) -> None:
        """等待元素可编辑后清空并输入文本。"""
        logger.info("⌨️ 输入文本: %s", text)
        # 显式等待元素可交互，规避页面加载动画期间输入失败
        locator.wait_for(state="attached", timeout=settings.timeout)
        expect(locator).to_be_editable(timeout=settings.timeout)
        locator.fill(text)

    def click(self, locator: Locator) -> None:
        """点击元素并等待其可交互。"""
        logger.info("🖱️ 点击元素")
        locator.click()

    def expect_text(self, locator: Locator, text: str) -> None:
        """断言元素包含预期文本。"""
        logger.info("✅ 断言元素包含文本: %s", text)
        expect(locator).to_contain_text(text, timeout=settings.timeout)

    def expect_attached(self, locator: Locator) -> None:
        """断言元素已挂载到 DOM（适用于加载动画期间可见性不稳定的场景）。"""
        logger.info("✅ 断言元素已挂载")
        expect(locator).to_be_attached(timeout=settings.timeout)

    def expect_url(self, url: str, *, exact: bool = True) -> None:
        """断言当前页面 URL。"""
        logger.info("✅ 断言当前 URL: %s", url)
        if exact:
            expect(self.page).to_have_url(url, timeout=settings.timeout)
        else:
            expect(self.page).to_have_url(url, timeout=settings.timeout)
