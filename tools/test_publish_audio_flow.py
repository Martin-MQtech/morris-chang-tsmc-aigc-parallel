# -*- coding: utf-8 -*-
"""
测试视频号【发表音频】真实发布表单与合集绑定流
"""

import os, sys, time
from playwright.sync_api import sync_playwright
from audio_posts_data import EPISODES_DATA

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def test_publish_audio_ep00():
    ep00 = EPISODES_DATA[0]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print("1. 访问视频号助手主页...")
        page.goto("https://channels.weixin.qq.com/platform", wait_until="domcontentloaded")
        time.sleep(3)

        print("2. 点击【内容管理】->【音频】...")
        page.locator(".weui-desktop-menu__name:has-text('内容管理'), :text('内容管理')").first.click()
        time.sleep(1)
        page.locator(".weui-desktop-menu-sub__name:has-text('音频'), :text('音频')").first.click()
        time.sleep(3)

        print("3. 点击右上角橙色【发表音频】按钮...")
        pub_audio_btn = page.locator("button:has-text('发表音频')").first
        pub_audio_btn.click()
        time.sleep(4)

        shot1 = os.path.join(COOKIE_PROFILE_DIR, "step_publish_form.png")
        page.screenshot(path=shot1)
        print(f"发表表单截图已留存: {shot1}")
        print("发表页面 URL:", page.url)

        # 检查表单中的所有 input 与 textarea
        file_inputs = page.locator("input[type='file']").all()
        print(f"找到 file input 数量: {len(file_inputs)}")
        for idx, fi in enumerate(file_inputs):
            print(f"  file[{idx}] accept={fi.get_attribute('accept')}")

        text_inputs = page.locator("input[type='text'], input:not([type='file']), textarea").all()
        print(f"找到文本输入框数量: {len(text_inputs)}")
        for idx, ti in enumerate(text_inputs):
            print(f"  text[{idx}] placeholder={ti.get_attribute('placeholder')} class={ti.get_attribute('class')}")

        # 检查是否有合集下拉框或选择项
        collection_select = page.locator(":has-text('合集'), :has-text('添加到合集')").all_inner_texts()
        print("合集相关区域文本:", collection_select[:5])

        # 注入第 00 期音频
        if len(file_inputs) > 0:
            print(f"⏳ 注入第 00 期音频: {ep00['audio_path']}")
            file_inputs[0].set_input_files(ep00["audio_path"])
            time.sleep(6)
            page.screenshot(path=os.path.join(COOKIE_PROFILE_DIR, "step_audio_injected.png"))

        # 如果有封面选择框
        if len(file_inputs) > 1:
            print(f"⏳ 注入封面: {ep00['cover_path']}")
            file_inputs[1].set_input_files(ep00["cover_path"])
            time.sleep(3)

        # 填标题
        title_in = page.locator("input[placeholder*='标题'], input[maxlength='25'], input[maxlength='30']").first
        if title_in.is_visible():
            title_in.fill(ep00["title"][:25])
            print("✅ 标题已填入:", ep00["title"][:25])

        # 填正文
        editor = page.locator("div[contenteditable='true'], textarea").first
        if editor.is_visible():
            editor.click()
            editor.fill(ep00["desc"])
            print("✅ 正文描述已填入")

        time.sleep(3)
        final_shot = os.path.join(COOKIE_PROFILE_DIR, "step_form_filled.png")
        page.screenshot(path=final_shot)
        print(f"最终表单填写完成截图: {final_shot}")

        # 查看发表/保存按钮
        submit_btn = page.locator("button:has-text('发表'), button:has-text('发布')")
        print(f"发表按钮数量: {submit_btn.count()}")

        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    test_publish_audio_ep00()
