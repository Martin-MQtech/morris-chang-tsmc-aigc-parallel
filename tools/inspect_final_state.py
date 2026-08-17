# -*- coding: utf-8 -*-
"""
全面检查英文合集和音频列表状态
"""
import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_TITLE = "TSMC & Morris Chang: Parallel World"

def inspect():
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

        # 1. 检查合集管理
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)

        print("=== 现存合集列表 ===")
        for idx, r in enumerate(page.locator("tbody tr").all()):
            print(f"[{idx}] {r.inner_text().replace(chr(10), ' | ')}")

        col_row = page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first
        col_row.locator("a:has-text('详情')").first.click()
        time.sleep(4)

        print("\n=== 《TSMC & Morris Chang: Parallel World》合集内容 PAGE 1 ===")
        for idx, r in enumerate(page.locator("tbody tr").all()):
            print(f"[{idx}] {r.inner_text().replace(chr(10), ' | ')}")

        nb = page.locator("a:has-text('下一页')").first
        if nb.is_visible():
            nb.click()
            time.sleep(2)
            print("\n=== 《TSMC & Morris Chang: Parallel World》合集内容 PAGE 2 ===")
            for idx, r in enumerate(page.locator("tbody tr").all()):
                print(f"[{idx}] {r.inner_text().replace(chr(10), ' | ')}")

        shot = os.path.join(COOKIE_PROFILE_DIR, "live_collection_audit.png")
        page.screenshot(path=shot, full_page=True)
        print(f"\n📸 实时截图已保存: {shot}")

        browser.close()

if __name__ == "__main__":
    inspect()
