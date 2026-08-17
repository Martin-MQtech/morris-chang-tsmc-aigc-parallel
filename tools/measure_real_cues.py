#!/usr/bin/env python3
"""Measure REAL per-segment timestamps from the final MP3 waveform.

make_tts.py concatenates per-segment edge-tts clips with a fixed 0.7s
digital-silence gap between them. Those gaps appear as long near-zero
amplitude runs in the waveform. We detect them with an ADAPTIVE threshold
(0.55s → 1.70s step 0.05s) and pick the first threshold whose speech-span
count exactly matches the number of text segments. This yields physically
exact per-segment boundaries — no character-count estimation, no drift.

Usage: python3 tools/measure_real_cues.py [ep01 ep02 ...]
"""
import os
import re
import sys
import json
import subprocess
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

RATE = 24000          # match make_tts.py silence generation
WIN = 480             # 20ms RMS window
HOP = 120             # 5ms hop → 200 frames/sec
THRESH = 0.02         # silence if rms < max_rms * THRESH


def decode_to_float(path):
    """Decode MP3 → mono float32 at RATE via ffmpeg."""
    proc = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(RATE),
         "-f", "f32le", "-"],
        capture_output=True, check=True)
    return np.frombuffer(proc.stdout, dtype=np.float32)


def detect_gaps(x, min_gap):
    """Return list of (gap_start_s, gap_end_s) for silence runs ≥ min_gap."""
    n = len(x)
    idx = 0
    rms = []
    while idx + WIN <= n:
        seg = x[idx:idx + WIN]
        rms.append(float(np.sqrt(np.mean(seg * seg))))
        idx += HOP
    if idx < n:
        rms.append(float(np.sqrt(np.mean(x[idx:] * x[idx:]))))
    rms = np.array(rms)
    peak = rms.max()
    if peak <= 0:
        return []
    thr = max(peak * THRESH, 1e-4)
    silent = rms < thr

    gaps = []
    i = 0
    frames = len(silent)
    while i < frames:
        if silent[i]:
            j = i
            while j < frames and silent[j]:
                j += 1
            dur = (j - i) * HOP / RATE
            if dur >= min_gap:
                gaps.append((i * HOP / RATE, j * HOP / RATE))
            i = j
        else:
            i += 1
    return gaps


def spans_from(gaps, total_dur):
    """Speech spans between gaps (leading span starts at 0, trailing at end)."""
    spans = []
    prev = 0.0
    for (gs, ge) in gaps:
        if ge - prev > 0.1:
            spans.append((prev, gs))
        prev = ge
    if total_dur - prev > 0.1:
        spans.append((prev, total_dur))
    return spans


def build_cues(gaps, total_dur, seg_texts):
    """Map speech spans to text segments; normalize leading/trailing gaps."""
    target = len(seg_texts)

    def try_spans(glist):
        sp = spans_from(glist, total_dur)
        if len(sp) == target:
            return sp
        # audio may start with silence (drop first gap) or end with the
        # appended 0.7s pause (drop last gap)
        if len(sp) == target + 1 and glist:
            sp2 = spans_from(glist[1:], total_dur)
            if len(sp2) == target:
                return sp2
            sp3 = spans_from(glist[:-1], total_dur)
            if len(sp3) == target:
                return sp3
        return None

    spans = try_spans(gaps)
    if spans is None:
        return None

    cues = []
    for i, (st, et) in enumerate(spans):
        cues.append({
            "idx": i,
            "start": round(st, 2),
            "end": round(et, 2),
            "zh": seg_texts[i][0],
            "en": seg_texts[i][1] if len(seg_texts[i]) > 1 else "",
        })
    return cues


def find_best_cues(x, total_dur, seg_texts):
    """Adaptive threshold scan: first min_gap whose span count matches."""
    for t in np.arange(0.55, 1.71, 0.05):
        t = round(float(t), 2)
        gaps = detect_gaps(x, t)
        cues = build_cues(gaps, total_dur, seg_texts)
        if cues is not None:
            return cues, t
    return None, None


def clean_segments(text):
    """Same logic as make_tts.py — only lines the TTS actually reads."""
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


def main():
    targets = sys.argv[1:] or [f"ep{i:02d}" for i in range(19)]
    results = {}
    for tag in targets:
        ep = tag if tag.startswith("ep") else f"ep{tag}"
        ep_num = ep[2:]
        mp3 = os.path.join("audio", f"{ep}-zh.mp3")
        if not os.path.exists(mp3):
            print(f"{ep}: MP3 not found, skip")
            continue

        matches = [d for d in os.listdir("03-剧集") if d.startswith(f"第{ep_num}期")]
        folder = os.path.join("03-剧集", matches[0]) if matches else None
        zh_file = os.path.join(folder, "中文文字稿.md") if folder else None
        en_file = os.path.join(folder, "英文文字稿.md") if folder else None
        if not zh_file or not os.path.exists(zh_file):
            print(f"{ep}: no script, skip")
            continue

        zh_segs = clean_segments(open(zh_file, encoding="utf-8").read())
        en_segs = clean_segments(open(en_file, encoding="utf-8").read()) if os.path.exists(en_file) else []
        seg_texts = [(s, en_segs[i] if i < len(en_segs) else "") for i, s in enumerate(zh_segs)]

        x = decode_to_float(mp3)
        total_dur = len(x) / RATE
        cues, thr = find_best_cues(x, total_dur, seg_texts)

        if cues is None:
            print(f"{ep}: ❌ 无法匹配 {len(zh_segs)} 段文本 — 跳过")
            continue

        results[ep] = {"cues": cues, "duration": round(total_dur, 2)}
        last_end = cues[-1]["end"]
        print(f"{ep}: ✅ {len(cues)} 段全部对齐 (阈值 {thr}s) | 音频 {total_dur:.1f}s | "
              f"最后字幕 {last_end:.1f}s")

    with open(os.path.join(BASE, "tools", "real_cues.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)
    print(f"\n已保存 tools/real_cues.json（{len(results)} 期成功）")


if __name__ == "__main__":
    main()
