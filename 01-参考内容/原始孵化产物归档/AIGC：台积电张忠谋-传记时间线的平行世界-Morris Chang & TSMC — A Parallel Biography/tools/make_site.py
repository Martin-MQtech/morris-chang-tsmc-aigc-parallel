#!/usr/bin/env python3
"""
ReadShift 平行世界 · 作品官网生成器

把整部「一册 18 期」平行传记打包成一个可线上发布的自包含 HTML 官网首页:
    python3 tools/make_site.py            # 输出 作品官网.html 到项目根

内嵌封面 + 第 01–18 期章首插图（自动压缩转 JPG base64），单文件即可发布；
挂域名时把本文件改名为 index.html 放站点根目录即可。
"""
import base64
import html
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART_DIR = os.path.join(ROOT, "设计资产", "插图", "排版版")
COVER_PATH = os.path.join(ROOT, "设计资产", "封面", "封面_排版版.jpg")
OUT = os.path.join(ROOT, "作品官网.html")

# (期号, 短标题(与插图文件名一致), 时间范围, 一句话, 是否已上线)
EPISODES = [
    (1, "逃难的孩子", "1937–42", "一个孩子的记忆里，战争不是历史，是一张张搬家的船票。", "In a child's memory, war is not history — only one boat ticket after another.", True),
    (2, "考不进去的南开与作家梦", "1943–48", "一扇进不去的门，一支停不下的笔。", "A door that wouldn't open, a pen that wouldn't stop.", True),
    (3, "从黄浦江到查尔斯河", "1949–50", "一条发光的航线，横渡两个世界。", "One luminous route, crossing two worlds.", True),
    (4, "四十封求职信", "1954–58", "四十封信里，只有一封被点亮。", "Among forty letters, only one was lit.", True),
    (5, "隔岸观火的叛乱", "1957–68", "隔着一道玻璃墙，看别人的火。", "Watching another's fire through a wall of glass.", True),
    (6, "德仪的太空竞赛岁月", "1958–64", "一枚瞄准太空的硅片。", "A sliver of silicon aimed at space.", True),
    (7, "半导体之巅的十年", "1964–78", "在硅片堆成的山顶，独自站立。", "Standing alone at the summit of a silicon mountain.", True),
    (8, "离开德州与受邀回台", "1978–87", "一张空了的椅子，一束来自大洋彼岸的光。", "An empty chair, a light from across the ocean.", True),
    (9, "纯代工的革命", "1987–95", "颠覆者不做主角，做平台——让所有人成为主角。", "The disruptor takes no lead role — it builds the platform for everyone else.", True),
    (10, "从台湾到世界", "1995–98", "纽约的钟声，向世界荡开。", "The bell of New York, ringing out to the world.", True),
    (11, "记忆体的诱惑", "1998–2000", "巅峰前的最后一次心动：他说不再碰记忆体，却又被它吸引。", "One last temptation before the peak: he swore off memory chips, then was drawn back in.", True),
    (12, "逆周期的定力", "2001–03", "不景气，是挖人才最好的时候。", "A downturn is the best time to poach talent.", True),
    (13, "交棒之痛", "2003–09", "亲手把 CEO 交出去，又在风暴里亲手拿了回来。", "He gave away the CEO seat, then took it back in the storm.", True),
    (14, "绚烂年代", "2009–12", "28nm 之战、英伟达的披萨之夜——重回技术巅峰。", "The 28nm war and Nvidia's pizza night — a return to the summit.", True),
    (15, "苹果来敲门", "2010–14", "最挑剔的客户，逼出了最强的一家工厂。", "The pickiest client forged the strongest factory.", True),
    (16, "摩尔定律的守卫者", "2014–18", "摩尔定律变老时，他回答：追，追到只剩你一个。", "When Moore's Law grew old, he answered: keep chasing, until only you are left.", True),
    (17, "交棒与退休", "2013–18", "贝多芬第九响起时，全场起立鼓掌。", "When Beethoven's Ninth began, the entire hall rose to its feet.", True),
    (18, "护国神山", "2018–今天", "一家公司，如何成为一个岛屿的命运共同体。", "How one company became the shared destiny of an island.", True),
]

