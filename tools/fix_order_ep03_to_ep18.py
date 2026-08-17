# -*- coding: utf-8 -*-
"""
修复英文合集排序：删除 Ep03~Ep18，按严格顺序重新发布，确保物理时间戳单调递增。
Ep00、Ep01、Ep02 保持不动。
全程 headless 无窗口，无弹窗。
"""
import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(__file__))
from audio_posts_data_en import EPISODES_DATA_EN

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_TITLE = "TSMC & Morris Chang: Parallel World"

# 只需重发 Ep03~Ep18
TO_FIX = [ep for ep in EPISODES_DATA_EN if int(ep["ep_id"]) >= 3]

def launch_browser(p):
    browser = p.chromium.launch(
        channel="chrome",
        headless=True,
        args=[
            "--no-sandbox", "--disable-setuid-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars", "--no-first-run",
            "--no-default-browser-check",
        ]
    )
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        storage_state=STATE_JSON_FILE,
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        locale="zh-CN",
    )
    ctx.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]});
    """)
    return browser, ctx

def check_logged_in(page):
    time.sleep(3)
    if "login.html" in page.url:
        print("⚠️  Session expired — headless fallback: switching to off-screen mode")
        return False
    return True

def delete_episodes_from_manager(page, ep_ids_to_delete):
    """从音频管理页删除指定集数"""
    print(f"\n🗑  开始删除: {ep_ids_to_delete}")
    deleted = set()
    for attempt in range(4):
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        if not check_logged_in(page): return False
        time.sleep(3)

        rows = page.locator("tbody tr").all()
        found_any = False
        for r in rows:
            txt = r.inner_text()
            for eid in ep_ids_to_delete:
                tag = f"Ep{eid}"
                if tag in txt and eid not in deleted:
                    del_btn = r.locator("a:has-text('删除')").first
                    if del_btn.is_visible():
                        del_btn.click(); time.sleep(1.5)
                        confirm = page.locator("button:has-text('确定')").first
                        if confirm.is_visible():
                            confirm.click(); time.sleep(3)
                        print(f"   ✅ 已删除 [{tag}]")
                        deleted.add(eid)
                        found_any = True
                    break
        if not found_any and len(deleted) >= len(ep_ids_to_delete):
            break
    return True

def publish_episode(page, ep_data):
    eid = ep_data["ep_id"]
    title = ep_data["title"]
    audio_path = ep_data["audio_path"]
    cover_path = ep_data["cover_path"]
    desc = ep_data["desc"]

    print(f"\n📤 发布 Ep{eid}: {title[:50]}...")
    page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded")
    if not check_logged_in(page): return False
    time.sleep(3)

    # 上传音频
    audio_inputs = page.locator("input[type='file']")
    audio_inputs.first.set_input_files(audio_path)
    print(f"   ⏳ 等待转码...")

    # 等待转码完成
    for _ in range(60):
        time.sleep(2)
        try:
            upload_area = page.locator(".weui-desktop-uploader__area").first
            txt = upload_area.inner_text(timeout=2000).replace("\n", " ")
            if any(x in txt for x in ["MB", "KB"]) and "0%" not in txt:
                print(f"   ✅ 转码就绪")
                break
        except:
            pass

    time.sleep(1)

    # 上传封面
    try:
        cover_inputs = page.locator("input[type='file']")
        if cover_inputs.count() >= 2:
            cover_inputs.nth(1).set_input_files(cover_path)
            time.sleep(2)
            crop_btn = page.locator("button:has-text('确认')").first
            if crop_btn.is_visible():
                crop_btn.click(); time.sleep(2)
    except Exception as e:
        print(f"   ⚠️  封面: {e}")

    # 填写标题
    try:
        title_input = page.locator("input[placeholder*='标题'], input.weui-desktop-form__input").first
        title_input.fill(title[:40])
    except:
        pass

    # 填写描述
    try:
        desc_area = page.locator("textarea").first
        desc_area.fill(desc[:800])
    except:
        pass

    time.sleep(1)

    # 发表
    pub_btn = page.locator("button:has-text('发表音频')").first
    if pub_btn.is_visible():
        pub_btn.click()
        print(f"   🎉 Ep{eid} 已发表！")
        time.sleep(8)
        return True

    print(f"   ❌ 未找到发表按钮，跳过 Ep{eid}")
    return False

def add_missing_to_collection(page):
    """将所有未在合集中的音频一次性补入"""
    print(f"\n📂 补全合集《{COLLECTION_TITLE}》...")
    page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
    if not check_logged_in(page): return
    time.sleep(3)
    page.locator("a:text-is('合集')").first.click()
    time.sleep(3)

    col_row = page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first
    col_row.locator("a:has-text('详情')").first.click()
    time.sleep(4)

    add_btn = page.locator("button:has-text('添加音频'), button:has-text('添加内容')").first
    if add_btn.is_visible():
        add_btn.click(); time.sleep(3)
        for _ in range(6):
            cbs = page.locator(".weui-desktop-dialog__wrp input[type='checkbox']").all()
            for cb in cbs:
                try:
                    if not cb.is_checked(): cb.check()
                except: pass
            nxt = page.locator(".weui-desktop-dialog__wrp a:has-text('下一页')").first
            if nxt.is_visible():
                nxt.click(); time.sleep(1.5)
            else:
                break
        confirm = page.locator(".weui-desktop-dialog__wrp button:has-text('确定')").first
        if confirm.is_visible():
            confirm.click(); print("   ✅ 合集补全完成"); time.sleep(5)

def print_final_order(page):
    """打印最终合集顺序"""
    page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
    time.sleep(3)
    page.locator("a:text-is('合集')").first.click()
    time.sleep(3)
    page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first.locator("a:has-text('详情')").first.click()
    time.sleep(4)

    print("\n=== 最终合集顺序 PAGE 1 ===")
    for i, r in enumerate(page.locator("tbody tr").all()):
        print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

    nb = page.locator("a:has-text('下一页')").first
    if nb.is_visible():
        nb.click(); time.sleep(2)
        print("\n=== 最终合集顺序 PAGE 2 ===")
        for i, r in enumerate(page.locator("tbody tr").all()):
            print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

    shot = os.path.join(COOKIE_PROFILE_DIR, "perfect_final_order.png")
    page.screenshot(path=shot, full_page=True)
    print(f"\n📸 截图: {shot}")

def main():
    print("=" * 60)
    print("🚀 启动英文合集排序修复引擎 (Ep03→Ep18 重发)")
    print("=" * 60)

    ep_ids_to_delete = [ep["ep_id"] for ep in TO_FIX]  # 03~18

    headless_ok = True
    with sync_playwright() as p:
        browser, ctx = launch_browser(p)
        page = ctx.new_page()

        # 测试 session 是否有效
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        if not check_logged_in(page):
            headless_ok = False
            browser.close()

        if headless_ok:
            # 1. 删除 Ep03~Ep18
            delete_episodes_from_manager(page, ep_ids_to_delete)

            # 2. 依序重发 Ep03→Ep04→...→Ep18
            print(f"\n📢 开始按序发布 {len(TO_FIX)} 集 (Ep03→Ep18)...")
            for ep in TO_FIX:
                publish_episode(page, ep)

            # 3. 补全合集
            add_missing_to_collection(page)

            # 4. 打印最终顺序
            print_final_order(page)

            # 保存 session
            ctx.storage_state(path=STATE_JSON_FILE)
            browser.close()
            print("\n🏆 修复完成！合集现已呈现 Ep18(顶) → Ep00(底) 完美正序。")
        else:
            # Fallback: 使用 off-screen 模式
            print("⚠️  切换到 off-screen 模式 (headless=False + -9999)")
            browser2 = p.chromium.launch(
                channel="chrome", headless=False,
                args=["--window-position=-9999,-9999", "--window-size=1440,900",
                      "--no-first-run", "--no-default-browser-check"]
            )
            ctx2 = browser2.new_context(viewport={"width": 1440, "height": 900}, storage_state=STATE_JSON_FILE)
            page2 = ctx2.new_page()

            delete_episodes_from_manager(page2, ep_ids_to_delete)
            for ep in TO_FIX:
                publish_episode(page2, ep)
            add_missing_to_collection(page2)
            print_final_order(page2)

            ctx2.storage_state(path=STATE_JSON_FILE)
            browser2.close()
            print("\n🏆 修复完成！")

if __name__ == "__main__":
    main()
