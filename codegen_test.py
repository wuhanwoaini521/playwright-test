"""使用 Playwright Codegen 生成的百度搜索交互脚本 🔍.

说明: 此脚本由 `playwright codegen` 录制生成，仅作示例参考。
实际建议直接使用 pytest 的形式编写 UI 自动化用例。
"""

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    """执行一次完整的百度搜索 + 知乎跳转流程。"""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.baidu.com/")
    page.locator("#kw").click()
    page.locator("#kw").fill("你好playwright")
    page.get_by_role("button", name="百度一下").click()

    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Hello Playwright:(1)从开发到部署 - 知乎").click()
    page1 = page1_info.value
    page1.get_by_role("button", name="关闭", exact=True).click()
    page1.get_by_role("textbox").locator("div").nth(2).click()
    page1.get_by_role("textbox").fill("你好")
    page1.get_by_role("img", name="发呆").click()
    page1.get_by_role("button", name="发布", exact=True).click()
    page1.get_by_role("button", name="关闭", exact=True).click()

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        run(p)
