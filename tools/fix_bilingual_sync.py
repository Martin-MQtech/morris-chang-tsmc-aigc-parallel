#!/usr/bin/env python3
"""Fix bilingual subtitle sync: add English cues + correct durationEn to all pages.

Root cause: durationEn was incorrectly set to durationZh (Chinese track duration),
and both players always used Chinese cue timestamps for subtitle highlighting.

This script:
  1. Regenerates audio_data.js with correct durationEn + cuesEn per episode.
  2. Patches audio.html EMBEDDED_MANIFEST + JS logic to use per-track cues.
  3. Patches all episode-XX.html: adds EP_CUES_EN + fixes JS logic.
"""
import json
import re
import os
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

with open("tools/real_cues.json", encoding="utf-8") as f:
    REAL = json.load(f)


# ── helpers ──

def fmt_ts(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m:02d}:{s:02d}"


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def build_ep_data(ep_num, ep_key):
    """Build audio_data.js entry for one episode."""
    r = REAL.get(ep_key)
    if not r:
        return None
    return {
        "id": f"{ep_num:02d}",
        "title": f"第{ep_num:02d}期",
        "enTitle": f"Episode {ep_num:02d}",
        "audioZh": f"audio/ep{ep_num:02d}-zh.mp3",
        "audioEn": f"audio/ep{ep_num:02d}-en.mp3",
        "durationZh": r["duration"],
        "durationEn": r["durationEn"],
        "cues": r["cues"],
        "cuesEn": r["cuesEn"],
    }


def build_subrow_html(cue, idx):
    """Build one sub-row HTML for episode-XX.html."""
    zh = esc(cue["zh"])
    en = esc(cue["en"])
    return (
        f'<div class="sub-row" id="sub-row-{idx}" data-index="{idx}" '
        f'data-start="{cue["start"]:.2f}" data-end="{cue["end"]:.2f}" '
        f'onclick="seekAndPlay({cue["start"]:.2f})">\n'
        f'            <span class="sub-time-tag">{fmt_ts(cue["start"])}</span>\n'
        f'            <div class="sub-content">\n'
        f'              <div class="sub-zh">{zh}</div>\n'
        f'              <div class="sub-en">{en}</div>\n'
        f'            </div>\n'
        f'          </div>'
    )


def build_cues_json_array(cues):
    """Build JSON array for EP_CUES / EP_CUES_EN."""
    return json.dumps(
        [{"secZh": "", "secEn": "", "speaker": "", "zh": c["zh"],
          "en": c["en"], "start": c["start"], "end": c["end"]} for c in cues],
        ensure_ascii=False)


# ══════════════════════════════════════════════════════════════
# STEP 1: Regenerate audio_data.js with correct durationEn + cuesEn
# ══════════════════════════════════════════════════════════════
def patch_audio_data_js():
    episodes = []
    for i in range(19):
        ep_key = f"ep{i:02d}"
        d = build_ep_data(i, ep_key)
        if d:
            episodes.append(d)

    js = ("// 自动生成：全19期双语剧场数据（波形实测真实时间戳，"
          "中英双轨各有独立时长与cue时间戳）\n")
    js += "window.AUDIO_DATA = " + json.dumps(episodes, ensure_ascii=False) + ";\n"
    js += "window.EPISODES_DATA = window.AUDIO_DATA;\n"

    with open("audio_data.js", "w", encoding="utf-8") as f:
        f.write(js)
    print(f"✅ audio_data.js 已更新（{len(episodes)} 期，含 cuesEn + 正确 durationEn）")
    return episodes


