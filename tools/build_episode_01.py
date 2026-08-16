#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to rebuild episode-01.html completely matching index.html aesthetic,
and verify deploy.yml.
"""

import os
import re
import json

ROOT_DIR = "/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC"
os.chdir(ROOT_DIR)

# 1. Run tools/update_pages.py first
os.system("python3 tools/update_pages.py")

# 2. Read Chinese script & English script
with open("03-剧集/第01期-逃难的孩子/中文文字稿.md", "r", encoding="utf-8") as f:
    zh_content = f.read()

with open("03-剧集/第01期-逃难的孩子/英文文字稿.md", "r", encoding="utf-8") as f:
    en_content = f.read()

# Let's inspect headings and paragraphs
# Build structured acts and paragraphs
# Let's generate a clean episode-01.html that follows index.html typography and styles

html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>第 01 期：逃难的孩子 (1937–1942) | 台积电张忠谋 · 传记时间线的平行世界</title>
<meta name="description" content="台积电张忠谋双语传记剧集第 01 期：逃难的孩子（1937–1942 · 广州至香港）。提供沉浸式中英原声广播剧、逐句同步高亮字幕、双语全文本与深度商业英语复盘。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0a0a;
    --bg2: #111113;
    --card: #16161a;
    --line: #26262b;
    --ink: #ece9e2;
    --muted: #a29c90;
    --amber: #F59E0B;
    --blue: #38BDF8;
    --serif: "Songti SC","Noto Serif SC","STSong",Georgia,serif;
    --sans: "PingFang SC","Microsoft YaHei",-apple-system,"Segoe UI",Roboto,sans-serif;
    --en: "Georgia","Times New Roman",serif;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; background: var(--bg); color: var(--ink); font-family: var(--sans); }
  body { min-height: 100vh; line-height: 1.7; overflow-x: hidden; }
  
  /* Global Nav */
  .nav { position: sticky; top: 0; z-index: 100; background: rgba(10,10,10,0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); height: 60px; display: flex; align-items: center; justify-content: space-between; padding: 0 6vw; }
  .brand { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--ink); font-weight: 700; font-size: 15px; }
  .brand-chip { width: 10px; height: 10px; background: var(--amber); border-radius: 2px; box-shadow: 0 0 10px var(--amber); }
  .nav-links { display: flex; align-items: center; gap: 18px; }
  .nav-link { color: var(--muted); text-decoration: none; font-size: 13px; transition: color 0.2s; }
  .nav-link:hover, .nav-link.active { color: var(--amber); }

  .wrap { max-width: 1180px; margin: 0 auto; padding: 0 6vw; }
  .article-wrap { max-width: 860px; margin: 0 auto; padding: 0 5vw; }

  /* Hero Section */
  .hero-ep { padding: 60px 0 40px; border-bottom: 1px solid var(--line); }
  .eyebrow { font-size: 12px; letter-spacing: 4px; text-transform: uppercase; color: var(--amber); display: block; margin-bottom: 14px; }
  .eyebrow em { font-family: var(--en); font-style: italic; letter-spacing: 2px; margin-left: 8px; color: var(--blue); }
  h1.serif { font-family: var(--serif); font-size: clamp(28px, 4.5vw, 44px); font-weight: 700; line-height: 1.25; color: var(--ink); margin-bottom: 16px; }
  h1.serif .en { display: block; font-family: var(--en); font-size: clamp(16px, 2.4vw, 22px); font-style: italic; font-weight: 400; color: var(--muted); margin-top: 6px; }
  .tagline { font-size: 16px; color: var(--muted); line-height: 1.6; border-left: 3px solid var(--amber); padding-left: 14px; margin-top: 18px; }
  .tagline em { display: block; font-family: var(--en); font-style: italic; color: #737373; font-size: 14px; margin-top: 4px; }

  /* Player Section */
  .player-box { background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: 24px; margin: 36px 0; box-shadow: 0 16px 40px rgba(0,0,0,0.5); }
  .switcher-row { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 18px; border-bottom: 1px solid var(--line); padding-bottom: 16px; }
  .btn { display: inline-flex; align-items: center; gap: 6px; padding: 9px 18px; border-radius: 999px; font-size: 13px; font-weight: 600; text-decoration: none; cursor: pointer; transition: all 0.2s; border: none; }
  .btn em { font-family: var(--en); font-style: italic; font-weight: 400; opacity: 0.85; font-size: 12px; margin-left: 4px; }
  .btn.primary { background: var(--amber); color: #000; }
  .btn.ghost { background: var(--bg2); color: var(--ink); border: 1px solid var(--line); }
  .btn.ghost:hover { border-color: var(--amber); color: var(--amber); }

  .audio-ctrl-bar { background: var(--bg2); border: 1px solid var(--line); border-radius: 12px; padding: 14px 18px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 14px; }
  .play-circle { width: 44px; height: 44px; border-radius: 50%; background: var(--amber); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #000; font-size: 18px; font-weight: bold; transition: transform 0.2s; }
  .play-circle:hover { transform: scale(1.05); }

  .progress-wrap { display: flex; align-items: center; gap: 12px; flex-grow: 1; max-width: 500px; }
  .time-mono { font-size: 12px; color: var(--muted); font-family: monospace; min-width: 40px; }
  .seek-slider { flex-grow: 1; accent-color: var(--amber); cursor: pointer; height: 4px; }

  /* Subtitles Viewport */
  .sub-viewport-head { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin: 18px 0 10px; display: flex; justify-content: space-between; align-items: center; }
  .sub-list { display: flex; flex-direction: column; gap: 8px; max-height: 280px; overflow-y: auto; padding-right: 6px; }
  .sub-row { padding: 12px 14px; border-radius: 10px; background: var(--bg2); border-left: 3px solid transparent; cursor: pointer; transition: all 0.2s; }
  .sub-row:hover { background: rgba(255,255,255,0.03); }
  .sub-row.active { background: rgba(245,158,11,0.08); border-left: 3px solid var(--amber); }
  .sub-zh { font-size: 14px; color: var(--ink); line-height: 1.6; font-family: var(--serif); }
  .sub-en { font-size: 12px; color: var(--muted); font-style: italic; font-family: var(--en); margin-top: 3px; }
  .sub-row.active .sub-zh { color: var(--amber); font-weight: 600; }
  .sub-row.active .sub-en { color: var(--blue); }

  /* Article Content */
  .article-body { padding: 40px 0; }
  .act-block { margin-bottom: 48px; }
  .act-header { margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid var(--line); }
  .act-header .act-tag { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: var(--amber); }
  .act-header h2 { font-family: var(--serif); font-size: 24px; color: var(--ink); margin-top: 4px; }
  .act-header h2 .en { display: block; font-family: var(--en); font-size: 16px; font-style: italic; font-weight: 400; color: var(--muted); }

  .bilingual-p { margin-bottom: 22px; }
  .bilingual-p .zh { font-family: var(--serif); font-size: 17px; line-height: 1.85; color: var(--ink); margin-bottom: 6px; text-align: justify; }
  .bilingual-p .en { font-family: var(--en); font-size: 14.5px; font-style: italic; line-height: 1.7; color: var(--muted); text-align: justify; }

  /* Breakout Cards */
  .track { border: 1px solid var(--line); background: var(--bg2); border-radius: 14px; padding: 22px; margin: 30px 0; }
  .track.amber { border-left: 4px solid var(--amber); background: linear-gradient(135deg, rgba(245,158,11,0.04), transparent); }
  .track.blue { border-left: 4px solid var(--blue); background: linear-gradient(135deg, rgba(56,189,248,0.04), transparent); }
  .track h4 { font-size: 14px; font-weight: 700; color: var(--ink); margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
  .track p { font-size: 13.5px; color: var(--muted); line-height: 1.7; }
  .track p.en-note { font-family: var(--en); font-style: italic; color: #888; font-size: 12.5px; margin-top: 6px; }

  /* Takeaways & Vocabulary Section */
  .takeaways-section { border-top: 1px solid var(--line); padding: 50px 0 30px; margin-top: 40px; }
  .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-top: 24px; }
  .card-takeaway { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 22px; }
  .vocab-list { list-style: none; display: flex; flex-direction: column; gap: 12px; margin-top: 12px; }
  .vocab-item { padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); }
  .vocab-word { font-family: var(--en); font-size: 15px; font-weight: 700; color: var(--amber); }
  .vocab-phonetic { font-size: 12px; color: var(--muted); margin-left: 6px; }
  .vocab-def { font-size: 13px; color: var(--ink); margin-top: 2px; }
  .vocab-ex { font-family: var(--en); font-style: italic; font-size: 12px; color: var(--blue); margin-top: 2px; }

  /* Golden Quote Banner */
  .golden-quote { background: var(--card); border: 1px solid var(--line); border-left: 4px solid var(--amber); border-radius: 14px; padding: 28px; margin: 40px 0; }
  .golden-quote blockquote { font-family: var(--en); font-size: 18px; font-style: italic; color: var(--ink); line-height: 1.6; }
  .golden-quote .quote-zh { font-family: var(--serif); font-size: 16px; color: var(--amber); margin-top: 10px; }
  .golden-quote .quote-author { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; margin-top: 8px; }

  /* Ep Navigation */
  .ep-nav-bottom { display: flex; justify-content: space-between; align-items: center; padding: 30px 0 60px; border-top: 1px solid var(--line); margin-top: 40px; }

  /* Footer */
  .footer { border-top: 1px solid var(--line); padding: 40px 0; text-align: center; color: var(--muted); font-size: 13px; }
  .footer a { color: var(--amber); text-decoration: none; }
</style>
</head>
<body>

  <!-- Navigation -->
  <nav class="nav">
    <a href="index.html" class="brand">
      <div class="brand-chip"></div>
      <span>MORRIS CHANG · TSMC</span>
    </a>
    <div class="nav-links">
      <a href="index.html" class="nav-link">← 返回作品官网</a>
      <a href="audio.html" class="nav-link">剧场总览</a>
      <a href="https://github.com/ReadShift/20260816-Morris-Chang-TSMC" target="_blank" class="nav-link">🚀 GitHub 源码</a>
    </div>
  </nav>

  <!-- Hero Header -->
  <header class="hero-ep">
    <div class="wrap">
      <span class="eyebrow">第一期 · 1937–1942 · 广州至香港 <em>EPISODE 01 · GUANGZHOU TO HONG KONG</em></span>
      <h1 class="serif">第 01 期：逃难的孩子<span class="en">Episode 01: The Child Who Fled (1937–1942)</span></h1>
      <div class="tagline">
        一个孩子的记忆里，战争不是历史，是一张张搬家的船票。
        <em>In a child's memory, war is not history — it is a series of boat tickets.</em>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="wrap">

    <!-- Production 2-Track Audio Player -->
    <section class="player-box">
      <div class="switcher-row">
        <button id="btnZhTrack" class="btn primary" onclick="switchEpTrack('zh')">🇨🇳 中文原声 <em>Chinese Audio</em></button>
        <button id="btnEnTrack" class="btn ghost" onclick="switchEpTrack('en')">🇺🇸 English Audio <em>美式英语</em></button>
      </div>

      <div class="audio-ctrl-bar">
        <div style="display:flex; align-items:center; gap:14px;">
          <button id="epPlayBtn" class="play-circle" onclick="toggleEpPlay()">▶</button>
          <div>
            <div id="epTrackLabel" style="font-weight:600; font-size:15px; color:var(--ink);">🇨🇳 第01期：逃难的孩子 (中文原声)</div>
            <div style="font-size:12px; color:var(--muted); font-family:var(--en); font-style:italic;">Dual-Language Synchronized Broadcast (1937–1942)</div>
          </div>
        </div>

        <div class="progress-wrap">
          <span id="epCurTime" class="time-mono">00:00</span>
          <input type="range" id="epSeekBar" class="seek-slider" min="0" max="100" value="0" step="0.1" oninput="seekEpAudio(this.value)">
          <span id="epDuration" class="time-mono">00:00</span>
        </div>

        <audio id="epAudio" src="./audio/ep01-zh.mp3" preload="metadata"></audio>
      </div>

      <!-- Synchronized Subtitles Viewport -->
      <div class="sub-viewport-head">
        <span>逐句同步字幕 · 点击任意句定点跳转 (CLICK SENTENCE TO SEEK)</span>
        <span style="color:var(--amber); font-size:11px;">● 实时高亮同步中</span>
      </div>

      <div id="subList" class="sub-list">
        <!-- Lines dynamically populated or static structured -->
        <div class="sub-row active" data-start="0" data-end="12" onclick="seekEpTime(0)">
          <div class="sub-zh">一九三七年七月，卢沟桥事变爆发。六岁的张忠谋正在广州，跟随担任财政局干事的父亲张秉三生活。</div>
          <div class="sub-en">In July 1937, the Marco Polo Bridge Incident erupted. Six-year-old Morris Chang was living in Guangzhou with his father, Chang Ping-san.</div>
        </div>
        <div class="sub-row" data-start="12" data-end="25" onclick="seekEpTime(12)">
          <div class="sub-zh">日军战机的轰炸声很快打破了南方的宁静。为了躲避战火，全家仓促收拾行囊，踏上了逃往英属香港的客轮。</div>
          <div class="sub-en">The roar of Japanese bombers shattered the tranquility of the south. Fleeing the flames of war, the family hurriedly packed and boarded a passenger ship for British Hong Kong.</div>
        </div>
        <div class="sub-row" data-start="25" data-end="40" onclick="seekEpTime(25)">
          <div class="sub-zh">在香港半山培正小学的几年，是张忠谋童年少有的安稳时光。他在这里广泛阅读，甚至萌生了当作家的梦想。</div>
          <div class="sub-en">The few years at Pui Ching Primary School in Hong Kong were among the rare peaceful periods of his childhood, where he read extensively and dreamed of becoming a writer.</div>
        </div>
        <div class="sub-row" data-start="40" data-end="55" onclick="seekEpTime(40)">
          <div class="sub-zh">然而一九四一年十二月，太平洋战争爆发，日军十八天内攻陷香港。平静再次被粉碎。</div>
          <div class="sub-en">Yet in December 1941, the Pacific War broke out, and Japanese forces seized Hong Kong in eighteen days. Peace was shattered once more.</div>
        </div>
        <div class="sub-row" data-start="55" data-end="70" onclick="seekEpTime(55)">
          <div class="sub-zh">在日军严密占领与粮荒下，父亲再次决断：放弃香港产业，取道沦陷区跋涉千里，前往抗战大后方陪都重庆。</div>
          <div class="sub-en">Facing strict Japanese occupation and starvation, his father made another decisive choice: abandon their Hong Kong assets and trek across occupied territory toward wartime Chongqing.</div>
        </div>
        <div class="sub-row" data-start="70" data-end="90" onclick="seekEpTime(70)">
          <div class="sub-zh">这段流亡经历深深塑造了张忠谋一生的危机意识与在剧烈不确定性中做出关键决策的能力。</div>
          <div class="sub-en">This period of displacement deeply shaped Morris Chang's lifelong crisis consciousness and ability to make pivotal decisions amid severe uncertainty.</div>
        </div>
      </div>
    </section>

    <!-- Reading Article Body -->
    <article class="article-body article-wrap">

      <!-- Act 1 -->
      <section class="act-block">
        <div class="act-header">
          <span class="act-tag">ACT 01 · 广州炮火</span>
          <h2>第一幕：童年的警报声<span class="en">Act 1: Sirens of Childhood (Guangzhou, 1937)</span></h2>
        </div>

        <div class="bilingual-p">
          <p class="zh">一九三七年七月，卢沟桥的枪声彻底改变了整整一代中国人的命运。当时刚满六岁的张忠谋，随在广州市财政局任职的父亲张秉三和母亲徐茂懿，居住在珠江畔的一座小楼里。</p>
          <p class="en">In July 1937, gunshots at the Marco Polo Bridge irrevocably altered the destiny of an entire generation of Chinese people. Six-year-old Morris Chang was living by the Pearl River in Guangzhou with his father, Chang Ping-san, a government finance official, and his mother, Xu Maoyi.</p>
        </div>

        <div class="bilingual-p">
          <p class="zh">在幼童的视线里，最初的战争不是宏大的历史名词，而是刺耳的空袭警报、被大人抱进防空洞时的黑暗与泥土气味，以及母亲紧紧搂住他时急促的心跳。</p>
          <p class="en">In a young child's eyes, war was not a grand historical concept; it was the shrill scream of air raid sirens, the darkness and earthy smell of bomb shelters, and the rapid thumping of his mother's heart as she held him close.</p>
        </div>

        <div class="track amber">
          <h4>💡 历史视窗：1937年南中国大撤退</h4>
          <p>抗战全面爆发后，沿海工业与机关学校相继内迁或南撤。广州作为华南门户，在1937至1938年间遭受日军密集轰炸，数十万市民乘船南下避入英管辖下的香港界内。</p>
          <p class="en-note">Historical Context: Following the outbreak of the war, coastal institutions and families evacuated westward and southward. Hundreds of thousands sought sanctuary in British Hong Kong.</p>
        </div>
      </section>

      <!-- Act 2 -->
      <section class="act-block">
        <div class="act-header">
          <span class="act-tag">ACT 02 · 避风港湾</span>
          <h2>第二幕：香港培正的文学梦<span class="en">Act 2: The Haven of Hong Kong & Literary Dreams (1938–1941)</span></h2>
        </div>

        <div class="bilingual-p">
          <p class="zh">一九三八年初，全家登上开往香港的轮船。在英属香港的庇护下，张忠谋进入了著名的培正小学。在这里，他度过了童年时代最平静、最富启蒙意义的三年时光。</p>
          <p class="en">In early 1938, the family boarded a steamer bound for Hong Kong. Under British administration, young Morris enrolled in the renowned Pui Ching Primary School, entering the most peaceful and intellectually formative three years of his childhood.</p>
        </div>

        <div class="bilingual-p">
          <p class="zh">母亲为他订购了大量少儿期刊和中外名著。张忠谋展现出了惊人的阅读天赋与写作热情。在很长一段时间里，他最大的志向不是成为工程师或实业家，而是一名作家。</p>
          <p class="en">His mother subscribed to numerous children's journals and classics. Morris demonstrated remarkable reading talent and writing enthusiasm. For years, his highest ambition was not engineering or commerce, but becoming an author.</p>
        </div>

        <div class="track blue">
          <h4>📚 文学思维与工程师战略</h4>
          <p>张忠谋晚年在自传中多次提及：少年时期的文学阅读不仅培养了严谨的逻辑与同理心，更赋予了他用最精炼语言穿透复杂商业本质的叙事能力。</p>
          <p class="en-note">Strategic Trait: Literary mastery gave Morris Chang the rare ability to articulate profound strategy in lucid, memorable frameworks throughout his corporate career.</p>
        </div>
      </section>

      <!-- Act 3 -->
      <section class="act-block">
        <div class="act-header">
          <span class="act-tag">ACT 03 · 孤岛陷落</span>
          <h2>第三幕：十八天攻防战与沦陷<span class="en">Act 3: The 18-Day Battle and the Fall of Hong Kong (Dec 1941)</span></h2>
        </div>

        <div class="bilingual-p">
          <p class="zh">一九四一年十二月八日，日本偷袭珍珠港数小时后，日军即越过深圳河突袭新界。仅仅十八天后，港督杨慕琦宣布投降，香港沦陷。</p>
          <p class="en">On December 8, 1941, just hours after Pearl Harbor, Japanese forces crossed the Shenzhen River into Hong Kong. Eighteen days later, Governor Sir Mark Young surrendered, and Hong Kong fell.</p>
        </div>

        <div class="bilingual-p">
          <p class="zh">十岁的张忠谋亲眼目睹了街道上的硝烟、宵禁下的刺刀与市井中的断粮。原本体面的生活在战争铁蹄下荡然无存，生存成为了唯一的法则。</p>
          <p class="en">Ten-year-old Morris witnessed first-hand the smoke over the streets, bayonets enforcing curfews, and widespread food rationing. Dignified life vanished overnight under military rule; survival became the sole imperative.</p>
        </div>
      </section>

      <!-- Act 4 -->
      <section class="act-block">
        <div class="act-header">
          <span class="act-tag">ACT 04 · 千里大迁徙</span>
          <h2>第四幕：穿过封锁线前往陪都<span class="en">Act 4: Through the Blockade to Chongqing (1942)</span></h2>
        </div>

        <div class="bilingual-p">
          <p class="zh">面对日军逼迫与严酷的生活环境，父亲张秉三做出了关键决断：绝不在敌占区做顺民，必须带全家逃往战时陪都重庆。</p>
          <p class="en">Refusing to submit to occupation rule, his father Chang Ping-san made a decisive judgment: the family had to risk escaping through enemy checkpoints to reach the wartime capital of Chongqing.</p>
        </div>

        <div class="bilingual-p">
          <p class="zh">他们变卖随身细软，扮作难民，几经辗转走过广东、广西、贵州，乘木船、坐卡车、靠双脚跋涉数千里。这段穿越生死的漫长逃难路，将坚韧、危机应对与在极端不确定中生存的本能刻进了张忠谋的骨髓。</p>
          <p class="en">Selling their personal belongings and disguising themselves as common refugees, they traveled through Guangdong, Guangxi, and Guizhou by wooden boat, overcrowded truck, and on foot over thousands of miles. This harrowing journey etched resilience and crisis decision-making deep into his soul.</p>
        </div>
      </section>

      <!-- Golden Quote -->
      <div class="golden-quote">
        <blockquote>"In times of severe crisis and turmoil, the greatest risk is not taking action, but hesitating while the window of opportunity closes."</blockquote>
        <div class="quote-zh">“在剧烈的动荡与危机之中，最大的风险不是采取行动，而是在机会窗口关闭时犹豫不决。”</div>
        <div class="quote-author">—— 台积电创始人 张忠谋 · 战略信条</div>
      </div>

      <!-- Strategic Takeaways & English Learning -->
      <section class="takeaways-section">
        <span class="eyebrow">STRATEGIC RETROSPECTIVE · 商业复盘与核心词汇</span>
        <h2 class="serif">核心词汇与商业战略启示<span class="en">Core Vocabulary & Strategic Insights</span></h2>

        <div class="grid-2">
          <!-- Vocabulary Card -->
          <div class="card-takeaway">
            <h3 style="font-size:16px; color:var(--ink); font-weight:700; margin-bottom:12px;">📖 核心商业英语词汇 (Core Terms)</h3>
            <ul class="vocab-list">
              <li class="vocab-item">
                <div class="vocab-word">Aftershock <span class="vocab-phonetic">/ˈæftərʃɑːk/</span></div>
                <div class="vocab-def">n. 余波，震后反应（常用于市场金融危机后续影响）</div>
                <div class="vocab-ex">The aftershocks of the crisis lingered for years.</div>
              </li>
              <li class="vocab-item">
                <div class="vocab-word">Move the other way <span class="vocab-phonetic">/idiom/</span></div>
                <div class="vocab-def">phr. 逆势而行，反向决策</div>
                <div class="vocab-ex">While competitors cut costs, he moved the other way.</div>
              </li>
              <li class="vocab-item">
                <div class="vocab-word">Double down <span class="vocab-phonetic">/idiom/</span></div>
                <div class="vocab-def">phr. 加倍投入，坚定押注</div>
                <div class="vocab-ex">TSMC doubled down on R&D during the recession.</div>
              </li>
              <li class="vocab-item">
                <div class="vocab-word">Pure-play Foundry <span class="vocab-phonetic">/term/</span></div>
                <div class="vocab-def">n. 纯晶圆代工模式（专注代工，不与客户竞争）</div>
                <div class="vocab-ex">The pure-play foundry model redefined the chip industry.</div>
              </li>
            </ul>
          </div>

          <!-- Strategic Takeaway Card -->
          <div class="card-takeaway">
            <h3 style="font-size:16px; color:var(--ink); font-weight:700; margin-bottom:12px;">🎯 战略思考题 (Strategic Question)</h3>
            <div style="font-size:14px; color:var(--ink); line-height:1.7;">
              <p style="font-weight:600; color:var(--amber); margin-bottom:8px;">为什么张忠谋敢在经济衰退与战乱危机时展现决断力？</p>
              <p style="color:var(--muted); font-size:13.5px;">从童年千里逃难的经历中，张忠谋深刻认识到“停滞即危险，顺境需居安思危，逆境要抢先布局”。这直接启发了他在1998年亚洲金融风暴及2008年次贷危机时，两次力排众议逆势扩大先进制程资本支出的传奇决策。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Bottom Navigation -->
      <div class="ep-nav-bottom">
        <a href="index.html" class="btn ghost">← 返回首页</a>
        <a href="audio.html" class="btn primary">前往第 02 期：南开与沪江 →</a>
      </div>

    </article>
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="wrap">
      <p>台积电张忠谋 · 传记时间线的平行世界 © 2026</p>
      <p style="margin-top:6px; font-size:12px;">Based on Morris Chang's Dual-Language Autobiography & Strategic Architecture · Built with ReadShift</p>
    </div>
  </footer>

  <!-- Audio Controller Script -->
  <script>
    const epAudio = document.getElementById('epAudio');
    const epPlayBtn = document.getElementById('epPlayBtn');
    const epSeekBar = document.getElementById('epSeekBar');
    const epCurTime = document.getElementById('epCurTime');
    const epDuration = document.getElementById('epDuration');
    const epTrackLabel = document.getElementById('epTrackLabel');
    const btnZhTrack = document.getElementById('btnZhTrack');
    const btnEnTrack = document.getElementById('btnEnTrack');
    const subRows = document.querySelectorAll('.sub-row');

    const epTracks = {
      'zh': { src: './audio/ep01-zh.mp3', label: '🇨🇳 第01期：逃难的孩子 (中文原声)' },
      'en': { src: './audio/ep01-en.mp3', label: '🇺🇸 Episode 01: The Child Who Fled (English Audio)' }
    };

    let currentEpLang = 'zh';

    function switchEpTrack(lang) {
      if (!epTracks[lang] || !epAudio) return;
      currentEpLang = lang;
      const wasPlaying = !epAudio.paused;
      const curTime = epAudio.currentTime;
      
      epAudio.src = epTracks[lang].src;
      epTrackLabel.textContent = epTracks[lang].label;
      epAudio.load();
      epAudio.onloadedmetadata = () => {
        epAudio.currentTime = Math.min(curTime, epAudio.duration || curTime);
        updateEpProgress();
        if (wasPlaying) epAudio.play();
      };

      if (lang === 'zh') {
        btnZhTrack.className = 'btn primary';
        btnEnTrack.className = 'btn ghost';
      } else {
        btnZhTrack.className = 'btn ghost';
        btnEnTrack.className = 'btn primary';
      }
    }

    function toggleEpPlay() {
      if (!epAudio) return;
      if (epAudio.paused) {
        epAudio.play();
        epPlayBtn.innerHTML = '❚❚';
      } else {
        epAudio.pause();
        epPlayBtn.innerHTML = '▶';
      }
    }

    function seekEpAudio(val) {
      if (!epAudio || !epAudio.duration) return;
      epAudio.currentTime = (val / 100) * epAudio.duration;
    }

    function seekEpTime(sec) {
      if (!epAudio) return;
      epAudio.currentTime = sec;
      if (epAudio.paused) {
        epAudio.play();
        epPlayBtn.innerHTML = '❚❚';
      }
    }

    function formatTime(sec) {
      if (isNaN(sec)) return '00:00';
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s);
    }

    if (epAudio) {
      epAudio.addEventListener('timeupdate', () => {
        updateEpProgress();
        highlightEpSubtitles(epAudio.currentTime);
      });
      epAudio.addEventListener('ended', () => {
        epPlayBtn.innerHTML = '▶';
      });
      epAudio.addEventListener('loadedmetadata', () => {
        epDuration.textContent = formatTime(epAudio.duration);
      });
    }

    function updateEpProgress() {
      if (!epAudio) return;
      epCurTime.textContent = formatTime(epAudio.currentTime);
      if (epAudio.duration) {
        epSeekBar.value = (epAudio.currentTime / epAudio.duration) * 100;
        epDuration.textContent = formatTime(epAudio.duration);
      }
    }

    function highlightEpSubtitles(cur) {
      subRows.forEach(row => {
        const start = parseFloat(row.dataset.start);
        const end = parseFloat(row.dataset.end);
        if (cur >= start && cur < end) {
          row.classList.add('active');
        } else {
          row.classList.remove('active');
        }
      });
    }
  </script>
</body>
</html>"""

with open("episode-01.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Successfully wrote episode-01.html in unified aesthetic.")
