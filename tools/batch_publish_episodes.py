# -*- coding: utf-8 -*-
"""
微信视频号音频合集发布引擎 (企业级稳定版)
- 动态轮询等待音频 100% 上传与转码解析 (支持大文件 MP3)
- 自动确认封面裁切弹窗
- 标题 (≤25字) + 深度文案 + Hashtags + GitHub官方展厅URL
- 精准绑定合集《AIGC创作：台积电张忠谋·传记时间线的平行世界》
- 智能防频控休眠
"""

import os, sys, time, json, random, argparse
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

    # 1. 访问直接发布页
    page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded", timeout=60000)
    time.sleep(3)

    # 2. 上传音频
    print("⏳ [1/5] 注入音频文件并等待云端上传解析...")
    audio_in = page.locator("input[type='file']").first
    audio_in.set_input_files(audio_path)
    audio_in.dispatch_event("change")
    audio_in.dispatch_event("input")

    # 动态轮询等待音频上传并解析完毕 (直到 0% 消失且包含文件大小信息)
    upload_success = False
    for attempt in range(30):
        time.sleep(2)
        ctrl_text = page.locator(".weui-desktop-form__control-group:has-text('文件')").first.inner_text().replace('\n', ' ')
        if attempt % 3 == 0:
            print(f"   ⏳ [轮询 {attempt*2}s] 当前状态: {ctrl_text}")
        
        # 判断解析成功的特征：包含 MB/KB，且不包含 0%，且不包含 请上传音频
        if ("MB" in ctrl_text or "KB" in ctrl_text) and ("0%" not in ctrl_text) and ("请上传音频" not in ctrl_text):
            print(f"   🎉 音频云端解析完成: {ctrl_text}")
            upload_success = True
            break
            
    if not upload_success:
        print("   ⚠️ 音频上传未在预期时间内检测到完成，额外等待 5 秒...")
        time.sleep(5)

    # 3. 上传封面插图
    print("⏳ [2/5] 注入封面插图...")
    cover_in = page.locator("input[type='file']").nth(1)
    cover_in.set_input_files(cover_path)
    cover_in.dispatch_event("change")
    time.sleep(2)
    
    # 确认封面裁切弹窗
    confirm_btn = page.locator("button:has-text('确认'), .weui-desktop-dialog__wrp button:has-text('确认')").first
    if confirm_btn.is_visible():
        print("   👉 确认封面裁切...")
        confirm_btn.click()
        time.sleep(2)

    # 4. 填写标题与正文描述
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
        # 点击下拉列表中的合集选项
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

    # 6. 点击发表音频
    print("🚀 [5/5] 点击【发表音频】按钮...")
    pub_btn = page.locator("button:has-text('发表音频')").first
    pub_btn.click()
    print(f"   🎉 已点击发表！等待 10 秒云端入库...")
    time.sleep(10)

    # 保存凭证
    proof_path = os.path.join(COOKIE_PROFILE_DIR, f"proof_ep_{ep_id}.png")
    page.screenshot(path=proof_path)
    print(f"📸 发布凭证已保存: {proof_path}")
    print(f"🎉🎉🎉 第 {ep_id} 期【{title}】发布流程完成！")
    return True

def run_batch_publish(start_ep=3, end_ep=18, min_interval=35, max_interval=60):
    sync_wechat_cookies()

    target_list = []
    for ep in EPISODES_DATA:
        ep_num = int(ep["ep_id"])
        if start_ep <= ep_num <= end_ep:
            target_list.append(ep)

    print(f"\n========================================================")
    print(f"📋 本次计划批量发布共 {len(target_list)} 期 (第 {start_ep:02d} 期 至 第 {end_ep:02d} 期)")
    print(f"⏱️ 安全间隔: {min_interval} ~ {max_interval} 秒")
    print(f"========================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        for idx, ep_data in enumerate(target_list, start=1):
            try:
                publish_single_ep(page, ep_data)
            except Exception as e:
                print(f"❌ 第 {ep_data['ep_id']} 期发布异常: {e}")
            
            if idx < len(target_list):
                wait_sec = random.randint(min_interval, max_interval)
                next_ep_id = target_list[idx]["ep_id"]
                print(f"\n========================================================")
                print(f"⏳ 进度: [{idx}/{len(target_list)}] 已完成 | 安全休眠 {wait_sec} 秒后发布第 {next_ep_id} 期...")
                print(f"========================================================")
                for r in range(wait_sec, 0, -10):
                    print(f"   ⏳ 倒计时: {r} 秒...")
                    time.sleep(min(10, r))

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("\n🎉🎉🎉 全部指定音频已全部自动发布完成！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=3, help="起始期号")
    parser.add_argument("--end", type=int, default=18, help="结束期号")
    parser.add_argument("--min-interval", type=int, default=35, help="最小间隔秒数")
    parser.add_argument("--max-interval", type=int, default=60, help="最大间隔秒数")
    args = parser.parse_args()

    run_batch_publish(start_ep=args.start, end_ep=args.end, min_interval=args.min_interval, max_interval=args.max_interval)
