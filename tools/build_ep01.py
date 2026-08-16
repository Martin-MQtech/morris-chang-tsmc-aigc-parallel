import json
import re
import html

# Load audio_data.js cues
with open("/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC/audio_data.js", "r", encoding="utf-8") as f:
    js = f.read()

ep01_match = re.search(r'\{\s*"id":\s*"01".*?"cues":\s*(\[.*?\])\s*\}', js, re.DOTALL)
cues = json.loads(ep01_match.group(1))

# Load markdown texts
def parse_markdown_sections(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
    
    sections = []
    cur_sec = None
    cur_paras = []
    
    for l in lines:
        if l.startswith("## "):
            if cur_sec is not None:
                sections.append((cur_sec, cur_paras))
            cur_sec = l[3:].strip()
            cur_paras = []
        elif l.startswith("# ") or l.startswith("> ") or l == "---" or not l:
            continue
        else:
            cur_paras.append(l)
            
    if cur_sec is not None:
        sections.append((cur_sec, cur_paras))
    return sections

zh_sections = parse_markdown_sections("/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC/03-剧集/第01期-逃难的孩子/中文文字稿.md")
en_sections = parse_markdown_sections("/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC/03-剧集/第01期-逃难的孩子/英文文字稿.md")

print(f"ZH sections: {len(zh_sections)}, EN sections: {len(en_sections)}")

# Build HTML
cues_json_str = json.dumps(cues, ensure_ascii=False)

story_html_parts = []
global_p_idx = 0

for sec_i in range(6):
    z_title, z_paras = zh_sections[sec_i]
    e_title, e_paras = en_sections[sec_i]
    
    if "第一幕" in z_title:
        sec_tag = "ACT 01 · GUANGZHOU"
    elif "第二幕" in z_title:
        sec_tag = "ACT 02 · THE HAVEN"
    elif "第三幕" in z_title:
        sec_tag = "ACT 03 · PEARL HARBOR & SIEGE"
    elif "第四幕" in z_title:
        sec_tag = "ACT 04 · OCCUPATION & GRADUATION"
    elif "尾声" in z_title:
        sec_tag = "EPILOGUE · PARALLEL VIEW"
    else:
        sec_tag = "PROLOGUE · OPENING"
        
    part = f"""
      <!-- Section: {z_title} -->
      <section class="book-section" id="section-{sec_i}">
        <div class="book-section-header">
          <span class="section-tag">{sec_tag}</span>
          <h2 class="serif">{z_title}<span class="en">{e_title}</span></h2>
        </div>
        <div class="book-section-body">
    """
    
    for p_i in range(len(z_paras)):
        zp = z_paras[p_i]
        ep = e_paras[p_i]
        cue_idx = global_p_idx
        start_t = cues[cue_idx]["start"] if cue_idx < len(cues) else 0.0
        
        is_sfx = "【音效" in zp or "[SFX" in ep
        is_narrator = "【主叙述者" in zp or "[Main narrator" in ep
        
        extra_cls = ""
        if is_sfx:
            extra_cls = " sfx-badge"
        elif is_narrator:
            extra_cls = " narrator-badge"
            
        part += f"""
          <div class="bilingual-p{extra_cls}" id="p-{cue_idx}" data-idx="{cue_idx}" data-start="{start_t}" onclick="jumpToCue({cue_idx})">
            <div class="zh-para">{html.escape(zp)}</div>
            <div class="en-para">{html.escape(ep)}</div>
          </div>
        """
        global_p_idx += 1
        
    part += """
        </div>
      </section>
    """
    story_html_parts.append(part)

story_content_html = "".join(story_html_parts)

# Subtitle list HTML for the player
sub_list_html = []
for idx, c in enumerate(cues):
    sub_list_html.append(f"""
        <div class="sub-row{' active' if idx == 0 else ''}" id="sub-row-{idx}" data-idx="{idx}" data-start="{c['start']}" data-end="{c['end']}" onclick="jumpToCue({idx})">
          <div class="sub-time-tag">{int(c['start']//60):02d}:{int(c['start']%60):02d}</div>
          <div class="sub-content">
            <div class="sub-zh">{html.escape(c['zh'])}</div>
            <div class="sub-en">{html.escape(c['en'])}</div>
          </div>
        </div>
    """)
sub_list_full_html = "".join(sub_list_html)

full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>第 01 期：逃难的孩子 (1937–1942 · 广州至香港) | 台积电张忠谋 · 传记时间线的平行世界</title>
<meta name="description" content="台积电张忠谋传记时间线的平行世界 · 第 01 期《逃难的孩子》（1937–1942 · 广州至香港）。纯净双语典藏电子书，中英双语原声有声剧场，逐句同步高亮字幕，时代历史坐标与双语精读笔记。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0a0a0a;
    --bg2: #111113;
    --card: #16161a;
    --line: #26262b;
    --amber: #F59E0B;
    --blue: #38BDF8;
    --ink: #ece9e2;
    --muted: #a29c90;
    --serif: "Songti SC", "Noto Serif SC", "STSong", Georgia, serif;
    --sans: "PingFang SC", "Microsoft YaHei", -apple-system, "Segoe UI", Roboto, sans-serif;
    --en: "Georgia", "Times New Roman", serif;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; background: var(--bg); color: var(--ink); font-family: var(--sans); -webkit-font-smoothing: antialiased; }}
  body {{ min-height: 100vh; line-height: 1.8; overflow-x: hidden; padding-bottom: 60px; }}

  /* Top Navigation */
  .nav {{ position: sticky; top: 0; z-index: 100; background: rgba(10,10,10,0.88); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); height: 60px; display: flex; align-items: center; justify-content: space-between; padding: 0 6vw; }}
  .brand {{ display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--ink); font-weight: 700; font-size: 15px; letter-spacing: 0.5px; }}
  .brand-chip {{ width: 10px; height: 10px; background: var(--amber); border-radius: 2px; box-shadow: 0 0 12px var(--amber); }}
  .nav-links {{ display: flex; align-items: center; gap: 20px; }}
  .nav-link {{ color: var(--muted); text-decoration: none; font-size: 13.5px; transition: color 0.2s; }}
  .nav-link:hover, .nav-link.active {{ color: var(--amber); }}

  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 6vw; }}
  .article-wrap {{ max-width: 880px; margin: 0 auto; padding: 0 5vw; }}

  /* Hero Section */
  .hero-ep {{ padding: 56px 0 36px; border-bottom: 1px solid var(--line); background: radial-gradient(800px 400px at 80% -10%, rgba(245,158,11,0.08), transparent 60%), radial-gradient(700px 350px at 10% 110%, rgba(56,189,248,0.06), transparent 60%); }}
  .eyebrow {{ font-size: 12px; letter-spacing: 4px; text-transform: uppercase; color: var(--amber); display: block; margin-bottom: 14px; font-weight: 600; }}
  .eyebrow em {{ font-family: var(--en); font-style: italic; letter-spacing: 2px; margin-left: 8px; color: var(--blue); }}
  h1.serif {{ font-family: var(--serif); font-size: clamp(30px, 4.8vw, 46px); font-weight: 700; line-height: 1.25; color: var(--ink); margin-bottom: 16px; letter-spacing: 1px; }}
  h1.serif .en {{ display: block; font-family: var(--en); font-size: clamp(16px, 2.3vw, 22px); font-style: italic; font-weight: 400; color: var(--muted); margin-top: 8px; }}
  
  .tagline-box {{ background: var(--bg2); border-left: 4px solid var(--amber); border-radius: 0 12px 12px 0; padding: 18px 24px; margin-top: 22px; border-top: 1px solid var(--line); border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); }}
  .tagline-zh {{ font-family: var(--serif); font-size: 16.5px; color: var(--ink); line-height: 1.7; }}
  .tagline-en {{ font-family: var(--en); font-style: italic; color: var(--muted); font-size: 14.5px; margin-top: 6px; }}

  .meta-pills {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 24px; }}
  .pill {{ font-size: 12.5px; color: var(--muted); background: var(--card); border: 1px solid var(--line); padding: 6px 14px; border-radius: 999px; display: inline-flex; align-items: center; gap: 6px; }}
  .pill b {{ color: var(--ink); }}

  /* Audio Player Module */
  .player-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 20px; padding: 26px; margin: 36px 0; box-shadow: 0 20px 50px rgba(0,0,0,0.6); position: relative; overflow: hidden; }}
  .player-card::before {{ content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--amber), var(--blue)); }}
  
  .track-switcher {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 14px; margin-bottom: 20px; border-bottom: 1px solid var(--line); padding-bottom: 16px; }}
  .track-btns {{ display: flex; gap: 10px; }}
  .btn-track {{ display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 999px; font-size: 13.5px; font-weight: 600; cursor: pointer; transition: all 0.25s ease; border: 1px solid var(--line); background: var(--bg2); color: var(--muted); }}
  .btn-track em {{ font-family: var(--en); font-style: italic; font-weight: 400; font-size: 12px; }}
  .btn-track.active {{ background: var(--amber); color: #000; border-color: var(--amber); box-shadow: 0 4px 18px rgba(245,158,11,0.35); }}
  .btn-track.active em {{ color: #1a1205; }}
  .btn-track:hover:not(.active) {{ border-color: var(--amber); color: var(--amber); transform: translateY(-1px); }}

  .player-state-pill {{ font-size: 12px; color: var(--muted); display: flex; align-items: center; gap: 6px; font-family: monospace; }}
  .status-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #555; display: inline-block; }}
  .status-dot.playing {{ background: #10B981; box-shadow: 0 0 10px #10B981; animation: pulse 1.5s infinite; }}
  @keyframes pulse {{ 0% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.6; }} }}

  .player-main-ctrl {{ background: var(--bg2); border: 1px solid var(--line); border-radius: 14px; padding: 16px 20px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 18px; }}
  .ctrl-left {{ display: flex; align-items: center; gap: 16px; min-width: 240px; }}
  .play-btn {{ width: 48px; height: 48px; border-radius: 50%; background: var(--amber); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #000; font-size: 20px; font-weight: bold; transition: all 0.2s; box-shadow: 0 4px 16px rgba(245,158,11,0.3); }}
  .play-btn:hover {{ transform: scale(1.08); background: #fbb028; }}
  
  .track-meta {{ display: flex; flex-direction: column; }}
  .track-meta-title {{ font-size: 14.5px; font-weight: 600; color: var(--ink); }}
  .track-meta-sub {{ font-size: 12px; color: var(--muted); font-family: var(--en); font-style: italic; }}

  .progress-container {{ display: flex; align-items: center; gap: 12px; flex-grow: 1; min-width: 280px; }}
  .time-text {{ font-size: 12px; color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; min-width: 44px; text-align: center; }}
  .seek-bar {{ flex-grow: 1; accent-color: var(--amber); cursor: pointer; height: 5px; background: var(--line); border-radius: 4px; outline: none; }}

  .playback-options {{ display: flex; align-items: center; gap: 10px; }}
  .speed-select {{ background: var(--card); border: 1px solid var(--line); color: var(--ink); border-radius: 6px; padding: 5px 8px; font-size: 12px; cursor: pointer; outline: none; }}
  .speed-select:focus {{ border-color: var(--amber); }}

  /* Subtitles Viewport */
  .teleprompter-box {{ margin-top: 22px; }}
  .teleprompter-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; padding: 0 4px; }}
  .teleprompter-title {{ font-size: 11.5px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); font-weight: 600; display: flex; align-items: center; gap: 8px; }}
  .teleprompter-title b {{ color: var(--amber); font-weight: normal; }}
  .teleprompter-tools {{ display: flex; align-items: center; gap: 12px; font-size: 12px; color: var(--muted); }}
  .btn-toggle-scroll {{ cursor: pointer; background: transparent; border: 1px solid var(--line); color: var(--muted); padding: 3px 10px; border-radius: 999px; font-size: 11px; }}
  .btn-toggle-scroll.active {{ border-color: var(--amber); color: var(--amber); }}

  .subtitles-scroll {{ max-height: 290px; overflow-y: auto; display: flex; flex-direction: column; gap: 6px; padding: 4px 6px 4px 0; scroll-behavior: smooth; border: 1px solid var(--line); border-radius: 12px; background: var(--bg2); }}
  .subtitles-scroll::-webkit-scrollbar {{ width: 6px; }}
  .subtitles-scroll::-webkit-scrollbar-track {{ background: var(--bg2); }}
  .subtitles-scroll::-webkit-scrollbar-thumb {{ background: #333; border-radius: 3px; }}
  .subtitles-scroll::-webkit-scrollbar-thumb:hover {{ background: #444; }}

  .sub-row {{ display: flex; gap: 14px; padding: 10px 14px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; border-left: 3px solid transparent; }}
  .sub-row:hover {{ background: rgba(255,255,255,0.03); }}
  .sub-row.active {{ background: rgba(245,158,11,0.09); border-left-color: var(--amber); }}
  .sub-time-tag {{ font-size: 11px; font-family: monospace; color: var(--muted); padding-top: 2px; min-width: 38px; }}
  .sub-row.active .sub-time-tag {{ color: var(--amber); font-weight: bold; }}
  .sub-content {{ flex-grow: 1; }}
  .sub-zh {{ font-size: 14px; line-height: 1.6; color: var(--ink); font-family: var(--serif); }}
  .sub-en {{ font-size: 12px; line-height: 1.5; color: var(--muted); font-family: var(--en); font-style: italic; margin-top: 3px; }}
  .sub-row.active .sub-zh {{ color: var(--amber); font-weight: 600; }}
  .sub-row.active .sub-en {{ color: var(--blue); }}

  /* Lead Artwork (Chapter Hero Image) */
  .lead-artwork-figure {{ margin: 36px 0 52px; border: 1px solid var(--line); border-radius: 18px; overflow: hidden; background: var(--card); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }}
  .lead-artwork-img {{ width: 100%; height: auto; max-height: 520px; object-fit: cover; object-position: center 25%; display: block; }}
  .lead-artwork-caption {{ padding: 14px 22px; font-size: 13px; color: var(--muted); border-top: 1px solid var(--line); background: rgba(17,17,19,0.95); display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; }}
  .lead-artwork-caption .caption-zh {{ font-family: var(--serif); color: var(--ink); font-weight: 500; }}
  .lead-artwork-caption .caption-en {{ font-family: var(--en); font-style: italic; color: #888; font-size: 12px; }}

  /* 75% Pure Bilingual Book Body */
  .bilingual-book {{ margin-top: 20px; }}
  .book-section {{ margin-bottom: 56px; border-bottom: 1px solid var(--line); padding-bottom: 48px; }}
  .book-section:last-of-type {{ border-bottom: none; }}
  
  .book-section-header {{ margin-bottom: 28px; padding-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.06); }}
  .section-tag {{ font-size: 11.5px; letter-spacing: 3px; text-transform: uppercase; color: var(--amber); font-weight: 600; display: block; margin-bottom: 6px; }}
  .book-section-header h2.serif {{ font-size: 26px; color: var(--ink); line-height: 1.3; }}
  .book-section-header h2.serif .en {{ display: block; font-family: var(--en); font-size: 16px; font-style: italic; font-weight: 400; color: var(--muted); margin-top: 4px; }}

  .bilingual-p {{ padding: 14px 18px; border-radius: 10px; margin-bottom: 18px; transition: all 0.25s ease; border-left: 3px solid transparent; cursor: pointer; }}
  .bilingual-p:hover {{ background: rgba(255,255,255,0.02); }}
  .bilingual-p.active-para {{ background: rgba(245,158,11,0.08); border-left: 3px solid var(--amber); }}
  .zh-para {{ font-family: var(--serif); font-size: 17.5px; line-height: 1.9; color: var(--ink); margin-bottom: 8px; text-align: justify; letter-spacing: 0.2px; }}
  .en-para {{ font-family: var(--en); font-size: 15px; font-style: italic; line-height: 1.75; color: var(--muted); text-align: justify; }}
  .bilingual-p.active-para .zh-para {{ color: #ffffff; }}
  .bilingual-p.active-para .en-para {{ color: var(--blue); }}

  .bilingual-p.sfx-badge {{ background: rgba(56,189,248,0.04); border: 1px dashed rgba(56,189,248,0.25); border-left: 3px solid var(--blue); }}
  .bilingual-p.sfx-badge .zh-para {{ font-size: 14.5px; color: var(--blue); }}
  .bilingual-p.sfx-badge .en-para {{ font-size: 13px; color: #7dd3fc; }}

  .bilingual-p.narrator-badge {{ padding: 6px 14px; margin-bottom: 10px; background: transparent; border-left: 2px solid #555; }}
  .bilingual-p.narrator-badge .zh-para {{ font-size: 13px; color: #888; margin-bottom: 2px; }}
  .bilingual-p.narrator-badge .en-para {{ font-size: 12px; color: #666; }}

  /* 25% Secondary Extension & Historical Context Notes */
  .extension-zone {{ margin-top: 60px; padding-top: 48px; border-top: 2px solid var(--line); }}
  .extension-head {{ text-align: center; margin-bottom: 40px; }}
  .extension-head .ext-badge {{ font-size: 11.5px; letter-spacing: 4px; text-transform: uppercase; color: var(--amber); font-weight: 600; display: block; margin-bottom: 8px; }}
  .extension-head h2 {{ font-family: var(--serif); font-size: 28px; color: var(--ink); }}
  .extension-head h2 .en {{ display: block; font-family: var(--en); font-size: 15px; font-style: italic; color: var(--muted); margin-top: 4px; }}

  .ext-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 36px; }}
  @media (max-width: 820px) {{
    .ext-grid {{ grid-template-columns: 1fr; }}
  }}

  .ext-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 24px; }}
  .ext-card-title {{ font-family: var(--serif); font-size: 18px; color: var(--ink); font-weight: 600; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--line); padding-bottom: 12px; }}
  .ext-card-title span.tag {{ font-size: 11px; background: var(--bg2); border: 1px solid var(--line); color: var(--amber); padding: 2px 8px; border-radius: 4px; font-family: var(--sans); }}

  /* Vocabulary Item */
  .vocab-list {{ display: flex; flex-direction: column; gap: 16px; }}
  .vocab-item {{ border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px; }}
  .vocab-item:last-child {{ border-bottom: none; padding-bottom: 0; }}
  .vocab-word-row {{ display: flex; align-items: baseline; gap: 8px; margin-bottom: 4px; }}
  .vocab-word {{ font-family: var(--en); font-size: 16px; font-weight: 700; color: var(--amber); }}
  .vocab-ipa {{ font-family: var(--en); font-size: 13px; color: var(--muted); }}
  .vocab-zh {{ font-size: 13.5px; color: var(--ink); font-weight: 500; }}
  .vocab-note {{ font-size: 12.5px; color: var(--muted); line-height: 1.6; margin-top: 3px; }}
  .vocab-ex {{ font-family: var(--en); font-style: italic; font-size: 12.5px; color: var(--blue); margin-top: 4px; line-height: 1.5; }}

  /* Historical Timeline Card */
  .history-list {{ display: flex; flex-direction: column; gap: 14px; }}
  .history-item {{ display: flex; gap: 12px; align-items: flex-start; }}
  .history-num {{ width: 22px; height: 22px; border-radius: 50%; background: var(--bg2); border: 1px solid var(--line); display: flex; align-items: center; justify-content: center; font-size: 11px; color: var(--amber); font-weight: bold; flex-shrink: 0; margin-top: 2px; }}
  .history-text {{ font-size: 13.5px; line-height: 1.7; color: var(--muted); }}
  .history-text b {{ color: var(--ink); }}

  /* Golden Quote Card */
  .golden-card {{ background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(17,17,19,0.95)); border: 1px solid var(--amber); border-radius: 16px; padding: 28px; margin: 36px 0; text-align: center; }}
  .golden-card .quote-mark {{ font-family: var(--serif); font-size: 36px; color: var(--amber); line-height: 1; margin-bottom: 8px; }}
  .golden-card .quote-zh {{ font-family: var(--serif); font-size: 20px; font-weight: 700; color: #ffffff; line-height: 1.6; letter-spacing: 0.5px; }}
  .golden-card .quote-en {{ font-family: var(--en); font-style: italic; font-size: 16px; color: var(--amber); margin-top: 8px; line-height: 1.6; }}
  .golden-card .quote-author {{ font-size: 12px; letter-spacing: 2px; color: var(--muted); text-transform: uppercase; margin-top: 14px; }}

  /* Episode Nav Footer */
  .ep-nav-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 32px 0 20px; border-top: 1px solid var(--line); margin-top: 48px; }}
  .ep-nav-btn {{ display: inline-flex; align-items: center; gap: 8px; padding: 12px 22px; border-radius: 999px; background: var(--bg2); border: 1px solid var(--line); color: var(--ink); text-decoration: none; font-size: 13.5px; transition: all 0.2s; }}
  .ep-nav-btn:hover {{ border-color: var(--amber); color: var(--amber); transform: translateY(-2px); }}
  .ep-nav-btn.next {{ background: linear-gradient(135deg, rgba(245,158,11,0.15), var(--bg2)); border-color: rgba(245,158,11,0.4); }}
  .ep-nav-btn.next:hover {{ border-color: var(--amber); }}

  /* Footer */
  .footer {{ border-top: 1px solid var(--line); padding: 40px 0; text-align: center; color: var(--muted); font-size: 13px; margin-top: 40px; }}
  .footer a {{ color: var(--amber); text-decoration: none; }}
</style>
</head>
<body>

  <!-- Sticky Global Navigation -->
  <nav class="nav">
    <a href="index.html" class="brand">
      <div class="brand-chip"></div>
      <span>MORRIS CHANG · TSMC</span>
    </a>
    <div class="nav-links">
      <a href="index.html" class="nav-link">← 返回作品官网</a>
      <a href="audio.html" class="nav-link">剧场总览</a>
      <a href="reader.html" class="nav-link">全册电子书</a>
      <a href="map.html" class="nav-link">平行地图</a>
      <a href="cards.html" class="nav-link">金句卡片</a>
    </div>
  </nav>

  <!-- Hero Header -->
  <header class="hero-ep">
    <div class="wrap">
      <span class="eyebrow">第 01 期 · 1937–1942 · 广州至香港 <em>EPISODE 01 · GUANGZHOU TO HONG KONG</em></span>
      <h1 class="serif">第 01 期：逃难的孩子<span class="en">Episode 01: The Child Who Fled (1937–1942)</span></h1>
      
      <div class="tagline-box">
        <div class="tagline-zh">一个孩子的记忆里，战争不是历史，是一张张搬家的船票。——时代推着人走，人在时代里长出自己的根。</div>
        <div class="tagline-en">In a child's memory, war is not history — it is a series of boat tickets. The era pushes a person; the person grows roots of their own.</div>
      </div>

      <div class="meta-pills">
        <span class="pill">⏱ 目标时长 <b>20 分钟 (20 Min)</b></span>
        <span class="pill">🎧 <b>中英双语原声 TTS</b> (Chinese & English Tracks)</span>
        <span class="pill">📜 <b>128 句同步字幕</b> (Real-time Synced Teleprompter)</span>
        <span class="pill">📖 <b>典藏双语书</b> (Exact Parallel Text)</span>
      </div>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="wrap">

    <!-- 1. Production Audio Player & Synced Subtitles Viewport -->
    <section class="player-card" id="player-box">
      
      <!-- Track Switcher -->
      <div class="track-switcher">
        <div class="track-btns">
          <button id="btnZhTrack" class="btn-track active" onclick="switchAudioTrack('zh')">🇨🇳 中文原声 <em>Chinese Audio</em></button>
          <button id="btnEnTrack" class="btn-track" onclick="switchAudioTrack('en')">🇺🇸 English Audio <em>美式英语</em></button>
        </div>
        <div class="player-state-pill">
          <span id="statusDot" class="status-dot"></span>
          <span id="statusText">准备就绪 / READY</span>
        </div>
      </div>

      <!-- Main Audio Controls -->
      <div class="player-main-ctrl">
        <div class="ctrl-left">
          <button id="playBtn" class="play-btn" onclick="togglePlay()" title="播放 / 暂停">▶</button>
          <div class="track-meta">
            <div id="trackMetaTitle" class="track-meta-title">第 01 期：逃难的孩子 (中文原声)</div>
            <div id="trackMetaSub" class="track-meta-sub">Dual-Language Synchronized Broadcast · 1937–1942</div>
          </div>
        </div>

        <div class="progress-container">
          <span id="curTimeText" class="time-text">00:00</span>
          <input type="range" id="audioSeekBar" class="seek-bar" min="0" max="100" value="0" step="0.1" oninput="onSeekSlider(this.value)">
          <span id="durTimeText" class="time-text">17:27</span>
        </div>

        <div class="playback-options">
          <select id="speedSelect" class="speed-select" onchange="changePlaybackRate(this.value)" title="播放语速">
            <option value="0.8">0.8x 慢速</option>
            <option value="1.0" selected>1.0x 正常</option>
            <option value="1.25">1.25x 快速</option>
            <option value="1.5">1.5x 加速</option>
          </select>
        </div>

        <audio id="mainAudio" src="./audio/ep01-zh.mp3" preload="metadata"></audio>
      </div>

      <!-- Teleprompter / Subtitles Scroll Container -->
      <div class="teleprompter-box">
        <div class="teleprompter-header">
          <div class="teleprompter-title">
            <span>逐句同步字幕 · 点击任意句定点跳转</span>
            <b>(REAL MATCHED SUBTITLES · CLICK TO SEEK)</b>
          </div>
          <div class="teleprompter-tools">
            <button id="toggleScrollBtn" class="btn-toggle-scroll active" onclick="toggleAutoScroll()">自动滚动: 开</button>
            <span id="activeCueInfo" style="font-size:11px; font-family:monospace; color:var(--amber);">CUE 1 / 128</span>
          </div>
        </div>

        <div id="subtitlesList" class="subtitles-scroll">
          {sub_list_full_html}
        </div>
      </div>

    </section>

    <!-- 2. Pure Bilingual Book Section (75% Main Core) -->
    <article class="bilingual-book article-wrap" id="bilingual-reader">

      <!-- Lead Artwork Illustration at Top of Book -->
      <figure class="lead-artwork-figure">
        <img class="lead-artwork-img" src="./设计资产/插图/第01期-逃难的孩子.png" alt="第 01 期 概念插画 · 逃难的孩子 (1937–1942)" loading="lazy">
        <figcaption class="lead-artwork-caption">
          <span class="caption-zh">🎨 第 01 期 概念插画 · 逃难的孩子 (1937–1942 · 广州至香港)</span>
          <span class="caption-en">Episode 01 Concept Artwork: The Child Who Fled (Guangzhou to Hong Kong)</span>
        </figcaption>
      </figure>

      <!-- Exact Text Parallel Book Content -->
      {story_content_html}

    </article>

    <!-- 3. Secondary Extension (25% Bottom Notes & Historical Context) -->
    <section class="extension-zone article-wrap">
      
      <div class="extension-head">
        <span class="ext-badge">HISTORICAL CONTEXT & ENGLISH STUDY</span>
        <h2 class="serif">周边延伸解读与双语学习<span class="en">Historical Context & English Notes</span></h2>
      </div>

      <div class="ext-grid">
        
        <!-- Key Vocabulary Card -->
        <div class="ext-card">
          <div class="ext-card-title">
            <span>📖 本期重点词汇精读</span>
            <span class="tag">VOCABULARY</span>
          </div>
          <div class="vocab-list">
            
            <div class="vocab-item">
              <div class="vocab-word-row">
                <span class="vocab-word">Refugee</span>
                <span class="vocab-ipa">/ˌrefjuˈdʒiː/</span>
                <span class="vocab-zh">n. 难民；逃难者</span>
              </div>
              <div class="vocab-note">因战争或灾难被迫离开家园的人。在传主记忆中，童年是一连串搬家的船票。</div>
              <div class="vocab-ex">"In a child's memory, war is not history — it is a series of boat tickets."</div>
            </div>

            <div class="vocab-item">
              <div class="vocab-word-row">
                <span class="vocab-word">Bombing / Air Raid</span>
                <span class="vocab-ipa">/ˈbɒmɪŋ/</span>
                <span class="vocab-zh">n. 空袭；轰炸</span>
              </div>
              <div class="vocab-note">敌机对地面目标的空中打击。1937-1938年广州大轰炸是传主童年直面战争的开端。</div>
              <div class="vocab-ex">"Japanese planes raided Canton day after day, deliberately bombing residential districts."</div>
            </div>

            <div class="vocab-item">
              <div class="vocab-word-row">
                <span class="vocab-word">Haven</span>
                <span class="vocab-ipa">/ˈheɪvn/</span>
                <span class="vocab-zh">n. 避风港；安全庇护所</span>
              </div>
              <div class="vocab-note">躲避风暴或危险的安全之地。香港在太平洋战争爆发前曾为无数南下家庭提供了宝贵的平静。</div>
              <div class="vocab-ex">"While war consumed the mainland, Hong Kong was, for a time, a genuine haven."</div>
            </div>

            <div class="vocab-item">
              <div class="vocab-word-row">
                <span class="vocab-word">Occupation</span>
                <span class="vocab-ipa">/ˌɒkjuˈpeɪʃn/</span>
                <span class="vocab-zh">n. 占领；沦陷时期</span>
              </div>
              <div class="vocab-note">军事力量对领土的强制占领管制。香港经历了三年零八个月的日据时期。</div>
              <div class="vocab-ex">"Hong Kong entered the years of Japanese occupation, where passersby were required to bow to sentries."</div>
            </div>

            <div class="vocab-item">
              <div class="vocab-word-row">
                <span class="vocab-word">Boat Ticket</span>
                <span class="vocab-ipa">/bəʊt ˈtɪkɪt/</span>
                <span class="vocab-zh">n. 船票</span>
              </div>
              <div class="vocab-note">逃难与迁徙的具象载体。从广州到香港、再从香港到上海，串联起动荡时代的童年轨迹。</div>
              <div class="vocab-ex">"And it all began here — with a boat ticket in the hand of a five-year-old."</div>
            </div>

          </div>
        </div>

        <!-- Historical Background Card -->
        <div class="ext-card">
          <div class="ext-card-title">
            <span>🏛️ 时代坐标与历史背景</span>
            <span class="tag">1937–1942</span>
          </div>
          <div class="history-list">
            
            <div class="history-item">
              <div class="history-num">1</div>
              <div class="history-text">
                <b>广州大轰炸（1937–1938）</b>：1937 年 10 月起，日机开始频繁空袭广州；1938 年 5–6 月轰炸加剧，城市大片沦为废墟，平民伤亡惨重。
              </div>
            </div>

            <div class="history-item">
              <div class="history-num">2</div>
              <div class="history-text">
                <b>广州沦陷（1938.10）</b>：日军大亚湾登陆后攻占广州，华南沿海对外通道切断。
              </div>
            </div>

            <div class="history-item">
              <div class="history-num">3</div>
              <div class="history-text">
                <b>珍珠港事变（1941.12.7）</b>：日本偷袭美国珍珠港，太平洋战争全面爆发，同盟国与轴心国进入生死决战。
              </div>
            </div>

            <div class="history-item">
              <div class="history-num">4</div>
              <div class="history-text">
                <b>香港保卫战（1941.12.8–12.25）</b>：日军数小时内进攻香港，英军与加拿大援军坚守18天后，港督杨慕琦于圣诞夜宣布投降。
              </div>
            </div>

            <div class="history-item">
              <div class="history-num">5</div>
              <div class="history-text">
                <b>香港日据时期（1941–1945）</b>：市民经过哨兵需行鞠躬礼；英军撤离至日军完全接管的间隙，九龙一度治安失控抢劫频发。
              </div>
            </div>

            <div class="history-item">
              <div class="history-num">6</div>
              <div class="history-text">
                <b>宁波商帮背景</b>：世代以经营钱庄、航运与实业闻名，构成了传主家庭坚韧稳健的文化底色与家风传承。
              </div>
            </div>

            <div class="history-item">
              <div class="history-num">7</div>
              <div class="history-text">
                <b>传主童年轨迹</b>：1936 迁广州、1937 迁香港、1941 亲历香港战役与酒店避难、1942 培正小学毕业后赴沪西行。
              </div>
            </div>

          </div>
        </div>

      </div>

      <!-- Golden Quote Banner -->
      <div class="golden-card">
        <div class="quote-mark">“</div>
        <div class="quote-zh">时代可以推着你走，但走成什么样，从来是你自己的事。</div>
        <div class="quote-en">"The era may push you — but what you become is always your own doing."</div>
        <div class="quote-author">— 第 01 期 · 尾声平行叙事金句</div>
      </div>

      <!-- Bottom Episode Navigation -->
      <div class="ep-nav-bar">
        <a href="reader.html" class="ep-nav-btn">← 返回全册电子书导读</a>
        <a href="audio.html" class="ep-nav-btn next">进入第 02 期：考不进去的南开 & 作家梦 →</a>
      </div>

    </section>

  </main>

  <!-- Global Footer -->
  <footer class="footer wrap">
    <div>台积电张忠谋 · 传记时间线的平行世界 · AIGC 原创作品</div>
    <div style="margin-top:6px; color:#666; font-size:12px;">© 2026 Parallel World Project. Pure Bilingual Edition. All Rights Reserved.</div>
  </footer>

  <!-- Script for Synchronized Audio & Subtitles -->
  <script>
    const EP_CUES = {cues_json_str};

    let currentTrack = 'zh'; // 'zh' or 'en'
    let autoScroll = true;
    let activeCueIndex = -1;

    const audioEl = document.getElementById('mainAudio');
    const playBtn = document.getElementById('playBtn');
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    const curTimeText = document.getElementById('curTimeText');
    const durTimeText = document.getElementById('durTimeText');
    const seekBar = document.getElementById('audioSeekBar');
    const trackTitle = document.getElementById('trackMetaTitle');
    const subtitlesContainer = document.getElementById('subtitlesList');
    const btnZh = document.getElementById('btnZhTrack');
    const btnEn = document.getElementById('btnEnTrack');
    const toggleScrollBtn = document.getElementById('toggleScrollBtn');
    const activeCueInfo = document.getElementById('activeCueInfo');

    function formatTime(sec) {{
      if (isNaN(sec) || sec < 0) return "00:00";
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
    }}

    function switchAudioTrack(lang) {{
      if (lang === currentTrack) return;
      const wasPlaying = !audioEl.paused;
      const curRatio = audioEl.duration ? (audioEl.currentTime / audioEl.duration) : 0;
      
      currentTrack = lang;
      if (lang === 'zh') {{
        audioEl.src = './audio/ep01-zh.mp3';
        btnZh.className = 'btn-track active';
        btnEn.className = 'btn-track';
        trackTitle.innerText = '第 01 期：逃难的孩子 (中文原声)';
      }} else {{
        audioEl.src = './audio/ep01-en.mp3';
        btnZh.className = 'btn-track';
        btnEn.className = 'btn-track active';
        trackTitle.innerText = 'Episode 01: The Child Who Fled (English Audio)';
      }}
      
      audioEl.load();
      audioEl.onloadedmetadata = () => {{
        durTimeText.innerText = formatTime(audioEl.duration);
        if (curRatio > 0) {{
          audioEl.currentTime = curRatio * audioEl.duration;
        }}
        if (wasPlaying) {{
          audioEl.play();
        }}
      }};
    }}

    function togglePlay() {{
      if (audioEl.paused) {{
        audioEl.play();
      }} else {{
        audioEl.pause();
      }}
    }}

    function onSeekSlider(val) {{
      if (audioEl.duration) {{
        const target = (val / 100) * audioEl.duration;
        audioEl.currentTime = target;
      }}
    }}

    function changePlaybackRate(rate) {{
      audioEl.playbackRate = parseFloat(rate);
    }}

    function toggleAutoScroll() {{
      autoScroll = !autoScroll;
      if (autoScroll) {{
        toggleScrollBtn.innerText = '自动滚动: 开';
        toggleScrollBtn.className = 'btn-toggle-scroll active';
      }} else {{
        toggleScrollBtn.innerText = '自动滚动: 关';
        toggleScrollBtn.className = 'btn-toggle-scroll';
      }}
    }}

    function jumpToCue(idx) {{
      if (idx >= 0 && idx < EP_CUES.length) {{
        const cue = EP_CUES[idx];
        audioEl.currentTime = cue.start;
        if (audioEl.paused) {{
          audioEl.play();
        }}
        highlightCue(idx, true);
      }}
    }}

    function highlightCue(idx, forceScroll) {{
      if (idx === activeCueIndex && !forceScroll) return;
      
      // Clear previous active
      if (activeCueIndex >= 0) {{
        const prevSub = document.getElementById('sub-row-' + activeCueIndex);
        if (prevSub) prevSub.classList.remove('active');
        const prevPara = document.getElementById('p-' + activeCueIndex);
        if (prevPara) prevPara.classList.remove('active-para');
      }}

      activeCueIndex = idx;
      if (idx < 0 || idx >= EP_CUES.length) return;

      activeCueInfo.innerText = "CUE " + (idx + 1) + " / " + EP_CUES.length;

      // Highlight subtitle row
      const subRow = document.getElementById('sub-row-' + idx);
      if (subRow) {{
        subRow.classList.add('active');
        if (autoScroll || forceScroll) {{
          const offsetTop = subRow.offsetTop - subtitlesContainer.offsetTop - 80;
          subtitlesContainer.scrollTo({{ top: Math.max(0, offsetTop), behavior: 'smooth' }});
        }}
      }}

      // Highlight corresponding book paragraph
      const paraEl = document.getElementById('p-' + idx);
      if (paraEl) {{
        paraEl.classList.add('active-para');
      }}
    }}

    // Audio Event Handlers
    audioEl.addEventListener('play', () => {{
      playBtn.innerText = '❚❚';
      statusDot.className = 'status-dot playing';
      statusText.innerText = currentTrack === 'zh' ? '正在播放 (中文)' : 'PLAYING (EN)';
    }});

    audioEl.addEventListener('pause', () => {{
      playBtn.innerText = '▶';
      statusDot.className = 'status-dot';
      statusText.innerText = '已暂停 / PAUSED';
    }});

    audioEl.addEventListener('timeupdate', () => {{
      const cur = audioEl.currentTime;
      const dur = audioEl.duration || 1047;
      curTimeText.innerText = formatTime(cur);
      durTimeText.innerText = formatTime(dur);
      seekBar.value = (cur / dur) * 100;

      // Find matching cue in EP_CUES
      let matchedIdx = -1;
      for (let i = 0; i < EP_CUES.length; i++) {{
        if (cur >= EP_CUES[i].start && cur < EP_CUES[i].end) {{
          matchedIdx = i;
          break;
        }}
      }}
      if (matchedIdx !== -1 && matchedIdx !== activeCueIndex) {{
        highlightCue(matchedIdx, false);
      }}
    }});

    audioEl.addEventListener('loadedmetadata', () => {{
      durTimeText.innerText = formatTime(audioEl.duration);
    }});

    // Initialize highlight
    highlightCue(0, false);
  </script>
</body>
</html>
"""

# Write to episode-01.html
out_path = "/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC/episode-01.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Successfully written episode-01.html! File size:", len(full_html))
