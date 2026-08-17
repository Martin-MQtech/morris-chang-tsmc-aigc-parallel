# -*- coding: utf-8 -*-
"""
诊断微信视频号助手音频发布页面的真实 DOM 结构与 UI 元素 (使用本地 Google Chrome)
"""

import os, sys, time, json
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def diagnose_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print("1. 访问视频号助手主页...")
        page.goto("https://channels.weixin.qq.com/platform", timeout=60000)
        time.sleep(3)
        page.screenshot(path=os.path.join(COOKIE_PROFILE_DIR, "diag_1_home.png"))

        print("2. 导航到音频管理列表...")
        page.goto("https://channels.weixin.qq.com/platform/post/audio", timeout=60000)
        time.sleep(4)
        page.screenshot(path=os.path.join(COOKIE_PROFILE_DIR, "diag_2_audio.png"))
        print("当前 URL:", page.url)

        # 查找所有按钮与链接
        buttons = page.locator("button, a").all_inner_texts()
        valid_buttons = [b.strip().replace("\n", " ") for b in buttons if b.strip()]
        print("当前页面可见主要按钮/链接:", valid_buttons[:25])

        # 查找包含「台积电」或「平行世界」的合集
        collection_card = page.locator(":has-text('台积电张忠谋')")
        print(f"包含台积电的元素数: {collection_card.count()}")
        
        # 寻找添加音频按钮
        add_btns = page.locator("button:has-text('添加音频'), button:has-text('发表音频'), button:has-text('新建音频')")
        print(f"找到添加音频按钮数: {add_btns.count()}")

        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    diagnose_ui()
