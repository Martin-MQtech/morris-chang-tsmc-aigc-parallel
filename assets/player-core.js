/*!
 * player-core.js — 全站共享播放器核心（双语剧场 + 单集页共用一套）
 *
 * 统一能力：
 *  - 中英双轨切换（音轨 + 字幕时间戳同步切换）
 *  - 字幕逐句高亮 + 居中滚动
 *  - 播放/暂停/进度/倍速/音量
 *  - 全站单音频排他（同一时刻只有一个音频在响）
 *
 * 用法（剧场 / 单集页各自实例化，注入自己的 DOM）：
 *   const player = new PlayerCore({
 *     audioEl,            // <audio> 元素
 *     container,          // 字幕滚动容器
 *     playBtn,            // 播放/暂停按钮（可选）
 *     playIcon,           // 播放图标（可选）
 *     curTimeEl,          // 当前时间文本（可选）
 *     totalTimeEl,        // 总时长文本（可选）
 *     progressFill,       // 进度条填充（可选）
 *     seekBar,            // 进度条（可选）
 *     speedSelect,        // 倍速选择（可选）
 *     volSlider,          // 音量滑杆（可选）
 *     trackZhBtn, trackEnBtn,  // 中英切换按钮（可选）
 *     onTrackChange(lang, ep)  // 切轨后回调（页面更新标题/按钮态）
 *   });
 *   player.loadEpisode(epData, {autoPlay:false, lang:'zh'});
 *   player.switchTrack('en');
 *
 * 数据约定：ep 形如 {audioZh, audioEn, durationZh, durationEn, cues, cuesEn}
 *   cues / cuesEn 元素形如 {start, end, zh, en}
 */
