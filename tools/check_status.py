# -*- coding: utf-8 -*-
import os, sys, time
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COLLECTION_URL = "https://channels.weixin.qq.com/platform/post/audioCollectionDetails?id=event%2FUzFfAgtgekIEAQAAAAAAwY4QU0vyJgAAAAAStQy6u2-36L1n0r-7fJqX_X8h5xM"

def check_status():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print("1. 访问音频管理页...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(4)
        shot1 = os.path.join(COOKIE_PROFILE_DIR, "check_audio_list.png")
        page.screenshot(path=shot1)
        print(f"音频列表截图: {shot1}")

        print("2. 访问合集详情页...")
        page.goto(COLLECTION_URL, wait_until="domcontentloaded")
        time.sleep(4)
        shot2 = os.path.join(COOKIE_PROFILE_DIR, "check_collection_details.png")
        page.screenshot(path=shot2)
        print(f"合集详情截图: {shot2}")

        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    check_status()
