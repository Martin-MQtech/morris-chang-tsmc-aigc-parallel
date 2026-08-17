# -*- coding: utf-8 -*-
"""
收官总巡检：同步最新 Cookie 并截取音频列表与合集详情全景
"""

import os, sys, time, json
from playwright.sync_api import sync_playwright
import browser_cookie3

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")

def sync_wechat_cookies():
    os.makedirs(COOKIE_PROFILE_DIR, exist_ok=True)
    domains = ["weixin.qq.com", "qq.com"]
    all_cookies = []
    for domain in domains:
        try:
            cj = browser_cookie3.chrome(domain_name=domain)
            for c in cj:
                all_cookies.append({
                    "name": str(c.name),
                    "value": str(c.value),
                    "domain": str(c.domain),
                    "path": str(c.path),
                    "expires": float(c.expires) if c.expires else -1.0,
                    "httpOnly": False,
                    "secure": bool(c.secure),
                    "sameSite": "Lax"
                })
        except Exception:
            pass
            
    if all_cookies:
        state_data = {"cookies": all_cookies, "origins": []}
        with open(STATE_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)
        return True
    return False

def capture_verified():
    sync_wechat_cookies()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        print("1. 截取音频管理列表最终状态...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(5)
        shot1 = os.path.join(COOKIE_PROFILE_DIR, "verified_final_audio_list.png")
        page.screenshot(path=shot1)
        print(f"📸 最终音频列表截图: {shot1}")

        print("2. 截取合集列表最终状态...")
        tab_col = page.locator(":text('合集')").first
        if tab_col.is_visible():
            tab_col.click()
            time.sleep(3)
            shot2 = os.path.join(COOKIE_PROFILE_DIR, "verified_final_collection_tab.png")
            page.screenshot(path=shot2)
            print(f"📸 最终合集标签页截图: {shot2}")

        browser.close()

if __name__ == "__main__":
    capture_verified()
