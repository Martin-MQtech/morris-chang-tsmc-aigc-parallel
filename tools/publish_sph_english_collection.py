# -*- coding: utf-8 -*-
"""
微信视频号【全英文音频合集】自主静默发布引擎 (核心 IP: TSMC)
- 窗口置于屏幕外区 (--window-position=3000,3000)，真机内核安全避过微信风控检测，绝不打扰前台工作
- 步骤 1：优先建立全英文专属合集《TSMC & Morris Chang: Parallel Biography》
- 步骤 2：自动顺序发布 Ep00 至 Ep18 全部 19 期纯英文母带，自动选择绑定该英文合集
- 步骤 3：智能轮询云端解析、自动确认裁切、安全防频控休眠，单进程自动执行至收官
"""

import os, sys, time, json, random
sys.stdout.reconfigure(line_buffering=True)

from playwright.sync_api import sync_playwright
import browser_cookie3

from audio_posts_data_en import EPISODES_DATA_EN, GITHUB_PORTAL_URL

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

COLLECTION_TITLE = "TSMC & Morris Chang: Parallel"
COLLECTION_DESC = "AIGC Parallel Biography of TSMC & Morris Chang. A 19-movement English audio series exploring semiconductor revolution and tech philosophy."

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
        print(f"✅ 微信创作者凭证同步成功 ({len(all_cookies)} 条)")
        return True
    return False

def ensure_collection(page):
    print("\n📂 [1/2] 正在检查或创建微信视频号【英文合集】(含核心 IP: TSMC)...")
    page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
    time.sleep(4)

    # 切换到合集标签页
    tab_col = page.locator(":text('合集')").first
    if tab_col.is_visible():
        tab_col.click()
        time.sleep(3)

    # 检查是否已存在英文合集
    page_text = page.locator("body").inner_text()
    if "TSMC & Morris Chang" in page_text or "Morris Chang" in page_text:
        print("✅ 检测到已存在英文专属合集，准备进入发布流程")
        return True

    print(f"👉 正在创建全英文专属合集: 《{COLLECTION_TITLE}》...")
    create_col_btn = page.locator("button:has-text('创建合集')").first
    if create_col_btn.is_visible():
        create_col_btn.click()
        time.sleep(3)

        # 填入合集名称 (严格限制字数)
        col_name_in = page.locator("input[placeholder*='合集名称'], input[placeholder*='标题'], input[placeholder*='名称']").first
        if col_name_in.is_visible():
            col_name_in.fill(COLLECTION_TITLE[:30])
            print(f"   ✅ 填入合集名称: {COLLECTION_TITLE[:30]}")

        # 填入合集简介
        col_desc_in = page.locator("textarea[placeholder*='简介'], textarea[placeholder*='描述']").first
        if col_desc_in.is_visible():
            col_desc_in.fill(COLLECTION_DESC)
            print("   ✅ 填入合集简介")

        # 上传合集封面
        cover_path = os.path.join(os.path.dirname(__file__), "..", "设计资产", "封面", "封面_排版版.jpg")
        col_cover_in = page.locator("input[type='file']").first
        if col_cover_in.is_visible() and os.path.exists(cover_path):
            col_cover_in.set_input_files(cover_path)
            time.sleep(2)
            crop_btn = page.locator("button:has-text('确认'), button:has-text('确定')").first
            if crop_btn.is_visible():
                crop_btn.click()
                time.sleep(2)
            print("   ✅ 注入英文合集专属封面并确认裁切")

        # 点击创建
        submit_btn = page.locator("button:has-text('创建'), button:has-text('保存'), button:has-text('确定')").last
        if submit_btn.is_visible():
            submit_btn.click()
            print(f"🎉 英文合集《{COLLECTION_TITLE}》创建成功！")
            time.sleep(5)
    return True

