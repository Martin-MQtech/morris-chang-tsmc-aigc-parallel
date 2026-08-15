#!/usr/bin/env python3
"""
ReadShift 平行世界 · 全册电子书生成器

读取 03-剧集/ 下第 01–18 期的中英文字稿（第 11–18 期完成后自动并入）, 清洗舞台标记后,
生成一份自包含的杂志级双语 HTML 电子书（无外部依赖）:
    python3 tools/make_ebook.py            # 输出 全册电子书.html 到项目根

v4: 全站中英双语——目录（中英标题）、金句（中英对照）、章标题、页脚全部双语；
    正文「一段中文 + 一段英文」段落级交错（逐段对照）；内嵌封面 + 章首插图 + 中英图注。
"""

import base64
import html
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP_DIR = os.path.join(ROOT, "03-剧集")
ART_DIR = os.path.join(ROOT, "设计资产", "插图")
COVER_PATH = os.path.join(ROOT, "设计资产", "封面", "封面_排版版.jpg")
OUT = os.path.join(ROOT, "全册电子书.html")

# 每期元数据: (文件夹名, 中文章标题, 英文章标题, 时间范围, 中文金句, 英文金句, 图注中文, 图注英文)
EPISODES = [
    ("第01期-逃难的孩子", "第 01 期 · 逃难的孩子", "The Child Who Fled", "1937–1942",
     "一个孩子的记忆里，战争不是历史，是一张张搬家的船票。",
     "In a child's memory, war is not history — only one boat ticket after another.",
     "一只太早打包的箱子", "A suitcase packed too early"),
    ("第02期-考不进去的南开与作家梦", "第 02 期 · 考不进去的南开 & 作家梦", "The Closed Door & the Writer's Dream", "1943–1948",
     "关系可以给你一张门票，但只有实力，能让你一直坐在场上；而那个被按下去的梦，教会他如何记得自己是谁。",
     "Connections can hand you a ticket, but only ability keeps you on the field — and the dream that was pushed down taught him to remember who he is.",
     "一扇进不去的门，一支停不下的笔", "A closed door, an unstoppable pen"),
    ("第03期-从黄浦江到查尔斯河", "第 03 期 · 从黄浦江到查尔斯河", "From the Huangpu River to the Charles", "1949–1950",
     "他不知道，这一走，他和那个时代许多知识分子一样，把离开当成了暂时，却走出了一条不归路。",
     "He did not know that, like so many intellectuals of his generation, he was treating a permanent farewell as a temporary one — and stepping onto a road with no return.",
     "一条发光的航线，横渡两个世界", "One luminous route across two worlds"),
    ("第04期-四十封求职信", "第 04 期 · 四十封求职信", "Forty Job Applications", "1954–1958",
     "被拒绝不是终点，是命运在给你指另一条路——只是当时没人知道，这条路通向半导体。",
     "Rejection is not the end — it is fate pointing you toward another road. Only no one knew then that the road led to semiconductors.",
     "四十封信里，只有一封被点亮", "One reply among forty"),
    ("第05期-隔岸观火的叛乱", "第 05 期 · 隔岸观火的叛乱", "Watching the Rebellion from Across the Water", "1957–1968",
     "他隔着半个美国看完的那场叛乱，后来成了他自己的剧本——只是他的舞台，在台湾。",
     "The rebellion he watched from half a country away would one day become his own script — only his stage was Taiwan.",
     "隔着一道玻璃墙，看别人的火", "Watching another's fire through glass"),
    ("第06期-德仪的太空竞赛岁月", "第 06 期 · 德仪的太空竞赛岁月", "The Space-Race Years at Texas Instruments", "1958–1964",
     "他在一家赌上太空竞赛的公司里，学会了什么叫技术的信仰；而真正的强者，敢于在上升期把自己清零。",
     "At a company betting everything on the space race, he learned what faith in technology means — and the truly strong dare to reset themselves to zero in mid-ascent.",
     "一枚瞄准太空的硅片", "Silicon aimed at space"),
    ("第07期-半导体之巅的十年", "第 07 期 · 半导体之巅的十年", "A Decade at the Summit of Semiconductors", "1964–1978",
     "最难的仗，往往不在市场上，而在会议室里。",
     "The hardest battles are fought not in the market, but in the boardroom.",
     "在硅片堆成的山顶，独自站立", "Standing alone atop a summit of silicon"),
    ("第08期-离开德州与受邀回台", "第 08 期 · 离开德州 & 受邀回台", "Leaving Texas & the Call Home", "1978–1987",
     "有时候，离开一个错误的位置，是人生最重要的一步棋；归乡者的赌注——他押的不是自己的余生，是一个产业的未来。",
     "Sometimes leaving the wrong position is the most important move of a life — and a homecomer's wager: he was betting not his remaining years, but the future of an industry.",
     "一张空了的椅子，一束来自大洋彼岸的光", "An empty chair, a call across the ocean"),
    ("第09期-纯代工的革命", "第 09 期 · 纯代工的革命", "The Pure-Play Revolution", "1987–1995",
     "颠覆者不做主角，做平台——让所有人成为主角。",
     "The disruptor takes no lead role — it builds the platform that makes everyone a star.",
     "一座为所有人而建、却空着主角的舞台", "A stage built for everyone but the builder"),
    ("第10期-从台湾到世界", "第 10 期 · 从台湾到世界", "From Taiwan to the World", "1995–1998",
     "当风暴来时，扎实的企业反而被看见。",
     "When the storm comes, it is the solid companies that get seen.",
     "纽约的钟声，向世界荡开", "The bell of New York, ringing across the world"),
    ("第11期-记忆体的诱惑", "第 11 期 · 记忆体的诱惑", "The Memory Temptation", "1998–2000",
     "诱惑之所以是诱惑，是因为它长得像机会；真正的强者，是在狂欢里还能听见周期钟声的人。",
     "Temptation is temptation because it looks like an opportunity; the truly strong can still hear the clock of the cycle amid the revelry.",
     "一颗诱人却危险的晶体", "A beautiful, dangerous crystal"),
    ("第12期-逆周期的定力", "第 12 期 · 逆周期的定力", "Resolve Against the Cycle", "2001–2003",
     "周期不是用来恐惧的，是用来踩节奏的；定力，是一个领导者最昂贵的资产。",
     "The cycle is not something to fear but something to time; steadiness is a leader's most expensive asset.",
     "逆流而上的一道光柱", "A column of light rising against the stream"),
    ("第13期-交棒之痛", "第 13 期 · 交棒之痛", "The Pain of the Handover", "2003–2009",
     "把权力交出去需要勇气，把它拿回来需要更大的勇气——而两次，都是为了同一家公司。",
     "It takes courage to give power away, and greater courage to take it back — and both times, for the same company.",
     "悬在半空的权杖", "A scepter caught mid-exchange"),
    ("第14期-绚烂年代", "第 14 期 · 绚烂年代", "The Splendid Years", "2009–2012",
     "老骥伏枥，志在千里——年龄从不决定一个人还能不能战斗，只决定他敢不敢再上战场。",
     "An old steed in the stable still aspires to a thousand li — age never decides whether a man can still fight, only whether he dares to return to the battlefield.",
     "一颗散发光芒的硅片", "A chip radiating brilliance"),
    ("第15期-苹果来敲门", "第 15 期 · 苹果来敲门", "Apple Comes Knocking", "2010–2014",
     "最挑剔的客户，是最好的磨刀石——它逼你长出别人没有的能力。",
     "The most demanding customer is the best whetstone — it forces you to grow abilities no one else has.",
     "门上落下的苹果光斑", "An apple-shaped light on the door"),
    ("第16期-摩尔定律的守卫者", "第 16 期 · 摩尔定律的守卫者", "Guardian of Moore's Law", "2014–2018",
     "摩尔定律的尽头，站着的是最后还愿意奔跑的人。",
     "At the end of Moore's Law stands the one still willing to run.",
     "越走越窄的阶梯", "A staircase thinning toward the summit"),
    ("第17期-交棒与退休", "第 17 期 · 交棒与退休", "The Handover & Retirement", "2013–2018",
     "真正的传承，不是找一个像自己的人，而是把公司交给一套比个人更持久的制度。",
     "True succession is not finding someone who resembles you, but handing the company to a system more lasting than any individual.",
     "轻轻放下的指挥棒", "A baton laid gently to rest"),
    ("第18期-护国神山", "第 18 期 · 护国神山", "The Mountain That Shields the Island", "2018–今天",
     "一座「护国神山」，从来不是一个人搬上去的，而是一代人的选择，被时间砌成了山。",
     "A 'sacred mountain' is never carried up by one person — it is a generation's choices, laid into a mountain by time.",
     "一座硅晶体巨山", "A mountain of silicon crystal"),
]

