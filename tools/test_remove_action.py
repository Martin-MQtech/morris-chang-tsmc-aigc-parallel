# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_TITLE = "TSMC & Morris Chang: Parallel World"

def test_remove_action():
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

        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)

        col_row = page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first
        col_row.locator("a:has-text('详情')").first.click()
        time.sleep(4)

        # 翻到第2页
        nxt = page.locator("a:has-text('下一页')").first
        if nxt.is_visible():
            nxt.click(); time.sleep(2)

        print("Before click rows count:", len(page.locator("tbody tr").all()))
        target_row = page.locator("tbody tr:has-text('13:30')").first
        if target_row.is_visible():
            print("Found target row 13:30!")
            # 监听所有弹窗或 dialog
            btn = target_row.locator("a:has-text('移除')").first
            btn.click()
            time.sleep(1.5)

            # 看看是否有任何弹窗或确认按钮出现
            body_text = page.locator("body").inner_text()
            print("Visible dialogs/modals on page:")
            for m in page.locator(".weui-desktop-dialog, .weui-desktop-popover, .weui-desktop-modal, [role='dialog']").all():
                print("Modal text:", m.inner_text())
                # 尝试点击里面的确认/确定按钮
                for b in m.locator("button, a").all():
                    if any(w in b.inner_text() for w in ["确定", "确认", "移除"]):
                        print("Clicking modal button:", b.inner_text())
                        b.click()
                        time.sleep(2)
                        break

            time.sleep(2)
            page.reload()
            time.sleep(3)
            # 重新翻到第2页看看
            nxt2 = page.locator("a:has-text('下一页')").first
            if nxt2.is_visible():
                nxt2.click(); time.sleep(2)
            print("After remove & reload, page 2 rows:")
            for i, r in enumerate(page.locator("tbody tr").all()):
                print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        browser.close()

if __name__ == "__main__":
    test_remove_action()
