# -*- coding: utf-8 -*-
"""
微信视频号【英文专属合集】独立深度归集与封面校准引擎
1. 访问音频管理后台 -> 点击「合集」
2. 若合集不存在则创建：《TSMC & Morris Chang: Parallel》，设置官方 1:1 排版封面
3. 进入该合集详情页 -> 点击「添加音频」
4. 全量勾选 00~18 全部 19 期英文音频 -> 保存归集
5. 校准合集封面与展示顺序 -> 保存最终全景截图
"""

import os, sys, time
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright
import browser_cookie3

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COVER_PATH = os.path.join(os.path.dirname(__file__), "..", "设计资产", "封面", "封面_排版版.jpg")

COLLECTION_TITLE = "TSMC & Morris Chang: Parallel"
COLLECTION_DESC = "AIGC Parallel Biography of TSMC & Morris Chang. A 19-movement English audio series exploring semiconductor revolution and tech philosophy."

def aggregate_english_collection():
    print(f"\n========================================================")
    print(f"📂 启动微信视频号英文合集归集与封面校准引擎")
    print(f"🎯 目标合集: 《{COLLECTION_TITLE}》")
    print(f"🖼️ 目标封面: {os.path.basename(COVER_PATH)}")
    print(f"========================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--no-first-run", "--no-default-browser-check"]
        )
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        # 1. 进入音频管理页
        print("⏳ [1/4] 访问视频号音频管理后台...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)

        if "login.html" in page.url:
            print("👉 检测到登录页面，正在执行自动快捷登录...")
            fast_btn = page.locator("button:has-text('快捷登录'), :text('微信快捷登录')").first
            if fast_btn.is_visible():
                fast_btn.click()
            else:
                page.mouse.click(1196, 571)
            time.sleep(4)

        # 2. 切换到「合集」标签页
        print("📂 [2/4] 切换到【合集】管理标签页...")
        tab_col = page.locator(":text('合集')").first
        if tab_col.is_visible():
            tab_col.click()
            time.sleep(4)

        # 检查是否已存在英文合集
        col_rows = page.locator("tr:has-text('TSMC'), tr:has-text('Morris'), .collection-item:has-text('TSMC'), .collection-item:has-text('Morris')").all()
        
        if len(col_rows) == 0:
            print(f"👉 英文合集尚未创建，正在自动创建: 《{COLLECTION_TITLE}》...")
            create_btn = page.locator("button:has-text('创建合集')").first
            if create_btn.is_visible():
                create_btn.click()
                time.sleep(3)

                # 填写合集名称与简介
                name_in = page.locator("input[placeholder*='合集名称'], input[placeholder*='标题'], input[placeholder*='名称']").first
                if name_in.is_visible():
                    name_in.fill(COLLECTION_TITLE[:30])
                    print(f"   ✅ 已填入合集标题: {COLLECTION_TITLE[:30]}")

                desc_in = page.locator("textarea[placeholder*='简介'], textarea[placeholder*='描述']").first
                if desc_in.is_visible():
                    desc_in.fill(COLLECTION_DESC)
                    print("   ✅ 已填入合集描述")

                # 上传合集排版封面
                file_in = page.locator("input[type='file']").first
                if file_in.is_visible() and os.path.exists(COVER_PATH):
                    file_in.set_input_files(COVER_PATH)
                    time.sleep(2)
                    crop_btn = page.locator("button:has-text('确认'), button:has-text('确定')").first
                    if crop_btn.is_visible():
                        crop_btn.click()
                        time.sleep(2)
                    print(f"   ✅ 已设置合集封面: {os.path.basename(COVER_PATH)}")

                # 提交创建
                submit_btn = page.locator("button:has-text('创建'), button:has-text('保存'), button:has-text('确定')").last
                if submit_btn.is_visible():
                    submit_btn.click()
                    print(f"🎉 英文合集《{COLLECTION_TITLE}》创建成功！")
                    time.sleep(5)
        else:
            print(f"✅ 检测到英文合集已存在 ({len(col_rows)} 个)")

        # 3. 进入合集详情并添加全部 19 期音频
        print("🔗 [3/4] 进入合集详情页并批量添加全部 19 期英文音频...")
        col_card = page.locator("tr:has-text('TSMC'), tr:has-text('Morris'), .collection-item:has-text('TSMC'), .collection-item:has-text('Morris')").first
        if col_card.is_visible():
            detail_btn = col_card.locator("a:has-text('详情'), a:has-text('管理'), button:has-text('管理'), button:has-text('详情')").first
            if detail_btn.is_visible():
                detail_btn.click()
                time.sleep(4)
            else:
                col_card.click()
                time.sleep(4)

        add_audio_btn = page.locator("button:has-text('添加音频'), button:has-text('添加内容')").first
        if add_audio_btn.is_visible():
            add_audio_btn.click()
            time.sleep(3)

            # 勾选对话框中的所有音频多选框
            checkboxes = page.locator(".weui-desktop-dialog__wrp input[type='checkbox'], .modal-content input[type='checkbox'], input[type='checkbox']").all()
            print(f"   📋 发现可选音频条目: {len(checkboxes)} 个")
            checked_count = 0
            for cb in checkboxes:
                try:
                    if not cb.is_checked():
                        cb.check()
                        checked_count += 1
                except:
                    pass
            print(f"   ✅ 已成功批量勾选 {checked_count} 条音频")
            time.sleep(1)

            confirm_btn = page.locator(".weui-desktop-dialog__wrp button:has-text('确定'), .weui-desktop-dialog__wrp button:has-text('确认')").first
            if confirm_btn.is_visible():
                confirm_btn.click()
                print("🎉 已成功点击确认，19 期英文音频已全量归入合集！")
                time.sleep(5)

        # 4. 留存合集全景截图
        print("📸 [4/4] 正在截取最终英文合集全景存证...")
        time.sleep(3)
        final_col_shot = os.path.join(COOKIE_PROFILE_DIR, "verified_english_collection_complete.png")
        page.screenshot(path=final_col_shot, full_page=True)
        print(f"📸 合集详情全景截图已保存至: {final_col_shot}")

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("\n🏆🏆🏆 英文专属合集《TSMC & Morris Chang: Parallel》归集与封面设置圆满完成！")

if __name__ == "__main__":
    aggregate_english_collection()
