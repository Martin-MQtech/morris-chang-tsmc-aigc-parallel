# -*- coding: utf-8 -*-
"""
深入监控网络与组件事件，确保音频上传进度 100% 并成功选择合集发表
"""

import os, sys, time
from playwright.sync_api import sync_playwright
from audio_posts_data import EPISODES_DATA

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def monitor_and_publish():
    ep00 = EPISODES_DATA[0]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        # 监听网络请求和响应
        def on_response(response):
            if "upload" in response.url or "cos" in response.url or "audio" in response.url:
                print(f"📡 Response [{response.status}] {response.url[:80]}")
        page.on("response", on_response)

        # 监听控制台错误
        page.on("console", lambda msg: print(f"🖥️ Console [{msg.type}]: {msg.text}") if msg.type in ["error", "warning"] else None)

        print("1. 访问发布页: https://channels.weixin.qq.com/platform/post/createAudio")
        page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded")
        time.sleep(3)

        # 2. 上传音频
        print("2. 设置音频文件 input...")
        audio_input = page.locator("input[type='file']").first
        audio_input.set_input_files(ep00["audio_path"])
        
        # 触发 change 与 input 事件
        audio_input.dispatch_event("change")
        audio_input.dispatch_event("input")

        # 轮询等待上传完成
        print("   ⏳ 监控上传进度...")
        for sec in range(20):
            time.sleep(1)
            # 检查是否有进度条、已上传完成状态
            txt = page.locator(".weui-desktop-form__control-group:has-text('文件')").first.inner_text()
            if sec % 3 == 0:
                print(f"   [{sec}s] 文件区文本: {txt.replace('\n', ' ')}")
            if "0%" not in txt and ("MB" in txt or "KB" in txt):
                print(f"   🎉 [{sec}s] 进度完成，进入就绪态: {txt.replace('\n', ' ')}")
                break

        # 3. 封面上传
        print("3. 设置封面 input...")
        cover_input = page.locator("input[type='file']").nth(1)
        cover_input.set_input_files(ep00["cover_path"])
        cover_input.dispatch_event("change")
        time.sleep(2)
        
        # 点击封面裁切确认
        crop_btn = page.locator("button:has-text('确认'), .weui-desktop-dialog__wrp button:has-text('确认')").first
        if crop_btn.is_visible():
            print("   👉 点击封面裁切【确认】...")
            crop_btn.click()
            time.sleep(2)

        # 4. 标题与描述
        print("4. 填入标题与正文描述...")
        page.locator("input[placeholder='请填写标题']").first.fill(ep00["title"][:40])
        page.locator("textarea[placeholder='请填写描述']").first.fill(ep00["desc"])
        time.sleep(1)

        # 5. 选择合集
        print("5. 选择合集下拉项...")
        col_selector = page.locator(":text('选择合集')").first
        col_selector.click()
        time.sleep(1.5)

        # 点击包含「台积电」的下拉列表选项
        col_opt = page.locator(".weui-desktop-dropdown__list-item:has-text('台积电'), li:has-text('台积电'), :text('AIGC创作：台积电')").first
        if col_opt.is_visible():
            col_opt.click()
            print("   ✅ 点击了【AIGC创作：台积电...】合集选项！")
            time.sleep(2)

        # 截图最终就绪状态
        full_ready_shot = os.path.join(COOKIE_PROFILE_DIR, "full_ready_ep00.png")
        page.screenshot(path=full_ready_shot)
        print(f"📸 最终就绪截图: {full_ready_shot}")

        # 6. 点击发表音频
        print("6. 点击【发表音频】按钮...")
        pub_btn = page.locator("button:has-text('发表音频')").first
        pub_btn.click()
        print("   👉 已点击发表，等待 8 秒...")
        time.sleep(8)

        full_pub_shot = os.path.join(COOKIE_PROFILE_DIR, "full_pub_ep00.png")
        page.screenshot(path=full_pub_shot)
        print(f"📸 发布后截图: {full_pub_shot}")
        print("最终页面 URL:", page.url)

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    monitor_and_publish()
