#!/usr/bin/env python3
"""
ReadShift 平行世界 · 出版级 EPUB 3.0 生成器

读取 03-剧集/ 下第 01–18 期的中英文字稿（有正文的期数自动并入），按
《电子书EPUB制作规范.md》打包成流式 EPUB 3.0（双层目录 + 双语 lang 标注 +
封面/章首插图 + 合规打包），供 Apple Books / 微信读书 / Google Play / Kobo 阅读:
    python3 tools/make_epub.py            # 输出 台积电张忠谋-传记时间线的平行世界.epub
    python3 tools/make_epub.py --check    # 生成后做结构自检

规范要点（见 电子书EPUB制作规范.md）：mimetype 第一位无压缩；nav.xhtml+toc.ncx 双目录；
底色透明；中英块各自 lang 标注；封面/插图走 设计资产/；AIGC 原创声明（仅供学习交流、禁止商用）。
"""
import html
import io
import os
import re
import sys
import uuid
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP_DIR = os.path.join(ROOT, "03-剧集")
ART_DIR = os.path.join(ROOT, "设计资产", "插图", "排版版")
COVER_PATH = os.path.join(ROOT, "设计资产", "封面", "封面_排版版.jpg")
OUT = os.path.join(ROOT, "台积电张忠谋-传记时间线的平行世界.epub")

TITLE = "台积电张忠谋 · 传记时间线的平行世界"
CREATOR = "ReadShift · 平行叙事引擎"
UUID = str(uuid.uuid4())

# (期号, 文件夹名, 章标题, 英文章标题, 时间范围, 金句, 图注中文, 图注英文)
# 英文标题与 tools/make_typography.py、tools/make_ebook.py 的权威英文标题表对齐
EPISODES = [
    (1, "第01期-逃难的孩子", "逃难的孩子", "The Child Who Fled", "1937–42",
     "一个孩子的记忆里，战争不是历史，是一张张搬家的船票。", "一只太早打包的箱子", "A suitcase packed too early"),
    (2, "第02期-考不进去的南开与作家梦", "考不进去的南开 & 作家梦", "The Closed Door & the Writer's Dream", "1943–48",
     "关系可以给你一张门票，但只有实力，能让你一直坐在场上。", "一扇进不去的门，一支停不下的笔", "A closed door, an unstoppable pen"),
    (3, "第03期-从黄浦江到查尔斯河", "从黄浦江到查尔斯河", "From the Huangpu River to the Charles", "1949–50",
     "他把离开当成了暂时，却走出了一条不归路。", "一条发光的航线，横渡两个世界", "One luminous route across two worlds"),
    (4, "第04期-四十封求职信", "四十封求职信", "Forty Job Applications", "1954–58",
     "被拒绝不是终点，是命运在给你指另一条路。", "四十封信里，只有一封被点亮", "One reply among forty"),
    (5, "第05期-隔岸观火的叛乱", "隔岸观火的叛乱", "Watching the Rebellion from Across the Water", "1957–68",
     "他隔岸看完的那场叛乱，后来成了他自己的剧本。", "隔着一道玻璃墙，看别人的火", "Watching another's fire through glass"),
    (6, "第06期-德仪的太空竞赛岁月", "德仪的太空竞赛岁月", "The Space-Race Years at Texas Instruments", "1958–64",
     "真正的强者，敢于在上升期把自己清零。", "一枚瞄准太空的硅片", "Silicon aimed at space"),
    (7, "第07期-半导体之巅的十年", "半导体之巅的十年", "A Decade at the Summit of Semiconductors", "1964–78",
     "最难的仗，往往不在市场上，而在会议室里。", "在硅片堆成的山顶，独自站立", "Standing alone atop a summit of silicon"),
    (8, "第08期-离开德州与受邀回台", "离开德州 & 受邀回台", "Leaving Texas & the Call Home", "1978–87",
     "离开一个错误的位置，是人生最重要的一步棋。", "一张空了的椅子，一束来自大洋彼岸的光", "An empty chair, a call across the ocean"),
    (9, "第09期-纯代工的革命", "纯代工的革命", "The Pure-Play Revolution", "1987–95",
     "颠覆者不做主角，做平台——让所有人成为主角。", "一座为所有人而建、却空着主角的舞台", "A stage built for everyone but the builder"),
    (10, "第10期-从台湾到世界", "从台湾到世界", "From Taiwan to the World", "1995–98",
     "当风暴来时，扎实的企业反而被看见。", "纽约的钟声，向世界荡开", "The bell of New York, ringing across the world"),
    (11, "第11期-记忆体的诱惑", "记忆体的诱惑", "The Memory Temptation", "1998–2000",
     "巅峰前的最后一次心动。", "一颗诱人却危险的晶体", "A beautiful, dangerous crystal"),
    (12, "第12期-逆周期的定力", "逆周期的定力", "Resolve Against the Cycle", "2001–03",
     "不景气，是挖人才最好的时候。", "逆流而上的一道光柱", "A column of light rising against the stream"),
    (13, "第13期-交棒之痛", "交棒之痛", "The Pain of the Handover", "2003–09",
     "亲手交出 CEO，又亲手拿回来。", "悬在半空的权杖", "A scepter caught mid-exchange"),
    (14, "第14期-绚烂年代", "绚烂年代", "The Splendid Years", "2009–12",
     "28nm 之战、英伟达的披萨之夜。", "一颗散发光芒的硅片", "A chip radiating brilliance"),
    (15, "第15期-苹果来敲门", "苹果来敲门", "Apple Comes Knocking", "2010–14",
     "最挑剔的客户，逼出了最强的一家工厂。", "门上落下的苹果光斑", "An apple-shaped light on the door"),
    (16, "第16期-摩尔定律的守卫者", "摩尔定律的守卫者", "Guardian of Moore's Law", "2014–18",
     "追，追到只剩你一个。", "越走越窄的阶梯", "A staircase thinning toward the summit"),
    (17, "第17期-交棒与退休", "交棒与退休", "The Handover & Retirement", "2013–18",
     "贝多芬第九响起时，全场起立鼓掌。", "轻轻放下的指挥棒", "A baton laid gently to rest"),
    (18, "第18期-护国神山", "护国神山", "The Mountain That Shields the Island", "2018–今天",
     "一家公司，如何成为一个岛屿的命运共同体。", "一座硅晶体巨山", "A mountain of silicon crystal"),
]