STAGE = re.compile(r"^【|^\[SFX|^\[Main\s+narrator|^\[Narrator|^\[主叙述者")


def img_data_uri(path, max_w=1400, quality=82):
    """读取图片, 缩放到指定宽度并转 JPG, 返回 base64 data URI（自包含内嵌）。"""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        h = max(1, int(im.height * max_w / im.width))
        im = im.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def parse_sections(path):
    """解析文字稿 → [(小节标题, [段落]), ...]，跳过舞台标记/下期预告。"""
    sections = []
    cur_head, cur_paras = None, []
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for line in lines:
        s = line.strip()
        if not s:
            continue
        m = re.match(r"^##\s+(.*)", s)
        if m:
            head = m.group(1).strip()
            if "预告" in head or "Next Episode" in head or "Preview" in head:
                break
            if cur_head is not None or cur_paras:
                sections.append((cur_head, cur_paras))
            cur_head, cur_paras = head, []
            continue
        if re.match(r"^#\s", s):
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


def interleave_html(zh_sections, en_sections, base_id):
    """中英段落级交错 → HTML。返回 (html, [(小节id, 中文标题, 英文标题), ...])。"""
    out = []
    toc = []
    n = max(len(zh_sections), len(en_sections))
    for i in range(n):
        zh_head, zh_paras = zh_sections[i] if i < len(zh_sections) else (None, [])
        en_head, en_paras = en_sections[i] if i < len(en_sections) else (None, [])
        sid = "%s-%d" % (base_id, i + 1)
        if zh_head or en_head:
            toc.append((sid, zh_head or "", en_head or ""))
        if zh_head or en_head:
            zs = ('<span class="zh">%s</span>' % html.escape(zh_head)) if zh_head else ""
            es = ('<span class="en">%s</span>' % html.escape(en_head)) if en_head else ""
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
                out.append('<p class="cn-para">%s</p>' % html.escape(zh_paras[j]))
            if j < len(en_paras):
                out.append('<div class="rebook-translation">'
                           '<p class="en-para">%s</p></div>' % html.escape(en_paras[j]))
    return "\n".join(out), toc


