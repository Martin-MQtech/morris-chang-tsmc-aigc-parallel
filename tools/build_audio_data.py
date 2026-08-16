#!/usr/bin/env python3
import os
import glob
import re
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPISODES_DIR = os.path.join(BASE_DIR, '03-剧集')

def get_duration(file_path):
    if not os.path.exists(file_path):
        return 600.0
    try:
        res = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], capture_output=True, text=True)
        out = res.stdout.strip()
        if out:
            return float(out)
    except Exception as e:
        pass
    # Fallback estimation based on file size: 64kbps MP3 is ~8KB/s
    size = os.path.getsize(file_path)
    return round(size / 8000.0, 2)

def clean_script_paras(text):
    # Split by lines
    lines = text.split('\n')
    paras = []
    current_sec = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('# '):
            continue
        if line.startswith('> '):
            continue
        if line.startswith('---'):
            continue
        if line.startswith('## '):
            current_sec = line.replace('## ', '').strip()
            continue
        paras.append({
            'sec': current_sec,
            'text': line
        })
    return paras

def process_all_episodes():
    episodes = sorted([d for d in glob.glob(os.path.join(EPISODES_DIR, '第*')) if os.path.isdir(d)])
    all_episodes_data = []

    print(f"Found {len(episodes)} episodes.")

    for ep_dir in episodes:
        folder_name = os.path.basename(ep_dir)
        m = re.match(r'第(\d+)期-(.+)', folder_name)
        ep_id = m.group(1) if m else '00'
        ep_name = m.group(2) if m else folder_name

        zh_path = os.path.join(ep_dir, '中文文字稿.md')
        en_path = os.path.join(ep_dir, '英文文字稿.md')
        zh_mp3 = f'./03-剧集/{folder_name}/中文音频.mp3'
        en_mp3 = f'./03-剧集/{folder_name}/英文音频.mp3'

        zh_dur = get_duration(os.path.join(ep_dir, '中文音频.mp3'))
        en_dur = get_duration(os.path.join(ep_dir, '英文音频.mp3'))

        with open(zh_path, 'r', encoding='utf-8') as f:
            zh_text = f.read()
        with open(en_path, 'r', encoding='utf-8') as f:
            en_text = f.read()

        # Extract title
        en_title_match = re.search(r'# Morris Chang\'s Parallel World · Episode \d+: "(.*?)"', en_text)
        if not en_title_match:
            en_title_match = re.search(r'# Morris Chang\'s Parallel World · Episode \d+: (.*?)\n', en_text)
        en_title = en_title_match.group(1).strip() if en_title_match else ep_name

        zh_title = f'第{ep_id}期 {ep_name}'

        zh_paras = clean_script_paras(zh_text)
        en_paras = clean_script_paras(en_text)

        # Align paragraphs
        # Pair them by matching index or normalizing
        cues = []
        max_len = max(len(zh_paras), len(en_paras))
        for i in range(max_len):
            zp = zh_paras[i] if i < len(zh_paras) else {'sec': '', 'text': ''}
            ep = en_paras[i] if i < len(en_paras) else {'sec': '', 'text': ''}
            
            zh_text_line = zp['text']
            en_text_line = ep['text']
            sec_zh = zp['sec'] or ep['sec'] or '正文'
            sec_en = ep['sec'] or zp['sec'] or 'Narrative'

            # Speaker check
            speaker = ""
            if zh_text_line.startswith('【') and '】' in zh_text_line:
                speaker_match = re.match(r'【(.*?)】', zh_text_line)
                if speaker_match:
                    speaker = speaker_match.group(1)
            elif en_text_line.startswith('[') and ']' in en_text_line:
                speaker_match = re.match(r'\[(.*?)\]', en_text_line)
                if speaker_match:
                    speaker = speaker_match.group(1)

            cues.append({
                'secZh': sec_zh,
                'secEn': sec_en,
                'speaker': speaker,
                'zh': zh_text_line,
                'en': en_text_line
            })

        # Calculate time weights
        total_weight = 0
        for c in cues:
            # Calculate weight based on character count and word count
            w = max(len(c['zh']) * 1.6, len(c['en'].split()) * 2.0, 5.0)
            c['weight'] = w
            total_weight += w

        # Assign start and end timestamps
        cur_time = 0.0
        duration = zh_dur if zh_dur > 10 else 600.0
        for c in cues:
            cue_dur = (c['weight'] / total_weight) * duration
            c['start'] = round(cur_time, 2)
            cur_time += cue_dur
            c['end'] = round(cur_time, 2)
            del c['weight']

        # Ensure last cue ends exactly at duration
        if cues:
            cues[-1]['end'] = round(duration, 2)

        ep_data = {
            'id': ep_id,
            'title': zh_title,
            'enTitle': f'Episode {ep_id}: {en_title}',
            'summary': f'{ep_name} · 双语沉浸式有声剧场',
            'audioZh': zh_mp3,
            'audioEn': en_mp3,
            'durationZh': round(zh_dur, 2),
            'durationEn': round(en_dur, 2),
            'cues': cues
        }
        all_episodes_data.append(ep_data)
        print(f"Processed Episode {ep_id}: {zh_title} | {len(cues)} cues | ZH: {round(zh_dur,1)}s | EN: {round(en_dur,1)}s")

    # Output JS file
    output_js = os.path.join(BASE_DIR, 'audio_data.js')
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write("/* Auto-generated Bilingual Subtitle & Episode Database for TSMC Morris Chang Parallel World */\n")
        f.write("window.EPISODES_DATA = ")
        f.write(json.dumps(all_episodes_data, ensure_ascii=False, indent=2))
        f.write(";\n")

    print(f"\nSuccessfully wrote {len(all_episodes_data)} episodes to {output_js}")

if __name__ == '__main__':
    process_all_episodes()