STAGE = re.compile(r"^【|^\[SFX|^\[Main\s+narrator|^\[Narrator|^\[主叙述者")


def esc(s):
    return html.escape(s, quote=True)


def jpg_bytes(path, max_w=1400, quality=84):
    """读取图片 → 缩放 → JPG bytes。"""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        h = max(1, int(im.height * max_w / im.width))
        im = im.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return buf.getvalue()


def parse(path):
    """解析文字稿 → [(小节标题, [段落]), ...]，跳过舞台标记/下期预告。"""
    sections = []
    cur_head = None
    cur_paras = []
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for line in lines:
        s = line.strip()
        if not s:
            continue
        m = re.match(r"^##\s+(.*)", s)
        if m:
            head = m.group(1).strip()
            # 下集/下期预告标题不统一（下期预告 / 下集预告 / Next Episode Preview），一律截止
            if ("预告" in head or "Next Episode" in head or "Preview" in head):
                break
            if cur_head is not None or cur_paras:
                sections.append((cur_head, cur_paras))
            cur_head = head
            cur_paras = []
            continue
        if re.match(r"^#\s", s):          # 一级标题（本集标题），跳过
            continue
        if s.startswith(">"):
            continue
        if re.match(r"^-{3,}$", s):
            continue
        if STAGE.match(s):
            continue
        if ("以下为公开资料核实" in s or "Verified public facts" in s
                or s.startswith("（以下为公开资料")):
            continue
        cur_paras.append(s.replace("**", ""))
    if cur_head is not None or cur_paras:
        sections.append((cur_head, cur_paras))
    return sections


