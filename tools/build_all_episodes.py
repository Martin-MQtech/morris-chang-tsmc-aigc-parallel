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
        "prev_link": "index.html",
        "prev_label": "← 回到总目录",
        "next_link": "episode-02.html",
        "next_label": "下一期：第 02 期 考不进去的南开与作家梦 →",
        "vocab": [
            ("Refugee", "/ˌref.jʊˈdʒiː/", "难民，逃难者", "A person who has been forced to leave their country in order to escape war, persecution, or natural disaster."),
            ("Sanctuary", "/ˈsæŋk.tʃʊə.ri/", "避难所，庇护所", "A place of safety or protection, as Hong Kong initially served before December 1941."),
            ("Displacement", "/dɪsˈpleɪs.mənt/", "流离失所，流徙", "The enforced departure of people from their homes, typical of wartime China."),
            ("Resilience", "/rɪˈzɪl.jəns/", "坚韧，复原力", "The capacity to recover quickly from difficulties; toughness in character.")
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
            ("Aspiration", "/ˌæs.pəˈreɪ.ʃən/", "志向，文学梦与追求", "A hope or ambition of achieving something, such as Morris Chang's early literary dream.")
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
            ("Pivot", "/ˈpɪv.ət/", "关键转折，战略转向", "A crucial turning point or shift in strategy and career direction.")
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
            ("Fortitude", "/ˈfɔː.tɪ.tjuːd/", "刚毅，不屈不挠的勇气", "Courage in pain or adversity; the tenacity shown during the job hunt.")
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
        "act_tag": "ACT 05 · 1957–1968 · 达拉斯与硅谷",
        "title_zh": "第 05 期：隔岸观火的叛乱",
        "title_en": "Episode 05: The Rebellion Observed from Afar",
        "time_loc": "1957–1968 · 达拉斯与硅谷",
        "tagline_zh": "硅谷的起点不是技术，是八个人敢于离开的勇气。他隔着半个美国看这场叛乱，后来成了他自己的剧本。",
        "tagline_en": "Silicon Valley's genesis was not technology, but the courage of eight to walk away. The rebellion he watched from afar would become his own playbook.",
        "duration": "20:30",
        "pills": [
            ("历史坐标", "叛逆八帮 · 仙童半导体 · 创投起源 · 英特尔诞生"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第05期-隔岸观火的叛乱.png",
        "prev_link": "episode-04.html",
        "prev_label": "← 上一期：第 04 期 四十封求职信",
        "next_link": "episode-06.html",
        "next_label": "下一期：第 06 期 德仪的太空竞赛岁月 →",
        "vocab": [
            ("Traitorous Eight", "/ˈtreɪtərəs eɪt/", "叛逆八帮", "The eight engineers who left Shockley Semiconductor in 1957 to found Fairchild Semiconductor."),
            ("Venture Capital", "/ˈven.tʃər ˈkæp.ɪ.təl/", "风险投资", "Capital invested in a project in which there is a substantial element of risk, pioneered by Arthur Rock."),
            ("Equity", "/ˈek.wɪ.ti/", "股权，资产净值", "The value of the shares issued by a company, central to Silicon Valley's incentive revolution."),
            ("Incubation", "/ˌɪŋ.kjʊˈbeɪ.ʃən/", "孵化，培育", "The process of nurturing and developing early-stage technology enterprises.")
        ],
        "timeline": [
            ("1957 · 秋", "诺伊斯、摩尔等八名工程师离开肖克利实验室，在阿瑟·洛克牵线下创立仙童半导体。"),
            ("1958 · 5月", "张忠谋加入德州仪器达拉斯总部，将IBM委托产线良率从近零拉升至20%以上。"),
            ("1960年代初", "仙童发明硅平面工艺，成为硅谷半导体的「黄埔军校」。"),
            ("1968 · 7月", "诺伊斯与摩尔脱离仙童创立英特尔（Intel），阿瑟·洛克担任董事长，开启股权激励革命。"),
            ("1972", "张忠谋升任TI集团副总裁，在达拉斯隔空与硅谷英特尔展开长达十余年的巅峰正面对决。")
        ],
        "quote_zh": "硅谷的起点不是技术，是八个人敢于离开的勇气；他隔着半个美国看完的那场叛乱，后来成了他自己的剧本。",
        "quote_en": "The genesis of Silicon Valley was not technology, but the courage of eight individuals to walk away; the rebellion he watched from halfway across America became his own playbook."
    },
    {
        "id": "06",
        "file_name": "episode-06.html",
        "folder": "第06期-德仪的太空竞赛岁月",
        "act_tag": "ACT 06 · 1958–1964 · 达拉斯至斯坦福",
        "title_zh": "第 06 期：德仪的太空竞赛岁月",
        "title_en": "Episode 06: TI's Space Race Years",
        "time_loc": "1958–1964 · 达拉斯至斯坦福",
        "tagline_zh": "他在一家赌上太空竞赛的公司里，学会了什么叫技术的信仰；真正的强者，敢于在上升期把自己清零。",
        "tagline_en": "At a company wagering on the space race, he learned true technological faith; the truly formidable dare to reset themselves at their peak.",
        "duration": "19:45",
        "pills": [
            ("历史坐标", "集成电路发明 · NASA阿波罗登月 · 斯坦福电机博士 · 归零再出发"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第06期-德仪的太空竞赛岁月.png",
        "prev_link": "episode-05.html",
        "prev_label": "← 上一期：第 05 期 隔岸观火的叛乱",
        "next_link": "episode-07.html",
        "next_label": "下一期：第 07 期 半导体之巅的十年 →",
        "vocab": [
            ("Integrated Circuit", "/ˈɪn.tɪ.ɡreɪ.tɪd ˈsɜː.kɪt/", "集成电路，芯片", "An electronic circuit formed on a small piece of semiconducting material, invented in 1958."),
            ("Monolithic", "/ˌmɒn.əˈlɪθ.ɪk/", "单片集成的", "Formed of a single large block or crystal; integrated on a single semiconductor substrate."),
            ("Space Race", "/ˈspeɪs reɪs/", "太空竞赛", "The 20th-century competition between cold war rivals for dominance in spaceflight capability."),
            ("Zero-Base", "/ˈzɪə.rəʊ beɪs/", "归零重置", "Starting from an initial point of zero rather than building on previous momentum.")
        ],
        "timeline": [
            ("1958 · 9月12日", "德州仪器新员工杰克·基尔比（Jack Kilby）在实验室成功演示人类首块集成电路。"),
            ("1961 · 5月", "肯尼迪总统宣布阿波罗登月计划；TI集成电路进入民兵导弹与阿波罗导航计算机。"),
            ("1961 · 秋", "张忠谋获TI全薪全额资助，赴斯坦福大学攻读电机工程博士学位。"),
            ("1964 · 初", "以极高效率完成斯坦福博士论文，重返TI达拉斯总部，随即被任命为锗晶体管部总经理。"),
            ("1964–1965", "以深厚半导体物理功底重组生产线，德仪确立全球半导体霸权。")
        ],
        "quote_zh": "他在一家赌上太空竞赛的公司里，学会了什么叫技术的信仰；真正的强者，敢于在上升期把自己清零。",
        "quote_en": "At a company that bet its future on the space race, he learned faith in technology; the truly formidable dare to reset themselves to zero at the height of their ascent."
    },
    {
        "id": "07",
        "file_name": "episode-07.html",
        "folder": "第07期-半导体之巅的十年",
        "act_tag": "ACT 07 · 1964–1978 · 达拉斯德州仪器",
        "title_zh": "第 07 期：半导体之巅的十年",
        "title_en": "Episode 07: A Decade at the Semiconductor Zenith",
        "time_loc": "1964–1978 · 达拉斯德州仪器",
        "tagline_zh": "他赢下了几乎所有战役，却没赢下德仪内部的权力棋局。最难的仗，往往不在市场上，而在会议室里。",
        "tagline_en": "He won almost every battle, yet lost the corporate power game inside TI. The hardest fights are rarely won in the marketplace, but in the boardroom.",
        "duration": "20:25",
        "pills": [
            ("历史坐标", "学习曲线定价 · TI与Intel对垒 · 石油危机 · 权力棋局"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第07期-半导体之巅的十年.png",
        "prev_link": "episode-06.html",
        "prev_label": "← 上一期：第 06 期 德仪的太空竞赛岁月",
        "next_link": "episode-08.html",
        "next_label": "下一期：第 08 期 离开德州与受邀回台 →",
        "vocab": [
            ("Learning Curve", "/ˈlɜː.nɪŋ kɜːv/", "学习曲线，经验曲线", "The rate of a person's progress in gaining experience or a firm's reduction in costs as volume scales."),
            ("Microprocessor", "/ˌmaɪ.krəʊˈprəʊ.ses.ər/", "微处理器，CPU", "An integrated circuit that contains all the functions of a central processing unit of a computer."),
            ("Stagflation", "/stæɡˈfleɪ.ʃən/", "滞胀（停滞性通货膨胀）", "Persistent high inflation combined with high unemployment and stagnant demand."),
            ("Meritocracy", "/ˌmer.ɪˈtɒk.rə.si/", "唯才是用制度", "A government or the holding of power by people selected on the basis of their ability.")
        ],
        "timeline": [
            ("1967", "升任TI副总裁兼集成电路部总经理，首创运用BCG学习曲线进行每季度主动降价。"),
            ("1971–1972", "英特尔发布4004微处理器；张忠谋升任TI集团副总裁兼半导体集团总经理，统领全球最大芯片业务。"),
            ("1973", "第四次中东战争爆发与第一次石油危机，美国制造业陷入十年滞胀。"),
            ("1977–1978", "因与公司最高层战略分歧，主动请求调任消费者产品集团，推出经典语音玩具Speak & Spell。"),
            ("1981", "在TI内部权力斗争中被转任质量与生产力总监，陷入职业生涯至暗低谷。")
        ],
        "quote_zh": "他赢下了几乎所有战役，却没赢下德州仪器内部的权力棋局；最难的仗，往往不在市场上，而在会议室里。",
        "quote_en": "He won almost every battle in the market, but not the political chess match within TI; the hardest struggles are rarely fought in the marketplace, but in conference rooms."
    },
    {
        "id": "08",
        "file_name": "episode-08.html",
        "folder": "第08期-离开德州与受邀回台",
        "act_tag": "ACT 08 · 1978–1987 · 达拉斯·纽约至新竹",
        "title_zh": "第 08 期：离开德州与受邀回台",
        "title_en": "Episode 08: Leaving Texas & The Homeland Calling",
        "time_loc": "1978–1987 · 达拉斯·纽约至新竹",
        "tagline_zh": "离开一个错误的位置，是人生最重要的一步棋；归乡者的赌注——他押上的不是自己的余生，是一个产业的未来。",
        "tagline_en": "Leaving the wrong position is often life's most crucial move; the returnee's gamble—what he wagered was not merely the rest of his life, but the destiny of an entire industry.",
        "duration": "20:10",
        "pills": [
            ("历史坐标", "辞职德仪 · 通用器材 · 李国鼎三顾 · 工研院 · 台积电诞生"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第08期-离开德州与受邀回台.png",
        "prev_link": "episode-07.html",
        "prev_label": "← 上一期：第 07 期 半导体之巅的十年",
        "next_link": "episode-09.html",
        "next_label": "下一期：第 09 期 纯代工的革命 →",
        "vocab": [
            ("Disillusionment", "/ˌdɪs.ɪˈluː.ʒən.mənt/", "幻灭，醒悟", "A feeling of disappointment resulting from the discovery that something is not as good as believed."),
            ("Foundry", "/ˈfaʊn.dri/", "晶圆代工厂", "A factory where microchips are manufactured for other companies."),
            ("Repatriation", "/ˌriː.pæt.riˈeɪ.ʃən/", "归国，重返故土", "The return of someone to their own country or cultural homeland."),
            ("Pure-play", "/pjʊər pleɪ/", "专业专注的，纯粹经营的", "A company that focuses solely on one particular type of product or service.")
        ],
        "timeline": [
            ("1983 · 底", "辞去效力25年的德州仪器职位，彻底切断与达拉斯老东家的关系。"),
            ("1984–1985", "出任纽约通用器材（General Instrument）总裁兼COO，一年后因理念不合离任。"),
            ("1985 · 夏", "应李国鼎、徐贤修、俞国华之邀赴台，出任工业技术研究院（ITRI）院长。"),
            ("1986 · 春-冬", "针对台湾半导体无设计强项但制造良率高的现状，构思出纯晶圆代工模式并全力筹备。"),
            ("1987 · 2月21日", "台湾积体电路制造股份有限公司（TSMC）在新竹科学园区正式创立，张忠谋任董事长。")
        ],
        "quote_zh": "有时候，离开一个错误的位置，是人生最重要的一步棋；归乡者的赌注——他押上的不是自己的余生，是一个产业的未来。",
        "quote_en": "Sometimes, leaving the wrong position is the most decisive move in life; the returnee's wager—he bet not just the remainder of his life, but the future of an entire industry."
    },
    {
        "id": "09",
        "file_name": "episode-09.html",
        "folder": "第09期-纯代工的革命",
        "act_tag": "ACT 09 · 1987–1995 · 新竹科学园区",
        "title_zh": "第 09 期：纯代工的革命",
        "title_en": "Episode 09: The Pure Foundry Revolution",
        "time_loc": "1987–1995 · 新竹科学园区",
        "tagline_zh": "他不造自己的芯片，只造别人的芯片，却改写了整个行业。颠覆者不做主角，做平台，让所有人成为主角。",
        "tagline_en": "He made no chips of his own—only fabricating for others, yet revolutionized the global industry. The true disruptor takes no center stage, but builds the platform where everyone else becomes the protagonist.",
        "duration": "19:50",
        "pills": [
            ("历史坐标", "Fab 1改造 · 纯代工模式 · Fabless无厂浪潮 · 破10亿美元营收"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第09期-纯代工的革命.png",
        "prev_link": "episode-08.html",
        "prev_label": "← 上一期：第 08 期 离开德州与受邀回台",
        "next_link": "episode-10.html",
        "next_label": "下一期：第 10 期 从台湾到世界 →",
        "vocab": [
            ("Fabless", "/ˈfæb.ləs/", "无晶圆厂芯片设计公司", "A company that designs microchips but outsources their actual fabrication to a foundry."),
            ("Yield Rate", "/jiːld reɪt/", "良率，合格品产出率", "The percentage of correctly operating chips on a manufactured semiconductor wafer."),
            ("Ecosystem", "/ˈiː.kəʊˌsɪs.təm/", "商业生态系统", "A complex network of interconnected organizations including suppliers, customers, and partners."),
            ("Disruption", "/dɪsˈrʌp.ʃən/", "颠覆性创新", "Disturbance or radical change in an industry caused by new business models.")
        ],
        "timeline": [
            ("1987", "台积电租用工研院旧产线（Fab 1）上线运营，庄严确立「不与客户竞争」铁律。"),
            ("1988–1990", "英特尔安迪·葛洛夫率队实地认证，促使台积电通过200多项品管严苛考验；建立全资Fab 2。"),
            ("1993", "斥巨资投建台湾首座8吋晶圆厂（Fab 3），良率超越美日巨头。"),
            ("1994 · 9月5日", "台积电在台湾证券交易所正式挂牌上市（股票代号 2330）。"),
            ("1995", "年营收首度突破10亿美元大关，高通、英伟达等全球Fabless巨头生态成型。")
        ],
        "quote_zh": "颠覆者不做主角，做平台——让所有人成为主角；他不造自己的芯片，只造别人的芯片，却改写了整个行业。",
        "quote_en": "Disruptors do not seek the spotlight; they build the platform, allowing everyone else to become the protagonist."
    },
    {
        "id": "10",
        "file_name": "episode-10.html",
        "folder": "第10期-从台湾到世界",
        "act_tag": "ACT 10 · 1995–1998 · 新竹至纽约",
        "title_zh": "第 10 期：从台湾到世界",
        "title_en": "Episode 10: From Taiwan to the World",
        "time_loc": "1995–1998 · 新竹至纽约",
        "tagline_zh": "当风暴来时，扎实的企业反而被看见。亚洲金融风暴里，一家台湾公司站上了世界舞台。",
        "tagline_en": "When the storm hits, solid enterprises stand out all the clearer. Amidst the Asian Financial Crisis, a Taiwanese company rose to the world stage.",
        "duration": "18:59",
        "pills": [
            ("历史坐标", "亚洲金融风暴 · 纽交所敲钟 · 商业周刊25最佳经理人 · 自传上册出版"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第10期-从台湾到世界.png",
        "prev_link": "episode-09.html",
        "prev_label": "← 上一期：第 09 期 纯代工的革命",
        "next_link": "episode-11.html",
        "next_label": "下一期：第 11 期 记忆体的诱惑 →",
        "vocab": [
            ("Depreciation", "/dɪˌpriː.ʃiˈeɪ.ʃən/", "贬值，折旧", "A reduction in the value of an asset or national currency over time."),
            ("ADR", "/ˌeɪ.diːˈɑːr/", "美国存托凭证", "American Depositary Receipt, allowing US investors to trade foreign company shares."),
            ("Tenacity", "/təˈnæs.ə.ti/", "坚忍，沉着定力", "The quality or fact of being able to grip something firmly; determination in crisis."),
            ("Benchmark", "/ˈbentʃ.mɑːk/", "基准，行业标杆", "A standard or point of reference against which things may be compared or assessed.")
        ],
        "timeline": [
            ("1997 · 7月", "泰国放弃固定汇率引发泰铢暴跌，亚洲金融风暴全面席卷东亚经济体。"),
            ("1997 · 10月8日", "台积电赴纽约证券交易所挂牌发行ADR，成为首家在华尔街上市的中国台湾企业。"),
            ("1998 · 1月", "美国《商业周刊》（BusinessWeek）评选张忠谋为全球年度最佳25位经理人之一。"),
            ("1998 · 秋", "《张忠谋自传》上册出版，全景回顾1931–1964年传奇求学与德仪岁月。"),
            ("1998 · 底", "台积电在全球代工市占率突破50%，成为世界半导体基础设施中不可或缺的基石。")
        ],
        "quote_zh": "当风暴来时，扎实的企业反而被看见；在动荡中保持定力，世界自会为你让路。",
        "quote_en": "When the storm strikes, solid enterprises are seen most clearly; retain your composure in upheaval, and the world will make way."
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
        "tagline_en": "Temptation is seductive because it masquerades as opportunity. The truly formidable are those who can still hear the tolling bell of cycles amidst the revelry.",
        "duration": "21:18",
        "pills": [
            ("历史坐标", "世界先进 · DRAM价格雪崩 · 三星记忆体霸权 · 德碁世大购并"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第11期-记忆体的诱惑.png",
        "prev_link": "episode-10.html",
        "prev_label": "← 上一期：第 10 期 从台湾到世界",
        "next_link": "episode-12.html",
        "next_label": "下一期：第 12 期 逆周期的定力 →",
        "vocab": [
            ("Commodity", "/kəˈmɒd.ə.ti/", "大宗标准商品", "A raw material or standard product that can be bought and sold with little qualitative difference."),
            ("DRAM", "/ˈdiː.ræm/", "动态随机存取记忆体", "Dynamic Random-Access Memory, a type of semiconductor memory widely used in computers."),
            ("Boom-Bust", "/buːm bʌst/", "繁荣与萧条交替的周期", "A process of economic expansion and contraction that occurs repeatedly."),
            ("Divestiture", "/daɪˈves.tɪ.tʃər/", "剥离，断舍离退出", "The action or process of selling off subsidiary business interests or investments.")
        ],
        "timeline": [
            ("1994", "工研院次微米计划衍生「世界先进」（VIS），台积电作为唯一投标人主导成立。"),
            ("1996–1997", "DRAM价格雪崩跌去超80%，全球记忆体厂商陷入巨额亏损深渊。"),
            ("1998", "三星李健熙早餐会展现记忆体规模杀伤力；张忠谋坚定反思记忆体业务重创教训。"),
            ("1999–2000", "台积电购并德碁半导体与世大积体电路，蔡力行果断提议将产线全数转型代工。"),
            ("2000 · 7月", "台积电创下1662亿新台币历史新高营收，但在狂欢之夜敏锐警惕周期下行乌云。")
        ],
        "quote_zh": "诱惑之所以是诱惑，是因为它长得像机会；真正的强者，是在狂欢里还能听见周期钟声的人。",
        "quote_en": "Temptation is seductive because it masquerades as opportunity; the truly formidable are those who hear the bell of cycle inflection even at the height of celebration."
    },
    {
        "id": "12",
        "file_name": "episode-12.html",
        "folder": "第12期-逆周期的定力",
        "act_tag": "ACT 12 · 2001–2003 · 互联网泡沫破裂",
        "title_zh": "第 12 期：逆周期的定力",
        "title_en": "Episode 12: The Poise of Counter-Cyclicality",
        "time_loc": "2001–2003 · 互联网泡沫破裂",
        "tagline_zh": "周期不是用来恐惧的，是用来踩节奏的；定力，是一个领导者最昂贵的资产。",
        "tagline_en": "Economic cycles are not meant to be feared, but to set your rhythm; steadfast poise is a leader's most priceless asset.",
        "duration": "18:17",
        "pills": [
            ("历史坐标", "半导体史上最惨衰退 · 直线投资理念 · 绝不裁员承诺 · 0.13微米铜制程"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第12期-逆周期的定力.png",
        "prev_link": "episode-11.html",
        "prev_label": "← 上一期：第 11 期 记忆体的诱惑",
        "next_link": "episode-13.html",
        "next_label": "下一期：第 13 期 交棒之痛 →",
        "vocab": [
            ("Counter-Cyclical", "/ˌkaʊn.təˈsɪk.lɪ.kəl/", "逆周期的", "Moving in the opposite direction of the overall economic cycle or industry downturn."),
            ("Downturn", "/ˈdaʊn.tɜːn/", "经济低迷期，衰退", "A decline in economic, business, or other activity."),
            ("Straight-Line", "/streɪt laɪn/", "直线平准投资法", "Maintaining constant, measured capacity expansion regardless of short-term quarterly swings."),
            ("Retention", "/rɪˈten.ʃən/", "人才留存，维系", "The continued possession, use, or control of key skilled engineering personnel.")
        ],
        "timeline": [
            ("2000 · 末", "全球互联网泡沫破灭，半导体行业迎来1964年以来第七次、也是史上最惨烈衰退。"),
            ("2001", "全球芯片市场暴跌32%，各大半导体厂商相继大规模裁员关厂。"),
            ("2001–2002", "张忠谋在台积电全面贯彻「直线投资」理念：不裁员、不缩减核心研发，逆势投资建厂。"),
            ("2003 · 初", "台积电率先突破0.13微米铜制程技术难关，良率大幅碾压主要竞争对手联电。"),
            ("2003 · 底", "半导体市场全面复苏，台积电以充沛产能和领先工艺一举夺取全球代工过半份额。")
        ],
        "quote_zh": "周期不是用来恐惧的，是用来踩节奏的；定力，是一个领导者最昂贵的资产。",
        "quote_en": "Economic cycles are not meant to be feared, but to calibrate your cadence; steadfast poise is a leader's most expensive asset."
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
        "tagline_en": "Surrendering power requires courage; taking it back requires even greater resolve—and both times, it was done for the very same enterprise.",
        "duration": "19:46",
        "pills": [
            ("历史坐标", "交棒蔡力行 · 2008金融海啸 · 840人裁员风波 · 78岁重任CEO"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第13期-交棒之痛.png",
        "prev_link": "episode-12.html",
        "prev_label": "← 上一期：第 12 期 逆周期的定力",
        "next_link": "episode-14.html",
        "next_label": "下一期：第 14 期 绚烂年代 →",
        "vocab": [
            ("Succession", "/səkˈseʃ.ən/", "接班传承，继任", "The action or process of inheriting a title, office, or leadership position."),
            ("Stewardship", "/ˈstjuː.əd.ʃɪp/", "掌舵责任，管家职守", "The job of supervising or taking care of something, such as an organization or company culture."),
            ("Severance", "/ˈsev.ər.əns/", "遣散费，解雇补偿", "The state of being separated or pay given upon termination of employment."),
            ("Reinstatement", "/ˌriː.ɪnˈsteɪt.mənt/", "复职，重新归位", "The action of giving someone back their former position, status, or job.")
        ],
        "timeline": [
            ("2005 · 7月", "74岁的张忠谋卸下CEO职位，正式交棒给战将蔡力行，自己专任董事长。"),
            ("2008 · 9月", "雷曼兄弟倒闭引爆全球金融海啸，半导体订单遭遇断崖式下滑。"),
            ("2009 · 1月", "台积电以考核机制变相裁员840人，引发员工抗议与严重企业文化信任危机。"),
            ("2009 · 5月", "张忠谋与离职员工代表直接对话，承诺全数迎回离职同仁并补足薪资。"),
            ("2009 · 6月11日", "78岁高龄的张忠谋宣布重新兼任CEO，以铁腕和担当重整台积电军心。")
        ],
        "quote_zh": "把权力交出去需要勇气，把它拿回来需要更大的勇气——而两次，都是为了同一家公司。",
        "quote_en": "Relinquishing power demands courage, but taking it back demands even greater fortitude—and both times, it was done for the selfsame company."
    },
    {
        "id": "14",
        "file_name": "episode-14.html",
        "folder": "第14期-绚烂年代",
        "act_tag": "ACT 14 · 2009–2012 · 78岁重披战袍",
        "title_zh": "第 14 期：绚烂年代",
        "title_en": "Episode 14: The Splendid Era",
        "time_loc": "2009–2012 · 78岁重披战袍",
        "tagline_zh": "老骥伏枥，志在千里。年龄从不决定一个人还能不能战斗，只决定他敢不敢再上战场。",
        "tagline_en": "An old steed in the stable still aspires to gallop a thousand miles. Age never dictates whether a warrior can fight—only whether he dares return to the arena.",
        "duration": "18:23",
        "pills": [
            ("历史坐标", "40纳米良率危机 · 黄仁勋书房48小时 · 研发定8% · 28纳米大包圆"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第14期-绚烂年代.png",
        "prev_link": "episode-13.html",
        "prev_label": "← 上一期：第 13 期 交棒之痛",
        "next_link": "episode-15.html",
        "next_label": "下一期：第 15 期 苹果来敲门 →",
        "vocab": [
            ("Resurgence", "/rɪˈsɜː.dʒəns/", "强势复兴，再现辉煌", "An increase or revival after a period of little activity, popularity, or occurrence."),
            ("R&D Intensity", "/ɑːr en diː ɪnˈten.sə.ti/", "研发强度（营收占比）", "The ratio of research and development expenditure to total business revenue."),
            ("Capex", "/ˈkæp.eks/", "资本支出", "Capital expenditure, money spent by a business on acquiring or maintaining fixed assets."),
            ("Wager", "/ˈweɪ.dʒər/", "下注，重磅赌注", "More formal term for bet; a risk taken on a critical outcome.")
        ],
        "timeline": [
            ("2009 · 6月", "回任CEO面对40纳米良率仅20–30%的严重卡壳危机，令刘德音每日直接报告进展。"),
            ("2009 · 7月15日", "亲赴加州在黄仁勋书房展开披萨长谈，以48小时死线化解上亿美元辉达供货索赔案。"),
            ("2009 · 秋", "在牛肉面馆亲自说服已退休的蒋尚义重回台积电掌管研发。"),
            ("2010", "顶住董事会压力将研发支出永久锁定为营收的8%，并将资本支出翻倍至59亿美元。"),
            ("2011–2012", "台积电28纳米制程大获全胜，独家包揽全球移动芯片市场绝大多数订单。")
        ],
        "quote_zh": "老骥伏枥，志在千里；年龄从不决定一个人还能不能战斗，只决定他敢不敢再上战场。",
        "quote_en": "Age never determines whether one can still wage battle, only whether one possesses the fortitude to step onto the battlefield once more."
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
        "tagline_en": "The most demanding customer is the ultimate whetstone—forcing you to forge capabilities no competitor can match.",
        "duration": "18:27",
        "pills": [
            ("历史坐标", "郭台铭引荐苹果高管 · 举债71亿美元 · 20纳米半节点 · 独家A8芯片"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第15期-苹果来敲门.png",
        "prev_link": "episode-14.html",
        "prev_label": "← 上一期：第 14 期 绚烂年代",
        "next_link": "episode-16.html",
        "next_label": "下一期：第 16 期 摩尔定律的守卫者 →",
        "vocab": [
            ("Whetstone", "/ˈwet.stəʊn/", "磨刀石，严苛考验", "A fine-grained stone used for sharpening cutting tools; a metaphor for demanding clients."),
            ("Exclusivity", "/ˌek.skluːˈsɪv.ə.ti/", "独家性，专属性", "The practice of excluding all others; sole supplier relationship."),
            ("Half-Node", "/hɑːf nəʊd/", "半代制程节点", "An intermediate semiconductor process node between two major standardized generations."),
            ("Synergy", "/ˈsɪn.ə.dʒi/", "协同效应", "The interaction or cooperation of two organizations to produce a combined effect greater than the sum of separate effects.")
        ],
        "timeline": [
            ("2010 · 11月9日", "郭台铭携苹果COO杰夫·威廉姆斯（Jeff Williams）夜访张忠谋台北家中，开启合作序幕。"),
            ("2011 · 春", "苹果因三星自研Galaxy手机与其决裂，张忠谋飞赴库比蒂诺会见库克，敲定战略代工意向。"),
            ("2011–2013", "台积电发行71亿美元公司债全力扩产建厂，但坚持「只承诺客户一半需求」的审慎原则。"),
            ("2013", "在20纳米制程上实现良率惊险跨越，彻底甩开竞争对手。"),
            ("2014 · 秋", "搭载台积电独家代工A8处理器的iPhone 6发布，全球狂销上亿台，开启十年苹果深度结盟。")
        ],
        "quote_zh": "最挑剔的客户，是最好的磨刀石——它逼你长出别人没有的能力。",
        "quote_en": "The most exacting customer serves as the finest whetstone—compelling you to forge capabilities that none other possess."
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
        "tagline_en": "When Moore's Law began to age and the world asked 'shall we still chase it?', he answered through a decade: chase it, until you are the last one standing.",
        "duration": "18:04",
        "pills": [
            ("历史坐标", "摩尔定律极限 · 百亿美元年资本支出 · 7纳米独霸世界 · 格罗方德退赛"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第16期-摩尔定律的守卫者.png",
        "prev_link": "episode-15.html",
        "prev_label": "← 上一期：第 15 期 苹果来敲门",
        "next_link": "episode-17.html",
        "next_label": "下一期：第 17 期 交棒与退休 →",
        "vocab": [
            ("Moore's Law", "/mɔːz lɔː/", "摩尔定律", "The empirical observation that the number of transistors on a microchip doubles roughly every two years."),
            ("Extreme Ultraviolet", "/ɪkˈstriːm ˌʌl.trəˈvaɪə.lət/", "极紫外光光刻（EUV）", "Photolithography technology using light with a wavelength of 13.5 nm to etch microscopic circuits."),
            ("Packaging", "/ˈpæk.ɪ.dʒɪŋ/", "先进封装（InFO/CoWoS）", "The process of encasing discrete semiconductor chips together into a high-density unified system."),
            ("Monopoly", "/məˈnɒp.əl.i/", "独占性技术领先", "The exclusive possession or control of the supply of or trade in a leading technological commodity.")
        ],
        "timeline": [
            ("2014–2015", "全球晶圆厂在10/7纳米节点展开白热化军备竞赛，英特尔与三星遭遇良率瓶颈。"),
            ("2016", "台积电年度资本支出首次突破100亿美元大关，率先引入InFO与CoWoS先进封装技术。"),
            ("2017", "台积电年营收逼近1兆元新台币大关，提前锁定极紫外光（EUV）关键产能。"),
            ("2018 · 5月", "台积电量产全球首颗7纳米移动芯片Apple A12，独家领先全行业。"),
            ("2018 · 8月27日", "主要竞争对手格罗方德正式宣布无限期搁置7纳米研发，台积电在尖端制程独揽95%以上份额。")
        ],
        "quote_zh": "当摩尔定律开始变老，全世界都在问「还要不要追」——他用十年回答：追，而且要追到只剩你一个。",
        "quote_en": "As Moore's Law aged, the world wavered on whether to pursue it; he spent a decade proving the answer: pursue it, until you stand alone at the pinnacle."
    },
    {
        "id": "17",
        "file_name": "episode-17.html",
        "folder": "第17期-交棒与退休",
        "act_tag": "ACT 17 · 2013–2018 · 双首长制与贝多芬第九",
        "title_zh": "第 17 期：交棒与退休",
        "title_en": "Episode 17: Passing the Torch and Retirement",
        "time_loc": "2013–2018 · 双首长制与贝多芬第九",
        "tagline_zh": "真正的传承，不是找一个像自己的人，而是把公司交给一套比个人更持久的制度。",
        "tagline_en": "True institutional succession is not finding a replica of oneself, but entrusting the enterprise to an enduring system greater than any individual.",
        "duration": "18:24",
        "pills": [
            ("历史坐标", "征询黄仁勋 · 双首长制架构 · 30周年贝多芬第九 · 2018正式退休"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第17期-交棒与退休.png",
        "prev_link": "episode-16.html",
        "prev_label": "← 上一期：第 16 期 摩尔定律的守卫者",
        "next_link": "episode-18.html",
        "next_label": "下一期：第 18 期 护国神山 →",
        "vocab": [
            ("Dual Leadership", "/ˈdjuː.əl ˈliː.də.ʃɪp/", "双首长治理体制", "A governance structure dividing authority between an Executive Chairman and a Chief Executive Officer."),
            ("Institutionalization", "/ˌɪn.stɪˌtjuː.ʃən.əl.aɪˈzeɪ.ʃən/", "制度化建设", "The action of establishing something as a norm or institution rather than relying on personality."),
            ("Ode to Joy", "/əʊd tuː dʒɔɪ/", "欢乐颂（贝多芬第九交响曲）", "The choral finale of Beethoven's Symphony No. 9, symbolizing triumph, unity, and humanity."),
            ("Consummation", "/ˌkɒn.səˈmeɪ.ʃən/", "功德圆满，终局升华", "The point at which something is complete or finalized with supreme perfection.")
        ],
        "timeline": [
            ("2013 · 初", "张忠谋向黄仁勋征询接任台积电CEO意向，黄仁勋回应「我已有工作（辉达）」。"),
            ("2013 · 底", "张忠谋正式设计并落地「双首长制」：刘德音任董事长主外与董事会，魏哲家任总裁主内与运营。"),
            ("2017 · 10月23日", "台积电举行30周年庆典，邀请国际交响乐团演出贝多芬第九《合唱》，随后正式宣布退休日程。"),
            ("2018 · 6月5日", "主持最后一次股东常会后正式退休，结束长达63年的半导体职业传奇生涯。"),
            ("2018 · 夏", "台积电在无创始人的常态下平稳过渡，制度与文化经受住了世界级检验。")
        ],
        "quote_zh": "真正的传承，不是找一个像自己的人，而是把公司交给一套比个人更持久的制度。",
        "quote_en": "True succession does not consist of finding a clone of oneself, but in entrusting the company to a governance architecture more enduring than any single individual."
    },
    {
        "id": "18",
        "file_name": "episode-18.html",
        "folder": "第18期-护国神山",
        "act_tag": "ACT 18 · 2018–今天 · 地缘政治、AI革命与世纪收官",
        "title_zh": "第 18 期：护国神山",
        "title_en": "Episode 18: The Sacred Mountain of State",
        "time_loc": "2018–今天 · 地缘政治、AI革命与世纪收官",
        "tagline_zh": "一座「护国神山」，从来不是一个人搬上去的，而是一代人的选择，被时间砌成了山。",
        "tagline_en": "A 'Sacred Mountain of State' is never hoisted by a single man; it is the shared choices of a whole generation, sculpted into bedrock by time.",
        "duration": "18:00",
        "pills": [
            ("历史坐标", "中美科技博弈 · 亚利桑那与熊本建厂 · 生成式AI爆发 · 中山勋章全景收官"),
            ("有声轨", "中英双轨 20min 广播级剧场原声"),
            ("双语阅读", "75% 原著双语对齐 · 25% 时代与词汇解析")
        ],
        "image_path": "./设计资产/插图/第18期-护国神山.png",
        "prev_link": "episode-17.html",
        "prev_label": "← 上一期：第 17 期 交棒与退休",
        "next_link": "index.html",
        "next_label": "回到全册总目录 (18期全集收官) →",
        "vocab": [
            ("Chokepoint", "/ˈtʃəʊk.pɔɪnt/", "地缘战略咽喉", "A strategic narrow point of access or critical supply vulnerability in global tech geopolitics."),
            ("Anchor", "/ˈæŋ.kər/", "定海神针，国家支柱", "A person or thing that provides strength and stability in times of storm."),
            ("CoWoS", "/ˈkəʊ.wɒs/", "晶圆级芯片封装（先进封装）", "Chip-on-Wafer-on-Substrate, TSMC's proprietary 2.5D packaging essential for AI GPUs."),
            ("Legacy", "/ˈleɡ.ə.si/", "历史遗产，精神长青", "Something that is passed down from predecessors, continuing to influence future generations.")
        ],
        "timeline": [
            ("2018 · 6月", "张忠谋退休后，半导体地缘政治升温，台积电被外媒与社会公认为台湾「护国神山」。"),
            ("2020 · 5月", "因应美国出口管制规则停止接纳华为新订单；同日宣布投资120亿美元于美国亚利桑那州建厂。"),
            ("2021–2024", "台积电与索尼、丰田合资在日本熊本设立JASM晶圆厂，并于2024年2月正式落成投产。"),
            ("2023–2024", "生成式AI（ChatGPT、英伟达GPU）席卷全球，台积电先进封装CoWoS产能成为算力基础设施最大瓶颈。"),
            ("2024 · 4月", "张忠谋获颁象征崇高荣誉的「中山勋章」，全剧在此迎来历史收官与黄仁勋时代的宏大伏笔。")
        ],
        "quote_zh": "一座「护国神山」，从来不是一个人搬上去的，而是一代人的选择，被时间砌成了山。",
        "quote_en": "A 'Sacred Mountain Protecting the Realm' is never carried up by a single man; it is the choices of an entire generation, cemented into bedrock across time."
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
        print(f"Warning: cues not found for {ep_id}")
        
    cues_json_str = json.dumps(cues, ensure_ascii=False)
    
    # Build Story HTML
    story_html_parts = []
    global_p_idx = 0
    
    # Filter out Knowledge Card and Next Episode Preview from core body
    main_sec_count = 0
    for s in zh_sections:
        if "知识" in s[0] or "预告" in s[0] or "延伸" in s[0]:
            break
        main_sec_count += 1
        
    for sec_i in range(main_sec_count):
        z_title, z_paras = zh_sections[sec_i]
        e_title, e_paras = en_sections[sec_i] if sec_i < len(en_sections) else ("", [])
        
        sec_tag = f"ACT {sec_i:02d} · SECTION {sec_i+1}"
        if "开场" in z_title:
            sec_tag = "PROLOGUE · OPENING"
        elif "第一幕" in z_title:
            sec_tag = "ACT 01"
        elif "第二幕" in z_title:
            sec_tag = "ACT 02"
        elif "第三幕" in z_title:
            sec_tag = "ACT 03"
        elif "第四幕" in z_title:
            sec_tag = "ACT 04"
        elif "第五幕" in z_title:
            sec_tag = "ACT 05"
        elif "第六幕" in z_title:
            sec_tag = "ACT 06"
        elif "尾声" in z_title:
            sec_tag = "EPILOGUE · PARALLEL VIEW"
            
        part = f"""
      <!-- Section: {z_title} -->
      <section class="book-section" id="section-{sec_i}">
        <div class="book-section-header">
          <span class="section-tag">{sec_tag}</span>
          <h2 class="serif">{z_title}<span class="en">{e_title}</span></h2>
        </div>
        <div class="book-section-body">
        """
        
        max_p = max(len(z_paras), len(e_paras))
        for p_i in range(max_p):
            zp = z_paras[p_i] if p_i < len(z_paras) else ""
            ep_text = e_paras[p_i] if p_i < len(e_paras) else ""
            cue_idx = global_p_idx
            start_t = cues[cue_idx]["start"] if cue_idx < len(cues) else 0.0
            
            is_sfx = "【音效" in zp or "[SFX" in ep_text or "【配乐" in zp
            sfx_cls = " sfx-row" if is_sfx else ""
            
            # Format time
            m_val = int(start_t // 60)
            s_val = int(start_t % 60)
            time_display = f"{m_val:02d}:{s_val:02d}"
            
            part += f"""
          <div class="bilingual-para{sfx_cls}" id="p-{cue_idx}" data-time="{start_t:.2f}" onclick="seekAndPlay({start_t:.2f})">
            <div class="para-time-badge" title="点击跳转至此段落音频">{time_display}</div>
            <div class="para-content">
              <p class="zh-para">{html.escape(zp)}</p>
              <p class="en-para">{html.escape(ep_text)}</p>
            </div>
          </div>
            """
            global_p_idx += 1
            
        part += """
        </div>
      </section>
        """
        story_html_parts.append(part)
        
    story_html = "\n".join(story_html_parts)
    
    # Subtitles list
    sub_items_html = []
    for idx, c in enumerate(cues):
        st = c["start"]
        m_val = int(st // 60)
        s_val = int(st % 60)
        td = f"{m_val:02d}:{s_val:02d}"
        zh_t = html.escape(c["zh"])
        en_t = html.escape(c["en"])
        sub_items_html.append(f"""
          <div class="sub-row" id="sub-row-{idx}" data-index="{idx}" data-start="{st}" data-end="{c['end']}" onclick="seekAndPlay({st})">
            <span class="sub-time-tag">{td}</span>
            <div class="sub-content">
              <div class="sub-zh">{zh_t}</div>
              <div class="sub-en">{en_t}</div>
            </div>
          </div>
        """)
    subtitles_html = "\n".join(sub_items_html)
    
    # Vocab cards
    vocab_cards_html = []
    for w, pr, zh_def, en_def in ep["vocab"]:
        vocab_cards_html.append(f"""
          <div class="vocab-card">
            <div class="vocab-word-row">
              <span class="vocab-word">{w}</span>
              <span class="vocab-phonetic">{pr}</span>
            </div>
            <div class="vocab-zh">{zh_def}</div>
            <div class="vocab-en">{en_def}</div>
          </div>
        """)
    vocab_html = "\n".join(vocab_cards_html)
    
    # Timeline
    timeline_html_list = []
    for yr, desc in ep["timeline"]:
        timeline_html_list.append(f"""
          <div class="tl-item">
            <div class="tl-year">{yr}</div>
            <div class="tl-desc">{desc}</div>
          </div>
        """)
    timeline_html = "\n".join(timeline_html_list)
    
    # Pills HTML
    pills_html_list = []
    for pk, pv in ep["pills"]:
        pills_html_list.append(f'<span class="pill"><b>{pk}</b> · {pv}</span>')
    pills_html = "\n".join(pills_html_list)
    
    page_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{ep['title_zh']} ({ep['time_loc']}) | 台积电张忠谋 · 传记时间线的平行世界</title>
<meta name="description" content="台积电张忠谋传记时间线的平行世界 · {ep['title_zh']}（{ep['time_loc']}）。纯净双语典藏电子书，中英双语原声有声剧场，逐句同步高亮字幕，时代历史坐标与双语精读笔记。">

<!-- Open Graph / Facebook / LinkedIn -->
<meta property="og:type" content="article">
<meta property="og:title" content="《台积电张忠谋：{ep['title_zh']} ({ep['time_loc']})》· 传记时间线的平行世界">
<meta property="og:description" content="17分钟双语原声TTS + 逐句同步字幕 + 商业深度复盘。同一时间线，另一个视角。">
<meta property="og:image" content="https://martin-mqtech.github.io/morris-chang-tsmc-aigc-parallel/设计资产/插图/{ep['folder']}.png">
<meta property="og:url" content="https://martin-mqtech.github.io/morris-chang-tsmc-aigc-parallel/{ep['file_name']}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="《台积电张忠谋：{ep['title_zh']} ({ep['time_loc']})》· 传记时间线的平行世界">
<meta name="twitter:description" content="17分钟双语原声TTS + 逐句同步字幕 + 商业深度复盘。同一时间线，另一个视角。">
<meta name="twitter:image" content="https://martin-mqtech.github.io/morris-chang-tsmc-aigc-parallel/设计资产/插图/{ep['folder']}.png">

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
  .en-para {{ font-family: var(--en); font-size: 13.5px; line-height: 1.7; color: #a8a398; font-style: italic; text-align: justify; }}
  
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
  .vocab-word-row {{ display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 3px; }}
  .vocab-word {{ font-family: var(--en); font-weight: 700; font-size: 14px; color: var(--amber); }}
  .vocab-phonetic {{ font-size: 11px; color: var(--muted); font-family: var(--sans); }}
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
      <span class="eyebrow">{ep['act_tag']} <em>EPISODE {ep['id']}</em></span>
      <h1 class="serif">{ep['title_zh']}<span class="en">{ep['title_en']}</span></h1>
      
      <div class="hero-split-grid">
        <div class="hero-left-col">
          <div class="tagline-box" style="margin-top: 0;">
            <div class="tagline-zh">“{ep['tagline_zh']}”</div>
            <div class="tagline-en">"{ep['tagline_en']}"</div>
          </div>
        </div>

        <div class="hero-right-col">
          <figure class="lead-artwork-figure">
            <img class="lead-artwork-img" src="{ep['image_path']}" alt="{ep['title_zh']} 概念插画" loading="lazy">
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
            <span class="track-meta-title" id="track-title-display">{ep['title_zh']} · 中文广播级原声</span>
            <span class="track-meta-sub" id="track-sub-display">{ep['title_en']} · Mandarin Master Audio ({ep['duration']})</span>
          </div>
        </div>

        <div class="progress-container">
          <span class="time-text" id="cur-time">00:00</span>
          <input type="range" class="seek-bar" id="seek-bar" min="0" max="100" value="0" step="0.1" oninput="onSeekInput(this.value)" onchange="onSeekChange(this.value)">
          <span class="time-text" id="total-dur">{ep['duration']}</span>
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
          {subtitles_html}
        </div>
      </div>

      <!-- Native Audio Element (Hidden) with clean audio/ path and fallback -->
      <audio id="main-audio" preload="metadata" src="audio/ep{ep['id']}-zh.mp3"></audio>
    </div>

    <!-- Meta pills placed BELOW the audio player card -->
    <div class="meta-pills">
      {pills_html}
    </div>

    <!-- Dual Layout Body: 75% Pure Book + 25% Learning Sidebar -->
    <div class="content-grid">
      <!-- 75% Pure Bilingual Book -->
      <div class="book-main">
        {story_html}

        <!-- Bottom Share Card -->
        <div class="share-bottom-card">
          <div class="share-bottom-title">觉得本期有启发？一键分享给朋友</div>
          <div class="share-bottom-sub">传递张忠谋与台积电的时代智慧与历史回响 · 支持 8 大主流社交渠道</div>
          <div class="share-matrix-bottom">
            <button class="btn-share-lg primary" onclick="copyViralShare()">📋 复制金句双语卡片</button>
            <button class="btn-share-lg" onclick="openWeChatShare()">💬 微信</button>
            <button class="btn-share-lg" onclick="shareToWeibo()">🔴 微博</button>
            <button class="btn-share-lg" onclick="shareToLinkedIn()">💼 领英 LinkedIn</button>
            <button class="btn-share-lg" onclick="shareToX()">𝕏 X (Twitter)</button>
            <button class="btn-share-lg" onclick="shareToWhatsApp()">📱 WhatsApp</button>
            <button class="btn-share-lg" onclick="shareToTelegram()">✈️ Telegram</button>
            <button class="btn-share-lg" onclick="shareToFacebook()">📘 Facebook</button>
          </div>
        </div>

        <!-- Episode Footer Navigation -->
        <div class="ep-footer-nav">
          <a href="{ep['prev_link']}" class="ep-nav-btn">{ep['prev_label']}</a>
          <a href="{ep['next_link']}" class="ep-nav-btn primary">{ep['next_label']}</a>
        </div>
      </div>

      <!-- 25% Learning & Knowledge Sidebar -->
      <aside class="learning-sidebar">
        <!-- Golden Quote Card -->
        <div class="quote-card">
          <div class="quote-symbol">“</div>
          <div class="quote-zh">{ep['quote_zh']}</div>
          <div class="quote-en">"{ep['quote_en']}"</div>
        </div>

        <!-- Core Vocabulary Card -->
        <div class="side-widget">
          <div class="widget-title">
            <span class="icon">📖</span>
            <span>本期核心词汇与表达</span>
          </div>
          <div class="vocab-list">
            {vocab_html}
          </div>
        </div>

        <!-- Historical Timeline Card -->
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

  <!-- WeChat Share Modal -->
  <div class="modal-overlay" id="wechat-modal" onclick="closeWeChatShare(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <button class="modal-close" onclick="closeWeChatShare()">&times;</button>
      <h3 style="font-size: 16px; margin-bottom: 6px; color: var(--ink);">微信扫一扫分享</h3>
      <p class="modal-text">使用微信「扫一扫」在手机端阅读与收听本期有声剧</p>
      <div class="modal-qr-placeholder">
        <img id="wechat-qr-img" class="modal-qr-img" src="" alt="WeChat QR Code">
      </div>
      <p class="modal-text" style="font-size: 11.5px; opacity: 0.7;">扫码即可在微信内收藏或转发给好友 / 朋友圈</p>
    </div>
  </div>

  <!-- Toast Element -->
  <div class="toast" id="toast-msg">分享文案已复制到剪贴板！</div>

  <!-- Client Script -->
  <script>
    const CUES_DATA = {cues_json_str};
    const EP_DATA = {{
      id: "{ep['id']}",
      titleZh: "{ep['title_zh']}",
      titleEn: "{ep['title_en']}",
      folder: "{ep['folder']}",
      duration: "{ep['duration']}",
      quoteZh: "{ep['quote_zh']}",
      quoteEn: "{ep['quote_en']}"
    }};

    let currentTrack = "zh";
    let isPlaying = false;
    let autoScroll = true;
    let currentCueIndex = -1;
    let userSeeking = false;

    const audio = document.getElementById("main-audio");
    const playBtn = document.getElementById("master-play-btn");
    const seekBar = document.getElementById("seek-bar");
    const curTimeEl = document.getElementById("cur-time");
    const totalDurEl = document.getElementById("total-dur");
    const speedSelect = document.getElementById("speed-select");
    const subViewport = document.getElementById("subtitles-viewport");
    const btnAutoScroll = document.getElementById("btn-auto-scroll");
    const trackBtnZh = document.getElementById("track-btn-zh");
    const trackBtnEn = document.getElementById("track-btn-en");
    const trackTitleDisplay = document.getElementById("track-title-display");
    const trackSubDisplay = document.getElementById("track-sub-display");

    // Single Audio Playback Guarantee
    function ensureSingleAudioPlayback() {{
      const allAudios = document.querySelectorAll("audio");
      allAudios.forEach(a => {{
        if (a !== audio && !a.paused) {{
          a.pause();
        }}
      }});
    }}

    function switchTrack(lang) {{
      if (currentTrack === lang) return;
      currentTrack = lang;
      audio.dataset.fallbackTried = "";
      const curTime = audio.currentTime;
      const wasPlaying = !audio.paused;

      if (lang === "zh") {{
        audio.src = "audio/ep" + EP_DATA.id + "-zh.mp3";
        trackBtnZh.classList.add("active");
        trackBtnEn.classList.remove("active");
        trackTitleDisplay.textContent = EP_DATA.titleZh + " · 中文广播级原声";
        trackSubDisplay.textContent = EP_DATA.titleEn + " · Mandarin Master Audio (" + EP_DATA.duration + ")";
      }} else {{
        audio.src = "audio/ep" + EP_DATA.id + "-en.mp3";
        trackBtnEn.classList.add("active");
        trackBtnZh.classList.remove("active");
        trackTitleDisplay.textContent = EP_DATA.titleEn + " · American English Master";
        trackSubDisplay.textContent = EP_DATA.titleZh + " · 英文纯正沉浸配音 (" + EP_DATA.duration + ")";
      }}

      audio.currentTime = curTime;
      audio.playbackRate = parseFloat(speedSelect.value);
      if (wasPlaying) {{
        ensureSingleAudioPlayback();
        audio.play().catch(e => console.log("Play interrupted", e));
      }}
    }}

    // Audio fallback handler
    audio.addEventListener("error", function(e) {{
      console.warn("Audio primary path failed, attempting fallback...", e);
      if (!audio.dataset.fallbackTried) {{
        audio.dataset.fallbackTried = "true";
        if (currentTrack === "zh") {{
          audio.src = "./03-剧集/" + EP_DATA.folder + "/中文音频.mp3";
        }} else {{
          audio.src = "./03-剧集/" + EP_DATA.folder + "/英文音频.mp3";
        }}
        if (isPlaying) {{
          audio.play().catch(err => console.log("Fallback play error:", err));
        }}
      }}
    }});

    function togglePlay() {{
      if (audio.paused) {{
        ensureSingleAudioPlayback();
        audio.play().then(() => {{
          playBtn.textContent = "⏸";
          isPlaying = true;
        }}).catch(err => console.log("Play error:", err));
      }} else {{
        audio.pause();
        playBtn.textContent = "▶";
        isPlaying = false;
      }}
    }}

    function seekAndPlay(timeSec) {{
      audio.currentTime = timeSec;
      if (audio.paused) {{
        ensureSingleAudioPlayback();
        audio.play().then(() => {{
          playBtn.textContent = "⏸";
          isPlaying = true;
        }}).catch(e => console.log(e));
      }}
    }}

    function onSeekInput(val) {{
      userSeeking = true;
      if (audio.duration) {{
        const targetTime = (val / 100) * audio.duration;
        curTimeEl.textContent = formatTime(targetTime);
      }}
    }}

    function onSeekChange(val) {{
      if (audio.duration) {{
        audio.currentTime = (val / 100) * audio.duration;
      }}
      userSeeking = false;
    }}

    function changeSpeed(val) {{
      audio.playbackRate = parseFloat(val);
    }}

    function toggleAutoScroll() {{
      autoScroll = !autoScroll;
      btnAutoScroll.classList.toggle("active", autoScroll);
      btnAutoScroll.textContent = "自动滚动: " + (autoScroll ? "开" : "关");
    }}

    function formatTime(sec) {{
      if (isNaN(sec)) return "00:00";
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
    }}

    // Audio Event Handlers
    audio.addEventListener("loadedmetadata", () => {{
      totalDurEl.textContent = formatTime(audio.duration);
    }});

    audio.addEventListener("timeupdate", () => {{
      const ct = audio.currentTime;
      if (!userSeeking && audio.duration) {{
        curTimeEl.textContent = formatTime(ct);
        seekBar.value = (ct / audio.duration) * 100;
      }}

      // Find active cue
      let activeIdx = -1;
      for (let i = 0; i < CUES_DATA.length; i++) {{
        if (ct >= CUES_DATA[i].start && ct < CUES_DATA[i].end) {{
          activeIdx = i;
          break;
        }}
      }}

      if (activeIdx !== currentCueIndex) {{
        if (currentCueIndex !== -1) {{
          const oldSub = document.getElementById("sub-row-" + currentCueIndex);
          if (oldSub) oldSub.classList.remove("active");
          const oldPara = document.getElementById("p-" + currentCueIndex);
          if (oldPara) oldPara.classList.remove("current-reading");
        }}

        currentCueIndex = activeIdx;

        if (currentCueIndex !== -1) {{
          const newSub = document.getElementById("sub-row-" + currentCueIndex);
          if (newSub) {{
            newSub.classList.add("active");
            if (autoScroll) {{
              const containerTop = subViewport.offsetTop;
              const targetTop = newSub.offsetTop;
              subViewport.scrollTo({{
                top: targetTop - containerTop - 70,
                behavior: "smooth"
              }});
            }}
          }}
          const newPara = document.getElementById("p-" + currentCueIndex);
          if (newPara) {{
            newPara.classList.add("current-reading");
          }}
        }}
      }}
    }});

    audio.addEventListener("play", () => {{
      playBtn.textContent = "⏸";
      isPlaying = true;
      ensureSingleAudioPlayback();
    }});

    audio.addEventListener("pause", () => {{
      playBtn.textContent = "▶";
      isPlaying = false;
    }});

    audio.addEventListener("ended", () => {{
      playBtn.textContent = "▶";
      isPlaying = false;
    }});

    // 8-Channel Social Sharing Functions
    function getShareData() {{
      const shareUrl = window.location.href;
      const title = document.title;
      const summary = "【台积电张忠谋 · " + EP_DATA.titleZh + "】\\n“" + EP_DATA.quoteZh + "”\\n中英双语原声电子书已上线，即刻收听与精读：";
      return {{ shareUrl, title, summary }};
    }}

    function getShareCopyText() {{
      const data = getShareData();
      return "【台积电张忠谋传记时间线的平行世界 · " + EP_DATA.titleZh + "】\\n\\n“" + EP_DATA.quoteZh + "”\\n\\\"" + EP_DATA.quoteEn + "\\\"\\n\\n🎧 纯净中英双语原声 + 逐句高亮字幕提词器：\\n👉 " + data.shareUrl;
    }}

    function showToast(msg) {{
      const toast = document.getElementById("toast-msg");
      toast.textContent = msg;
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 2800);
    }}

    function openWeChatShare() {{
      const modal = document.getElementById("wechat-modal");
      const qrImg = document.getElementById("wechat-qr-img");
      const pageUrl = encodeURIComponent(window.location.href);
      qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + pageUrl;
      modal.classList.add("active");
    }}

    function closeWeChatShare(e) {{
      const modal = document.getElementById("wechat-modal");
      modal.classList.remove("active");
    }}

    function shareToWeibo() {{
      const data = getShareData();
      const text = encodeURIComponent(data.summary);
      const url = encodeURIComponent(data.shareUrl);
      window.open("https://service.weibo.com/share/share.php?url=" + url + "&title=" + text, "_blank", "width=600,height=500");
    }}

    function shareToLinkedIn() {{
      const data = getShareData();
      const url = encodeURIComponent(data.shareUrl);
      window.open("https://www.linkedin.com/sharing/share-offsite/?url=" + url, "_blank", "width=600,height=500");
    }}

    function shareToX() {{
      const data = getShareData();
      const text = encodeURIComponent("【台积电张忠谋 · " + EP_DATA.titleZh + "】 “" + EP_DATA.quoteZh + "” #TSMC #MorrisChang #Semiconductor");
      const url = encodeURIComponent(data.shareUrl);
      window.open("https://twitter.com/intent/tweet?text=" + text + "&url=" + url, "_blank", "width=600,height=500");
    }}

    function shareToWhatsApp() {{
      const data = getShareData();
      const text = encodeURIComponent("【台积电张忠谋 · " + EP_DATA.titleZh + "】\\n“" + EP_DATA.quoteZh + "”\\n" + data.shareUrl);
      window.open("https://api.whatsapp.com/send?text=" + text, "_blank");
    }}

    function shareToTelegram() {{
      const data = getShareData();
      const text = encodeURIComponent("【台积电张忠谋 · " + EP_DATA.titleZh + "】\\n“" + EP_DATA.quoteZh + "”");
      const url = encodeURIComponent(data.shareUrl);
      window.open("https://t.me/share/url?url=" + url + "&text=" + text, "_blank");
    }}

    function shareToFacebook() {{
      const data = getShareData();
      const url = encodeURIComponent(data.shareUrl);
      window.open("https://www.facebook.com/sharer/sharer.php?u=" + url, "_blank", "width=600,height=500");
    }}

    function copyViralShare() {{
      const text = getShareCopyText();
      if (navigator.clipboard && window.isSecureContext) {{
        navigator.clipboard.writeText(text).then(() => {{
          showToast("✨ 双语金句精选分享文案已复制到剪贴板！");
        }}).catch(() => {{
          fallbackCopyText(text);
        }});
      }} else {{
        fallbackCopyText(text);
      }}
    }}

    function fallbackCopyText(text) {{
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {{
        document.execCommand('copy');
        showToast("✨ 双语金句精选分享文案已复制到剪贴板！");
      }} catch (err) {{
        prompt("请手动复制分享文案：", text);
      }}
      document.body.removeChild(ta);
    }}
  </script>
</body>
</html>
"""
    
    out_file = os.path.join(WORKSPACE, ep["file_name"])
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"Generated {ep['file_name']} (Total size: {len(page_html):,} bytes)")

print("\nAll 18 episodes generated successfully matching Master Standard!")
