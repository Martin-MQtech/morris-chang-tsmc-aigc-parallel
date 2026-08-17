# -*- coding: utf-8 -*-
"""
收官总巡检：截取音频列表与合集详情最终全景截图
"""

import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_URL = "https://channels.weixin.qq.com/platform/post/audioCollectionDetails?id=event%2FUzFfAgtgekIEAQAAAAAAwY4QU0vyJgAAAAAStQy6u2-36L1n0r-7fJqX_X8h5xM"

def capture_final_status():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print("1. 截取音频管理列表最终状态...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(5)
        shot1 = os.path.join(COOKIE_PROFILE_DIR, "final_all_audio_list.png")
        page.screenshot(path=shot1)
        print(f"📸 最终音频列表截图: {shot1}")

        print("2. 截取合集列表最终状态...")
        tab_col = page.locator(":text('合集')").first
        if tab_col.is_visible():
            tab_col.click()
            time.sleep(3)
            shot2 = os.path.join(COOKIE_PROFILE_DIR, "final_collection_tab.png")
            page.screenshot(path=shot2)
            print(f"📸 最终合集标签页截图: {shot2}")

        browser.close()

if __name__ == "__main__":
    capture_final_status()