def interleave_xhtml(zh_sections, en_sections, num):
    """中英段落级交错 → XHTML。返回 (html, [(小节id, 中文标题), ...])。"""
    out = []
    toc = []
    n = max(len(zh_sections), len(en_sections))
    for i in range(n):
        zh_head, zh_paras = zh_sections[i] if i < len(zh_sections) else (None, [])
        en_head, en_paras = en_sections[i] if i < len(en_sections) else (None, [])
        sid = "sub-%02d-%d" % (num, i + 1)
        if zh_head:
            toc.append((sid, zh_head))
        if zh_head or en_head:
            zs = ('<span class="zh" xml:lang="zh-CN" lang="zh-CN">%s</span>' % esc(zh_head)) if zh_head else ""
            es = ('<span class="en" xml:lang="en" lang="en">%s</span>' % esc(en_head)) if en_head else ""
            out.append('<h3 class="subsection" id="%s">%s%s</h3>' % (sid, zs, es))
        # 对齐段数：一侧尾部多出的段落并回上一段（保证中英一一对应，不丢文字）
        nzh, nen = len(zh_paras), len(en_paras)
        if nzh > nen > 0:
            zh_paras = zh_paras[:nen - 1] + ["".join(zh_paras[nen - 1:])]
        elif nen > nzh > 0:
            en_paras = en_paras[:nzh - 1] + [" ".join(en_paras[nzh - 1:])]
        m = max(len(zh_paras), len(en_paras))
        for j in range(m):
            if j < len(zh_paras):
                out.append('<p class="cn-para" xml:lang="zh-CN" lang="zh-CN">%s</p>' % esc(zh_paras[j]))
            if j < len(en_paras):
                out.append('<div class="rebook-translation">'
                           '<p class="en-para" xml:lang="en" lang="en">%s</p></div>' % esc(en_paras[j]))
    return "\n".join(out), toc


def build_chapter(num, folder, title, en_title, span, motto, cap_zh, cap_en):
    zh_path = os.path.join(EP_DIR, folder, "中文文字稿.md")
    en_path = os.path.join(EP_DIR, folder, "英文文字稿.md")
    if not os.path.exists(zh_path):
        return None  # 正文未到位，跳过（如第 11–18 期）

    zh_sections = parse(zh_path)
    en_sections = parse(en_path) if os.path.exists(en_path) else []
    body_html, zh_toc = interleave_xhtml(zh_sections, en_sections, num)

    art = os.path.join(ART_DIR, folder + ".jpg")
    art_img = ""
    if os.path.exists(art):
        art_img = ('<figure class="chapter-art page-break">\n'
                   '  <img src="../Images/chapter_art_%02d.jpg" alt="第 %02d 期 · %s"/>\n'
                   '  <figcaption><span class="zh">%s</span><span class="en">%s</span></figcaption>\n'
                   '</figure>\n' % (num, num, esc(title), esc(cap_zh), esc(cap_en)))

    doc = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>第 %02d 期 · %s · %s</title>
<link rel="stylesheet" type="text/css" href="../Stylesheet.css"/>
</head>
<body>
<section epub:type="chapter" id="ch%02d">
<h2 class="sr-only">第 %02d 期 · %s</h2>
%s
<blockquote class="motto">%s</blockquote>

