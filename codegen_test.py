from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
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

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