QUOTES = [
    ("颠覆者不做主角，做平台——让所有人成为主角。", "The disruptor takes no lead role — it builds the platform that makes everyone a star.", "第 09 期 · 纯代工的革命", "Ep. 09 · The Pure-Play Revolution"),
    ("被拒绝不是终点，是命运在给你指另一条路。", "Rejection is not the end — it is fate pointing you toward another road.", "第 04 期 · 四十封求职信", "Ep. 04 · Forty Job Applications"),
    ("有时候，离开一个错误的位置，是人生最重要的一步棋。", "Sometimes leaving the wrong position is the most important move of a life.", "第 08 期 · 离开德州 & 受邀回台", "Ep. 08 · Leaving Texas & the Call Home"),
    ("最难的仗，往往不在市场上，而在会议室里。", "The hardest battles are fought not in the market, but in the boardroom.", "第 07 期 · 半导体之巅的十年", "Ep. 07 · A Decade at the Summit"),
    ("当风暴来时，扎实的企业反而被看见。", "When the storm comes, it is the solid companies that get seen.", "第 10 期 · 从台湾到世界", "Ep. 10 · From Taiwan to the World"),
]


def img_data_uri(path, max_w=900, quality=80):
    """读取图片, 缩放到指定宽度并转 JPG, 返回 base64 data URI。"""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        h = max(1, int(im.height * max_w / im.width))
        im = im.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    cover_uri = img_data_uri(COVER_PATH, max_w=560, quality=84) if os.path.exists(COVER_PATH) else ""

    cards = []
    for num, title, span, teaser, en_teaser, done in EPISODES:
        art = os.path.join(ART_DIR, "第%02d期-%s.jpg" % (num, title))
        art_uri = img_data_uri(art, max_w=760, quality=82) if os.path.exists(art) else ""
        badge = ('<span class="badge on">已上线 <em>Live</em></span>' if done
                 else '<span class="badge soon">即将上线 <em>Soon</em></span>')
        cards.append(
            '<article class="card%s">\n'
            '  <div class="card-art">%s%s</div>\n'
            '  <div class="card-body">\n'
            '    <h3 class="sr-only">第 %02d 期 · %s · %s</h3>\n'
            '    <p class="teaser">%s<span class="en">%s</span></p>\n'
            '  </div>\n'
            '</article>' % (
                "" if done else " soon",
                ('<img src="%s" alt="第 %02d 期 · %s">' % (art_uri, num, html.escape(title))) if art_uri else "",
                badge,
                num, html.escape(title), html.escape(span),
                html.escape(teaser), html.escape(en_teaser),
            )
        )

    quotes_html = "\n".join(
        '<blockquote><p>%s<span class="en">%s</span></p><cite>%s · %s</cite></blockquote>'
        % (html.escape(q), html.escape(q_en), html.escape(src), html.escape(src_en))
        for q, q_en, src, src_en in QUOTES
    )

    doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>台积电张忠谋 · 传记时间线的平行世界</title>
