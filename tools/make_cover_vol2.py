#!/usr/bin/env python3
"""
《张忠谋自传 · 下册 (1964 - 2018)》双语典藏版封面生成脚本
半导体微架构白线描 + 芯片中心精致TSMC白标 + 左下角纯文字说明（零底框、零补丁，100%连贯通透）
"""

import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

ROOT = "/Users/martin/Desktop/电子书制作研究/AIGC讲述"
DESKTOP_DIR = "/Users/martin/Desktop"
ASSETS_DIR = os.path.join(ROOT, "设计资产", "封面")
VOL2_DIR = os.path.join(ROOT, "01-参考内容", "下册_1964-2018")
BRAIN_DIR = "/Users/martin/.gemini/antigravity-cli/brain/2ec4490a-b4e2-45f3-8c06-501a17787b33"
BASE_MICROPROCESSOR = os.path.join(BRAIN_DIR, "vol2_blueprint_tsmc_base_b_1786792671383.jpg")
LOGO_PATH = os.path.join(ASSETS_DIR, "tsmc_clean_letters.png")

# Fonts
F_SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"
F_HIRA = "/System/Library/Fonts/Hiragino Sans GB.ttc"
F_AVENIR = "/System/Library/Fonts/Avenir Next.ttc"

def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

def v_gradient_mask(w, h, top_alpha, bottom_alpha):
    a = np.linspace(top_alpha, bottom_alpha, h).astype("uint8")
    return Image.fromarray(np.tile(a.reshape(h, 1), (1, w)), "L")

def overlay_gradient(base, box, top_alpha, bottom_alpha, color=(10, 11, 14)):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    mask = v_gradient_mask(w, h, top_alpha, bottom_alpha)
    black = Image.new("RGBA", (w, h), color + (255,))
    base.paste(black, (x0, y0), mask)

def prepare_clean_tsmc_badge(logo_path, target_w=700, bg_halo_radius=16):
    logo_img = Image.open(logo_path).convert("RGBA")
    target_h = int(target_w / logo_img.width * logo_img.height)
    logo_resized = logo_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    logo_arr = np.array(logo_resized)
    alpha = logo_arr[:, :, 3]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    dilated = cv2.dilate(alpha, kernel, iterations=1)
    dilated = cv2.GaussianBlur(dilated, (3, 3), 0)
    
    white_letters = np.zeros((target_h, target_w, 4), dtype=np.uint8)
    white_letters[:, :, 0] = 255
    white_letters[:, :, 1] = 255
    white_letters[:, :, 2] = 255
    white_letters[:, :, 3] = dilated
    im_white = Image.fromarray(white_letters, "RGBA")
    
    pad = bg_halo_radius * 2 + 10
    halo_w = target_w + pad * 2
    halo_h = target_h + pad * 2
    
    alpha_pad = np.pad(alpha, ((pad, pad), (pad, pad)), mode="constant")
    kernel_halo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (bg_halo_radius * 2 + 1, bg_halo_radius * 2 + 1))
    halo_mask = cv2.dilate(alpha_pad, kernel_halo, iterations=1)
    halo_mask = cv2.GaussianBlur(halo_mask, (15, 15), 0)
    
    halo_arr = np.zeros((halo_h, halo_w, 4), dtype=np.uint8)
    halo_arr[:, :, 0] = 10
    halo_arr[:, :, 1] = 11
    halo_arr[:, :, 2] = 14
    halo_arr[:, :, 3] = (halo_mask * 0.95).astype(np.uint8)
    
    im_halo = Image.fromarray(halo_arr, "RGBA")
    im_halo.paste(im_white, (pad, pad), im_white)
    return im_halo

def render_pure_text_note(draw, x_start=120, y_start=3080):
    COLOR_GOLD = (245, 180, 65)        # 暖琥珀金 (#F5B441)
    COLOR_GRAY = (200, 210, 225)       # 统一清晰亮银灰
    
    f_note_hd = font(F_HIRA, 27, index=2)       # 27px加粗
    f_note_zh = font(F_HIRA, 24, index=2)       # 24px清晰
    f_git = font(F_AVENIR, 20, index=2)         # 20px Avenir
    
    draw.text((x_start, y_start), "PRODUCTION NOTE / 制作说明:", font=f_note_hd, fill=COLOR_GOLD, anchor="la")
    cur_y = y_start + 48
    
    zh_lines = [
        "本版本由 ReadShift 平行叙事引擎深度重构，",
        "实现全书语义级中英双语对照排版与知识延伸。",
        "同一时间线，两个世界的历史回响。"
    ]
    for l in zh_lines:
        draw.text((x_start, cur_y), l, font=f_note_zh, fill=COLOR_GRAY, anchor="la")
        cur_y += 38
        
    cur_y += 10
    draw.text((x_start, cur_y), "https://github.com/Martin-MQtech/ReadShift", font=f_git, fill=COLOR_GOLD, anchor="la")

