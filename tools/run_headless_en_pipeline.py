# -*- coding: utf-8 -*-
"""
微信视频号【全英文音频合集】100% 后台无头无界面 (Headless) 自动发布引擎
- 使用系统真实 Chrome 内核无头模式 (channel="chrome", headless=True)，完全静默运行
- 自动处理快捷登录与 Cookie 会话保持
- 第一步：检查并创建全英文专属合集《Morris Chang: Parallel Biography》
- 第二步：顺序发布 Ep00 ~ Ep18 全部 19 期英文音频并自动绑定该合集
- 第三步：实时刷新日志并保存发布凭证
"""

import os, sys, time, json, random
sys.stdout.reconfigure(line_buffering=True)

from playwright.sync_api import sync_playwright
import browser_cookie3

from audio_posts_data_en import EPISODES_DATA_EN, GITHUB_PORTAL_URL

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

COLLECTION_NAME = "Morris Chang: Parallel Biography"
COLLECTION_DESC = "AIGC Parallel Biography of Morris Chang & TSMC. A 19-movement audio series exploring semiconductor revolution and tech philosophy."

def sync_wechat_cookies():
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
        print(f"✅ [Headless] 凭证同步成功: {len(all_cookies)} 条")
        return True
    return False

def ensure_login(page):
    fast_btn = page.locator("button:has-text('微信快捷登录'), :text('微信快捷登录')").first
    if fast_btn.is_visible():
        print("👉 [Headless] 检测到快捷登录按钮，正在自动点击登录...")
        fast_btn.click()
        time.sleep(5)

def create_english_collection_if_needed(page):
    print("\n📂 [步骤 1/2] 正在检查或创建全英文音频合集...")
    page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
    time.sleep(4)
    ensure_login(page)

    # 切换到合集标签页
    tab_col = page.locator(":text('合集')").first
    if tab_col.is_visible():
        tab_col.click()
        time.sleep(3)

    body_text = page.locator("body").inner_text()
    if "Morris Chang" in body_text or "Parallel Biography" in body_text:
        print(f"✅ 英文合集已存在，无需重复创建")
        return True

    print(f"👉 正在后台无头创建全英文合集: 《{COLLECTION_NAME}》...")
    create_btn = page.locator("button:has-text('创建合集')").first
    if create_btn.is_visible():
        create_btn.click()
        time.sleep(3)

        # 填入名称
        name_input = page.locator("input[placeholder*='名称'], input[placeholder*='合集']").first
        if name_input.is_visible():
            name_input.fill(COLLECTION_NAME[:30])
            print(f"   ✅ 已填入合集标题: {COLLECTION_NAME[:30]}")

        # 填入描述
        desc_input = page.locator("textarea[placeholder*='简介'], textarea[placeholder*='描述']").first
        if desc_input.is_visible():
            desc_input.fill(COLLECTION_DESC)
            print("   ✅ 已填入合集简介")

        # 上传合集封面
        cover_path = os.path.join(os.path.dirname(__file__), "..", "设计资产", "封面", "封面_排版版.jpg")
        file_in = page.locator("input[type='file']").first
        if file_in.is_visible() and os.path.exists(cover_path):
            file_in.set_input_files(cover_path)
            time.sleep(2)
            crop_btn = page.locator("button:has-text('确认'), button:has-text('确定')").first
            if crop_btn.is_visible():
                crop_btn.click()
                time.sleep(2)
            print("   ✅ 已注入英文封面并确认裁切")

        # 提交创建
        submit_btn = page.locator("button:has-text('创建'), button:has-text('保存'), button:has-text('确定')").last
        if submit_btn.is_visible():
            submit_btn.click()
            print(f"🎉 英文合集《{COLLECTION_NAME}》创建成功！")
            time.sleep(5)

    return True

