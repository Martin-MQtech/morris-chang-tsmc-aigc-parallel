#!/usr/bin/env python3
"""
《张忠谋自传 · 上册 (1931 - 1964)》双语典藏版封面生成脚本
基于原生上册全真底图（完全保留原生纯白线描与黑曜石背景），仅精准替换左下角制作说明文字（零黑色大补丁，零背景篡改）
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ROOT = "/Users/martin/Desktop/电子书制作研究/AIGC讲述"
DESKTOP_DIR = "/Users/martin/Desktop"
ASSETS_DIR = os.path.join(ROOT, "设计资产", "封面")
BRAIN_DIR = "/Users/martin/.gemini/antigravity-cli/brain/2ec4490a-b4e2-45f3-8c06-501a17787b33"
SOURCE_VOL1 = os.path.join(BRAIN_DIR, ".user_uploaded", "uploaded_media_1_1786791511848.jpg")

# Fonts
F_HIRA = "/System/Library/Fonts/Hiragino Sans GB.ttc"
F_AVENIR = "/System/Library/Fonts/Avenir Next.ttc"

def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

def generate_vol1_final():
    if not os.path.exists(SOURCE_VOL1):
        raise FileNotFoundError(f"Source Vol 1 image not found: {SOURCE_VOL1}")
        
    img_v1 = Image.open(SOURCE_VOL1).convert("RGB")
    arr = np.array(img_v1)
    
    # 仅在无晶片线条的安全纯黑留白区（x: 0..650, y: 2920..3550）用原生底色 [12, 12, 14] 擦除旧文字
    # 严禁触碰 x >= 680 的任何晶圆线条，绝无任何方块色差或补丁
    arr[2920:3550, 0:650] = [12, 12, 14]
    
    img_cleaned = Image.fromarray(arr)
    draw = ImageDraw.Draw(img_cleaned)
    
    COLOR_GOLD = (245, 180, 65)        # 暖琥珀金 (#F5B441)
    COLOR_GRAY = (200, 210, 225)       # 统一清晰亮银灰
    
    f_note_hd = font(F_HIRA, 27, index=2)       # 27px加粗
    f_note_zh = font(F_HIRA, 24, index=2)       # 24px清晰
    f_git = font(F_AVENIR, 20, index=2)         # 20px Avenir
    
    x_start = 120
    y_start = 3080
    
    # 标题行
    draw.text((x_start, y_start), "PRODUCTION NOTE / 制作说明:", font=f_note_hd, fill=COLOR_GOLD, anchor="la")
    cur_y = y_start + 48
    
    # 3 行中文说明
    zh_lines = [
        "本版本由 ReadShift 平行叙事引擎深度重构，",
        "实现全书语义级中英双语对照排版与知识延伸。",
        "同一时间线，两个世界的历史回响。"
    ]
    for l in zh_lines:
        draw.text((x_start, cur_y), l, font=f_note_zh, fill=COLOR_GRAY, anchor="la")
        cur_y += 38
        
    # GitHub 仓库链接
    cur_y += 10
    draw.text((x_start, cur_y), "https://github.com/Martin-MQtech/ReadShift", font=f_git, fill=COLOR_GOLD, anchor="la")
    
    targets = [
        os.path.join(DESKTOP_DIR, "张忠谋自传_上册_封面.jpg"),
        os.path.join(ASSETS_DIR, "封面_上册_排版版.jpg"),
        os.path.join(BRAIN_DIR, "cover_vol1_final_clean.jpg"),
    ]
    
    for p in targets:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img_cleaned.save(p, "JPEG", quality=96, optimize=True)
        print(f"✅ Generated: {p}")
        
    img_1700 = img_cleaned.resize((1700, 2550), Image.Resampling.LANCZOS)
    img_1700.save(os.path.join(ASSETS_DIR, "封面_上册_1700x2550.jpg"), "JPEG", quality=95, optimize=True)
    
    return img_cleaned

if __name__ == "__main__":
    generate_vol1_final()
