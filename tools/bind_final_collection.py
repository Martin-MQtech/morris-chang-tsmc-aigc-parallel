# -*- coding: utf-8 -*-
"""
合集快速绑定与验证
"""
import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_TITLE = "TSMC & Morris Chang: Parallel World"

def bind_collection():
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

        # 打开音频管理 -> 合集
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)

        # 检查是否已有该合集
        col_row = page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first
        if col_row.is_visible():
            print(f"✅ 找到合集: {COLLECTION_TITLE}")
            col_row.locator("a:has-text('详情')").first.click()
            time.sleep(4)
        else:
            print("🔍 查找创建入口...")
            # 点击任何包含新建文本的按钮
            page.evaluate("""() => {
                const elements = Array.from(document.querySelectorAll('button, a'));
                const btn = elements.find(el => el.textContent.includes('新建') && el.offsetParent !== null);
                if (btn) btn.click();
            }""")
            time.sleep(3)

            # 填写表单
            title_input = page.locator(".weui-desktop-dialog__wrp input[placeholder*='标题'], .weui-desktop-dialog__wrp input.weui-desktop-form__input").first
            if title_input.is_visible():
                title_input.fill(COLLECTION_TITLE)
                time.sleep(1)
                submit_btn = page.locator(".weui-desktop-dialog__wrp button:has-text('确定')").first
                if submit_btn.is_visible():
                    submit_btn.click()
                    time.sleep(4)

            # 进入详情
            col_row = page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first
            col_row.locator("a:has-text('详情')").first.click()
            time.sleep(4)

        # 添加音频
        add_btn = page.locator("button:has-text('添加音频'), button:has-text('添加内容')").first
        if add_btn.is_visible():
            add_btn.click(); time.sleep(3)
            for _ in range(5):
                cbs = page.locator(".weui-desktop-dialog__wrp input[type='checkbox']").all()
                for cb in cbs:
                    try:
                        if not cb.is_checked(): cb.check()
                    except: pass
                nxt = page.locator(".weui-desktop-dialog__wrp a:has-text('下一页')").first
                if nxt.is_visible() and not nxt.get_attribute("class").find("disabled") != -1:
                    nxt.click(); time.sleep(1.5)
                else:
                    break
            confirm = page.locator(".weui-desktop-dialog__wrp button:has-text('确定')").first
            if confirm.is_visible():
                confirm.click(); time.sleep(5)
                print("🎉 音频录入完成！")

        # 验证输出
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)
        page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first.locator("a:has-text('详情')").first.click()
        time.sleep(4)

        print("\n=== 合集最终排序 PAGE 1 ===")
        for i, r in enumerate(page.locator("tbody tr").all()):
            print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        nb = page.locator("a:has-text('下一页')").first
        if nb.is_visible():
            nb.click(); time.sleep(2)
            print("\n=== 合集最终排序 PAGE 2 ===")
            for i, r in enumerate(page.locator("tbody tr").all()):
                print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        shot = os.path.join(COOKIE_PROFILE_DIR, "final_verified_order_locked.png")
        page.screenshot(path=shot, full_page=True)
        print(f"\n📸 最终截图: {shot}")

        ctx.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    bind_collection()