(function (global) {
  'use strict';

  var ACTIVE_AUDIO = null;

  /** 全站排他：新音频播放时暂停其他所有音频 */
  function ensureSingleAudioPlayback(el) {
    if (ACTIVE_AUDIO && ACTIVE_AUDIO !== el && !ACTIVE_AUDIO.paused) {
      ACTIVE_AUDIO.pause();
    }
    ACTIVE_AUDIO = el;
  }

  /** 秒 -> mm:ss */
  function formatTime(sec) {
    if (isNaN(sec) || sec < 0) sec = 0;
    var m = Math.floor(sec / 60);
    var s = Math.floor(sec % 60);
    return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  }

  /** 根据当前时间找到 active cue 索引（-1 表示未命中） */
  function findActiveCue(cues, time) {
    if (!cues || cues.length === 0) return -1;
    for (var i = 0; i < cues.length; i++) {
      var c = cues[i];
      if (time >= c.start && time < c.end) return i;
    }
    var last = cues[cues.length - 1];
    if (time >= last.end) return cues.length - 1;
    return -1;
  }

  function PlayerCore(opts) {
    if (!(this instanceof PlayerCore)) return new PlayerCore(opts);
    this.opts = opts || {};
    this.audioEl = this.opts.audioEl;
    this.lang = this.opts.initialLang || 'zh';
    this.ep = null;
    this.currentCues = [];
    this._activeIdx = -1;
    this._bindEvents();
    this._bindControls();
  }

  PlayerCore.prototype._bindEvents = function () {
    var self = this;
    var audio = this.audioEl;
    if (!audio) return;

    audio.addEventListener('play', function () {
      ensureSingleAudioPlayback(audio);
      self._setPlaying(true);
    });
    audio.addEventListener('pause', function () { self._setPlaying(false); });
    audio.addEventListener('timeupdate', function () { self._onTimeUpdate(); });
    audio.addEventListener('loadedmetadata', function () {
      if (self.opts.totalTimeEl && audio.duration && !isNaN(audio.duration)) {
        self.opts.totalTimeEl.textContent = formatTime(audio.duration);
      }
    });
  };

  PlayerCore.prototype._bindControls = function () {
    var self = this;
    var o = this.opts;

    if (o.playBtn && o.bindPlayBtn !== false) {
      o.playBtn.addEventListener('click', function () { self.togglePlay(); });
    }
    if (o.trackZhBtn && o.bindTrackBtns !== false) {
      o.trackZhBtn.addEventListener('click', function () { self.switchTrack('zh'); });
    }
    if (o.trackEnBtn && o.bindTrackBtns !== false) {
      o.trackEnBtn.addEventListener('click', function () { self.switchTrack('en'); });
    }
    if (o.speedSelect && o.bindSpeed !== false) {
      o.speedSelect.addEventListener('change', function () {
        self.audioEl.playbackRate = parseFloat(o.speedSelect.value) || 1;
      });
    }
    if (o.volSlider) {
      o.volSlider.addEventListener('input', function () {
        self.audioEl.volume = parseFloat(o.volSlider.value) || 1;
      });
    }
    if (o.seekBar && o.bindSeekBar !== false) {
      o.seekBar.addEventListener('input', function () {
        if (self.audioEl.duration) {
          self.audioEl.currentTime = (parseFloat(o.seekBar.value) / 100) * self.audioEl.duration;
        }
      });
      o.seekBar.addEventListener('change', function () {
        if (self.audioEl.duration) {
          self.audioEl.currentTime = (parseFloat(o.seekBar.value) / 100) * self.audioEl.duration;
        }
      });
    }
  };

  PlayerCore.prototype._setPlaying = function (playing) {
    this.isPlaying = playing;
    var o = this.opts;
    if (o.playBtn) {
      o.playBtn.classList.toggle('active', playing);
      if (o.playBtn.dataset.playingText) o.playBtn.textContent = playing ? o.playBtn.dataset.playingText : o.playBtn.dataset.pausedText;
    }
    if (o.playIcon && typeof o.playIcon === 'object' && o.playIcon.tagName !== 'svg') {
      o.playIcon.textContent = playing ? '⏸' : '▶';
    }
    if (o.onPlayChange) o.onPlayChange(playing);
  };

  /** 加载一期（数据统一来自 window.EPISODES_DATA） */
  PlayerCore.prototype.loadEpisode = function (ep, extra) {
    extra = extra || {};
    if (!ep) return;
    this.ep = ep;
    if (extra.lang) this.lang = extra.lang;
    this.currentCues = this.lang === 'en' ? (ep.cuesEn || ep.cues || []) : (ep.cues || []);
    this._activeIdx = -1;

    var src = this.lang === 'en' ? ep.audioEn : ep.audioZh;
    if (src && this.audioEl.src !== this._abs(src)) {
      this.audioEl.src = src;
      this.audioEl.load();
    }
    if (this.opts.onTrackChange) this.opts.onTrackChange(this.lang, ep);
    if (extra.autoPlay) this.play();
  };

  PlayerCore.prototype._abs = function (url) {
    try { return new URL(url, global.location.href).href; } catch (e) { return url; }
  };

  /** 切换中英轨：换音轨 + 换字幕时间戳数组，保留当前播放进度 */
  PlayerCore.prototype.switchTrack = function (lang) {
    if (!this.ep || lang === this.lang) return;
    var cur = this.audioEl.currentTime || 0;
    var wasPlaying = !this.audioEl.paused;
    this.lang = lang;
    this.currentCues = lang === 'en' ? (this.ep.cuesEn || this.ep.cues || []) : (this.ep.cues || []);
    this._activeIdx = -1;

    var src = lang === 'en' ? this.ep.audioEn : this.ep.audioZh;
    if (src) {
      this.audioEl.src = src;
      this.audioEl.load();
      var self = this;
      this.audioEl.onloadedmetadata = function () {
        self.audioEl.currentTime = Math.min(cur, self.audioEl.duration || cur);
        if (wasPlaying) {
          ensureSingleAudioPlayback(self.audioEl);
          self.audioEl.play().catch(function () {});
        }
      };
    }
    if (this.opts.onTrackChange) this.opts.onTrackChange(lang, this.ep);
  };

  PlayerCore.prototype.play = function () {
    var audio = this.audioEl;
    if (!audio) return;
    ensureSingleAudioPlayback(audio);
    audio.play().then(function () {
      // play 事件会同步 _setPlaying
    }).catch(function (e) { console.error('Playback error:', e); });
  };

  PlayerCore.prototype.pause = function () {
    if (this.audioEl) this.audioEl.pause();
  };

  PlayerCore.prototype.togglePlay = function () {
    if (!this.audioEl) return;
    if (this.audioEl.paused) this.play();
    else this.pause();
  };

  PlayerCore.prototype.seekTo = function (t) {
    if (this.audioEl && this.audioEl.duration) {
      this.audioEl.currentTime = Math.max(0, Math.min(t, this.audioEl.duration));
    }
  };

  /** timeupdate：高亮当前句 + 更新进度 UI */
  PlayerCore.prototype._onTimeUpdate = function () {
    var audio = this.audioEl;
    if (!audio) return;
    var o = this.opts;
    if (o.seekGuard && o.seekGuard()) return;  // 拖动进度条时暂停同步

    if (o.curTimeEl) o.curTimeEl.textContent = formatTime(audio.currentTime);
    if (o.totalTimeEl && audio.duration && !isNaN(audio.duration)) {
      o.totalTimeEl.textContent = formatTime(audio.duration);
    }
    if (o.seekBar && audio.duration) {
      o.seekBar.value = (audio.currentTime / audio.duration) * 100;
    }
    if (o.progressFill && audio.duration) {
      o.progressFill.style.width = ((audio.currentTime / audio.duration) * 100).toFixed(2) + '%';
    }

    var idx = findActiveCue(this.currentCues, audio.currentTime);
    if (idx !== this._activeIdx) {
      this._activeIdx = idx;
      if (this.opts.onCueChange) this.opts.onCueChange(idx, this.currentCues[idx]);
    }
  };

  /** 立即按当前时间同步高亮（seek / 兜底计时器时手动触发） */
  PlayerCore.prototype.syncNow = function () {
    this._onTimeUpdate();
  };

  PlayerCore.prototype.getActiveIndex = function () { return this._activeIdx; };
  PlayerCore.prototype.getCues = function () { return this.currentCues; };
  PlayerCore.prototype.getLang = function () { return this.lang; };

  // 导出
  global.PlayerCore = PlayerCore;
  global.ensureSingleAudioPlayback = ensureSingleAudioPlayback;
  global.formatTime = formatTime;
  global.findActiveCue = findActiveCue;
})(typeof window !== 'undefined' ? window : this);