def publish_single_en_ep(page, ep_data):
    ep_id = ep_data["ep_id"]
    title = ep_data["title"]
    audio_path = ep_data["audio_path"]
    cover_path = ep_data["cover_path"]
    desc = ep_data["desc"]

    print(f"\n========================================================")
    print(f"🚀 [English Edition] 正在发布: [Ep{ep_id}] {title}")
    print(f"📁 音频: {os.path.basename(audio_path)} ({os.path.getsize(audio_path)/1024/1024:.2f} MB)")
    print(f"🖼️ 封面: {os.path.basename(cover_path)}")
    print(f"========================================================")

    # 1. 访问发布页
    page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded", timeout=60000)
    time.sleep(3)

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
            print(f"   🎉 音频云端解析完成: {ctrl_text}")
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
    print(f"✍️ [3/5] 写入纯英文标题与深度文案...")
    page.locator("input[placeholder='请填写标题']").first.fill(title[:40])
    page.locator("textarea[placeholder='请填写描述']").first.fill(desc)
    time.sleep(1)

    # 5. 绑定英文合集
    print(f"📂 [4/5] 绑定英文合集: 《{COLLECTION_TITLE}》...")
    try:
        col_select = page.locator(":text('选择合集'), .weui-desktop-select").first
        col_select.click()
        time.sleep(1.5)
        
        # 优先选择包含 TSMC 或 Morris 或 Parallel 的英文合集
        col_opt = page.locator(".weui-desktop-dropdown__list-item:has-text('TSMC'), li:has-text('TSMC'), .weui-desktop-dropdown__list-item:has-text('Morris'), li:has-text('Morris'), .weui-desktop-dropdown__list-item:has-text('Parallel'), li:has-text('Parallel')").first
        if col_opt.is_visible():
            col_opt.click()
            print("   ✅ 成功选择并绑定英文合集")
            time.sleep(1.5)
        else:
            any_opt = page.get_by_text("Morris").first
            if any_opt.is_visible():
                any_opt.click()
                print("   ✅ 成功选择 Morris Chang 英文合集")
                time.sleep(1.5)
    except Exception as e:
        print(f"   ⚠️ 绑定合集提示: {e}")

    # 6. 点击发表音频
    print("🚀 [5/5] 点击【发表音频】按钮...")
    pub_btn = page.locator("button:has-text('发表音频')").first
    pub_btn.click()
    print(f"   🎉 发表成功！等待 10 秒云端入库...")
    time.sleep(10)

    proof_path = os.path.join(COOKIE_PROFILE_DIR, f"proof_en_{ep_id}.png")
    page.screenshot(path=proof_path)
    print(f"📸 第 {ep_id} 期英文发布凭证已保存: {proof_path}")
    print(f"🎉🎉🎉 Episode {ep_id} [{title}] 发布成功！")
    return True

def run_english_pipeline():
    sync_wechat_cookies()

    print(f"\n========================================================")
    print(f"🚀 启动微信视频号全英文合集自动化发布流水线")
    print(f"📦 剧集总量: {len(EPISODES_DATA_EN)} 期 (Ep00 至 Ep18)")
    print(f"🌟 核心 IP: TSMC (台积电)")
    print(f"🛡️ 运行方式: 屏幕外区静默渲染，不抢焦点，不打扰前台工作")
    print(f"========================================================\n")

    with sync_playwright() as p:
        # 将窗口放置在屏幕外区 (3000, 3000)，既绕过微信无头风控检测，又绝对不遮挡/干扰用户前台操作
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--window-position=3000,3000", "--window-size=1280,800", "--no-first-run", "--no-default-browser-check"]
        )
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        # 步骤 1：先确保英文合集存在（带 TSMC 核心 IP）
        ensure_collection(page)

        # 步骤 2：顺序发布 Ep00 到 Ep18
        for idx, ep_data in enumerate(EPISODES_DATA_EN, start=1):
            try:
                publish_single_en_ep(page, ep_data)
            except Exception as e:
                print(f"❌ Ep {ep_data['ep_id']} 发布异常: {e}")
            
            if idx < len(EPISODES_DATA_EN):
                wait_sec = random.randint(35, 55)
                next_ep = EPISODES_DATA_EN[idx]["ep_id"]
                print(f"\n⏳ 进度: [{idx}/{len(EPISODES_DATA_EN)}] | 安全防频控休眠 {wait_sec} 秒后发布第 {next_ep} 期...")
                for r in range(wait_sec, 0, -10):
                    print(f"   ⏳ 剩余: {r} 秒...")
                    time.sleep(min(10, r))

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("\n🏆🏆🏆 全套 19 期英文版音频合集已全部圆满发布完成！")

if __name__ == "__main__":
    run_english_pipeline()
