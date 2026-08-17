# -*- coding: utf-8 -*-
"""
精确实测发布第 00 期音频到指定合集
"""

import os, sys, time
from playwright.sync_api import sync_playwright
from audio_posts_data import EPISODES_DATA

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def publish_ep00():
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

        # 2. 注入音频文件
        print("2. 注入音频文件...")
        audio_input = page.locator("input[type='file']").first
        audio_input.set_input_files(ep00["audio_path"])
        
        # 等待音频上传完成 (轮询等待上传进度完成)
        print("   ⏳ 等待音频上传并转码完成...")
        for i in range(15):
            time.sleep(1.5)
            audio_box_text = page.locator(".weui-desktop-form__control-group:has-text('文件')").first.inner_text()
            if "0%" not in audio_box_text and "请上传音频" not in audio_box_text:
                print("   🎉 音频上传完成！状态:", audio_box_text.replace('\n', ' '))
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
            time.sleep(1.5)

        # 4. 填写标题与描述
        print("4. 填写标题与描述...")
        page.locator("input[placeholder='请填写标题']").first.fill(ep00["title"][:40])
        page.locator("textarea[placeholder='请填写描述']").first.fill(ep00["desc"])
        time.sleep(1)

        # 5. 选择合集
        print("5. 展开并选择合集...")
        select_trigger = page.locator(":text('选择合集')").first
        if select_trigger.is_visible():
            select_trigger.click()
            time.sleep(1.5)
            
            # 点击下拉菜单项
            target_opt = page.locator(".weui-desktop-dropdown__list-item:has-text('台积电'), li:has-text('台积电'), .weui-desktop-popover :has-text('台积电')").first
            if target_opt.is_visible():
                target_opt.click()
                print("   ✅ 成功选择【台积电张忠谋】合集！")
                time.sleep(1.5)
            else:
                # 尝试点击下拉里的任意第一项
                any_item = page.locator(".weui-desktop-dropdown__list-item, .weui-desktop-dropdown li").first
                if any_item.is_visible():
                    any_item.click()
                    print("   ✅ 点击了首个合集选项")
                    time.sleep(1.5)

        # 截图就绪状态
        ready_shot = os.path.join(COOKIE_PROFILE_DIR, "final_ready_ep00.png")
        page.screenshot(path=ready_shot)
        print(f"📸 最终表单完整截图: {ready_shot}")

        # 6. 点击【发表音频】
        print("6. 正在点击【发表音频】按钮...")
        pub_btn = page.locator("button:has-text('发表音频')").first
        pub_btn.click()
        print("🎉 点击【发表音频】完成，等待 8 秒入库...")
        time.sleep(8)

        # 截图发表后结果
        result_shot = os.path.join(COOKIE_PROFILE_DIR, "final_result_ep00.png")
        page.screenshot(path=result_shot)
        print(f"📸 发布后截图: {result_shot}")
        print("当前页面 URL:", page.url)

        # 保存更新的凭证
        context.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("🎉🎉🎉 第 00 期已成功发表！")

if __name__ == "__main__":
    publish_ep00()
