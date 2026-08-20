"""百度搜索 POM 测试用例 🔎.

演示基于 Page Object 模式的用例写法。

说明：
- ``test_open_homepage`` 为核心冒烟用例，CI 默认稳定运行。
- ``test_search_keyword`` 依赖百度外网真实可交互性，在无头/受限网络下
  可能因被测站点动态行为失败，故标记为 ``slow`` 默认跳过；
  本地联网可运行： ``PW_RUN_SLOW=1 uv run pytest -m slow``
"""

from __future__ import annotations

import os

import allure
import pytest
from pages.search_page import BaiduSearchPage
from playwright.sync_api import Page

# 仅当显式开启时才运行 slow 用例
_RUN_SLOW = os.getenv("PW_RUN_SLOW", "0") in ("1", "true", "yes", "on")
skipif_slow = pytest.mark.skipif(not _RUN_SLOW, reason="慢速用例需设置 PW_RUN_SLOW=1 才运行")


@allure.suite("百度搜索")
class TestBaiduSearch:
    """百度首页打开与搜索验证。"""

    @pytest.mark.smoke
    @allure.feature("页面加载")
    @allure.story("打开首页")
    def test_open_homepage(self, page: Page) -> None:
        """打开百度首页并确认 URL 与关键元素挂载。"""
        with allure.step("打开百度首页"):
            home = BaiduSearchPage(page).open()
        with allure.step("断言 URL 正确"):
            home.expect_url("https://www.baidu.com/")
        with allure.step("断言搜索框已挂载"):
            # 使用 attached 而非 visible，规避页面加载动画期间元素可见性抖动
            home.expect_attached(home.locators.search_input)

    @pytest.mark.slow
    @skipif_slow
    @allure.feature("搜索")
    @allure.story("关键词搜索")
    def test_search_keyword(self, page: Page) -> None:
        """执行关键词搜索并确认进入结果页（需联网）。"""
        home = BaiduSearchPage(page).open()
        with allure.step("输入关键词并点击搜索"):
            home.search("Playwright 测试")
        with allure.step("断言进入搜索结果页"):
            page.wait_for_url("**/s?*", timeout=15000)
            home.expect_url("https://www.baidu.com/s", exact=False)
            home.expect_attached(home.locators.result_items.first)
