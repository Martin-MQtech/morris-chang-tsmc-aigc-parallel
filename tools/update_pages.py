#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to:
1. Embed 4-voice sample showcase in index.html matching design system
2. Rebuild episode-01.html completely with index.html design tokens, 2-track switcher, synced teleprompter subtitles, bilingual full text, historical breakout boxes, vocabulary, strategic takeaways, golden quote, and navigation to Chapter 02.
3. Update .github/workflows/deploy.yml
"""

import os
import re
import shutil

ROOT_DIR = "/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC"
os.chdir(ROOT_DIR)

# 1. Copy audio files
os.makedirs("audio", exist_ok=True)
if os.path.exists("03-剧集/第01期-逃难的孩子/中文音频.mp3"):
    shutil.copy("03-剧集/第01期-逃难的孩子/中文音频.mp3", "audio/ep01-zh.mp3")
if os.path.exists("03-剧集/第01期-逃难的孩子/英文音频.mp3"):
    shutil.copy("03-剧集/第01期-逃难的孩子/英文音频.mp3", "audio/ep01-en.mp3")

# 2. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    index_content = f.read()

# Only add if not already present
if 'id="samples"' not in index_content:
    sample_section = """
  <!-- Samples & Voice Showcase -->
  <section class="section" id="samples" style="padding-top:0;">
    <div class="wrap">
      <div class="section-head">
        <span class="label">VOICE SAMPLES & DEMO · 音色与双语演示</span>
        <h2 class="serif">4-Voice Dual-Language Showcase<span class="en">AI Broadcast Voices with Real-Time Synced Script</span></h2>
        <p>提供 4 种中英专业广播级音色（男声/女声），支持逐句定点点击跳转与同步高亮字幕试听。</p>
      </div>

      <div style="background:var(--card); border:1px solid var(--line); border-radius:18px; padding:28px 24px; margin-top:20px; box-shadow:0 12px 36px rgba(0,0,0,0.4);">
        <!-- Voice Switcher Tabs -->
        <div style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:20px; border-bottom:1px solid var(--line); padding-bottom:16px;">
          <button class="btn primary demo-track-btn" data-track="zh-a" onclick="switchDemoTrack('zh-a', this)" style="font-size:13px; padding:8px 16px;">🇨🇳 中文 A (云健·男声)</button>
          <button class="btn ghost demo-track-btn" data-track="zh-b" onclick="switchDemoTrack('zh-b', this)" style="font-size:13px; padding:8px 16px;">🇨🇳 中文 B (云希·男声)</button>
          <button class="btn ghost demo-track-btn" data-track="en-a" onclick="switchDemoTrack('en-a', this)" style="font-size:13px; padding:8px 16px;">🇺🇸 英文 A (Christopher·男声)</button>
          <button class="btn ghost demo-track-btn" data-track="en-b" onclick="switchDemoTrack('en-b', this)" style="font-size:13px; padding:8px 16px;">🇺🇸 英文 B (Aria·女声)</button>
        </div>

        <!-- Audio Player Controls -->
        <div style="background:var(--bg2); border:1px solid var(--line); border-radius:12px; padding:16px 20px; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:16px;">
          <div style="display:flex; align-items:center; gap:14px;">
            <button id="demoPlayBtn" onclick="toggleDemoPlay()" style="width:44px; height:44px; border-radius:50%; background:var(--amber); border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; color:#000; font-size:18px; font-weight:bold; transition:transform 0.2s;">▶</button>
            <div>
              <div id="demoTrackTitle" style="font-weight:600; font-size:15px; color:var(--ink);">🇨🇳 中文 A (云健·男声)</div>
              <div style="font-size:12px; color:var(--muted); font-family:var(--en); font-style:italic;">Sample: The 1998 Asian Financial Crisis & TSMC's Counter-Cyclical Strategy</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:12px; flex-grow:1; max-width:480px;">
            <span id="demoCurTime" style="font-size:12px; color:var(--muted); font-family:monospace; min-width:38px;">00:00</span>
            <input type="range" id="demoSeek" min="0" max="100" value="0" step="0.1" oninput="seekDemoAudio(this.value)" style="flex-grow:1; accent-color:var(--amber); cursor:pointer; height:4px;">
            <span id="demoDuration" style="font-size:12px; color:var(--muted); font-family:monospace; min-width:38px;">00:00</span>
          </div>
          <audio id="demoAudioEl" src="./audio/zh-a.mp3" preload="metadata"></audio>
        </div>

        <!-- Synced Subtitles Viewport -->
        <div style="margin-top:20px;">
          <div style="font-size:11px; letter-spacing:2px; text-transform:uppercase; color:var(--muted); margin-bottom:12px; display:flex; justify-content:space-between;">
            <span>逐句同步字幕 · 点击任意句跳转 (CLICK SENTENCE TO SEEK)</span>
            <span style="color:var(--amber);">● 实时跟踪中</span>
          </div>
          <div id="demoSubtitlesList" style="display:flex; flex-direction:column; gap:10px; max-height:280px; overflow-y:auto; padding-right:8px;">
            
            <div class="demo-sub-item active" data-start="0" data-end="7" onclick="seekDemoTime(0)" style="padding:12px 16px; border-radius:10px; background:rgba(245,158,11,0.08); border-left:3px solid var(--amber); cursor:pointer; transition:all 0.2s;">
              <div style="font-size:15px; color:var(--amber); font-weight:600; line-height:1.6; font-family:'Songti SC','Noto Serif SC',serif;">一九九八年，亚洲金融风暴的余波未平，全球半导体业跌进近三十年最冷的冬天。</div>
              <div style="font-size:13px; color:#38BDF8; font-style:italic; font-family:Georgia,serif; margin-top:4px;">In 1998, the aftershocks of the Asian financial crisis still lingered, and the global semiconductor industry had fallen into its coldest winter in nearly three decades.</div>
            </div>

            <div class="demo-sub-item" data-start="7" data-end="13" onclick="seekDemoTime(7)" style="padding:12px 16px; border-radius:10px; background:var(--bg2); border-left:3px solid transparent; cursor:pointer; transition:all 0.2s;">
              <div style="font-size:15px; color:var(--ink); line-height:1.6; font-family:'Songti SC','Noto Serif SC',serif;">多数晶圆厂裁员、缩减资本支出，新竹科学园区的气氛凝重。</div>
              <div style="font-size:13px; color:var(--muted); font-style:italic; font-family:Georgia,serif; margin-top:4px;">Most semiconductor fabrication plants laid off workers and slashed capital expenditure. The atmosphere across the Hsinchu Science Park was grim.</div>
            </div>

            <div class="demo-sub-item" data-start="13" data-end="19" onclick="seekDemoTime(13)" style="padding:12px 16px; border-radius:10px; background:var(--bg2); border-left:3px solid transparent; cursor:pointer; transition:all 0.2s;">
              <div style="font-size:15px; color:var(--ink); line-height:1.6; font-family:'Songti SC','Noto Serif SC',serif;">但张忠谋做了一个让所有人意外的决定：逆势加码研发，扩建厂房。</div>
              <div style="font-size:13px; color:var(--muted); font-style:italic; font-family:Georgia,serif; margin-top:4px;">Yet Morris Chang made a decision that caught everyone off guard: he moved the other way, doubling down on R&D and expanding fab capacity.</div>
            </div>

            <div class="demo-sub-item" data-start="19" data-end="26" onclick="seekDemoTime(19)" style="padding:12px 16px; border-radius:10px; background:var(--bg2); border-left:3px solid transparent; cursor:pointer; transition:all 0.2s;">
              <div style="font-size:15px; color:var(--ink); line-height:1.6; font-family:'Songti SC','Noto Serif SC',serif;">他说：“不景气，是挖人才最好的时候。等景气回来，我们已经在下一个世代等他们了。”</div>
              <div style="font-size:13px; color:var(--muted); font-style:italic; font-family:Georgia,serif; margin-top:4px;">He said: "A recession is the best time to hire top talent. When the market rebounds, we will already be waiting for them at the next generation."</div>
            </div>

            <div class="demo-sub-item" data-start="26" data-end="35" onclick="seekDemoTime(26)" style="padding:12px 16px; border-radius:10px; background:var(--bg2); border-left:3px solid transparent; cursor:pointer; transition:all 0.2s;">
              <div style="font-size:15px; color:var(--ink); line-height:1.6; font-family:'Songti SC','Noto Serif SC',serif;">这就是台积电建立不可替代壁垒的关键时刻。</div>
              <div style="font-size:13px; color:var(--muted); font-style:italic; font-family:Georgia,serif; margin-top:4px;">This was precisely the defining moment when TSMC forged its irreplaceable moat.</div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </section>