<meta name="description" content="一册 18 期的原创平行传记：同一时间线，另一个视角。中英双语有声 · 典藏电子书 · AIGC 原创。">
<style>
:root { --bg:#0a0a0a; --bg2:#111113; --card:#16161a; --line:#26262b;
  --amber:#F59E0B; --blue:#38BDF8; --ink:#ece9e2; --muted:#a29c90; }
* { box-sizing:border-box; margin:0; padding:0; }
html { scroll-behavior:smooth; }
body { background:var(--bg); color:var(--ink);
  font-family:"PingFang SC","Microsoft YaHei",-apple-system,"Segoe UI",Roboto,sans-serif;
  line-height:1.8; -webkit-font-smoothing:antialiased; }
.serif { font-family:"Songti SC","Noto Serif SC","STSong",Georgia,serif; }
a { color:inherit; text-decoration:none; }
img { display:block; max-width:100%; }
.wrap { max-width:1180px; margin:0 auto; padding:0 6vw; }
.en { display:block; font-family:"Georgia","Times New Roman",serif; font-style:italic;
  font-size:.8em; color:var(--muted); letter-spacing:.02em; line-height:1.65; margin-top:4px; }
em { font-family:"Georgia","Times New Roman",serif; font-style:italic; font-size:.85em;
  color:var(--muted); letter-spacing:.02em; }
h1 .en, h2 .en, h3 .en { font-weight:400; margin-top:6px; }
h1 .en { font-size:clamp(15px,1.7vw,20px); margin-top:10px; }
.badge em { color:inherit; opacity:.85; margin-left:4px; }
.btn em { opacity:.72; font-size:.85em; margin-left:5px; }

/* ── 顶部导航 ── */
.nav { position:sticky; top:0; z-index:20; background:rgba(10,10,10,.82);
  backdrop-filter:blur(12px); border-bottom:1px solid var(--line); }
.nav-inner { max-width:1180px; margin:0 auto; padding:14px 6vw;
  display:flex; align-items:center; justify-content:space-between; }
.nav .brand { font-family:"Songti SC","Noto Serif SC",serif; letter-spacing:2px;
  font-size:15px; color:var(--ink); }
.nav .brand b { color:var(--amber); }
.nav .links { display:flex; gap:22px; font-size:13px; color:var(--muted); }
.nav .links a:hover { color:var(--amber); }

/* ── Hero ── */
.hero { min-height:88vh; display:flex; align-items:center;
  background:radial-gradient(1200px 600px at 78% -10%, rgba(245,158,11,.13), transparent 60%),
             radial-gradient(900px 500px at 8% 110%, rgba(56,189,248,.10), transparent 60%), var(--bg); }
.hero-inner { display:grid; grid-template-columns:1.08fr .92fr; gap:56px; align-items:center;
  max-width:1180px; margin:0 auto; padding:72px 6vw; }
.eyebrow { font-size:12px; letter-spacing:5px; color:var(--amber); text-transform:uppercase;
  margin-bottom:22px; }
.hero h1 { font-size:clamp(34px,5.2vw,60px); line-height:1.22; font-weight:600; letter-spacing:2px; }
.hero h1 .thin { color:var(--muted); font-weight:400; }
.hero .tagline { margin-top:22px; font-size:18px; color:var(--muted); letter-spacing:3px; }
.hero .stats { display:flex; flex-wrap:wrap; gap:12px; margin-top:34px; }
.hero .stat { padding:10px 18px; border:1px solid var(--line); border-radius:100px;
  font-size:13px; color:var(--muted); letter-spacing:1px; }
.hero .stat b { color:var(--ink); font-weight:600; }
.hero .cta { display:flex; flex-wrap:wrap; gap:14px; margin-top:36px; }
.btn { display:inline-block; padding:13px 28px; border-radius:100px; font-size:15px;
  letter-spacing:1px; transition:.2s; }
.btn.primary { background:linear-gradient(135deg,var(--amber),#d97706); color:#1a1205; font-weight:600; }
.btn.primary:hover { transform:translateY(-2px); box-shadow:0 10px 30px rgba(245,158,11,.28); }
.btn.ghost { border:1px solid var(--line); color:var(--ink); }
.btn.ghost:hover { border-color:var(--amber); color:var(--amber); }
.hero-cover { justify-self:center; }
.hero-cover img { width:min(60vw,360px); border-radius:10px;
  box-shadow:0 30px 90px rgba(0,0,0,.6), 0 0 0 1px var(--line); }
.hero-cover .glow { margin-top:-6px; height:2px; width:70%; margin-left:15%;
  background:linear-gradient(90deg,transparent,var(--amber),var(--blue),transparent); opacity:.7; }

/* ── 通用 section ── */
.section { padding:96px 0; }
.section-head { text-align:center; margin-bottom:56px; }
.section-head .kicker { font-size:12px; letter-spacing:5px; color:var(--amber);
  text-transform:uppercase; margin-bottom:14px; }
.section-head h2 { font-size:clamp(26px,3.4vw,40px); font-weight:600; letter-spacing:2px; }
.section-head .sub { margin-top:14px; color:var(--muted); font-size:15px; }

/* ── 概念 ── */
.concept { background:var(--bg2); border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
.tracks { display:grid; grid-template-columns:1fr 1fr; gap:0; max-width:900px; margin:0 auto;
  border:1px solid var(--line); border-radius:14px; overflow:hidden; }
.track { padding:40px 36px; }
.track.amber { background:linear-gradient(160deg, rgba(245,158,11,.12), transparent 55%); }
.track.blue { background:linear-gradient(200deg, rgba(56,189,248,.10), transparent 55%); }
.track .t-label { font-size:12px; letter-spacing:4px; margin-bottom:16px; }
.track.amber .t-label { color:var(--amber); }
.track.blue .t-label { color:var(--blue); }
.track h3 { font-family:"Songti SC","Noto Serif SC",serif; font-size:22px; font-weight:600; margin-bottom:12px; }
.track p { color:var(--muted); font-size:14.5px; }
.concept-note { max-width:760px; margin:44px auto 0; text-align:center; color:var(--muted); font-size:15px; }

/* ── 18期卡片 ── */
.grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:26px; }
.card { background:var(--card); border:1px solid var(--line); border-radius:14px; overflow:hidden;
  transition:.25s; }
.card:hover { transform:translateY(-5px); border-color:#3a3a40;
  box-shadow:0 20px 50px rgba(0,0,0,.5); }
.card.soon { opacity:.72; }
.card-art { position:relative; aspect-ratio:3/2; overflow:hidden; background:#000; }
.card-art img { width:100%; height:100%; object-fit:cover; }
.card-art .badge { position:absolute; top:12px; left:12px; margin-left:0;
  background:rgba(10,10,10,.72); backdrop-filter:blur(4px); }
.card-body { padding:18px 22px 22px; }
.card-body .teaser { font-family:"Songti SC","Noto Serif SC",serif; font-size:14.5px; color:var(--muted); line-height:1.75; }
.sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0; }
.card-meta { display:flex; align-items:center; gap:12px; margin-bottom:10px; flex-wrap:wrap; }
.card-meta .num { font-size:12px; letter-spacing:2px; color:var(--amber); font-weight:600; }
.card-meta .span { font-size:12px; color:var(--muted); letter-spacing:1px; }
.badge { font-size:11px; padding:2px 10px; border-radius:100px; letter-spacing:1px; margin-left:auto; }
.badge.on { background:rgba(245,158,11,.15); color:var(--amber); }
.badge.soon { background:rgba(56,189,248,.12); color:var(--blue); }
.card h3 { font-family:"Songti SC","Noto Serif SC",serif; font-size:19px; font-weight:600; margin-bottom:8px; }
.card p { font-size:14px; color:var(--muted); line-height:1.7; }

/* ── 特色 ── */
.features { display:grid; grid-template-columns:repeat(auto-fit, minmax(220px,1fr)); gap:22px; }
.feature { padding:32px 28px; border:1px solid var(--line); border-radius:14px; background:var(--bg2); }
.feature .ico { font-size:26px; margin-bottom:16px; }
.feature h3 { font-size:17px; font-weight:600; margin-bottom:10px; }
.feature p { font-size:13.5px; color:var(--muted); }

/* ── 金句 ── */
.quotes { max-width:820px; margin:0 auto; display:grid; gap:20px; }
.quotes blockquote { padding:30px 34px; border-left:3px solid var(--amber);
  background:var(--bg2); border-radius:0 12px 12px 0; }
.quotes blockquote p { font-family:"Songti SC","Noto Serif SC",serif; font-size:21px;
  line-height:1.7; color:var(--ink); }
.quotes blockquote cite { display:block; margin-top:14px; font-size:12.5px; font-style:normal;
  color:var(--amber); letter-spacing:2px; }

/* ── CTA ── */
.final { text-align:center; background:radial-gradient(700px 400px at 50% 0%, rgba(245,158,11,.12), transparent 65%), var(--bg); }
.final h2 { font-size:clamp(26px,3.4vw,38px); font-weight:600; letter-spacing:2px; margin-bottom:16px; }
.final p { color:var(--muted); margin-bottom:36px; }

/* ── 页脚 ── */
.footer { border-top:1px solid var(--line); padding:56px 0 64px; color:var(--muted); font-size:13px; }
.footer-inner { max-width:1180px; margin:0 auto; padding:0 6vw; }
.footer .f-top { display:flex; justify-content:space-between; gap:24px; flex-wrap:wrap; margin-bottom:28px; }
.footer .f-brand { font-family:"Songti SC","Noto Serif SC",serif; letter-spacing:2px; color:var(--ink); }
.footer .f-links { display:flex; gap:20px; flex-wrap:wrap; }
.footer .f-links a:hover { color:var(--amber); }
.footer .f-note { border-top:1px solid var(--line); padding-top:22px; line-height:1.9; }

@media (max-width:820px) {
  .hero-inner { grid-template-columns:1fr; gap:40px; padding:56px 6vw; }
  .hero-cover { order:-1; }
  .hero-cover img { width:min(70vw,300px); }
  .tracks { grid-template-columns:1fr; }
}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <div class="brand">平行世界 · 张忠谋 <em>Parallel Worlds · Morris Chang</em></div>
    <div class="links">
      <a href="#concept">概念 <em>Concept</em></a>
      <a href="#episodes">十八期 <em>Episodes</em></a>
      <a href="#features">双语 <em>Bilingual</em></a>
      <a href="#quotes">金句 <em>Quotes</em></a>
    </div>
  </div>
</nav>

<header class="hero">
  <div class="hero-inner">
    <div>
      <div class="eyebrow">AIGC 原创平行传记 · 中英双语有声 <em>Original Parallel Biography · Bilingual Audio</em></div>
      <h1>台积电张忠谋<br><span class="thin">传记时间线的平行世界</span><span class="en">Morris Chang &amp; TSMC — The Parallel Worlds of a Biography</span></h1>
      <p class="tagline">同一时间线，另一个视角 <em>Same timeline, another view.</em></p>
      <div class="stats">
        <span class="stat"><b>18</b> 期 · 一册 <em>Episodes</em></span>
        <span class="stat"><b>1931</b> – 今天 <em>Today</em></span>
        <span class="stat">中英 <b>双语</b> <em>Bilingual</em></span>
        <span class="stat"><b>AIGC</b> 原创 <em>Original</em></span>
      </div>
      <div class="cta">
        <a class="btn primary" href="#episodes">浏览全部 18 期 <em>Browse All</em></a>
        <a class="btn ghost" href="全册电子书.html">进入典藏电子书 <em>Open the Ebook</em></a>
      </div>
    </div>
    <div class="hero-cover">
      __COVER__
      <div class="glow"></div>
    </div>
  </div>
</header>

<section class="section concept" id="concept">
  <div class="section-head">
    <div class="kicker">平行叙事 · Parallel Narrative</div>
    <h2>什么是「平行世界」<span class="en">What is “Parallel Worlds”?</span></h2>
    <p class="sub">一条人生线，一条世界线——在同一个时间刻度上，平行展开。<span class="en">One lifeline, one world line — unfolding in parallel on the same clock.</span></p>
  </div>
  <div class="tracks">
    <div class="track amber">
      <div class="t-label">他这一年 <em>His Year</em></div>
      <h3>一个人的抉择 <span class="en">One Man’s Choices</span></h3>
      <p>张忠谋从战乱中的孩子，到半导体工程师，再到台积电的创办人——每一次押上自己，都改写了命运的走向。<span class="en">From a child of war to a semiconductor engineer, to the founder of TSMC — every time he bet on himself, he rewrote the course of his fate.</span></p>
    </div>
    <div class="track blue">
      <div class="t-label">世界这一年 <em>The World’s Year</em></div>
      <h3>一个时代的洪流 <span class="en">The Tide of an Era</span></h3>
      <p>太空竞赛、半导体革命、全球化、AI 浪潮——大时代是看不见的手，把他一次次推上风口。<span class="en">The space race, the semiconductor revolution, globalization, the AI wave — an invisible hand that kept pushing him into the wind.</span></p>
    </div>
  </div>
  <p class="concept-note">不翻译原书、不复述史实，而是以第三方视角，把一段传奇重讲给你听——这就是「平行叙事」。<span class="en">No translating the original book, no retelling the history — only a legend retold from a third-person view. That is “parallel narrative.”</span></p>
</section>

<section class="section" id="episodes">
  <div class="section-head">
    <div class="kicker">十八期 · 18 Episodes</div>
    <h2>一册 · 十八期<span class="en">One Volume · 18 Episodes</span></h2>
    <p class="sub">1931 – 今天 · 每期 20 分钟 · 中英双轨 · 音频 + 文字稿 + 电子书一章<span class="en">1931 – Today · 20 min per episode · Chinese &amp; English audio · audio + script + one ebook chapter</span></p>
  </div>
  <div class="wrap">
    <div class="grid">
__CARDS__
    </div>
  </div>
</section>

<section class="section" id="features" style="padding-top:0;">
  <div class="wrap">
    <div class="features">
      <div class="feature"><div class="ico">🎧</div><h3>中英双轨音频 <span class="en">Bilingual Audio</span></h3><p>每期中文 + 英文各约 20 分钟，沉稳旁白，通勤与睡前皆宜。<span class="en">~20 minutes each in Chinese and English — steady narration for commutes and bedtime.</span></p></div>
      <div class="feature"><div class="ico">📖</div><h3>典藏电子书 <span class="en">Collector’s Ebook</span></h3><p>18 期 = 18 章，双语正文 + 章首插图 + 金句，单文件即可读。<span class="en">18 episodes = 18 chapters — bilingual text + chapter art + quotes, all in one file.</span></p></div>
      <div class="feature"><div class="ico">🕰️</div><h3>平行时刻 <span class="en">Parallel Moments</span></h3><p>「他这一年 ‖ 世界这一年」双轨对照，把人生放进大时代里看。<span class="en">“His year ‖ The world’s year” side by side — a life seen inside its era.</span></p></div>
      <div class="feature"><div class="ico">🗣️</div><h3>边听边学英语 <span class="en">Learn by Listening</span></h3><p>词汇卡 + 金句跟读，把一段传奇听成你的英语课。<span class="en">Vocabulary cards + quote shadowing — turn a legend into your English class.</span></p></div>
    </div>
  </div>
</section>

<section class="section" id="quotes" style="padding-top:0;">
  <div class="section-head">
    <div class="kicker">金句 · Quotes</div>
    <h2>金句<span class="en">Quotes</span></h2>
  </div>
  <div class="wrap"><div class="quotes">
__QUOTES__
  </div></div>
</section>

<section class="section final">
  <div class="wrap">
    <h2>从一个人的故事，读一个时代<span class="en">Read an era through one man’s story</span></h2>
    <p>同一时间线，另一个视角。<em>Same timeline, another view.</em></p>
    <a class="btn primary" href="全册电子书.html">打开典藏电子书 <em>Open the Ebook</em></a>
  </div>
</section>

<footer class="footer">
  <div class="footer-inner">
    <div class="f-top">
      <div class="f-brand">台积电张忠谋 · 传记时间线的平行世界 <em>Morris Chang &amp; TSMC — The Parallel Worlds of a Biography</em></div>
      <div class="f-links">
        <a href="全册电子书.html">电子书 <em>Ebook</em></a>
        <a href="平行世界地图.html">时间轴地图 <em>Timeline</em></a>
        <a href="金句知识卡片.html">金句卡片 <em>Quote Cards</em></a>
      </div>
    </div>
    <div class="f-note">
      本作品为 AIGC 原创，基于公开资料和史实创作加设计 · 仅供学习交流，禁止商业用途。<br>
      <em>This work is AIGC-original, created and designed from public materials and historical facts · For learning and exchange only, not for commercial use.</em><br>
      github.com/Martin-MQtech/ReadShift<br>
      © 2026 ReadShift · 平行叙事引擎出品 · Powered by the Parallel Narrative Engine
    </div>
  </div>
</footer>

</body>
</html>
"""

    doc = doc.replace("__COVER__", ('<img src="%s" alt="封面">' % cover_uri) if cover_uri else "")
    doc = doc.replace("__CARDS__", "\n".join(cards))
    doc = doc.replace("__QUOTES__", quotes_html)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print("生成:", OUT)
    print("期数:", len(EPISODES), "| 大小:", round(os.path.getsize(OUT) / 1024 / 1024, 2), "MB")


if __name__ == "__main__":
    main()
