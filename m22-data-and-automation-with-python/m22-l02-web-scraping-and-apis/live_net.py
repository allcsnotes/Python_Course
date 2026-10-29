from playwright.sync_api import sync_playwright


def show(r):
    print(r.status, r.request.resource_type, r.url)


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("response", show)
    page.goto("http://localhost:22280/live")
    page.wait_for_selector("li.session")
    browser.close()
