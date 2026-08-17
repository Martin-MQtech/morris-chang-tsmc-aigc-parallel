# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def inspect_collection_tab():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=[
                "--no-sandbox", "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars", "--no-first-run",
                "--no-default-browser-check",
            ]
        )
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            storage_state=STATE_JSON_FILE,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            locale="zh-CN",
        )
        page = ctx.new_page()

        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)

        shot = os.path.join(COOKIE_PROFILE_DIR, "collection_tab_debug.png")
        page.screenshot(path=shot, full_page=True)
        print("Screenshot saved to:", shot)

        print("\nAll visible buttons:")
        for b in page.locator("button, a").all():
            if b.is_visible() and b.inner_text().strip():
                print(f"[{b.inner_text().strip()}] -> tag: {b.evaluate('el => el.tagName')}, class: {b.get_attribute('class')}")

        browser.close()

if __name__ == "__main__":
    inspect_collection_tab()
