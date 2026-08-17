# -*- coding: utf-8 -*-
"""
精准移除合集中带 13: 时间戳的历史冗余项
"""
import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_TITLE = "TSMC & Morris Chang: Parallel World"

def remove_13xx():
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

        for attempt in range(20):
            # 翻到最后一页找 13:
            found_13 = False
            for p_num in range(4):
                rows = page.locator("tbody tr").all()
                for r in rows:
                    txt = r.inner_text()
                    if "13:" in txt:
                        btn = r.locator("a:has-text('移除')").first
                        if btn.is_visible():
                            print(f"🗑 移除 13:xx 项: {txt.split(chr(10))[0]}")
                            btn.click(); time.sleep(1)
                            confirm = page.locator("button:has-text('确定')").first
                            if confirm.is_visible():
                                confirm.click(); time.sleep(2)
                            found_13 = True
                            break
                if found_13:
                    break
                nxt = page.locator("a:has-text('下一页')").first
                if nxt.is_visible() and not nxt.get_attribute("class").find("disabled") != -1:
                    nxt.click(); time.sleep(1.5)
                else:
                    break

            if not found_13:
                print("✅ 所有 13:xx 历史项已全部移出合集！")
                break

        # 检查是否包含 Ep00, Ep01, Ep02
        add_btn = page.locator("button:has-text('添加音频')").first
        if add_btn.is_visible():
            add_btn.click(); time.sleep(2.5)
            cbs = page.locator(".weui-desktop-dialog__wrp input[type='checkbox']").all()
            for cb in cbs:
                try:
                    if not cb.is_checked(): cb.check()
                except: pass
            confirm = page.locator(".weui-desktop-dialog__wrp button:has-text('确定')").first
            if confirm.is_visible():
                confirm.click(); time.sleep(4)

        # 最终验证
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)
        page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first.locator("a:has-text('详情')").first.click()
        time.sleep(4)

        print("\n=== 最终绝对正序合集 PAGE 1 ===")
        for i, r in enumerate(page.locator("tbody tr").all()):
            print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        nb = page.locator("a:has-text('下一页')").first
        if nb.is_visible():
            nb.click(); time.sleep(2)
            print("\n=== 最终绝对正序合集 PAGE 2 ===")
            for i, r in enumerate(page.locator("tbody tr").all()):
                print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        shot = os.path.join(COOKIE_PROFILE_DIR, "final_flawless_order.png")
        page.screenshot(path=shot, full_page=True)
        print(f"\n📸 最终截图已保存: {shot}")

        ctx.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    remove_13xx()
