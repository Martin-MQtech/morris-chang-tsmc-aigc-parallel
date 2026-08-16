import os
import json
import re
import html
import subprocess

WORKSPACE = "/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC"
AUDIO_DIR = os.path.join(WORKSPACE, "audio")
EPISODES_DIR = os.path.join(WORKSPACE, "03-剧集")

def get_mp3_duration(file_path):
    if not os.path.exists(file_path):
        return 0.0
    try:
        res = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], capture_output=True, text=True)
        out = res.stdout.strip()
        if out:
            return float(out)
    except Exception as e:
        pass
    size = os.path.getsize(file_path)
    return round(size / 8000.0, 2)

# Acoustic Timing Model parameters:
# - Periods / exclamation / question: +0.85s pause weight
# - Commas / semicolons: +0.38s pause weight
# - Dashes / colons: +0.55s pause weight
# - Section headers & narrator markers: +1.5s - 2.0s pause (use 1.8s)
# - Pure vocalization: ~3.82 Chinese chars / second
def compute_raw_cue_duration(zh_text, en_text, is_section_header=False):
    # Count characters for vocalization
    # Strip spaces and punctuation
    pure_zh_chars = len(re.findall(r'[\u4e00-\u9fff0-9a-zA-Z]', zh_text))
    if pure_zh_chars == 0:
        # Check english words
        en_words = len(en_text.split())
        vocal_time = en_words / 2.8 if en_words > 0 else 1.0
    else:
        vocal_time = pure_zh_chars / 3.82

    # Pause weights
    # Periods / exclamation / question
    p_count = len(re.findall(r'[。！？!?\.]', zh_text))
    p_pause = p_count * 0.85

    # Commas / semicolons
    c_count = len(re.findall(r'[，、；,;]', zh_text))
    c_pause = c_count * 0.38

    # Dashes / colons
    d_count = len(re.findall(r'[———：:\-]', zh_text))
    d_pause = d_count * 0.55

    # Section headers & narrator markers
    marker_pause = 0.0
    if is_section_header or zh_text.startswith("【") or zh_text.startswith("[") or "【主叙述者】" in zh_text or "【Morris】" in zh_text or "【音效" in zh_text or "[SFX" in en_text:
        marker_pause = 1.8

    raw_duration = vocal_time + p_pause + c_pause + d_pause + marker_pause
    return max(raw_duration, 0.8)

def parse_markdown_sections(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
    
    sections = []
    cur_sec = None
    cur_paras = []
    
    for l in lines:
        if l.startswith("## "):
            if cur_sec is not None:
                sections.append((cur_sec, cur_paras))
            cur_sec = l[3:].strip()
            cur_paras = []
        elif l.startswith("# ") or l.startswith("> ") or l == "---" or not l:
            continue
        else:
            cur_paras.append(l)
            
    if cur_sec is not None:
        sections.append((cur_sec, cur_paras))
    return sections

print("Helper script ready.")
