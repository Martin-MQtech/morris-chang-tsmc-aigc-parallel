import os
import json
import re
import html
import subprocess
from bs4 import BeautifulSoup

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
    pure_zh_chars = len(re.findall(r'[\u4e00-\u9fff0-9a-zA-Z]', zh_text))
    if pure_zh_chars == 0:
        en_words = len(en_text.split())
        vocal_time = en_words / 2.8 if en_words > 0 else 1.0
    else:
        vocal_time = pure_zh_chars / 3.82

    p_count = len(re.findall(r'[。！？!?\.]', zh_text))
    p_pause = p_count * 0.85

    c_count = len(re.findall(r'[，、；,;]', zh_text))
    c_pause = c_count * 0.38

    d_count = len(re.findall(r'[———：:\-]', zh_text))
    d_pause = d_count * 0.55

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

# Load existing metadata from episode HTML files
episodes_meta = []

ep_config = [
    {
        "id": "10",
        "file_name": "episode-10.html",
        "folder": "第10期-从台湾到世界",
        "act_tag": "ACT 10 · 1995–1998 · 新竹至纽约",
        "title_zh": "第 10 期：从台湾到世界",
        "title_en": "Episode 10: From Taiwan to the World",
        "time_loc": "1995–1998 · 新竹至纽约",
        "tagline_zh": "当风暴来时，扎实的企业反而被看见。亚洲金融风暴里，一家台湾公司站上了世界舞台。",
        "tagline_en": "When storms hit, solid companies stand out. Amidst the Asian Financial Crisis, a Taiwanese firm stepped onto the world stage.",
        "pills": [
            ("历史坐标", "纽交所上市 · 亚洲金融风暴 · 国际化资本 · 全球客户信赖"),
            ("有声轨", "中英双轨 19min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第10期-从台湾到世界.png",
        "prev_link": "episode-09.html",
        "prev_label": "← 上一期：第 09 期 纯代工的革命",
        "next_link": "episode-11.html",
        "next_label": "下一期：第 11 期 记忆体的诱惑 →",
        "quote_zh": "当风暴来时，扎实的企业反而被看见。亚洲金融风暴里，一家台湾公司站上了世界舞台。",
        "quote_en": "When storms hit, solid companies stand out. Amidst the Asian Financial Crisis, a Taiwanese firm stepped onto the world stage."
    },
    {
        "id": "11",
        "file_name": "episode-11.html",
        "folder": "第11期-记忆体的诱惑",
        "act_tag": "ACT 11 · 1998–2000 · 新竹至首尔",
        "title_zh": "第 11 期：记忆体的诱惑",
        "title_en": "Episode 11: The Temptation of Memory",
        "time_loc": "1998–2000 · 新竹至首尔",
        "tagline_zh": "诱惑之所以是诱惑，是因为它长得像机会。真正的强者，是在狂欢里还能听见周期钟声的人。",
        "tagline_en": "Temptation is tempting because it looks like opportunity. The truly strong are those who hear the cycle's bell even amidst celebration.",
        "pills": [
            ("历史坐标", "DRAM周期泡沫 · 拒绝DRAM代工 · 坚守纯代工逻辑 · 跨越周期陷阱"),
            ("有声轨", "中英双轨 21min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第11期-记忆体的诱惑.png",
        "prev_link": "episode-10.html",
        "prev_label": "← 上一期：第 10 期 从台湾到世界",
        "next_link": "episode-12.html",
        "next_label": "下一期：第 12 期 逆周期的定力 →",
        "quote_zh": "诱惑之所以是诱惑，是因为它长得像机会。真正的强者，是在狂欢里还能听见周期钟声的人。",
        "quote_en": "Temptation is tempting because it looks like opportunity. The truly strong are those who hear the cycle's bell even amidst celebration."
    },
    {
        "id": "12",
        "file_name": "episode-12.html",
        "folder": "第12期-逆周期的定力",
        "act_tag": "ACT 12 · 2001–2003 · 互联网泡沫破裂",
        "title_zh": "第 12 期：逆周期的定力",
        "title_en": "Episode 12: The Resolve Against Cycles",
        "time_loc": "2001–2003 · 互联网泡沫破裂",
        "tagline_zh": "周期不是用来恐惧的，是用来踩节奏的；定力，是一个领导者最昂贵的资产。",
        "tagline_en": "Cycles are not for fear, but for setting the pace; resolve is a leader's most precious asset.",
        "pills": [
            ("历史坐标", "Dot-com泡沫破裂 · 0.13微米铜制程破局 · 逆势扩产资本开支 · 甩开联电"),
            ("有声轨", "中英双轨 18min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第12期-逆周期的定力.png",
        "prev_link": "episode-11.html",
        "prev_label": "← 上一期：第 11 期 记忆体的诱惑",
        "next_link": "episode-13.html",
        "next_label": "下一期：第 13 期 交棒之痛 →",
        "quote_zh": "周期不是用来恐惧的，是用来踩节奏的；定力，是一个领导者最昂贵的资产。",
        "quote_en": "Cycles are not for fear, but for setting the pace; resolve is a leader's most precious asset."
    },
    {
        "id": "13",
        "file_name": "episode-13.html",
        "folder": "第13期-交棒之痛",
        "act_tag": "ACT 13 · 2003–2009 · 继承人与金融海啸",
        "title_zh": "第 13 期：交棒之痛",
        "title_en": "Episode 13: The Pain of Succession",
        "time_loc": "2003–2009 · 继承人与金融海啸",
        "tagline_zh": "把权力交出去需要勇气，把它拿回来需要更大的勇气——而两次，都是为了同一家公司。",
        "tagline_en": "Surrendering power takes courage; reclaiming it demands even greater bravery—and both times, for the very same company.",
        "pills": [
            ("历史坐标", "首次交棒CEO · 2008全球金融海啸 · 裁员风波与危机 · 78岁归来前夜"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第13期-交棒之痛.png",
        "prev_link": "episode-12.html",
        "prev_label": "← 上一期：第 12 期 逆周期的定力",
        "next_link": "episode-14.html",
        "next_label": "下一期：第 14 期 绚烂年代 →",
        "quote_zh": "把权力交出去需要勇气，把它拿回来需要更大的勇气——而两次，都是为了同一家公司。",
        "quote_en": "Surrendering power takes courage; reclaiming it demands even greater bravery—and both times, for the very same company."
    },
    {
        "id": "14",
        "file_name": "episode-14.html",
        "folder": "第14期-绚烂年代",
        "act_tag": "ACT 14 · 2009–2012 · 78岁重披战袍",
        "title_zh": "第 14 期：绚烂年代",
        "title_en": "Episode 14: The Resplendent Era",
        "time_loc": "2009–2012 · 78岁重披战袍",
        "tagline_zh": "老骥伏枥，志在千里。年龄从不决定一个人还能不能战斗，只决定他敢不敢再上战场。",
        "tagline_en": "Age never decides if one can still fight, only whether one dares to enter the battlefield again.",
        "pills": [
            ("历史坐标", "2009重任CEO · 召回离职员工 · 资本支出倍增至59亿美元 · 28纳米制霸"),
            ("有声轨", "中英双轨 18min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第14期-绚烂年代.png",
        "prev_link": "episode-13.html",
        "prev_label": "← 上一期：第 13 期 交棒之痛",
        "next_link": "episode-15.html",
        "next_label": "下一期：第 15 期 苹果来敲门 →",
        "quote_zh": "老骥伏枥，志在千里。年龄从不决定一个人还能不能战斗，只决定他敢不敢再上战场。",
        "quote_en": "Age never decides if one can still fight, only whether one dares to enter the battlefield again."
    },
    {
        "id": "15",
        "file_name": "episode-15.html",
        "folder": "第15期-苹果来敲门",
        "act_tag": "ACT 15 · 2010–2014 · 库克、郭台铭与iPhone之约",
        "title_zh": "第 15 期：苹果来敲门",
        "title_en": "Episode 15: Apple Comes Knocking",
        "time_loc": "2010–2014 · 库克、郭台铭与iPhone之约",
        "tagline_zh": "最挑剔的客户，是最好的磨刀石——它逼你长出别人没有的能力。",
        "tagline_en": "The most demanding client is the finest whetstone—forcing you to forge capabilities no one else possesses.",
        "pills": [
            ("历史坐标", "秘密赴美会见库克 · 郭台铭引荐 · A8芯片全代工 · 甩开三星垄断"),
            ("有声轨", "中英双轨 18min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第15期-苹果来敲门.png",
        "prev_link": "episode-14.html",
        "prev_label": "← 上一期：第 14 期 绚烂年代",
        "next_link": "episode-16.html",
        "next_label": "下一期：第 16 期 摩尔定律的守卫者 →",
        "quote_zh": "最挑剔的客户，是最好的磨刀石——它逼你长出别人没有的能力。",
        "quote_en": "The most demanding client is the finest whetstone—forcing you to forge capabilities no one else possesses."
    },
    {
        "id": "16",
        "file_name": "episode-16.html",
        "folder": "第16期-摩尔定律的守卫者",
        "act_tag": "ACT 16 · 2014–2018 · 7纳米与EUV终局之战",
        "title_zh": "第 16 期：摩尔定律的守卫者",
        "title_en": "Episode 16: Guardians of Moore's Law",
        "time_loc": "2014–2018 · 7纳米与EUV终局之战",
        "tagline_zh": "当摩尔定律开始变老，全世界都在问「还要不要追」——他用十年回答：追，而且要追到只剩你一个。",
        "tagline_en": "As Moore's Law aged and the world wondered whether to keep chasing—his decade-long answer: chase, until only you remain.",
        "pills": [
            ("历史坐标", "夜鹰计划24小时研发 · EUV极紫外光刻首秀 · 7纳米超越英特尔 · 全球技术登顶"),
            ("有声轨", "中英双轨 18min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第16期-摩尔定律的守卫者.png",
        "prev_link": "episode-15.html",
        "prev_label": "← 上一期：第 15 期 苹果来敲门",
        "next_link": "episode-17.html",
        "next_label": "下一期：第 17 期 交棒与退休 →",
        "quote_zh": "当摩尔定律开始变老，全世界都在问「还要不要追」——他用十年回答：追，而且要追到只剩你一个。",
        "quote_en": "As Moore's Law aged and the world wondered whether to keep chasing—his decade-long answer: chase, until only you remain."
    },
    {
        "id": "17",
        "file_name": "episode-17.html",
        "folder": "第17期-交棒与退休",
        "act_tag": "ACT 17 · 2013–2018 · 双首长制与贝多芬第九",
        "title_zh": "第 17 期：交棒与退休",
        "title_en": "Episode 17: Succession and Farewell",
        "time_loc": "2013–2018 · 双首长制与贝多芬第九",
        "tagline_zh": "真正的传承，不是找一个像自己的人，而是把公司交给一套比个人更持久的制度。",
        "tagline_en": "True succession is not finding a clone of oneself, but entrusting the enterprise to an enduring institutional system.",
        "pills": [
            ("历史坐标", "双首长制设计（刘德音+魏哲家） · 贝多芬第九交响曲告别 · 87岁功成身退 · 传承典范"),
            ("有声轨", "中英双轨 18min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第17期-交棒与退休.png",
        "prev_link": "episode-16.html",
        "prev_label": "← 上一期：第 16 期 摩尔定律的守卫者",
        "next_link": "episode-18.html",
        "next_label": "下一期：第 18 期 护国神山 →",
        "quote_zh": "真正的传承，不是找一个像自己的人，而是把公司交给一套比个人更持久的制度。",
        "quote_en": "True succession is not finding a clone of oneself, but entrusting the enterprise to an enduring institutional system."
    },
    {
        "id": "18",
        "file_name": "episode-18.html",
        "folder": "第18期-护国神山",
        "act_tag": "ACT 18 · 2018–今天 · 地缘政治、AI革命与世纪收官",
        "title_zh": "第 18 期：护国神山",
        "title_en": "Episode 18: The Sacred Silicon Mountain",
        "time_loc": "2018–今天 · 地缘政治、AI革命与世纪收官",
        "tagline_zh": "一座「护国神山」，从来不是一个人搬上去的，而是一代人的选择，被时间砌成了山。",
        "tagline_en": "A sacred mountain is never carried up by one man alone; it is the choices of a generation, mortared into a peak by time.",
        "pills": [
            ("历史坐标", "地缘政治必争之地 · 亚利桑那与熊本建厂 · AI算力中心 · 终局回望与世纪答卷"),
            ("有声轨", "中英双轨 18min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第18期-护国神山.png",
        "prev_link": "episode-17.html",
        "prev_label": "← 上一期：第 17 期 交棒与退休",
        "next_link": "index.html",
        "next_label": "回到全册总目录 (18期大结局) →",
        "quote_zh": "一座「护国神山」，从来不是一个人搬上去的，而是一代人的选择，被时间砌成了山。",
        "quote_en": "A sacred mountain is never carried up by one man alone; it is the choices of a generation, mortared into a peak by time."
    }
]

# Extract vocab and timeline from existing HTML files for high quality
for ep in ep_config:
    ep_num = int(ep["id"])
    fn = f"episode-{ep_num}.html"
    if os.path.exists(os.path.join(WORKSPACE, fn)):
        with open(os.path.join(WORKSPACE, fn), "r", encoding="utf-8") as f:
            html_text = f.read()
        soup = BeautifulSoup(html_text, "html.parser")
        
        vocab = []
        for card in soup.find_all("div", class_="vocab-card"):
            word = card.find("span", class_="vocab-word")
            ph = card.find("span", class_="vocab-phonetic")
            zh = card.find("div", class_="vocab-zh")
            en = card.find("div", class_="vocab-en")
            if word and zh:
                vocab.append((
                    word.text.strip(),
                    ph.text.strip() if ph else "",
                    zh.text.strip() if zh else "",
                    en.text.strip() if en else ""
                ))
        ep["vocab"] = vocab
        
        tl = []
        for item in soup.find_all("div", class_="tl-item"):
            yr = item.find("div", class_="tl-year")
            desc = item.find("div", class_="tl-desc")
            if yr and desc:
                tl.append((yr.text.strip(), desc.text.strip()))
        ep["timeline"] = tl

# Load audio_data.js
with open(os.path.join(WORKSPACE, "audio_data.js"), "r", encoding="utf-8") as f:
    audio_js_text = f.read()

# Extract existing audio_data JSON
match_json = re.search(r'const\s+AUDIO_EPISODES\s*=\s*(\[.*\])\s*;?\s*$', audio_js_text, re.DOTALL)
if not match_json:
    match_json = re.search(r'window\.AUDIO_DATA\s*=\s*(\[.*\])\s*;?\s*$', audio_js_text, re.DOTALL)
if not match_json:
    # find array
    start_bracket = audio_js_text.find('[')
    end_bracket = audio_js_text.rfind(']')
    audio_episodes_data = json.loads(audio_js_text[start_bracket:end_bracket+1])
else:
    audio_episodes_data = json.loads(match_json.group(1))

print(f"Loaded audio_data.js with {len(audio_episodes_data)} episodes.")

# Process episodes 10-18
all_new_cues_by_ep = {}

for ep in ep_config:
    ep_id = ep["id"]
    folder_path = os.path.join(WORKSPACE, "03-剧集", ep["folder"])
    zh_path = os.path.join(folder_path, "中文文字稿.md")
    en_path = os.path.join(folder_path, "英文文字稿.md")
    mp3_zh_path = os.path.join(AUDIO_DIR, f"ep{ep_id}-zh.mp3")
    mp3_en_path = os.path.join(AUDIO_DIR, f"ep{ep_id}-en.mp3")
    
    real_zh_dur = get_mp3_duration(mp3_zh_path)
    real_en_dur = get_mp3_duration(mp3_en_path)
    
    m_val = int(real_zh_dur // 60)
    s_val = int(real_zh_dur % 60)
    ep["duration"] = f"{m_val:02d}:{s_val:02d}"
    
    zh_sections = parse_markdown_sections(zh_path)
    en_sections = parse_markdown_sections(en_path)
    
    # Flatten paragraphs to generate cues
    cues_raw = []
    for s_idx, (sec_title, paras) in enumerate(zh_sections):
        en_sec_title = en_sections[s_idx][0] if s_idx < len(en_sections) else ""
        en_paras = en_sections[s_idx][1] if s_idx < len(en_sections) else []
        
        for p_idx, p_zh in enumerate(paras):
            p_en = en_paras[p_idx] if p_idx < len(en_paras) else ""
            
            speaker = ""
            if p_zh.startswith('【') and '】' in p_zh:
                m = re.match(r'【(.*?)】', p_zh)
                if m: speaker = m.group(1)
            elif p_en.startswith('[') and ']' in p_en:
                m = re.match(r'\[(.*?)\]', p_en)
                if m: speaker = m.group(1)
                
            raw_dur = compute_raw_cue_duration(p_zh, p_en, is_section_header=(p_idx==0))
            
            cues_raw.append({
                "secZh": sec_title,
                "secEn": en_sec_title,
                "speaker": speaker,
                "zh": p_zh,
                "en": p_en,
                "raw_dur": raw_dur
            })
            
    # Apply Acoustic Timing Model scaling to match real MP3 duration exactly
    total_raw_dur = sum(c["raw_dur"] for c in cues_raw)
    scale_factor = real_zh_dur / total_raw_dur if total_raw_dur > 0 else 1.0
    
    cur_t = 0.0
    final_cues = []
    for i, c in enumerate(cues_raw):
        dur = c["raw_dur"] * scale_factor
        start_t = round(cur_t, 2)
        end_t = round(cur_t + dur, 2)
        if i == len(cues_raw) - 1:
            end_t = round(real_zh_dur, 2)
            
        cur_t += dur
        final_cues.append({
            "secZh": c["secZh"],
            "secEn": c["secEn"],
            "speaker": c["speaker"],
            "zh": c["zh"],
            "en": c["en"],
            "start": start_t,
            "end": end_t
        })
        
    all_new_cues_by_ep[ep_id] = final_cues
    print(f"Ep {ep_id}: {len(final_cues)} cues calibrated against {real_zh_dur:.2f}s audio (scale={scale_factor:.4f})")

# Update audio_episodes_data
for ep_data in audio_episodes_data:
    ep_id = str(ep_data.get("id", "")).zfill(2)
    if ep_id in all_new_cues_by_ep:
        ep_data["cues"] = all_new_cues_by_ep[ep_id]
        ep_data["durationZh"] = get_mp3_duration(os.path.join(AUDIO_DIR, f"ep{ep_id}-zh.mp3"))
        ep_data["durationEn"] = get_mp3_duration(os.path.join(AUDIO_DIR, f"ep{ep_id}-en.mp3"))

# Write updated audio_data.js
new_audio_js = f"window.AUDIO_DATA = {json.dumps(audio_episodes_data, ensure_ascii=False, indent=2)};\n"
with open(os.path.join(WORKSPACE, "audio_data.js"), "w", encoding="utf-8") as f:
    f.write(new_audio_js)
print("Updated audio_data.js successfully.")

# Now regenerate episode-10.html through episode-18.html
for ep in ep_config:
    ep_id = ep["id"]
    cues = all_new_cues_by_ep[ep_id]
    
    folder_path = os.path.join(WORKSPACE, "03-剧集", ep["folder"])
    zh_path = os.path.join(folder_path, "中文文字稿.md")
    en_path = os.path.join(folder_path, "英文文字稿.md")
    
    zh_sections = parse_markdown_sections(zh_path)
    en_sections = parse_markdown_sections(en_path)
    
    pills_html = "".join([f'<span class="pill"><b>{k}：</b>{v}</span>' for k, v in ep["pills"]])
    
    # Cues rows HTML for teleprompter
    cues_rows_html = []
    for i, cue in enumerate(cues):
        start_sec = cue.get("start", 0.0)
        end_sec = cue.get("end", 0.0)
        m_val = int(start_sec // 60)
        s_val = int(start_sec % 60)
        time_str = f"{m_val:02d}:{s_val:02d}"
        
        zh_text = cue.get("zh", "")
        en_text = cue.get("en", "")
        
        cues_rows_html.append(f"""
          <div class="sub-row" id="sub-row-{i}" data-index="{i}" data-start="{start_sec:.2f}" data-end="{end_sec:.2f}" onclick="seekAndPlay({start_sec:.2f})">
            <span class="sub-time-tag">{time_str}</span>
            <div class="sub-content">
              <div class="sub-zh">{html.escape(zh_text)}</div>
              <div class="sub-en">{html.escape(en_text)}</div>
            </div>
          </div>
        """)
    cues_scroll_html = "\n".join(cues_rows_html)
    
    # Dual Book Sections HTML
    book_sections_html = []
    cue_idx = 0
    
    for s_idx, (sec_title, paras) in enumerate(zh_sections):
        en_sec_title = en_sections[s_idx][0] if s_idx < len(en_sections) else ""
        en_paras = en_sections[s_idx][1] if s_idx < len(en_sections) else []
        
        sec_paras_html = []
        for p_idx, p_zh in enumerate(paras):
            p_en = en_paras[p_idx] if p_idx < len(en_paras) else ""
            
            time_tag = "00:00"
            start_time = 0.0
            if cue_idx < len(cues):
                start_time = cues[cue_idx].get("start", 0.0)
                m_val = int(start_time // 60)
                s_val = int(start_time % 60)
                time_tag = f"{m_val:02d}:{s_val:02d}"
                c_idx = cue_idx
                cue_idx += 1
            else:
                c_idx = max(0, len(cues) - 1)
                
            is_sfx = "【音效" in p_zh or "[SFX" in p_en or "【主叙述者】" in p_zh or "【Morris】" in p_zh
            sfx_class = " sfx-row" if is_sfx else ""
            
            sec_paras_html.append(f"""
              <div class="bilingual-para{sfx_class}" id="para-{c_idx}" onclick="seekAndPlay({start_time:.2f})">
                <span class="para-time-badge">{time_tag}</span>
                <div class="para-content">
                  <p class="zh-para">{html.escape(p_zh)}</p>
                  <p class="en-para">{html.escape(p_en)}</p>
                </div>
              </div>
            """)
            
        sec_tag_num = f"ACT {s_idx + 1:02d}" if "幕" in sec_title or "Act" in sec_title else "SECTION"
        book_sections_html.append(f"""
          <section class="book-section">
            <div class="book-section-header">
              <span class="section-tag">{sec_tag_num}</span>
              <h2 class="serif">{html.escape(sec_title)}<span class="en">{html.escape(en_sec_title)}</span></h2>
            </div>
            <div class="section-body">
              {"".join(sec_paras_html)}
            </div>
          </section>
        """)
        
    book_body_html = "\n".join(book_sections_html)
    
    # Vocab cards HTML
    vocab_cards_html = []
    for w, ph, zh_def, en_def in ep["vocab"]:
        vocab_cards_html.append(f"""
          <div class="vocab-card">
            <div class="vocab-word-row">
              <span class="vocab-word">{html.escape(w)}</span>
              <span class="vocab-phonetic">{html.escape(ph)}</span>
              <button class="btn-pronounce" onclick="pronounceWord('{html.escape(w)}')" title="点击发音">🔊</button>
            </div>
            <div class="vocab-zh">{html.escape(zh_def)}</div>
            <div class="vocab-en">{html.escape(en_def)}</div>
          </div>
        """)
    vocab_html = "\n".join(vocab_cards_html)
    
    # Timeline HTML
    tl_items_html = []
    for yr, desc in ep["timeline"]:
        tl_items_html.append(f"""
          <div class="tl-item">
            <div class="tl-year">{html.escape(yr)}</div>
            <div class="tl-desc">{html.escape(desc)}</div>
          </div>
        """)
    timeline_html = "\n".join(tl_items_html)
    
    # Hero Split Grid
    hero_grid_html = f'''      <div class="hero-split-grid">
        <div class="hero-left-col">
          <div class="tagline-box" style="margin-top: 0;">
            <div class="tagline-zh">“{ep["tagline_zh"]}”</div>
            <div class="tagline-en">"{ep["tagline_en"]}"</div>
          </div>
        </div>

        <div class="hero-right-col">
          <figure class="lead-artwork-figure">
            <img class="lead-artwork-img" src="{ep["image_path"]}" alt="{ep["title_zh"]} 概念插画" loading="lazy">
          </figure>
        </div>
      </div>'''

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{ep["title_zh"]} ({ep["time_loc"]}) | 台积电张忠谋 · 传记时间线的平行世界</title>
<meta name="description" content="台积电张忠谋传记时间线的平行世界 · {ep["title_zh"]}（{ep["time_loc"]}）。纯净双语典藏电子书，中英双语原声有声剧场，逐句同步高亮字幕，时代历史坐标与双语精读笔记。">

<!-- Open Graph / Facebook / LinkedIn -->
<meta property="og:type" content="article">
<meta property="og:title" content="《台积电张忠谋：{ep["title_zh"]} ({ep["time_loc"]})》· 传记时间线的平行世界">
<meta property="og:description" content="{ep["duration"]}分钟双语原声TTS + 逐句同步字幕 + 商业深度复盘。同一时间线，另一个视角。">
<meta property="og:image" content="https://martin-mqtech.github.io/morris-chang-tsmc-aigc-parallel/{ep["image_path"].replace('./', '')}">
<meta property="og:url" content="https://martin-mqtech.github.io/morris-chang-tsmc-aigc-parallel/{ep["file_name"]}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="《台积电张忠谋：{ep["title_zh"]} ({ep["time_loc"]})》· 传记时间线的平行世界">
<meta name="twitter:description" content="{ep["duration"]}分钟双语原声TTS + 逐句同步字幕 + 商业深度复盘。同一时间线，另一个视角。">
<meta name="twitter:image" content="https://martin-mqtech.github.io/morris-chang-tsmc-aigc-parallel/{ep["image_path"].replace('./', '')}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0a0a0a;
    --bg2: #111113;
    --card: #16161a;
    --line: #26262b;
    --amber: #F59E0B;
    --blue: #38BDF8;
    --ink: #ece9e2;
    --muted: #a29c90;
    --serif: "Songti SC", "Noto Serif SC", "STSong", Georgia, serif;
    --sans: "PingFang SC", "Microsoft YaHei", -apple-system, "Segoe UI", Roboto, sans-serif;
    --en: "Georgia", "Times New Roman", serif;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; background: var(--bg); color: var(--ink); font-family: var(--sans); -webkit-font-smoothing: antialiased; }}
  body {{ min-height: 100vh; line-height: 1.8; overflow-x: hidden; padding-bottom: 60px; }}

  /* Top Navigation */
  .nav {{ position: sticky; top: 0; z-index: 100; background: rgba(10,10,10,0.88); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); height: 60px; display: flex; align-items: center; justify-content: space-between; padding: 0 6vw; }}
  .brand {{ display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--ink); font-weight: 700; font-size: 15px; letter-spacing: 0.5px; }}
  .brand-logo-img {{ width: 32px; height: 32px; border-radius: 50%; display: inline-block; vertical-align: middle; box-shadow: 0 0 10px rgba(255, 255, 255, 0.2); border: 1px solid #333; transition: transform 0.3s ease, box-shadow 0.3s ease; flex-shrink: 0; }}
  .brand:hover .brand-logo-img {{ transform: scale(1.08) rotate(4deg); box-shadow: 0 0 16px rgba(255, 255, 255, 0.35); border-color: #555; }}
  .nav-links {{ display: flex; align-items: center; gap: 20px; }}
  .nav-link {{ color: var(--muted); text-decoration: none; font-size: 13.5px; transition: color 0.2s; }}
  .nav-link:hover, .nav-link.active {{ color: var(--amber); }}
  .nav-badge {{ background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); color: var(--amber); font-size: 11px; padding: 2px 8px; border-radius: 999px; font-weight: 600; }}

  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 6vw; }}
  .article-wrap {{ max-width: 880px; margin: 0 auto; padding: 0 5vw; }}

  /* Hero Section - 50/50 Balanced Split */
  .hero-ep {{ padding: 36px 0 28px; border-bottom: 1px solid var(--line); background: radial-gradient(800px 400px at 80% -10%, rgba(245,158,11,0.08), transparent 60%), radial-gradient(700px 350px at 10% 110%, rgba(56,189,248,0.06), transparent 60%); }}
  .eyebrow {{ font-size: 12px; letter-spacing: 3px; text-transform: uppercase; color: var(--amber); display: block; margin-bottom: 12px; font-weight: 600; }}
  .eyebrow em {{ font-family: var(--en); font-style: italic; letter-spacing: 2px; margin-left: 8px; color: var(--blue); }}
  h1.serif {{ font-family: var(--serif); font-size: clamp(23px, 3.2vw, 32px); font-weight: 700; line-height: 1.25; color: var(--ink); margin-bottom: 10px; letter-spacing: 0.5px; }}
  h1.serif .en {{ display: block; font-family: var(--en); font-size: clamp(14px, 1.8vw, 17px); font-style: italic; font-weight: 400; color: var(--muted); margin-top: 6px; }}
  
  /* Hero Split Grid (50/50 Balanced Split) */
  .hero-split-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 36px;
    align-items: center;
    margin-top: 18px;
  }}
  @media (max-width: 820px) {{
    .hero-split-grid {{
      grid-template-columns: 1fr;
      gap: 20px;
    }}
  }}
  .hero-left-col {{
    max-width: 480px;
  }}
  .hero-right-col {{
    width: 100%;
  }}
  .lead-artwork-figure {{
    margin: 0;
    width: 100%;
    border: 1px solid var(--line);
    border-radius: 16px;
    overflow: hidden;
    background: var(--card);
    box-shadow: 0 18px 48px rgba(0,0,0,0.55);
  }}
  .lead-artwork-img {{
    width: 100%;
    height: auto;
    max-height: 290px;
    object-fit: cover;
    object-position: center 20%;
    display: block;
    transition: transform 0.5s ease;
  }}
  .lead-artwork-figure:hover .lead-artwork-img {{
    transform: scale(1.03);
  }}

  .tagline-box {{ background: var(--bg2); border-left: 4px solid var(--amber); border-radius: 0 12px 12px 0; padding: 16px 20px; border-top: 1px solid var(--line); border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); }}
  .tagline-zh {{ font-family: var(--serif); font-size: 15px; color: var(--ink); line-height: 1.65; }}
  .tagline-en {{ font-family: var(--en); font-style: italic; color: var(--muted); font-size: 13.5px; margin-top: 6px; }}

  /* Meta Pills below player */
  .meta-pills {{ display: flex; flex-wrap: wrap; gap: 8px; margin: -16px 0 32px 0; }}
  .pill {{ font-size: 11.5px; color: var(--muted); background: var(--card); border: 1px solid var(--line); padding: 5px 12px; border-radius: 999px; display: inline-flex; align-items: center; gap: 4px; }}
  .pill b {{ color: var(--ink); font-weight: 600; }}

  /* Audio Player Module */
  .player-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: 22px; margin: 28px 0 32px; box-shadow: 0 20px 50px rgba(0,0,0,0.6); position: relative; overflow: hidden; }}
  .player-card::before {{ content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--amber), var(--blue)); }}
  
  /* Layout Architecture for .track-switcher */
  .track-switcher {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 18px;
    border-bottom: 1px solid var(--line);
    padding-bottom: 14px;
    flex-wrap: nowrap;
    overflow-x: auto;
  }}
  .track-switcher::-webkit-scrollbar {{ display: none; }}

  .track-btns {{
    display: flex;
    gap: 8px;
    flex-shrink: 0;
  }}
  .btn-track {{
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 6px 14px;
    border-radius: 10px;
    font-size: 12.5px;
    line-height: 1.25;
    cursor: pointer;
    border: 1px solid var(--line);
    background: var(--bg2);
    color: var(--muted);
    transition: all 0.2s;
  }}
  .btn-track span.title-line {{ font-weight: 600; }}
  .btn-track span.sub-line {{ font-family: var(--en); font-style: italic; font-size: 10.5px; opacity: 0.85; margin-top: 1px; }}
  .btn-track.active {{
    background: var(--amber);
    color: #000;
    border-color: var(--amber);
  }}
  .btn-track.active span.sub-line {{ color: #1a1205; }}
  .btn-track:hover:not(.active) {{ border-color: var(--amber); color: var(--amber); transform: translateY(-1px); }}

  /* 8-Channel Share Bar in the parallel space on the same line */
  .share-matrix-inline {{
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }}
  .share-label {{
    font-size: 11px;
    letter-spacing: 1px;
    color: var(--muted);
    font-family: var(--en);
    font-style: italic;
    margin-right: 2px;
    white-space: nowrap;
  }}
  .btn-share {{
    padding: 5px 9px;
    border-radius: 6px;
    border: 1px solid var(--line);
    background: var(--bg2);
    color: var(--ink);
    font-size: 11px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    transition: all 0.2s;
    white-space: nowrap;
  }}
  .btn-share:hover {{
    border-color: var(--amber);
    color: var(--amber);
    transform: translateY(-1px);
  }}

  .player-main-ctrl {{ background: var(--bg2); border: 1px solid var(--line); border-radius: 14px; padding: 16px 20px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 18px; }}
  .ctrl-left {{ display: flex; align-items: center; gap: 16px; min-width: 240px; }}
  .play-btn {{ width: 48px; height: 48px; border-radius: 50%; background: var(--amber); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #000; font-size: 20px; font-weight: bold; transition: all 0.2s; box-shadow: 0 4px 16px rgba(245,158,11,0.3); }}
  .play-btn:hover {{ transform: scale(1.08); background: #fbb028; }}
  
  .track-meta {{ display: flex; flex-direction: column; }}
  .track-meta-title {{ font-size: 14.5px; font-weight: 600; color: var(--ink); }}
  .track-meta-sub {{ font-size: 12px; color: var(--muted); font-family: var(--en); font-style: italic; }}

  .progress-container {{ display: flex; align-items: center; gap: 12px; flex-grow: 1; min-width: 260px; }}
  .time-text {{ font-size: 12px; color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; min-width: 44px; text-align: center; }}
  .seek-bar {{ flex-grow: 1; accent-color: var(--amber); cursor: pointer; height: 5px; background: var(--line); border-radius: 4px; outline: none; }}

  .playback-options {{ display: flex; align-items: center; gap: 10px; }}
  .speed-select {{ background: var(--card); border: 1px solid var(--line); color: var(--ink); border-radius: 6px; padding: 5px 8px; font-size: 12px; cursor: pointer; outline: none; }}
  .speed-select:focus {{ border-color: var(--amber); }}

  /* Subtitles Viewport */
  .teleprompter-box {{ margin-top: 22px; }}
  .teleprompter-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; padding: 0 4px; }}
  .teleprompter-title {{ font-size: 11.5px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); font-weight: 600; display: flex; align-items: center; gap: 8px; }}
  .teleprompter-title b {{ color: var(--amber); font-weight: normal; }}
  .teleprompter-tools {{ display: flex; align-items: center; gap: 12px; font-size: 12px; color: var(--muted); }}
  .btn-toggle-scroll {{ cursor: pointer; background: transparent; border: 1px solid var(--line); color: var(--muted); padding: 3px 10px; border-radius: 999px; font-size: 11px; }}
  .btn-toggle-scroll.active {{ border-color: var(--amber); color: var(--amber); }}

  .subtitles-scroll {{ max-height: 290px; overflow-y: auto; display: flex; flex-direction: column; gap: 6px; padding: 4px 6px 4px 0; scroll-behavior: smooth; border: 1px solid var(--line); border-radius: 12px; background: var(--bg2); }}
  .subtitles-scroll::-webkit-scrollbar {{ width: 6px; }}
  .subtitles-scroll::-webkit-scrollbar-track {{ background: var(--bg2); }}
  .subtitles-scroll::-webkit-scrollbar-thumb {{ background: #333; border-radius: 3px; }}
  .subtitles-scroll::-webkit-scrollbar-thumb:hover {{ background: #444; }}

  .sub-row {{ display: flex; gap: 14px; padding: 10px 14px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; border-left: 3px solid transparent; }}
  .sub-row:hover {{ background: rgba(255,255,255,0.03); }}
  .sub-row.active {{ background: rgba(245,158,11,0.09); border-left-color: var(--amber); }}
  .sub-time-tag {{ font-size: 11px; font-family: monospace; color: var(--muted); padding-top: 2px; min-width: 38px; }}
  .sub-row.active .sub-time-tag {{ color: var(--amber); font-weight: bold; }}
  .sub-content {{ flex-grow: 1; }}
  .sub-zh {{ font-size: 14px; line-height: 1.6; color: var(--ink); font-family: var(--serif); }}
  .sub-en {{ font-size: 12.5px; line-height: 1.5; color: var(--muted); font-family: var(--en); font-style: italic; margin-top: 2px; }}
  .sub-row.active .sub-zh {{ color: #fff; font-weight: 600; }}
  .sub-row.active .sub-en {{ color: var(--amber); }}

  /* Dual Layout Body (75% Pure Book + 25% Learning & Notes) */
  .content-grid {{ display: grid; grid-template-columns: 1fr 320px; gap: 40px; margin-top: 20px; }}
  @media (max-width: 980px) {{
    .content-grid {{ grid-template-columns: 1fr; }}
  }}

  /* 75% Pure Bilingual Book */
  .book-main {{ min-width: 0; }}
  .book-section {{ margin-bottom: 48px; border-bottom: 1px solid var(--line); padding-bottom: 36px; }}
  .book-section:last-child {{ border-bottom: none; }}
  .book-section-header {{ margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.06); }}
  .section-tag {{ font-size: 11px; letter-spacing: 2.5px; text-transform: uppercase; color: var(--blue); font-weight: 600; display: block; margin-bottom: 4px; }}
  .book-section-header h2.serif {{ font-size: 20px; color: var(--ink); font-weight: 700; }}
  .book-section-header h2.serif .en {{ display: block; font-size: 13.5px; font-family: var(--en); font-style: italic; color: var(--muted); font-weight: 400; margin-top: 3px; }}

  .bilingual-para {{ display: flex; gap: 16px; margin-bottom: 22px; padding: 12px 16px; border-radius: 10px; transition: all 0.2s ease; border-left: 3px solid transparent; cursor: pointer; }}
  .bilingual-para:hover {{ background: rgba(255,255,255,0.025); border-left-color: rgba(245,158,11,0.4); }}
  .bilingual-para.current-reading {{ background: rgba(245,158,11,0.08); border-left-color: var(--amber); }}
  
  .para-time-badge {{ font-size: 10.5px; font-family: monospace; color: var(--muted); padding-top: 3px; min-width: 36px; flex-shrink: 0; opacity: 0.6; }}
  .bilingual-para:hover .para-time-badge, .bilingual-para.current-reading .para-time-badge {{ opacity: 1; color: var(--amber); }}
  
  .para-content {{ flex-grow: 1; }}
  .zh-para {{ font-family: var(--serif); font-size: 15.5px; line-height: 1.85; color: #f0ede6; text-align: justify; margin-bottom: 6px; }}
  .en-para {{ font-family: var(--en); font-style: italic; font-size: 13.5px; line-height: 1.7; color: #a8a398; text-align: justify; }}
  
  .bilingual-para.sfx-row {{ background: rgba(56,189,248,0.04); border-radius: 8px; padding: 8px 14px; margin: 16px 0; border-left: 3px solid rgba(56,189,248,0.4); }}
  .bilingual-para.sfx-row .zh-para {{ font-size: 13px; color: var(--blue); font-family: var(--sans); }}
  .bilingual-para.sfx-row .en-para {{ font-size: 12px; color: #7dd3fc; }}

  /* 25% Learning & Knowledge Sidebar */
  .learning-sidebar {{ display: flex; flex-direction: column; gap: 24px; }}
  .side-widget {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 20px; position: sticky; }}
  .widget-title {{ font-size: 13px; font-weight: 700; color: var(--ink); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--line); padding-bottom: 10px; }}
  .widget-title span.icon {{ font-size: 15px; }}

  /* Vocab flashcards */
  .vocab-list {{ display: flex; flex-direction: column; gap: 12px; }}
  .vocab-card {{ background: var(--bg2); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; }}
  .vocab-word-row {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 3px; }}
  .vocab-word {{ font-family: var(--en); font-weight: 700; font-size: 14px; color: var(--amber); }}
  .vocab-phonetic {{ font-size: 11px; color: var(--muted); font-family: var(--sans); margin-left: auto; margin-right: 8px; }}
  .btn-pronounce {{ background: none; border: none; font-size: 12px; cursor: pointer; color: var(--muted); transition: color 0.2s; }}
  .btn-pronounce:hover {{ color: var(--amber); }}
  .vocab-zh {{ font-size: 12.5px; color: var(--ink); font-weight: 500; margin-bottom: 3px; }}
  .vocab-en {{ font-size: 11.5px; color: var(--muted); font-family: var(--en); font-style: italic; line-height: 1.4; }}

  /* Historical Timeline */
  .timeline-list {{ display: flex; flex-direction: column; gap: 14px; position: relative; padding-left: 14px; }}
  .timeline-list::before {{ content: ""; position: absolute; left: 4px; top: 6px; bottom: 6px; width: 2px; background: var(--line); }}
  .tl-item {{ position: relative; }}
  .tl-item::before {{ content: ""; position: absolute; left: -14px; top: 6px; width: 8px; height: 8px; border-radius: 50%; background: var(--amber); border: 2px solid var(--bg); }}
  .tl-year {{ font-size: 11.5px; font-weight: 700; color: var(--amber); font-family: var(--en); margin-bottom: 2px; }}
  .tl-desc {{ font-size: 12px; color: #b8b3a8; line-height: 1.5; }}

  /* Bottom Navigation */
  .ep-footer-nav {{ margin-top: 60px; padding-top: 30px; border-top: 1px solid var(--line); display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }}
  .btn-nav-ep {{ display: inline-flex; align-items: center; gap: 8px; padding: 12px 20px; border-radius: 10px; background: var(--card); border: 1px solid var(--line); color: var(--ink); text-decoration: none; font-size: 13.5px; font-weight: 600; transition: all 0.2s; }}
  .btn-nav-ep:hover {{ border-color: var(--amber); color: var(--amber); transform: translateY(-2px); }}
  .btn-nav-ep.next {{ background: rgba(245,158,11,0.1); border-color: rgba(245,158,11,0.3); color: var(--amber); }}
  .btn-nav-ep.next:hover {{ background: var(--amber); color: #000; }}

  /* Quote banner */
  .quote-banner {{ background: linear-gradient(135deg, rgba(245,158,11,0.06), rgba(56,189,248,0.04)); border: 1px solid var(--line); border-radius: 14px; padding: 24px 28px; margin: 40px 0; text-align: center; }}
  .quote-zh {{ font-family: var(--serif); font-size: 17px; font-weight: 600; color: var(--ink); line-height: 1.7; margin-bottom: 8px; }}
  .quote-en {{ font-family: var(--en); font-style: italic; font-size: 14px; color: var(--muted); }}

  /* Toast Notification */
  .toast-msg {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px); background: rgba(17,17,19,0.95); border: 1px solid var(--amber); color: #fff; padding: 10px 22px; border-radius: 999px; font-size: 13px; font-weight: 500; box-shadow: 0 10px 30px rgba(0,0,0,0.8); z-index: 9999; opacity: 0; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); pointer-events: none; }}
  .toast-msg.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}

  /* WeChat Modal */
  .wechat-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.75); z-index: 10000; align-items: center; justify-content: center; backdrop-filter: blur(6px); }}
  .wechat-modal-box {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 28px 32px; max-width: 380px; width: 90%; text-align: center; position: relative; box-shadow: 0 24px 60px rgba(0,0,0,0.8); }}
  .wechat-modal-close {{ position: absolute; top: 12px; right: 16px; font-size: 22px; color: var(--muted); cursor: pointer; border: none; background: none; }}
  .wechat-modal-title {{ font-size: 16px; font-weight: 700; color: var(--ink); margin-bottom: 12px; }}
  .wechat-modal-desc {{ font-size: 12.5px; color: var(--muted); margin-bottom: 16px; line-height: 1.5; }}
  .wechat-qrcode-wrap {{ background: #fff; padding: 12px; border-radius: 12px; display: inline-block; box-shadow: 0 4px 16px rgba(0,0,0,0.4); margin-bottom: 14px; }}
  .wechat-qrcode-img {{ width: 180px; height: 180px; display: block; }}
</style>
</head>
<body>

  <!-- Navigation -->
  <nav class="nav">
    <a href="index.html" class="brand">
      <img src="logo.svg" alt="Logo" class="brand-logo-img">
      <span>平行张忠谋 · TSMC</span>
    </a>
    <div class="nav-links">
      <a href="index.html" class="nav-link">总目录</a>
      <a href="reader.html" class="nav-link">双语全书</a>
      <a href="map.html" class="nav-link">平行地图</a>
      <a href="cards.html" class="nav-link">金句卡片</a>
      <span class="nav-badge">EP {ep["id"]}</span>
    </div>
  </nav>

  <!-- Hero Header -->
  <header class="hero-ep">
    <div class="wrap">
      <span class="eyebrow">{ep["act_tag"]} <em>EPISODE {ep["id"]}</em></span>
      <h1 class="serif">{ep["title_zh"]}<span class="en">{ep["title_en"]}</span></h1>
      
{hero_grid_html}
    </div>
  </header>

  <!-- Main Workspace -->
  <main class="wrap" style="padding-top: 30px;">

    <!-- Audio Player Module -->
    <div class="player-card">
      <div class="track-switcher">
        <div class="track-btns">
          <button class="btn-track active" id="btn-track-zh" onclick="switchTrack('zh')">
            <span class="title-line">🇨🇳 中文原声剧场</span>
            <span class="sub-line">Chinese Audio · 广播级剧场母带</span>
          </button>
          <button class="btn-track" id="btn-track-en" onclick="switchTrack('en')">
            <span class="title-line">🇺🇸 English Theatre</span>
            <span class="sub-line">English Dubbing · Theatre Voice</span>
          </button>
        </div>

        <div class="share-matrix-inline">
          <span class="share-label">SHARE</span>
          <button class="btn-share" onclick="openWeChatShare()" title="分享到微信朋友圈">💬 微信</button>
          <button class="btn-share" onclick="shareToWeibo()" title="分享至新浪微博">🔴 微博</button>
          <button class="btn-share" onclick="shareToLinkedIn()" title="Share to LinkedIn">💼 LinkedIn</button>
          <button class="btn-share" onclick="shareToX()" title="Share to X (Twitter)">𝕏 Post</button>
          <button class="btn-share" onclick="shareToWhatsApp()" title="Share to WhatsApp">🟢 WhatsApp</button>
          <button class="btn-share" onclick="shareToTelegram()" title="Share to Telegram">✈️ Telegram</button>
          <button class="btn-share" onclick="shareToFacebook()" title="Share to Facebook">📘 Facebook</button>
          <button class="btn-share" onclick="copyViralShare()" title="复制金句精编文案">📋 复制文案</button>
        </div>
      </div>

      <div class="player-main-ctrl">
        <div class="ctrl-left">
          <button class="play-btn" id="master-play-btn" onclick="togglePlay()">▶</button>
          <div class="track-meta">
            <span class="track-meta-title" id="track-meta-title">{ep["title_zh"]}（中文原声）</span>
            <span class="track-meta-sub" id="track-meta-sub">Morris Chang Parallel World · EP {ep["id"]}</span>
          </div>
        </div>

        <div class="progress-container">
          <span class="time-text" id="cur-time">00:00</span>
          <input type="range" class="seek-bar" id="seek-slider" min="0" max="100" value="0" step="0.1" oninput="onSeekInput(this.value)" onchange="onSeekChange(this.value)">
          <span class="time-text" id="total-time">{ep["duration"]}</span>
        </div>

        <div class="playback-options">
          <select class="speed-select" id="speed-select" onchange="changeSpeed(this.value)">
            <option value="0.8">0.8x</option>
            <option value="1.0" selected>1.0x</option>
            <option value="1.2">1.2x</option>
            <option value="1.5">1.5x</option>
            <option value="2.0">2.0x</option>
          </select>
        </div>
      </div>

      <!-- Teleprompter Subtitle Stream -->
      <div class="teleprompter-box">
        <div class="teleprompter-header">
          <div class="teleprompter-title">
            <span>逐句同步字幕 · <b>TELEPROMPTER</b></span>
          </div>
          <div class="teleprompter-tools">
            <button class="btn-toggle-scroll active" id="btn-auto-scroll" onclick="toggleAutoScroll()">自动滚动: 开</button>
          </div>
        </div>

        <div class="subtitles-scroll" id="subtitles-viewport">
{cues_scroll_html}
        </div>
      </div>
    </div>

    <!-- Episode Meta Pills -->
    <div class="meta-pills">
      {pills_html}
    </div>

    <!-- Dual Layout Body: 75% Pure Book + 25% Learning Sidebar -->
    <div class="content-grid">
      <!-- 75% Pure Bilingual Reading -->
      <div class="book-main">
{book_body_html}

        <!-- Quote Banner -->
        <div class="quote-banner">
          <div class="quote-zh">“{ep["quote_zh"]}”</div>
          <div class="quote-en">"{ep["quote_en"]}"</div>
        </div>

        <!-- Episode Navigation -->
        <div class="ep-footer-nav">
          <a href="{ep["prev_link"]}" class="btn-nav-ep prev">{ep["prev_label"]}</a>
          <a href="{ep["next_link"]}" class="btn-nav-ep next">{ep["next_label"]}</a>
        </div>
      </div>

      <!-- 25% Learning & Knowledge Sidebar -->
      <aside class="learning-sidebar">
        <!-- Vocab Widget -->
        <div class="side-widget">
          <div class="widget-title">
            <span class="icon">📖</span>
            <span>核心商务与半导体英语</span>
          </div>
          <div class="vocab-list">
{vocab_html}
          </div>
        </div>

        <!-- Historical Timeline Widget -->
        <div class="side-widget">
          <div class="widget-title">
            <span class="icon">⏳</span>
            <span>时代历史坐标</span>
          </div>
          <div class="timeline-list">
{timeline_html}
          </div>
        </div>
      </aside>
    </div>

  </main>

  <!-- Audio Element -->
  <audio id="main-audio" preload="metadata">
    <source id="audio-source" src="./audio/ep{ep["id"]}-zh.mp3" type="audio/mpeg">
  </audio>

  <!-- Toast Element -->
  <div class="toast-msg" id="toast">已复制到剪贴板</div>

  <!-- WeChat Share Modal -->
  <div class="wechat-modal" id="wechat-modal" onclick="closeWeChatShare()">
    <div class="wechat-modal-box" onclick="event.stopPropagation()">
      <button class="wechat-modal-close" onclick="closeWeChatShare()">&times;</button>
      <div class="wechat-modal-title">微信扫码分享</div>
      <div class="wechat-modal-desc">用微信扫描下方二维码，即可在手机端沉浸研读并一键分享至朋友圈与好友：</div>
      <div class="wechat-qrcode-wrap">
        <img class="wechat-qrcode-img" id="wechat-qrcode" src="" alt="微信二维码">
      </div>
      <div style="font-size: 11.5px; color: var(--amber);">支持原声剧场 · 逐句同步字幕 · 双语精读</div>
    </div>
  </div>

  <script>
    const EPISODE_META = {json.dumps(ep, ensure_ascii=False)};
    const EP_CUES = {json.dumps(cues, ensure_ascii=False)};

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

    function ensureSingleAudioPlayback(activeAudio) {{
      document.querySelectorAll('audio').forEach(a => {{
        if (a !== activeAudio && !a.paused) {{
          a.pause();
        }}
      }});
    }}

    function switchTrack(track) {{
      if (currentTrack === track) return;
      currentTrack = track;
      const curPos = audioEl.currentTime;
      const wasPlaying = !audioEl.paused;

      if (track === 'zh') {{
        btnTrackZh.classList.add('active');
        btnTrackEn.classList.remove('active');
        audioSource.src = './audio/ep' + EPISODE_META.id + '-zh.mp3';
        trackMetaTitle.textContent = EPISODE_META.title_zh + '（中文原声）';
      }} else {{
        btnTrackEn.classList.add('active');
        btnTrackZh.classList.remove('active');
        audioSource.src = './audio/ep' + EPISODE_META.id + '-en.mp3';
        trackMetaTitle.textContent = EPISODE_META.title_en + ' (English Voice)';
      }}

      audioEl.load();
      audioEl.onloadedmetadata = () => {{
        audioEl.currentTime = Math.min(curPos, audioEl.duration || curPos);
        totalTimeEl.textContent = formatTime(audioEl.duration);
        if (wasPlaying) {{
          ensureSingleAudioPlayback(audioEl);
          audioEl.play().then(() => {{
            isPlaying = true;
            playBtn.textContent = '⏸';
          }}).catch(() => {{}});
        }}
      }};
    }}

    function togglePlay() {{
      if (audioEl.paused) {{
        ensureSingleAudioPlayback(audioEl);
        audioEl.play().then(() => {{
          isPlaying = true;
          playBtn.textContent = '⏸';
        }}).catch(e => {{
          console.error("Playback error:", e);
        }});
      }} else {{
        audioEl.pause();
        isPlaying = false;
        playBtn.textContent = '▶';
      }}
    }}

    audioEl.addEventListener('play', () => {{
      ensureSingleAudioPlayback(audioEl);
      isPlaying = true;
      playBtn.textContent = '⏸';
    }});

    audioEl.addEventListener('pause', () => {{
      isPlaying = false;
      playBtn.textContent = '▶';
    }});

    audioEl.addEventListener('loadedmetadata', () => {{
      totalTimeEl.textContent = formatTime(audioEl.duration);
    }});

    audioEl.addEventListener('timeupdate', () => {{
      if (isSeeking) return;
      const cur = audioEl.currentTime;
      const dur = audioEl.duration || 1;
      curTimeEl.textContent = formatTime(cur);
      seekSlider.value = (cur / dur) * 100;

      // Update Active Cue
      let foundIdx = -1;
      for (let i = 0; i < EP_CUES.length; i++) {{
        const c = EP_CUES[i];
        if (cur >= c.start && cur < c.end) {{
          foundIdx = i;
          break;
        }}
      }}

      if (foundIdx === -1 && cur >= EP_CUES[EP_CUES.length - 1].end) {{
        foundIdx = EP_CUES.length - 1;
      }}

      if (foundIdx !== -1 && foundIdx !== activeCueIndex) {{
        setActiveCue(foundIdx);
      }}
    }});

    // Detection for User Manual Wheel or Touch Drag
    let isUserScrolling = false;
    let userScrollTimer = null;

    if (subtitlesViewport) {{
      subtitlesViewport.addEventListener('wheel', () => {{
        isUserScrolling = true;
        clearTimeout(userScrollTimer);
        userScrollTimer = setTimeout(() => {{ isUserScrolling = false; }}, 2000);
      }}, {{ passive: true }});

      subtitlesViewport.addEventListener('touchstart', () => {{
        isUserScrolling = true;
        clearTimeout(userScrollTimer);
        userScrollTimer = setTimeout(() => {{ isUserScrolling = false; }}, 2000);
      }}, {{ passive: true }});
    }}

    // Rock-Solid Container Center Scroll Logic
    function scrollSubtitleToCenter(container, activeElement) {{
      if (!container || !activeElement || !autoScroll || isUserScrolling) return;
      
      const containerRect = container.getBoundingClientRect();
      const elementRect = activeElement.getBoundingClientRect();
      
      // Calculate active element center relative to container scroll position
      const elementRelativeTop = elementRect.top - containerRect.top + container.scrollTop;
      const targetScrollTop = elementRelativeTop - (container.clientHeight / 2) + (elementRect.height / 2);
      
      container.scrollTo({{
        top: Math.max(0, targetScrollTop),
        behavior: 'smooth'
      }});
    }}

    function setActiveCue(index) {{
      activeCueIndex = index;

      // Update Subtitles List
      document.querySelectorAll('.sub-row').forEach(row => row.classList.remove('active'));
      const activeRow = document.getElementById('sub-row-' + index);
      if (activeRow) {{
        activeRow.classList.add('active');
        if (autoScroll && subtitlesViewport) {{
          scrollSubtitleToCenter(subtitlesViewport, activeRow);
        }}
      }}

      // Update Book Paragraphs
      document.querySelectorAll('.bilingual-para').forEach(p => p.classList.remove('current-reading'));
      const activePara = document.getElementById('para-' + index);
      if (activePara) {{
        activePara.classList.add('current-reading');
      }}
    }}

    function seekAndPlay(timeSec) {{
      audioEl.currentTime = timeSec;
      ensureSingleAudioPlayback(audioEl);
      audioEl.play().then(() => {{
        isPlaying = true;
        playBtn.textContent = '⏸';
      }}).catch(() => {{}});
    }}

    function onSeekInput(val) {{
      isSeeking = true;
      const targetTime = (val / 100) * (audioEl.duration || 0);
      curTimeEl.textContent = formatTime(targetTime);
    }}

    function onSeekChange(val) {{
      isSeeking = false;
      const targetTime = (val / 100) * (audioEl.duration || 0);
      audioEl.currentTime = targetTime;
    }}

    function changeSpeed(spd) {{
      audioEl.playbackRate = parseFloat(spd);
    }}

    function toggleAutoScroll() {{
      autoScroll = !autoScroll;
      btnAutoScroll.textContent = '自动滚动: ' + (autoScroll ? '开' : '关');
      btnAutoScroll.classList.toggle('active', autoScroll);
      showToast(autoScroll ? '字幕已开启自动跟随滚动' : '字幕自动滚动已关闭');
    }}

    function formatTime(sec) {{
      if (isNaN(sec) || sec < 0) return '00:00';
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s);
    }}

    function pronounceWord(word) {{
      if ('speechSynthesis' in window) {{
        const utterance = new SpeechSynthesisUtterance(word);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
      }} else {{
        showToast('浏览器不支持语音朗读');
      }}
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => {{
        toast.classList.remove('show');
      }}, 2600);
    }}

    // Sharing Matrix Logic
    function openWeChatShare() {{
      const modal = document.getElementById('wechat-modal');
      const qrcode = document.getElementById('wechat-qrcode');
      const curUrl = encodeURIComponent(window.location.href);
      qrcode.src = 'https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=' + curUrl;
      modal.style.display = 'flex';
    }}

    function closeWeChatShare() {{
      document.getElementById('wechat-modal').style.display = 'none';
    }}

    function shareToWeibo() {{
      const text = encodeURIComponent('【台积电张忠谋 · 传记时间线的平行世界】' + EPISODE_META.title_zh + '：' + EPISODE_META.tagline_zh);
      const url = encodeURIComponent(window.location.href);
      window.open('https://service.weibo.com/share/share.php?title=' + text + '&url=' + url, '_blank');
    }}

    function shareToLinkedIn() {{
      const url = encodeURIComponent(window.location.href);
      window.open('https://www.linkedin.com/sharing/share-offsite/?url=' + url, '_blank');
    }}

    function shareToX() {{
      const text = encodeURIComponent('Reading & Listening to "Morris Chang & TSMC Parallel World" - ' + EPISODE_META.title_en + ':\\n"' + EPISODE_META.tagline_en + '"');
      const url = encodeURIComponent(window.location.href);
      window.open('https://twitter.com/intent/tweet?text=' + text + '&url=' + url, '_blank');
    }}

    function shareToWhatsApp() {{
      const text = encodeURIComponent('《台积电张忠谋：传记时间线的平行世界》' + EPISODE_META.title_zh + '\\n' + window.location.href);
      window.open('https://api.whatsapp.com/send?text=' + text, '_blank');
    }}

    function shareToTelegram() {{
      const text = encodeURIComponent('《台积电张忠谋：传记时间线的平行世界》' + EPISODE_META.title_zh);
      const url = encodeURIComponent(window.location.href);
      window.open('https://t.me/share/url?url=' + url + '&text=' + text, '_blank');
    }}

    function shareToFacebook() {{
      const url = encodeURIComponent(window.location.href);
      window.open('https://www.facebook.com/sharer/sharer.php?u=' + url, '_blank');
    }}

    function copyViralShare() {{
      const viralText = '【台积电张忠谋 · 传记时间线的平行世界】\\n' +
        '📖 ' + EPISODE_META.title_zh + ' (' + EPISODE_META.time_loc + ')\\n' +
        '💡 金句：' + EPISODE_META.tagline_zh + '\\n' +
        '🎧 中英双语广播级原声剧场 + 逐句高亮字幕 + 深度研读笔记：\\n' +
        window.location.href;
      
      if (navigator.clipboard && window.isSecureContext) {{
        navigator.clipboard.writeText(viralText).then(() => {{
          showToast('精选文案与链接已复制，去微信/小红书分享吧！');
        }}).catch(() => {{
          promptCopy(viralText);
        }});
      }} else {{
        promptCopy(viralText);
      }}
    }}

    function promptCopy(text) {{
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-999999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {{
        document.execCommand('copy');
        showToast('精选文案与链接已复制！');
      }} catch (err) {{
        showToast('复制失败，请手动长按复制');
      }}
      document.body.removeChild(textArea);
    }}
  </script>
</body>
</html>
"""
    output_path = os.path.join(WORKSPACE, ep["file_name"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated {ep['file_name']} successfully.")

print("All episodes 10-18 rebuilt and verified.")
