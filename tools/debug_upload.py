# -*- coding: utf-8 -*-
"""
精确调试音频上传完成状态与合集下拉选项选择
"""

import os, sys, time
from playwright.sync_api import sync_playwright
from audio_posts_data import EPISODES_DATA

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def debug_upload_and_collection():
    ep00 = EPISODES_DATA[0]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print("1. 访问发布页: https://channels.weixin.qq.com/platform/post/createAudio")
        page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded")
        time.sleep(3)

        # 2. 上传音频
        print("2. 注入音频文件...")
        audio_input = page.locator("input[type='file']").first
        audio_input.set_input_files(ep00["audio_path"])
        
        # 等待音频上传完成 (轮询等待上传进度完成)
        print("   ⏳ 等待音频上传并转码完成...")
        for i in range(20):
            time.sleep(2)
            # 检查是否有删除按钮或播放图标或进度文本
            audio_box_text = page.locator(".weui-desktop-form__control-group:has-text('文件')").first.inner_text()
            print(f"   [t={i*2}s] 音频区域状态: {audio_box_text.replace('\n', ' ')}")
            if "请上传音频" not in audio_box_text and "0%" not in audio_box_text:
                print("   🎉 音频上传完全就绪！")
                break

        # 3. 注入封面
        print("3. 注入封面...")
        cover_input = page.locator("input[type='file']").nth(1)
        cover_input.set_input_files(ep00["cover_path"])
        time.sleep(2)
        crop_btn = page.locator("button:has-text('确认')").first
        if crop_btn.is_visible():
            print("   点击封面裁切确认...")
            crop_btn.click()
            time.sleep(2)

        # 4. 填写标题与描述
        page.locator("input[placeholder='请填写标题']").first.fill(ep00["title"][:40])
        page.locator("textarea[placeholder='请填写描述']").first.fill(ep00["desc"])
        time.sleep(1)

        # 5. 展开并选择合集
        print("5. 展开合集下拉菜单...")
        # 寻找合集区域的点击触发器
        col_group = page.locator(".weui-desktop-form__control-group:has-text('合集')")
        col_select = col_group.locator(".weui-desktop-select, input, .weui-desktop-dropdown").first
        col_select.click()
        time.sleep(2)
        page.screenshot(path=os.path.join(COOKIE_PROFILE_DIR, "debug_col_open.png"))

        # 列出所有可见的下拉选项
        dropdown_items = page.locator(".weui-desktop-dropdown__list-item, .weui-desktop-dropdown-list__item, li.weui-desktop-dropdown__list-item, .weui-desktop-popover__content li").all()
        print(f"找到合集下拉项共 {len(dropdown_items)} 个:")
        for idx, item in enumerate(dropdown_items):
            print(f"  [{idx}] text={item.inner_text().strip()}")
            if "台积电" in item.inner_text() or "AIGC" in item.inner_text():
                print(f"  👉 命中目标合集，正在点击 [{idx}]...")
                item.click()
                time.sleep(2)
                break

        final_debug = os.path.join(COOKIE_PROFILE_DIR, "debug_form_final.png")
        page.screenshot(path=final_debug)
        print(f"最终状态截图: {final_debug}")

        # 6. 点击发表音频
        print("6. 点击【发表音频】...")
        pub_btn = page.locator("button:has-text('发表音频')").first
        pub_btn.click()
        time.sleep(6)

        after_pub = os.path.join(COOKIE_PROFILE_DIR, "debug_after_pub.png")
        page.screenshot(path=after_pub)
        print(f"发布后页面截图: {after_pub}")
        print("发布后 URL:", page.url)

        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    debug_upload_and_collection()