%s
</section>
</body>
</html>
""" % (num, esc(title), esc(en_title), num, num, esc(title), art_img, esc(motto), body_html)
    return {"html": doc, "zh_toc": zh_toc, "title": title, "span": span, "num": num}


def main():
    chapters = []
    for num, folder, title, en_title, span, motto, cap_zh, cap_en in EPISODES:
        ch = build_chapter(num, folder, title, en_title, span, motto, cap_zh, cap_en)
        if ch:
            chapters.append(ch)

    if not chapters:
        raise SystemExit("未找到任何有正文的期数")

    files = {}  # {zip内路径: bytes}

    # 1. mimetype（必须第一位，无压缩）
    files["mimetype"] = b"application/epub+zip"

    # 2. container.xml
    files["META-INF/container.xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
        '  <rootfiles>\n'
        '    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n'
        '  </rootfiles>\n'
        '</container>\n'
    ).encode("utf-8")

    # 3. 封面图 + 章首图
    cover_jpg = jpg_bytes(COVER_PATH, max_w=1600, quality=85) if os.path.exists(COVER_PATH) else b""
    files["OEBPS/Images/cover.jpg"] = cover_jpg
    for ch in chapters:
        num = ch["num"]
        folder = EPISODES[num - 1][1]
        art = os.path.join(ART_DIR, folder + ".jpg")
        if os.path.exists(art):
            files["OEBPS/Images/chapter_art_%02d.jpg" % num] = jpg_bytes(art, max_w=1376, quality=88)

    # 4. Stylesheet.css
    files["OEBPS/Stylesheet.css"] = STYLESHEET.encode("utf-8")

    # 5. 封面页 / 扉页 / nav
    files["OEBPS/Text/cover.xhtml"] = COVER_XHTML.encode("utf-8")
    files["OEBPS/Text/title_page.xhtml"] = TITLE_PAGE.encode("utf-8")
    files["OEBPS/Text/reading_guide.xhtml"] = READING_GUIDE.encode("utf-8")

    # 6. 章节
    for ch in chapters:
        files["OEBPS/Text/chap_%02d.xhtml" % ch["num"]] = ch["html"].encode("utf-8")

    # 7. toc.ncx + nav.xhtml
    files["OEBPS/toc.ncx"] = build_ncx(chapters).encode("utf-8")
    files["OEBPS/Text/nav.xhtml"] = build_nav(chapters).encode("utf-8")

    # 8. content.opf
    files["OEBPS/content.opf"] = build_opf(chapters).encode("utf-8")

    # 9. 打包
    with zipfile.ZipFile(OUT, "w") as z:
        z.writestr("mimetype", files["mimetype"], compress_type=zipfile.ZIP_STORED)
        for name in sorted(files):
            if name == "mimetype":
                continue
            z.writestr(name, files[name], compress_type=zipfile.ZIP_DEFLATED)

    size_mb = os.path.getsize(OUT) / 1024 / 1024
    print("生成:", OUT)
    print("章数:", len(chapters), "| 大小:", round(size_mb, 2), "MB")

    if "--check" in sys.argv:
        self_check(files, chapters)


def build_opf(chapters):
    manifest_items = [
        '<item href="Text/nav.xhtml" id="nav" media-type="application/xhtml+xml" properties="nav"/>',
        '<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>',
        '<item href="Stylesheet.css" id="css" media-type="text/css"/>',
        '<item href="Text/cover.xhtml" id="cover" media-type="application/xhtml+xml"/>',
        '<item href="Text/title_page.xhtml" id="title_page" media-type="application/xhtml+xml"/>',
        '<item href="Text/reading_guide.xhtml" id="reading_guide" media-type="application/xhtml+xml"/>',
        '<item href="Images/cover.jpg" id="cover-image" media-type="image/jpeg" properties="cover-image"/>',
    ]
    spine_items = [
        '<itemref idref="cover"/>',
        '<itemref idref="title_page"/>',
        '<itemref idref="reading_guide"/>',
        '<itemref idref="nav"/>',
    ]
    for ch in chapters:
        num = ch["num"]
        manifest_items.append('<item href="Images/chapter_art_%02d.jpg" id="art%02d" media-type="image/jpeg"/>' % (num, num))
        manifest_items.append('<item href="Text/chap_%02d.xhtml" id="chap_%02d" media-type="application/xhtml+xml"/>' % (num, num))
        spine_items.append('<itemref idref="chap_%02d"/>' % num)

    return """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="zh-CN">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">urn:uuid:%s</dc:identifier>
