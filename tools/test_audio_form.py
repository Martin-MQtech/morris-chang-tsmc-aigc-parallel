# -*- coding: utf-8 -*-
"""
测试微信视频号【合集】列表与【发表音频】表单结构
"""

import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def test_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print("1. 访问视频号助手主页并点击【内容管理】->【音频】...")
        page.goto("https://channels.weixin.qq.com/platform", wait_until="networkidle")
        time.sleep(2)
        page.locator(".weui-desktop-menu__name:has-text('内容管理'), :text('内容管理')").first.click()
        time.sleep(1)
        page.locator(".weui-desktop-menu-sub__name:has-text('音频'), :text('音频')").first.click()
        time.sleep(3)

        print("2. 切换到【合集】标签页...")
        tab_collection = page.locator(":text('合集')").first
        tab_collection.click()
        time.sleep(3)
        page.screenshot(path=os.path.join(COOKIE_PROFILE_DIR, "step2_collections_tab.png"))

        # 查看合集列表内容
        print("合集列表文本:")
        print(page.locator(".table-wrap, .weui-desktop-table, body").first.inner_text()[:400])

        # 点击合集名称进入详情
        tsmc_col = page.locator(":text('台积电张忠谋')").first
        if tsmc_col.is_visible():
            print("👉 找到【台积电张忠谋】合集，点击进入详情...")
            tsmc_col.click()
            time.sleep(3)
            page.screenshot(path=os.path.join(COOKIE_PROFILE_DIR, "step3_collection_details.png"))
            print("合集详情页 URL:", page.url)

            # 寻找【添加音频】按钮
            add_audio_btn = page.locator("button:has-text('添加音频')").first
            if add_audio_btn.is_visible():
                print("👉 点击【添加音频】按钮...")
                add_audio_btn.click()
                time.sleep(3)
                page.screenshot(path=os.path.join(COOKIE_PROFILE_DIR, "step4_audio_publish_modal.png"))
                print("发表表单 URL:", page.url)

        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    test_form()
