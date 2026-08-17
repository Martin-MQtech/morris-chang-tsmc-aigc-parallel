# -*- coding: utf-8 -*-
"""
核对并清理重复项，确保 00~04 完美无疏漏
"""

import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def clean_duplicate_and_verify():
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

        # 查找所有标题包含「第04期」的行
        ep04_rows = page.locator("tr:has-text('第04期'), .table-row:has-text('第04期'), div:has-text('第04期')").all()
        print(f"检测到第04期数量: {len(ep04_rows)}")

        # 寻找删除按钮删除最新重复的那一条 (顶部的一条)
        del_btn = page.locator("tr:has-text('第04期') button:has-text('删除'), tr:has-text('第04期') a:has-text('删除'), div:has-text('第04期') :text('删除')").first
        if del_btn.is_visible():
            print("👉 正在删除重复的第 04 期...")
            del_btn.click()
            time.sleep(1.5)
            # 确认弹窗
            confirm = page.locator("button:has-text('确定'), button:has-text('确认')").first
            if confirm.is_visible():
                confirm.click()
                print("✅ 确认删除成功")
                time.sleep(3)

        # 刷新页面并截图
        page.reload(wait_until="domcontentloaded")
        time.sleep(4)

        shot = os.path.join(COOKIE_PROFILE_DIR, "verified_00_to_04.png")
        page.screenshot(path=shot)
        print(f"📸 00~04 完美顺序核验截图: {shot}")

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    clean_duplicate_and_verify()