<dc:title>%s</dc:title>
<dc:creator>%s</dc:creator>
<dc:language>zh-CN</dc:language>
<dc:language>en</dc:language>
<dc:publisher>ReadShift Publishing</dc:publisher>
<dc:date>2026-08-15</dc:date>
<dc:description>一册 18 期的原创平行传记：同一时间线，另一个视角。中英双语 · 典藏插图 · AIGC 原创。</dc:description>
<meta property="dcterms:modified">2026-08-15T00:00:00Z</meta>
<meta content="cover-image" name="cover"/>
</metadata>
<manifest>
%s
</manifest>
<spine toc="ncx">
%s
</spine>
</package>
""" % (UUID, esc(TITLE), esc(CREATOR), "\n".join(manifest_items), "\n".join(spine_items))


def build_ncx(chapters):
    order = [0]
    def nxt():
        order[0] += 1
        return order[0]

    head = [
        '<navPoint id="nav_cover" playOrder="%d"><navLabel><text>封面</text></navLabel><content src="Text/cover.xhtml"/></navPoint>' % nxt(),
        '<navPoint id="nav_title" playOrder="%d"><navLabel><text>扉页</text></navLabel><content src="Text/title_page.xhtml"/></navPoint>' % nxt(),
        '<navPoint id="nav_guide" playOrder="%d"><navLabel><text>阅读指南</text></navLabel><content src="Text/reading_guide.xhtml"/></navPoint>' % nxt(),
        '<navPoint id="nav_toc" playOrder="%d"><navLabel><text>目录</text></navLabel><content src="Text/nav.xhtml"/></navPoint>' % nxt(),
    ]
    for ch in chapters:
        num = ch["num"]
        chap_play = nxt()  # 章节点 playOrder 先于其子节点
        subs = "".join(
            '<navPoint id="chap_%02d_sub%d" playOrder="%d"><navLabel><text>%s</text></navLabel>'
            '<content src="Text/chap_%02d.xhtml#%s"/></navPoint>'
            % (num, i, nxt(), esc(h), num, sid)
            for i, (sid, h) in enumerate(ch["zh_toc"], 1)
        )
        head.append(
            '<navPoint id="chap_%02d" playOrder="%d"><navLabel><text>第 %02d 期 · %s</text></navLabel>'
            '<content src="Text/chap_%02d.xhtml"/>%s</navPoint>'
            % (num, chap_play, num, esc(ch["title"]), num, subs)
        )

    return """<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="zh-CN">
<head>
<meta name="dtb:uid" content="urn:uuid:%s"/>
<meta name="dtb:depth" content="2"/>
<meta name="dtb:totalPageCount" content="0"/>
<meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle><text>%s</text></docTitle>
<navMap>
%s
</navMap>
</ncx>
""" % (UUID, esc(TITLE), "\n".join(head))


def build_nav(chapters):
    items = []
    for ch in chapters:
        num = ch["num"]
        subs = "".join(
            '<li><a href="Text/chap_%02d.xhtml#%s">%s</a></li>' % (num, sid, esc(h))
            for sid, h in ch["zh_toc"]
        )
        items.append('<li><a href="Text/chap_%02d.xhtml">第 %02d 期 · %s <span>%s</span></a>%s</li>'
                     % (num, num, esc(ch["title"]), esc(ch["span"]),
                        ('<ol>%s</ol>' % subs) if subs else ""))

    return """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>目录</title>
