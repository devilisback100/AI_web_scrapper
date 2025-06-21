import random
import time
from playwright.sync_api import sync_playwright


def scrape_chapter(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        page.goto(url, timeout=60000)
        title = page.title()
        if "Wikimedia Error" in title or "Error" in title:
            print(f"Error page detected for URL: {url}\nPage title: {title}")
            print("Page content preview:")
            print(page.content()[:1000])
            browser.close()
            raise RuntimeError(
                "Aborting scrape: Wikimedia Error page detected.")
        try:
            page.wait_for_selector('#mw-content-text', timeout=60000)
            time.sleep(random.uniform(2, 5))
        except Exception as e:
            print(
                f"Error: Selector content not found or page load timeout for URL: {url}")
            print(f"Exception: {e}")
            print("Page content preview:")
            print(page.content()[:1000])
            browser.close()
            raise
        content = page.query_selector('#mw-content-text')
        chapter_text = content.inner_text() if content else ''
        browser.close()
        return chapter_text
