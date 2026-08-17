# -*- coding: utf-8 -*-
"""
精准删除 21:51 发布的旧版第04期，保留 21:56 的第04期
使时间线呈现绝对完美的 00 -> 01 -> 02 -> 03 -> 04 顺序
"""

import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def delete_older_ep04():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print("1. 访问音频管理页...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(4)

        # 定位 21:51 的那一行第04期
        target_row = page.locator("tr:has-text('21:51'), .table-row:has-text('21:51')").first
        if target_row.is_visible():
            del_btn = target_row.locator("a:has-text('删除'), button:has-text('删除'), :text('删除')").first
            print("👉 找到 21:51 夹在第2集和第3集之间的第4期，正在点击删除...")
            del_btn.click()
            time.sleep(1.5)
            # 点击弹出的二次确认按钮
            confirm_btn = page.locator("button:has-text('确定'), button:has-text('确认')").first
            if confirm_btn.is_visible():
                confirm_btn.click()
                print("✅ 已确认删除 21:51 的旧第4期")
                time.sleep(3)
        else:
            print("未找到 21:51 的行")

        # 刷新并重新截取完美顺序长图
        page.reload(wait_until="domcontentloaded")
        time.sleep(4)
        shot = os.path.join(COOKIE_PROFILE_DIR, "perfect_order_00_to_04.png")
        page.screenshot(path=shot)
        print(f"📸 完美顺序核验证明: {shot}")

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    delete_older_ep04()
