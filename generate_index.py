import os, glob, json

# Episode metadata
episodes_data = [
    {
        "id": "00",
        "title_zh": "全册导读：三大乐章与时代群像",
        "title_en": "Guide: Three Movements & The Era of Giants",
        "period": "1931–2024",
        "theme": "序幕 · 全局鸟瞰",
        "summary": "全局总览台积电与张忠谋的百年史诗：从流离失所的民国少年，到德州仪器的半导体元老，再到56岁独创晶圆代工模式、建立全球半导体护国神山。以AIGC重构多维时空线索。",
        "zh_audio": "03-剧集/第00期-全册导读/中文音频.mp3",
        "en_audio": "03-剧集/第00期-全册导读/英文音频.mp3",
        "zh_dur": "10:35",
        "en_dur": "11:15",
        "tag": "导读篇"
    },
    {
        "id": "01",
        "title_zh": "逃难的孩子",
        "title_en": "Child of Exodus",
        "period": "1937–1942",
        "theme": "战乱 · 迁徙 · 广州至香港",
        "summary": "1937年抗战爆发，6岁的张忠谋跟随父母在战火与轰炸中颠沛流离，穿越火线辗转香港。幼年在防空洞中的记忆，塑造了日后处变不惊、在不确定风暴中寻找确定性的坚毅性格。",
        "zh_audio": "03-剧集/第01期-逃难的孩子/中文音频.mp3",
        "en_audio": "03-剧集/第01期-逃难的孩子/英文音频.mp3",
        "zh_dur": "18:42",
        "en_dur": "19:15",
        "tag": "第一乐章"
    },
    {
        "id": "02",
        "title_zh": "考不进去的南开与作家梦",
        "title_en": "The Nankai Dream & The Reluctant Pragmatist",
        "period": "1942–1948",
        "theme": "重庆南开 · 文人梦断 · 现实抉择",
        "summary": "少年张忠谋原本沉醉于文学与历史，立志成为作家；然而父亲的一句「当作家会挨饿」，以及动荡时局中实业救国的浪潮，将他推向了工程与科学的现实大道。",
        "zh_audio": "03-剧集/第02期-考不进去的南开与作家梦/中文音频.mp3",
        "en_audio": "03-剧集/第02期-考不进去的南开与作家梦/英文音频.mp3",
        "zh_dur": "19:10",
        "en_dur": "19:48",
        "tag": "第一乐章"
    },
    {
        "id": "03",
        "title_zh": "从黄浦江到查尔斯河",
        "title_en": "From Huangpu River to the Charles River",
        "period": "1949–1953",
        "theme": "赴美求学 · 哈佛转麻省理工 · 文化重塑",
        "summary": "1949年只身赴美，成为哈佛大学当年唯一的中国本科新生。在查尔斯河畔浸润人文经典一年后，为了生计转入MIT机械系，开启跨文明重建与硬核工程训练。",
        "zh_audio": "03-剧集/第03期-从黄浦江到查尔斯河/中文音频.mp3",
        "en_audio": "03-剧集/第03期-从黄浦江到查尔斯河/英文音频.mp3",
        "zh_dur": "21:45",
        "en_dur": "22:30",
        "tag": "第一乐章"
    },
    {
        "id": "04",
        "title_zh": "四十封求职信",
        "title_en": "Forty Letters of Application",
        "period": "1953–1955",
        "theme": "MIT博士落第 · 一美元之差 · 误入半导体",
        "summary": "MIT博士资格考意外落榜成为人生最大挫折。投出40封求职信后，因福特汽车不愿多给1美元薪水（月薪469 vs 470），毅然转投半导体先驱希凡尼亚（Sylvania），阴差阳错踏入改变命运的晶体管世界。",
        "zh_audio": "03-剧集/第04期-四十封求职信/中文音频.mp3",
        "en_audio": "03-剧集/第04期-四十封求职信/英文音频.mp3",
        "zh_dur": "21:30",
        "en_dur": "22:15",
        "tag": "第一乐章"
    },
    {
        "id": "05",
        "title_zh": "隔岸观火的叛乱",
        "title_en": "Rebellion Across the Coast",
        "period": "1955–1958",
        "theme": "肖克利实验室 · 仙童八叛逆 · 硅谷破晓",
        "summary": "半导体黎明期，诺奖得主肖克利在西海岸点燃火种，随后『八叛逆』出走创立仙童半导体。在东海岸希凡尼亚冷眼旁观的张忠谋，敏锐察觉到了产业转移与技术革命的剧烈脉动。",
        "zh_audio": "03-剧集/第05期-隔岸观火的叛乱/中文音频.mp3",
        "en_audio": "03-剧集/第05期-隔岸观火的叛乱/英文音频.mp3",
        "zh_dur": "20:50",
        "en_dur": "21:40",
        "tag": "第一乐章"
    },
    {
        "id": "06",
        "title_zh": "德仪的太空竞赛岁月",
        "title_en": "Texas Instruments & The Space Race Era",
        "period": "1958–1964",
        "theme": "加盟德仪 · 基尔比集成电路 · 攻克良率",
        "summary": "1958年加盟德州仪器（TI），与集成电路发明人杰克·基尔比成为同事。张忠谋以严谨的工程思维攻克IBM晶体管良率难题（从0%奇迹般提至20%），获TI全额资助赴斯坦福攻读电机博士。",
        "zh_audio": "03-剧集/第06期-德仪的太空竞赛岁月/中文音频.mp3",
        "en_audio": "03-剧集/第06期-德仪的太空竞赛岁月/英文音频.mp3",
        "zh_dur": "20:55",
        "en_dur": "21:50",
        "tag": "第二乐章"
    },
    {
        "id": "07",
        "title_zh": "半导体之巅的十年",
        "title_en": "A Decade at the Semiconductor Pinnacle",
        "period": "1964–1978",
        "theme": "德仪全球资深副总 · 统治半导体 · 价格战策略",
        "summary": "执掌德仪全球半导体事业部（员工达数万人），首创「学习曲线定价法」，横扫全球芯片市场。成为美国顶尖科技巨头中华人职级最高、权力最大的超级主管。",
        "zh_audio": "03-剧集/第07期-半导体之巅的十年/中文音频.mp3",
        "en_audio": "03-剧集/第07期-半导体之巅的十年/英文音频.mp3",
        "zh_dur": "21:20",
        "en_dur": "21:55",
        "tag": "第二乐章"
    },
    {
        "id": "08",
        "title_zh": "离开德州与受邀回台",
        "title_en": "Leaving Texas & The Taiwan Calling",
        "period": "1978–1985",
        "theme": "战略分歧 · 辞别TI · 执掌工研院",
        "summary": "因TI战略转向消费电子而与高层产生不可弥合分歧，张忠谋告别25载德仪岁月。在李国鼎等人的三顾茅庐与力邀下，54岁的他跨越太平洋回台出任工研院院长。",
        "zh_audio": "03-剧集/第08期-离开德州与受邀回台/中文音频.mp3",
        "en_audio": "03-剧集/第08期-离开德州与受邀回台/英文音频.mp3",
        "zh_dur": "21:05",
        "en_dur": "21:45",
        "tag": "第二乐章"
    },
    {
        "id": "09",
        "title_zh": "纯代工的革命",
        "title_en": "The Pure-Play Foundry Revolution",
        "period": "1985–1987",
        "theme": "商业模式创新 · 创立台积电 · 不与客户竞争",
        "summary": "面对台湾既无设计能力又无销售通路的劣势，张忠谋以惊世魄力提出「纯晶圆代工（Pure-Play Foundry）」模式：只替客户生产、绝不推出自有品牌与客户竞争。半导体垂直分工时代自此开创。",
        "zh_audio": "03-剧集/第09期-纯代工的革命/中文音频.mp3",
        "en_audio": "03-剧集/第09期-纯代工的革命/英文音频.mp3",
        "zh_dur": "20:45",
        "en_dur": "21:10",
        "tag": "第二乐章"
    },
    {
        "id": "10",
        "title_zh": "从台湾到世界",
        "title_en": "From Taiwan to the Global Stage",
        "period": "1988–1997",
        "theme": "英特尔认证 · 纽交所上市 · 无厂晶圆崛起",
        "summary": "1988年安迪·格鲁夫率英特尔团队严苛审核台积电，通过认证一战成名。台积电模式催生了英伟达、高通、博通等全球无晶圆厂（Fabless）设计群雄的百花齐放。",
        "zh_audio": "03-剧集/第10期-从台湾到世界/中文音频.mp3",
        "en_audio": "03-剧集/第10期-从台湾到世界/英文音频.mp3",
        "zh_dur": "20:15",
        "en_dur": "20:50",
        "tag": "第二乐章"
    },
    {
        "id": "11",
        "title_zh": "记忆体的诱惑",
        "title_en": "The Memory Temptation",
        "period": "1998–2000",
        "theme": "德碁合并 · 拒绝DRAM陷阱 · 坚守逻辑代工",
        "summary": "千禧年前夕，面对DRAM存储巨浪诱惑，张忠谋果断拒绝周期毁灭陷阱，主导兼并德碁与世大半导体，一举确立全球逻辑晶圆代工绝对霸主地位。",
        "zh_audio": "03-剧集/第11期-记忆体的诱惑/中文音频.mp3",
        "en_audio": "03-剧集/第11期-记忆体的诱惑/英文音频.mp3",
        "zh_dur": "21:18",
        "en_dur": "21:50",
        "tag": "第三乐章"
    },
    {
        "id": "12",
        "title_zh": "逆周期的定力",
        "title_en": "Contrarian Resilience Through the Dot-Com Bust",
        "period": "2001–2003",
        "theme": "互联网泡沫 · 逆势扩产 · 0.13微米铜制程破局",
        "summary": "全球互联网泡沫破灭、半导体行业断崖式下跌，台积电逆势研发，自主攻克0.13微米铜制程，彻底甩开IBM与联电，技术实力首次跃居世界第一梯队。",
        "zh_audio": "03-剧集/第12期-逆周期的定力/中文音频.mp3",
        "en_audio": "03-剧集/第12期-逆周期的定力/英文音频.mp3",
        "zh_dur": "18:17",
        "en_dur": "19:19",
        "tag": "第三乐章"
    },
    {
        "id": "13",
        "title_zh": "交棒之痛",
        "title_en": "The Agony of Succession",
        "period": "2003–2009",
        "theme": "首次退休 · 金融危机 · 78岁王者归来",
        "summary": "2005年首度交棒CEO，随后遭遇2008全球金融海啸与裁员动荡。78岁的张忠谋力挽狂澜重返第一线，召回老将、重聚人心，决战移动互联网前夜。",
        "zh_audio": "03-剧集/第13期-交棒之痛/中文音频.mp3",
        "en_audio": "03-剧集/第13期-交棒之痛/英文音频.mp3",
        "zh_dur": "19:46",
        "en_dur": "21:36",
        "tag": "第三乐章"
    },
    {
        "id": "14",
        "title_zh": "绚烂年代",
        "title_en": "The Golden Surge of Mobile Era",
        "period": "2009–2012",
        "theme": "资本开支跃升 · 28纳米豪赌 · 移动革命主航道",
        "summary": "重掌帅印后，张忠谋力排众议将资本支出翻倍至百亿美元，全面押注28纳米与移动芯片。28纳米成为半导体史上盈利最丰厚、统治时间最长的一代神级工艺。",
        "zh_audio": "03-剧集/第14期-绚烂年代/中文音频.mp3",
        "en_audio": "03-剧集/第14期-绚烂年代/英文音频.mp3",
        "zh_dur": "18:23",
        "en_dur": "19:50",
        "tag": "第三乐章"
    },
    {
        "id": "15",
        "title_zh": "苹果来敲门",
        "title_en": "When Apple Knocked on the Door",
        "period": "2010–2014",
        "theme": "秘密谈判 · 独吃A系列芯片 · 斩断三星供应链",
        "summary": "乔布斯与库克急于摆脱对三星的依赖，张忠谋派出顶尖精锐飞赴库比蒂诺，以零泄密、全封闭产线的极致信任拿下iPhone A8/A9处理器独家代工，登顶移动时代王座。",
        "zh_audio": "03-剧集/第15期-苹果来敲门/中文音频.mp3",
        "en_audio": "03-剧集/第15期-苹果来敲门/英文音频.mp3",
        "zh_dur": "18:27",
        "en_dur": "19:57",
        "tag": "第三乐章"
    },
    {
        "id": "16",
        "title_zh": "摩尔定律的守卫者",
        "title_en": "Defenders of Moore's Law",
        "period": "2013–2018",
        "theme": "浸润式光刻 · 7nm与EUV极紫外光刻 · 战胜英特尔",
        "summary": "林本坚浸润式光刻奇思妙想落地，联合ASML研发极紫外光（EUV），台积电在7nm/5nm先进制程全面击败英特尔与三星，成为全球唯一擎起摩尔定律火炬的神级工厂。",
        "zh_audio": "03-剧集/第16期-摩尔定律的守卫者/中文音频.mp3",
        "en_audio": "03-剧集/第16期-摩尔定律的守卫者/英文音频.mp3",
        "zh_dur": "18:04",
        "en_dur": "18:44",
        "tag": "第三乐章"
    },
    {
        "id": "17",
        "title_zh": "交棒与退休",
        "title_en": "Succession & Final Retirement",
        "period": "2013–2018",
        "theme": "双首长制 · 刘德音与魏哲家 · 功成身退",
        "summary": "构建「双首长制」权力架构，确保庞大帝国在制度下平稳运转。2018年6月，87岁的张忠谋正式宣布全面退休，留下一座无懈可击的全球科技巨塔。",
        "zh_audio": "03-剧集/第17期-交棒与退休/中文音频.mp3",
        "en_audio": "03-剧集/第17期-交棒与退休/英文音频.mp3",
        "zh_dur": "18:24",
        "en_dur": "19:31",
        "tag": "第三乐章"
    },
    {
        "id": "18",
        "title_zh": "护国神山与地缘风暴",
        "title_en": "The Silicon Shield & The Geopolitical Storm",
        "period": "2018–2026",
        "theme": "AI算力心脏 · 地缘兵家必争 · 尾声与英伟达序章",
        "summary": "台积电成为全球AI浪潮的核心发动机（ChatGPT、英伟达GPU、苹果芯片的心脏）。张忠谋直言「全球化已死，地缘政治让台积电成为兵家必争之地」。全系列收官，并为案例二（黄仁勋）埋下辉煌伏笔。",
        "zh_audio": "03-剧集/第18期-护国神山/中文音频.mp3",
        "en_audio": "03-剧集/第18期-护国神山/英文音频.mp3",
        "zh_dur": "18:00",
        "en_dur": "18:02",
        "tag": "全系列大收官"
    }
]

