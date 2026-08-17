# -*- coding: utf-8 -*-
import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def inspect_uploader_dom():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded")
        time.sleep(3)

        # 打印上传区域 HTML
        html = page.locator(".weui-desktop-form__control-group").first.evaluate("el => el.outerHTML")
        print("Upload Group HTML:")
        print(html)

        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    inspect_uploader_dom()
