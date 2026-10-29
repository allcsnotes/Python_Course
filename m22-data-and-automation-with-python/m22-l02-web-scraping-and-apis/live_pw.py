import time

from playwright.sync_api import sync_playwright

start = time.perf_counter()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:22280/live")
    page.wait_for_selector("li.session")
    for text in page.locator("li.session").all_text_contents():
        print(text)
    browser.close()
print(f"{time.perf_counter() - start:.2f} s")