# ══════════════════════════════════════════════════════════════
# STEP 2: Patch audio.html — EMBEDDED_MANIFEST + JS logic
# ══════════════════════════════════════════════════════════════
def patch_audio_html(episodes):
    with open("audio.html", encoding="utf-8") as f:
        code = f.read()

    # 2a: Replace EMBEDDED_MANIFEST
    m = re.search(r'const EMBEDDED_MANIFEST = \[.*?\];', code, re.DOTALL)
    if m:
        manifest_json = json.dumps(episodes, ensure_ascii=False)
        code = code[:m.start()] + f"const EMBEDDED_MANIFEST = {manifest_json};" + code[m.end():]
    else:
        print("  ⚠️ audio.html: EMBEDDED_MANIFEST not found")
        return False

    # 2b: Fix renderSubtitles — use per-track cues
    # Current: ep.cues.forEach(...)
    # New:     (state.lang === 'zh' ? ep.cues : (ep.cuesEn || ep.cues)).forEach(...)
    old_render = "ep.cues.forEach((cue, cIdx) => {"
    new_render = "(state.lang === 'zh' ? ep.cues : (ep.cuesEn || ep.cues)).forEach((cue, cIdx) => {"
    if old_render in code:
        code = code.replace(old_render, new_render)
    else:
        print("  ⚠️ audio.html: renderSubtitles ep.cues.forEach not found (may already be patched)")

    # Also fix the guard: if (!ep.cues || ep.cues.length === 0)
    # Change to check active cues
    old_guard = "if (!ep.cues || ep.cues.length === 0)"
    new_guard = "if (!ep.cues || ep.cues.length === 0) { if (!(ep.cuesEn && ep.cuesEn.length > 0))"
    # Actually, simpler: just check both
    if old_guard in code:
        code = code.replace(old_guard,
            "if ((!ep.cues || ep.cues.length === 0) && (!ep.cuesEn || ep.cuesEn.length === 0))")

    # 2c: Fix syncSubtitles — use per-track cues
    # Current: for (let i = 0; i < ep.cues.length; i++) { if (time >= ep.cues[i].start ...
    old_sync_block = """function syncSubtitles(time) {
  const ep = state.episodes[state.currentEpIndex];
  if (!ep || !ep.cues) return;
  let activeIdx = -1;
  for (let i = 0; i < ep.cues.length; i++) {
    if (time >= ep.cues[i].start && time <= ep.cues[i].end) {"""
    new_sync_block = """function syncSubtitles(time) {
  const ep = state.episodes[state.currentEpIndex];
  if (!ep) return;
  const cues = state.lang === 'zh' ? ep.cues : (ep.cuesEn || ep.cues);
  if (!cues) return;
  let activeIdx = -1;
  for (let i = 0; i < cues.length; i++) {
    if (time >= cues[i].start && time <= cues[i].end) {"""
    if old_sync_block in code:
        code = code.replace(old_sync_block, new_sync_block)
    else:
        print("  ⚠️ audio.html: syncSubtitles block not found verbatim (checking partial)")
        # Try partial replacement
        if "if (!ep || !ep.cues) return;" in code:
            code = code.replace("if (!ep || !ep.cues) return;",
                "if (!ep) return;\n  const cues = state.lang === 'zh' ? ep.cues : (ep.cuesEn || ep.cues);\n  if (!cues) return;")

    with open("audio.html", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ audio.html 已更新（EMBEDDED_MANIFEST + renderSubtitles + syncSubtitles）")
    return True


# ══════════════════════════════════════════════════════════════
# STEP 3: Patch episode-XX.html — add EP_CUES_EN + fix JS logic
# ══════════════════════════════════════════════════════════════
def patch_episode_page(path, ep_key):
    with open(path, encoding="utf-8") as f:
        code = f.read()
    orig = code
    r = REAL.get(ep_key)
    if not r:
        return False

    cues_zh = r["cues"]
    cues_en = r["cuesEn"]

    # 3a: Replace sub-row HTML with ZH rows (default) + add data-start-en/data-end-en
    m = re.search(
        r'(<div class="subtitles-scroll" id="subtitles-viewport">)(.*?)(</div>\s*</div>\s*</div>\s*</div>)',
        code, re.DOTALL)
    if m:
        # Build rows with both zh and en timing
        rows = []
        for i, (cz, ce) in enumerate(zip(cues_zh, cues_en)):
            zh_text = esc(cz["zh"])
            en_text = esc(cz["en"])
            # Store both timings as data attributes
            rows.append(
                f'<div class="sub-row" id="sub-row-{i}" data-index="{i}" '
                f'data-start="{cz["start"]:.2f}" data-end="{cz["end"]:.2f}" '
                f'data-start-en="{ce["start"]:.2f}" data-end-en="{ce["end"]:.2f}" '
                f'onclick="seekAndPlay({cz["start"]:.2f})">\n'
                f'            <span class="sub-time-tag">{fmt_ts(cz["start"])}</span>\n'
                f'            <div class="sub-content">\n'
                f'              <div class="sub-zh">{zh_text}</div>\n'
                f'              <div class="sub-en">{en_text}</div>\n'
                f'            </div>\n'
                f'          </div>')
        rows_html = "\n".join(rows)
        new_block = m.group(1) + "\n" + rows_html + "\n          " + m.group(3)
        code = code[:m.start()] + new_block + code[m.end():]
    else:
        print(f"  ⚠️ {path}: viewport pattern not found")

    # 3b: Add EP_CUES_EN after EP_CUES definition
    en_cues_json = build_cues_json_array(cues_en)
    m2 = re.search(r'const EP_CUES\s*=\s*\[.*?\];', code, re.DOTALL)
    if m2:
        # Replace EP_CUES with correct zh cues AND add EP_CUES_EN
        zh_cues_json = build_cues_json_array(cues_zh)
        new_defs = f"const EP_CUES = {zh_cues_json};\nconst EP_CUES_EN = {en_cues_json};"
        code = code[:m2.start()] + new_defs + code[m2.end():]
    else:
        print(f"  ⚠️ {path}: EP_CUES not found")

    # 3c: Add getActiveCues helper and fix timeupdate handler
    # Replace the EP_CUES loop in timeupdate with getActiveCues()
    old_loop = "for (let i = 0; i < EP_CUES.length; i++) {"
    new_loop = "const _ac = currentTrack === 'en' ? EP_CUES_EN : EP_CUES; for (let i = 0; i < _ac.length; i++) {"
    code = code.replace(old_loop, new_loop)

    old_cue_ref = "const c = EP_CUES[i];"
    new_cue_ref = "const c = _ac[i];"
    code = code.replace(old_cue_ref, new_cue_ref)

    # Fix the boundary check: EP_CUES[EP_CUES.length - 1].end
    old_boundary = "cur >= EP_CUES[EP_CUES.length - 1].end"
    new_boundary = "cur >= _ac[_ac.length - 1].end"
    code = code.replace(old_boundary, new_boundary)

    old_boundary2 = "foundIdx = EP_CUES.length - 1;"
    new_boundary2 = "foundIdx = _ac.length - 1;"
    code = code.replace(old_boundary2, new_boundary2)

    # 3d: Fix switchTrack — update sub-row data attributes on track change
    # Find the end of switchTrack function and add row update logic
    old_switch_end = """      audioEl.load();
      audioEl.onloadedmetadata = () => {
        audioEl.currentTime = Math.min(curPos, audioEl.duration || curPos);
        totalTimeEl.textContent = formatTime(audioEl.duration);"""

    # Replace to also update sub-row data attributes
    new_switch_end = """      audioEl.load();
      audioEl.onloadedmetadata = () => {
        audioEl.currentTime = Math.min(curPos, audioEl.duration || curPos);
        totalTimeEl.textContent = formatTime(audioEl.duration);

        // Update sub-row timing + onclick to match active track
        const ac = currentTrack === 'en' ? EP_CUES_EN : EP_CUES;
        document.querySelectorAll('.sub-row').forEach((row, idx) => {
          if (idx < ac.length) {
            const c = ac[idx];
            row.dataset.start = c.start.toFixed(2);
            row.dataset.end = c.end.toFixed(2);
            row.setAttribute('onclick', 'seekAndPlay(' + c.start.toFixed(2) + ')');
            const timeTag = row.querySelector('.sub-time-tag');
            if (timeTag) timeTag.textContent = formatTime(c.start);
          }
        });"""

    if old_switch_end in code:
        code = code.replace(old_switch_end, new_switch_end)
    else:
        print(f"  ⚠️ {path}: switchTrack load pattern not found verbatim")

    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    return code != orig


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("🔧 修复双语字幕同步：添加英文轨 cues + 修正 durationEn")
    print("=" * 60)

    # Step 1: audio_data.js
    print("\n[1/3] 修复 audio_data.js ...")
    episodes = patch_audio_data_js()

    # Step 2: audio.html
    print("\n[2/3] 修复 audio.html ...")
    patch_audio_html(episodes)

    # Step 3: episode-XX.html
    print("\n[3/3] 修复 episode-XX.html ...")
    n = 0
    for i in range(19):
        ep_key = f"ep{i:02d}"
        ep_page = f"episode-{i:02d}.html"
        if os.path.exists(ep_page) and ep_key in REAL:
            if patch_episode_page(ep_page, ep_key):
                n += 1
                r = REAL[ep_key]
                print(f"  ✅ {ep_page}: {len(r['cues'])}条zh cues + {len(r['cuesEn'])}条en cues")
            else:
                print(f"  ⚠️ {ep_page}: 未修改（可能已打过补丁）")

    print(f"\n{'=' * 60}")
    print(f"修复完成：{n}/19 章节页 + audio.html + audio_data.js")
    print(f"durationEn 已从中文时长更正为英文实测时长")
    print(f"字幕高亮/滚动/seek 现在按当前音轨使用独立 cue 时间戳")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
