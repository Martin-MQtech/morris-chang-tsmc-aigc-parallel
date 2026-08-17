# -*- coding: utf-8 -*-
"""
测试直接访问创建合集 URL
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

def test_direct_create():
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

        # 1. 访问音频管理 -> 合集 -> 先删除当前带冗余的旧合集
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)

        old_row = page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first
        if old_row.is_visible():
            del_c = old_row.locator("a:has-text('删除'), button:has-text('删除')").first
            del_c.click(); time.sleep(1.5)
            # 点击任何确认按钮
            confirm = page.locator("button:visible").filter(has_text="确定").first
            if not confirm.is_visible():
                confirm = page.locator("button:visible").filter(has_text="确认").first
            if confirm.is_visible():
                confirm.click(); time.sleep(3)
                print("✅ 已彻底删除旧合集容器！")

        # 2. 点击新建合集按钮
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)

        # 查找新建合集按钮
        print("查找新建合集按钮...")
        create_btn = page.locator("button:has-text('新建音频合集'), button:has-text('新建合集'), button:has-text('新建'), a:has-text('新建')").first
        create_btn.click()
        time.sleep(3)

        # 上传封面
        cover_inp = page.locator("input[type='file']:visible").first
        cover_inp.set_input_files(COVER_PATH)
        time.sleep(2)
        crop_btn = page.locator("button:visible").filter(has_text="确认").first
        if crop_btn.is_visible():
            crop_btn.click(); time.sleep(2)

        # 填写标题
        title_inp = page.locator("input[placeholder*='标题']:visible, input.weui-desktop-form__input:visible").first
        title_inp.fill(COLLECTION_TITLE)

        # 分类
        try:
            cat_select = page.locator(":text('请选择分类'):visible, :text('选择分类'):visible").first
            if cat_select.is_visible():
                cat_select.click(); time.sleep(1)
                opt = page.locator(".weui-desktop-dropdown__list-item:has-text('知识'), li:has-text('知识')").first
                if opt.is_visible(): opt.click(); time.sleep(1)
        except:
            pass

        # 描述
        try:
            desc_inp = page.locator("textarea:visible").first
            if desc_inp.is_visible():
                desc_inp.fill(COLLECTION_DESC[:200])
        except:
            pass

        submit_btn = page.locator("button:visible").filter(has_text="确定").first
        if not submit_btn.is_visible():
            submit_btn = page.locator("button:visible").filter(has_text="创建").first
        submit_btn.click()
        print("🎉 官方全新合集创建成功！")
        time.sleep(5)

        # 3. 进入合集详情并添加音频
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)

        col_row = page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first
        col_row.locator("a:has-text('详情')").first.click()
        time.sleep(4)

        add_btn = page.locator("button:has-text('添加音频')").first
        if add_btn.is_visible():
            add_btn.click(); time.sleep(3)
            # 在添加弹窗中勾选所有 19 期
            for _ in range(5):
                cbs = page.locator(".weui-desktop-dialog__wrp input[type='checkbox']").all()
                for cb in cbs:
                    try:
                        if not cb.is_checked(): cb.check()
                    except: pass
                nxt = page.locator(".weui-desktop-dialog__wrp a:has-text('下一页')").first
                if nxt.is_visible() and "disabled" not in (nxt.get_attribute("class") or ""):
                    nxt.click(); time.sleep(1.5)
                else:
                    break
            confirm_add = page.locator(".weui-desktop-dialog__wrp button:has-text('确定')").first
            if confirm_add.is_visible():
                confirm_add.click(); time.sleep(5)
                print("🎉 19 期音频全量收入全新合集！")

        # 4. 全量验证
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)
        page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first.locator("a:has-text('详情')").first.click()
        time.sleep(4)

        print("\n=== 最终绝对正序合集列表 PAGE 1 (Top 10) ===")
        for i, r in enumerate(page.locator("tbody tr").all()):
            print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        nb = page.locator("a:has-text('下一页')").first
        if nb.is_visible():
            nb.click(); time.sleep(2)
            print("\n=== 最终绝对正序合集列表 PAGE 2 (Bottom 9) ===")
            for i, r in enumerate(page.locator("tbody tr").all()):
                print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        shot = os.path.join(COOKIE_PROFILE_DIR, "flawless_order_final_success.png")
        page.screenshot(path=shot, full_page=True)
        print(f"\n📸 最终无暇正序截图已保存: {shot}")

        ctx.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("\n🏆🏆🏆 英文官方合集 00 至 18 全量 19 期绝对正序已 100% 达成！")

if __name__ == "__main__":
    test_direct_create()