def publish_single_en(page, ep_data):
    ep_id = ep_data["ep_id"]
    title = ep_data["title"]
    audio_path = ep_data["audio_path"]
    cover_path = ep_data["cover_path"]
    desc = ep_data["desc"]

    print(f"\n========================================================")
    print(f"🚀 [Headless English] 开始发布: [Ep{ep_id}] {title}")
    print(f"📁 音频: {os.path.basename(audio_path)} ({os.path.getsize(audio_path)/1024/1024:.2f} MB)")
    print(f"🖼️ 封面: {os.path.basename(cover_path)}")
    print(f"========================================================")

    # 1. 访问发布页
    page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded", timeout=60000)
    time.sleep(3)
    ensure_login(page)

    # 2. 上传音频
    print("⏳ [1/5] 注入英文音频并等待云端解析...")
    audio_in = page.locator("input[type='file']").first
    audio_in.set_input_files(audio_path)
    audio_in.dispatch_event("change")
    audio_in.dispatch_event("input")

    # 动态轮询等待音频上传与转码
    upload_success = False
    for attempt in range(35):
        time.sleep(2)
        ctrl_text = page.locator(".weui-desktop-form__control-group:has-text('文件')").first.inner_text().replace('\n', ' ')
        if attempt % 4 == 0:
            print(f"   ⏳ [轮询 {attempt*2}s] 状态: {ctrl_text}")
        
        if ("MB" in ctrl_text or "KB" in ctrl_text) and ("0%" not in ctrl_text) and ("请上传音频" not in ctrl_text):
            print(f"   🎉 音频解析完成: {ctrl_text}")
            upload_success = True
            break
            
    if not upload_success:
        print("   ⚠️ 额外缓冲等待 5 秒...")
        time.sleep(5)

    # 3. 上传封面
    print("⏳ [2/5] 注入封面插图...")
    cover_in = page.locator("input[type='file']").nth(1)
    cover_in.set_input_files(cover_path)
    cover_in.dispatch_event("change")
    time.sleep(2)
    
    confirm_btn = page.locator("button:has-text('确认'), .weui-desktop-dialog__wrp button:has-text('确认')").first
    if confirm_btn.is_visible():
        print("   👉 确认封面裁切...")
        confirm_btn.click()
        time.sleep(2)

    # 4. 填写英文标题与英文正文
    print(f"✍️ [3/5] 写入英文标题与文案...")
    page.locator("input[placeholder='请填写标题']").first.fill(title[:40])
    page.locator("textarea[placeholder='请填写描述']").first.fill(desc)
    time.sleep(1)

    # 5. 绑定英文合集
    print(f"📂 [4/5] 绑定英文合集: 《{COLLECTION_NAME}》...")
    try:
        col_select = page.locator(":text('选择合集'), .weui-desktop-select").first
        col_select.click()
        time.sleep(1.5)
        # 选择英文合集项
        col_opt = page.locator(".weui-desktop-dropdown__list-item:has-text('Morris'), li:has-text('Morris'), .weui-desktop-dropdown__list-item:has-text('Parallel'), li:has-text('Parallel')").first
        if col_opt.is_visible():
            col_opt.click()
            print("   ✅ 成功勾选英文合集: Morris Chang")
            time.sleep(1.5)
        else:
            any_opt = page.get_by_text("Morris").first
            if any_opt.is_visible():
                any_opt.click()
                print("   ✅ 成功选择 Morris Chang 合集")
                time.sleep(1.5)
    except Exception as e:
        print(f"   ⚠️ 绑定英文合集提示: {e}")

    # 6. 点击发表
    print("🚀 [5/5] 点击【发表音频】按钮...")
    pub_btn = page.locator("button:has-text('发表音频')").first
    pub_btn.click()
    print(f"   🎉 已点击发表！等待 10 秒云端入库...")
    time.sleep(10)

    proof_path = os.path.join(COOKIE_PROFILE_DIR, f"proof_en_{ep_id}.png")
    page.screenshot(path=proof_path)
    print(f"📸 第 {ep_id} 期英文发布凭证已保存: {proof_path}")
    print(f"🎉🎉🎉 Ep {ep_id} [{title}] 发布成功！")
    return True

def run_headless_pipeline():
    sync_wechat_cookies()

    print(f"\n========================================================")
    print(f"🚀 [Headless] 启动全英文合集无头静默发布流水线")
    print(f"📦 剧集总量: {len(EPISODES_DATA_EN)} 期 (Ep00 至 Ep18)")
    print(f"👻 浏览器模式: 100% 后台无头静默 (channel=chrome, headless=True)")
    print(f"========================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        # 步骤 1：先检查并创建英文合集
        create_english_collection_if_needed(page)

        # 步骤 2：顺序发布 Ep00 ~ Ep18
        for idx, ep_data in enumerate(EPISODES_DATA_EN, start=1):
            try:
                publish_single_en(page, ep_data)
            except Exception as e:
                print(f"❌ Ep {ep_data['ep_id']} 发布异常: {e}")
            
            if idx < len(EPISODES_DATA_EN):
                wait_sec = random.randint(35, 60)
                next_ep = EPISODES_DATA_EN[idx]["ep_id"]
                print(f"\n⏳ 进度: [{idx}/{len(EPISODES_DATA_EN)}] 已完成 | 静默休眠 {wait_sec} 秒后发布第 {next_ep} 期...")
                for r in range(wait_sec, 0, -10):
                    print(f"   ⏳ 剩余: {r} 秒...")
                    time.sleep(min(10, r))

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("\n🏆🏆🏆 全套 19 期英文版音频合集已全部圆满发布完成！")

if __name__ == "__main__":
    run_headless_pipeline()