<link rel="stylesheet" type="text/css" href="../Stylesheet.css"/>
</head>
<body>
<nav epub:type="toc" id="toc">
<h1 class="toc-title">目录</h1>
<ol>
<li><a href="Text/cover.xhtml">封面</a></li>
<li><a href="Text/title_page.xhtml">扉页</a></li>
<li><a href="Text/reading_guide.xhtml">阅读指南</a></li>
%s
</ol>
</nav>
<nav epub:type="landmarks" id="landmarks" hidden="hidden">
<h2>地标</h2>
<ol>
<li><a epub:type="cover" href="Text/cover.xhtml">封面</a></li>
<li><a epub:type="bodymatter" href="Text/chap_01.xhtml">正文开始</a></li>
</ol>
</nav>
</body>
</html>
""" % "\n".join(items)


def self_check(files, chapters):
    """结构自检：mimetype 首位 / manifest 引用齐全 / XML 良构。"""
    import xml.etree.ElementTree as ET
    ok = True
    names = set(files.keys())
    # 1) XML 良构
    for n in ("OEBPS/content.opf", "OEBPS/toc.ncx", "OEBPS/Text/nav.xhtml", "OEBPS/Text/cover.xhtml", "OEBPS/Text/title_page.xhtml", "OEBPS/Text/reading_guide.xhtml"):
        try:
            ET.fromstring(files[n])
        except ET.ParseError as e:
            print("✗ XML 良构失败:", n, e)
            ok = False
    for ch in chapters:
        try:
            ET.fromstring(ch["html"].encode("utf-8"))
        except ET.ParseError as e:
            print("✗ 章节 XML 良构失败:", ch["num"], e)
            ok = False
    # 2) 引用完整性：章节/封面/目录里的相对图片/链接必须落到实际文件
    missing = []
    for ch in chapters:
        html_text = ch["html"]
        for m in re.findall(r'(?:src|href)="\.\./(Images/[^"]+)"', html_text):
            if ("OEBPS/" + m) not in names:
                missing.append("OEBPS/" + m)
    for m in re.findall(r'src="\.\./(Images/[^"]+)"', files.get("OEBPS/Text/cover.xhtml", b"").decode("utf-8")):
        if ("OEBPS/" + m) not in names:
            missing.append("OEBPS/" + m)
    if missing:
        print("✗ 缺失引用:", sorted(set(missing)))
        ok = False
    # 3) manifest 声明与 spine 引用一致
    opf = files["OEBPS/content.opf"].decode("utf-8")
    manifest_hrefs = set(re.findall(r'<item[^>]*href="([^"]+)"', opf))
    for h in manifest_hrefs:
        if ("OEBPS/" + h if not h.startswith("OEBPS/") else h) not in names:
            print("✗ manifest 声明但文件缺失:", h)
            ok = False
    print("✓ mimetype 位于:", list(files.keys())[0] == "mimetype")
    print("✓ 章数:", len(chapters), "| 文件数:", len(names), "| 章首图:",
          sum(1 for n in names if "chapter_art" in n))
    if ok:
        print("✓ 结构自检通过（提示：上架前仍建议跑 epubcheck 完整校验）")
    else:
        raise SystemExit("✗ 自检发现错误")


STYLESHEET = """@charset "UTF-8";
/* 出版级 EPUB 3.0 样式 · 透明底 + 双语 lang + 防撕裂 */
html, body { margin:0; padding:0; line-height:1.85; }
body { padding:4% 5% 8%; color:#1c1917; background:transparent;
  font-family:"Songti SC","Source Han Serif SC","Noto Serif CJK SC","SimSun",Georgia,serif; }

/* 封面 */
.cover-container { text-align:center; }
.cover-img { width:100%; height:auto; max-width:100%; }

