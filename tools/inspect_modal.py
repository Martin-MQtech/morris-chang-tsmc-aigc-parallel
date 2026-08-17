# -*- coding: utf-8 -*-
import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_URL = "https://channels.weixin.qq.com/platform/post/audioCollectionDetails?id=event%2FUzFfAgtgekIEAQAAAAAAwY4QU0vyJgAAAAAStQy6u2-36L1n0r-7fJqX_X8h5xM"

def inspect_modal():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print(f"1. 直接访问合集详情页: {COLLECTION_URL}")
        page.goto(COLLECTION_URL, wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)

        print("2. 点击【添加音频】按钮...")
        btn = page.locator("button:has-text('添加音频')").first
        if btn.is_visible():
            btn.click()
            time.sleep(3)
        else:
            print("未找到添加音频按钮，打印页面文本:")
            print(page.locator("body").inner_text()[:400])

        shot = os.path.join(COOKIE_PROFILE_DIR, "modal_add_audio.png")
        page.screenshot(path=shot)
        print(f"截图留存: {shot}")

        # 检查模态框内的所有 input / button / textarea / contenteditable
        inputs = page.locator("input").all()
        print(f"找到 input 元素共 {len(inputs)} 个:")
        for idx, inp in enumerate(inputs):
            try:
                print(f"  [{idx}] type={inp.get_attribute('type')} accept={inp.get_attribute('accept')} placeholder={inp.get_attribute('placeholder')}")
            except Exception:
                pass

        buttons = page.locator("button").all_inner_texts()
        print("可见按钮:", [b.strip() for b in buttons if b.strip()])

        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    inspect_modal()
