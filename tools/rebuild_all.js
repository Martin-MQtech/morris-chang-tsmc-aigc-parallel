const fs = require('fs');
const path = require('path');

const baseDir = '/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC';

// 1. Read audio_data.js
let audioDataCode = fs.readFileSync(path.join(baseDir, 'audio_data.js'), 'utf8');

// Ensure audio_data.js defines both AUDIO_DATA and EPISODES_DATA
if (!audioDataCode.includes('window.EPISODES_DATA = window.AUDIO_DATA')) {
  audioDataCode += '\nif (typeof window !== "undefined") { window.EPISODES_DATA = window.AUDIO_DATA; }\n';
  fs.writeFileSync(path.join(baseDir, 'audio_data.js'), audioDataCode, 'utf8');
}

const sandbox = { window: {} };
eval('(function(window) { ' + audioDataCode + ' })(sandbox.window)');
const allEpisodes = sandbox.window.AUDIO_DATA || sandbox.window.EPISODES_DATA || [];
console.log(`Loaded ${allEpisodes.length} episodes from audio_data.js`);

// Common Unified Top Nav HTML
function getUnifiedNavHtml(activePage) {
  return `<!-- Unified Locked Top Navigation Bar -->
<nav class="unified-top-nav">
  <div class="unified-nav-inner">
    <a href="index.html" class="unified-brand">
      <img src="assets/logo.svg" alt="Logo" onerror="this.src='logo.svg'; this.onerror=null;">
      <span>台积电张忠谋 · 传记时间线的平行世界</span>
    </a>
    <ul class="unified-nav-links">
      <li><a href="index.html"${activePage === 'index' ? ' class="active"' : ''}>🏠 官网首页</a></li>
      <li><a href="reader.html"${activePage === 'reader' ? ' class="active"' : ''}>📖 全册电子书</a></li>
      <li><a href="audio.html"${activePage === 'audio' ? ' class="active"' : ''}>🎙️ 双语剧场</a></li>
      <li><a href="map.html"${activePage === 'map' ? ' class="active"' : ''}>🗺️ 平行地图</a></li>
      <li><a href="cards.html"${activePage === 'cards' ? ' class="active"' : ''}>🎴 金句卡片</a></li>
      <li><a href="https://github.com/Martin-MQtech/ReadShift" target="_blank" class="unified-nav-btn">🚀 ReadShift 主体工程</a></li>
    </ul>
  </div>
</nav>`;
}

// Common Unified Top Nav CSS
const unifiedNavCss = `
/* Unified Global Locked Top Navigation Bar */
.unified-top-nav {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  width: 100% !important;
  height: 58px !important;
  z-index: 9999 !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  background: rgba(8, 12, 20, 0.94) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-sizing: border-box !important;
  display: flex !important;
  align-items: center !important;
}
.unified-nav-inner {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}
.unified-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #f3f0e8;
  font-weight: 600;
  font-family: "Songti SC", "Noto Serif SC", serif;
  font-size: 15px;
  letter-spacing: 0.5px;
  white-space: nowrap;
}
.unified-brand:hover {
  color: #d97706;
}
.unified-brand img {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: block;
}
.unified-nav-links {
  display: flex;
  align-items: center;
  gap: 12px;
  list-style: none;
  margin: 0;
  padding: 0;
}
.unified-nav-links a {
  text-decoration: none;
  font-size: 13px;
  color: #a29c90;
  padding: 5px 10px;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}
.unified-nav-links a:hover {
  color: #f3f0e8;
  background: rgba(255, 255, 255, 0.05);
}
.unified-nav-links a.active {
  color: #00f0ff;
  font-weight: 600;
  background: rgba(0, 240, 255, 0.1);
  border: 1px solid rgba(0, 240, 255, 0.25);
}
.unified-nav-btn {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%) !important;
  color: #fff !important;
  font-weight: 600 !important;
  padding: 5px 12px !important;
  border-radius: 6px !important;
  box-shadow: 0 2px 8px rgba(217, 119, 6, 0.3) !important;
}
.unified-nav-btn:hover {
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.5) !important;
  transform: translateY(-1px);
}
@media (max-width: 768px) {
  .unified-nav-links {
    display: none;
  }
}
`;