# Generate Episode HTML cards
ep_cards_html = ""
for ep in episodes_data:
    ep_cards_html += f"""
    <div class="ep-card glassmorphism" data-id="{ep['id']}">
      <div class="ep-header">
        <span class="ep-badge">{ep['tag']} · EP {ep['id']}</span>
        <span class="ep-period">{ep['period']}</span>
      </div>
      <h3 class="ep-title">{ep['title_zh']}</h3>
      <p class="ep-en-title">{ep['title_en']}</p>
      <div class="ep-theme"><span class="icon">⚡</span> {ep['theme']}</div>
      <p class="ep-desc">{ep['summary']}</p>
      
      <div class="audio-panel">
        <div class="audio-track-tabs">
          <button class="track-tab active" onclick="switchTrack(this, '{ep['id']}', 'zh')">🇨🇳 中文原声 ({ep['zh_dur']})</button>
          <button class="track-tab" onclick="switchTrack(this, '{ep['id']}', 'en')">🇺🇸 English ({ep['en_dur']})</button>
        </div>
        <audio id="audio-{ep['id']}" controls preload="none" class="custom-audio" src="{ep['zh_audio']}"></audio>
      </div>

      <div class="ep-actions">
        <a href="03-剧集/{ep['title_zh'] if ep['id']=='00' else '第'+ep['id']+'期-'+ep['title_zh'].split('：')[0]}/README.md" class="btn-subtle" target="_blank">📖 剧集文档</a>
        <a href="portal.html" class="btn-subtle">🌟 官网沉浸版</a>
      </div>
    </div>
    """

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>台积电张忠谋 · 传记时间线的平行世界 | Morris Chang & TSMC: A Parallel Biography</title>
  <meta name="description" content="同一时间线，另一个视角。以台积电张忠谋生平为锚点，由 AIGC 平行叙事引擎打造的中英双语有声传记、交互地图、典藏电子书与知识卡片全矩阵。">
  <meta name="keywords" content="张忠谋,台积电,TSMC,Morris Chang,半导体,Foundry,晶圆代工,AIGC,双语传记,GitHub Pages">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@400;600;700;900&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg-dark: #0a0e17;
      --bg-surface: #111726;
      --bg-card: rgba(18, 26, 43, 0.75);
      --border-card: rgba(0, 240, 255, 0.15);
      --border-hover: rgba(0, 240, 255, 0.45);
      --cyan-tsmc: #00f0ff;
      --cyan-glow: rgba(0, 240, 255, 0.35);
      --gold-silicon: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.3);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent-purple: #8b5cf6;
      --font-serif: "Noto Serif SC", "Songti SC", Georgia, serif;
      --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-display: "Cinzel", "Noto Serif SC", serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.7;
      overflow-x: hidden;
      background-image: 
        radial-gradient(circle at 15% 20%, rgba(0, 240, 255, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 60%, rgba(245, 158, 11, 0.06) 0%, transparent 45%),
        linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 48px 48px, 48px 48px;
    }}

    /* Global Container */
    .container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    /* Glassmorphism */
    .glassmorphism {{
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-card);
      border-radius: 16px;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .glassmorphism:hover {{
      border-color: var(--border-hover);
      box-shadow: 0 10px 30px -10px var(--cyan-glow);
    }}

    /* Header Nav */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(10, 14, 23, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding: 16px 0;
    }}
    .nav-content {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand-logo {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text-main);
    }}
    .brand-wafer {{
      width: 32px;
      height: 32px;
      background: linear-gradient(135deg, var(--cyan-tsmc), var(--gold-silicon));
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      box-shadow: 0 0 12px var(--cyan-glow);
    }}
    .brand-name {{
      font-family: var(--font-serif);
      font-weight: 700;
      font-size: 18px;
      letter-spacing: 1px;
    }}
    .brand-name span {{
      color: var(--cyan-tsmc);
    }}
    .nav-links {{
      display: flex;
      gap: 24px;
      align-items: center;
    }}
    .nav-link {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 14px;
      font-weight: 500;
      transition: color 0.2s;
    }}
    .nav-link:hover {{
      color: var(--cyan-tsmc);
    }}
    .nav-cta {{
      background: linear-gradient(135deg, var(--cyan-tsmc), #0284c7);
      color: #03111f;
      font-weight: 600;
      padding: 8px 18px;
      border-radius: 20px;
      font-size: 13px;
      text-decoration: none;
      transition: all 0.25s;
    }}
    .nav-cta:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 16px var(--cyan-glow);
    }}

    /* Hero Section */
    .hero {{
      padding: 90px 0 60px;
      position: relative;
    }}
    .hero-badge-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 24px;
    }}
    .badge {{
      background: rgba(0, 240, 255, 0.08);
      border: 1px solid rgba(0, 240, 255, 0.25);
      color: var(--cyan-tsmc);
      font-size: 12px;
      font-weight: 600;
      padding: 4px 12px;
      border-radius: 30px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .badge.gold {{
      background: rgba(245, 158, 11, 0.1);
      border-color: rgba(245, 158, 11, 0.3);
      color: var(--gold-silicon);
    }}
    .hero-title {{
      font-family: var(--font-serif);
      font-size: clamp(32px, 5.5vw, 58px);
      font-weight: 900;
      line-height: 1.15;
      letter-spacing: -0.5px;
      margin-bottom: 16px;
      background: linear-gradient(135deg, #ffffff 40%, var(--cyan-tsmc) 80%, var(--gold-silicon) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .hero-subtitle {{
      font-family: var(--font-display);
      font-size: clamp(16px, 2.2vw, 22px);
      color: var(--text-muted);
      letter-spacing: 2px;
      margin-bottom: 20px;
    }}
    .hero-tagline {{
      font-size: clamp(16px, 1.8vw, 19px);
      color: var(--text-main);
      max-width: 820px;
      margin-bottom: 36px;
      line-height: 1.8;
    }}
    .hero-tagline strong {{
      color: var(--gold-silicon);
    }}
    .hero-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 48px;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, var(--cyan-tsmc), #0284c7);
      color: #03111f;
      font-weight: 700;
      padding: 14px 28px;
      border-radius: 12px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 20px var(--cyan-glow);
      transition: all 0.25s;
    }}
    .btn-primary:hover {{
      transform: translateY(-3px);
      box-shadow: 0 8px 30px var(--cyan-glow);
    }}
    .btn-secondary {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: var(--text-main);
      font-weight: 600;
      padding: 14px 24px;
      border-radius: 12px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.25s;
    }}
    .btn-secondary:hover {{
      background: rgba(255, 255, 255, 0.1);
      border-color: var(--cyan-tsmc);
      color: var(--cyan-tsmc);
      transform: translateY(-3px);
    }}

    /* Key Statistics Bar */
    .stats-bar {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      padding: 24px;
      margin-bottom: 80px;
    }}
    .stat-item {{
      text-align: center;
    }}
    .stat-num {{
      font-family: var(--font-display);
      font-size: 32px;
      font-weight: 700;
      color: var(--cyan-tsmc);
      margin-bottom: 4px;
    }}
    .stat-label {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    /* Section Title */
    .section-header {{
      text-align: center;
      margin-bottom: 48px;
    }}
    .section-tag {{
      font-size: 12px;
      font-weight: 700;
      color: var(--cyan-tsmc);
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-bottom: 8px;
      display: block;
    }}
    .section-title {{
      font-family: var(--font-serif);
      font-size: clamp(26px, 3.5vw, 38px);
      color: var(--text-main);
      margin-bottom: 12px;
    }}
    .section-desc {{
      font-size: 15px;
      color: var(--text-muted);
      max-width: 680px;
      margin: 0 auto;
    }}

    /* Showcase Matrix (Portals) */
    .portal-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
      margin-bottom: 90px;
    }}
    .portal-card {{
      padding: 32px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }}
    .portal-card::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 4px;
      background: linear-gradient(90deg, var(--cyan-tsmc), transparent);
    }}
    .portal-card.gold::before {{
      background: linear-gradient(90deg, var(--gold-silicon), transparent);
    }}
    .portal-icon {{
      font-size: 36px;
      margin-bottom: 16px;
      display: inline-block;
    }}
    .portal-title {{
      font-family: var(--font-serif);
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 8px;
      color: #fff;
    }}
    .portal-text {{
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 24px;
      flex-grow: 1;
    }}
    .portal-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 14px;
      font-weight: 600;
      color: var(--cyan-tsmc);
      text-decoration: none;
      transition: gap 0.2s;
    }}
    .portal-card.gold .portal-link {{
      color: var(--gold-silicon);
    }}
    .portal-link:hover {{
      gap: 10px;
    }}

    /* Episodes Grid */
    .episodes-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 28px;
      margin-bottom: 90px;
    }}
    .ep-card {{
      padding: 24px;
      display: flex;
      flex-direction: column;
    }}
    .ep-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .ep-badge {{
      font-size: 11px;
      font-weight: 700;
      color: var(--gold-silicon);
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid rgba(245, 158, 11, 0.25);
      padding: 2px 8px;
      border-radius: 6px;
    }}
    .ep-period {{
      font-size: 12px;
      color: var(--text-dim);
      font-family: var(--font-display);
    }}
    .ep-title {{
      font-family: var(--font-serif);
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 4px;
    }}
    .ep-en-title {{
      font-size: 12px;
      font-style: italic;
      color: var(--text-dim);
      margin-bottom: 12px;
    }}
    .ep-theme {{
      font-size: 12px;
      font-weight: 500;
      color: var(--cyan-tsmc);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .ep-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.65;
      margin-bottom: 18px;
      flex-grow: 1;
    }}
    .audio-panel {{
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 10px;
      padding: 12px;
      margin-bottom: 16px;
    }}
    .audio-track-tabs {{
      display: flex;
      gap: 8px;
      margin-bottom: 8px;
    }}
    .track-tab {{
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-size: 11px;
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 4px;
      transition: all 0.2s;
    }}
    .track-tab.active {{
      background: rgba(0, 240, 255, 0.15);
      color: var(--cyan-tsmc);
      font-weight: 600;
    }}
    .custom-audio {{
      width: 100%;
      height: 32px;
      outline: none;
    }}
    .ep-actions {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding-top: 12px;
    }}
    .btn-subtle {{
      font-size: 12px;
      color: var(--text-muted);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: color 0.2s;
    }}
    .btn-subtle:hover {{
      color: var(--cyan-tsmc);
    }}

    /* AIGC Pipeline Architecture */
    .pipeline-section {{
      padding: 48px;
      margin-bottom: 90px;
    }}
    .pipeline-flow {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      position: relative;
      margin-top: 40px;
    }}
    .pipeline-step {{
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      position: relative;
    }}
    .step-num {{
      width: 28px;
      height: 28px;
      background: var(--cyan-tsmc);
      color: #03111f;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 13px;
      margin: 0 auto 12px;
    }}
    .step-title {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 6px;
    }}
    .step-desc {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    /* Footer */
    .footer {{
      background: #06090f;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding: 60px 0 30px;
    }}
    .footer-grid {{
      display: grid;
      grid-template-columns: 2fr 1fr 1fr;
      gap: 40px;
      margin-bottom: 40px;
    }}
    .footer-brand {{
      font-family: var(--font-serif);
      font-size: 20px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 12px;
    }}
    .footer-desc {{
      font-size: 13px;
      color: var(--text-muted);
      max-width: 440px;
      line-height: 1.8;
    }}
    .footer-col h4 {{
      font-size: 14px;
      font-weight: 700;
      color: var(--cyan-tsmc);
      margin-bottom: 16px;
    }}
    .footer-links {{
      list-style: none;
    }}
    .footer-links li {{
      margin-bottom: 10px;
    }}
    .footer-links a {{
      color: var(--text-muted);
      font-size: 13px;
      text-decoration: none;
      transition: color 0.2s;
    }}
    .footer-links a:hover {{
      color: #fff;
    }}
    .footer-bottom {{
      text-align: center;
      padding-top: 30px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 12px;
      color: var(--text-dim);
    }}

    @media (max-width: 768px) {{
      .episodes-grid {{
        grid-template-columns: 1fr;
      }}
      .footer-grid {{
        grid-template-columns: 1fr;
      }}
      .hero-actions {{
        flex-direction: column;
      }}
    }}
  </style>
</head>
<body>

  <!-- Navbar -->
  <header class="navbar">
    <div class="container nav-content">
      <a href="#" class="brand-logo">
        <div class="brand-wafer">⚡</div>
        <div class="brand-name">Morris Chang · <span>台积电平行世界</span></div>
      </a>
      <nav class="nav-links">
        <a href="#overview" class="nav-link">项目全景</a>
        <a href="#portals" class="nav-link">作品矩阵</a>
        <a href="#episodes" class="nav-link">剧集矩阵</a>
        <a href="#pipeline" class="nav-link">AIGC 架构</a>
        <a href="https://github.com/Martin-MQtech/morris-chang-tsmc-aigc-parallel" target="_blank" class="nav-cta">GitHub 源码 ↗</a>
      </nav>
    </div>
  </header>

  <!-- Hero Section -->
  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-badge-group">
          <span class="badge">🌐 GitHub Pages Live</span>
          <span class="badge gold">🇨🇳 🇺🇸 中英双语有声全册</span>
          <span class="badge">⚡ AIGC 平行叙事引擎</span>
          <span class="badge">💎 00–18 期完结收官</span>
        </div>

        <h1 class="hero-title">台积电张忠谋 · 传记时间线的平行世界</h1>
        <div class="hero-subtitle">Morris Chang & TSMC: A Parallel Biography</div>

        <p class="hero-tagline">
          <strong>同一时间线，另一个视角。</strong> 以张忠谋生平与半导体产业风云为时空坐标，由 AIGC 平行叙事引擎萃取历史图谱，融合艾萨克森的冷峻洞察、吴晓波的时代浪潮感与史景迁的文学史笔，打造的全套中英双语多模态传记巨作。
        </p>

        <div class="hero-actions">
          <a href="portal.html" class="btn-primary">🌟 沉浸式作品官网 ↗</a>
          <a href="map.html" class="btn-secondary">🗺️ 交互式平行世界地图</a>
          <a href="reader.html" class="btn-secondary">📖 全册电子书在线阅读</a>
          <a href="cards.html" class="btn-secondary">🎴 金句知识卡片</a>
          <a href="台积电张忠谋-传记时间线的平行世界.epub" download class="btn-secondary">📥 EPUB 典藏版下载</a>
        </div>

        <!-- Key Metrics -->
        <div class="stats-bar glassmorphism">
          <div class="stat-item">
            <div class="stat-num">19</div>
            <div class="stat-label">全册精制剧集 (00–18期)</div>
          </div>
          <div class="stat-item">
            <div class="stat-num">380+</div>
            <div class="stat-label">分钟中英双轨广播剧</div>
          </div>
          <div class="stat-item">
            <div class="stat-num">108</div>
            <div class="stat-label">条跨学科公开史实源</div>
          </div>
          <div class="stat-item">
            <div class="stat-num">100%</div>
            <div class="stat-label">AIGC 全流程自洽闭环</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Overview Section -->
    <section id="overview" class="container" style="margin-bottom: 90px;">
      <div class="section-header">
        <span class="section-tag">OVERVIEW & CORE PHILOSOPHY</span>
        <h2 class="section-title">项目核心全景与叙事哲学</h2>
        <p class="section-desc">用最硬核的技术生产最温润的人文叙事，在跨文明旅程中解构半导体传奇。</p>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px;">
        <div class="glassmorphism" style="padding: 32px;">
          <h3 style="font-family: var(--font-serif); color: var(--cyan-tsmc); margin-bottom: 12px; font-size: 20px;">⚡ 纯代工模式的商业哲学</h3>
          <p style="color: var(--text-muted); font-size: 14px; line-height: 1.8;">
            1987年台积电的诞生，彻底打破了半导体行业IDM纵向一体化的旧秩序。「绝不与客户竞争」的信条，催生了全球芯片设计产业（Fabless）的繁荣，孕育了英伟达、高通与苹果自研芯片的时代奇迹。
          </p>
        </div>
        <div class="glassmorphism" style="padding: 32px;">
          <h3 style="font-family: var(--font-serif); color: var(--gold-silicon); margin-bottom: 12px; font-size: 20px;">🌏 跨文明重建与华人精神</h3>
          <p style="color: var(--text-muted); font-size: 14px; line-height: 1.8;">
            从流离失所的民国逃难少年，到MIT机械学子、德州仪器副总，再到54岁跨越太平洋回台创业。全剧贯穿东方人在西方顶级科技世界中自我重建、勇拓边界的坚毅商业精神。
          </p>
        </div>
        <div class="glassmorphism" style="padding: 32px;">
          <h3 style="font-family: var(--font-serif); color: var(--accent-purple); margin-bottom: 12px; font-size: 20px;">🧬 平行叙事引擎 (PNE)</h3>
          <p style="color: var(--text-muted); font-size: 14px; line-height: 1.8;">
            三维立体二创法：以真实生平为时间轴锚点（内圈交集），融合时代宏观群像与科技博弈（外圈拓展），AI旁白置换第一人称，打造完全独立版权、兼具文学与知识密度的全新叙事。
          </p>
        </div>
      </div>
    </section>

    <!-- Showcase Portals -->
    <section id="portals" class="container">
      <div class="section-header">
        <span class="section-tag">EXPLORE MATRIX</span>
        <h2 class="section-title">交互探索与作品矩阵</h2>
        <p class="section-desc">多维度、沉浸式互动形态，满足深度阅读、快速查阅、听觉体验与社交传播。</p>
      </div>

      <div class="portal-grid">
        <div class="portal-card glassmorphism">
          <div>
            <span class="portal-icon">🌟</span>
            <h3 class="portal-title">《作品官网》</h3>
            <p class="portal-text">杂志级排版视觉官网，集成了全18期精美章首插图、双语简介与中英双轨直载音频播放器。</p>
          </div>
          <a href="portal.html" class="portal-link">打开作品官网 <span>→</span></a>
        </div>

        <div class="portal-card glassmorphism gold">
          <div>
            <span class="portal-icon">🗺️</span>
            <h3 class="portal-title">《平行世界地图》</h3>
            <p class="portal-text">双轨时间轴交互罗盘：上轴记录张忠谋的人生抉择点，下轴呈现同时期的世界科技与历史大事件对照。</p>
          </div>
          <a href="map.html" class="portal-link">探索平行地图 <span>→</span></a>
        </div>

        <div class="portal-card glassmorphism">
          <div>
            <span class="portal-icon">📖</span>
            <h3 class="portal-title">《全册电子书在线版》</h3>
            <p class="portal-text">400万字双语典藏级HTML电子书，段落级中英对照，内嵌高清插图与学术级图注，支持全文阅读。</p>
          </div>
          <a href="reader.html" class="portal-link">在线畅读全书 <span>→</span></a>
        </div>

        <div class="portal-card glassmorphism gold">
          <div>
            <span class="portal-icon">🎴</span>
            <h3 class="portal-title">《金句知识卡片》</h3>
            <p class="portal-text">Bento 风格设计的商业智慧与金句卡片，萃取传主在战略、管理、人生逆境中的认知精华，适合快速阅读与分享。</p>
          </div>
          <a href="cards.html" class="portal-link">查看金句卡片 <span>→</span></a>
        </div>
      </div>
    </section>

    <!-- Episodes Grid -->
    <section id="episodes" class="container">
      <div class="section-header">
        <span class="section-tag">MULTIMODAL EPISODES</span>
        <h2 class="section-title">全 19 期多模态剧集矩阵 (00–18)</h2>
        <p class="section-desc">中英双语原声音频点播 · 时代背景透视 · 传记关键抉择节点全览</p>
      </div>

      <div class="episodes-grid">
        {ep_cards_html}
      </div>
    </section>

    <!-- AIGC Pipeline Architecture -->
    <section id="pipeline" class="container">
      <div class="pipeline-section glassmorphism">
        <div class="section-header" style="margin-bottom: 24px;">
          <span class="section-tag">ENGINEERING PIPELINE</span>
          <h2 class="section-title">AIGC 并行生产工程架构</h2>
          <p class="section-desc">从事实抽取到多模态出版物的一体化 SOP 自动化流水线</p>
        </div>

        <div class="pipeline-flow">
          <div class="pipeline-step">
            <div class="step-num">1</div>
            <div class="step-title">知识图谱提取</div>
            <div class="step-desc">提取真实传记年表与公开史料（S01–S108），建立实体知识图谱。</div>
          </div>
          <div class="pipeline-step">
            <div class="step-num">2</div>
            <div class="step-title">平行叙事编织</div>
            <div class="step-desc">第三方旁白置换，编织宏观时代背景与人物冲突，输出中英文稿。</div>
          </div>
          <div class="pipeline-step">
            <div class="step-num">3</div>
            <div class="step-title">双语 TTS 语音合成</div>
            <div class="step-desc">并发调用神经语音合成模型（中英双角色），生成广播剧级高品质音频。</div>
          </div>
          <div class="pipeline-step">
            <div class="step-num">4</div>
            <div class="step-title">质量与史实门禁</div>
            <div class="step-desc">自动化清洗舞台标记，校对敏感年份与术语，确保学术级史实自洽。</div>
          </div>
          <div class="pipeline-step">
            <div class="step-num">5</div>
            <div class="step-title">多矩阵渲染打包</div>
            <div class="step-desc">一键编译出版级 EPUB 3.0、全册 HTML 电子书、互动地图与静态网页。</div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">台积电张忠谋 · 传记时间线的平行世界</div>
          <p class="footer-desc">
            本项目由 Martin-MQtech 主理，属于 ReadShift 主体工程下游 AIGC 创意示范项目。遵循开源共享精神，仅供科技与人文研究、语言学习交流使用。
          </p>
        </div>
        <div class="footer-col">
          <h4>作品导航</h4>
          <ul class="footer-links">
            <li><a href="portal.html">作品官网 Portal</a></li>
            <li><a href="map.html">平行世界地图 Map</a></li>
            <li><a href="reader.html">全册电子书 Reader</a></li>
            <li><a href="cards.html">金句知识卡片 Cards</a></li>
            <li><a href="台积电张忠谋-传记时间线的平行世界.epub">下载 EPUB 电子书</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>开源与架构</h4>
          <ul class="footer-links">
            <li><a href="https://github.com/Martin-MQtech/morris-chang-tsmc-aigc-parallel" target="_blank">GitHub 仓库</a></li>
            <li><a href="README.md" target="_blank">主控架构 SOP</a></li>
            <li><a href="平行叙事引擎.md" target="_blank">平行叙事引擎方法论</a></li>
            <li><a href="完结说明.md" target="_blank">全书完结审计报告</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2026 Martin-MQtech & Parallel Narrative Engine. Released under MIT & CC-BY-NC 4.0 Licenses.</p>
      </div>
    </div>
  </footer>

  <script>
    function switchTrack(btn, epId, lang) {{
      const card = btn.closest('.ep-card');
      const tabs = card.querySelectorAll('.track-tab');
      tabs.forEach(t => t.classList.remove('active'));
      btn.classList.add('active');

      const audio = document.getElementById('audio-' + epId);
      const wasPlaying = !audio.paused;
      
      // Find audio source based on episode ID
      const ep = {json.dumps({ep['id']: {'zh': ep['zh_audio'], 'en': ep['en_audio']} for ep in episodes_data})}[epId];
      if (ep) {{
        audio.src = ep[lang];
        if (wasPlaying) {{
          audio.play();
        }}
      }}
    }}
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated index.html successfully!")
