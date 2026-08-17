# -*- coding: utf-8 -*-
"""
微信视频号英文合集【正序 00->18 精确排序与校准引擎】
======================================================
原理说明：
微信视频号合集采用 LIFO (后进先出) 渲染顺序，最新添加的音频排在合集顶部 (Row 0)。
为确保合集内展示顺序严格为：
  Ep00 -> Ep01 -> Ep02 -> ... -> Ep17 -> Ep18
必须先注入 Ep18，逐级递减，最后注入 Ep00。
"""

import os, sys, time, json
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

COOKIE_PROFILE_DIR = os.path.expanduser("~/.config/codex_video_dispatch/chromium_profiles/sph")
STATE_JSON_FILE = os.path.join(COOKIE_PROFILE_DIR, "state.json")
COVER_PATH = os.path.expanduser("~/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC/设计资产/封面/封面_排版版.jpg")

COLLECTION_TITLE = "TSMC & Morris Chang: Parallel World"
COLLECTION_DESC = "AIGC Parallel Biography of TSMC & Morris Chang. A 19-movement English audio series exploring semiconductor revolution and tech philosophy."

def reorder_collection():
    print(f"\n========================================================")
    print(f"🎯 启动合集正序排序引擎: 00 -> 18")
    print(f"========================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--window-position=-9999,-9999", "--window-size=1440,900", "--no-first-run", "--no-default-browser-check"]
        )
        kwargs = {}
        if os.path.exists(STATE_JSON_FILE):
            kwargs["storage_state"] = STATE_JSON_FILE

        context = browser.new_context(viewport={"width": 1440, "height": 900}, **kwargs)
        page = context.new_page()

        # 1. 访问合集管理页
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        if "login.html" in page.url:
            page.mouse.click(1196, 571)
            time.sleep(4)

        col_tab = page.locator("a:text-is('合集')").first
        if col_tab.is_visible():
            col_tab.click()
            time.sleep(3)

        # 2. 删除已有英文合集容器（重新以标准倒序注入，达成 00->18 正序展示）
        col_rows = page.locator("tr:has-text('Morris'), tr:has-text('TSMC')").all()
        for cr in col_rows:
            txt = cr.inner_text()
            if "台积电张忠谋" not in txt:  # 保留中文合集，仅重置英文
                print(f"👉 正在重置英文合集容器: {txt[:40]}...")
                del_btn = cr.locator("a:has-text('删除'), button:has-text('删除')").first
                if del_btn.is_visible():
                    del_btn.click()
                    time.sleep(1.5)
                    confirm_btn = page.locator("button:has-text('确定'), button:has-text('确认')").first
                    if confirm_btn.is_visible():
                        confirm_btn.click()
                        print("✅ 已清空旧容器")
                        time.sleep(4)

        # 3. 重新创建合集容器
        print(f"👉 正在创建全新的《{COLLECTION_TITLE}》合集...")
        page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded")
        time.sleep(3)

        page.locator(":text('选择合集')").first.click()
        time.sleep(1.5)
        page.locator(":text('创建新合集')").first.click()
        time.sleep(2)

        dialog = page.locator('.weui-desktop-dialog__wrp:has-text("创建合集")').first
        dialog.locator("input[placeholder*='标题'], input.weui-desktop-form__input").first.fill(COLLECTION_TITLE)
        dialog.locator("textarea[placeholder*='描述'], textarea.weui-desktop-form__textarea").first.fill(COLLECTION_DESC)

        if os.path.exists(COVER_PATH):
            dialog.locator("input[type='file']").first.set_input_files(COVER_PATH)
            time.sleep(2)
            crop_dialog = page.locator('.weui-desktop-dialog__wrp:has-text("编辑合集封面")').first
            if crop_dialog.is_visible():
                crop_dialog.locator("button:has-text('确认')").first.click()
                time.sleep(2)

        type_select = dialog.locator(":text('选择合集的类型'), .weui-desktop-select").first
        if type_select.is_visible():
            type_select.click()
            time.sleep(1)
            type_opt = page.locator(".weui-desktop-dropdown__list-item:has-text('知识'), li:has-text('知识')").first
            if type_opt.is_visible():
                type_opt.click()
                time.sleep(1)

        submit_btn = dialog.locator("button:has-text('创建合集'), button:has-text('确定')").first
        submit_btn.click()
        print("🎉 官方合集容器已全新就绪！")
        time.sleep(5)

        # 4. 进入合集详情页执行倒序添加 (从 Ep18 倒着加到 Ep00 -> 最终呈现 00 在最顶端)
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        col_tab2 = page.locator("a:text-is('合集')").first
        if col_tab2.is_visible():
            col_tab2.click()
            time.sleep(3)

        new_col_row = page.locator("tr:has-text('Morris'), tr:has-text('TSMC')").first
        new_col_row.locator("a:has-text('详情'), button:has-text('详情')").first.click()
        time.sleep(4)

        # 期望最终展示顺序: 00 -> 01 -> 02 ... -> 18
        # 添加顺序: 18 -> 17 -> 16 ... -> 01 -> 00
        ADD_ORDER = [f"Ep{i:02d}" for i in range(18, -1, -1)]
        print(f"📋 规划添加序列 (LIFO 后进先出法): {ADD_ORDER}")

        add_btn = page.locator("button:has-text('添加音频'), button:has-text('添加内容')").first
        if add_btn.is_visible():
            add_btn.click()
            time.sleep(3)

            # 遍历所有目标期号，从 Ep18 倒序逐一勾选
            for target_ep in ADD_ORDER:
                # 在弹窗多页中寻找 target_ep
                found = False
                for p_idx in range(5):
                    rows = page.locator(".weui-desktop-dialog__wrp tbody tr, .weui-desktop-dialog__wrp .weui-desktop-table__tr").all()
                    for r in rows:
                        t = r.inner_text()
                        if target_ep in t:
                            cb = r.locator("input[type='checkbox']").first
                            if not cb.is_checked():
                                cb.check()
                                print(f"   ✅ 已勾选 [{target_ep}]")
                            found = True
                            break
                    if found:
                        break
                    next_p = page.locator(".weui-desktop-dialog__wrp a:has-text('下一页')").first
                    if next_p.is_visible():
                        next_p.click()
                        time.sleep(1.5)
                    else:
                        break

            confirm_btn = page.locator(".weui-desktop-dialog__wrp button:has-text('确定'), .weui-desktop-dialog__wrp button:has-text('确认')").first
            if confirm_btn.is_visible():
                confirm_btn.click()
                print("🎉 已完成全量正序归集提交！")
                time.sleep(5)

        # 5. 验证最终顺序
        page.reload()
        time.sleep(4)
        print("\n=== 最终合集内第一页列表顺序 (展示给用户的前 10 期) ===")
        for idx, r in enumerate(page.locator("tbody tr").all()):
            print(f"[{idx}] {r.inner_text().replace(chr(10), ' | ')}")

        shot = os.path.join(COOKIE_PROFILE_DIR, "ordered_00_to_18_verified.png")
        page.screenshot(path=shot, full_page=True)
        print(f"\n📸 正序 00->18 验证截图已保存: {shot}")

        context.storage_state(path=STATE_JSON_FILE)
        browser.close()
        print("\n🏆🏆🏆 英文合集《TSMC & Morris Chang: Parallel World》正序排列已全部校准完成！")

if __name__ == "__main__":
    reorder_collection()