// ==========================================
// 1. REBUILD audio.html
// ==========================================
const audioHtml = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>双语音频剧场 | 台积电张忠谋 · 传记时间线的平行世界</title>
  <meta name="description" content="台积电张忠谋传记时间线的平行世界 · 沉浸式双语音频剧场。提供逐句时间戳高亮对齐、中英双语切换、点击定点跳转与智能语音流播放。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@400;600;700;900&display=swap" rel="stylesheet">
  <script src="audio_data.js"></script>
  <style>
    :root {
      --bg-dark: #070b12;
      --bg-surface: #0e1524;
      --bg-panel: rgba(14, 21, 36, 0.85);
      --bg-active: rgba(0, 240, 255, 0.12);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-cyan: rgba(0, 240, 255, 0.3);
      --border-gold: rgba(245, 158, 11, 0.35);
      --cyan-tsmc: #00f0ff;
      --cyan-glow: rgba(0, 240, 255, 0.35);
      --gold-silicon: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.25);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --font-serif: "Noto Serif SC", "Songti SC", Georgia, serif;
      --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-display: "Cinzel", "Noto Serif SC", serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { height: 100%; }
    body {
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-sans);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      padding-top: 58px;
      margin: 0;
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(0, 240, 255, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(245, 158, 11, 0.04) 0%, transparent 40%),
        linear-gradient(to right, rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
    }

    ${unifiedNavCss}

    /* Main Theater Layout */
    .theater-container {
      display: flex;
      flex: 1;
      overflow: hidden;
      position: relative;
      height: calc(100vh - 58px - 96px);
    }

    /* Left Sidebar: Episode List */
    .episode-sidebar {
      width: 340px;
      flex-shrink: 0;
      background: var(--bg-panel);
      backdrop-filter: blur(20px);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 30;
    }
    .sidebar-header {
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(14, 21, 36, 0.95);
    }
    .sidebar-header h2 {
      font-size: 13px;
      font-weight: 700;
      color: var(--cyan-tsmc);
      letter-spacing: 1px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .episode-count-tag {
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 12px;
      background: rgba(0, 240, 255, 0.1);
      color: var(--cyan-tsmc);
      border: 1px solid rgba(0, 240, 255, 0.2);
    }
    .episode-list {
      flex: 1;
      overflow-y: auto;
      padding: 10px 8px;
      list-style: none;
    }
    .episode-list::-webkit-scrollbar { width: 5px; }
    .episode-list::-webkit-scrollbar-track { background: transparent; }
    .episode-list::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 3px; }

    .ep-item {
      padding: 10px 12px;
      border-radius: 8px;
      margin-bottom: 5px;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s ease;
      position: relative;
    }
    .ep-item:hover {
      background: rgba(255, 255, 255, 0.04);
      border-color: rgba(255, 255, 255, 0.08);
    }
    .ep-item.active {
      background: var(--bg-active);
      border-color: var(--border-cyan);
      box-shadow: 0 4px 16px -4px var(--cyan-glow);
    }
    .ep-badge-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 3px;
    }
    .ep-id {
      font-size: 11px;
      font-family: var(--font-display);
      font-weight: 700;
      color: var(--cyan-tsmc);
    }
    .ep-duration {
      font-size: 10px;
      color: var(--text-dim);
    }
    .ep-title-zh {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 2px;
      line-height: 1.35;
    }
    .ep-title-en {
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.25;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    /* Main Theater Area */
    .stage-main {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
      background: radial-gradient(circle at 50% 10%, rgba(0, 240, 255, 0.03) 0%, transparent 60%);
    }

    /* Episode Banner Bar */
    .stage-header {
      padding: 12px 24px;
      background: rgba(14, 21, 36, 0.7);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
      gap: 12px;
    }
    .current-meta {
      min-width: 0;
      flex: 1;
    }
    .current-meta h3 {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 10px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .current-meta p {
      font-size: 12px;
      color: var(--cyan-tsmc);
      margin-top: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .view-toggles {
      display: flex;
      align-items: center;
      gap: 4px;
      background: rgba(0, 0, 0, 0.4);
      padding: 3px;
      border-radius: 8px;
      border: 1px solid var(--border-subtle);
    }
    .mode-btn {
      padding: 4px 10px;
      border-radius: 6px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .mode-btn:hover { color: var(--text-main); }
    .mode-btn.active {
      background: linear-gradient(135deg, rgba(0, 240, 255, 0.2), rgba(0, 240, 255, 0.05));
      color: var(--cyan-tsmc);
      border: 1px solid var(--border-cyan);
    }

    .menu-toggle-btn {
      display: none;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      color: var(--cyan-tsmc);
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
    }

    /* Subtitles Container / Teleprompter */
    .subtitles-viewport {
      flex: 1;
      overflow-y: auto;
      padding: 30px 12% 80px;
      scroll-behavior: smooth;
    }
    .subtitles-viewport::-webkit-scrollbar { width: 6px; }
    .subtitles-viewport::-webkit-scrollbar-track { background: transparent; }
    .subtitles-viewport::-webkit-scrollbar-thumb { background: rgba(0, 240, 255, 0.15); border-radius: 4px; }

    .cue-group {
      margin-bottom: 20px;
      padding: 14px 18px;
      border-radius: 10px;
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }
    .cue-group:hover {
      background: rgba(255, 255, 255, 0.02);
      border-color: rgba(255, 255, 255, 0.06);
    }
    .cue-group.active {
      background: rgba(0, 240, 255, 0.08);
      border-color: var(--border-cyan);
      box-shadow: 0 6px 20px -4px var(--cyan-glow);
      transform: scale(1.012);
    }

    .cue-tag {
      font-size: 11px;
      font-family: var(--font-display);
      color: var(--gold-silicon);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 6px;
      opacity: 0.9;
    }
    .cue-en {
      font-size: 15px;
      font-weight: 500;
      color: #e2e8f0;
      line-height: 1.6;
      margin-bottom: 6px;
      transition: color 0.2s;
    }
    .cue-group.active .cue-en {
      color: var(--cyan-tsmc);
      font-weight: 600;
    }
    .cue-zh {
      font-size: 14.5px;
      font-family: var(--font-serif);
      color: #94a3b8;
      line-height: 1.65;
      transition: color 0.2s;
    }
    .cue-group.active .cue-zh {
      color: #ffffff;
    }

    .hide-zh .cue-zh { display: none !important; }
    .hide-en .cue-en { display: none !important; }

    /* Bottom Control Bar */
    .player-dock {
      height: 96px;
      flex-shrink: 0;
      background: rgba(9, 13, 22, 0.96);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-top: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 0 24px;
      z-index: 40;
      position: relative;
    }

    /* Progress Bar */
    .timeline-container {
      display: flex;
      align-items: center;
      gap: 12px;
      width: 100%;
      margin-bottom: 8px;
    }
    .time-lbl {
      font-size: 11px;
      font-family: var(--font-display);
      color: var(--text-muted);
      min-width: 44px;
    }
    .progress-track {
      flex: 1;
      height: 6px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 3px;
      position: relative;
      cursor: pointer;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--cyan-tsmc), var(--gold-silicon));
      border-radius: 3px;
      width: 0%;
      position: relative;
    }
    .progress-fill::after {
      content: "";
      position: absolute;
      right: -5px;
      top: -3px;
      width: 12px;
      height: 12px;
      background: #ffffff;
      box-shadow: 0 0 8px var(--cyan-tsmc);
      border-radius: 50%;
    }

    /* Action Controls Row */
    .controls-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .track-toggle-grp {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .track-btn {
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 600;
      border-radius: 12px;
      border: 1px solid var(--border-subtle);
      background: rgba(255, 255, 255, 0.03);
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .track-btn.active {
      background: rgba(0, 240, 255, 0.15);
      border-color: var(--cyan-tsmc);
      color: var(--cyan-tsmc);
    }

    .main-btns {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .ctrl-btn {
      background: transparent;
      border: none;
      color: var(--text-main);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
    }
    .ctrl-btn:hover {
      color: var(--cyan-tsmc);
      transform: scale(1.1);
    }
    .btn-play-hero {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--cyan-tsmc), #00a8ff);
      color: #070b12;
      box-shadow: 0 0 16px var(--cyan-glow);
    }
    .btn-play-hero:hover {
      background: linear-gradient(135deg, #38f9d7, var(--cyan-tsmc));
      box-shadow: 0 0 24px var(--cyan-glow);
      color: #000;
      transform: scale(1.06);
    }

    .playback-opts {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .speed-select {
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      font-size: 11px;
      padding: 4px 8px;
      border-radius: 6px;
      outline: none;
      cursor: pointer;
    }
    .vol-slider {
      width: 75px;
      accent-color: var(--cyan-tsmc);
      cursor: pointer;
    }

    @media (max-width: 900px) {
      .episode-sidebar {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        transform: translateX(-100%);
      }
      .episode-sidebar.open {
        transform: translateX(0);
      }
      .menu-toggle-btn { display: block; }
      .subtitles-viewport { padding: 20px 16px 80px; }
      .unified-nav-links { display: none; }
    }
  </style>
</head>
<body>

  ${getUnifiedNavHtml('audio')}

  <!-- Theater Workspace -->
  <div class="theater-container">
    
    <!-- Sidebar: Episode List -->
    <aside class="episode-sidebar" id="sidebar">
      <div class="sidebar-header">
        <h2><span>⚡</span> 剧集与乐章目录</h2>
        <span class="episode-count-tag" id="epTotalCount">19 集全收官</span>
      </div>
      <ul class="episode-list" id="episodeList">
        <!-- Injected via JS -->
      </ul>
    </aside>

    <!-- Center Stage: Subtitles Viewport -->
    <main class="stage-main">
      <div class="stage-header">
        <div class="current-meta">
          <h3 id="currentEpTitle">第00期 全册导读</h3>
          <p id="currentEpEnTitle">Episode 00: A Guide to the Whole Volume</p>
        </div>

        <div class="header-actions">
          <div class="view-toggles">
            <button class="mode-btn active" data-mode="both">🌐 双语</button>
            <button class="mode-btn" data-mode="zh">🇨🇳 中文</button>
            <button class="mode-btn" data-mode="en">🇺🇸 英文</button>
          </div>
          <button class="menu-toggle-btn" id="btnToggleSidebar">☰ 剧集目录</button>
        </div>
      </div>

      <div class="subtitles-viewport" id="subtitlesContainer">
        <!-- Subtitles Injected via JS -->
      </div>
    </main>
  </div>

  <!-- Bottom Player Dock -->
  <footer class="player-dock">
    <div class="timeline-container">
      <span class="time-lbl" id="curTimeText">00:00</span>
      <div class="progress-track" id="progressTrack">
        <div class="progress-fill" id="progressFill"></div>
      </div>
      <span class="time-lbl" id="totalTimeText">00:00</span>
    </div>

    <div class="controls-row">
      <!-- Audio Track Language Toggle -->
      <div class="track-toggle-grp">
        <span style="font-size: 11px; color: var(--text-dim); margin-right: 4px;">声道:</span>
        <button class="track-btn active" id="btnTrackZh">🇨🇳 中文原声</button>
        <button class="track-btn" id="btnTrackEn">🇺🇸 English Track</button>
      </div>

      <!-- Main Play / Pause Controls -->
      <div class="main-btns">
        <button class="ctrl-btn" id="btnPrev" title="上一集">
          <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6 8.5 6V6z"/></svg>
        </button>
        <button class="ctrl-btn btn-play-hero" id="btnPlay" title="播放 / 暂停">
          <svg width="22" height="22" fill="currentColor" id="playIcon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
        </button>
        <button class="ctrl-btn" id="btnNext" title="下一集">
          <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="m6 18 8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg>
        </button>
      </div>

      <!-- Playback Speed & Volume -->
      <div class="playback-opts">
        <select class="speed-select" id="speedSelect">
          <option value="0.8">0.8x</option>
          <option value="1.0" selected>1.0x</option>
          <option value="1.25">1.25x</option>
          <option value="1.5">1.5x</option>
          <option value="2.0">2.0x</option>
        </select>
        <input type="range" class="vol-slider" id="volSlider" min="0" max="1" step="0.05" value="1" title="音量调节">
      </div>
    </div>
  </footer>

  <audio id="audioEl" preload="auto"></audio>

  <script>
    // Embedded Fallback Episode Manifest (19 full episodes self-contained)
    const EMBEDDED_MANIFEST = ${JSON.stringify(allEpisodes)};

    // State management
    const state = {
      episodes: (window.AUDIO_DATA && window.AUDIO_DATA.length > 0) ? window.AUDIO_DATA : ((window.EPISODES_DATA && window.EPISODES_DATA.length > 0) ? window.EPISODES_DATA : EMBEDDED_MANIFEST),
      currentEpIndex: 0,
      lang: 'zh',
      mode: 'both',
      isPlaying: false,
      currentTime: 0,
      duration: 0
    };

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

    function formatTime(secs) {
      if (isNaN(secs) || secs < 0) return '00:00';
      const m = Math.floor(secs / 60);
      const s = Math.floor(secs % 60);
      return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
    }

    // Initialize episode list
    function renderEpisodeList() {
      if (!episodeListEl) return;
      episodeListEl.innerHTML = '';
      state.episodes.forEach((ep, idx) => {
        const li = document.createElement('li');
        li.className = 'ep-item ' + (idx === state.currentEpIndex ? 'active' : '');
        li.onclick = () => {
          loadEpisode(idx, true);
          if (window.innerWidth <= 900 && sidebar) {
            sidebar.classList.remove('open');
          }
        };
        li.innerHTML = '<div class="ep-badge-row">' +
            '<span class="ep-id">EP.' + ep.id + '</span>' +
            '<span class="ep-duration">' + formatTime(ep.durationZh || 360) + '</span>' +
          '</div>' +
          '<div class="ep-title-zh">' + ep.title + '</div>' +
          '<div class="ep-title-en">' + (ep.enTitle || '') + '</div>';
        episodeListEl.appendChild(li);
      });
    }

    // Load episode
    function loadEpisode(index, autoPlay = false) {
      state.currentEpIndex = index;
      const ep = state.episodes[index];
      if (!ep) return;

      if (currentEpTitle) currentEpTitle.textContent = ep.title;
      if (currentEpEnTitle) currentEpEnTitle.textContent = ep.enTitle || '';

      document.querySelectorAll('.ep-item').forEach((item, idx) => {
        item.classList.toggle('active', idx === index);
      });

      renderSubtitles(ep);

      const audioSrc = state.lang === 'zh' ? (ep.audioZh || '') : (ep.audioEn || '');
      audioEl.src = audioSrc;
      audioEl.load();

      state.duration = (state.lang === 'zh' ? ep.durationZh : ep.durationEn) || 300;
      totalTimeText.textContent = formatTime(state.duration);

      audioEl.onloadedmetadata = () => {
        if (audioEl.duration && !isNaN(audioEl.duration)) {
          state.duration = audioEl.duration;
          totalTimeText.textContent = formatTime(state.duration);
        }
        if (autoPlay) playAudio();
      };

      state.currentTime = 0;
      updateTimelineUI(0);
      if (autoPlay) playAudio();
    }

    // Render Subtitles
    function renderSubtitles(ep) {
      if (!subtitlesContainer) return;
      subtitlesContainer.innerHTML = '';
      if (!ep.cues || ep.cues.length === 0) {
        subtitlesContainer.innerHTML = '<div style="text-align:center; padding: 40px; color: var(--text-dim);">本乐章暂无逐句字幕</div>';
        return;
      }

      ep.cues.forEach((cue, cIdx) => {
        const div = document.createElement('div');
        div.className = 'cue-group';
        div.id = 'cue-' + cIdx;
        div.dataset.start = cue.start;
        div.dataset.end = cue.end;

        div.onclick = () => {
          seekTo(cue.start);
          if (!state.isPlaying) playAudio();
        };

        const secTag = cue.secZh ? '<div class="cue-tag">⚡ ' + cue.secZh + ' <span style="opacity:0.6; font-size:10px;">' + formatTime(cue.start) + '</span></div>' : '';
        const enHtml = cue.en ? '<div class="cue-en">' + cue.en + '</div>' : '';
        const zhHtml = cue.zh ? '<div class="cue-zh">' + cue.zh + '</div>' : '';

        div.innerHTML = secTag + enHtml + zhHtml;
        subtitlesContainer.appendChild(div);
      });
    }

    // Subtitle sync
    let currentActiveCue = -1;
    function syncSubtitles(time) {
      const ep = state.episodes[state.currentEpIndex];
      if (!ep || !ep.cues) return;

      let activeIdx = -1;
      for (let i = 0; i < ep.cues.length; i++) {
        if (time >= ep.cues[i].start && time <= ep.cues[i].end) {
          activeIdx = i;
          break;
        }
      }

      if (activeIdx !== currentActiveCue) {
        currentActiveCue = activeIdx;
        document.querySelectorAll('.cue-group').forEach((el, idx) => {
          if (idx === activeIdx) {
            el.classList.add('active');
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          } else {
            el.classList.remove('active');
          }
        });
      }
    }

    function updateTimelineUI(time) {
      curTimeText.textContent = formatTime(time);
      const ratio = state.duration > 0 ? (time / state.duration) : 0;
      progressFill.style.width = Math.min(100, Math.max(0, ratio * 100)) + '%';
    }

    // Playback functions
    let timerFallback = null;

    function playAudio() {
      state.isPlaying = true;
      playIcon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
      
      const playPromise = audioEl.play();
      if (playPromise !== undefined) {
        playPromise.catch(() => {
          startFallbackTimer();
        });
      }
    }

    function pauseAudio() {
      state.isPlaying = false;
      playIcon.innerHTML = '<path d="M8 5v14l11-7z"/>';
      audioEl.pause();
      if (timerFallback) clearInterval(timerFallback);
    }

    function togglePlay() {
      if (state.isPlaying) pauseAudio();
      else playAudio();
    }

    function seekTo(seconds) {
      state.currentTime = seconds;
      audioEl.currentTime = seconds;
      updateTimelineUI(seconds);
      syncSubtitles(seconds);
    }

    function startFallbackTimer() {
      if (timerFallback) clearInterval(timerFallback);
      timerFallback = setInterval(() => {
        if (!state.isPlaying) return;
        state.currentTime += 0.25 * audioEl.playbackRate;
        if (state.currentTime >= state.duration) {
          pauseAudio();
          if (state.currentEpIndex < state.episodes.length - 1) {
            loadEpisode(state.currentEpIndex + 1, true);
          }
          return;
        }
        updateTimelineUI(state.currentTime);
        syncSubtitles(state.currentTime);
      }, 250);
    }

    // Event Listeners
    audioEl.ontimeupdate = () => {
      state.currentTime = audioEl.currentTime;
      updateTimelineUI(state.currentTime);
      syncSubtitles(state.currentTime);
    };

    audioEl.onended = () => {
      pauseAudio();
      if (state.currentEpIndex < state.episodes.length - 1) {
        loadEpisode(state.currentEpIndex + 1, true);
      }
    };

    btnPlay.onclick = togglePlay;

    btnPrev.onclick = () => {
      if (state.currentEpIndex > 0) {
        loadEpisode(state.currentEpIndex - 1, state.isPlaying);
      }
    };

    btnNext.onclick = () => {
      if (state.currentEpIndex < state.episodes.length - 1) {
        loadEpisode(state.currentEpIndex + 1, state.isPlaying);
      }
    };

    // Track Language Toggle
    btnTrackZh.onclick = () => {
      if (state.lang === 'zh') return;
      state.lang = 'zh';
      btnTrackZh.classList.add('active');
      btnTrackEn.classList.remove('active');
      const savedTime = state.currentTime;
      const wasPlaying = state.isPlaying;
      loadEpisode(state.currentEpIndex, false);
      seekTo(savedTime);
      if (wasPlaying) playAudio();
    };

    btnTrackEn.onclick = () => {
      if (state.lang === 'en') return;
      state.lang = 'en';
      btnTrackEn.classList.add('active');
      btnTrackZh.classList.remove('active');
      const savedTime = state.currentTime;
      const wasPlaying = state.isPlaying;
      loadEpisode(state.currentEpIndex, false);
      seekTo(savedTime);
      if (wasPlaying) playAudio();
    };

    // Subtitle View Mode
    document.querySelectorAll('.mode-btn').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const mode = btn.dataset.mode;
        state.mode = mode;
        subtitlesContainer.className = 'subtitles-viewport';
        if (mode === 'zh') subtitlesContainer.classList.add('hide-en');
        if (mode === 'en') subtitlesContainer.classList.add('hide-zh');
      };
    });

    // Speed & Volume
    speedSelect.onchange = (e) => {
      audioEl.playbackRate = parseFloat(e.target.value);
    };

    volSlider.oninput = (e) => {
      audioEl.volume = parseFloat(e.target.value);
    };

    // Seek via Progress Track
    progressTrack.onclick = (e) => {
      const rect = progressTrack.getBoundingClientRect();
      const clickRatio = (e.clientX - rect.left) / rect.width;
      const targetSec = clickRatio * state.duration;
      seekTo(targetSec);
    };

    // Mobile sidebar toggle
    if (btnToggleSidebar && sidebar) {
      btnToggleSidebar.onclick = () => {
        sidebar.classList.toggle('open');
      };
    }

    // URL Query Parameter ?ep=01
    const urlParams = new URLSearchParams(window.location.search);
    const targetEp = urlParams.get('ep');
    let initIdx = 0;
    if (targetEp) {
      const foundIdx = state.episodes.findIndex(e => e.id === targetEp || e.id === String(targetEp).padStart(2, '0'));
      if (foundIdx !== -1) initIdx = foundIdx;
    }

    // Boot instantly
    renderEpisodeList();
    loadEpisode(initIdx, false);
  </script>
</body>
</html>`;

fs.writeFileSync(path.join(baseDir, 'audio.html'), audioHtml, 'utf8');
console.log('Successfully written audio.html with embedded dataset!');

// ==========================================
// 2. REBUILD map.html and 平行世界地图.html
// ==========================================
const mapHtml = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>平行世界地图 · 台积电张忠谋传记时间线 (11城轨迹+18决策节点)</title>
  <meta name="description" content="台积电张忠谋1931-2026全球11城人生轨迹图与18个重大历史平行决策节点。双重视角：他这一年 vs 世界这一年。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800;900&family=Noto+Serif+SC:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #080c14;
      --bg-card: #0f172a;
      --bg-card-hover: #17233d;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(0, 240, 255, 0.3);
      --cyan-tsmc: #00f0ff;
      --cyan-glow: rgba(0, 240, 255, 0.25);
      --gold-silicon: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.25);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --he-color: #38bdf8;
      --world-color: #fb7185;
      --font-serif: "Noto Serif SC", "Songti SC", Georgia, serif;
      --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-display: "Cinzel", serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.7;
      padding-top: 58px;
      margin: 0;
      background-image: 
        radial-gradient(circle at 20% 15%, rgba(0, 240, 255, 0.04) 0%, transparent 50%),
        radial-gradient(circle at 80% 85%, rgba(245, 158, 11, 0.04) 0%, transparent 50%),
        linear-gradient(to right, rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 48px 48px, 48px 48px;
    }

    ${unifiedNavCss}

    .page-container {
      max-width: 1140px;
      margin: 0 auto;
      padding: 40px 24px 100px;
    }

    .hero-header {
      text-align: center;
      padding: 30px 0 40px;
    }
    .hero-header h1 {
      font-family: var(--font-serif);
      font-size: 34px;
      font-weight: 900;
      letter-spacing: 2px;
      background: linear-gradient(135deg, #ffffff 0%, var(--cyan-tsmc) 60%, var(--gold-silicon) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 12px;
    }
    .hero-header .subtitle {
      font-size: 16px;
      color: var(--text-muted);
      font-family: var(--font-serif);
      letter-spacing: 1px;
    }
    .hero-header .en-sub {
      font-size: 13px;
      color: var(--text-dim);
      font-family: var(--font-display);
      margin-top: 4px;
      letter-spacing: 1.5px;
    }

    /* Trajectory City Map Section */
    .section-title {
      font-family: var(--font-serif);
      font-size: 22px;
      font-weight: 700;
      color: var(--cyan-tsmc);
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 40px 0 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-subtle);
    }
    .section-title span {
      font-family: var(--font-display);
      font-size: 14px;
      color: var(--gold-silicon);
      font-weight: 600;
    }

    /* 11-City Trajectory Grid */
    .trajectory-timeline {
      position: relative;
      margin: 24px 0 60px;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 16px;
    }
    .city-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 18px 20px;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }
    .city-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: linear-gradient(to bottom, var(--cyan-tsmc), var(--gold-silicon));
      opacity: 0.7;
    }
    .city-card:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-accent);
      transform: translateY(-3px);
      box-shadow: 0 10px 24px -6px var(--cyan-glow);
    }
    .city-card .step-no {
      font-size: 11px;
      font-family: var(--font-display);
      color: var(--gold-silicon);
      font-weight: 700;
      letter-spacing: 1px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .city-card .step-year {
      font-size: 11px;
      color: var(--text-dim);
      background: rgba(255, 255, 255, 0.05);
      padding: 1px 6px;
      border-radius: 4px;
    }
    .city-card .city-name {
      font-size: 17px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 4px;
      display: flex;
      align-items: baseline;
      gap: 8px;
    }
    .city-card .city-name-en {
      font-size: 12px;
      color: var(--cyan-tsmc);
      font-family: var(--font-sans);
      font-weight: 400;
    }
    .city-card .city-desc {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.6;
    }

    /* 18 Decision Nodes */
    .nodes-container {
      display: flex;
      flex-direction: column;
      gap: 20px;
      margin-top: 24px;
    }
    .node-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 24px 28px;
      transition: all 0.25s ease;
      position: relative;
    }
    .node-card:hover {
      border-color: rgba(0, 240, 255, 0.35);
      background: var(--bg-card-hover);
      box-shadow: 0 8px 28px -6px rgba(0, 0, 0, 0.5);
    }
    .node-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      padding-bottom: 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      margin-bottom: 18px;
    }
    .node-badge {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .node-ep {
      font-size: 12px;
      font-weight: 700;
      color: var(--cyan-tsmc);
      font-family: var(--font-display);
      padding: 3px 8px;
      background: rgba(0, 240, 255, 0.1);
      border: 1px solid rgba(0, 240, 255, 0.2);
      border-radius: 6px;
    }
    .node-title {
      font-family: var(--font-serif);
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
    }
    .node-time {
      font-size: 13px;
      font-family: var(--font-display);
      color: var(--gold-silicon);
      font-weight: 600;
      background: rgba(245, 158, 11, 0.1);
      padding: 3px 10px;
      border-radius: 20px;
      border: 1px solid rgba(245, 158, 11, 0.2);
    }

    .node-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }
    .node-col {
      padding: 14px 16px;
      border-radius: 8px;
      background: rgba(0, 0, 0, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.03);
    }
    .node-col.he {
      border-left: 3px solid var(--he-color);
    }
    .node-col.world {
      border-left: 3px solid var(--world-color);
    }
    .node-col-tag {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .node-col.he .node-col-tag { color: var(--he-color); }
    .node-col.world .node-col-tag { color: var(--world-color); }

    .node-col-text {
      font-size: 14px;
      color: #cbd5e1;
      line-height: 1.6;
      margin-bottom: 6px;
    }
    .node-col-en {
      font-size: 12px;
      color: var(--text-dim);
      line-height: 1.45;
      font-family: var(--font-serif);
      font-style: italic;
    }

    .node-motto {
      margin-top: 16px;
      padding: 12px 18px;
      background: rgba(245, 158, 11, 0.08);
      border-left: 3px solid var(--gold-silicon);
      border-radius: 0 8px 8px 0;
      color: #fde68a;
      font-size: 13.5px;
      font-family: var(--font-serif);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }
    .node-motto .quote-text {
      flex: 1;
    }
    .node-motto .node-link {
      font-size: 12px;
      font-family: var(--font-sans);
      color: var(--cyan-tsmc);
      text-decoration: none;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(0, 240, 255, 0.1);
      border: 1px solid rgba(0, 240, 255, 0.2);
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .node-motto .node-link:hover {
      background: rgba(0, 240, 255, 0.2);
      color: #ffffff;
      transform: translateY(-1px);
    }

    @media (max-width: 768px) {
      .node-grid { grid-template-columns: 1fr; }
      .hero-header h1 { font-size: 26px; }
      .trajectory-timeline { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  ${getUnifiedNavHtml('map')}

  <div class="page-container">
    
    <header class="hero-header">
      <h1>平行世界地图</h1>
      <div class="subtitle">台积电张忠谋 · 传记时间线的平行世界 · 全册 1931–至今</div>
      <div class="en-sub">The Parallel Worlds Map · Morris Chang &amp; TSMC · 11 Cities &amp; 18 Decision Nodes</div>
    </header>

    <!-- 11 Cities Life Trajectory Map -->
    <h2 class="section-title">
      🌍 全球 11 城人生轨迹图
      <span>Global 11-City Trajectory (1931–Present)</span>
    </h2>

    <div class="trajectory-timeline">
      <div class="city-card">
        <div class="step-no"><span>01 / 出生地</span><span class="step-year">1931</span></div>
        <div class="city-name">宁波 <span class="city-name-en">Ningbo</span></div>
        <div class="city-desc">出生于浙江宁波。战火逼近前度过短暂宁静的幼年启蒙时光。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>02 / 避难</span><span class="step-year">1937–38</span></div>
        <div class="city-name">广州 <span class="city-name-en">Guangzhou</span></div>
        <div class="city-desc">随父母南迁避难，经历广州大轰炸，在防空警报中学会收拾行囊。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>03 / 启蒙与转口</span><span class="step-year">1938–41, 48–49</span></div>
        <div class="city-name">香港 <span class="city-name-en">Hong Kong</span></div>
        <div class="city-desc">培正小学求学，见证香港沦陷。1949年在此搭乘泛美航空赴美求学。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>04 / 陪都求学</span><span class="step-year">1942–45</span></div>
        <div class="city-name">重庆 <span class="city-name-en">Chongqing</span></div>
        <div class="city-desc">战时陪都重庆南开中学。在沙坪坝受张伯苓校风熏陶，沉迷文史与文学。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>05 / 作家梦破</span><span class="step-year">1945–48</span></div>
        <div class="city-name">上海 <span class="city-name-en">Shanghai</span></div>
        <div class="city-desc">南洋模范中学。金圆券恶性通胀爆发，在父亲劝告下放弃作家梦转向理工。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>06 / 哈佛与麻省理工</span><span class="step-year">1949–55</span></div>
        <div class="city-name">剑桥 / 波士顿 <span class="city-name-en">Boston / MIT</span></div>
        <div class="city-desc">1949年入哈佛大学，1950年转入MIT获机械系学士与硕士。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>07 / 半导体入行</span><span class="step-year">1955–58</span></div>
        <div class="city-name">波士顿 <span class="city-name-en">Sylvania</span></div>
        <div class="city-desc">因1美元月薪之差弃福特汽车，加入希尔瓦尼亚半导体，踏入半导体产业。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>08 / 德仪光辉岁月</span><span class="step-year">1958–83</span></div>
        <div class="city-name">达拉斯 <span class="city-name-en">Dallas / TI</span></div>
        <div class="city-desc">德州仪器25载，从工程经理攀升至资深副总裁兼半导体集团总经理。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>09 / 博士深造</span><span class="step-year">1961–64</span></div>
        <div class="city-name">硅谷 / 斯坦福 <span class="city-name-en">Stanford</span></div>
        <div class="city-desc">德仪全薪资助攻读斯坦福大学电机工程博士，系统建立半导体理论体系。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>10 / 纽约驻足</span><span class="step-year">1984–85</span></div>
        <div class="city-name">纽约 <span class="city-name-en">New York / GI</span></div>
        <div class="city-desc">出任通用仪器 (General Instrument) 总裁兼COO，旋即迎来台湾李国鼎的诚挚邀请。</div>
      </div>

      <div class="city-card">
        <div class="step-no"><span>11 / 创立台积电</span><span class="step-year">1985–至今</span></div>
        <div class="city-name">新竹 <span class="city-name-en">Hsinchu / TSMC</span></div>
        <div class="city-desc">出任工研院院长，1987年创立台积电开创纯代工模式，铸造全球护国神山。</div>
      </div>
    </div>

    <!-- 18 Parallel Decision Nodes -->
    <h2 class="section-title">
      ⚡ 18 个历史平行决策节点
      <span>18 Parallel Worlds Decision Nodes</span>
    </h2>

    <div class="nodes-container">
      
      <!-- Node 01 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.01</span>
            <h3 class="node-title">逃难的孩子</h3>
          </div>
          <span class="node-time">1937–1942</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">随父母从广州辗转逃难至香港，在频繁的防空警报声里度过童年。</div>
            <div class="node-col-en">Moved from Guangzhou to Hong Kong with his parents, spending his childhood to air-raid sirens.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">广州大轰炸、香港沦陷，东亚全面卷入二战烽火。</div>
            <div class="node-col-en">The bombing of Guangzhou and fall of Hong Kong dragged East Asia into all-out war.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 一个孩子学会的第一件事，是随时收拾行李。<span style="opacity:0.7; font-size:12px; margin-left:8px;">The first thing a child learned was to pack.</span></div>
          <a href="audio.html?ep=01" class="node-link">🎙️ 聆听剧场 EP.01</a>
        </div>
      </div>

      <!-- Node 02 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.02</span>
            <h3 class="node-title">考不进去的南开与作家梦</h3>
          </div>
          <span class="node-time">1943–1948</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">重庆南开受教，上海南洋模范毕业。作家梦被父亲一句「写作会挨饿」按捺。</div>
            <div class="node-col-en">At Chongqing Nankai and Shanghai Nanyang Model, his writing dream was shelved: "Writing will leave you hungry."</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">抗战胜利与国共内战爆发，1948金圆券恶性通胀摧毁中产财富。</div>
            <div class="node-col-en">Victory in WWII followed by civil war; the 1948 hyperinflation wiped out middle-class wealth.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 时代用通胀，替他改写了职业志愿。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Inflation rewrote his career plans for him.</span></div>
          <a href="audio.html?ep=02" class="node-link">🎙️ 聆听剧场 EP.02</a>
        </div>
      </div>

      <!-- Node 03 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.03</span>
            <h3 class="node-title">从黄浦江到查尔斯河</h3>
          </div>
          <span class="node-time">1949–1950</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">1949年告别中国赴美入读哈佛，1950年因谋生考量转入MIT攻读机械系。</div>
            <div class="node-col-en">Left for Harvard in 1949; transferred to MIT in 1950 for practical engineering skills.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">新中国成立、冷战铁幕垂下，太平洋航线阻断。</div>
            <div class="node-col-en">New China founded, Iron Curtain lowered, Pacific links severed.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 他以为的「暂时离开」，变成了人生的「不归路」。<span style="opacity:0.7; font-size:12px; margin-left:8px;">The temporary departure became a point of no return.</span></div>
          <a href="audio.html?ep=03" class="node-link">🎙️ 聆听剧场 EP.03</a>
        </div>
      </div>

      <!-- Node 04 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.04</span>
            <h3 class="node-title">四十封求职信</h3>
          </div>
          <span class="node-time">1954–1958</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">两次MIT博士资格考落第。投出40封求职信，因福特拒绝多给1美元月薪而选择希尔瓦尼亚半导体。</div>
            <div class="node-col-en">Failed MIT PhD exams twice; chose Sylvania over Ford for a $1/month difference.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">贝尔实验室发明晶体管，苏联斯普特尼克人造卫星发射震撼美国。</div>
            <div class="node-col-en">Transistor invented; Sputnik launch jolted America into tech race.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 被拒绝，是命运在指引另一条路。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Rejection is fate pointing out another path.</span></div>
          <a href="audio.html?ep=04" class="node-link">🎙️ 聆听剧场 EP.04</a>
        </div>
      </div>

      <!-- Node 05 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.05</span>
            <h3 class="node-title">隔岸观火的叛乱</h3>
          </div>
          <span class="node-time">1957–1958</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">希尔瓦尼亚日渐平庸，张忠谋果断跳槽德州仪器，搬往达拉斯。</div>
            <div class="node-col-en">Sylvania stagnated; Morris decisively joined Texas Instruments in Dallas.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">肖克利实验室「八叛徒」出走创立仙童半导体，硅谷传奇大幕拉开。</div>
            <div class="node-col-en">The Traitorous Eight left Shockley to found Fairchild, starting Silicon Valley.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 他没有加入硅谷叛乱，而是走进了德州军团。<span style="opacity:0.7; font-size:12px; margin-left:8px;">He did not join the valley rebels; he entered the Texas legions.</span></div>
          <a href="audio.html?ep=05" class="node-link">🎙️ 聆听剧场 EP.05</a>
        </div>
      </div>

      <!-- Node 06 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.06</span>
            <h3 class="node-title">德仪的太空竞赛岁月</h3>
          </div>
          <span class="node-time">1958–1964</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">在TI展现卓越良率控制才能，获公司全薪资助前往斯坦福攻读电机工程博士。</div>
            <div class="node-col-en">Demonstrated yield mastery at TI; sponsored with full salary for Stanford PhD.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">基尔比发明集成电路，阿波罗登月计划与民兵导弹全面采购芯片。</div>
            <div class="node-col-en">Kilby invented the IC; Apollo program and Minuteman missiles adopted chips.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 技术的突破需要灵感，产业的统治需要良率。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Breakthroughs need inspiration; industry rule needs yield.</span></div>
          <a href="audio.html?ep=06" class="node-link">🎙️ 聆听剧场 EP.06</a>
        </div>
      </div>

      <!-- Node 07 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.07</span>
            <h3 class="node-title">半导体之巅的十年</h3>
          </div>
          <span class="node-time">1964–1974</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">执掌TI半导体事业部，开创激进的「学习曲线降价定价法」，横扫全球半导体市场。</div>
            <div class="node-col-en">Headed TI semiconductor group, executing the learning-curve aggressive pricing to dominate globally.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">摩尔定律提出，微处理器诞生，个人计算时代萌芽。</div>
            <div class="node-col-en">Moore's Law formulated, microprocessors born, personal computing dawned.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 用规模压低成本，用成本击穿竞争对手防线。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Crush costs with scale, and pierce rivals with cost advantage.</span></div>
          <a href="audio.html?ep=07" class="node-link">🎙️ 聆听剧场 EP.07</a>
        </div>
      </div>

      <!-- Node 08 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.08</span>
            <h3 class="node-title">离开德州与受邀回台</h3>
          </div>
          <span class="node-time">1975–1985</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">因TI押注消费电子分歧离职，短暂任职通用仪器总裁。1985年接受李国鼎邀请出任工研院院长。</div>
            <div class="node-col-en">Left TI over consumer strategy clash, headed GI, then accepted K.T. Li's call to lead ITRI in Taiwan.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">日本半导体以DRAM崛起席卷全球，美日半导体贸易摩擦白热化。</div>
            <div class="node-col-en">Japan DRAM dominated global markets; US-Japan chip trade war peaked.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 五十四岁，大多数人规划退休，他选择跨海创业。<span style="opacity:0.7; font-size:12px; margin-left:8px;">At 54, when others planned retirement, he crossed the sea to start fresh.</span></div>
          <a href="audio.html?ep=08" class="node-link">🎙️ 聆听剧场 EP.08</a>
        </div>
      </div>

      <!-- Node 09 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.09</span>
            <h3 class="node-title">纯代工的革命</h3>
          </div>
          <span class="node-time">1985–1987</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">创立台积电（TSMC），确立「只做制造、绝不与客户竞争」的纯晶圆代工模式（Pure-play Foundry）。</div>
            <div class="node-col-en">Founded TSMC, creating the pure-play foundry model: never compete with customers.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">IDM垂直整合巨头垄断全球芯片产业，外界对纯代工普遍持怀疑态度。</div>
            <div class="node-col-en">IDM giants dominated the global industry; pure foundry was viewed with skepticism.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 商业模式的创新，往往比技术发明更能重塑整个世界。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Business model innovation reshapes the world deeper than pure tech.</span></div>
          <a href="audio.html?ep=09" class="node-link">🎙️ 聆听剧场 EP.09</a>
        </div>
      </div>

      <!-- Node 10 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.10</span>
            <h3 class="node-title">从台湾到世界</h3>
          </div>
          <span class="node-time">1987–1990</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">邀请格鲁夫访台，台积电通过英特尔苛刻的200多道质检认证，打开全球市场大门。</div>
            <div class="node-col-en">Invited Andy Grove; passed Intel's 200+ rigorous inspection criteria, winning global credibility.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">个人电脑时代全面爆发，英特尔与微软Wintel联盟确立全球统治。</div>
            <div class="node-col-en">PC boom accelerated; Intel and Microsoft Wintel alliance took command.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 英特尔的认证，是台积电走向世界的第一张通行证。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Intel's certification was TSMC's passport to the world.</span></div>
          <a href="audio.html?ep=10" class="node-link">🎙️ 聆听剧场 EP.10</a>
        </div>
      </div>

      <!-- Node 11 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.11</span>
            <h3 class="node-title">记忆体的诱惑</h3>
          </div>
          <span class="node-time">1990–1995</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">顶住DRAM暴利诱惑，果断剥离德碁存储业务，全面聚焦逻辑芯片代工。</div>
            <div class="node-col-en">Resisted lucrative DRAM hype; severed TI-Acer memory business to stay pure in logic foundry.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">DRAM行业剧烈过山车式暴跌，众多巨头在惨烈周期中元气大伤。</div>
            <div class="node-col-en">DRAM market entered a brutal cyclical crash, crushing overextended players.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 战略不是决定做什么，而是坚决决定不做什么。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Strategy is defined not by what to do, but what not to do.</span></div>
          <a href="audio.html?ep=11" class="node-link">🎙️ 聆听剧场 EP.11</a>
        </div>
      </div>

      <!-- Node 12 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.12</span>
            <h3 class="node-title">逆周期的定力</h3>
          </div>
          <span class="node-time">1995–2000</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">亚洲金融危机期间逆势投资百亿建厂，2000年闪电并购世大积体电路确立霸权。</div>
            <div class="node-col-en">Counter-cyclically invested billions during Asian crisis; acquired WSMC in 2000 to cement dominance.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">互联网泡沫狂飙至顶峰后破裂，全球芯片业经历大洗牌。</div>
            <div class="node-col-en">Dot-com bubble peaked and burst, reshuffling global semiconductor ecosystem.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 繁荣时积蓄弹药，衰退时果断落子。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Save ammunition during booms; make decisive bets in recessions.</span></div>
          <a href="audio.html?ep=12" class="node-link">🎙️ 聆听剧场 EP.12</a>
        </div>
      </div>

      <!-- Node 13 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.13</span>
            <h3 class="node-title">交棒之痛</h3>
          </div>
          <span class="node-time">2000–2009</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">0.13微米铜制程自主突破战胜IBM。2005年交棒蔡力行，2009年金融危机期间78岁高龄披挂复出。</div>
            <div class="node-col-en">Beat IBM in 0.13-micron copper; handed reins in 2005, returned at age 78 during 2009 crisis.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">全球次贷危机爆发，消费电子全面萎缩，智能手机新革命前夕。</div>
            <div class="node-col-en">Global financial crisis hit, while mobile smartphone revolution prepared to erupt.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 老兵永远不死，当公司需要他时，他会立即上马。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Old soldiers never die; when needed, they mount their steed once more.</span></div>
          <a href="audio.html?ep=13" class="node-link">🎙️ 聆听剧场 EP.13</a>
        </div>
      </div>

      <!-- Node 14 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.14</span>
            <h3 class="node-title">绚烂年代</h3>
          </div>
          <span class="node-time">2009–2010</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">复出后力排众议将资本支出翻倍至48亿美元，组建「夜鹰突击队」攻坚28纳米制程。</div>
            <div class="node-col-en">Doubled capex to $4.8B; created Night Hawk 24/7 team to conquer 28nm node.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">移动互联网爆发，iPhone与Android推动智能手机全球放量。</div>
            <div class="node-col-en">Mobile Internet exploded; iPhone and Android triggered soaring demand.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 敢在别人恐惧时贪婪，需要对行业终局有极其清晰的预判。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Greedy when others are fearful requires absolute clarity on the endgame.</span></div>
          <a href="audio.html?ep=14" class="node-link">🎙️ 聆听剧场 EP.14</a>
        </div>
      </div>

      <!-- Node 15 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.15</span>
            <h3 class="node-title">苹果来敲门</h3>
          </div>
          <span class="node-time">2010–2015</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">亲自飞赴库比蒂诺会晤乔布斯与库克，台积电独家拿下A8/A9及后续所有iPhone芯片订单。</div>
            <div class="node-col-en">Met Jobs and Cook in Cupertino; TSMC locked in exclusive production of Apple A-series silicon.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">苹果成为全球市值最大科技公司，三星因专利战与代工冲突被苹果剔除。</div>
            <div class="node-col-en">Apple became the world's most valuable company; Samsung sidelined by patent wars.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 信任是商业世界最昂贵的资产，也是唯一的护城河。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Trust is the rarest asset in business, and the only true moat.</span></div>
          <a href="audio.html?ep=15" class="node-link">🎙️ 聆听剧场 EP.15</a>
        </div>
      </div>

      <!-- Node 16 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.16</span>
            <h3 class="node-title">摩尔定律的守卫者</h3>
          </div>
          <span class="node-time">2015–2018</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">与林本坚团队力推浸润式微影，全面押注ASML EUV光刻机，制程全面超越英特尔。</div>
            <div class="node-col-en">Pioneered immersion lithography with Burn Lin; adopted ASML EUV to surpass Intel.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">物理极限逼近，摩尔定律放缓，先进制程进入个位数纳米终极战场。</div>
            <div class="node-col-en">Physical limits approached; leading-edge race entered single-digit nanometer endgame.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 只要物理学定律没有禁止，我们就会继续推进微缩。<span style="opacity:0.7; font-size:12px; margin-left:8px;">As long as physics allows, we will keep scaling.</span></div>
          <a href="audio.html?ep=16" class="node-link">🎙️ 聆听剧场 EP.16</a>
        </div>
      </div>

      <!-- Node 17 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.17</span>
            <h3 class="node-title">交棒与退休</h3>
          </div>
          <span class="node-time">2018</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">87岁高龄正式退休，建立刘德音（董事长）与魏哲家（总裁）「双首长制」平稳交接。</div>
            <div class="node-col-en">Retired at 87, establishing the dual-leadership model with Mark Liu and C.C. Wei.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">全球半导体成为大国地缘博弈核心，台积电成为全球算力皇冠上的明珠。</div>
            <div class="node-col-en">Semiconductors became core to geopolitical strategy; TSMC crowned computing king.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 功成身退，是企业家对企业最深沉的托付。<span style="opacity:0.7; font-size:12px; margin-left:8px;">Graceful departure is the deepest entrustment a founder can make.</span></div>
          <a href="audio.html?ep=17" class="node-link">🎙️ 聆听剧场 EP.17</a>
        </div>
      </div>

      <!-- Node 18 -->
      <div class="node-card">
        <div class="node-header">
          <div class="node-badge">
            <span class="node-ep">EP.18</span>
            <h3 class="node-title">护国神山</h3>
          </div>
          <span class="node-time">2018–至今</span>
        </div>
        <div class="node-grid">
          <div class="node-col he">
            <div class="node-col-tag">👤 他这一年 · His Year</div>
            <div class="node-col-text">台积电市值突破万亿美元，全球AI浪潮下与英伟达深度绑定，成为无可替代的全球硅基中枢。</div>
            <div class="node-col-en">TSMC market cap surpassed $1T; powered the global AI revolution with Nvidia as irreplaceable silicon hub.</div>
          </div>
          <div class="node-col world">
            <div class="node-col-tag">🌐 世界这一年 · The World's Year</div>
            <div class="node-col-text">全球化已死，半导体地缘政治必争之地，大国角力下的硅盾神话。</div>
            <div class="node-col-en">Globalization splintered; semiconductors became the ultimate geopolitical asset.</div>
          </div>
        </div>
        <div class="node-motto">
          <div class="quote-text">💬 台积电已经成为地缘政治家的必争之地。<span style="opacity:0.7; font-size:12px; margin-left:8px;">TSMC has become a geopolitical battleground.</span></div>
          <a href="audio.html?ep=18" class="node-link">🎙️ 聆听剧场 EP.18</a>
        </div>
      </div>

    </div>

    <footer style="text-align:center; padding: 60px 0 20px; color: var(--text-dim); font-size: 13px;">
      <p>台积电张忠谋 · 传记时间线的平行世界 · 1931–至今</p>
      <p style="margin-top:4px; font-family: var(--font-display); font-size: 11px;">The Parallel Worlds of Morris Chang &amp; TSMC</p>
    </footer>
  </div>

</body>
</html>`;

fs.writeFileSync(path.join(baseDir, 'map.html'), mapHtml, 'utf8');
fs.writeFileSync(path.join(baseDir, '平行世界地图.html'), mapHtml, 'utf8');
console.log('Successfully written map.html and 平行世界地图.html');

// ==========================================
// 3. LOCK TOP NAVBAR ACROSS ALL HTML PAGES
// ==========================================
const htmlFiles = fs.readdirSync(baseDir).filter(f => f.endsWith('.html'));
console.log(`Found ${htmlFiles.length} HTML files to verify & lock top navbar.`);

htmlFiles.forEach(fileName => {
  const filePath = path.join(baseDir, fileName);
  let content = fs.readFileSync(filePath, 'utf8');

  // Determine active nav
  let activeNav = 'index';
  if (fileName.includes('reader') || fileName.includes('全册电子书')) activeNav = 'reader';
  else if (fileName.includes('audio')) activeNav = 'audio';
  else if (fileName.includes('map') || fileName.includes('平行世界地图')) activeNav = 'map';
  else if (fileName.includes('card') || fileName.includes('金句')) activeNav = 'cards';
  else if (fileName.startsWith('episode-')) activeNav = 'reader';

  // For other HTML files (like index.html, reader.html, cards.html, episode-*.html)
  if (fileName !== 'audio.html' && fileName !== 'map.html' && fileName !== '平行世界地图.html') {
    // Ensure body has padding-top: 58px; margin: 0;
    if (content.includes('body {') || content.includes('body{')) {
      content = content.replace(/body\s*\{([^}]*)\}/, (match, p1) => {
        let updated = p1.replace(/padding-top:[^;]+;?/g, '').replace(/margin:[^;]+;?/g, '');
        return 'body {' + updated + ' padding-top: 58px !important; margin: 0 !important; }';
      });
    }

    // Ensure unified-top-nav CSS has position: fixed !important; top: 0; left: 0; right: 0; z-index: 9999;
    if (content.includes('.unified-top-nav')) {
      content = content.replace(/\.unified-top-nav\s*\{[^}]*\}/, `
.unified-top-nav {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  width: 100% !important;
  height: 58px !important;
  z-index: 9999 !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  background: rgba(8, 12, 20, 0.94) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-sizing: border-box !important;
  display: flex !important;
  align-items: center !important;
}`);
    } else {
      // Inject CSS into head
      if (content.includes('</head>')) {
        content = content.replace('</head>', `<style>${unifiedNavCss}\nbody { padding-top: 58px !important; margin: 0 !important; }</style>\n</head>`);
      }
    }

    // Ensure single unified nav HTML exists and remove redundant secondary navbars
    if (!content.includes('class="unified-top-nav"')) {
      if (content.includes('<body')) {
        content = content.replace(/<body[^>]*>/, match => `${match}\n${getUnifiedNavHtml(activeNav)}`);
      }
    }

    fs.writeFileSync(filePath, content, 'utf8');
  }
});

console.log('ALL TASKS REBUILT AND COMPLETED SUCCESSFULLY!');
