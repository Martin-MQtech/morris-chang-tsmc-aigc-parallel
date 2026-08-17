#!/usr/bin/env python3
"""19个单集页统一接入共享播放器架构：
- 数据：assets/episode-data.js（window.EPISODES_DATA，与双语剧场同源）
- 核心：assets/player-core.js（PlayerCore，与双语剧场共用一套）
- 保留：EPISODE_META、sub-row/bilingual-para 渲染、滚动、分享、词汇等页面特有逻辑
- 移除：内联 EP_CUES/EP_CUES_EN/ZH2EN 大数据块（改为运行时从共享数据构建）
"""
import re
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 单集页新 JS 主体（EPISODE_META 之前保留，此块从 `const EP_CUES` 起替换到脚本尾）
NEW_BODY = r"""    // ── 统一数据源（与双语剧场共用 assets/episode-data.js，波形实测时间戳）──
    const _EP = (window.EPISODES_DATA || []).find(function (e) { return e.id === EPISODE_META.id; }) || {};
    const EP_CUES = _EP.cues || [];
    const EP_CUES_EN = _EP.cuesEn || [];
    // ZH2EN：中文字幕段 -> 英文字幕段索引（按文本精确匹配；段数不匹配的附录段兜底到英文末尾）
    const ZH2EN = (function () {
      const norm = function (s) { return (s || '').replace(/\s+/g, ''); };
      const map = {};
      EP_CUES_EN.forEach(function (c, i) { if (c.zh) map[norm(c.zh)] = i; });
      return EP_CUES.map(function (c) {
        const z = norm(c.zh);
        return (z && map[z] !== undefined) ? map[z] : (EP_CUES_EN.length - 1);
      });
    })();

    let currentTrack = 'zh';
    let isPlaying = false;
    let autoScroll = true;
    let activeCueIndex = -1;
    let isSeeking = false;

    const audioEl = document.getElementById('main-audio');
    const audioSource = document.getElementById('audio-source');
    const playBtn = document.getElementById('master-play-btn');
    const curTimeEl = document.getElementById('cur-time');
    const totalTimeEl = document.getElementById('total-time');
    const seekSlider = document.getElementById('seek-slider');
    const btnTrackZh = document.getElementById('btn-track-zh');
    const btnTrackEn = document.getElementById('btn-track-en');
    const trackMetaTitle = document.getElementById('track-meta-title');
    const subtitlesViewport = document.getElementById('subtitles-viewport');
    const btnAutoScroll = document.getElementById('btn-auto-scroll');

    // ── 共享播放器核心（与双语剧场同一套 player-core.js）──
    const player = new PlayerCore({
      audioEl: audioEl,
      curTimeEl: curTimeEl,
      totalTimeEl: totalTimeEl,
      seekBar: seekSlider,
      bindSeekBar: false,          // 进度条拖动由页面 onSeekInput/onSeekChange 处理
      seekGuard: function () { return isSeeking; },
      bindPlayBtn: false,          // 播放按钮由页面 togglePlay() 处理
      bindTrackBtns: false,        // 切轨按钮由页面 switchTrack() 处理
      bindSpeed: false,            // 倍速由页面 changeSpeed() 处理
      onTrackChange: function (lang, ep) {
        currentTrack = lang;
        if (btnTrackZh) btnTrackZh.classList.toggle('active', lang === 'zh');
        if (btnTrackEn) btnTrackEn.classList.toggle('active', lang === 'en');
        if (trackMetaTitle) {
          trackMetaTitle.textContent = lang === 'zh'
            ? EPISODE_META.title_zh + '（中文原声）'
            : EPISODE_META.title_en + ' (English Voice)';
        }
        // sub-row 时间戳按目标轨更新（段数不匹配时重建）
        const ac = lang === 'en' ? EP_CUES_EN : EP_CUES;
        const rows = document.querySelectorAll('.sub-row');
        if (rows.length !== ac.length) {
          rebuildSubRows(ac);
        } else {
          rows.forEach(function (row, idx) {
            const c = ac[idx];
            row.dataset.start = c.start.toFixed(2);
            row.dataset.end = c.end.toFixed(2);
            row.setAttribute('onclick', 'seekAndPlay(' + c.start.toFixed(2) + ')');
            const timeTag = row.querySelector('.sub-time-tag');
            if (timeTag) timeTag.textContent = formatTime(c.start);
          });
        }
        // bilingual-para 时间戳 + 徽章按目标轨更新
        document.querySelectorAll('.bilingual-para').forEach(function (para) {
          const ci = parseInt(para.dataset.cueIdx, 10);
          if (isNaN(ci)) return;
          const pi = lang === 'en' ? (ZH2EN[ci] !== undefined ? ZH2EN[ci] : EP_CUES_EN.length - 1) : ci;
          const c = ac[Math.min(pi, ac.length - 1)];
          if (!c) return;
          para.setAttribute('onclick', 'seekAndPlay(' + c.start.toFixed(2) + ')');
          const badge = para.querySelector('.para-time-badge');
          if (badge) badge.textContent = formatTime(c.start);
        });
      },
      onCueChange: function (idx) {
        setActiveCue(idx);
      },
      onPlayChange: function (playing) {
        isPlaying = playing;
        if (playBtn) playBtn.textContent = playing ? '⏸' : '▶';
      }
    });

    // 页面特有：字幕行渲染（段数不匹配时按目标轨重建）
    function rebuildSubRows(cues) {
      const vp = document.getElementById('subtitles-viewport');
      if (!vp) return;
      vp.innerHTML = '';
      cues.forEach(function (c, i) {
        const row = document.createElement('div');
        row.className = 'sub-row';
        row.id = 'sub-row-' + i;
        row.dataset.index = i;
        row.dataset.start = c.start.toFixed(2);
        row.dataset.end = c.end.toFixed(2);
        row.onclick = function () { seekAndPlay(c.start); };
        const tag = document.createElement('span');
        tag.className = 'sub-time-tag';
        tag.textContent = formatTime(c.start);
        const content = document.createElement('div');
        content.className = 'sub-content';
        const zh = document.createElement('div');
        zh.className = 'sub-zh';
        zh.textContent = c.zh || '';
        const en = document.createElement('div');
        en.className = 'sub-en';
        en.textContent = c.en || '';
        content.appendChild(zh);
        content.appendChild(en);
        row.appendChild(tag);
        row.appendChild(content);
        vp.appendChild(row);
      });
    }

    function switchTrack(track) {
      player.switchTrack(track);
    }

    function togglePlay() {
      player.togglePlay();
    }

    function seekAndPlay(timeSec) {
      player.seekTo(timeSec);
      player.play();
    }

    function onSeekInput(val) {
      isSeeking = true;
      const targetTime = (val / 100) * (audioEl.duration || 0);
      curTimeEl.textContent = formatTime(targetTime);
    }

    function onSeekChange(val) {
      isSeeking = false;
      const targetTime = (val / 100) * (audioEl.duration || 0);
      audioEl.currentTime = targetTime;
    }

    function changeSpeed(spd) {
      audioEl.playbackRate = parseFloat(spd);
    }

    function toggleAutoScroll() {
      autoScroll = !autoScroll;
      btnAutoScroll.textContent = '自动滚动: ' + (autoScroll ? '开' : '关');
      btnAutoScroll.classList.toggle('active', autoScroll);
      showToast(autoScroll ? '字幕已开启自动跟随滚动' : '字幕自动滚动已关闭');
    }

    // Detection for User Manual Wheel or Touch Drag
    let isUserScrolling = false;
    let userScrollTimer = null;

    if (subtitlesViewport) {
      subtitlesViewport.addEventListener('wheel', function () {
        isUserScrolling = true;
        clearTimeout(userScrollTimer);
        userScrollTimer = setTimeout(function () { isUserScrolling = false; }, 2000);
      }, { passive: true });

      subtitlesViewport.addEventListener('touchstart', function () {
        isUserScrolling = true;
        clearTimeout(userScrollTimer);
        userScrollTimer = setTimeout(function () { isUserScrolling = false; }, 2000);
      }, { passive: true });
    }

    // Rock-Solid Container Center Scroll Logic
    function scrollSubtitleToCenter(container, activeElement) {
      if (!container || !activeElement || !autoScroll || isUserScrolling) return;

      const containerRect = container.getBoundingClientRect();
      const elementRect = activeElement.getBoundingClientRect();

      const elementRelativeTop = elementRect.top - containerRect.top + container.scrollTop;
      const targetScrollTop = elementRelativeTop - (container.clientHeight / 2) + (elementRect.height / 2);

      container.scrollTo({
        top: Math.max(0, targetScrollTop),
        behavior: 'smooth'
      });
    }

    function setActiveCue(index) {
      activeCueIndex = index;

      // Update Subtitles List
      document.querySelectorAll('.sub-row').forEach(function (row) { row.classList.remove('active'); });
      const activeRow = document.getElementById('sub-row-' + index);
      if (activeRow) {
        activeRow.classList.add('active');
        if (autoScroll && subtitlesViewport) {
          scrollSubtitleToCenter(subtitlesViewport, activeRow);
        }
      }

      // Update Book Paragraphs
      document.querySelectorAll('.bilingual-para').forEach(function (p) { p.classList.remove('current-reading'); });
      const activePara = document.querySelector('.bilingual-para[data-cue-idx="' + index + '"]');
      if (activePara) {
        activePara.classList.add('current-reading');
      }
    }

    function pronounceWord(word) {
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(word);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
      } else {
        showToast('浏览器不支持语音朗读');
      }
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(function () {
        toast.classList.remove('show');
      }, 2600);
    }

    // Sharing Matrix Logic
    function openWeChatShare() {
      const modal = document.getElementById('wechat-modal');
      const qrcode = document.getElementById('wechat-qrcode');
      const curUrl = encodeURIComponent(window.location.href);
      qrcode.src = 'https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=' + curUrl;
      modal.style.display = 'flex';
    }

    function closeWeChatShare() {
      document.getElementById('wechat-modal').style.display = 'none';
    }

    function shareToWeibo() {
      const text = encodeURIComponent('【台积电张忠谋 · 传记时间线的平行世界】' + EPISODE_META.title_zh + '：' + EPISODE_META.tagline_zh);
      const url = encodeURIComponent(window.location.href);
      window.open('https://service.weibo.com/share/share.php?title=' + text + '&url=' + url, '_blank');
    }

    function shareToLinkedIn() {
      const url = encodeURIComponent(window.location.href);
      window.open('https://www.linkedin.com/sharing/share-offsite/?url=' + url, '_blank');
    }

    function shareToX() {
      const text = encodeURIComponent('Reading & Listening to "Morris Chang & TSMC Parallel World" - ' + EPISODE_META.title_en + ':\n"' + EPISODE_META.tagline_en + '"');
      const url = encodeURIComponent(window.location.href);
      window.open('https://twitter.com/intent/tweet?text=' + text + '&url=' + url, '_blank');
    }

    function shareToWhatsApp() {
      const text = encodeURIComponent('《台积电张忠谋：传记时间线的平行世界》' + EPISODE_META.title_zh + '\n' + window.location.href);
      window.open('https://api.whatsapp.com/send?text=' + text, '_blank');
    }

    function shareToTelegram() {
      const text = encodeURIComponent('《台积电张忠谋：传记时间线的平行世界》' + EPISODE_META.title_zh);
      const url = encodeURIComponent(window.location.href);
      window.open('https://t.me/share/url?url=' + url + '&text=' + text, '_blank');
    }

    function shareToFacebook() {
      const url = encodeURIComponent(window.location.href);
      window.open('https://www.facebook.com/sharer/sharer.php?u=' + url, '_blank');
    }

    function copyViralShare() {
      const viralText = '【台积电张忠谋 · 传记时间线的平行世界】\n' +
        '📖 ' + EPISODE_META.title_zh + ' (' + EPISODE_META.time_loc + ')\n' +
        '💡 金句：' + EPISODE_META.tagline_zh + '\n' +
        '🎧 中英双语广播级原声剧场 + 逐句高亮字幕 + 深度研读笔记：\n' +
        window.location.href;

      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(viralText).then(function () {
          showToast('精选文案与链接已复制，去微信/小红书分享吧！');
        }).catch(function () {
          promptCopy(viralText);
        });
      } else {
        promptCopy(viralText);
      }
    }

    function promptCopy(text) {
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-999999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
        document.execCommand('copy');
        showToast('精选文案与链接已复制！');
      } catch (err) {
        showToast('复制失败，请手动长按复制');
      }
      document.body.removeChild(textArea);
    }

    // 启动：注入共享数据（音轨与字幕时间戳与双语剧场完全一致）
    player.loadEpisode({
      audioZh: './audio/ep' + EPISODE_META.id + '-zh.mp3',
      audioEn: './audio/ep' + EPISODE_META.id + '-en.mp3',
      durationZh: EP_CUES.length ? EP_CUES[EP_CUES.length - 1].end : 0,
      durationEn: EP_CUES_EN.length ? EP_CUES_EN[EP_CUES_EN.length - 1].end : 0,
      cues: EP_CUES,
      cuesEn: EP_CUES_EN
    }, {});
"""


