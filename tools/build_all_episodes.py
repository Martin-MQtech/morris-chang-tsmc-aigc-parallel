import os
import json
import re
import html

WORKSPACE = "/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC"

# Load audio_data.js
with open(os.path.join(WORKSPACE, "audio_data.js"), "r", encoding="utf-8") as f:
    audio_js = f.read()

episodes_meta = [
    {
        "id": "00",
        "file_name": "episode-00.html",
        "folder": "第00期-全册导读",
        "act_tag": "PRELUDE · 导读 · 一个人的平行世界",
        "title_zh": "第 00 期：全册导读 · 一个人的平行世界",
        "title_en": "Episode 00: A Guide to the Whole Volume — One Man's Parallel World",
        "time_loc": "1931–2024 · 跨越近百年的时代坐标",
        "tagline_zh": "历史没有如果，但思考有。在张忠谋走过的每一个路口，平行世界都在向我们招手。",
        "tagline_en": "History has no 'what ifs,' but our contemplation does. At every crossroads Morris Chang walked, parallel worlds beckon.",
        "duration": "06:45",
        "pills": [
            ("历史坐标", "1931–2024 · 宁波-香港-波士顿-达拉斯-新竹"),
            ("有声轨", "中英双轨 7min 广播级剧场原声"),
            ("双语阅读", "75% 全册导言双语对齐 · 25% 时代与方法论解析")
        ],
        "image_path": "./设计资产/封面/封面_上册_蓝图晶圆版.jpg",
        "prev_link": "index.html",
        "prev_label": "← 回到总目录",
        "next_link": "episode-01.html",
        "next_label": "下一期：第 01 期 逃难的孩子 →",
        "vocab": [
            ("Parallel World", "/ˈpær.ə.lel wɜːld/", "平行世界，平行时空", "A hypothetical self-contained reality co-existing with one's own, exploring alternative historical choices."),
            ("Foundry Model", "/ˈfaʊn.dri ˈmɒd.əl/", "晶圆代工模式", "A business model pioneered by TSMC that exclusively manufactures semiconductor chips for fabless companies."),
            ("Semiconductor", "/ˌsem.i.kənˈdʌk.tər/", "半导体", "A material whose electrical conductivity lies between a conductor and an insulator, powering the digital era."),
            ("First Principles", "/fɜːst ˈprɪn.sə.pəlz/", "第一性原理", "The fundamental premise or proposition that cannot be deduced any further from any other proposition."),
            ("Chronicle", "/ˈkrɒn.ɪ.kəl/", "编年史，传记纪事", "A factual written account of important or historical events in the order of their occurrence."),
            ("Geopolitics", "/ˌdʒiː.əʊˈpɒl.ə.tɪks/", "地缘政治", "Politics, especially international relations, as influenced by geographical factors."),
            ("Moore's Law", "/mɔːz lɔː/", "摩尔定律", "The observation that the number of transistors on a microchip doubles roughly every two years."),
            ("Legacy", "/ˈleɡ.ə.si/", "历史遗产，精神传承", "An enduring impact or body of work left behind by a transformative leader.")
        ],
        "timeline": [
            ("1931 · 7月", "张忠谋出生于浙江宁波，开启横跨动荡与变革的世纪人生。"),
            ("1949 · 9月", "赴美求学，先后就读哈佛大学与麻省理工学院（MIT）。"),
            ("1958 · 5月", "加入德州仪器（TI），二十五年间跃升全球半导体领军人物。"),
            ("1985 · 8月", "应邀赴台出任工研院院长，擘画台湾半导体未来蓝图。"),
            ("1987 · 2月", "创立台湾积体电路制造公司（TSMC），首创纯晶圆代工模式。"),
            ("2018 · 6月", "台积电市值突破千亿美元，张忠谋正式退休，被尊为「护国神山」之父。"),
            ("2024 · 至今", "台积电先进制程引领全球AI算力革命，纯代工传奇仍在续写。")
        ],
        "quote_zh": "历史没有如果，但思考有。在张忠谋走过的每一个路口，平行世界都在向我们招手。",
        "quote_en": "History has no 'what ifs,' but our contemplation does. At every crossroads Morris Chang walked, parallel worlds beckon."
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
        "tagline_en": "The times may push you along, but who you become is always up to you.",
        "duration": "18:42",
        "pills": [
            ("历史坐标", "广州轰炸 · 香港保卫战 · 珍珠港事变"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第01期-逃难的孩子.png",
        "prev_link": "episode-00.html",
        "prev_label": "← 上一期：第 00 期 全册导读",
        "next_link": "episode-02.html",
        "next_label": "下一期：第 02 期 考不进去的南开与作家梦 →",
        "vocab": [
            ("Refugee", "/ˌref.jʊˈdʒiː/", "难民，逃难者", "A person who has been forced to leave their country in order to escape war, persecution, or natural disaster."),
            ("Sanctuary", "/ˈsæŋk.tʃʊə.ri/", "避难所，庇护所", "A place of safety or protection, as Hong Kong initially served before December 1941."),
            ("Displacement", "/dɪsˈpleɪs.mənt/", "流离失所，流徙", "The enforced departure of people from their homes, typical of wartime China."),
            ("Resilience", "/rɪˈzɪl.jəns/", "坚韧，复原力", "The capacity to recover quickly from difficulties; toughness in character."),
            ("Turbulence", "/ˈtɜː.bjə.ləns/", "动荡，骚乱", "A state of conflict, confusion, or lack of order during wartime."),
            ("Exile", "/ˈek.saɪl/", "流亡，离乡背井", "The state of being barred from one's native country, typically for political or wartime reasons."),
            ("Perseverance", "/ˌpɜː.sɪˈvɪə.rəns/", "锲而不舍，坚持不懈", "Persistence in doing something despite difficulty or delay in achieving success."),
            ("Destiny", "/ˈdes.tɪ.ni/", "命运，宿命", "The events that will necessarily happen to a particular person or thing in the future.")
        ],
        "timeline": [
            ("1931 · 7月", "张忠谋出生于浙江宁波，父张蔚观，母胡秉祥。"),
            ("1937 · 7月-8月", "七七事变后抗战全面爆发，随父母举家避难广州。"),
            ("1938 · 10月", "日军大轰炸并逼近广州，全家乘船逃往香港（九龙界限街）。"),
            ("1941 · 12月", "太平洋战争爆发，日军突袭香港，经历香港保卫战与沦陷。"),
            ("1942 · 夏", "在日据香港就读香港培正小学毕业，准备穿越沦陷区前往重庆。")
        ],
        "quote_zh": "时代可以推着你走，但走成什么样，从来是你自己的事。",
        "quote_en": "The times may push you along, but who you become is always up to you."
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
        "tagline_en": "A warning of 'going hungry' closed one door; yet life's greatest wonder lies in the detours we are forced to take.",
        "duration": "19:15",
        "pills": [
            ("历史坐标", "陪都重庆 · 沙坪坝南开 · 战后上海 · 金圆券危机"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第02期-考不进去的南开与作家梦.png",
        "prev_link": "episode-01.html",
        "prev_label": "← 上一期：第 01 期 逃难的孩子",
        "next_link": "episode-03.html",
        "next_label": "下一期：第 03 期 从黄浦江到查尔斯河 →",
        "vocab": [
            ("Detour", "/ˈdiː.tɔːr/", "弯路，绕行之路", "A long or roundabout course taken unexpectedly instead of the direct way."),
            ("Pragmatism", "/ˈpræɡ.mə.tɪ.zəm/", "实用主义，注重实效", "An approach that assesses the truth of meaning of theories or beliefs in terms of their practical application."),
            ("Inflation", "/ɪnˈfleɪ.ʃən/", "恶性通货膨胀", "A general increase in prices and fall in the purchasing value of money (e.g. Golden Yuan 1948)."),
            ("Aspiration", "/ˌæs.pəˈreɪ.ʃən/", "志向，文学梦与追求", "A hope or ambition of achieving something, such as Morris Chang's early literary dream."),
            ("Rigorous", "/ˈrɪɡ.ər.əs/", "严谨的，严格的", "Extremely thorough and accurate, as seen in Nankai Middle School's training."),
            ("Humanities", "/hjuːˈmæn.ə.tiz/", "人文科学，博雅文史", "Academic disciplines that study human culture, including literature and history."),
            ("Crossroads", "/ˈkrɒs.rəʊdz/", "抉择路口", "A crucial point of decision affecting one's entire future career."),
            ("Versatility", "/ˌvɜː.səˈtɪl.ə.ti/", "通融多能，兼收并蓄", "Ability to adapt or be adapted to many different functions or activities.")
        ],
        "timeline": [
            ("1943 · 春", "全家历经五十天险阻穿越千里沦陷区，抵达战时陪都重庆。"),
            ("1943 · 秋", "报考重庆南开中学初中未被录取，入读暑期补习班奋起直追，终以插班第一考入。"),
            ("1945 · 8月", "抗战胜利，迁往上海就读上海市南洋模范中学，饱览中西文学经典。"),
            ("1948 · 8月", "国民政府发行金圆券引发恶性通胀，父亲劝阻其作家梦想，建议投身实用工科。"),
            ("1948 · 冬", "国共内战局势突变，全家再次南下香港避难。")
        ],
        "quote_zh": "一个「会饿肚子」的警告，关上了一扇门；但生命最奇妙的，正是那些不得不拐的弯。",
        "quote_en": "A warning of 'going hungry' closed one door; yet life's greatest wonder lies in the detours we are forced to take."
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
        "tagline_en": "In the chasm between two civilizations, he learned to calibrate his entire life against the world.",
        "duration": "22:08",
        "pills": [
            ("历史坐标", "1949国共易手 · 泛美航空 · 哈佛大一 · 转学MIT"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第03期-从黄浦江到查尔斯河.png",
        "prev_link": "episode-02.html",
        "prev_label": "← 上一期：第 02 期 考不进去的南开与作家梦",
        "next_link": "episode-04.html",
        "next_label": "下一期：第 04 期 四十封求职信 →",
        "vocab": [
            ("Odyssey", "/ˈɒd.ɪ.si/", "漫长而充满冒险的史诗旅程", "A long and eventful or adventurous journey or transition."),
            ("Acculturation", "/əˌkʌl.tʃəˈreɪ.ʃən/", "文化适应，文化融合", "Assimilation to a different culture, typically the dominant one."),
            ("Liberal Arts", "/ˌlɪb.ər.əl ˈɑːts/", "博雅教育，通识人文", "Academic subjects such as literature, philosophy, and history rather than technical science."),
            ("Pivot", "/ˈpɪv.ət/", "关键转折，战略转向", "A crucial turning point or shift in strategy and career direction."),
            ("Cosmopolitan", "/ˌkɒz.məˈpɒl.ɪ.tən/", "世界主义的，开阔的", "Familiar with and at ease in many different countries and cultures."),
            ("Assimilation", "/əˌsɪm.ɪˈleɪ.ʃən/", "同化与融入", "The process of taking in and fully understanding information or ideas from a culture."),
            ("Orientation", "/ˌɔː.ri.enˈteɪ.ʃən/", "方向定位，价值取向", "The determination of the relative position of something or someone."),
            ("Transformation", "/ˌtræns.fəˈmeɪ.ʃən/", "蜕变，深刻变革", "A marked change in form, nature, or appearance.")
        ],
        "timeline": [
            ("1949 · 2月-9月", "在香港暂居七个月，办理赴美留学签证与准备手续。"),
            ("1949 · 9月", "搭乘泛美航空波音客机飞越太平洋抵美，成为哈佛大学当年唯一中国本科新生。"),
            ("1949–1950", "在哈佛度过极为充实的人文通识教育一年，沉浸于莎士比亚与西方文明经典。"),
            ("1950 · 6月", "因考虑未来在美生存与就业现实，决定转入麻省理工学院（MIT）机械工程系。"),
            ("1950 · 秋", "跨过查尔斯河进入MIT，开始高强度的工程技术训练。")
        ],
        "quote_zh": "在两座文明的裂缝之间，他学会了以世界为坐标校准自己的一生。",
        "quote_en": "In the chasm between two civilizations, he learned to calibrate his entire life against the world."
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
        "tagline_en": "Rejection is not the end; it is destiny pointing to another road—leading toward the golden age of semiconductors.",
        "duration": "21:54",
        "pills": [
            ("历史坐标", "MIT博士两次落第 · 福特vs希凡尼亚 · 晶体管萌芽 · 德仪新篇"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第04期-四十封求职信.png",
        "prev_link": "episode-03.html",
        "prev_label": "← 上一期：第 03 期 从黄浦江到查尔斯河",
        "next_link": "episode-05.html",
        "next_label": "下一期：第 05 期 隔岸观火的叛乱 →",
        "vocab": [
            ("Setback", "/ˈset.bæk/", "挫折，逆境", "A reversal or check in progress; the failure of MIT doctoral qualifying exams."),
            ("Semiconductor", "/ˌsem.i.kənˈdʌk.tər/", "半导体", "A solid substance with conductivity between insulator and conductor, altering world history."),
            ("Transistor", "/trænˈzɪs.tər/", "晶体管", "A semiconductor device used to amplify or switch electrical signals and power."),
            ("Fortitude", "/ˈfɔː.tɪ.tjuːd/", "刚毅，不屈不挠的勇气", "Courage in pain or adversity; the tenacity shown during the job hunt."),
            ("Negotiation", "/nɪˌɡəʊ.ʃiˈeɪ.ʃən/", "薪酬博弈与谈判", "Discussion aimed at reaching an agreement, famously demonstrated over the $1 pay gap."),
            ("Germanium", "/dʒɜːˈmeɪ.ni.əm/", "锗（早期半导体材料）", "A chemical element widely used in early transistors before silicon became standard."),
            ("Self-taught", "/ˌselfˈtɔːt/", "无师自通，自学成才", "Having acquired knowledge or skill on one's own initiative rather than through formal instruction."),
            ("Opportunity", "/ˌɒp.əˈtjuː.nə.ti/", "时代机遇", "A set of circumstances that makes it possible to do something transformative.")
        ],
        "timeline": [
            ("1952–1953", "在MIT获得机械工程学士及硕士学位。"),
            ("1954 · 2月&5月", "连续两次未通过MIT博士资格考试，遭遇人生迄今最沉重的学术打击。"),
            ("1955 · 春", "寄出四十封求职信；因1美元薪资差额选择加入希凡尼亚（Sylvania）半导体部门。"),
            ("1955–1958", "在希凡尼亚从零自学半导体物理与锗晶体管制造，快速晋升为研发部门主管。"),
            ("1958 · 5月", "接受德州仪器（TI）邀请移居达拉斯，正式踏上半导体之巅的传奇征程。")
        ],
        "quote_zh": "被拒绝不是终点，是命运在给你指另一条路——通向半导体的黄金时代。",
        "quote_en": "Rejection is not the end; it is destiny pointing to another road—leading toward the golden age of semiconductors."
    },
    {
        "id": "05",
        "file_name": "episode-05.html",
        "folder": "第05期-隔岸观火的叛乱",
        "act_tag": "ACT 05 · 1957–1958 · 硅谷初生与仙童叛乱",
        "title_zh": "第 05 期：隔岸观火的叛乱",
        "title_en": "Episode 05: Watching the Rebellion from Afar",
        "time_loc": "1957–1958 · 波士顿至达拉斯",
        "tagline_zh": "当一群年轻人掀翻旧桌子时，远在东岸的他看懂了一件事：规则要由下场的人来定。",
        "tagline_en": "When a group of young men overturned the old table, he understood from the East Coast: rules are written by those in the arena.",
        "duration": "21:05",
        "pills": [
            ("历史坐标", "肖克利半导体 · 八叛逆与仙童成立 · 硅谷得名 · 德仪达拉斯邀约"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第05期-隔岸观火的叛乱.png",
        "prev_link": "episode-04.html",
        "prev_label": "← 上一期：第 04 期 四十封求职信",
        "next_link": "episode-06.html",
        "next_label": "下一期：第 06 期 德仪的太空竞赛岁月 →",
        "vocab": [
            ("Traitorous Eight", "/ˈtreɪ.tər.əs eɪt/", "八叛逆", "The group of eight employees who left Shockley Semiconductor in 1957 to co-found Fairchild Semiconductor."),
            ("Disruption", "/dɪsˈrʌp.ʃən/", "颠覆式创新", "Radical change in an existing industry or market through technological innovation."),
            ("Incubation", "/ˌɪŋ.kjʊˈbeɪ.ʃən/", "孵化，培育", "The development of nascent technology and venture startups in fertile ecosystems."),
            ("Silicon Valley", "/ˈsɪl.ɪ.kən ˈvæl.i/", "硅谷", "The global epicenter of high-tech innovation in the southern San Francisco Bay Area."),
            ("Venture Capital", "/ˈven.tʃər ˈkæp.ɪ.təl/", "风险投资", "Capital invested in a project in which there is a substantial element of risk, typically new businesses."),
            ("Defection", "/dɪˈfek.ʃən/", "出走，离职叛逃", "The conscious abandonment of loyalty or allegiance to an established institution."),
            ("Ecosystem", "/ˈiː.kəʊˌsɪs.təm/", "产业生态系统", "A complex network of interconnected companies, suppliers, and talents driving industry growth."),
            ("Foresight", "/ˈfɔː.saɪt/", "远见卓识", "The ability to predict or the action of predicting what will happen or be needed in the future.")
        ],
        "timeline": [
            ("1956 · 11月", "威廉·肖克利因发明晶体管荣获诺贝尔物理学奖，在加州创立肖克利半导体。"),
            ("1957 · 9月", "肖克利实验室八位核心科学家（八叛逆）集体辞职出走。"),
            ("1957 · 10月", "在阿瑟·洛克引荐下获得谢尔曼·仙童资助，仙童半导体（Fairchild）正式成立。"),
            ("1957–1958", "张忠谋在东岸希凡尼亚密切关注西岸晶体管技术革命与产业剧变。"),
            ("1958 · 5月", "张忠谋离开希凡尼亚，接受德州仪器（TI）邀请迁往达拉斯。")
        ],
        "quote_zh": "当一群年轻人掀翻旧桌子时，远在东岸的他看懂了一件事：规则要由下场的人来定。",
        "quote_en": "When a group of young men overturned the old table, he understood from the East Coast: rules are written by those in the arena."
    },
    {
        "id": "06",
        "file_name": "episode-06.html",
        "folder": "第06期-德仪的太空竞赛岁月",
        "act_tag": "ACT 06 · 1958–1964 · 德仪与集成电路",
        "title_zh": "第 06 期：德仪的太空竞赛岁月",
        "title_en": "Episode 06: The Space Race Years at Texas Instruments",
        "time_loc": "1958–1964 · 达拉斯与斯坦福",
        "tagline_zh": "冷战的火箭把人类送进太空，也把集成电路推上了历史的浪尖。他在达拉斯看到了未来。",
        "tagline_en": "Cold War rockets thrust humanity into space and propelled the integrated circuit to the crest of history. In Dallas, he saw the future.",
        "duration": "20:51",
        "pills": [
            ("历史坐标", "基尔比集成电路 · 阿波罗登月计划 · 德仪资助斯坦福博士 · 良率突破"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第06期-德仪的太空竞赛岁月.png",
        "prev_link": "episode-05.html",
        "prev_label": "← 上一期：第 05 期 隔岸观火的叛乱",
        "next_link": "episode-07.html",
        "next_label": "下一期：第 07 期 半导体之巅的十年 →",
        "vocab": [
            ("Integrated Circuit", "/ˈɪn.tɪ.ɡreɪ.tɪd ˈsɜː.kɪt/", "集成电路（IC）", "An electronic circuit formed on a small piece of semiconducting material, performing the same function as a larger circuit."),
            ("Space Race", "/ˈspeɪs reɪs/", "太空竞赛", "The 20th-century competition between Cold War adversaries USSR and USA for dominance in spaceflight capability."),
            ("Yield Rate", "/jiːld reɪt/", "良品率，晶圆良率", "The percentage of non-defective manufactured chips produced on a semiconductor wafer."),
            ("Sponsorship", "/ˈspɒn.sə.ʃɪp/", "企业全额资助培养", "Financial support given by TI to send Morris Chang to Stanford for his Ph.D. in electrical engineering."),
            ("Miniaturization", "/ˌmɪn.i.ə.tʃə.raɪˈzeɪ.ʃən/", "微型化", "The design and manufacture of ever smaller electrical components and chips."),
            ("Aerospace", "/ˈeə.rəʊ.speɪs/", "航天航空工业", "The branch of technology and industry concerned with aviation and space flight."),
            ("Breakthrough", "/ˈbreɪk.θruː/", "重大技术突破", "A sudden, dramatic, and important discovery or development."),
            ("Tenacity", "/təˈnæs.ə.ti/", "坚毅与顽强", "The quality or fact of being very determined; determination.")
        ],
        "timeline": [
            ("1958 · 9月", "杰克·基尔比在德州仪器实验室成功发明世界上第一块集成电路（IC）。"),
            ("1958–1961", "张忠谋在德仪大幅提升锗晶体管与硅晶体管良品率，获公司高层极度赏识。"),
            ("1961 · 秋", "德仪全薪全额资助张忠谋前往斯坦福大学攻读电气工程博士学位。"),
            ("1964 · 2月", "以两年半创纪录速度顺利通过斯坦福博士答辩，重返德州仪器达拉斯总部。"),
            ("1964 · 夏", "升任德仪锗三极管研发及生产总经理，全面统领核心业务部门。")
        ],
        "quote_zh": "冷战的火箭把人类送进太空，也把集成电路推上了历史的浪尖。他在达拉斯看到了未来。",
        "quote_en": "Cold War rockets thrust humanity into space and propelled the integrated circuit to the crest of history. In Dallas, he saw the future."
    },
    {
        "id": "07",
        "file_name": "episode-07.html",
        "folder": "第07期-半导体之巅的十年",
        "act_tag": "ACT 07 · 1964–1974 · 德仪全球副总裁",
        "title_zh": "第 07 期：半导体之巅的十年",
        "title_en": "Episode 07: The Decade at the Summit of Semiconductors",
        "time_loc": "1964–1974 · 达拉斯与全球扩张",
        "tagline_zh": "坐在全球半导体的王座上，他发现决定胜负的不仅是技术，更是学习曲线上的疯狂下杀。",
        "tagline_en": "Sitting atop the semiconductor throne, he discovered victory was decided not just by technology, but by ruthless learning curve pricing.",
        "duration": "21:29",
        "pills": [
            ("历史坐标", "德仪全球副总裁 · 学习曲线定价策略 · 全球建厂 · 30000名跨国员工"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第07期-半导体之巅的十年.png",
        "prev_link": "episode-06.html",
        "prev_label": "← 上一期：第 06 期 德仪的太空竞赛岁月",
        "next_link": "episode-08.html",
        "next_label": "下一期：第 08 期 离开德州与受邀回台 →",
        "vocab": [
            ("Learning Curve", "/ˈlɜː.nɪŋ kɜːv/", "学习曲线理论", "The concept that cumulative production volume reduces manufacturing cost by a predictable percentage."),
            ("Aggressive Pricing", "/əˈɡres.ɪv ˈpraɪ.sɪŋ/", "进攻性定价策略", "Lowering prices in anticipation of future cost declines to deter competitors and gain dominant market share."),
            ("Global Footprint", "/ˈɡləʊ.bəl ˈfʊt.prɪnt/", "全球制造足迹", "Establishing multi-national manufacturing and packaging facilities across Asia and Latin America."),
            ("Vice President", "/vaɪs ˈprez.ɪ.dənt/", "全球副总裁兼总经理", "Executive corporate officer leading enterprise-scale business units and thousands of personnel."),
            ("Scale Advantage", "/skeɪl ədˈvɑːn.tɪdʒ/", "规模优势", "Cost advantages that enterprises obtain due to their scale of operation."),
            ("Execution", "/ˌek.sɪˈkjuː.ʃən/", "执行力", "The carrying out or putting into effect of a plan, order, or course of action."),
            ("Dominance", "/ˈdɒm.ɪ.nəns/", "市场主导地位", "Power and influence over others in an industry segment."),
            ("Consolidation", "/kənˌsɒl.ɪˈdeɪ.ʃən/", "行业整合", "The process of uniting separate parts into a single whole or dominant force.")
        ],
        "timeline": [
            ("1967 · 10月", "升任德仪副总裁，掌管德仪全美及全球半导体元件业务。"),
            ("1969 · 夏", "代表德仪赴台湾新竹与中坜考察并投资设立封测工厂。"),
            ("1972 · 12月", "升任德仪全球集团副总裁（Group VP），统领半导体事业部（3万名员工）。"),
            ("1973–1974", "推行激进的学习曲线定价战略，击溃多数竞争对手，确立德仪全球第一芯片霸主地位。"),
            ("1974 · 冬", "德仪战略重心向消费类电子产品（计算器、电子表）转移，内部分歧初现。")
        ],
        "quote_zh": "坐在全球半导体的王座上，他发现决定胜负的不仅是技术，更是学习曲线上的疯狂下杀。",
        "quote_en": "Sitting atop the semiconductor throne, he discovered victory was decided not just by technology, but by ruthless learning curve pricing."
    },
    {
        "id": "08",
        "file_name": "episode-08.html",
        "folder": "第08期-离开德州与受邀回台",
        "act_tag": "ACT 08 · 1983–1985 · 离开德仪与跨海邀约",
        "title_zh": "第 08 期：离开德州与受邀回台",
        "title_en": "Episode 08: Leaving Texas & the Invitation Home",
        "time_loc": "1983–1985 · 达拉斯-纽约-台北",
        "tagline_zh": "五十四岁，有人准备退休，他却把前半生积攒的所有筹码，押上了一场无人看好的赌局。",
        "tagline_en": "At age fifty-four, when others prepare for retirement, he staked all the chips gathered over a lifetime on a gamble no one believed in.",
        "duration": "21:10",
        "pills": [
            ("历史坐标", "告别德州仪器 · 通用仪器总裁 · 孙运璿与李国鼎邀约 · 出任工研院院长"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第08期-离开德州与受邀回台.png",
        "prev_link": "episode-07.html",
        "prev_label": "← 上一期：第 07 期 半导体之巅的十年",
        "next_link": "episode-09.html",
        "next_label": "下一期：第 09 期 纯代工的革命 →",
        "vocab": [
            ("Crossroads", "/ˈkrɒs.rəʊdz/", "十字路口，人生命运转折点", "An intersection of two or more roads; a point at which a crucial decision must be made."),
            ("Resignation", "/ˌrez.ɪɡˈneɪ.ʃən/", "辞职，告别旧舞台", "The act of giving up a position, office, or employment."),
            ("Industrial Technology", "/ɪnˈdʌs.tri.əl tekˈnɒl.ə.dʒi/", "工业技术研究院（ITRI）", "A non-profit applied research institution established to spur industrial innovation in Taiwan."),
            ("Entrepreneurship", "/ˌɒn.trə.prəˈnɜː.ʃɪp/", "二次创业精神", "The activity of setting up a business or taking on financial risks in the hope of profit at mature age."),
            ("Mandate", "/ˈmæn.deɪt/", "使命，历史委托", "An official order or commission to do something; a historic authorization."),
            ("Transition", "/trænˈzɪʃ.ən/", "转型期", "The process or a period of changing from one state or condition to another."),
            ("Conviction", "/kənˈvɪk.ʃən/", "坚定信念", "A firmly held belief or opinion that guides difficult choices."),
            ("Legacy Pivot", "/ˈleɡ.ə.si ˈpɪv.ət/", "生涯转型", "A high-stakes pivot in career aimed at leaving a lasting historical impact.")
        ],
        "timeline": [
            ("1983 · 12月", "因对德仪战略转向消费电子无法苟同，正式辞去德州仪器副总裁职务。"),
            ("1984 · 2月", "加入纽约通用仪器公司（General Instrument）担任总裁兼首席运营官。"),
            ("1985 · 5月", "李国鼎与俞国华数次派员力邀张忠谋回台主持工业技术研究院（ITRI）。"),
            ("1985 · 8月", "辞去通用仪器职位，正式抵达台北，就任工业技术研究院院长。"),
            ("1985 · 冬", "对台湾半导体产业基础进行严密调研，提出颠覆性的「纯晶圆代工」商业构想。")
        ],
        "quote_zh": "五十四岁，有人准备退休，他却把前半生积攒的所有筹码，押上了一场无人看好的赌局。",
        "quote_en": "At age fifty-four, when others prepare for retirement, he staked all the chips gathered over a lifetime on a gamble no one believed in."
    },
    {
        "id": "09",
        "file_name": "episode-09.html",
        "folder": "第09期-纯代工的革命",
        "act_tag": "ACT 09 · 1986–1987 · 台积电诞生与纯代工",
        "title_zh": "第 09 期：纯代工的革命",
        "title_en": "Episode 09: The Pure-Play Revolution",
        "time_loc": "1986–1987 · 新竹科学园区",
        "tagline_zh": "不和客户竞争，只做客户的制造后盾——看似退让的一步，改写了全球芯片工业的游戏规则。",
        "tagline_en": "Do not compete with customers; be their manufacturing backbone. A seemingly humble retreat that rewrote the rules of the global semiconductor game.",
        "duration": "21:00",
        "pills": [
            ("历史坐标", "纯代工商业模式 (Pure-Play Foundry) · 飞利浦注资 · 1987新竹创立 · 无厂半导体诞生"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第09期-纯代工的革命.png",
        "prev_link": "episode-08.html",
        "prev_label": "← 上一期：第 08 期 离开德州与受邀回台",
        "next_link": "index.html",
        "next_label": "回到全册总目录 (下册 第 10 期 敬请期待) →",
        "vocab": [
            ("Pure-Play Foundry", "/pjʊər pleɪ ˈfaʊn.dri/", "纯晶圆代工", "A semiconductor company focused purely on manufacturing wafers for external designers without designing own products."),
            ("Fabless", "/ˈfæb.ləs/", "无晶圆厂芯片设计公司", "Companies that design microchips but outsource hardware fabrication to pure foundry partners (e.g. Nvidia, Qualcomm)."),
            ("IDM", "/ˌaɪ.diːˈem/", "整合元件制造商", "Integrated Device Manufacturer; a company that designs, manufactures, and sells integrated circuits in-house (e.g. Intel, TI)."),
            ("Value Proposition", "/ˈvæl.juː ˌprɒp.əˈzɪʃ.ən/", "核心价值主张", "A statement of the unique value that a business brings to its clients, namely non-competition and absolute trust."),
            ("Confidentiality", "/ˌkɒn.fɪˌden.ʃiˈæl.ə.ti/", "客户机密保护与信赖", "The state of keeping customer designs strictly secret, the cornerstone of TSMC's partnership ethos."),
            ("Capital Intensity", "/ˈkæp.ɪ.təl ɪnˈten.sɪ.ti/", "资本密集型特性", "The amount of fixed capital required in relation to other factors of production in high-end wafer fabs."),
            ("Paradigm Shift", "/ˈpær.ə.daɪm ʃɪft/", "范式转移", "A fundamental change in approach or underlying assumptions in global industrial division of labor."),
            ("Foundational Trust", "/faʊnˈdeɪ.ʃən.əl trʌst/", "基石级客户信任", "The unshakeable commitment that TSMC will never compete with its customers.")
        ],
        "timeline": [
            ("1986 · 春", "张忠谋确立 TSMC 核心商业模式：纯晶圆代工（Pure-Play Foundry），绝不做自有品牌。"),
            ("1986 · 下半年", "完成多方融资谈判，台湾行政院开发基金注资48.3%，荷兰飞利浦（Philips）注资27.5%，民间企业注资24.2%。"),
            ("1987 · 2月21日", "台湾积体电路制造股份有限公司（TSMC）正式注册成立，张忠谋出任董事长。"),
            ("1987 · 5月", "租用工研院实验厂启动量产，首开全球代工商业新范式。"),
            ("1987 · 至今", "孵化全球数千家 Fabless 芯片设计巨头，掀起全球科技产业大分工浪潮。")
        ],
        "quote_zh": "不和客户竞争，只做客户的制造后盾——看似退让的一步，改写了全球芯片工业的游戏规则。",
        "quote_en": "Do not compete with customers; be their manufacturing backbone. A seemingly humble retreat that rewrote the rules of the global semiconductor game."
    }
]

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

for ep in episodes_meta:
    ep_id = ep["id"]
    folder_path = os.path.join(WORKSPACE, "03-剧集", ep["folder"])
    zh_path = os.path.join(folder_path, "中文文字稿.md")
    en_path = os.path.join(folder_path, "英文文字稿.md")
    
    zh_sections = parse_markdown_sections(zh_path)
    en_sections = parse_markdown_sections(en_path)
    
    # Extract cues from audio_js
    m = re.search(r'\{\s*"id":\s*"' + ep_id + r'".*?"cues":\s*(\[.*?\])\s*\}', audio_js, re.DOTALL)
    if m:
        cues = json.loads(m.group(1))
    else:
        cues = []
        
    # Generate HTML content
    pills_html = "".join([f'<span class="pill"><b>{k}：</b>{v}</span>' for k, v in ep["pills"]])
    
    # Cues HTML for teleprompter
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
        # find matching en section
        en_sec_title = en_sections[s_idx][0] if s_idx < len(en_sections) else ""
        en_paras = en_sections[s_idx][1] if s_idx < len(en_sections) else []
        
        sec_paras_html = []
        for p_idx, p_zh in enumerate(paras):
            p_en = en_paras[p_idx] if p_idx < len(en_paras) else ""
            
            # Match time tag with cue
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
    
    html_template = f"""<!DOCTYPE html>
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
  .timeline-list::before {{ content: ""; position: absolute; top: 6px; bottom: 6px; left: 4px; width: 2px; background: var(--line); }}
  .tl-item {{ position: relative; }}
  .tl-item::before {{ content: ""; position: absolute; left: -14px; top: 6px; width: 6px; height: 6px; border-radius: 50%; background: var(--amber); box-shadow: 0 0 8px var(--amber); }}
  .tl-year {{ font-size: 11px; font-weight: 700; color: var(--amber); font-family: monospace; margin-bottom: 2px; }}
  .tl-desc {{ font-size: 12.5px; color: var(--ink); line-height: 1.5; }}

  /* Golden Quote Card */
  .quote-card {{ background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(56,189,248,0.06)); border: 1px solid rgba(245,158,11,0.3); border-radius: 14px; padding: 20px; text-align: center; }}
  .quote-symbol {{ font-size: 32px; color: var(--amber); font-family: var(--serif); line-height: 1; opacity: 0.5; }}
  .quote-zh {{ font-family: var(--serif); font-size: 15px; font-weight: 600; color: var(--ink); line-height: 1.7; margin: 8px 0; }}
  .quote-en {{ font-family: var(--en); font-style: italic; font-size: 13px; color: var(--muted); line-height: 1.5; }}

  /* Episode Footer Navigation */
  .ep-footer-nav {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; margin: 48px 0 24px; padding-top: 24px; border-top: 1px solid var(--line); }}
  .ep-nav-btn {{ display: inline-flex; align-items: center; gap: 8px; padding: 12px 20px; border-radius: 10px; background: var(--card); border: 1px solid var(--line); color: var(--ink); text-decoration: none; font-size: 13.5px; font-weight: 600; transition: all 0.2s; }}
  .ep-nav-btn:hover {{ border-color: var(--amber); color: var(--amber); transform: translateY(-2px); }}
  .ep-nav-btn.primary {{ background: var(--amber); color: #000; border-color: var(--amber); }}
  .ep-nav-btn.primary:hover {{ background: #fbb028; }}

  /* Social Share Bottom Card */
  .share-bottom-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 28px; text-align: center; margin: 40px 0; }}
  .share-bottom-title {{ font-size: 16px; font-weight: 700; color: var(--ink); margin-bottom: 6px; }}
  .share-bottom-sub {{ font-size: 13px; color: var(--muted); margin-bottom: 20px; }}
  .share-matrix-bottom {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }}
  .btn-share-lg {{ padding: 8px 16px; border-radius: 8px; border: 1px solid var(--line); background: var(--bg2); color: var(--ink); font-size: 12.5px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s; }}
  .btn-share-lg:hover {{ border-color: var(--amber); color: var(--amber); transform: translateY(-2px); }}
  .btn-share-lg.primary {{ background: var(--amber); color: #000; border-color: var(--amber); font-weight: 600; }}

  /* WeChat QR Modal */
  .modal-overlay {{ position: fixed; inset: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 1000; }}
  .modal-overlay.active {{ display: flex; }}
  .modal-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 28px; max-width: 360px; text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.8); position: relative; }}
  .modal-close {{ position: absolute; top: 14px; right: 14px; background: transparent; border: none; color: var(--muted); font-size: 20px; cursor: pointer; }}
  .modal-qr-placeholder {{ width: 180px; height: 180px; margin: 16px auto; background: #fff; padding: 10px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }}
  .modal-qr-img {{ width: 100%; height: 100%; object-fit: contain; }}
  .modal-text {{ font-size: 13px; color: var(--muted); line-height: 1.6; }}

  /* Toast Notification */
  .toast {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px); background: var(--amber); color: #000; font-weight: 600; font-size: 13px; padding: 10px 22px; border-radius: 999px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); opacity: 0; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); z-index: 1001; pointer-events: none; }}
  .toast.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}
</style>
</head>
<body>

  <!-- Sticky Navbar -->
  <nav class="nav">
    <a href="index.html" class="brand">
      <img src="logo.svg" alt="Morris Chang & TSMC Logo" class="brand-logo-img">
      <span>台积电张忠谋 · 传记时间线的平行世界</span>
    </a>
    <div class="nav-links">
      <span class="nav-badge">🚀 ReadShift 主体工程</span>
      <a href="index.html" class="nav-link">总目录</a>
      <a href="reader.html" class="nav-link">全册电子书</a>
      <a href="portal.html" class="nav-link">作品官网</a>
    </div>
  </nav>

  <!-- Hero Header (50/50 Balanced Split) -->
  <header class="hero-ep">
    <div class="wrap">
      <span class="eyebrow">{ep["act_tag"]} <em>EPISODE {ep["id"]}</em></span>
      <h1 class="serif">{ep["title_zh"]}<span class="en">{ep["title_en"]}</span></h1>
      
      <div class="hero-split-grid">
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
      </div>
    </div>
  </header>

  <main class="wrap">
    <!-- Audio Player Module -->
    <div class="player-card" id="audio-theater">
      
      <!-- Track Switcher Header with Single-Row Parallel Share Matrix -->
      <div class="track-switcher">
        <div class="track-btns">
          <button class="btn-track active" id="track-btn-zh" onclick="switchTrack('zh')">
            <span class="title-line">中文原声</span>
            <span class="sub-line">Chinese audio</span>
          </button>
          <button class="btn-track" id="track-btn-en" onclick="switchTrack('en')">
            <span class="title-line">美式英语</span>
            <span class="sub-line">American English</span>
          </button>
        </div>

        <!-- 8-Channel Share Bar in parallel space on the same line -->
        <div class="share-matrix-inline">
          <span class="share-label">SHARE / 分享</span>
          <button class="btn-share" onclick="openWeChatShare()" title="微信分享">💬 微信</button>
          <button class="btn-share" onclick="shareToWeibo()" title="微博分享">🔴 微博</button>
          <button class="btn-share" onclick="shareToLinkedIn()" title="LinkedIn 分享">💼 领英</button>
          <button class="btn-share" onclick="shareToX()" title="X (Twitter) 分享">𝕏 X</button>
          <button class="btn-share" onclick="shareToWhatsApp()" title="WhatsApp 分享">📱 WhatsApp</button>
          <button class="btn-share" onclick="shareToTelegram()" title="Telegram 分享">✈️ Telegram</button>
          <button class="btn-share" onclick="shareToFacebook()" title="Facebook 分享">📘 Facebook</button>
          <button class="btn-share" onclick="copyViralShare()" title="复制金句精选分享文案">📋 复制</button>
        </div>
      </div>

      <!-- Main Controls Row -->
      <div class="player-main-ctrl">
        <div class="ctrl-left">
          <button class="play-btn" id="master-play-btn" onclick="togglePlay()" aria-label="播放/暂停">▶</button>
          <div class="track-meta">
            <span class="track-meta-title" id="track-title-display">{ep["title_zh"]} · 中文广播级原声</span>
            <span class="track-meta-sub" id="track-sub-display">{ep["title_en"]} · Mandarin Master Audio ({ep["duration"]})</span>
          </div>
        </div>

        <div class="progress-container">
          <span class="time-text" id="cur-time">00:00</span>
          <input type="range" class="seek-bar" id="seek-bar" min="0" max="100" value="0" step="0.1" oninput="onSeekInput(this.value)" onchange="onSeekChange(this.value)">
          <span class="time-text" id="total-dur">{ep["duration"]}</span>
        </div>

        <div class="playback-options">
          <select class="speed-select" id="speed-select" onchange="changeSpeed(this.value)">
            <option value="0.8">0.8x</option>
            <option value="1.0" selected>1.0x</option>
            <option value="1.25">1.25x</option>
            <option value="1.5">1.5x</option>
            <option value="2.0">2.0x</option>
          </select>
        </div>
      </div>

      <!-- Teleprompter Subtitles Container -->
      <div class="teleprompter-box">
        <div class="teleprompter-header">
          <div class="teleprompter-title">
            <span>🎙️ 逐句高亮字幕提词器</span>
            <b>· 点击任意段落直接跳转试听</b>
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

    <!-- Meta Information Pills Below Audio Module -->
    <div class="meta-pills">
      {pills_html}
    </div>

    <!-- Dual Layout Body: 75% Pure Book + 25% Learning/Notes -->
    <div class="content-grid">
      <!-- 75% Pure Bilingual Book Area -->
      <article class="book-main">
        {book_body_html}
      </article>

      <!-- 25% Learning & Knowledge Sidebar -->
      <aside class="learning-sidebar">
        <!-- Vocab Widget -->
        <div class="side-widget">
          <div class="widget-title"><span class="icon">📖</span> 核心商业/传记词汇</div>
          <div class="vocab-list">
            {vocab_html}
          </div>
        </div>

        <!-- Historical Timeline Widget -->
        <div class="side-widget">
          <div class="widget-title"><span class="icon">⏳</span> 时代历史坐标</div>
          <div class="timeline-list">
            {timeline_html}
          </div>
        </div>

        <!-- Golden Quote Banner Widget -->
        <div class="side-widget quote-card">
          <div class="quote-symbol">“</div>
          <div class="quote-zh">{ep["quote_zh"]}</div>
          <div class="quote-en">{ep["quote_en"]}</div>
        </div>
      </aside>
    </div>

    <!-- Bottom Social Share Card (8 Channels) -->
    <div class="share-bottom-card">
      <div class="share-bottom-title">觉得本期有启发？一键分享给更多创业者与思考者</div>
      <div class="share-bottom-sub">《台积电张忠谋 · 传记时间线的平行世界》系列视听双语典藏</div>
      <div class="share-matrix-bottom">
        <button class="btn-share-lg primary" onclick="copyViralShare()">📋 复制金句分享文案</button>
        <button class="btn-share-lg" onclick="openWeChatShare()">💬 微信朋友圈 / 好友</button>
        <button class="btn-share-lg" onclick="shareToWeibo()">🔴 新浪微博</button>
        <button class="btn-share-lg" onclick="shareToLinkedIn()">💼 LinkedIn 领英</button>
        <button class="btn-share-lg" onclick="shareToX()">𝕏 X (Twitter)</button>
        <button class="btn-share-lg" onclick="shareToWhatsApp()">📱 WhatsApp</button>
        <button class="btn-share-lg" onclick="shareToTelegram()">✈️ Telegram</button>
        <button class="btn-share-lg" onclick="shareToFacebook()">📘 Facebook</button>
      </div>
    </div>

    <!-- Bottom Episode Navigation -->
    <div class="ep-footer-nav">
      <a href="{ep["prev_link"]}" class="ep-nav-btn">{ep["prev_label"]}</a>
      <a href="{ep["next_link"]}" class="ep-nav-btn primary">{ep["next_label"]}</a>
    </div>
  </main>

  <!-- Audio Element -->
  <audio id="main-audio" preload="metadata">
    <source id="audio-source" src="./audio/ep{ep["id"]}-zh.mp3" type="audio/mpeg">
  </audio>

  <!-- WeChat Share Modal -->
  <div class="modal-overlay" id="wechat-modal" onclick="closeWeChatShare()">
    <div class="modal-card" onclick="event.stopPropagation()">
      <button class="modal-close" onclick="closeWeChatShare()">✕</button>
      <h3 style="font-size: 16px; margin-bottom: 8px; color: var(--ink);">微信扫码或复制链接分享</h3>
      <div class="modal-qr-placeholder">
        <!-- Generates QR code via qrserver API dynamically -->
        <img class="modal-qr-img" id="wechat-qr-img" src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=https://martin-mqtech.github.io/morris-chang-tsmc-aigc-parallel/{ep["file_name"]}" alt="WeChat QR Code">
      </div>
      <p class="modal-text">微信扫描上方二维码<br>或点击下方按钮复制完整双语金句卡片</p>
      <button class="btn-share-lg primary" style="margin-top: 14px; width: 100%; justify-content: center;" onclick="copyViralShare()">复制分享链接及文案</button>
    </div>
  </div>

  <!-- Toast Element -->
  <div class="toast" id="toast-msg">已复制金句文案与链接到剪贴板！</div>

  <!-- Client JavaScript Logic -->
  <script>
    const EPISODE_META = {json.dumps(ep, ensure_ascii=False)};
    const EP_CUES = {json.dumps(cues, ensure_ascii=False)};
    
    let currentTrack = 'zh'; // 'zh' or 'en'
    let isPlaying = false;
    let autoScroll = true;
    let activeCueIndex = -1;

    const audioEl = document.getElementById('main-audio');
    const audioSource = document.getElementById('audio-source');
    const playBtn = document.getElementById('master-play-btn');
    const curTimeDisplay = document.getElementById('cur-time');
    const totalDurDisplay = document.getElementById('total-dur');
    const seekBar = document.getElementById('seek-bar');
    const trackTitleDisplay = document.getElementById('track-title-display');
    const trackSubDisplay = document.getElementById('track-sub-display');
    const btnTrackZh = document.getElementById('track-btn-zh');
    const btnTrackEn = document.getElementById('track-btn-en');
    const subtitlesViewport = document.getElementById('subtitles-viewport');
    const btnAutoScroll = document.getElementById('btn-auto-scroll');

    // Master Single Audio Enforcement
    function ensureSingleAudioPlayback(activeAudio) {{
      document.querySelectorAll('audio').forEach(el => {{
        if (el !== activeAudio && !el.paused) {{
          el.pause();
        }}
      }});
      if (window.speechSynthesis && window.speechSynthesis.speaking) {{
        window.speechSynthesis.cancel();
      }}
    }}

    // Switch Audio Track (zh / en)
    function switchTrack(track) {{
      if (currentTrack === track) return;
      
      const prevTime = audioEl.currentTime || 0;
      const prevRatio = audioEl.duration ? (prevTime / audioEl.duration) : 0;
      const wasPlaying = !audioEl.paused;

      currentTrack = track;
      ensureSingleAudioPlayback(audioEl);

      if (track === 'zh') {{
        btnTrackZh.classList.add('active');
        btnTrackEn.classList.remove('active');
        audioSource.src = './audio/ep' + EPISODE_META.id + '-zh.mp3';
        trackTitleDisplay.textContent = EPISODE_META.title_zh + ' · 中文广播级原声';
        trackSubDisplay.textContent = EPISODE_META.title_en + ' · Mandarin Master Audio (' + EPISODE_META.duration + ')';
      }} else {{
        btnTrackEn.classList.add('active');
        btnTrackZh.classList.remove('active');
        audioSource.src = './audio/ep' + EPISODE_META.id + '-en.mp3';
        trackTitleDisplay.textContent = EPISODE_META.title_en + ' · American English Audio';
        trackSubDisplay.textContent = EPISODE_META.title_zh + ' · US English Narration (' + EPISODE_META.duration + ')';
      }}

      audioEl.load();
      audioEl.onloadedmetadata = function() {{
        if (audioEl.duration && prevRatio > 0) {{
          audioEl.currentTime = prevRatio * audioEl.duration;
        }}
        if (wasPlaying) {{
          audioEl.play().catch(e => console.log('Autoplay prevented:', e));
        }}
      }};
      showToast(track === 'zh' ? '已切换至中文广播级原声轨' : 'Switched to American English Audio track');
    }}

    // Toggle Play / Pause
    function togglePlay() {{
      if (audioEl.paused) {{
        ensureSingleAudioPlayback(audioEl);
        audioEl.play().then(() => {{
          isPlaying = true;
          playBtn.textContent = '❚❚';
        }}).catch(e => {{
          console.error('Play failed:', e);
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
      playBtn.textContent = '❚❚';
    }});

    audioEl.addEventListener('pause', () => {{
      isPlaying = false;
      playBtn.textContent = '▶';
    }});

    audioEl.addEventListener('timeupdate', () => {{
      if (!audioEl.duration) return;
      const cur = audioEl.currentTime;
      const dur = audioEl.duration;
      
      // Update progress bar
      const pct = (cur / dur) * 100;
      seekBar.value = pct;
      curTimeDisplay.textContent = formatTime(cur);
      totalDurDisplay.textContent = formatTime(dur);

      // Match Cues with 0.15s advance offset for instant sync
      const syncTime = cur + 0.15;
      let matchedIdx = -1;
      
      for (let i = 0; i < EP_CUES.length; i++) {{
        const c = EP_CUES[i];
        if (syncTime >= c.start && syncTime <= c.end) {{
          matchedIdx = i;
          break;
        }}
        if (syncTime < c.start && i > 0 && syncTime >= EP_CUES[i-1].end) {{
          matchedIdx = i - 1;
          break;
        }}
      }}
      if (matchedIdx === -1 && EP_CUES.length > 0) {{
        if (syncTime >= EP_CUES[EP_CUES.length - 1].end) {{
          matchedIdx = EP_CUES.length - 1;
        }}
      }}

      if (matchedIdx !== -1 && matchedIdx !== activeCueIndex) {{
        setActiveCue(matchedIdx);
      }}
    }});

    function setActiveCue(index) {{
      if (index === activeCueIndex) return;
      
      // Remove previous active classes
      if (activeCueIndex !== -1) {{
        const prevRow = document.getElementById('sub-row-' + activeCueIndex);
        if (prevRow) prevRow.classList.remove('active');
        const prevPara = document.getElementById('para-' + activeCueIndex);
        if (prevPara) prevPara.classList.remove('current-reading');
      }}

      activeCueIndex = index;
      const activeRow = document.getElementById('sub-row-' + index);
      if (activeRow) {{
        activeRow.classList.add('active');
        if (autoScroll && subtitlesViewport) {{
          const rowTop = activeRow.offsetTop;
          const rowHeight = activeRow.offsetHeight;
          const containerHeight = subtitlesViewport.clientHeight;
          subtitlesViewport.scrollTo({{
            top: rowTop - (containerHeight / 2) + (rowHeight / 2),
            behavior: 'smooth'
          }});
        }}
      }}

      const activePara = document.getElementById('para-' + index);
      if (activePara) {{
        activePara.classList.add('current-reading');
      }}
    }}

    function seekAndPlay(timeSec) {{
      ensureSingleAudioPlayback(audioEl);
      audioEl.currentTime = timeSec;
      if (audioEl.paused) {{
        audioEl.play().catch(e => console.log(e));
      }}
    }}

    function onSeekInput(val) {{
      if (!audioEl.duration) return;
      const targetTime = (val / 100) * audioEl.duration;
      curTimeDisplay.textContent = formatTime(targetTime);
    }}

    function onSeekChange(val) {{
      if (!audioEl.duration) return;
      audioEl.currentTime = (val / 100) * audioEl.duration;
    }}

    function changeSpeed(spd) {{
      audioEl.playbackRate = parseFloat(spd);
      showToast('播放倍速已设为 ' + spd + 'x');
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

    // Pronounce single vocabulary word via Web Speech API
    function pronounceWord(word) {{
      ensureSingleAudioPlayback(null);
      if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(word);
        utter.lang = 'en-US';
        utter.rate = 0.9;
        window.speechSynthesis.speak(utter);
      }} else {{
        showToast('当前浏览器不支持语音发音功能');
      }}
    }}

    // Toast Notification helper
    function showToast(msg) {{
      const t = document.getElementById('toast-msg');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => {{
        t.classList.remove('show');
      }}, 2600);
    }}

    // 8-Channel Social Share Suite
    const pageUrl = window.location.href;
    const shareTitle = document.title;
    const viralQuote = '“' + EPISODE_META.tagline_zh + '” —— 聆听《台积电张忠谋 · 传记时间线的平行世界》' + EPISODE_META.title_zh;

    function openWeChatShare() {{
      document.getElementById('wechat-modal').classList.add('active');
    }}

    function closeWeChatShare() {{
      document.getElementById('wechat-modal').classList.remove('active');
    }}

    function shareToWeibo() {{
      const url = 'https://service.weibo.com/share/share.php?url=' + encodeURIComponent(pageUrl) + '&title=' + encodeURIComponent(viralQuote + ' ' + pageUrl);
      window.open(url, '_blank', 'width=620,height=500');
    }}

    function shareToLinkedIn() {{
      const url = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(pageUrl);
      window.open(url, '_blank', 'width=620,height=500');
    }}

    function shareToX() {{
      const tweet = viralQuote + '\\n\\n' + pageUrl;
      const url = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(tweet);
      window.open(url, '_blank', 'width=620,height=500');
    }}

    function shareToWhatsApp() {{
      const url = 'https://api.whatsapp.com/send?text=' + encodeURIComponent(viralQuote + '\\n' + pageUrl);
      window.open(url, '_blank');
    }}

    function shareToTelegram() {{
      const url = 'https://t.me/share/url?url=' + encodeURIComponent(pageUrl) + '&text=' + encodeURIComponent(viralQuote);
      window.open(url, '_blank');
    }}

    function shareToFacebook() {{
      const url = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(pageUrl);
      window.open(url, '_blank', 'width=620,height=500');
    }}

    function copyViralShare() {{
      const textToCopy = '🎙️【双语原声剧场 & 商业典藏】' + EPISODE_META.title_zh + '\\n' +
                         '“' + EPISODE_META.tagline_zh + '”\\n\\n' +
                         '中英双语原声 · 逐句同步字幕 · 75%原著精排 · 25%认知精读\\n' +
                         '立即阅读与收听：' + pageUrl;
      
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(textToCopy).then(() => {{
          showToast('已复制金句文案与完整链接到剪贴板！');
        }}).catch(() => {{
          promptCopy(textToCopy);
        }});
      }} else {{
        promptCopy(textToCopy);
      }}
    }}

    function promptCopy(text) {{
      window.prompt('请按 Ctrl+C / Cmd+C 复制分享内容：', text);
    }}
  </script>
</body>
</html>
"""
    
    out_path = os.path.join(WORKSPACE, ep["file_name"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Generated {ep['file_name']} successfully ({len(html_template)} bytes, {len(cues)} cues, {len(zh_sections)} sections).")

print("All episodes (00-09) built successfully!")