def main():
    chapters = []
    toc_links = []
    for folder, title, en_title, span, motto, en_motto, cap_zh, cap_en in EPISODES:
        zh = os.path.join(EP_DIR, folder, "中文文字稿.md")
        en = os.path.join(EP_DIR, folder, "英文文字稿.md")
        art = os.path.join(ART_DIR, folder + ".png")
        zh_sections = parse_sections(zh) if os.path.exists(zh) else []
        en_sections = parse_sections(en) if os.path.exists(en) else []
        num = len(chapters) + 1
        body_html, _ = interleave_html(zh_sections, en_sections, "sub-%02d" % num)
        chapters.append({
            "title": title, "en_title": en_title, "span": span,
            "motto": motto, "en_motto": en_motto,
            "cap_zh": cap_zh, "cap_en": cap_en,
            "art": img_data_uri(art, max_w=1600, quality=88) if os.path.exists(art) else "",
            "body": body_html,
        })
        toc_links.append(
            '<a href="#ch%d"><span class="toc-txt">'
            '<span class="zh">%s</span><span class="en">%s</span></span>'
            '<span class="toc-span">%s</span></a>'
            % (num, title, en_title, span))

    cover_uri = img_data_uri(COVER_PATH, max_w=1100, quality=90) if os.path.exists(COVER_PATH) else ""

    body = []
    body.append('<section class="cover">')
    if cover_uri:
        body.append('<img class="cover-img" src="%s" alt="封面：台积电张忠谋 · 传记时间线的平行世界">' % cover_uri)
    body.append('<h1 class="book-title">'
                '<span class="zh">台积电张忠谋</span>'
                '<span class="zh-sub">传记时间线的平行世界</span>'
                '<span class="en">Morris Chang &amp; TSMC — A Parallel Biography</span></h1>')
    body.append('<p class="tagline"><span class="zh">同一时间线，另一个视角</span>'
                '<span class="en">Same timeline, another view.</span></p>')
    body.append('<p class="meta"><span class="zh">一册 · 十八期 · 1931–今天 · 中英双语</span>'
                '<span class="en">One Volume · 18 Episodes · 1931–Today · Bilingual</span></p>')
    body.append('</section>')
    body.append('<nav class="toc"><h2><span class="zh">目录</span><span class="en">Contents</span></h2>'
                + "\n".join(toc_links) + '</nav>')

    for i, c in enumerate(chapters, 1):
        body.append('<section class="chapter" id="ch%d">' % i)
        body.append('<header class="ch-head">'
                    '<h2><span class="zh">%s</span><span class="en">%s</span></h2>'
                    '<p class="ch-span">%s</p></header>'
                    % (c["title"], c["en_title"], c["span"]))
        if c["art"]:
            body.append('<figure class="chapter-art">'
                        '<img src="%s" alt="%s">' % (c["art"], html.escape(c["title"])))
            body.append('<figcaption><span class="zh">%s</span>'
                        '<span class="en">%s</span></figcaption>' % (html.escape(c["cap_zh"]), html.escape(c["cap_en"])))
            body.append('</figure>')
        body.append('<blockquote class="motto">'
                    '<span class="zh">%s</span><span class="en">%s</span></blockquote>'
                    % (html.escape(c["motto"]), html.escape(c["en_motto"])))
        body.append(c["body"])
        body.append('</section>')

    doc = DOC_TEMPLATE.replace("__BODY__", "\n".join(body))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print("生成:", OUT)
    print("章数:", len(chapters), "| 大小:", round(os.path.getsize(OUT) / 1024 / 1024, 2), "MB")


