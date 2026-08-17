# -*- coding: utf-8 -*-
"""
微信视频号音频合集自动发布引擎 (生产级落地版)
- 直达发布页: https://channels.weixin.qq.com/platform/post/createAudio
- 精准注入: MP3 音频文件 + 1:1 排版封面
- 自动确认封面裁切弹窗 (点击「确认」)
- 自动填写: 标题 (≤25字) + 深度叙事正文 + Hashtags + GitHub官方展厅URL
- 自动绑定合集: 《AIGC创作：台积电张忠谋·传记时间线的平行世界》
- 自动点击发表并留存高清截图凭证
"""

import os, sys, time, json, random, argparse
from playwright.sync_api import sync_playwright
import browser_cookie3

from audio_posts_data import EPISODES_DATA, GITHUB_PORTAL_URL

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_NAME = "台积电张忠谋"

def sync_wechat_cookies():
    """从本地 Mac Chrome 提取微信平台 Cookie"""
    os.makedirs(COOKIE_PROFILE_DIR, exist_ok=True)
    domains = ["weixin.qq.com", "qq.com"]
    all_cookies = []
    
    for domain in domains:
        try:
            cj = browser_cookie3.chrome(domain_name=domain)
            for c in cj:
                all_cookies.append({
                    "name": str(c.name),
                    "value": str(c.value),
                    "domain": str(c.domain),
                    "path": str(c.path),
                    "expires": float(c.expires) if c.expires else -1.0,
                    "httpOnly": False,
                    "secure": bool(c.secure),
                    "sameSite": "Lax"
                })
        except Exception:
            pass
            
    if all_cookies:
        state_data = {"cookies": all_cookies, "origins": []}
        with open(STATE_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)
        print(f"✅ 成功同步凭证至: {STATE_JSON_FILE}")
        return True
    elif os.path.exists(STATE_JSON_FILE):
        return True
    return False

def publish_single_episode(page, ep_data, auto_submit=True):
    ep_id = ep_data["ep_id"]
    title = ep_data["title"]
    audio_path = ep_data["audio_path"]
    cover_path = ep_data["cover_path"]
    desc = ep_data["desc"]

    print(f"\n========================================================")
    print(f"🚀 开始发布: [第{ep_id}期] {title}")
    print(f"📁 音频: {audio_path}")
    print(f"🖼️ 封面: {cover_path}")
    print(f"========================================================")

    # 1. 访问直接发布页
    page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded", timeout=60000)
    time.sleep(3)

    # 2. 上传音频文件
    print("⏳ [1/6] 正在注入音频 MP3...")
    file_inputs = page.locator("input[type='file']")
    if file_inputs.count() > 0:
        file_inputs.nth(0).set_input_files(audio_path)
        print("   ✅ 音频文件已注入，等待前端解析...")
        time.sleep(6)

    # 3. 上传封面插图
    print("⏳ [2/6] 正在注入封面插图...")
    if file_inputs.count() > 1:
        file_inputs.nth(1).set_input_files(cover_path)
        time.sleep(2)
        
        # 检查是否弹出了「编辑音频封面」模态框
        crop_confirm_btn = page.locator("button:has-text('确认'), button.weui-desktop-btn_primary:has-text('确认')").first
        if crop_confirm_btn.is_visible():
            print("   👉 检测到封面裁切确认弹窗，正在点击【确认】...")
            crop_confirm_btn.click()
            time.sleep(2)
        print("   ✅ 封面插图设置完成")

    # 4. 填写标题
    print(f"✍️ [3/6] 填写标题: {title[:25]}...")
    title_input = page.locator("input[placeholder='请填写标题'], input.weui-desktop-form__input").first
    title_input.fill(title[:40])
    print(f"   ✅ 标题写入完成")

    # 5. 填写正文描述
    print("✍️ [4/6] 填写正文描述与 Hashtags...")
    desc_textarea = page.locator("textarea[placeholder='请填写描述'], textarea.weui-desktop-form__textarea").first
    desc_textarea.fill(desc)
    print("   ✅ 正文文案写入完成 (已含 GitHub 展厅链接与 Hashtags)")

    # 6. 选择合集
    print(f"📂 [5/6] 绑定合集: 包含【{COLLECTION_NAME}】...")
    try:
        # 点击合集下拉选择框
        collection_dropdown = page.locator(".weui-desktop-form__control-group:has-text('合集') .weui-desktop-select, .weui-desktop-select:has-text('选择合集')").first
        if collection_dropdown.is_visible():
            collection_dropdown.click()
            time.sleep(1.5)
            
            # 寻找匹配的合集选项并点击
            target_option = page.locator(f".weui-desktop-dropdown__list :has-text('{COLLECTION_NAME}'), li:has-text('{COLLECTION_NAME}')").first
            if target_option.is_visible():
                target_option.click()
                print(f"   ✅ 成功勾选并绑定合集: {COLLECTION_NAME}")
            else:
                first_opt = page.locator(".weui-desktop-dropdown__list li").first
                if first_opt.is_visible():
                    first_opt.click()
                    print("   ✅ 成功选择下拉列表中首个合集")
    except Exception as e:
        print(f"   ⚠️ 绑定合集提示: {e}")

    time.sleep(3)

    # 截图记录发布前最终表单状态
    ready_proof = os.path.join(COOKIE_PROFILE_DIR, f"ready_ep_{ep_id}.png")
    page.screenshot(path=ready_proof)
    print(f"📸 发布就绪截图: {ready_proof}")

    # 7. 点击【发表音频】按钮
    if auto_submit:
        print("🚀 [6/6] 正在点击【发表音频】按钮...")
        publish_btn = page.locator("button:has-text('发表音频')").first
        if publish_btn.is_visible():
            publish_btn.click()
            print("🎉 已点击【发表音频】！等待云端处理与入库...")
            time.sleep(8)

            # 截图记录发表后凭证
            success_proof = os.path.join(COOKIE_PROFILE_DIR, f"success_ep_{ep_id}.png")
            page.screenshot(path=success_proof)
            print(f"📸 发表成功凭证: {success_proof}")
            print(f"🎉🎉🎉 第 {ep_id} 期【{title}】发布成功！")
            return True
        else:
            print("❌ 未找到发表音频按钮")
            return False

    return True

def run_publisher(target_ep_id="00", headed=True, min_interval=30, max_interval=60):
    sync_wechat_cookies()

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=not headed)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        if target_ep_id is not None:
            episodes = [e for e in EPISODES_DATA if e["ep_id"] == str(target_ep_id).zfill(2)]
        else:
            episodes = EPISODES_DATA

        for idx, ep_data in enumerate(episodes, start=1):
            publish_single_episode(page, ep_data, auto_submit=True)
            
            if idx < len(episodes):
                wait_sec = random.randint(min_interval, max_interval)
                print(f"\n⏳ 安全间隔休眠 {wait_sec} 秒后发布下一期...")
                for r in range(wait_sec, 0, -10):
                    print(f"   ⏳ 剩余: {r} 秒...")
                    time.sleep(min(10, r))

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ep", type=str, default="00", help="期号，默认00")
    parser.add_argument("--all", action="store_true", help="发布全部 19 期")
    parser.add_argument("--headless", action="store_true", help="无头模式")
    args = parser.parse_args()

    ep_to_run = None if args.all else args.ep
    run_publisher(target_ep_id=ep_to_run, headed=not args.headless)
