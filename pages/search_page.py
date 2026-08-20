"""百度首页页面对象 🔎.

以百度搜索为例，展示 POM 模式的页面对象写法。
实际项目请按被测系统替换。
"""

from __future__ import annotations

from locators.baidu_locators import SearchPageLocators
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class BaiduSearchPage(BasePage):
    """百度搜索页页面对象。"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.locators = SearchPageLocators(page)

    def search_loader(self) -> Locator:
        return self.locators.search_input

    def search(self, keyword: str) -> None:
        """输入关键词并点击搜索。"""
        self.fill(self.locators.search_input, keyword)
        self.click(self.locators.search_button)

    def searched(self) -> None:
        """等待搜索结果出现。"""
        self.expect_url("https://www.baidu.com/s")
        self.expect_attached(self.locators.result_items.first)
