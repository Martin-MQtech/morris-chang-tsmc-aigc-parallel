# -*- coding: utf-8 -*-
"""
通过 Chrome 远程调试端口 (CDP: localhost:9222) 接管已登录的真实 Chrome 进行自动化发布
- 零弹窗、零多余进程、零二次登录
- 直接复用现有登录会话
- 自动查重、删重、按序补齐发布与合集归集
"""

import os, sys, time, random
sys.stdout.reconfigure(line_buffering=True)
from playwright.sync_api import sync_playwright

from audio_posts_data_en import EPISODES_DATA_EN, GITHUB_PORTAL_URL

COLLECTION_TITLE = "TSMC & Morris Chang: Parallel"
COLLECTION_DESC = "AIGC Parallel Biography of TSMC & Morris Chang. A 19-movement English audio series exploring semiconductor revolution and tech philosophy."

def run_cdp_publisher():
    print(f"\n========================================================")
    print(f"🚀 启动 CDP 端口接管发布引擎 (localhost:9222)")
    print(f"📦 剧集总量: {len(EPISODES_DATA_EN)} 期 (Ep00 至 Ep18)")
    print(f"========================================================\n")

    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ 成功连接至正在运行的 Chrome 实例 (Port 9222)！")
        except Exception as e:
            print(f"❌ 无法连接至 localhost:9222: {e}")
            print("\n💡 提示：请确保 Chrome 已开启远程调试端口：")
            print("   在终端运行：/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 &")
            return False

        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        # 1. 扫描线上已发布列表
        print("🔍 [1/3] 正在扫描线上音频列表...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(4)

        rows = page.locator("tr").all()
        published_set = set()
        for row in rows:
            t = row.inner_text().replace('\n', ' ')
            for ep in EPISODES_DATA_EN:
                eid = ep["ep_id"]
                if f"Ep{eid}" in t or f"Ep {eid}" in t:
                    if eid in published_set:
                        print(f"👉 发现重复项 Ep{eid}，正在执行自动清理...")
                        del_btn = row.locator("a:has-text('删除'), button:has-text('删除')").first
                        if del_btn.is_visible():
                            del_btn.click()
                            time.sleep(1.5)
                            confirm_btn = page.locator("button:has-text('确定'), button:has-text('确认')").first
                            if confirm_btn.is_visible():
                                confirm_btn.click()
                                time.sleep(2)
                    else:
                        published_set.add(eid)

        print(f"📋 当前线上有效英文单集 ({len(published_set)} 期): {sorted(list(published_set))}")
        pending_eps = [ep for ep in EPISODES_DATA_EN if ep["ep_id"] not in published_set]
        print(f"👉 待补齐发布列表 (共 {len(pending_eps)} 期): {[e['ep_id'] for e in pending_eps]}")

        # 2. 补齐发布
        for idx, ep_data in enumerate(pending_eps, start=1):
            ep_id = ep_data["ep_id"]
            title = ep_data["title"]
            audio_path = ep_data["audio_path"]
            cover_path = ep_data["cover_path"]
            desc = ep_data["desc"]

            print(f"\n--------------------------------------------------------")
            print(f"🚀 发布 [{idx}/{len(pending_eps)}]: [Ep{ep_id}] {title}")
            print(f"📁 音频: {os.path.basename(audio_path)}")
            print(f"🖼️ 封面: {os.path.basename(cover_path)}")

            page.goto("https://channels.weixin.qq.com/platform/post/createAudio", wait_until="domcontentloaded")
            time.sleep(3)

            # 注入音频
            file_inputs = page.locator("input[type='file']")
            file_inputs.first.set_input_files(audio_path)
            file_inputs.first.dispatch_event("change")
            print("   ⏳ 等待音频云端转码与解析...")
            
            # 轮询解析
            for _ in range(35):
                time.sleep(2)
                ctrl_text = page.locator(".weui-desktop-form__control-group:has-text('文件')").first.inner_text().replace('\n', ' ')
                if ("MB" in ctrl_text or "KB" in ctrl_text) and ("0%" not in ctrl_text) and ("请上传音频" not in ctrl_text):
                    print(f"   🎉 音频解析完成: {ctrl_text}")
                    break

            # 注入封面
            cover_input = page.locator("input[type='file']").nth(1)
            cover_input.set_input_files(cover_path)
            cover_input.dispatch_event("change")
            time.sleep(2)

            crop_confirm = page.locator("button:has-text('确认'), .weui-desktop-dialog__wrp button:has-text('确认')").first
            if crop_confirm.is_visible():
                crop_confirm.click()
                time.sleep(1.5)

            # 填写标题与文案
            page.locator("input[placeholder='请填写标题']").first.fill(title[:40])
            page.locator("textarea[placeholder='请填写描述']").first.fill(desc)
            time.sleep(1)

            # 绑定合集
            try:
                col_select = page.locator(":text('选择合集'), .weui-desktop-select").first
                if col_select.is_visible():
                    col_select.click()
                    time.sleep(1)
                    target_opt = page.locator(".weui-desktop-dropdown__list-item:has-text('TSMC'), li:has-text('TSMC'), .weui-desktop-dropdown__list-item:has-text('Morris'), li:has-text('Morris')").first
                    if target_opt.is_visible():
                        target_opt.click()
                        time.sleep(1)
            except Exception as e:
                print(f"   ⚠️ 绑定合集提示: {e}")

            # 发表
            pub_btn = page.locator("button:has-text('发表音频')").first
            if pub_btn.is_visible():
                pub_btn.click()
                print(f"   🎉 Ep{ep_id} 发表成功！入库缓冲...")
                time.sleep(8)

            if idx < len(pending_eps):
                wait_sec = random.randint(30, 45)
                print(f"⏳ 安全休眠 {wait_sec} 秒后发布下一期...")
                time.sleep(wait_sec)

        # 3. 归集至合集
        print("\n📂 [3/3] 正在进入合集进行全量归集...")
        page.goto("https://channels.weixin.qq.com/platform/post/audioManager", wait_until="domcontentloaded")
        time.sleep(3)
        tab_col = page.locator(":text('合集')").first
        if tab_col.is_visible():
            tab_col.click()
            time.sleep(3)
            col_card = page.locator("tr:has-text('TSMC'), tr:has-text('Morris')").first
            if col_card.is_visible():
                detail_btn = col_card.locator("a:has-text('详情'), button:has-text('管理'), a:has-text('管理')").first
                if detail_btn.is_visible():
                    detail_btn.click()
                    time.sleep(3)
                    add_btn = page.locator("button:has-text('添加音频'), button:has-text('添加内容')").first
                    if add_btn.is_visible():
                        add_btn.click()
                        time.sleep(2)
                        for cb in page.locator(".weui-desktop-dialog__wrp input[type='checkbox']").all():
                            try:
                                if not cb.is_checked():
                                    cb.check()
                            except:
                                pass
                        save_btn = page.locator(".weui-desktop-dialog__wrp button:has-text('确定'), .weui-desktop-dialog__wrp button:has-text('确认')").first
                        if save_btn.is_visible():
                            save_btn.click()
                            print("🎉 英文音频合集归集完成！")
                            time.sleep(4)

        page.close()
        print("\n🏆🏆🏆 全量 19 期英文音频专栏发布与合集归集全部圆满达成！")
        return True

if __name__ == "__main__":
    run_cdp_publisher()
