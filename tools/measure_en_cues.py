#!/usr/bin/env python3
"""Measure REAL per-segment timestamps for the ENGLISH track of each episode.

Mirrors tools/measure_real_cues.py but for the English audio
(audio/epXX-en.mp3) paired with the English script segments
(03-剧集/<期>/英文文字稿.md). The Chinese track already has its cues in
tools/real_cues.json; this produces the matching English cue set so the
player can switch tracks without subtitle drift.

Writes output to a JSON file (one per batch to allow parallel runs):
{ "epXX": {"cues": [...], "duration": <s>, "zhCount": n, "enCount": n} }

Usage: python3 tools/measure_en_cues.py <out.json> ep00 ep01 ...
"""
import os
import re
import sys
import json
import subprocess
import importlib.util

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

_spec = importlib.util.spec_from_file_location(
    "measure_real_cues", os.path.join(BASE, "tools", "measure_real_cues.py"))
mr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mr)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 tools/measure_en_cues.py <out.json> ep00 ep01 ...")
        sys.exit(1)
    out_path = sys.argv[1]
    targets = sys.argv[2:]

    results = {}
    for tag in targets:
        ep = tag if tag.startswith("ep") else f"ep{tag}"
        ep_num = ep[2:]
        mp3 = os.path.join("audio", f"{ep}-en.mp3")
        if not os.path.exists(mp3):
            print(f"{ep}: EN MP3 not found, skip")
            continue

        matches = [d for d in os.listdir("03-剧集") if d.startswith(f"第{ep_num}期")]
        folder = os.path.join("03-剧集", matches[0]) if matches else None
        en_file = os.path.join(folder, "英文文字稿.md") if folder else None
        zh_file = os.path.join(folder, "中文文字稿.md") if folder else None
        if not en_file or not os.path.exists(en_file):
            print(f"{ep}: no EN script, skip")
            continue

        zh_segs = mr.clean_segments(open(zh_file, encoding="utf-8").read())
        en_segs = mr.clean_segments(open(en_file, encoding="utf-8").read())
        seg_texts = [(zh_segs[i] if i < len(zh_segs) else "", s)
                     for i, s in enumerate(en_segs)]

        x = mr.decode_to_float(mp3)
        total_dur = len(x) / mr.RATE
        cues, thr = mr.find_best_cues(x, total_dur, seg_texts)

        if cues is None:
            print(f"{ep}: ❌ 无法匹配 {len(en_segs)} 段英文文本 — 跳过 "
                  f"(zh={len(zh_segs)} 段)")
            continue

        results[ep] = {
            "cues": cues,
            "duration": round(total_dur, 2),
            "zhCount": len(zh_segs),
            "enCount": len(en_segs),
        }
        last_end = cues[-1]["end"]
        print(f"{ep}: ✅ 英文 {len(cues)} 段对齐 (阈值 {thr}s) | 英文音频 {total_dur:.1f}s | "
              f"最后字幕 {last_end:.1f}s | zh段={len(zh_segs)} en段={len(en_segs)}")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)
    print(f"\n已保存 {out_path}（{len(results)} 期英文轨成功）")


if __name__ == "__main__":
    main()