DOC_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>台积电张忠谋 · 传记时间线的平行世界 · 全册 · Morris Chang & TSMC — A Parallel Biography</title>
<style>
:root { --ink:#1c1917; --sub:#78716c; --accent:#9a3412; --accent-strong:#ea580c; --paper:#faf8f3; --line:#e7e0d3; }
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink);
  font-family:"Songti SC","Noto Serif SC","STSong",Georgia,"Times New Roman",serif;
  line-height:1.9; font-size:17px; }
.wrap { max-width:760px; margin:0 auto; padding:0 28px 80px; }
.sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0; }
.en { font-family:Georgia,"Times New Roman",serif; font-style:italic; }
.cover { text-align:center; padding:56px 0 64px; }
.cover-img { width:min(80vw,540px); max-width:100%; height:auto; border-radius:6px;
  box-shadow:0 16px 48px rgba(0,0,0,.35); display:block; margin:0 auto 40px; }
.book-title { margin:0; }
.book-title .zh { display:block; font-size:34px; letter-spacing:5px; line-height:1.5; font-weight:600; }
.book-title .zh-sub { display:block; font-size:21px; letter-spacing:4px; color:var(--accent); margin-top:6px; }
.book-title .en { display:block; font-size:14px; color:var(--sub); letter-spacing:1px; margin-top:12px; }
.cover .tagline { margin:20px 0 0; }
.cover .tagline .zh { display:block; font-size:16px; letter-spacing:3px; color:#57534e; }
.cover .tagline .en { display:block; font-size:13px; color:var(--sub); margin-top:3px; }
.cover .meta { margin:16px 0 0; }
.cover .meta .zh { display:block; font-size:13px; letter-spacing:2px; color:var(--accent); }
.cover .meta .en { display:block; font-size:12px; color:var(--sub); letter-spacing:1px; margin-top:3px; }

.toc { padding:32px 0; border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
.toc h2 { font-size:20px; letter-spacing:6px; text-align:center; color:var(--accent); margin:0 0 22px; }
.toc h2 .zh { display:block; }
.toc h2 .en { display:block; font-size:13px; letter-spacing:2px; color:var(--sub); margin-top:2px; }
.toc a { display:flex; align-items:center; gap:14px; padding:11px 2px; color:var(--ink);
  text-decoration:none; border-bottom:1px dotted var(--line); }
.toc .toc-txt { flex:1; }
.toc .toc-txt .zh { display:block; }
.toc .toc-txt .en { display:block; font-size:13px; color:var(--sub); margin-top:1px; }
.toc .toc-span { color:var(--accent); font-size:13px; letter-spacing:1px; white-space:nowrap; }

.chapter { padding:56px 0 24px; border-bottom:1px solid var(--line); }
.ch-head { margin:0 0 4px; }
.ch-head h2 { margin:0; }
.ch-head h2 .zh { display:block; font-size:26px; letter-spacing:2px; font-weight:600; }
.ch-head h2 .en { display:block; font-size:15px; color:var(--accent); margin-top:3px; }
.ch-head .ch-span { margin:6px 0 0; color:var(--accent); letter-spacing:3px; font-size:14px; }
.chapter-art { margin:26px 0 10px; }
.chapter-art img { width:100%; height:auto; border-radius:6px;
  box-shadow:0 8px 28px rgba(0,0,0,.28); display:block; }
.chapter-art figcaption { margin:12px 0 0; font-size:14px; line-height:1.6; color:var(--sub); }
.chapter-art figcaption .zh { display:block; color:#57534e; }
.chapter-art figcaption .en { display:block; color:var(--accent); }

.motto { margin:22px 0 30px; padding:14px 20px; border-left:3px solid var(--accent);
  background:#f4eddf; }
.motto .zh { display:block; color:#5a4630; font-style:italic; }
.motto .en { display:block; font-size:14px; color:var(--sub); margin-top:6px; }

/* 双语段落级交错 */
.subsection { margin:34px 0 8px; padding-bottom:6px; border-bottom:1px solid var(--line); }
.subsection .zh { display:block; font-size:20px; font-weight:600; color:var(--ink); }
.subsection .en { display:block; font-size:14px; color:var(--accent); margin-top:2px; }
.cn-para { margin:16px 0 4px; text-align:justify; color:var(--ink); }
.rebook-translation { margin:4px 0 16px; padding:6px 12px 9px 14px;
  border-left:3px solid var(--accent-strong); background:rgba(154,52,18,.045); border-radius:0 5px 5px 0; }
.en-para { font-family:Georgia,"Times New Roman",serif; font-size:15px; line-height:1.7;
  color:#44403c; text-align:justify; margin:0; }

.footer { text-align:center; color:var(--sub); padding:48px 0 24px; font-size:14px; letter-spacing:2px; }
.footer .en { display:block; font-size:12.5px; letter-spacing:1px; margin-top:8px; }
@media print { body{background:#fff} .chapter{page-break-before:always} }
</style>
</head>
<body>
<div class="wrap">
__BODY__
<div class="footer">
台积电张忠谋 · 传记时间线的平行世界 · 全册 · 1931–今天
<span class="en">Morris Chang &amp; TSMC · The Parallel Worlds of a Biography · One Volume · 1931–Today</span>
本作品为 AIGC 原创，基于公开资料和史实创作加设计 · 仅供学习交流，禁止商业用途。
<span class="en">This work is AIGC-original, created and designed from public materials and historical facts · For learning and exchange only, not for commercial use.</span>
github.com/Martin-MQtech/ReadShift
</div>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    main()
