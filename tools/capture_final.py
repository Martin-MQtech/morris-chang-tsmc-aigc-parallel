# -*- coding: utf-8 -*-
"""
一键快捷登录并截取最终收官全景
"""

import os, sys, time, json
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def capture_fast_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        page.goto("https://channels.weixin.qq.com/platform", wait_until="domcontentloaded")
        time.sleep(3)

        # 如果出现「微信快捷登录」按钮，点击快捷登录
        fast_btn = page.locator("button:has-text('微信快捷登录'), :text('微信快捷登录')").first
        if fast_btn.is_visible():
            print("👉 点击【微信快捷登录】...")
            fast_btn.click()
            time.sleep(5)

        print("1. 导航至【音频管理】...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(5)
        shot1 = os.path.join(COOKIE_PROFILE_DIR, "final_complete_audio_list.png")
        page.screenshot(path=shot1)
        print(f"📸 最终音频列表截图: {shot1}")

        print("2. 切换至【合集】标签页...")
        tab_col = page.locator(":text('合集')").first
        if tab_col.is_visible():
            tab_col.click()
            time.sleep(4)
            shot2 = os.path.join(COOKIE_PROFILE_DIR, "final_complete_collection_list.png")
            page.screenshot(path=shot2)
            print(f"📸 最终合集列表截图: {shot2}")

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    capture_fast_login()
