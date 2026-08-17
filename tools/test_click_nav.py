# -*- coding: utf-8 -*-
import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def test_click_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print("1. 访问主页...")
        page.goto("https://channels.weixin.qq.com/platform", wait_until="networkidle", timeout=60000)
        time.sleep(3)

        print("2. 点击侧边栏【内容管理】...")
        content_btn = page.locator(".weui-desktop-menu__name:has-text('内容管理'), :text('内容管理')").first
        content_btn.click()
        time.sleep(1)

        print("3. 点击二级菜单【音频】...")
        audio_sub = page.locator(".weui-desktop-menu-sub__name:has-text('音频'), :text('音频')").first
        audio_sub.click()
        time.sleep(5)

        shot1 = os.path.join(COOKIE_PROFILE_DIR, "diag_3_after_click_audio.png")
        page.screenshot(path=shot1)
        print(f"截图留存: {shot1}")
        print("当前页面 URL:", page.url)

        # 检查页面内的所有文本与结构
        body_text = page.locator("body").inner_text()
        print("页面文本节选:\n", body_text[:600])

        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    test_click_navigation()
