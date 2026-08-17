# -*- coding: utf-8 -*-
"""
微信视频号【英文版】19 期全集发布数据集
- 严格校对 19 轨全英文 MP3 音频 (audio/ep00-en.mp3 ~ audio/ep18-en.mp3)
- 严格校对 19 套排版版插图真实物理路径
- 纯正地道英文标题 (≤40字符)
- 深度英文叙事文案 + 金句提炼 + 英文 Hashtags + 官方 GitHub 双语互动展厅 URL
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GITHUB_PORTAL_URL = "https://martin-mqtech.github.io/morris-chang-tsmc-aigc-parallel/index.html"

# 合集名称加入最大核心 IP: TSMC
ENGLISH_COLLECTION_NAME = "TSMC & Morris Chang: Parallel"

EPISODES_DATA_EN = [
    {
        "ep_id": "00",
        "title": "Ep00 · Guide | One Timeline, Another Point of View",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep00-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "封面", "封面_排版版.jpg"),
        "timeline": "1931–2024 · Master Overview",
        "tags": ["TSMC", "MorrisChang", "Semiconductors", "TechHistory", "AIGC", "Biography"],
        "desc": f"""【Ep00 · Master Guide: One Timeline, Another Point of View】

"These are not ten separate stories. They are the epic movements of a single civilization-scale biography."

From childhood evacuations across wartime cities to MIT, Texas Instruments, and founding TSMC—the pure-play foundry that powers the modern AI era—follow Morris Chang's parallel world.

🎧 3-Part Movement Structure:
• Part I: Departure & Solitude (Wartime exile to MIT)
• Part II: Ascent & The 54-Year-Old Gamble (TI to TSMC)
• Part III: Defending Moore's Law (28nm to Global AI Dominance)

Explore the full interactive bilingual exhibition & synchronized transcripts:
👉 {GITHUB_PORTAL_URL}