def generate_vol2_final():
    if not os.path.exists(BASE_MICROPROCESSOR):
        raise FileNotFoundError(f"Base microprocessor image not found: {BASE_MICROPROCESSOR}")
        
    W, H = 2400, 3577
    img = Image.open(BASE_MICROPROCESSOR).convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
    
    # 顶部平滑全宽渐变
    overlay_gradient(img, (0, 0, W, int(H * 0.32)), 255, 0, color=(10, 11, 14))
    # 彻底去除左下角任何矩形或局部渐变
    
    if os.path.exists(LOGO_PATH):
        badge = prepare_clean_tsmc_badge(LOGO_PATH, target_w=700, bg_halo_radius=16)
        bx = int(1905 - badge.width / 2)
        by = int(2201 - badge.height / 2)
        img.paste(badge, (bx, by), badge)
        
    draw = ImageDraw.Draw(img)
    
    COLOR_WHITE = (247, 244, 237)
    COLOR_GOLD = (245, 180, 65)
    COLOR_SILVER = (226, 232, 240)
    
    # 1. 顶部系列标
    f_top = font(F_AVENIR, 42, index=2)
    top_text = "AIGC POWERED · READSHIFT EDITION"
    cx = W / 2
    w_top = sum(draw.textbbox((0, 0), c, font=f_top)[2] - draw.textbbox((0, 0), c, font=f_top)[0] + 6 for c in top_text) - 6
    x_top = cx - w_top / 2
    y_top = 160
    for c in top_text:
        cw = draw.textbbox((0, 0), c, font=f_top)[2] - draw.textbbox((0, 0), c, font=f_top)[0]
        draw.text((x_top, y_top), c, font=f_top, fill=COLOR_SILVER, anchor="la")
        x_top += cw + 6
        
    y_line = 245
    margin_line = 120
    draw.line([(margin_line, y_line), (W - margin_line, y_line)], fill=(255, 255, 255, 45), width=2)
    
    # 2. 中文主书名
    f_zh_main = font(F_SONG, 185, index=0)
    f_zh_sub = font(F_SONG, 86, index=1)
    x_main = 246
    y_main = 355
    draw.text((x_main, y_main), "张忠谋自传", font=f_zh_main, fill=COLOR_WHITE, anchor="la")
    draw.text((1285, 416), " · 下册 (1964 - 2018)", font=f_zh_sub, fill=COLOR_GOLD, anchor="la")
    
    # 3. 英文主书名
    f_en_title = font(F_AVENIR, 64, index=2)
    draw.text((x_main, 650), "MORRIS CHANG AUTOBIOGRAPHY · VOL. 2 (1964–2018)", font=f_en_title, fill=COLOR_SILVER, anchor="la")
    
    # 4. 作者行
    f_auth_zh = font(F_SONG, 68, index=1)
    f_auth_en = font(F_AVENIR, 56, index=2)
    y_auth = 840
    t_auth_zh = "张忠谋 著"
    draw.text((x_main, y_auth), t_auth_zh, font=f_auth_zh, fill=COLOR_WHITE, anchor="la")
    w_auth_zh = draw.textbbox((0, 0), t_auth_zh, font=f_auth_zh)[2] - draw.textbbox((0, 0), t_auth_zh, font=f_auth_zh)[0]
    draw.text((x_main + w_auth_zh + 15, y_auth + 8), " / TSMC FOUNDER", font=f_auth_en, fill=COLOR_SILVER, anchor="la")
    
    # 5. 左下角纯文字说明（零底框、零补丁）
    render_pure_text_note(draw, x_start=120, y_start=3080)
    
    final_img = img.convert("RGB")
    
    targets = [
        os.path.join(DESKTOP_DIR, "张忠谋自传_下册_封面.jpg"),
        os.path.join(ASSETS_DIR, "封面_下册_排版版.jpg"),
        os.path.join(VOL2_DIR, "下册封面.jpg"),
        os.path.join(BRAIN_DIR, "cover_vol2_glass.jpg"),
    ]
    
    for p in targets:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        final_img.save(p, "JPEG", quality=96, optimize=True)
        print(f"✅ Generated: {p}")
        
    img_1700 = final_img.resize((1700, 2550), Image.Resampling.LANCZOS)
    img_1700.save(os.path.join(ASSETS_DIR, "封面_下册_1700x2550.jpg"), "JPEG", quality=95, optimize=True)
    
    return final_img

if __name__ == "__main__":
    generate_vol2_final()
