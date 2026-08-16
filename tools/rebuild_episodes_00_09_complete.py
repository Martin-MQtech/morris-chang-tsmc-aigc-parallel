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

ep_config = [
    {
        "id": "00",
        "file_name": "episode-00.html",
        "folder": "第00期-全册导读",
        "act_tag": "PRELUDE · 导读 · 一个人的平行世界",
        "title_zh": "第 00 期：全册导读 · 一个人的平行世界",
        "title_en": "Episode 00: A Guide to the Whole Volume — One Man's Parallel World",
        "time_loc": "全书导览 · 18幕平行回望",
        "tagline_zh": "历史没有如果，但思考有。在张忠谋走过的每一个路口，平行世界都在向我们招手。",
        "tagline_en": "History has no ifs, but contemplation does. At every crossroad Morris Chang took, a parallel world beckons.",
        "pills": [
            ("历史坐标", "全书导读 · 18幕商业决策复盘 · 晶圆代工模式演进 · 半导体半世纪风云"),
            ("有声轨", "中英双轨 6min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/封面/封面_排版版.jpg",
        "prev_link": "index.html",
        "prev_label": "← 回到总目录",
        "next_link": "episode-01.html",
        "next_label": "下一期：第 01 期 逃难的孩子 →",
        "quote_zh": "历史没有如果，但思考有。在张忠谋走过的每一个路口，平行世界都在向我们招手。",
        "quote_en": "History has no ifs, but contemplation does. At every crossroad Morris Chang took, a parallel world beckons."
    },
    {
        "id": "01",
        "file_name": "episode-01.html",
        "folder": "第01期-逃难的孩子",
        "act_tag": "ACT 01 · 1937–1942 · 广州至香港",
        "title_zh": "第 01 期：逃难的孩子",
        "title_en": "Episode 01: The Refugee Child",
        "time_loc": "1937–1942 · 广州至香港",
        "tagline_zh": "时代可以推着你走，但走成什么样，从来是你自己的事。",
        "tagline_en": "The era may push you along, but who you become has always been up to you.",
        "pills": [
            ("历史坐标", "抗日战争爆发 · 广州沦陷 · 逃难香港 · 颠沛童年与乱世启蒙"),
            ("有声轨", "中英双轨 18min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第01期-逃难的孩子.png",
        "prev_link": "episode-00.html",
        "prev_label": "← 上一期：第 00 期 全册导读",
        "next_link": "episode-02.html",
        "next_label": "下一期：第 02 期 考不进去的南开与作家梦 →",
        "quote_zh": "时代可以推着你走，但走成什么样，从来是你自己的事。",
        "quote_en": "The era may push you along, but who you become has always been up to you."
    },
    {
        "id": "02",
        "file_name": "episode-02.html",
        "folder": "第02期-考不进去的南开与作家梦",
        "act_tag": "ACT 02 · 1943–1948 · 重庆至上海",
        "title_zh": "第 02 期：考不进去的南开与作家梦",
        "title_en": "Episode 02: Failing Nankai and the Writer's Dream",
        "time_loc": "1943–1948 · 重庆至上海",
        "tagline_zh": "一个「会饿肚子」的警告，关上了一扇门；但生命最奇妙的，正是那些不得不拐的弯。",
        "tagline_en": "A warning about going hungry closed one door; yet life's true wonder lies in the unavoidable detours.",
        "pills": [
            ("历史坐标", "重庆南开中学 · 作家文学梦 · 父亲的实用主义劝诫 · 沪江大学预备"),
            ("有声轨", "中英双轨 19min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第02期-考不进去的南开与作家梦.png",
        "prev_link": "episode-01.html",
        "prev_label": "← 上一期：第 01 期 逃难的孩子",
        "next_link": "episode-03.html",
        "next_label": "下一期：第 03 期 从黄浦江到查尔斯河 →",
        "quote_zh": "一个「会饿肚子」的警告，关上了一扇门；但生命最奇妙的，正是那些不得不拐的弯。",
        "quote_en": "A warning about going hungry closed one door; yet life's true wonder lies in the unavoidable detours."
    },
    {
        "id": "03",
        "file_name": "episode-03.html",
        "folder": "第03期-从黄浦江到查尔斯河",
        "act_tag": "ACT 03 · 1949–1950 · 赴美哈佛至MIT",
        "title_zh": "第 03 期：从黄浦江到查尔斯河",
        "title_en": "Episode 03: From the Huangpu to the Charles River",
        "time_loc": "1949–1950 · 赴美哈佛至MIT",
        "tagline_zh": "在两座文明的裂缝之间，他学会了以世界为坐标校准自己的一生。",
        "tagline_en": "Between the fractures of two civilizations, he learned to calibrate his life by a global compass.",
        "pills": [
            ("历史坐标", "克利夫兰总统号轮船 · 哈佛唯一华人本科生 · 莎士比亚与荷马 · 转学麻省理工MIT"),
            ("有声轨", "中英双轨 22min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第03期-从黄浦江到查尔斯河.png",
        "prev_link": "episode-02.html",
        "prev_label": "← 上一期：第 02 期 考不进去的南开与作家梦",
        "next_link": "episode-04.html",
        "next_label": "下一期：第 04 期 四十封求职信 →",
        "quote_zh": "在两座文明的裂缝之间，他学会了以世界为坐标校准自己的一生。",
        "quote_en": "Between the fractures of two civilizations, he learned to calibrate his life by a global compass."
    },
    {
        "id": "04",
        "file_name": "episode-04.html",
        "folder": "第04期-四十封求职信",
        "act_tag": "ACT 04 · 1954–1958 · MIT挫折与希凡尼亚",
        "title_zh": "第 04 期：四十封求职信",
        "title_en": "Episode 04: Forty Job Applications",
        "time_loc": "1954–1958 · MIT挫折与希凡尼亚",
        "tagline_zh": "被拒绝不是终点，是命运在给你指另一条路——通向半导体的黄金时代。",
        "tagline_en": "Rejection is never the end; it is destiny redirecting your path toward semiconductors' golden age.",
        "pills": [
            ("历史坐标", "MIT博士资格考失利 · 投递40封求职简历 · 因一美元之差拒绝福特 · 进入希凡尼亚"),
            ("有声轨", "中英双轨 21min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第04期-四十封求职信.png",
        "prev_link": "episode-03.html",
        "prev_label": "← 上一期：第 03 期 从黄浦江到查尔斯河",
        "next_link": "episode-05.html",
        "next_label": "下一期：第 05 期 隔岸观火的叛乱 →",
        "quote_zh": "被拒绝不是终点，是命运在给你指另一条路——通向半导体的黄金时代。",
        "quote_en": "Rejection is never the end; it is destiny redirecting your path toward semiconductors' golden age."
    },
    {
        "id": "05",
        "file_name": "episode-05.html",
        "folder": "第05期-隔岸观火的叛乱",
        "act_tag": "ACT 05 · 1957–1958 · 硅谷初生与仙童叛乱",
        "title_zh": "第 05 期：隔岸观火的叛乱",
        "title_en": "Episode 05: Watching the Rebellion from Afar",
        "time_loc": "1957–1958 · 硅谷初生与仙童叛乱",
        "tagline_zh": "当一群年轻人掀翻旧桌子时，远在东岸的他看懂了一件事：规则要由下场的人来定。",
        "tagline_en": "When a rebel pack overturned the old table, he realized from the East Coast: rules belong to those on the field.",
        "pills": [
            ("历史坐标", "肖克利半导体 · 仙童八叛逆出走 · 硅谷创投模式萌芽 · 东西海岸半导体暗战"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第05期-隔岸观火的叛乱.png",
        "prev_link": "episode-04.html",
        "prev_label": "← 上一期：第 04 期 四十封求职信",
        "next_link": "episode-06.html",
        "next_label": "下一期：第 06 期 德仪的太空竞赛岁月 →",
        "quote_zh": "当一群年轻人掀翻旧桌子时，远在东岸的他看懂了一件事：规则要由下场的人来定。",
        "quote_en": "When a rebel pack overturned the old table, he realized from the East Coast: rules belong to those on the field."
    },
    {
        "id": "06",
        "file_name": "episode-06.html",
        "folder": "第06期-德仪的太空竞赛岁月",
        "act_tag": "ACT 06 · 1958–1964 · 德仪与集成电路",
        "title_zh": "第 06 期：德仪的太空竞赛岁月",
        "title_en": "Episode 06: The Space Race Years at Texas Instruments",
        "time_loc": "1958–1964 · 德仪与集成电路",
        "tagline_zh": "冷战的火箭把人类送进太空，也把集成电路推上了历史的浪尖。他在达拉斯看到了未来。",
        "tagline_en": "Cold War rockets hurled humanity into space and thrust ICs onto history's crest. In Dallas, he saw the future.",
        "pills": [
            ("历史坐标", "加盟德州仪器TI · 基尔比发明集成电路 · 阿波罗与民兵导弹订单 · 斯坦福博士深造"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第06期-德仪的太空竞赛岁月.png",
        "prev_link": "episode-05.html",
        "prev_label": "← 上一期：第 05 期 隔岸观火的叛乱",
        "next_link": "episode-07.html",
        "next_label": "下一期：第 07 期 半导体之巅的十年 →",
        "quote_zh": "冷战的火箭把人类送进太空，也把集成电路推上了历史的浪尖。他在达拉斯看到了未来。",
        "quote_en": "Cold War rockets hurled humanity into space and thrust ICs onto history's crest. In Dallas, he saw the future."
    },
    {
        "id": "07",
        "file_name": "episode-07.html",
        "folder": "第07期-半导体之巅的十年",
        "act_tag": "ACT 07 · 1964–1974 · 德仪全球副总裁",
        "title_zh": "第 07 期：半导体之巅的十年",
        "title_en": "Episode 07: The Decade at the Summit of Semiconductors",
        "time_loc": "1964–1974 · 德仪全球副总裁",
        "tagline_zh": "坐在全球半导体的王座上，他发现决定胜负的不仅是技术，更是学习曲线上的疯狂下杀。",
        "tagline_en": "At the semiconductor peak, he discovered victory hinged not merely on tech, but aggressive learning-curve pricing.",
        "pills": [
            ("历史坐标", "统领TI半导体三万人 · 学习曲线与激进降价 · 击溃仙童与摩托罗拉 · 全球芯片霸主"),
            ("有声轨", "中英双轨 21min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第07期-半导体之巅的十年.png",
        "prev_link": "episode-06.html",
        "prev_label": "← 上一期：第 06 期 德仪的太空竞赛岁月",
        "next_link": "episode-08.html",
        "next_label": "下一期：第 08 期 离开德州与受邀回台 →",
        "quote_zh": "坐在全球半导体的王座上，他发现决定胜负的不仅是技术，更是学习曲线上的疯狂下杀。",
        "quote_en": "At the semiconductor peak, he discovered victory hinged not merely on tech, but aggressive learning-curve pricing."
    },
    {
        "id": "08",
        "file_name": "episode-08.html",
        "folder": "第08期-离开德州与受邀回台",
        "act_tag": "ACT 08 · 1983–1985 · 离开德仪与跨海邀约",
        "title_zh": "第 08 期：离开德州与受邀回台",
        "title_en": "Episode 08: Leaving Texas & the Invitation Home",
        "time_loc": "1983–1985 · 离开德仪与跨海邀约",
        "tagline_zh": "五十四岁，有人准备退休，他却把前半生积攒的所有筹码，押上了一场无人看好的赌局。",
        "tagline_en": "At 54, when many prepare to retire, he wagered his entire life's chips on a gamble nobody favored.",
        "pills": [
            ("历史坐标", "消费电子战略分歧 · 辞去TI资深副总裁 · 通用仪器短暂任职 · 孙运璿与李国鼎跨海延揽"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第08期-离开德州与受邀回台.png",
        "prev_link": "episode-07.html",
        "prev_label": "← 上一期：第 07 期 半导体之巅的十年",
        "next_link": "episode-09.html",
        "next_label": "下一期：第 09 期 纯代工的革命 →",
        "quote_zh": "五十四岁，有人准备退休，他却把前半生积攒的所有筹码，押上了一场无人看好的赌局。",
        "quote_en": "At 54, when many prepare to retire, he wagered his entire life's chips on a gamble nobody favored."
    },
    {
        "id": "09",
        "file_name": "episode-09.html",
        "folder": "第09期-纯代工的革命",
        "act_tag": "ACT 09 · 1986–1987 · 台积电诞生与纯代工",
        "title_zh": "第 09 期：纯代工的革命",
        "title_en": "Episode 09: The Pure-Play Revolution",
        "time_loc": "1986–1987 · 台积电诞生与纯代工",
        "tagline_zh": "不和客户竞争，只做客户的制造后盾——看似退让的一步，改写了全球芯片工业的游戏规则。",
        "tagline_en": "Never compete with customers; serve solely as their manufacturing spine—a concession that remade the chip industry.",
        "pills": [
            ("历史坐标", "接任工研院院长 · 纯晶圆代工商业模式开创 · 飞利浦资本引入 · 台积电TSMC成立"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第09期-纯代工的革命.png",
        "prev_link": "episode-08.html",
        "prev_label": "← 上一期：第 08 期 离开德州与受邀回台",
        "next_link": "episode-10.html",
        "next_label": "下一期：第 10 期 从台湾到世界 →",
        "quote_zh": "不和客户竞争，只做客户的制造后盾——看似退让的一步，改写了全球芯片工业的游戏规则。",
        "quote_en": "Never compete with customers; serve solely as their manufacturing spine—a concession that remade the chip industry."
    }
]

# Extract vocab and timeline from existing HTML files for high quality
for ep in ep_config:
    fn = ep["file_name"]
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

# Fallback timeline or vocab if empty
for ep in ep_config:
    if not ep.get("vocab"):
        ep["vocab"] = [
            ("Semiconductor", "/ˌsemikənˈdʌktər/", "半导体", "Materials with electrical conductivity between conductors and insulators."),
            ("Pure-Play Foundry", "/pjʊər pleɪ ˈfaʊndri/", "纯晶圆代工厂", "A semiconductor company exclusively manufacturing chips for other designers."),
            ("Disruption", "/dɪsˈrʌpʃən/", "颠覆性创新", "Innovation that significantly alters the way that consumers, industries, or businesses operate.")
        ]
    if not ep.get("timeline"):
        ep["timeline"] = [
            (ep["time_loc"].split("·")[0].strip(), ep["tagline_zh"])
        ]

# Load audio_data.js
with open(os.path.join(WORKSPACE, "audio_data.js"), "r", encoding="utf-8") as f:
    audio_js_text = f.read()

# Extract existing audio_data JSON
start_bracket = audio_js_text.find('[')
end_bracket = audio_js_text.rfind(']')
audio_episodes_data = json.loads(audio_js_text[start_bracket:end_bracket+1])

print(f"Loaded audio_data.js with {len(audio_episodes_data)} episodes.")

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

# Update audio_episodes_data in audio_data.js
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

# Now regenerate episode-00.html through episode-09.html
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
        
        cues_rows_html.append(f"""          <div class="sub-row" id="sub-row-{i}" data-index="{i}" data-start="{start_sec:.2f}" data-end="{end_sec:.2f}" onclick="seekAndPlay({start_sec:.2f})">
            <span class="sub-time-tag">{time_str}</span>
            <div class="sub-content">
              <div class="sub-zh">{html.escape(zh_text)}</div>
              <div class="sub-en">{html.escape(en_text)}</div>
            </div>
          </div>""")
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
            
            sec_paras_html.append(f"""              <div class="bilingual-para{sfx_class}" id="para-{c_idx}" onclick="seekAndPlay({start_time:.2f})">
                <span class="para-time-badge">{time_tag}</span>
                <div class="para-content">
                  <p class="zh-para">{html.escape(p_zh)}</p>
                  <p class="en-para">{html.escape(p_en)}</p>
                </div>
              </div>""")
            
        sec_tag_num = f"ACT {s_idx + 1:02d}" if "幕" in sec_title or "Act" in sec_title else "SECTION"
        book_sections_html.append(f"""          <section class="book-section">
            <div class="book-section-header">
              <span class="section-tag">{sec_tag_num}</span>
              <h2 class="serif">{html.escape(sec_title)}<span class="en">{html.escape(en_sec_title)}</span></h2>
            </div>
            <div class="section-body">
{"\n".join(sec_paras_html)}
            </div>
          </section>""")
        
    book_body_html = "\n".join(book_sections_html)
    
    # Vocab cards HTML
    vocab_cards_html = []
    for w, ph, zh_def, en_def in ep["vocab"]:
        vocab_cards_html.append(f"""          <div class="vocab-card">
            <div class="vocab-word-row">
              <span class="vocab-word">{html.escape(w)}</span>
              <span class="vocab-phonetic">{html.escape(ph)}</span>
              <button class="btn-pronounce" onclick="pronounceWord('{html.escape(w)}')" title="点击发音">🔊</button>
            </div>
            <div class="vocab-zh">{html.escape(zh_def)}</div>
            <div class="vocab-en">{html.escape(en_def)}</div>
          </div>""")
    vocab_html = "\n".join(vocab_cards_html)
    
    # Timeline HTML
    tl_items_html = []
    for yr, desc in ep["timeline"]:
        tl_items_html.append(f"""          <div class="tl-item">
            <div class="tl-year">{html.escape(yr)}</div>
            <div class="tl-desc">{html.escape(desc)}</div>
          </div>""")
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

print("All episodes 00-09 rebuilt and calibrated successfully.")
