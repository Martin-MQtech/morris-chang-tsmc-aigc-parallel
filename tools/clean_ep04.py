# -*- coding: utf-8 -*-
"""
精准删除第 04 期并重置为 00 -> 01 -> 02 -> 03 严格升序
"""

import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def clean_ep04():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(4)

        # 循环删除所有标题包含第04期的条目
        for loop in range(3):
            # 查找所有包含 第04期 的行中的删除按钮
            ep04_btn = page.locator(".weui-desktop-table tr:has-text('第04期') a:has-text('删除'), .weui-desktop-table tr:has-text('第04期') button:has-text('删除')").first
            if ep04_btn.is_visible():
                print(f"👉 正在删除第 04 期条目 (第 {loop+1} 次)...")
                ep04_btn.click()
                time.sleep(1.5)
                # 确认删除弹窗
                confirm_btn = page.locator("button:has-text('确定'), button:has-text('确认')").first
                if confirm_btn.is_visible():
                    confirm_btn.click()
                    print("   ✅ 点击确定删除")
                    time.sleep(3)
            else:
                print("已无更多第04期条目")
                break

        page.reload(wait_until="domcontentloaded")
        time.sleep(4)
        shot = os.path.join(COOKIE_PROFILE_DIR, "verified_00_to_03_clean.png")
        page.screenshot(path=shot)
        print(f"📸 00~03 干净状态截图: {shot}")

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    clean_ep04()
