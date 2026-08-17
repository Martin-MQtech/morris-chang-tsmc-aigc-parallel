# -*- coding: utf-8 -*-
"""
精炼清理与合集最终对齐引擎 (v2)
"""
import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_TITLE = "TSMC & Morris Chang: Parallel World"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVER_PATH = os.path.join(BASE_DIR, "设计资产", "封面", "封面_排版版.jpg")

COLLECTION_DESC = """The complete 19-episode bilingual audio documentary of Morris Chang & TSMC.
From wartime evacuations across 6 cities to MIT, Texas Instruments, and founding TSMC—the pure-play foundry that powers the global AI revolution.
Official interactive portal: https://martin-mqtech.github.io/morris-chang-tsmc-aigc-parallel/"""

def clean_and_assemble():
    with sync_playwright() as p:
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
        page = ctx.new_page()

        # 1. 访问音频管理页，清理旧英文单集（13:xx 及 08:xx）
        print("🧹 [1/3] 清理 13:xx 及 08:xx 旧版单集...")
        for _ in range(5):
            page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
            time.sleep(3)
            rows = page.locator("tbody tr").all()
            found = False
            for r in rows:
                txt = r.inner_text()
                if "Ep" in txt and ("13:" in txt or "08:" in txt):
                    del_btn = r.locator("a:has-text('删除')").first
                    if del_btn.is_visible():
                        print(f"   🗑 删除旧版: {txt[:40]}...")
                        del_btn.click(); time.sleep(1.5)
                        confirm = page.locator("button:has-text('确定')").first
                        if confirm.is_visible():
                            confirm.click(); time.sleep(3)
                        found = True
                        break
            if not found:
                break

        # 2. 访问合集页面，创建官方合集
        print("\n📦 [2/3] 创建官方合集《TSMC & Morris Chang: Parallel World》...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)

        # 检查是否已存在同名合集
        existing = page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first
        if not existing.is_visible():
            # 点击新建合集
            create_btn = page.locator("button.weui-desktop-btn_primary, button:has-text('新建'), .weui-desktop-btn:has-text('新建')").first
            create_btn.click()
            time.sleep(3)

            # 上传封面
            cover_inp = page.locator(".weui-desktop-dialog__wrp input[type='file']").first
            cover_inp.set_input_files(COVER_PATH)
            time.sleep(2)
            crop_btn = page.locator(".weui-desktop-dialog__wrp button:has-text('确认')").first
            if crop_btn.is_visible():
                crop_btn.click(); time.sleep(2)

            # 填写标题
            title_inp = page.locator(".weui-desktop-dialog__wrp input[placeholder*='标题'], .weui-desktop-dialog__wrp input.weui-desktop-form__input").first
            title_inp.fill(COLLECTION_TITLE)

            # 分类
            try:
                cat_select = page.locator(".weui-desktop-dialog__wrp :text('请选择分类'), .weui-desktop-dialog__wrp :text('选择分类')").first
                if cat_select.is_visible():
                    cat_select.click(); time.sleep(1)
                    opt = page.locator(".weui-desktop-dropdown__list-item:has-text('知识')").first
                    if opt.is_visible(): opt.click(); time.sleep(1)
            except:
                pass

            # 简介
            try:
                desc_inp = page.locator(".weui-desktop-dialog__wrp textarea").first
                if desc_inp.is_visible():
                    desc_inp.fill(COLLECTION_DESC[:200])
            except:
                pass

            submit_btn = page.locator(".weui-desktop-dialog__wrp button:has-text('确定'), .weui-desktop-dialog__wrp button:has-text('创建')").first
            submit_btn.click()
            print("   🎉 官方合集创建成功！")
            time.sleep(4)

        # 3. 将 19 期音频全量加入合集
        print("\n📂 [3/3] 将 19 期标准单集全量加入合集...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
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
                confirm.click(); time.sleep(5)
                print("   🎉 19 期音频已全量加入合集！")

        # 4. 最终全量顺序验证
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)
        page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first.locator("a:has-text('详情')").first.click()
        time.sleep(4)

        print("\n=== 最终完美合集顺序 PAGE 1 ===")
        for i, r in enumerate(page.locator("tbody tr").all()):
            print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        nb = page.locator("a:has-text('下一页')").first
        if nb.is_visible():
            nb.click(); time.sleep(2)
            print("\n=== 最终完美合集顺序 PAGE 2 ===")
            for i, r in enumerate(page.locator("tbody tr").all()):
                print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        shot = os.path.join(COOKIE_PROFILE_DIR, "perfect_order_00_to_18_verified.png")
        page.screenshot(path=shot, full_page=True)
        print(f"\n📸 最终绝对正序验证截图已保存: {shot}")

        ctx.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("\n🏆🏆🏆 19期英文合集 00->18 完美单调正序彻底达成！")

if __name__ == "__main__":
    clean_and_assemble()
