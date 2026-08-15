#!/usr/bin/env python3
"""
生成下册 CHAPTER_MAP 并替换 renderer 中的对应部分。
同时修改 chaptersDir 和 outPath 指向下册工作区。
"""

import json
import os
import re

WORKSPACE = "/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift"
RENDERER = os.path.join(WORKSPACE, "下册项目工作区", "render_html_v9.js")
GOLDEN = os.path.join(WORKSPACE, "下册项目工作区", "standards", "golden-v2.json")

# 读取 golden-v2.json
with open(GOLDEN, "r", encoding="utf-8") as f:
    golden = json.load(f)

# 英文标题映射（基于原书目录）
EN_TITLES = {
    0: ("Publisher's Note: A \"Triple Win\" at the Intersection of Globalization and Geopolitics", "高希均"),
    1: ("Author's Preface to the Second Volume", "张忠谋"),
    2: ("Glossary", None),
    3: ("Texas Instruments: Prologue", None),
    4: ("TI Chapter 1: \"When Are You Coming Back to Texas?\"", "张忠谋"),
    5: ("TI Chapter 2: From Engineer to General Manager Overnight", "张忠谋"),
    6: ("TI Chapter 3: Learning to Be a General Manager", "张忠谋"),
    7: ("TI Chapter 4: Smooth Sailing", "张忠谋"),
    8: ("TI Chapter 5: Four Bosses", "张忠谋"),
    9: ("TI Chapter 6: Realizing the American Dream", "张忠谋"),
    10: ("TI Chapter 7: TI's Southeast Asia Factories", "张忠谋"),
    11: ("TI Chapter 8: TI Loses Its Way", "张忠谋"),
    12: ("TI Chapter 9: Fighting and Struggling as Semiconductor Group GM", "张忠谋"),
    13: ("TI Chapter 10: A Way Station — Consumer Products Group GM", "张忠谋"),
    14: ("TI Chapter 11: The Last Cry — Quality!", "张忠谋"),
    15: ("TI Chapter 12: All Good Things Must Come to an End", "张忠谋"),
    16: ("TI Chapter 13: Career Interlude — General Instruments", "张忠谋"),
    17: ("TSMC Part I: A Date with Destiny (Prologue)", None),
    18: ("TSMC Part I Chapter 14: My Ties with Taiwan", "张忠谋"),
    19: ("TSMC Part I Chapter 15: ITRI — The Industrial Technology Research Institute", "张忠谋"),
    20: ("TSMC Part I Chapter 16: A Date with Destiny", "张忠谋"),
    21: ("TSMC Part I Chapter 17: Fundraising", "张忠谋"),
    22: ("TSMC Part I Chapter 18: Creating a New World", "张忠谋"),
    23: ("TSMC Part I Chapter 19: Blazing a Trail Through the Wilderness", "张忠谋"),
    24: ("TSMC Part II: The Roaring Nineties (Prologue)", None),
    25: ("TSMC Part II Chapter 20: The Pure-Play Foundry Model Shines", "张忠谋"),
    26: ("TSMC Part II Chapter 21: TSMC's Philosophy and 1990s Strategy", "张忠谋"),
    27: ("TSMC Part II Chapter 22: Control Battles Concluded; IPO in Taiwan and the US", "张忠谋"),
    28: ("TSMC Part II Chapter 23: The Temptation of Memory — Vanguard and WaferTech", "张忠谋"),
    29: ("TSMC Part II Chapter 24: Winning Customer Trust", "张忠谋"),
    30: ("TSMC Part II Chapter 25: Author and Professor", "张忠谋"),
    31: ("TSMC Part II Chapter 26: Key Clients Built in the 1990s", "张忠谋"),
    32: ("TSMC Part II Chapter 27: From \"Technological Self-Reliance\" to \"Technology Leadership\"", "张忠谋"),
    33: ("TSMC Part III: The Turbulent New Century (Prologue)", None),
    34: ("TSMC Part III Chapter 28: Marriage", "张忠谋"),
    35: ("TSMC Part III Chapter 29: From \"Roaring\" to \"Splendor\"", "张忠谋"),
    36: ("TSMC Part III Chapter 30: Building an Ideal Board of Directors", "张忠谋"),
    37: ("TSMC Part III Chapter 31: Releasing and Reclaiming the CEO Role", "张忠谋"),
    38: ("TSMC Part III Chapter 32: Old Steed in the Stable", "张忠谋"),
    39: ("TSMC Part III Chapter 33: Apple Comes Knocking", "张忠谋"),
    40: ("TSMC Part III Chapter 34: Succession Planning and Retirement", "张忠谋"),
    41: ("Acknowledgments", None),
    42: ("Chronology of Morris Chang", None),
    43: ("Photo Gallery (Photo Captions)", None),
    44: ("Copyright & Revenue Growth Chart", None),
}

def js_str(s):
    """安全转义 JavaScript 字符串字面量（单引号包裹）"""
    if not s:
        return ""
    # 先转义反斜杠，再转义单引号，最后转义双引号
    s = s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    return s


def make_entry(ch):
    cid = ch["id"]
    start = ch["page_start"]
    slug = js_str(ch["slug"])
    en_info = EN_TITLES.get(cid, (None, None))
    en_title, by = en_info

    if cid in (0, 1, 2):
        typ = "front"
    elif cid in (3, 17, 24, 33):
        typ = "front"
    elif cid >= 41:
        typ = "back"
    else:
        typ = "chapter"

    by_str = f", by: '{js_str(by)}'" if by else ""
    title_zh_str = f", title_zh: '{slug}'" if en_title else ""
    title_en_str = f", title_en: '{js_str(en_title)}'" if en_title else ""

    return f"    {{ start: {start}, name: '{slug}', type: '{typ}'{title_zh_str}{title_en_str}{by_str} }},"


# 生成 CHAPTER_MAP
entries = [make_entry(ch) for ch in golden["chapters"]]
chap_map_js = "const CHAPTER_MAP = [\n" + "\n".join(entries) + "\n];"

# 读取 renderer
with open(RENDERER, "r", encoding="utf-8") as f:
    code = f.read()

# 1. 替换 CHAPTER_MAP
pattern = r'const CHAPTER_MAP = \[.*?\];'
code = re.sub(pattern, chap_map_js, code, flags=re.DOTALL)

# 2. 修改 chaptersDir
code = code.replace(
    "const chaptersDir = path.join(__dirname, '..', 'output', 'chapters');",
    "const chaptersDir = path.join(__dirname, '.');"
)

# 3. 修改 fullDir
code = code.replace(
    "let fullDir = path.join(__dirname, '..', 'output', 'full');",
    "let fullDir = path.join(__dirname, 'output', 'full');"
)

# 4. 修改 outPath 默认值
code = code.replace(
    "path.join(__dirname, '..', 'output', 'preview_book.html');",
    "path.join(__dirname, 'output', 'preview_book.html');"
)

# 写回
with open(RENDERER, "w", encoding="utf-8") as f:
    f.write(code)

print("=== renderer 修改完成 ===")
print(f"CHAPTER_MAP: {len(entries)} 项")
print(f"chaptersDir -> 下册项目工作区/")
