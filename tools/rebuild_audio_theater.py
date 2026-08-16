#!/usr/bin/env python3
"""Rebuild audio.html (self-contained bilingual theater) + audio_data.js.

Fixes:
1. Missing DOM elements (playIcon, btnPrev, btnNext, volSlider, btnToggleSidebar)
   that crashed the boot script before renderEpisodeList().
2. Ghost subtitle cues (【音效】/【主叙述者】/## headers) that TTS never reads,
   causing audio/subtitle drift. Uses the same clean_segments logic as make_tts.py.
3. Subtitle auto-scroll inside the container (centered), not window.scrollIntoView.
"""
import os
import re
import json
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

EPISODE_DIR = "03-剧集"
AUDIO_DIR = "audio"
PAUSE = 0.7  # same as make_tts.py


def clean_segments(text):
    """Identical logic to make_tts.py: only lines the TTS actually reads."""
    lines = text.splitlines()
    segs = []
    cur = []
    for line in lines:
        s = line.strip()
        if re.match(r"^#{1,6}\s", s):
            continue
        if s.startswith(">"):
            continue
        if re.match(r"^-{3,}$", s):
            continue
        if re.match(r"^【|^\[SFX|^\[Main\s+narrator|^\[Narrator|^\[主叙述者", s):
            continue
        if not s:
            if cur:
                segs.append(" ".join(cur))
                cur = []
            continue
        cur.append(s)
    if cur:
        segs.append(" ".join(cur))
    out = []
    for s in segs:
        s = s.replace("**", "").replace("__", "")
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            out.append(s)
    return out


def measure_mp3(path):
    """Return duration in seconds using afinfo (macOS)."""
    try:
        res = subprocess.run(["afinfo", path], capture_output=True, text=True)
        m = re.search(r"estimated duration:\s*([0-9\.]+)\s*sec", res.stdout)
        if m:
            return float(m.group(1))
    except Exception:
        pass
    return 0.0


def build_episode(idx):
    ep_str = f"{idx:02d}"
    matches = [d for d in os.listdir(EPISODE_DIR) if d.startswith(f"第{ep_str}期")]
    folder = os.path.join(EPISODE_DIR, matches[0]) if matches else None

    zh_file = os.path.join(folder, "中文文字稿.md") if folder else None
    en_file = os.path.join(folder, "英文文字稿.md") if folder else None
    zh_raw = open(zh_file, encoding="utf-8").read() if zh_file and os.path.exists(zh_file) else ""
    en_raw = open(en_file, encoding="utf-8").read() if en_file and os.path.exists(en_file) else ""

    zh_segs = clean_segments(zh_raw)
    en_segs = clean_segments(en_raw)

    mp3_zh = os.path.join(AUDIO_DIR, f"ep{ep_str}-zh.mp3")
    mp3_en = os.path.join(AUDIO_DIR, f"ep{ep_str}-en.mp3")
    dur_zh = measure_mp3(mp3_zh) if os.path.exists(mp3_zh) else 0.0
    dur_en = measure_mp3(mp3_en) if os.path.exists(mp3_en) else 0.0

    # Weight = phoneme time + punctuation pause + inter-segment silence
    def weights(segs):
        w = []
        for s in segs:
            chars = len(s)
            commas = len(re.findall(r"[，,、；;]", s))
            periods = len(re.findall(r"[。\.！？!\?]", s))
            dashes = len(re.findall(r"[——:：—]", s))
            wt = chars / 3.85 + commas * 0.35 + periods * 0.8 + dashes * 0.5 + PAUSE
            w.append(max(1.0, wt))
        return w

    zh_w = weights(zh_segs)
    total_w = sum(zh_w) or 1.0
    scale = (dur_zh / total_w) if dur_zh > 0 else 1.0

    cues = []
    t = 0.0
    for i, s in enumerate(zh_segs):
        d = zh_w[i] * scale
        st = round(t, 2)
        et = round(t + d, 2)
        t += d
        cues.append({
            "idx": i,
            "start": st,
            "end": et,
            "zh": s,
            "en": en_segs[i] if i < len(en_segs) else "",
        })

    title = f"第{ep_str}期"
    en_title = f"Episode {ep_str}"
    if folder:
        m = re.search(r"第\d+期[ -]*(.*)", os.path.basename(folder))
        if m and m.group(1).strip():
            title = f"第{ep_str}期 {m.group(1).strip()}"
            en_title = f"Episode {ep_str}: {m.group(1).strip()}"

    return {
        "id": ep_str,
        "title": title,
        "enTitle": en_title,
        "audioZh": f"audio/ep{ep_str}-zh.mp3",
        "audioEn": f"audio/ep{ep_str}-en.mp3",
        "durationZh": round(dur_zh, 2),
        "durationEn": round(dur_en, 2),
        "cuesCount": len(cues),
        "cues": cues,
    }