/* 扉页 */
.title-page { text-align:center; padding:14% 5% 10%; }
.title-page .eyebrow { font-size:.8em; letter-spacing:.2em; color:#78716c; text-transform:uppercase; }
.title-page h1 { font-size:1.8em; font-weight:700; margin:.5em 0; line-height:1.3; }
.title-page .author { font-size:1em; color:#57534e; margin-top:1.4em; }
.title-page .ornament { color:#9a3412; margin:1em 0; }
.title-page .copyright { margin-top:2em; padding:1em 1.4em; border:1px solid #e7e0d3;
  border-radius:8px; font-size:.85em; color:#44403c; text-align:left; line-height:1.8; }

/* 目录 */
.toc-title { font-size:1.5em; text-align:center; letter-spacing:.3em; color:#9a3412; }
nav#toc ol { list-style:none; padding:0; margin:1.5em 0; }
nav#toc > ol > li { margin:.5em 0; }
nav#toc > ol > li > a { font-weight:600; color:#1c1917; text-decoration:none; }
nav#toc > ol > li > a span { color:#78716c; font-weight:400; font-size:.85em; }
nav#toc ol ol { padding-left:1.2em; margin:.2em 0 .6em; }
nav#toc ol ol a { font-weight:400; color:#57534e; font-size:.9em; }

/* 章节头 */
.chapter-title { font-size:1.5em; font-weight:700; margin:1.2em 0 .2em; line-height:1.35;
  page-break-before:always; }
.sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden;
  clip:rect(0 0 0 0); white-space:nowrap; border:0; }
.chapter-span { color:#9a3412; letter-spacing:.2em; font-size:.9em; margin:0; }
.motto { margin:1.2em 0 1.8em; padding:.8em 1.1em; border-left:3px solid #9a3412;
  background:#f4eddf; font-style:italic; color:#5a4630; }

/* 章首图 + 图注 */
.chapter-art { margin:0 0 1.2em; text-align:center; page-break-inside:avoid; }
.chapter-art.page-break { page-break-before:always; }
.chapter-art img { width:100%; height:auto; border-radius:4px; }
.chapter-art figcaption { font-size:.85em; color:#78716c; margin-top:.4em; }
.chapter-art figcaption .zh { display:block; color:#57534e; }
.chapter-art figcaption .en { display:block; font-style:italic; color:#9a3412; }

/* 双语段落级交错（一段中文 + 一段英文，逐段对照） */
.subsection { margin:1.6em 0 .6em; padding-bottom:.4em; border-bottom:1px solid #e7e0d3;
  page-break-after:avoid; }
.subsection .zh { display:block; font-size:1.15em; font-weight:700; color:#1c1917; }
.subsection .en { display:block; font-family:Georgia,"Times New Roman",serif; font-style:italic;
  font-size:.85em; color:#9a3412; margin-top:.15em; }
.cn-para { margin:.8em 0 .25em; text-align:justify; color:#1c1917; }
.rebook-translation { margin:.25em 0 .9em; padding:.3em .6em .5em .8em;
  border-left:2px solid #ea580c; background:rgba(154,52,18,.045); border-radius:0 4px 4px 0; }
.en-para { font-family:Georgia,"Times New Roman",serif; font-size:.9em; color:#44403c;
  line-height:1.6; text-align:justify; margin:0; }
"""

COVER_XHTML = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head><meta charset="utf-8"/><title>封面</title><link rel="stylesheet" type="text/css" href="../Stylesheet.css"/></head>
<body>
<div class="cover-container">
<img class="cover-img" src="../Images/cover.jpg" alt="台积电张忠谋 · 传记时间线的平行世界 封面" epub:type="cover"/>
</div>
</body>
</html>
"""

TITLE_PAGE = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head><meta charset="utf-8"/><title>扉页</title><link rel="stylesheet" type="text/css" href="../Stylesheet.css"/></head>
<body>
<div class="title-page">
<p class="eyebrow">AIGC ORIGINAL · PARALLEL BIOGRAPHY</p>
<h1>台积电张忠谋<br/>传记时间线的平行世界</h1>
<p class="author">ReadShift · 平行叙事引擎 出品</p>
<div class="ornament">✦</div>
<div class="copyright">
本作品为 AIGC 原创，基于公开资料和史实创作加设计<br/>
同一时间线，另一个视角 · 全书一册 18 期 · 中英双语 · 典藏插图<br/>
仅供学习交流 · 禁止商业用途 · github.com/Martin-MQtech/ReadShift
</div>
</div>
</body>
</html>
"""

READING_GUIDE = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>阅读指南 · 双语对照与阅读设置</title>
<link rel="stylesheet" type="text/css" href="../Stylesheet.css"/>
<style>
.guide-box { max-width:38em; margin:0 auto; padding:1.1em 1.2em; }
.guide-header { text-align:center; margin-bottom:.6em; padding-bottom:.3em; border-bottom:1px solid #e7e0d3; }
.guide-eyebrow { font-size:.65em; letter-spacing:.18em; color:#9a3412; font-weight:700; text-transform:uppercase; display:block; margin-bottom:.2em; }
.guide-title { font-size:1.25em; font-weight:700; color:#1c1917; margin:0; }
.guide-section-title { font-size:.85em; font-weight:700; color:#9a3412; margin:.8em 0 .3em; }
.guide-table { width:100%; border-collapse:collapse; margin-bottom:.5em; font-size:.8em; }
.guide-table td { padding:.35em .5em; border:1px solid #e7e0d3; vertical-align:top; line-height:1.5; }
.guide-table .en { display:block; font-family:Georgia,"Times New Roman",serif; font-style:italic; font-size:.9em; color:#78716c; }
.guide-tip-card { padding:.5em .7em; border:1px solid #e7e0d3; border-radius:6px; font-size:.8em; line-height:1.55; margin-bottom:.4em; page-break-inside:avoid; }
.guide-tip-card__title { font-weight:700; color:#1c1917; margin-bottom:.15em; display:block; }
.guide-tip-card .en { display:block; font-family:Georgia,"Times New Roman",serif; font-style:italic; font-size:.9em; color:#78716c; margin-top:.1em; }
.guide-footer { font-size:.76em; color:#78716c; text-align:center; line-height:1.5; margin-top:.6em; padding-top:.5em; border-top:1px dashed #e7e0d3; }
</style>
</head>
<body>
<div class="guide-box">
<div class="guide-header">
<span class="guide-eyebrow">READER'S GUIDE</span>
<h2 class="guide-title">阅读指南 · 双语对照与阅读设置</h2>
</div>

<div class="guide-section-title">一、双语对照约定 · Bilingual Layout</div>
<table class="guide-table">
<tr><td style="width:26%; background:rgba(0,0,0,.02);"><b>中文正文</b></td><td>深色宋体，逐段叙述。<span class="en">Chinese text in dark serif.</span></td></tr>
<tr><td style="width:26%; background:rgba(154,52,18,.04);"><b>英文对照</b></td><td>紧跟每段中文下方，小一号 Georgia 衬线 + 焦橙左描边 + 淡底，可对照学习、也可跳过。<span class="en">English parallel text below each Chinese paragraph.</span></td></tr>
<tr><td style="width:26%; background:rgba(154,52,18,.04);"><b>章首图</b></td><td>每章一张暗黑金蓝章首插图，烙有章节数字与中英标题。<span class="en">One chapter-opener illustration per chapter.</span></td></tr>
<tr><td style="width:26%; background:rgba(37,99,235,.04);"><b>双层目录</b></td><td>侧边目录覆盖封面 / 扉页 / 阅读指南 / 全部章节与二级小节。<span class="en">Dual-level TOC in the reader sidebar.</span></td></tr>
</table>

<div class="guide-section-title">二、跨设备阅读设置建议 · Reader Settings</div>
<div class="guide-tip-card">
<span class="guide-tip-card__title">🍏 Apple Books（苹果图书 / iPhone / iPad / Mac）</span>
轻点屏幕中央呼出控制栏 → 点击右下角「≡ / AA」→ 在「页面翻动」中可选「仿真卷页 (Curl)」（还原纸质书翻页仪式感）或「垂直滚动」（单手滑屏）；Mac 电脑大屏默认呈现双页杂志级对开。
<span class="en">Tap the screen center → "≡ / AA" → Page Turn → Curl (paper-like) or Vertical Scroll.</span>
</div>
<div class="guide-tip-card">
<span class="guide-tip-card__title">🐧 微信读书 / Kindle / 多看阅读 等主流 App</span>
轻点屏幕中央呼出工具栏 → 点击「设置」→ 在「翻页方式」中选择「仿真」或「平移」，即可告别网页式下拉感，享受流式排版的纯正纸书翻阅质感。
<span class="en">Tap the screen center → Settings → Page Turn → Page-flip or Horizontal scroll.</span>
</div>

<div class="guide-footer">
<p>源起于文本，想象于无限。ReadShift 是一个开源的二次创作引擎——从纯文本出发，到多模态内容，连接思想与无限可能。</p>
<p>GitHub 开源仓库：https://github.com/Martin-MQtech/ReadShift</p>
</div>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    main()
