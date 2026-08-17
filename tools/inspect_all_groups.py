# -*- coding: utf-8 -*-
import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def inspect_all_groups():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded")
        time.sleep(3)

        groups = page.locator(".weui-desktop-form__control-group").all()
        print(f"Total control groups: {len(groups)}")
        for idx, g in enumerate(groups):
            print(f"\n--- Group [{idx}] ---")
            print(g.evaluate("el => el.outerHTML")[:600])

        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    inspect_all_groups()
