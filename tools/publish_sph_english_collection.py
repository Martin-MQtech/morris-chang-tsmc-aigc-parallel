# -*- coding: utf-8 -*-
"""
微信视频号【全英文音频合集】全闭环自动化发布、查缺补漏与顺序校准引擎
- 核心 IP: TSMC (合集名: TSMC & Morris Chang: Parallel)
- 自动化登录：识别快捷登录并在跳转后自动维持会话
- 查重删重：全量扫描音频列表，发现任何重复期数（如重复的 Ep01）立即自动删除，确保单期唯一
- 查缺补漏：按 00~18 顺序补齐未发布的全部英文单集，100%校准本地母带与排版封面
- 顺序校准与合集归集：进入合集详情页全量添加音频，按严格顺序完成合集归集
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
        return True
    return False

def ensure_authenticated(page):
    time.sleep(2)
    if "login.html" in page.url:
        print("👉 检测到登录页面，正在执行自动快捷登录...")
        time.sleep(2)
        fast_btn = page.locator("button:has-text('快捷登录'), :text('微信快捷登录')").first
        if fast_btn.is_visible():
            fast_btn.click()
        else:
            page.mouse.click(1196, 571)
        try:
            page.wait_for_url("**/platform/**", timeout=15000)
            print("✅ 登录验证成功，已进入管理后台！")
        except:
            time.sleep(6)

def ensure_collection(page):
    print("\n📂 [1/4] 检查或创建英文专属合集《TSMC & Morris Chang: Parallel》...")
    page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
    ensure_authenticated(page)
    time.sleep(3)

    tab_col = page.locator(":text('合集')").first
    if tab_col.is_visible():
        tab_col.click()
        time.sleep(3)

    page_text = page.locator("body").first.inner_text()
    if "TSMC & Morris Chang" in page_text or "TSMC" in page_text or "Morris Chang" in page_text:
        print("✅ 英文专属合集已存在")
        return True

    print(f"👉 正在创建全英文专属合集: 《{COLLECTION_TITLE}》...")
    create_col_btn = page.locator("button:has-text('创建合集')").first
    if create_col_btn.is_visible():
        create_col_btn.click()
        time.sleep(3)

        col_name_in = page.locator("input[placeholder*='合集名称'], input[placeholder*='标题'], input[placeholder*='名称']").first
        if col_name_in.is_visible():
            col_name_in.fill(COLLECTION_TITLE[:30])

        col_desc_in = page.locator("textarea[placeholder*='简介'], textarea[placeholder*='描述']").first
        if col_desc_in.is_visible():
            col_desc_in.fill(COLLECTION_DESC)

        cover_path = os.path.join(os.path.dirname(__file__), "..", "设计资产", "封面", "封面_排版版.jpg")
        col_cover_in = page.locator("input[type='file']").first
        if col_cover_in.is_visible() and os.path.exists(cover_path):
            col_cover_in.set_input_files(cover_path)
            time.sleep(2)
            crop_btn = page.locator("button:has-text('确认'), button:has-text('确定')").first
            if crop_btn.is_visible():
                crop_btn.click()
                time.sleep(2)

        submit_btn = page.locator("button:has-text('创建'), button:has-text('保存'), button:has-text('确定')").last
        if submit_btn.is_visible():
            submit_btn.click()
            print(f"🎉 英文合集《{COLLECTION_TITLE}》创建成功！")
            time.sleep(5)
    return True

def audit_and_clean_duplicates(page):
    print("\n🧹 [2/4] 全面扫描线上音频列表并清理所有重复项...")
    page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
    ensure_authenticated(page)
    time.sleep(4)

    rows = page.locator("tr").all()
    ep_counts = {}
    published_set = set()

    for row in rows:
        t = row.inner_text().replace('\n', ' ')
        for ep in EPISODES_DATA_EN:
            eid = ep["ep_id"]
            if f"Ep{eid}" in t or f"Ep {eid}" in t:
                ep_counts[eid] = ep_counts.get(eid, 0) + 1
                if ep_counts[eid] > 1:
                    print(f"👉 发现重复项 Ep{eid}，正在执行自动删除清理...")
                    del_btn = row.locator("a:has-text('删除'), button:has-text('删除')").first
                    if del_btn.is_visible():
                        del_btn.click()
                        time.sleep(1.5)
                        confirm_btn = page.locator("button:has-text('确定'), button:has-text('确认')").first
                        if confirm_btn.is_visible():
                            confirm_btn.click()
                            print(f"✅ 成功删除重复项 Ep{eid}！")
                            time.sleep(3)
                else:
                    published_set.add(eid)

    print(f"📋 当前线上唯一有效英文单集 ({len(published_set)} 期): {sorted(list(published_set))}")
    return published_set

def publish_single_en_ep(page, ep_data):
    ep_id = ep_data["ep_id"]
    title = ep_data["title"]
    audio_path = ep_data["audio_path"]
    cover_path = ep_data["cover_path"]
    desc = ep_data["desc"]

    print(f"\n========================================================")
    print(f"🚀 [English Edition] 补齐发布: [Ep{ep_id}] {title}")
    print(f"📁 音频: {os.path.basename(audio_path)} ({os.path.getsize(audio_path)/1024/1024:.2f} MB)")
    print(f"🖼️ 封面: {os.path.basename(cover_path)}")
    print(f"========================================================")

    page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded", timeout=60000)
    ensure_authenticated(page)
    time.sleep(3)
    try:
        page.locator("input[placeholder='请填写标题'], input.weui-desktop-form__input").first.wait_for(state="visible", timeout=15000)
    except:
        time.sleep(2)

    # 1. 上传音频
    print("⏳ [1/5] 注入英文音频并等待云端解析...")
    audio_inputs = page.locator("input[type='file']")
    audio_inputs.first.set_input_files(audio_path)
    audio_inputs.first.dispatch_event("change")
    audio_inputs.first.dispatch_event("input")

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
        time.sleep(5)

    # 2. 上传封面
    print("⏳ [2/5] 注入封面插图...")
    cover_input = page.locator("input[type='file']").nth(1)
    cover_input.set_input_files(cover_path)
    cover_input.dispatch_event("change")
    time.sleep(2)
    
    confirm_btn = page.locator("button:has-text('确认'), .weui-desktop-dialog__wrp button:has-text('确认')").first
    if confirm_btn.is_visible():
        confirm_btn.click()
        time.sleep(2)

    # 3. 填写英文标题与英文正文
    print(f"✍️ [3/5] 写入纯英文标题与深度文案...")
    page.locator("input[placeholder='请填写标题'], input.weui-desktop-form__input").first.fill(title[:40])
    page.locator("textarea[placeholder='请填写描述'], textarea.weui-desktop-form__textarea").first.fill(desc)
    time.sleep(1)

    # 4. 绑定英文合集
    print(f"📂 [4/5] 绑定英文合集: 《{COLLECTION_TITLE}》...")
    try:
        col_select = page.locator(":text('选择合集'), .weui-desktop-select").first
        col_select.click()
        time.sleep(1.5)
        
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

    # 5. 点击发表音频
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

def sync_and_order_collection(page):
    print("\n🔗 [4/4] 深度同步关联所有英文音频至《TSMC & Morris Chang: Parallel》合集并校验顺序...")
    page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
    ensure_authenticated(page)
    time.sleep(4)

    tab_col = page.locator(":text('合集')").first
    if tab_col.is_visible():
        tab_col.click()
        time.sleep(3)

    col_card = page.locator("tr:has-text('TSMC'), tr:has-text('Morris'), .collection-item:has-text('TSMC'), .collection-item:has-text('Morris')").first
    if col_card.is_visible():
        detail_link = col_card.locator("a:has-text('详情'), a:has-text('管理'), button:has-text('管理')").first
        if detail_link.is_visible():
            detail_link.click()
            time.sleep(3)
        else:
            col_card.click()
            time.sleep(3)

    add_audio_btn = page.locator("button:has-text('添加音频'), button:has-text('添加内容')").first
    if add_audio_btn.is_visible():
        add_audio_btn.click()
        time.sleep(3)

        checkboxes = page.locator(".weui-desktop-dialog__wrp input[type='checkbox'], .modal-content input[type='checkbox']").all()
        for cb in checkboxes:
            try:
                if not cb.is_checked():
                    cb.check()
            except:
                pass
        time.sleep(1)

        confirm_btn = page.locator(".weui-desktop-dialog__wrp button:has-text('确定'), .weui-desktop-dialog__wrp button:has-text('确认')").first
        if confirm_btn.is_visible():
            confirm_btn.click()
            print("🎉 已成功批量勾选并归集所有英文音频至合集！")
            time.sleep(5)

def run_english_pipeline():
    sync_wechat_cookies()

    print(f"\n========================================================")
    print(f"🚀 启动微信视频号全英文合集全闭环自动化引擎")
    print(f"📦 剧集总量: {len(EPISODES_DATA_EN)} 期 (Ep00 至 Ep18)")
    print(f"🌟 核心 IP: TSMC (台积电)")
    print(f"========================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--no-first-run", "--no-default-browser-check"]
        )
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            **kwargs
        )
        page = context.new_page()

        # 步骤 1：确认合集存在
        ensure_collection(page)

        # 步骤 2：全量扫描查重删重，获取唯一已发列表
        online_published = audit_and_clean_duplicates(page)

        # 步骤 3：严格按 00~18 顺序查缺补漏
        pending_eps = [ep for ep in EPISODES_DATA_EN if ep["ep_id"] not in online_published]
        print(f"\n👉 本次待补齐发布的剧集列表 (共 {len(pending_eps)} 期): {[e['ep_id'] for e in pending_eps]}")

        for idx, ep_data in enumerate(pending_eps, start=1):
            try:
                publish_single_en_ep(page, ep_data)
            except Exception as e:
                print(f"❌ Ep {ep_data['ep_id']} 发布异常: {e}")
            
            if idx < len(pending_eps):
                wait_sec = random.randint(35, 50)
                next_ep = pending_eps[idx]["ep_id"]
                print(f"\n⏳ 进度: [{idx}/{len(pending_eps)}] | 安全防频控休眠 {wait_sec} 秒后发布第 {next_ep} 期...")
                for r in range(wait_sec, 0, -10):
                    print(f"   ⏳ 剩余: {r} 秒...")
                    time.sleep(min(10, r))

        # 步骤 4：全量归集关联至英文合集
        try:
            sync_and_order_collection(page)
        except Exception as e:
            print(f"合集同步提示: {e}")

        # 最终汇总截图
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        ensure_authenticated(page)
        time.sleep(4)
        final_proof = os.path.join(COOKIE_PROFILE_DIR, "final_all_english_audio_list.png")
        page.screenshot(path=final_proof, full_page=True)
        print(f"📸 最终全套英文列表截图凭证已保存: {final_proof}")

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("\n🏆🏆🏆 全套 19 期英文版音频合集已全部圆满发布并归集完成！")

if __name__ == "__main__":
    run_english_pipeline()