def build_all():
    episodes = []
    for i in range(19):
        ep = build_episode(i)
        episodes.append(ep)
        print(f"Ep {ep['id']}: {len(ep['cues'])} cues | zh {ep['durationZh']}s")
    return episodes


NAV = """<nav class="unified-top-nav" style="position: fixed; top: 0; left: 0; right: 0; z-index: 9999; height: 58px; background: rgba(8,12,20,0.95); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid var(--line, #26262b); display: flex; align-items: center; justify-content: space-between; padding: 0 24px; box-sizing: border-box;">
  <a href="index.html" class="unified-brand" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: #f3f0e8; font-weight: 700; font-size: 14.5px;">
    <img src="logo.svg" alt="MC Logo" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #333; display: block;">
    <span>台积电张忠谋 · 双语剧场</span>
  </a>
  <div class="unified-nav-links" style="display: flex; align-items: center; gap: 18px;">
    <a href="index.html" style="color: #a29c90; text-decoration: none; font-size: 13px;">🏠 官网首页</a>
    <a href="reader.html" style="color: #a29c90; text-decoration: none; font-size: 13px;">📖 全册电子书</a>
    <a href="audio.html" style="color: #F59E0B; text-decoration: none; font-size: 13px; font-weight: 600;">🎙️ 双语剧场</a>
    <a href="map.html" style="color: #a29c90; text-decoration: none; font-size: 13px;">🗺️ 平行地图</a>
    <a href="cards.html" style="color: #a29c90; text-decoration: none; font-size: 13px;">🎴 金句卡片</a>
    <a href="https://github.com/Martin-MQtech/ReadShift" target="_blank" style="background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); color: #F59E0B; font-size: 11px; padding: 4px 10px; border-radius: 999px; font-weight: 600; text-decoration: none;">🚀 ReadShift 主体工程</a>
  </div>
</nav>"""


