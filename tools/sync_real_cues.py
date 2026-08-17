#!/usr/bin/env python3
"""Sync real waveform-measured cues into ALL pages.

episode-XX.html has THREE places holding subtitle timing:
  1. <div class="subtitles-scroll" id="subtitles-viewport"> sub-row list
  2. const EP_CUES = [...] (drives highlight sync)
  3. Book body: bilingual-para rows with onclick seek + time badge

We replace all three with waveform-measured real cues. Ghost rows
(【音效】/【主叙述者】/header markers) are REMOVED from the subtitle
teleprompter and cue array (TTS never reads them); they remain in the
book body as reading content but with mapped seek times.
"""
import os
import re
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

with open("tools/real_cues.json", encoding="utf-8") as f:
    REAL = json.load(f)


def fmt_ts(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m:02d}:{s:02d}"


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def build_subrow_html(cue):
    zh = esc(cue["zh"])
    en = esc(cue["en"])
    return (
        f'<div class="sub-row" id="sub-row-{cue["idx"]}" data-index="{cue["idx"]}" '
        f'data-start="{cue["start"]:.2f}" data-end="{cue["end"]:.2f}" '
        f'onclick="seekAndPlay({cue["start"]:.2f})">\n'
        f'            <span class="sub-time-tag">{fmt_ts(cue["start"])}</span>\n'
        f'            <div class="sub-content">\n'
        f'              <div class="sub-zh">{zh}</div>\n'
        f'              <div class="sub-en">{en}</div>\n'
        f'            </div>\n'
        f'          </div>'
    )


def patch_episode(path, cues):
    with open(path, encoding="utf-8") as f:
        code = f.read()
    orig = code

    # ── Step 1: Replace sub-row HTML inside subtitles-viewport ──
    m = re.search(
        r'(<div class="subtitles-scroll" id="subtitles-viewport">)(.*?)(</div>\s*</div>\s*</div>\s*</div>)',
        code, re.DOTALL)
    if not m:
        print(f"  ⚠️ {path}: viewport pattern not found")
        return False

    rows = "\n".join(build_subrow_html(c) for c in cues)
    indent_rows = "".join(f"          {line}\n" for line in rows.split("\n"))
    new_block = m.group(1) + "\n" + indent_rows + m.group(3)
    code = code[:m.start()] + new_block + code[m.end():]

    # ── Step 2: Replace EP_CUES / CUES array in script ──
    cues_json = json.dumps(
        [{"secZh": "", "secEn": "", "speaker": "", "zh": c["zh"],
          "en": c["en"], "start": c["start"], "end": c["end"]} for c in cues],
        ensure_ascii=False)
    m2 = re.search(r'const (?:EP_)?CUES\s*=\s*\[.*?\];', code, re.DOTALL)
    if m2:
        var_name = re.search(r'const ((?:EP_)?CUES)\s*=', code[m2.start():m2.start()+30]).group(1)
        code = code[:m2.start()] + f"const {var_name} = {cues_json};" + code[m2.end():]
    else:
        print(f"  ⚠️ {path}: CUES array not found")

    # ── Step 3: Sync bilingual-para seek times & badges in book body ──
    # Book body shows the FULL script (incl. SFX/narrator lines that TTS never
    # reads). Non-marker paras map in order to real cues; marker paras map to
    # the next real cue time.
    markers = re.compile(r"【音效|【主叙述|\[SFX|\[Main narrator")
    para_ids = [mm.group(1) for mm in re.finditer(
        r'<div class="bilingual-para[^"]*" id="para-(\d+)"', code)]
    zh_texts = re.findall(r'<p class="zh-para">([^<]*)</p>', code)

    cursor = 0
    for pid, zhtxt in zip(para_ids, zh_texts):
        if markers.search(zhtxt):
            t = cues[min(cursor, len(cues) - 1)]["start"]
        else:
            t = cues[min(cursor, len(cues) - 1)]["start"]
            cursor += 1
        badge = fmt_ts(t)
        code = re.sub(
            rf'(id="para-{pid}" onclick="seekAndPlay\()[\d\.]+(\)")',
            lambda mm: mm.group(1) + f"{t:.2f}" + mm.group(2), code)
        code = re.sub(
            rf'(id="para-{pid}"[^>]*>.*?<span class="para-time-badge">)[^<]*(</span>)',
            lambda mm: mm.group(1) + badge + mm.group(2), code, flags=re.DOTALL)

    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    return code != orig


def patch_audio_html(path, episodes):
    with open(path, encoding="utf-8") as f:
        code = f.read()
    m = re.search(r'const EMBEDDED_MANIFEST = \[.*?\];', code, re.DOTALL)
    if not m:
        return False
    manifest_json = json.dumps(episodes, ensure_ascii=False)
    code = code[:m.start()] + f"const EMBEDDED_MANIFEST = {manifest_json};" + code[m.end():]
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    return True


def patch_audio_data_js(path, episodes):
    js = "// 自动生成：全19期双语剧场数据（波形实测真实时间戳，无幽灵字幕）\n"
    js += "window.AUDIO_DATA = " + json.dumps(episodes, ensure_ascii=False) + ";\n"
    js += "window.EPISODES_DATA = window.AUDIO_DATA;\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(js)


def main():
    episodes = []
    n_ep = 0
    for i in range(19):
        ep = f"ep{i:02d}"
        if ep not in REAL:
            print(f"⚠️ {ep}: no real cues, skip")
            continue
        cues = REAL[ep]["cues"]
        episodes.append({
            "id": f"{i:02d}",
            "title": f"第{i:02d}期",
            "enTitle": f"Episode {i:02d}",
            "audioZh": f"audio/ep{i:02d}-zh.mp3",
            "audioEn": f"audio/ep{i:02d}-en.mp3",
            "durationZh": REAL[ep]["duration"],
            "durationEn": REAL[ep]["duration"],
            "cues": cues,
        })

        ep_page = f"episode-{i:02d}.html"
        if os.path.exists(ep_page):
            if patch_episode(ep_page, cues):
                n_ep += 1
                print(f"✅ {ep_page}: {len(cues)} 条真实字幕已注入")

    if patch_audio_html("audio.html", episodes):
        print(f"✅ audio.html: EMBEDDED_MANIFEST 已更新（{len(episodes)} 期）")

    patch_audio_data_js("audio_data.js", episodes)
    print(f"✅ audio_data.js 已更新")

    print(f"\n完成：{n_ep}/19 章节页 + audio.html + audio_data.js")


if __name__ == "__main__":
    main()