def patch_page(path):
    src = open(path, encoding="utf-8").read()
    orig = src

    # 1) 在 <script> 前插入共享资源引用
    script_tag = '<script>\n    const EPISODE_META'
    idx = src.find(script_tag)
    if idx == -1:
        print(f"  ❌ 未找到脚本起点")
        return False
    refs = '<script src="assets/player-core.js"></script>\n<script src="assets/episode-data.js"></script>\n'
    if 'assets/player-core.js' not in src:
        src = src[:idx] + refs + src[idx:]

    # 2) 替换从 `const EP_CUES` 到 `</script>` 前的内容
    start = src.find('    const EP_CUES = [')
    if start == -1:
        print(f"  ❌ 未找到 const EP_CUES")
        return False
    end = src.rfind('</script>')
    src = src[:start] + NEW_BODY + "\n  " + src[end:]

    if src == orig:
        print(f"  ⚠️ 无变化")
        return False
    open(path, "w", encoding="utf-8").write(src)
    return True


def main():
    ok = fail = 0
    for i in range(19):
        path = os.path.join(BASE, f"episode-{i:02d}.html")
        print(f"ep{i:02d}:")
        try:
            if patch_page(path):
                ok += 1
            else:
                fail += 1
        except Exception as e:
            fail += 1
            print(f"  ❌ 异常: {e}")
    print(f"\n完成：成功 {ok}，失败 {fail}")


if __name__ == "__main__":
    main()