def render_html(episodes):
    manifest_json = json.dumps(episodes, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>双语音频剧场 | 台积电张忠谋 · 传记时间线的平行世界</title>
<meta name="description" content="台积电张忠谋传记时间线的平行世界 · 沉浸式双语音频剧场。逐句时间戳高亮对齐、中英双语切换、点击定点跳转。">
<style>
  :root {{
    --bg:#0a0a0a; --bg2:#111113; --card:#16161a; --line:#26262b;
    --amber:#F59E0B; --blue:#38BDF8; --ink:#ece9e2; --muted:#a29c90;
    --sans:"PingFang SC","Microsoft YaHei",-apple-system,sans-serif;
    --serif:"Songti SC","Noto Serif SC",STSong,Georgia,serif;
    --en:"Georgia","Times New Roman",serif;
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  html,body {{ height:100%; background:var(--bg); color:var(--ink); font-family:var(--sans); overflow:hidden; }}

  /* ── Theater layout ── */
  .theater {{ display:flex; height:calc(100vh - 58px - 76px); margin-top:58px; }}
  .sidebar {{ width:340px; background:var(--bg2); border-right:1px solid var(--line); display:flex; flex-direction:column; flex-shrink:0; }}
  .sidebar-head {{ padding:18px 20px; border-bottom:1px solid var(--line); }}
  .sidebar-head h2 {{ font-size:14px; font-weight:700; letter-spacing:1px; color:var(--amber); }}
  .ep-list {{ flex:1; overflow-y:auto; padding:10px; list-style:none; display:flex; flex-direction:column; gap:6px; }}
  .ep-item {{ padding:12px 14px; border-radius:10px; background:var(--card); border:1px solid transparent; cursor:pointer; transition:all .2s ease; }}
  .ep-item:hover {{ background:rgba(255,255,255,0.03); border-color:rgba(255,255,255,0.08); }}
  .ep-item.active {{ background:rgba(245,158,11,0.12); border-color:var(--amber); }}
  .ep-badge-row {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }}
  .ep-id {{ font-size:10.5px; font-family:monospace; color:var(--amber); background:rgba(245,158,11,0.12); padding:2px 8px; border-radius:4px; }}
  .ep-duration {{ font-size:10px; font-family:monospace; color:var(--muted); }}
  .ep-title-zh {{ font-size:13.5px; font-weight:600; color:var(--ink); }}
  .ep-item.active .ep-title-zh {{ color:var(--amber); }}
  .ep-title-en {{ font-family:var(--en); font-style:italic; font-size:11px; color:var(--muted); }}

  .stage {{ flex:1; display:flex; flex-direction:column; background:var(--bg); overflow:hidden; }}
  .stage-head {{ padding:14px 28px; border-bottom:1px solid var(--line); display:flex; justify-content:space-between; align-items:center; background:rgba(17,17,19,0.9); }}
  .current-meta h3 {{ font-family:var(--serif); font-size:18px; color:var(--ink); font-weight:700; }}
  .current-meta p {{ font-family:var(--en); font-style:italic; font-size:12px; color:var(--muted); margin-top:2px; }}
  .view-toggles {{ display:flex; gap:6px; background:rgba(0,0,0,0.4); padding:3px; border-radius:8px; border:1px solid var(--line); }}
  .mode-btn {{ padding:5px 12px; border-radius:6px; border:none; background:transparent; color:var(--muted); font-size:12px; cursor:pointer; }}
  .mode-btn.active {{ background:var(--amber); color:#000; font-weight:600; }}

  .subtitles-viewport {{ flex:1; overflow-y:auto; padding:40px 18% 120px; scroll-behavior:smooth; position:relative; }}
  .subtitles-viewport.hide-en .cue-en {{ display:none; }}
  .subtitles-viewport.hide-zh .cue-zh {{ display:none; }}
  .cue-group {{ padding:16px 20px; border-radius:12px; border-left:3px solid transparent; margin-bottom:14px; cursor:pointer; transition:all .25s ease; }}
  .cue-group:hover {{ background:rgba(255,255,255,0.02); }}
  .cue-group.active {{ background:rgba(245,158,11,0.09); border-left-color:var(--amber); }}
  .cue-zh {{ font-family:var(--serif); font-size:16.5px; line-height:1.8; color:var(--ink); }}
  .cue-en {{ font-family:var(--en); font-style:italic; font-size:14px; line-height:1.65; color:var(--muted); margin-top:3px; }}
  .cue-group.active .cue-zh {{ color:#fff; font-weight:600; }}
  .cue-group.active .cue-en {{ color:var(--blue); }}

  /* ── Player dock ── */
  .player-dock {{ position:fixed; bottom:0; left:0; right:0; height:76px; background:rgba(17,17,19,0.98); border-top:1px solid var(--line); display:flex; align-items:center; justify-content:space-between; padding:0 24px; z-index:9999; gap:20px; }}
  .dock-left {{ display:flex; align-items:center; gap:12px; min-width:230px; }}
  .btn-play-hero {{ width:44px; height:44px; border-radius:50%; background:var(--amber); border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; }}
  .btn-play-hero svg {{ width:18px; height:18px; fill:#000; }}
  .track-toggle-grp {{ display:flex; gap:6px; }}
  .track-btn {{ padding:5px 10px; border-radius:6px; font-size:11px; cursor:pointer; border:1px solid var(--line); background:var(--bg); color:var(--muted); }}
  .track-btn.active {{ background:var(--amber); color:#000; border-color:var(--amber); font-weight:600; }}
  .dock-center {{ flex:1; display:flex; align-items:center; gap:12px; max-width:620px; }}
  .time-lbl {{ font-family:monospace; font-size:11px; color:var(--muted); min-width:42px; text-align:center; }}
  .progress-track {{ flex:1; height:6px; background:rgba(255,255,255,0.08); border-radius:3px; position:relative; cursor:pointer; }}
  .progress-fill {{ height:100%; width:0%; background:linear-gradient(90deg,var(--amber),var(--blue)); border-radius:3px; }}
  .dock-right {{ display:flex; align-items:center; gap:12px; }}
  .ctrl-btn {{ background:transparent; border:none; color:var(--muted); cursor:pointer; font-size:16px; }}
  .ctrl-btn:hover {{ color:var(--amber); }}
  .speed-sel {{ background:var(--bg); border:1px solid var(--line); color:var(--ink); border-radius:6px; padding:4px 8px; font-size:11px; }}
  .vol-slider {{ width:80px; accent-color:var(--amber); cursor:pointer; }}

  @media (max-width:900px) {{
    .sidebar {{ position:fixed; top:58px; bottom:76px; left:0; transform:translateX(-100%); transition:transform .25s ease; z-index:9998; }}
    .sidebar.open {{ transform:translateX(0); }}
    .menu-toggle {{ display:block; }}
    .subtitles-viewport {{ padding:24px 16px 120px; }}
    .unified-nav-links {{ display:none; }}
  }}
  .menu-toggle {{ display:none; background:transparent; border:1px solid var(--line); color:var(--ink); padding:6px 10px; border-radius:6px; cursor:pointer; font-size:13px; }}
</style>
</head>
<body>

{NAV}

<div class="theater">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-head">
      <h2>⚡ 剧集与乐章目录 (19集全景)</h2>
    </div>
    <ul class="ep-list" id="episodeList"></ul>
  </aside>

  <main class="stage">
    <div class="stage-head">
      <div class="current-meta">
        <h3 id="currentEpTitle">第 00 期 全册导读</h3>
        <p id="currentEpEnTitle">Episode 00: A Guide to the Whole Volume</p>
      </div>
      <div class="view-toggles">
        <button class="mode-btn active" data-mode="both">🌐 双语对照</button>
        <button class="mode-btn" data-mode="zh">🇨🇳 仅中文</button>
        <button class="mode-btn" data-mode="en">🇺🇸 仅英文</button>
      </div>
    </div>
    <div class="subtitles-viewport" id="subtitlesContainer"></div>
  </main>
</div>

<div class="player-dock">
  <div class="dock-left">
    <button id="btnPlay" class="btn-play-hero" onclick="togglePlay()">
      <svg id="playIcon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
    </button>
    <button id="btnPrev" class="ctrl-btn" title="上一集">⏮</button>
    <button id="btnNext" class="ctrl-btn" title="下一集">⏭</button>
    <div class="track-toggle-grp">
      <button id="btnTrackZh" class="track-btn active" onclick="switchTrack('zh')">🇨🇳 中文</button>
      <button id="btnTrackEn" class="track-btn" onclick="switchTrack('en')">🇺🇸 English</button>
    </div>
    <button id="btnToggleSidebar" class="menu-toggle">☰ 目录</button>
  </div>
  <div class="dock-center">
    <span id="curTimeText" class="time-lbl">00:00</span>
    <div id="progressTrack" class="progress-track"><div id="progressFill" class="progress-fill"></div></div>
    <span id="totalTimeText" class="time-lbl">00:00</span>
  </div>
  <div class="dock-right">
    <select id="speedSelect" class="speed-sel">
      <option value="0.8">0.8x</option>
      <option value="1.0" selected>1.0x</option>
      <option value="1.25">1.25x</option>
      <option value="1.5">1.5x</option>
    </select>
    <input id="volSlider" class="vol-slider" type="range" min="0" max="1" step="0.05" value="1">
  </div>
</div>

<audio id="audioEl" preload="metadata"></audio>

<script>
// ──────────────────────────────────────────────────────────────
// 自包含双语剧场数据（与 make_tts.py clean_segments 严格对齐）
// ──────────────────────────────────────────────────────────────
const EMBEDDED_MANIFEST = {manifest_json};

const state = {{
  episodes: (window.AUDIO_DATA && window.AUDIO_DATA.length > 0) ? window.AUDIO_DATA
           : ((window.EPISODES_DATA && window.EPISODES_DATA.length > 0) ? window.EPISODES_DATA : EMBEDDED_MANIFEST),
  currentEpIndex: 0,
  lang: 'zh',
  mode: 'both',
  isPlaying: false,
  currentTime: 0,
  duration: 0
}};

const audioEl = document.getElementById('audioEl');
const episodeListEl = document.getElementById('episodeList');
const subtitlesContainer = document.getElementById('subtitlesContainer');
const currentEpTitle = document.getElementById('currentEpTitle');
const currentEpEnTitle = document.getElementById('currentEpEnTitle');
const curTimeText = document.getElementById('curTimeText');
const totalTimeText = document.getElementById('totalTimeText');
const progressTrack = document.getElementById('progressTrack');
const progressFill = document.getElementById('progressFill');
const btnPlay = document.getElementById('btnPlay');
const playIcon = document.getElementById('playIcon');
const btnPrev = document.getElementById('btnPrev');
const btnNext = document.getElementById('btnNext');
const btnTrackZh = document.getElementById('btnTrackZh');
const btnTrackEn = document.getElementById('btnTrackEn');
const speedSelect = document.getElementById('speedSelect');
const volSlider = document.getElementById('volSlider');
const btnToggleSidebar = document.getElementById('btnToggleSidebar');
const sidebar = document.getElementById('sidebar');

function formatTime(secs) {{
  if (isNaN(secs) || secs < 0) return '00:00';
  const m = Math.floor(secs / 60);
  const s = Math.floor(secs % 60);
  return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
}}

// ── 剧集列表 ──
function renderEpisodeList() {{
  if (!episodeListEl) return;
  episodeListEl.innerHTML = '';
  state.episodes.forEach((ep, idx) => {{
    const li = document.createElement('li');
    li.className = 'ep-item ' + (idx === state.currentEpIndex ? 'active' : '');
    li.onclick = () => {{
      loadEpisode(idx, true);
      if (window.innerWidth <= 900 && sidebar) sidebar.classList.remove('open');
    }};
    li.innerHTML = '<div class="ep-badge-row">' +
        '<span class="ep-id">EP.' + ep.id + '</span>' +
        '<span class="ep-duration">' + formatTime(ep.durationZh || 360) + '</span>' +
      '</div>' +
      '<div class="ep-title-zh">' + ep.title + '</div>' +
      '<div class="ep-title-en">' + (ep.enTitle || '') + '</div>';
    episodeListEl.appendChild(li);
  }});
}}

// ── 加载剧集 ──
function loadEpisode(index, autoPlay = false) {{
  state.currentEpIndex = index;
  const ep = state.episodes[index];
  if (!ep) return;

  if (currentEpTitle) currentEpTitle.textContent = ep.title;
  if (currentEpEnTitle) currentEpEnTitle.textContent = ep.enTitle || '';

  document.querySelectorAll('.ep-item').forEach((item, idx) => {{
    item.classList.toggle('active', idx === index);
  }});

  renderSubtitles(ep);

  const audioSrc = state.lang === 'zh' ? (ep.audioZh || '') : (ep.audioEn || '');
  audioEl.src = audioSrc;
  audioEl.load();

  state.duration = (state.lang === 'zh' ? ep.durationZh : ep.durationEn) || 300;
  totalTimeText.textContent = formatTime(state.duration);

  audioEl.onloadedmetadata = () => {{
    if (audioEl.duration && !isNaN(audioEl.duration)) {{
      state.duration = audioEl.duration;
      totalTimeText.textContent = formatTime(state.duration);
    }}
    if (autoPlay) playAudio();
  }};

  state.currentTime = 0;
  updateTimelineUI(0);
  if (autoPlay) playAudio();
}}

// ── 字幕渲染 ──
function renderSubtitles(ep) {{
  if (!subtitlesContainer) return;
  subtitlesContainer.innerHTML = '';
  if (!ep.cues || ep.cues.length === 0) {{
    subtitlesContainer.innerHTML = '<div style="text-align:center; padding:40px; color:var(--muted);">本乐章暂无逐句字幕</div>';
    return;
  }}
  ep.cues.forEach((cue, cIdx) => {{
    const div = document.createElement('div');
    div.className = 'cue-group';
    div.id = 'cue-' + cIdx;
    div.dataset.start = cue.start;
    div.dataset.end = cue.end;
    div.onclick = () => {{
      seekTo(cue.start);
      if (!state.isPlaying) playAudio();
    }};
    const zhHtml = cue.zh ? '<div class="cue-zh">' + cue.zh + '</div>' : '';
    const enHtml = cue.en ? '<div class="cue-en">' + cue.en + '</div>' : '';
    div.innerHTML = zhHtml + enHtml;
    subtitlesContainer.appendChild(div);
  }});
}}

// ── 字幕同步（容器内居中滚动，不滚动整个页面）──
let currentActiveCue = -1;
let isUserScrolling = false;
let scrollTimer = null;

if (subtitlesContainer) {{
  subtitlesContainer.addEventListener('wheel', () => onUserScroll(), {{ passive: true }});
  subtitlesContainer.addEventListener('touchstart', () => onUserScroll(), {{ passive: true }});
  subtitlesContainer.addEventListener('touchmove', () => onUserScroll(), {{ passive: true }});
}}
function onUserScroll() {{
  isUserScrolling = true;
  clearTimeout(scrollTimer);
  scrollTimer = setTimeout(() => {{ isUserScrolling = false; }}, 4000);
}}

function scrollSubtitleToCenter(el) {{
  if (!el || !subtitlesContainer || isUserScrolling) return;
  const cRect = subtitlesContainer.getBoundingClientRect();
  const eRect = el.getBoundingClientRect();
  const relativeTop = eRect.top - cRect.top + subtitlesContainer.scrollTop;
  const target = relativeTop - (cRect.height / 2) + (eRect.height / 2);
  subtitlesContainer.scrollTo({{ top: Math.max(0, target), behavior: 'smooth' }});
}}

function syncSubtitles(time) {{
  const ep = state.episodes[state.currentEpIndex];
  if (!ep || !ep.cues) return;
  let activeIdx = -1;
  for (let i = 0; i < ep.cues.length; i++) {{
    if (time >= ep.cues[i].start && time <= ep.cues[i].end) {{
      activeIdx = i;
      break;
    }}
  }}
  if (activeIdx !== currentActiveCue) {{
    currentActiveCue = activeIdx;
    document.querySelectorAll('.cue-group').forEach((el, idx) => {{
      if (idx === activeIdx) {{
        el.classList.add('active');
        scrollSubtitleToCenter(el);
      }} else {{
        el.classList.remove('active');
      }}
    }});
  }}
}}

function updateTimelineUI(time) {{
  curTimeText.textContent = formatTime(time);
  const ratio = state.duration > 0 ? (time / state.duration) : 0;
  progressFill.style.width = Math.min(100, Math.max(0, ratio * 100)) + '%';
}}

// ── 播放控制 ──
let timerFallback = null;

function playAudio() {{
  state.isPlaying = true;
  if (playIcon) playIcon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
  const playPromise = audioEl.play();
  if (playPromise !== undefined) {{
    playPromise.catch(() => startFallbackTimer());
  }}
}}

function pauseAudio() {{
  state.isPlaying = false;
  if (playIcon) playIcon.innerHTML = '<path d="M8 5v14l11-7z"/>';
  audioEl.pause();
  if (timerFallback) clearInterval(timerFallback);
}}

function togglePlay() {{
  if (state.isPlaying) pauseAudio();
  else playAudio();
}}

function seekTo(seconds) {{
  state.currentTime = seconds;
  audioEl.currentTime = seconds;
  updateTimelineUI(seconds);
  syncSubtitles(seconds);
}}

function startFallbackTimer() {{
  if (timerFallback) clearInterval(timerFallback);
  timerFallback = setInterval(() => {{
    if (!state.isPlaying) return;
    state.currentTime += 0.25 * (audioEl.playbackRate || 1);
    if (state.currentTime >= state.duration) {{
      pauseAudio();
      if (state.currentEpIndex < state.episodes.length - 1) loadEpisode(state.currentEpIndex + 1, true);
      return;
    }}
    updateTimelineUI(state.currentTime);
    syncSubtitles(state.currentTime);
  }}, 250);
}}

function switchTrack(lang) {{
  if (state.lang === lang) return;
  const savedTime = state.currentTime;
  const wasPlaying = state.isPlaying;
  state.lang = lang;
  if (btnTrackZh) btnTrackZh.classList.toggle('active', lang === 'zh');
  if (btnTrackEn) btnTrackEn.classList.toggle('active', lang === 'en');
  loadEpisode(state.currentEpIndex, false);
  seekTo(savedTime);
  if (wasPlaying) playAudio();
}}

// ── 事件绑定（全部判空，杜绝 null 崩溃）──
audioEl.ontimeupdate = () => {{
  state.currentTime = audioEl.currentTime;
  updateTimelineUI(state.currentTime);
  syncSubtitles(state.currentTime);
}};
audioEl.onended = () => {{
  pauseAudio();
  if (state.currentEpIndex < state.episodes.length - 1) loadEpisode(state.currentEpIndex + 1, true);
}};
if (btnPlay) btnPlay.onclick = togglePlay;
if (btnPrev) btnPrev.onclick = () => {{ if (state.currentEpIndex > 0) loadEpisode(state.currentEpIndex - 1, state.isPlaying); }};
if (btnNext) btnNext.onclick = () => {{ if (state.currentEpIndex < state.episodes.length - 1) loadEpisode(state.currentEpIndex + 1, state.isPlaying); }};
if (btnTrackZh) btnTrackZh.onclick = () => switchTrack('zh');
if (btnTrackEn) btnTrackEn.onclick = () => switchTrack('en');

document.querySelectorAll('.mode-btn').forEach(btn => {{
  btn.onclick = () => {{
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.mode = btn.dataset.mode;
    if (subtitlesContainer) {{
      subtitlesContainer.className = 'subtitles-viewport';
      if (state.mode === 'zh') subtitlesContainer.classList.add('hide-en');
      if (state.mode === 'en') subtitlesContainer.classList.add('hide-zh');
    }}
  }};
}});

if (speedSelect) speedSelect.onchange = (e) => {{ audioEl.playbackRate = parseFloat(e.target.value); }};
if (volSlider) volSlider.oninput = (e) => {{ audioEl.volume = parseFloat(e.target.value); }};
if (progressTrack) progressTrack.onclick = (e) => {{
  const rect = progressTrack.getBoundingClientRect();
  const clickRatio = (e.clientX - rect.left) / rect.width;
  seekTo(clickRatio * state.duration);
}};
if (btnToggleSidebar && sidebar) {{
  btnToggleSidebar.onclick = () => sidebar.classList.toggle('open');
}}

// URL ?ep=01 直达
let initIdx = 0;
try {{
  const targetEp = new URLSearchParams(window.location.search).get('ep');
  if (targetEp) {{
    const foundIdx = state.episodes.findIndex(e => e.id === targetEp || e.id === String(targetEp).padStart(2, '0'));
    if (foundIdx !== -1) initIdx = foundIdx;
  }}
}} catch (e) {{}}

// 启动
renderEpisodeList();
loadEpisode(initIdx, false);
</script>
</body>
</html>"""


def main():
    episodes = build_all()
    html = render_html(episodes)

    with open("audio.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\naudio.html 写入完成 ({len(html)} bytes)")

    # Also write audio_data.js (window.AUDIO_DATA + window.EPISODES_DATA)
    js = "// 自动生成：全19期双语剧场数据（clean_segments 严格对齐，无幽灵字幕）\n"
    js += "window.AUDIO_DATA = " + json.dumps(episodes, ensure_ascii=False) + ";\n"
    js += "window.EPISODES_DATA = window.AUDIO_DATA;\n"
    with open("audio_data.js", "w", encoding="utf-8") as f:
        f.write(js)
    print(f"audio_data.js 写入完成 ({len(js)} bytes)")


if __name__ == "__main__":
    main()
