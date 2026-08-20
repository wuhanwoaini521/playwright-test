"""百度搜索页元素定位 🔍.

所有定位符集中在定位层，页面对象（pages）只负责操作与断言。
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page


class SearchPageLocators:
    """百度首页的 UI 元素定位集合。"""

    def __init__(self, page: Page) -> None:
        self._page = page

    @property
    def search_input(self) -> Locator:
        return self._page.locator("#kw")  # 搜索输入框

    @property
    def search_button(self) -> Locator:
        return self._page.get_by_role("button", name="百度一下")  # 搜索按钮

    @property
    def result_items(self) -> Locator:
        return self._page.locator("[id^='content_left'] h3")  # 搜索结果标题
