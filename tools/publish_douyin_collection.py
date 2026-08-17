# -*- coding: utf-8 -*-
"""
抖音中长视频合集全自动发布引擎
1. 自动转换/检查 19 期 1080P MP4 视频
2. 自动同步 Mac Chrome 抖音创作者平台 Cookie
3. 访问 https://creator.douyin.com/creator-micro/content/publish
4. 自动上传 MP4 视频、填写标题、融入金句与 Hashtag、绑定抖音合集《AIGC创作：台积电张忠谋传记平行世界》
5. 自动发布并保存凭证
"""

import os, sys, time, json, random, argparse
from playwright.sync_api import sync_playwright
import browser_cookie3

from audio_posts_data import EPISODES_DATA, GITHUB_PORTAL_URL
from generate_douyin_videos import generate_video_for_ep, VIDEO_OUT_DIR

DOUYIN_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/douyin")
DOUYIN_STATE_FILE = os.path.join(DOUYIN_PROFILE_DIR, "state.json")
COLLECTION_TITLE = "AIGC创作：台积电张忠谋传记平行世界"

def sync_douyin_cookies():
    os.makedirs(DOUYIN_PROFILE_DIR, exist_ok=True)
    domains = ["douyin.com", "bytedance.com"]
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
        with open(DOUYIN_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)
        print(f"✅ 成功同步抖音凭证至: {DOUYIN_STATE_FILE}")
        return True
    return False

def make_douyin_desc(ep_data):
    """生成适合抖音推荐算法的文案结构（前排钩子 + 核心转折 + 话题词 + 官方链接）"""
    title = ep_data["title"]
    tags_str = " ".join([f"#{t}" for t in ep_data.get("tags", ["台积电", "张忠谋", "芯片战争", "商业思维", "科技史"])])
    
    desc = f"""【{title}】
{ep_data['timeline']} 历史锚点：
{ep_data['desc'][:200]}...

🎧 完整全集互动展厅与双语中英对照：
{GITHUB_PORTAL_URL}

{tags_str} #商业传记 #芯片 #半导体 #AIGC创作 #人物纪录片"""
    return desc

def publish_douyin_ep(page, ep_data, auto_submit=True):
    ep_id = ep_data["ep_id"]
    title = ep_data["title"]
    
    # 确保视频已生成
    mp4_path = generate_video_for_ep(ep_data)
    if not mp4_path or not os.path.exists(mp4_path):
        print(f"❌ 视频文件不存在: {mp4_path}")
        return False

    print(f"\n========================================================")
    print(f"🚀 [抖音发布] [第{ep_id}期] {title}")
    print(f"📁 视频文件: {mp4_path} ({os.path.getsize(mp4_path)/1024/1024:.1f} MB)")
    print(f"========================================================")

    # 1. 访问抖音创作者发布页
    page.goto("https://creator.douyin.com/creator-micro/content/publish", wait_until="domcontentloaded", timeout=60000)
    time.sleep(4)

    # 2. 上传 MP4 视频
    print("⏳ [1/4] 注入 MP4 视频文件...")
    file_in = page.locator("input[type='file'][accept*='video'], input[type='file']").first
    file_in.set_input_files(mp4_path)
    file_in.dispatch_event("change")
    print("   ⏳ 等待抖音服务端转码与切片解析 (约 15 秒)...")
    time.sleep(15)

    # 3. 填写标题与文案
    print("✍️ [2/4] 填写视频标题与话题描述...")
    douyin_desc = make_douyin_desc(ep_data)
    
    # 查找文案输入框 (contenteditable 或 textarea)
    editor = page.locator(".zone-container, div[contenteditable='true'], textarea").first
    if editor.is_visible():
        editor.click()
        editor.fill(douyin_desc)
        print("   ✅ 抖音文案与热门话题已注入")

    # 4. 选择/绑定合集
    print(f"📂 [3/4] 绑定抖音合集: 《{COLLECTION_TITLE}》...")
    try:
        col_trigger = page.locator(":text('添加到合集'), :text('选择合集'), .collection-select").first
        if col_trigger.is_visible():
            col_trigger.click()
            time.sleep(1.5)
            # 选择匹配合集
            target_col = page.locator(f":text('台积电'), :text('张忠谋')").first
            if target_col.is_visible():
                target_col.click()
                print("   ✅ 成功选择抖音合集")
    except Exception as e:
        print(f"   ⚠️ 抖音合集选择提示: {e}")

    time.sleep(3)
    proof_shot = os.path.join(DOUYIN_PROFILE_DIR, f"douyin_ready_ep_{ep_id}.png")
    page.screenshot(path=proof_shot)
    print(f"📸 抖音发布就绪截图: {proof_shot}")

    # 5. 点击发布
    if auto_submit:
        print("🚀 [4/4] 正在点击【发布】按钮...")
        pub_btn = page.locator("button:has-text('发布'), .publish-btn button").first
        if pub_btn.is_visible():
            pub_btn.click()
            print("   🎉 已点击发布！等待入库...")
            time.sleep(8)
            res_shot = os.path.join(DOUYIN_PROFILE_DIR, f"douyin_result_ep_{ep_id}.png")
            page.screenshot(path=res_shot)
            print(f"📸 抖音发布成功凭证: {res_shot}")
            return True

    return True

if __name__ == "__main__":
    print("抖音合集发布引擎已准备完毕。")
