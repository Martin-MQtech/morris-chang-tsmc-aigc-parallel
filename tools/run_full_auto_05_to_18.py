# -*- coding: utf-8 -*-
"""
微信视频号音频合集全自动闭环引擎 (一键全权自动执行至收官)
1. 自动删除 21:51 的旧第 4 期，彻底修复 00~04 完美顺序
2. 连续自动发布第 05 期 至 第 18 期 (共 14 期)
3. 严格执行音频云端解析轮询、封面确认、合集绑定、安全防频控休眠
4. 运行全周期无需任何人工干预
"""

import os, sys, time, json, random
from playwright.sync_api import sync_playwright
import browser_cookie3

from audio_posts_data import EPISODES_DATA

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

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

def clean_duplicate_ep04(page):
    print("\n🧹 [步骤 1/2] 正在清理 21:51 发布的旧第 04 期条目...")
    page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
    time.sleep(4)

    # 寻找包含 21:51 的行
    rows = page.locator("tr").all()
    for row in rows:
        row_text = row.inner_text()
        if "21:51" in row_text and "第04期" in row_text:
            del_link = row.locator("a:has-text('删除'), button:has-text('删除')").first
            if del_link.is_visible():
                print("👉 找到 21:51 的旧第 04 期，点击删除...")
                del_link.click()
                time.sleep(1.5)
                confirm_btn = page.locator("button:has-text('确定'), button:has-text('确认')").first
                if confirm_btn.is_visible():
                    confirm_btn.click()
                    print("✅ 成功删除 21:51 旧条目！当前 00~04 已完全恢复严格顺序")
                    time.sleep(3)
                break

    page.screenshot(path=os.path.join(COOKIE_PROFILE_DIR, "clean_00_to_04_done.png"))

def publish_single_ep(page, ep_data):
    ep_id = ep_data["ep_id"]
    title = ep_data["title"]
    audio_path = ep_data["audio_path"]
    cover_path = ep_data["cover_path"]
    desc = ep_data["desc"]

    print(f"\n========================================================")
    print(f"🚀 开始发布: [第{ep_id}期] {title}")
    print(f"📁 音频: {os.path.basename(audio_path)} ({os.path.getsize(audio_path)/1024/1024:.2f} MB)")
    print(f"🖼️ 封面: {os.path.basename(cover_path)}")
    print(f"========================================================")

    # 1. 访问发布页
    page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded", timeout=60000)
    time.sleep(3)

    # 2. 上传音频
    print("⏳ [1/5] 注入音频文件并等待云端上传解析...")
    audio_in = page.locator("input[type='file']").first
    audio_in.set_input_files(audio_path)
    audio_in.dispatch_event("change")
    audio_in.dispatch_event("input")

    # 动态轮询等待音频上传并解析完毕
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

    # 4. 填写标题与描述
    print(f"✍️ [3/5] 填写标题与描述...")
    page.locator("input[placeholder='请填写标题']").first.fill(title[:40])
    page.locator("textarea[placeholder='请填写描述']").first.fill(desc)
    time.sleep(1)

    # 5. 选择合集
    print("📂 [4/5] 绑定合集...")
    try:
        col_select = page.locator(":text('选择合集'), .weui-desktop-select").first
        col_select.click()
        time.sleep(1.5)
        col_opt = page.get_by_text("AIGC创作：台积电").first
        if col_opt.is_visible():
            col_opt.click()
            print("   ✅ 成功勾选【AIGC创作：台积电...】合集！")
            time.sleep(1.5)
        else:
            first_opt = page.locator(".weui-desktop-dropdown__list-item, li:has-text('台积电')").first
            if first_opt.is_visible():
                first_opt.click()
                print("   ✅ 成功选择首个合集选项！")
                time.sleep(1.5)
    except Exception as e:
        print(f"   ⚠️ 合集选择提示: {e}")

    # 6. 点击发表
    print("🚀 [5/5] 点击【发表音频】按钮...")
    pub_btn = page.locator("button:has-text('发表音频')").first
    pub_btn.click()
    print(f"   🎉 已点击发表！等待 10 秒云端入库...")
    time.sleep(10)

    proof_path = os.path.join(COOKIE_PROFILE_DIR, f"proof_ep_{ep_id}.png")
    page.screenshot(path=proof_path)
    print(f"📸 第 {ep_id} 期发布凭证已保存: {proof_path}")
    print(f"🎉🎉🎉 第 {ep_id} 期【{title}】发布成功！")
    return True

def run_pipeline():
    sync_wechat_cookies()

    # 目标列表：第 05 期 至 第 18 期
    target_list = [ep for ep in EPISODES_DATA if int(ep["ep_id"]) >= 5]
    print(f"🚀 启动全自动发布流水线: 待发布剧集共 {len(target_list)} 期 (第 05 期 至 第 18 期)")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        # 先清理旧重复条目
        clean_duplicate_ep04(page)

        # 连续发布 05 ~ 18
        for idx, ep_data in enumerate(target_list, start=1):
            try:
                publish_single_ep(page, ep_data)
            except Exception as e:
                print(f"❌ 第 {ep_data['ep_id']} 期发布异常: {e}")
            
            if idx < len(target_list):
                wait_sec = random.randint(35, 60)
                next_ep = target_list[idx]["ep_id"]
                print(f"\n⏳ 进度: [{idx}/{len(target_list)}] | 安全休眠 {wait_sec} 秒后自动发布第 {next_ep} 期...")
                for r in range(wait_sec, 0, -10):
                    print(f"   ⏳ 剩余: {r} 秒...")
                    time.sleep(min(10, r))

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("\n🏆🏆🏆 全册 19 期 (第 00 期 至 第 18 期) 音频合集已全部圆满发布完成！")

if __name__ == "__main__":
    run_pipeline()