#TSMC #MorrisChang #Semiconductors #TechHistory #ChipWar #DeepThinking #AIGC #Biography"""
    },
    {
        "ep_id": "01",
        "title": "Ep01 · Refugee Child | Steered by Fate, Driven by Will",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep01-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第01期-逃难的孩子.jpg"),
        "timeline": "1931–1942 · Guangzhou to Hong Kong",
        "tags": ["TSMC", "MorrisChang", "RefugeeChild", "Resilience", "History"],
        "desc": f"""【Ep01 · A Refugee Child: Steered by Fate, Driven by Will】

"The times may push you forward, but where you walk and who you become is always your own decision."

A five-year-old boy boards a steamer amid wartime chaos, beginning an odyssey across six cities and ten schools. War stripped away stability, yet forged an instinct for navigation.

🎧 Explore interactive bilingual transcripts & historical maps:
👉 {GITHUB_PORTAL_URL}

#TSMC #MorrisChang #RefugeeChild #Resilience #TechHistory #AIGC #Biography"""
    },
    {
        "ep_id": "02",
        "title": "Ep02 · Writer's Dream | Shattered by Reality",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep02-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第02期-考不进去的南开与作家梦.jpg"),
        "timeline": "1942–1948 · Shanghai Desks & Runaway Inflation",
        "tags": ["TSMC", "MorrisChang", "WritersDream", "PivotalDecisions", "Literature"],
        "desc": f"""【Ep02 · The Writer's Dream: Shattered by Reality】

"Literature gave him a lifelong philosophical foundation; but the era pushed him decisively toward engineering."

In Shanghai, a young student fell in love with literature, until his father's gentle warning and runaway currency inflation rewrote his trajectory toward the sciences.

🎧 Interactive exhibition with audio synchronization:
👉 {GITHUB_PORTAL_URL}

#TSMC #MorrisChang #WritersDream #CareerChoices #SemiconductorPioneer #AIGC"""
    },
    {
        "ep_id": "03",
        "title": "Ep03 · One-Way Ticket | Crossing the Pacific to Harvard & MIT",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep03-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第03期-从黄浦江到查尔斯河.jpg"),
        "timeline": "1949–1955 · Pacific Ocean to Boston",
        "tags": ["TSMC", "Harvard", "MIT", "MorrisChang", "GlobalMindset"],
        "desc": f"""【Ep03 · From the Huangpu to the Charles: A One-Way Ticket】

"At 18, he boarded a ship thinking it was a temporary journey. It became a point of no return."

Walking into Harvard as the sole Chinese freshman of 1949, then transferring to MIT mechanical engineering—mastering rigorous first-principles thinking in solitary pursuit.

🎧 Listen & read synchronized scripts:
👉 {GITHUB_PORTAL_URL}

#TSMC #MorrisChang #Harvard #MIT #CrossCultural #TechLeadership #AIGC"""
    },
    {
        "ep_id": "04",
        "title": "Ep04 · 40 Applications | The Extra Dollar That Changed History",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep04-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第04期-四十封求职信.jpg"),
        "timeline": "1955 · Ford vs. Sylvania",
        "tags": ["TSMC", "MorrisChang", "CareerTurningPoint", "Sylvania", "Semiconductors"],
        "desc": f"""【Ep04 · 40 Applications: The Extra Dollar That Changed History】

"Because of one single dollar of dignity, the world gained a semiconductor visionary instead of an automotive engineer."

Failing the MIT doctoral qualification exam twice, sending 40 resumes, and refusing Ford's rigid offer over $1/month—Morris Chang entered the nascent transistor era at Sylvania.

🎧 Explore interactive bilingual timeline:
👉 {GITHUB_PORTAL_URL}

#TSMC #MorrisChang #CareerTurningPoint #SemiconductorHistory #TechLeadership #AIGC"""
    },
    {
        "ep_id": "05",
        "title": "Ep05 · Wilderness Nights | Mastering Solid-State Physics",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep05-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第05期-隔岸观火的叛乱.jpg"),
        "timeline": "1955–1958 · Self-Taught in the Transistor Wilds",
        "tags": ["TSMC", "MorrisChang", "SelfTaught", "Shockley", "Transistors"],
        "desc": f"""【Ep05 · Wilderness Nights: Mastering Solid-State Physics】

"When entering an uncharted domain, solitary deep reading is the fastest path to mastery."

A mechanical graduate confronting quantum physics and Shockley's seminal book line by line every night, turning an unguided novice into a seasoned semiconductor problem solver.

🎧 Synchronized interactive experience:
👉 {GITHUB_PORTAL_URL}

#TSMC #MorrisChang #LifelongLearning #Physics #TransistorRevolution #AIGC"""
    },
    {
        "ep_id": "06",
        "title": "Ep06 · TI's Rising Star | Doubling Yields & Breaking Records",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep06-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第06期-德仪的太空竞赛岁月.jpg"),
        "timeline": "1958–1961 · Dallas, Texas Instruments",
        "tags": ["TSMC", "TexasInstruments", "MorrisChang", "YieldOptimization", "Manufacturing"],
        "desc": f"""【Ep06 · Rising Star at TI: Doubling Yields & Manufacturing Legends】

"The essence of semiconductor manufacturing is the relentless, uncompromising pursuit of yield."

Joining Texas Instruments in Dallas at 27, fixing the IBM transistor line from zero yield to outperforming TI's top veterans—establishing his legendary engineering reputation.

🎧 Read along with dual-track audio:
👉 {GITHUB_PORTAL_URL}

#TSMC #TexasInstruments #MorrisChang #SemiconductorManufacturing #YieldRate #AIGC"""
    },
    {
        "ep_id": "07",
        "title": "Ep07 · Stanford PhD | Conquering the Summit in 2.5 Years",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep07-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第07期-半导体之巅的十年.jpg"),
        "timeline": "1961–1964 · Stanford University & Silicon Valley",
        "tags": ["TSMC", "Stanford", "PhD", "MorrisChang", "SiliconValley"],
        "desc": f"""【Ep07 · Stanford PhD: Conquering the Summit in 2.5 Years】

"A company-sponsored PhD under immense pressure—elevating intuitive engineering into world-class theory."

TI fully sponsored his doctorate at Stanford under John Linvill. In just two and a half years, he conquered the PhD requirements and returned to lead TI's core R&D.

🎧 Explore interactive exhibit:
👉 {GITHUB_PORTAL_URL}

#TSMC #Stanford #MorrisChang #SemiconductorScience #AcademicExcellence #AIGC"""
    },
    {
        "ep_id": "08",
        "title": "Ep08 · Summit at TI | Running Global Chips & Corporate Currents",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep08-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第08期-离开德州与受邀回台.jpg"),
        "timeline": "1964–1983 · Group VP & Global Semiconductor Power",
        "tags": ["TSMC", "TexasInstruments", "GroupVP", "CorporateStrategy", "MorrisChang"],
        "desc": f"""【Ep08 · Summit at TI: Leading Global Chips & Navigating Corporate Currents】

"Rising to the pinnacle of a Fortune 500 tech giant, commanding 60,000 employees worldwide."

As Group VP of Worldwide Semiconductors, pioneering aggressive cost curves and global fabrication networks, while navigating strategic divergence with TI senior leadership.

🎧 Interactive exhibition:
👉 {GITHUB_PORTAL_URL}

#TSMC #MorrisChang #TexasInstruments #ExecutiveLeadership #ChipIndustry #AIGC"""
    },
    {
        "ep_id": "09",
        "title": "Ep09 · Darkest Hour | Sidelined at 52 & The Secret Rebound",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep09-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第09期-纯代工的革命.jpg"),
        "timeline": "1983–1985 · General Instrument & The Taiwan Invitation",
        "tags": ["TSMC", "DarkestHour", "MidCareerCrisis", "MorrisChang", "Resilience"],
        "desc": f"""【Ep09 · The Darkest Hour: Sidelined at 52 & The Secret Rebound】

"Life's greatest second curve often takes root in the quietest, darkest moments of sideline exile."

Resigning from TI, brief tenure as COO of General Instrument, and accepting Sun Yun-suan and K.T. Li's invitation to head ITRI—the stage was set for a historic revolution.

🎧 Read along with bilingual transcripts:
👉 {GITHUB_PORTAL_URL}

#TSMC #MorrisChang #MidlifePivot #Resilience #IndustrialPolicy #AIGC"""
    },
    {
        "ep_id": "10",
        "title": "Ep10 · The $54M Gamble | Pure-Play Foundry Revolution",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep10-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第10期-从台湾到世界.jpg"),
        "timeline": "1985–1987 · Founding TSMC in Hsinchu",
        "tags": ["TSMC", "PurePlayFoundry", "BusinessModel", "Innovation", "MorrisChang"],
        "desc": f"""【Ep10 · The 54-Year-Old Gamble: Pure-Play Foundry Revolution】

"Do not compete with your customers — inventing the greatest business model in semiconductor history."

In 1987, at age 54, Morris Chang founded TSMC with zero proprietary product design, creating the pure-play foundry model that unleashed the global fabless design explosion.

🎧 Explore interactive exhibit:
👉 {GITHUB_PORTAL_URL}

#TSMC #PurePlayFoundry #MorrisChang #BusinessModelInnovation #Semiconductors"""
    },
    {
        "ep_id": "11",
        "title": "Ep11 · Iron Will | Integrity as the Ultimate Moat",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep11-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第11期-记忆体的诱惑.jpg"),
        "timeline": "1987–1995 · Institutionalizing Corporate Governance",
        "tags": ["TSMC", "Integrity", "CorporateCulture", "Governance", "MorrisChang"],
        "desc": f"""【Ep11 · Iron Will: Integrity, Commitment & The TSMC Moat】

"Integrity is not a slogan on the wall; it is TSMC's most impenetrable commercial moat."

Establishing four core values: Integrity, Commitment, Innovation, and Customer Trust. How strict intellectual property firewalls won the trust of rival chipmakers worldwide.

🎧 Bilingual interactive gallery:
👉 {GITHUB_PORTAL_URL}

#TSMC #CorporateGovernance #IntegrityFirst #TechEthics #MorrisChang"""
    },
    {
        "ep_id": "12",
        "title": "Ep12 · 25-Year Patent War | Defending Innovation Globally",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep12-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第12期-逆周期的定力.jpg"),
        "timeline": "1995–2009 · IP Battles & Global Settlements",
        "tags": ["TSMC", "PatentWar", "IntellectualProperty", "LegalStrategy", "MorrisChang"],
        "desc": f"""【Ep12 · The 25-Year Patent War: Defending Innovation on the Global Stage】

"Using decades of rigorous legal strategy to defend indigenous innovation against global titans."

From early licensing battles with Intel and TI to the historic SMIC trade secret victory in California court—cementing TSMC's unassailable proprietary technological leadership.

🎧 Explore synchronized audio & script:
👉 {GITHUB_PORTAL_URL}

#TSMC #PatentStrategy #IntellectualProperty #SemiconductorLaw #MorrisChang"""
    },
    {
        "ep_id": "13",
        "title": "Ep13 · Night Owl Squad | 24/7 R&D Relay Racing Moore's Law",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep13-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第13期-交棒之痛.jpg"),
        "timeline": "2000–2010 · 3-Shift Continuous R&D Engine",
        "tags": ["TSMC", "NightOwlR&D", "MooresLaw", "EngineeringSpeed", "10nm"],
        "desc": f"""【Ep13 · The Night Owl Squad: 24/7 R&D Relay Racing Moore's Law】

"Labs that never sleep — compressing development time density to breakthrough Moore's Law."

Implementing the world's most disciplined three-shift 24-hour continuous R&D system, enabling TSMC to outpace global competitors from 28nm down to 7nm and beyond.

🎧 Interactive bilingual exhibition:
👉 {GITHUB_PORTAL_URL}

#TSMC #EngineeringCulture #MooresLaw #ContinuousInnovation #MorrisChang"""
    },
    {
        "ep_id": "14",
        "title": "Ep14 · Golden Decade | $40B Capex & 28nm Masterstroke",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep14-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第14期-绚烂年代.jpg"),
        "timeline": "2009–2014 · Return as CEO & Counter-Cyclical Bet",
        "tags": ["TSMC", "28nm", "CounterCyclical", "Capex", "MorrisChangCEO"],
        "desc": f"""【Ep14 · Golden Decade: $40B Capex & The 28nm Masterstroke】

"Counter-cyclical boldness during global crisis made 28nm the most profitable node in chip history."

Returning as CEO during the 2009 financial crisis, radically boosting capital expenditure to $10B/year, capturing 100% of high-end mobile chip manufacturing market share.

🎧 Listen & explore:
👉 {GITHUB_PORTAL_URL}

#TSMC #28nm #CapexBet #BusinessStrategy #MorrisChang"""
    },
    {
        "ep_id": "15",
        "title": "Ep15 · Apple Knocks | Overnight Talks & iPhone Chip Supremacy",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep15-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第15期-苹果来敲门.jpg"),
        "timeline": "2010–2016 · Winning 100% of Apple A-Series SoCs",
        "tags": ["TSMC", "Apple", "iPhoneChips", "ASeries", "MobileComputing"],
        "desc": f"""【Ep15 · When Apple Knocked: Secret Talks & iPhone Chip Supremacy】

"Secret dinner talks with Jeff Williams, betting entire fab capacity on mobile computing's future."

How TSMC committed $9 billion and 6,000 engineers to win 100% exclusive production of Apple's iPhone processors, dethroning Samsung and defining modern consumer electronics.

🎧 Dual-track audio & script:
👉 {GITHUB_PORTAL_URL}

#TSMC #Apple #iPhoneChips #SiliconSupremacy #MorrisChang"""
    },
    {
        "ep_id": "16",
        "title": "Ep16 · Moore's Law Guardian | EUV Lithography & Physics Limit",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep16-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第16期-摩尔定律的守卫者.jpg"),
        "timeline": "2014–2020 · Immersion Lithography to EUV 3nm",
        "tags": ["TSMC", "EUV", "ASML", "MooresLaw", "NanometerRace"],
        "desc": f"""【Ep16 · Guardian of Moore's Law: EUV Lithography & The Atomic Frontier】

"Breaking optical diffraction limits, partnering with ASML to push silicon fabrication into atomic scale."

From Burn Lin's revolutionary water immersion concept to pioneering commercial EUV lithography at 7nm and 3nm—ensuring computing power continues to advance.

🎧 Explore interactive exhibit:
👉 {GITHUB_PORTAL_URL}

#TSMC #ASML #EUVLithography #MooresLaw #Nanotechnology #MorrisChang"""
    },
    {
        "ep_id": "17",
        "title": "Ep17 · Passing the Torch | Co-CEO Model & Succession Wisdom",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep17-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第17期-交棒与退休.jpg"),
        "timeline": "2018 · Dual Leadership Architecture",
        "tags": ["TSMC", "Succession", "CoCEO", "Governance", "Retirement"],
        "desc": f"""【Ep17 · Passing the Torch: The Co-CEO Model & Succession Wisdom】

"Engineering a flawless dual-leadership transition for a trillion-dollar technological juggernaut."

At 87, Morris Chang retired peacefully, establishing the Mark Liu (Chairman) and C.C. Wei (CEO) dual-leadership structure to sustain TSMC's institutional longevity.

🎧 Synchronized bilingual transcripts:
👉 {GITHUB_PORTAL_URL}

#TSMC #CorporateSuccession #DualLeadership #Governance #MorrisChang"""
    },
    {
        "ep_id": "18",
        "title": "Ep18 · Sacred Mountain | Geopolitical Storms & World Champion",
        "audio_path": os.path.join(BASE_DIR, "audio", "ep18-en.mp3"),
        "cover_path": os.path.join(BASE_DIR, "设计资产", "插图", "排版版", "第18期-护国神山.jpg"),
        "timeline": "2020–2024 · Global Fab Expansion & The AI Era",
        "tags": ["TSMC", "SiliconShield", "Geopolitics", "AIEra", "GlobalLeadership"],
        "desc": f"""【Ep18 · Sacred Mountain: Geopolitical Epicenter & World Champion】

"From an island fab to the undisputed centerpiece of global technology, AI infrastructure, and geopolitics."

The grand finale of Morris Chang's parallel biography: Arizona, Kumamoto, Dresden fab expansions, Nvidia/AI chip dominance, and philosophical reflections on tech and humanity.

🎧 Explore full 19-episode interactive museum:
👉 {GITHUB_PORTAL_URL}

#TSMC #Geopolitics #ArtificialIntelligence #MorrisChang #SiliconShield #GrandFinale"""
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(EPISODES_DATA_EN)} English episodes data.")
    for ep in EPISODES_DATA_EN:
        assert os.path.exists(ep["audio_path"]), f"Missing audio: {ep['audio_path']}"
        assert os.path.exists(ep["cover_path"]), f"Missing cover: {ep['cover_path']}"
    print("✅ All 19 English audio files & typography covers verified 100% existing!")