"""

    demo_script = """
<script>
  // 4-Voice Demo Showcase Controller
  const demoAudio = document.getElementById('demoAudioEl');
  const demoPlayBtn = document.getElementById('demoPlayBtn');
  const demoSeek = document.getElementById('demoSeek');
  const demoCurTime = document.getElementById('demoCurTime');
  const demoDuration = document.getElementById('demoDuration');
  const demoTrackTitle = document.getElementById('demoTrackTitle');
  const demoTrackBtns = document.querySelectorAll('.demo-track-btn');
  const demoSubItems = document.querySelectorAll('.demo-sub-item');

  const demoTracks = {
    'zh-a': { src: './audio/zh-a.mp3', title: '🇨🇳 中文 A (云健·男声)' },
    'zh-b': { src: './audio/zh-b.mp3', title: '🇨🇳 中文 B (云希·男声)' },
    'en-a': { src: './audio/en-a.mp3', title: '🇺🇸 英文 A (Christopher·男声)' },
    'en-b': { src: './audio/en-b.mp3', title: '🇺🇸 英文 B (Aria·女声)' }
  };

  function switchDemoTrack(trackKey, btn) {
    if (!demoTracks[trackKey] || !demoAudio) return;
    const wasPlaying = !demoAudio.paused;
    const curTime = demoAudio.currentTime;
    demoAudio.src = demoTracks[trackKey].src;
    demoTrackTitle.textContent = demoTracks[trackKey].title;
    demoAudio.load();
    demoAudio.onloadedmetadata = () => {
      demoAudio.currentTime = Math.min(curTime, demoAudio.duration || curTime);
      updateDemoProgress();
      if (wasPlaying) demoAudio.play();
    };
    demoTrackBtns.forEach(b => {
      b.classList.remove('primary');
      b.classList.add('ghost');
    });
    if (btn) {
      btn.classList.remove('ghost');
      btn.classList.add('primary');
    }
  }

  function toggleDemoPlay() {
    if (!demoAudio) return;
    if (demoAudio.paused) {
      demoAudio.play();
      demoPlayBtn.innerHTML = '❚❚';
    } else {
      demoAudio.pause();
      demoPlayBtn.innerHTML = '▶';
    }
  }

  function seekDemoAudio(val) {
    if (!demoAudio || !demoAudio.duration) return;
    demoAudio.currentTime = (val / 100) * demoAudio.duration;
  }

  function seekDemoTime(sec) {
    if (!demoAudio) return;
    demoAudio.currentTime = sec;
    if (demoAudio.paused) {
      demoAudio.play();
      demoPlayBtn.innerHTML = '❚❚';
    }
  }

  function formatDemoTime(sec) {
    if (isNaN(sec)) return '00:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s);
  }

  if (demoAudio) {
    demoAudio.addEventListener('timeupdate', () => {
      updateDemoProgress();
      highlightDemoSubtitles(demoAudio.currentTime);
    });
    demoAudio.addEventListener('ended', () => {
      demoPlayBtn.innerHTML = '▶';
    });
    demoAudio.addEventListener('loadedmetadata', () => {
      demoDuration.textContent = formatDemoTime(demoAudio.duration);
    });
  }

  function updateDemoProgress() {
    if (!demoAudio) return;
    demoCurTime.textContent = formatDemoTime(demoAudio.currentTime);
    if (demoAudio.duration) {
      demoSeek.value = (demoAudio.currentTime / demoAudio.duration) * 100;
      demoDuration.textContent = formatDemoTime(demoAudio.duration);
    }
  }

  function highlightDemoSubtitles(currentTime) {
    demoSubItems.forEach(item => {
      const start = parseFloat(item.dataset.start);
      const end = parseFloat(item.dataset.end);
      const zhP = item.querySelector('div:first-child');
      const enP = item.querySelector('div:last-child');
      if (currentTime >= start && currentTime < end) {
        item.style.background = 'rgba(245,158,11,0.08)';
        item.style.borderLeftColor = 'var(--amber)';
        if (zhP) zhP.style.color = 'var(--amber)';
        if (enP) enP.style.color = '#38BDF8';
      } else {
        item.style.background = 'var(--bg2)';
        item.style.borderLeftColor = 'transparent';
        if (zhP) zhP.style.color = 'var(--ink)';
        if (enP) enP.style.color = 'var(--muted)';
      }
    });
  }
</script>
"""

    features_end_idx = index_content.find('</section>', index_content.find('id="features"'))
    if features_end_idx != -1:
        insert_pos = features_end_idx + len('</section>')
        index_content = index_content[:insert_pos] + "\n" + sample_section + index_content[insert_pos:]
        body_end_idx = index_content.rfind('</body>')
        if body_end_idx != -1:
            index_content = index_content[:body_end_idx] + demo_script + "\n" + index_content[body_end_idx:]
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(index_content)
        print("Updated index.html successfully with 4-voice showcase!")

print("Step 2 completed.")
