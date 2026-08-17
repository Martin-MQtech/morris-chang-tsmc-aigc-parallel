# -*- coding: utf-8 -*-
"""
使用 expect_file_chooser 与原生点击进行精准音频发表测试
"""

import os, sys, time
from playwright.sync_api import sync_playwright
from audio_posts_data import EPISODES_DATA

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def test_publish_ep00_fc():
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

        # 2. 通过 file_chooser 上传音频
        print("2. 触发音频文件选择器上传 MP3...")
        try:
            with page.expect_file_chooser(timeout=5000) as fc_info:
                page.locator(":text('拖拽到此处上传')").first.click()
            fc = fc_info.value
            fc.set_files(ep00["audio_path"])
            print("   ✅ 音频文件选择器设置成功")
        except Exception as e:
            print("   ⚠️ file_chooser 备用回退为 input set_input_files:", e)
            page.locator("input[type='file']").first.set_input_files(ep00["audio_path"])

        # 等待上传转码完成
        print("   ⏳ 等待音频上传...")
        for i in range(20):
            time.sleep(1.5)
            group_txt = page.locator(".weui-desktop-form__control-group:has-text('文件')").first.inner_text()
            print(f"   [t={i*1.5:.1f}s] {group_txt.replace('\n', ' ')}")
            if "0%" not in group_txt and "请上传音频" not in group_txt and ("MB" in group_txt or "KB" in group_txt):
                print("   🎉 音频上传解析完成！")
                break

        # 3. 通过 file_chooser 上传封面
        print("3. 上传封面插图...")
        try:
            # 找到封面框的点击区域
            cover_box = page.locator(".weui-desktop-form__control-group:has-text('封面')").locator(".weui-desktop-icon-plus, svg, .upload-btn, div").first
            with page.expect_file_chooser(timeout=5000) as fc_info:
                cover_box.click()
            fc = fc_info.value
            fc.set_files(ep00["cover_path"])
        except Exception as e:
            print("   ⚠️ 封面 file_chooser 备用回退:", e)
            page.locator("input[type='file']").nth(1).set_input_files(ep00["cover_path"])

        time.sleep(2)
        crop_btn = page.locator("button:has-text('确认')").first
        if crop_btn.is_visible():
            print("   👉 确认封面裁切...")
            crop_btn.click()
            time.sleep(2)

        # 4. 填写标题与描述
        print("4. 填入标题与描述...")
        page.locator("input[placeholder='请填写标题']").first.fill(ep00["title"][:40])
        page.locator("textarea[placeholder='请填写描述']").first.fill(ep00["desc"])
        time.sleep(1)

        # 5. 选择合集
        print("5. 绑定合集...")
        page.locator(":text('选择合集')").first.click()
        time.sleep(1.5)
        # 点击下拉列表中的合集项
        page.locator(".weui-desktop-dropdown__list-item, li:has-text('台积电'), .weui-desktop-popover__content li").first.click()
        time.sleep(2)

        # 截图就绪状态
        ready_shot = os.path.join(COOKIE_PROFILE_DIR, "fc_ready_ep00.png")
        page.screenshot(path=ready_shot)
        print(f"📸 发布就绪截图: {ready_shot}")

        # 6. 点击发表音频
        print("6. 点击【发表音频】按钮...")
        pub_btn = page.locator("button:has-text('发表音频')").first
        pub_btn.click()
        time.sleep(8)

        # 截图结果
        pub_shot = os.path.join(COOKIE_PROFILE_DIR, "fc_pub_result.png")
        page.screenshot(path=pub_shot)
        print(f"📸 发表后截图: {pub_shot}")
        print("最终页面 URL:", page.url)

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    test_publish_ep00_fc()
