# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_TITLE = "TSMC & Morris Chang: Parallel World"

def inspect_remove():
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

        # 找到第1个 13: 按钮
        rows = page.locator("tbody tr").all()
        for r in rows:
            txt = r.inner_text()
            if "13:" in txt:
                print(f"Target row: {txt}")
                btn = r.locator("a:has-text('移除')").first
                btn.click()
                time.sleep(2)
                dialog = page.locator(".weui-desktop-dialog, .weui-desktop-dialog__wrp").first
                if dialog.is_visible():
                    print("Dialog html:", dialog.inner_html())
                    buttons = dialog.locator("button").all()
                    for b in buttons:
                        print("Dialog button:", b.inner_text())
                        if "确定" in b.inner_text() or "移除" in b.inner_text() or "确认" in b.inner_text():
                            b.click()
                            print("Clicked confirm button!")
                            time.sleep(2)
                            break
                break
        browser.close()

if __name__ == "__main__":
    inspect_remove()
