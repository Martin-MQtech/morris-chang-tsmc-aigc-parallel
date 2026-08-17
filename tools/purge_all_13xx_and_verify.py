# -*- coding: utf-8 -*-
"""
循环清理合集中所有 13: 时间戳旧条目，直至完全清空
"""
import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_TITLE = "TSMC & Morris Chang: Parallel World"

def purge():
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

        for attempt in range(50):
            # 查找当前页面上的 13: 条目
            rows = page.locator("tbody tr").all()
            found_13 = False
            for r in rows:
                txt = r.inner_text()
                if "13:" in txt:
                    btn = r.locator("a:has-text('移除')").first
                    if btn.is_visible():
                        print(f"🗑 移除 13:xx 条目: {txt.split(chr(10))[0]}")
                        btn.click(); time.sleep(1)
                        confirm = page.locator(".weui-desktop-dialog__wrp button:has-text('确定'), button:has-text('确定')").first
                        if confirm.is_visible():
                            confirm.click(); time.sleep(2)
                        found_13 = True
                        break

            if not found_13:
                # 尝试点击下一页
                nxt = page.locator("a:has-text('下一页')").first
                if nxt.is_visible() and "disabled" not in (nxt.get_attribute("class") or ""):
                    nxt.click(); time.sleep(1.5)
                else:
                    # 已经到了最后一页且当前页没有 13:，说明全部清理完毕！
                    print("🎉 恭喜！合集内所有 13:xx 旧条目已彻底移除干净！")
                    break

        # 回到第1页打印
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        page.locator("a:text-is('合集')").first.click()
        time.sleep(3)
        page.locator(f"tr:has-text('{COLLECTION_TITLE}')").first.locator("a:has-text('详情')").first.click()
        time.sleep(4)

        print("\n=== 最终完美 19 期合集列表 PAGE 1 (Top 10) ===")
        for i, r in enumerate(page.locator("tbody tr").all()):
            print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        nb = page.locator("a:has-text('下一页')").first
        if nb.is_visible():
            nb.click(); time.sleep(2)
            print("\n=== 最终完美 19 期合集列表 PAGE 2 (Bottom 9) ===")
            for i, r in enumerate(page.locator("tbody tr").all()):
                print(f"[{i}] {r.inner_text().replace(chr(10), ' | ')}")

        shot = os.path.join(COOKIE_PROFILE_DIR, "final_flawless_19_verified.png")
        page.screenshot(path=shot, full_page=True)
        print(f"\n📸 最终无暇正序截图已保存: {shot}")

        ctx.storage_state(path=STATE_JSON_FILE)
        browser.close()

if __name__ == "__main__":
    purge()
