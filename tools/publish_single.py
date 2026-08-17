# -*- coding: utf-8 -*-
"""
微信视频号【音频合集】单集精准发布工具
"""

import os, sys, time
from playwright.sync_api import sync_playwright
from audio_posts_data import EPISODES_DATA

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def publish_episode_clean(ep_index=0):
    ep = EPISODES_DATA[ep_index]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print(f"1. 访问发布页: [第{ep['ep_id']}期] {ep['title']}")
        page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded")
        time.sleep(3)

        # 2. 上传音频
        print("2. 注入音频文件...")
        audio_in = page.locator("input[type='file']").first
        audio_in.set_input_files(ep["audio_path"])
        print("   ⏳ 等待音频上传解析 (8秒)...")
        time.sleep(8)

        # 3. 上传封面
        print("3. 注入封面插图...")
        cover_in = page.locator("input[type='file']").nth(1)
        cover_in.set_input_files(ep["cover_path"])
        time.sleep(2)
        
        # 确认封面裁切
        confirm_btn = page.locator("button:has-text('确认')").first
        if confirm_btn.is_visible():
            print("   👉 确认封面裁切...")
            confirm_btn.click()
            time.sleep(2)

        # 4. 填写标题与描述
        print("4. 填写标题与正文描述...")
        page.locator("input[placeholder='请填写标题']").first.fill(ep["title"][:40])
        page.locator("textarea[placeholder='请填写描述']").first.fill(ep["desc"])
        time.sleep(1)

        # 5. 选择合集
        print("5. 绑定合集...")
        try:
            page.locator(":text('选择合集')").first.click()
            time.sleep(1.5)
            # 点击下拉列表中的合集选项
            page.get_by_text("AIGC创作：台积电").first.click()
            print("   ✅ 成功选择【AIGC创作：台积电...】合集！")
            time.sleep(1.5)
        except Exception as e:
            print("   ⚠️ 合集选择提示:", e)

        # 拍照留存发布就绪截图
        ready_shot = os.path.join(COOKIE_PROFILE_DIR, f"clean_ready_ep_{ep['ep_id']}.png")
        page.screenshot(path=ready_shot)
        print(f"📸 表单就绪截图: {ready_shot}")

        # 6. 点击发表音频
        print("6. 点击【发表音频】按钮...")
        pub_btn = page.locator("button:has-text('发表音频')").first
        pub_btn.click()
        print("   🎉 已点击发表，等待 10 秒入库...")
        time.sleep(10)

        # 拍照留存发布后截图
        after_shot = os.path.join(COOKIE_PROFILE_DIR, f"clean_after_ep_{ep['ep_id']}.png")
        page.screenshot(path=after_shot)
        print(f"📸 发布后截图: {after_shot}")
        print("当前页面 URL:", page.url)

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print(f"🎉🎉🎉 第 {ep['ep_id']} 期已处理完成！")

if __name__ == "__main__":
    publish_episode_clean(0)
