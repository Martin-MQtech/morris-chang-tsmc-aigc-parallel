#!/usr/bin/env python3
"""
ReadShift 平行世界 · 出版物排版合成器（v2）

把「纯图」升级成「杂志/书籍章首页」：在封面 + 18 张章首图上烙入版式文字与装饰元素
（大号章节数字水印 · 双平行线品牌标志 · 期号 · 时间 · 中文标题 · 英文标题 · 装饰线），
沿用品牌签名色（琥珀金 + 天蓝 + 暗黑虚空）。

产出：
    设计资产/封面/封面_排版版.jpg         （2:3 竖版封面，书名烙入）
    设计资产/插图/排版版/第NN期-标题.jpg  （3:2 章首图，标题烙入）

用法：
    python3 tools/make_typography.py

文字排版在图片上完成（非 HTML 叠加），保证独立于阅读器也完整呈现；正文仍以
HTML 文本承载（可选中、可检索、可用阅读器 TTS 正确发音）。
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART_DIR = os.path.join(ROOT, "设计资产", "插图")
COVER_IN = os.path.join(ROOT, "设计资产", "封面", "cover_wafer_blueprint.jpg")
if not os.path.exists(COVER_IN):
    COVER_IN = os.path.join(ROOT, "设计资产", "封面", "封面_底图.jpg")
if not os.path.exists(COVER_IN):
    COVER_IN = os.path.join(ROOT, "设计资产", "封面", "封面_gemini.png")
if not os.path.exists(COVER_IN):
    COVER_IN = os.path.join(ROOT, "设计资产", "封面", "封面.png")
COVER_OUT = os.path.join(ROOT, "设计资产", "封面", "封面_排版版.jpg")
OUT_DIR = os.path.join(ART_DIR, "排版版")

# ---- 品牌签名色 ----
AMBER = (232, 198, 132)     # 琥珀金（主强调、时间、规则线）
BLUE = (127, 179, 213)      # 天蓝（期号、英文副题）
WHITE = (244, 238, 226)     # 暖白（主标题）
MUTED = (196, 188, 172)     # 灰米（次要文字）
INK = (16, 16, 20)          # 暗黑底

# ---- 字体 ----
F_SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"   # 1=Bold, 6=Regular, 0=Black
F_DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"   # 1=Italic, 0=Regular, 2=Bold
if not os.path.exists(F_DIDOT):
    F_DIDOT = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
F_HELV = "/System/Library/Fonts/Helvetica.ttc"             # 4=Light

def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

# ---- 每期元数据: (中文标题, 英文标题, 时间) ----
EPISODES = [
    ("逃难的孩子", "The Child Who Fled", "1937–1942"),
    ("考不进去的南开与作家梦", "The Closed Door & the Writer's Dream", "1943–1948"),
    ("从黄浦江到查尔斯河", "From the Huangpu River to the Charles", "1949–1950"),
    ("四十封求职信", "Forty Job Applications", "1954–1958"),
    ("隔岸观火的叛乱", "Watching the Rebellion from Across the Water", "1957–1968"),
    ("德仪的太空竞赛岁月", "The Space-Race Years at Texas Instruments", "1958–1964"),
    ("半导体之巅的十年", "A Decade at the Summit of Semiconductors", "1964–1978"),
    ("离开德州与受邀回台", "Leaving Texas & the Call Home", "1978–1987"),
    ("纯代工的革命", "The Pure-Play Revolution", "1987–1995"),
    ("从台湾到世界", "From Taiwan to the World", "1995–1998"),
    ("记忆体的诱惑", "The Memory Temptation", "1998–2000"),
    ("逆周期的定力", "Resolve Against the Cycle", "2001–2003"),
    ("交棒之痛", "The Pain of the Handover", "2003–2009"),
    ("绚烂年代", "The Splendid Years", "2009–2012"),
    ("苹果来敲门", "Apple Comes Knocking", "2010–2014"),
    ("摩尔定律的守卫者", "Guardian of Moore's Law", "2014–2018"),
    ("交棒与退休", "The Handover & Retirement", "2013–2018"),
    ("护国神山", "The Mountain That Shields the Island", "2018–今天"),
]


def v_gradient_mask(w, h, top_alpha, bottom_alpha):
    try:
        import numpy as np
        a = np.linspace(top_alpha, bottom_alpha, h).astype("uint8")
        return Image.fromarray(np.tile(a.reshape(h, 1), (1, w)), "L")
    except ImportError:
        mask = Image.new("L", (w, h))
        px = mask.load()
        for y in range(h):
            val = int(top_alpha + (bottom_alpha - top_alpha) * y / max(1, h - 1))
            for x in range(w):
                px[x, y] = val
        return mask


def overlay_gradient(base, box, top_alpha, bottom_alpha):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    mask = v_gradient_mask(w, h, top_alpha, bottom_alpha)
    black = Image.new("RGBA", (w, h), INK + (255,))
    base.paste(black, (x0, y0), mask)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def fit_font(draw, text, path, index, max_w, start_size, min_size=20):
    size = start_size
    while size > min_size:
        f = font(path, size, index)
        if text_w(draw, text, f) <= max_w:
            return f, size
        size -= 2
    return font(path, min_size, index), min_size


def draw_tracked(draw, text, fnt, color, x, y, tracking, anchor="la"):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=color, anchor=anchor)
        cx += text_w(draw, ch, fnt) + tracking
    return cx


def brand_mark(img, x, y, w=64, bar_h=4, gap=11):
    """双平行线品牌标志：上琥珀金、下天蓝 —— 呼应「同一时间线，另一个视角」。"""
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + w, y + bar_h], fill=AMBER)
    draw.rectangle([x, y + bar_h + gap, x + w, y + bar_h + gap + bar_h], fill=BLUE)


def ghost_numeral(img, text, fnt, color, x, y, alpha=70, anchor="ra"):
    """大号半透明章节数字水印（如右上角『01』）。"""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.text((x, y), text, font=fnt, fill=color + (alpha,), anchor=anchor)
    return Image.alpha_composite(img, overlay)


def chapter_opener(img, num, zh, en, span):
    """3:2 章首图 → 装饰成杂志章首页：右上大号数字水印 + 左下品牌标志/期号/标题。"""
    W, H = img.size
    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 底部压暗渐变（保证文字可读）
    overlay_gradient(img, (0, int(H * 0.40), W, H), 0, 220)

    # --- 右上角大号章节数字水印 ---
    ghost_numeral(img, "%02d" % num, font(F_DIDOT, int(H * 0.22), 2),
                  WHITE, W - int(W * 0.045), int(H * 0.035), alpha=78)

    mx = int(W * 0.055)
    base = H - int(H * 0.085)

    # --- 标题与英文副题字号（先算，决定整体高度） ---
    title_f, _ = fit_font(draw, zh, F_SONG, 1, W - 2 * mx, 120)
    en_f, _ = fit_font(draw, en, F_DIDOT, 1, W - 2 * mx, 50)

    title_px = draw.textbbox((0, 0), zh, font=title_f)[3] - draw.textbbox((0, 0), zh, font=title_f)[1]
    en_px = draw.textbbox((0, 0), en, font=en_f)[3] - draw.textbbox((0, 0), en, font=en_f)[1]

    kicker_f_zh = font(F_SONG, 38, 1)
    kicker_f_en = font(F_HELV, 32, 4)
    kicker_px = 38

    brand_w, brand_gap = 60, 16
    gap_title, gap_en, rule_gap = 14, 13, 18

    # 自底向上定位
    y_en = base - en_px
    y_title = y_en - gap_en - title_px
    y_rule = y_title - rule_gap - 3
    y_kicker = y_rule - 14 - kicker_px
    y_brand = y_kicker - brand_gap - (4 + 11 + 4)

    # --- 双平行线品牌标志 ---
    brand_mark(img, mx, y_brand, w=brand_w)

    # --- 期号 + 时间（混合字体一行） ---
    cx = mx
    draw.text((cx, y_kicker), "第 %02d 期" % num, font=kicker_f_zh, fill=BLUE, anchor="la")
    cx += text_w(draw, "第 %02d 期" % num, kicker_f_zh) + 18
    draw_tracked(draw, span, kicker_f_en, AMBER, cx, y_kicker + 4, 2, "la")

    # --- 装饰线（琥珀金） ---
    draw.rectangle([mx, y_rule, mx + 96, y_rule + 3], fill=AMBER)

    # --- 中文标题 ---
    draw.text((mx, y_title), zh, font=title_f, fill=WHITE, anchor="la")

    # --- 英文副题 ---
    draw.text((mx, y_en), en, font=en_f, fill=BLUE, anchor="la")

    return img.convert("RGB")


def draw_frame(img, inset, color, width=2):
    """内嵌细框（经典书籍封面框线）。"""
    W, H = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rectangle([inset, inset, W - inset, H - inset], outline=color + (78,), width=width)
    return Image.alpha_composite(img, overlay)


def draw_badge(img, cx, cy, w, h, text, fnt, tcolor, ocolor):
    """圆角描边徽章（如『AIGC 原创』标识）。"""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([cx, cy, cx + w, cy + h], radius=h // 2, outline=ocolor + (255,), width=2)
    d.text((cx + w / 2, cy + h / 2), text, font=fnt, fill=tcolor + (255,), anchor="mm")
    return Image.alpha_composite(img, overlay)


def draw_mixed_center(img, cx, y, segments, tracking=0):
    """多字体混排一行并居中。segments=[(text, fnt, color), ...]。"""
    draw = ImageDraw.Draw(img)
    total = sum(text_w(draw, t, f) + tracking for t, f, c in segments) - tracking
    x = cx - total / 2
    for t, f, c in segments:
        draw.text((x, y), t, font=f, fill=c, anchor="la")
        x += text_w(draw, t, f) + tracking


def cover(img):
    """2:3 竖版封面 → 半导体蓝图微雕·建筑级典藏封面：巨幅光刻晶圆、3倍加粗 tsmc 核心字标、左对齐专著排版、微透毛玻璃制作说明。"""
    import numpy as np
    import cv2
    from PIL import ImageFilter
    W, H = 1700, 2550
    img = img.resize((W, H), Image.Resampling.LANCZOS).convert("RGBA")

    # 整体背景深度压暗
    dark_layer = Image.new("RGBA", img.size, (5, 6, 8, 55))
    img = Image.alpha_composite(img, dark_layer)

    # 顶部与左下角暗部渐变保护
    overlay_gradient(img, (0, 0, W, int(H * 0.38)), 255, 0)
    overlay_gradient(img, (0, int(H * 0.70), int(W * 0.55), H), 0, 220)

    F_DIN = "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf"
    F_AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
    F_HIRA = "/System/Library/Fonts/Hiragino Sans GB.ttc"

    f_top = font(F_AVENIR, 30, index=2)          # Avenir Next Demi Bold
    f_zh_title = font(F_HIRA, 116, index=2)     # Hiragino W6 116px 粗体
    f_zh_sub_inline = font(F_HIRA, 46, index=2) # Hiragino W6 琥珀金
    f_en_title = font(F_AVENIR, 42, index=2)    # Avenir Next Demi Bold 42px
    f_slogan = font(F_HIRA, 38, index=2)        # 38px
    f_engine = font(F_HIRA, 32, index=0)

    # 说明文字放大加粗，GitHub 相对精简缩小
    f_note_hd = font(F_HIRA, 25, index=2)       # Note header (25px 加粗)
    f_note_zh = font(F_HIRA, 23, index=2)       # Note text (23px 加粗清晰)
    f_git = font(F_AVENIR, 19, index=2)         # Git link (19px 紧凑典雅)

    COLOR_WHITE = (255, 255, 255)
    COLOR_GOLD = (245, 180, 65)         # 暖琥珀金
    COLOR_BLUE = (56, 189, 248)         # 科技天蓝
    COLOR_SILVER = (226, 232, 240)      # 明亮科技银白
    COLOR_GRAY = (200, 210, 225)        # 统一清晰亮银灰

    draw = ImageDraw.Draw(img)
    cx = W / 2
    margin_l = int(W * 0.075)

    # 1. 顶部系列标（居中 + 贯穿细线）
    y = int(H * 0.052)
    top_text = "AIGC POWERED · READSHIFT PARALLEL EDITION"
    w_top = sum(draw.textbbox((0, 0), c, font=f_top)[2] - draw.textbbox((0, 0), c, font=f_top)[0] + 5 for c in top_text) - 5
    x_top = cx - w_top / 2
    for c in top_text:
        cw = draw.textbbox((0, 0), c, font=f_top)[2] - draw.textbbox((0, 0), c, font=f_top)[0]
        draw.text((x_top, y), c, font=f_top, fill=COLOR_SILVER, anchor="la")
        x_top += cw + 5

    y += 44
    draw.line([(margin_l, y), (W - margin_l, y)], fill=(255, 255, 255, 36), width=1)
    y += 56

    # 2. 左对齐主标题区
    x_cur = margin_l
    t_main = "台积电张忠谋"
    draw.text((x_cur, y), t_main, font=f_zh_title, fill=COLOR_WHITE, anchor="la")
    x_cur += draw.textbbox((0, 0), t_main, font=f_zh_title)[2] - draw.textbbox((0, 0), t_main, font=f_zh_title)[0] + 28
    draw.text((x_cur, y + 46), "·  传记时间线的平行世界", font=f_zh_sub_inline, fill=COLOR_GOLD, anchor="la")
    y += 138

    t_en = "MORRIS CHANG & TSMC — A PARALLEL BIOGRAPHY"
    draw.text((margin_l, y), t_en, font=f_en_title, fill=COLOR_SILVER, anchor="la")
    y += 68

    draw.text((margin_l, y), "同一时间线，另一个视角", font=f_slogan, fill=COLOR_GOLD, anchor="la")
    w_s = draw.textbbox((0, 0), "同一时间线，另一个视角", font=f_slogan)[2] - draw.textbbox((0, 0), "同一时间线，另一个视角", font=f_slogan)[0]
    draw.text((margin_l + w_s + 20, y + 5), "/  READSHIFT 平行叙事引擎", font=f_engine, fill=COLOR_GRAY, anchor="la")

    # 3. 晶圆中心区：增大 3 倍的官方 tsmc 标识 (宽度 1100px)
    logo_path = os.path.join(ROOT, "设计资产", "封面", "tsmc_clean_letters.png")
    if not os.path.exists(logo_path):
        logo_path = "/Users/martin/Desktop/tsmc_clean_letters.png"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).convert("RGBA")
        target_w = 1100
        target_h = int(target_w / logo_img.width * logo_img.height)
        logo_resized = logo_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        logo_arr = np.array(logo_resized)
        alpha = logo_arr[:, :, 3]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(alpha, kernel, iterations=1)
        dilated = cv2.GaussianBlur(dilated, (3, 3), 0)
        logo_arr[:, :, 0] = 255
        logo_arr[:, :, 1] = 255
        logo_arr[:, :, 2] = 255
        logo_arr[:, :, 3] = dilated
        logo_final = Image.fromarray(logo_arr, "RGBA")
        logo_x = int(cx - target_w / 2)
        logo_y = int(1800 - target_h / 2)
        img.paste(logo_final, (logo_x, logo_y), logo_final)

    # 4. 左下角毛玻璃卡片（微透高斯模糊 + 居中紧凑排版）
    lines = [
        ("PRODUCTION NOTE / 制作说明:", f_note_hd, COLOR_GOLD, 12),
        ("本版本由 ReadShift 平行叙事引擎深度重构，", f_note_zh, COLOR_GRAY, 7),
        ("实现全书语义级中英双语对照排版与知识延伸。", f_note_zh, COLOR_GRAY, 7),
        ("同一时间线，两个世界的历史回响。", f_note_zh, COLOR_GRAY, 11),
        ("https://github.com/Martin-MQtech/ReadShift", f_git, COLOR_GOLD, 0)
    ]

    # 预计算每行实际宽高（水平居中 + 垂直居中共用）
    line_info = []
    for t, f, c, g in lines:
        bb = draw.textbbox((0, 0), t, font=f)
        w = bb[2] - bb[0]
        h = bb[3] - bb[1]
        line_info.append((t, f, c, g, w, h))

    max_w = max(w for t, f, c, g, w, h in line_info)
    content_h = sum(h + g for t, f, c, g, w, h in line_info)

    pad_x = 30
    pad_y = 24
    card_w = max_w + pad_x * 2
    card_h = content_h + pad_y * 2

    card_x1 = margin_l - 10
    card_y1 = int(H * 0.880)
    card_x2 = card_x1 + card_w
    card_y2 = card_y1 + card_h
    radius = 12

    sub = img.crop((card_x1, card_y1, card_x2, card_y2))
    blurred_sub = sub.filter(ImageFilter.GaussianBlur(radius=18))

    glass_overlay = Image.new("RGBA", blurred_sub.size, (10, 12, 16, 185))
    d_glass = ImageDraw.Draw(glass_overlay)
    d_glass.rounded_rectangle([0, 0, blurred_sub.size[0] - 1, blurred_sub.size[1] - 1], radius=radius, outline=(255, 255, 255, 42), width=1)

    glass_card = Image.alpha_composite(blurred_sub, glass_overlay)

    mask = Image.new("L", blurred_sub.size, 0)
    d_mask = ImageDraw.Draw(mask)
    d_mask.rounded_rectangle([0, 0, blurred_sub.size[0], blurred_sub.size[1]], radius=radius, fill=255)

    img.paste(glass_card, (card_x1, card_y1), mask)

    draw_final = ImageDraw.Draw(img)
    card_cx = (card_x1 + card_x2) / 2
    # 整段文字块在毛玻璃卡片内垂直居中（上下留白均匀）
    cur_y = card_y1 + (card_h - content_h) / 2

    for t, f, c, g, w, h in line_info:
        # 水平居中（按实际字宽居中于卡片中线）
        draw_final.text((card_cx - w / 2, cur_y), t, font=f, fill=c, anchor="la")
        cur_y += h + g

    return img.convert("RGB")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    im = Image.open(COVER_IN).convert("RGB")
    im = cover(im)
    im.save(COVER_OUT, "JPEG", quality=95, optimize=True)
    print("封面排版版:", COVER_OUT, im.size)

    for i, (zh, en, span) in enumerate(EPISODES, 1):
        src = None
        for cand in os.listdir(ART_DIR):
            if cand.startswith("第%02d期" % i) and cand.endswith(".png"):
                src = os.path.join(ART_DIR, cand)
                break
        if not src:
            print("!! 缺图:", "第%02d期" % i)
            continue
        im = Image.open(src).convert("RGB")
        chapter_opener(im, i, zh, en, span)
        out = os.path.join(OUT_DIR, "第%02d期-%s.jpg" % (i, zh))
        im.save(out, "JPEG", quality=92, optimize=True)
        print("章首图排版版: 第%02d期 %s" % (i, zh))


if __name__ == "__main__":
    main()
