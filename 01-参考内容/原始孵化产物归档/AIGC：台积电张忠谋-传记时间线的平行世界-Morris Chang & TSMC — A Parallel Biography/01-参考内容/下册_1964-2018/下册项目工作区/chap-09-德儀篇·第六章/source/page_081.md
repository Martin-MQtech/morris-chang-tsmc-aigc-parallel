# 德仪篇·第六章｜实现「美国梦」

承接 MOS 新任命——

一直到一九六〇年代后期，几乎所有的集成电路都是双极体，MOS 只是实验室的一个研究案。理论上，MOS 的密度可以较双极体高，但速度较双极体低，而且制造技术比双极体更不穩定。六〇年代的一般认知，MOS 在密度上的优点抵不过它在速度及制造技术上的缺点，所以一直到一九六〇年代晚期，MOS 都不被看好。

不看 MOS 的人士包括杰克·基比（Jack Kilby）——集成电路发明人，也是当时德仪半导体技术的「教主」。在德仪半导体技术研究中，基比有「一槌定案」的权威。在一九六〇年代中期及晚期，基比「一槌定案」的方向不是 MOS，而是另一个双极体方向——后来没有成功。基比是我认识的人中最富有想像力和创意者之一，但是在评估 MOS 潜力上面，他错了。

他低估 MOS 的潜力，使得德仪当时只有八名工程师的小团队从事 MOS 研发。而且这八个工程师相当苦闷——他们觉得公司不重视他们的工作，他们也不在我带领的士气高昂的集成电路部门，而是被冷落在研究单位里。

终于，他们的苦闷爆发了一九六八年，这八个工程师——德仪唯一的 MOS 团队——集体辞职！导火线是彪希要求他们搬到休斯顿去。实际原因是他们认为不受公司重视，更重要是——他们已在外面获得支持，要到外面自开公司了。

彪希很想留他们，但发现他们要自开公司后，雷霆大怒，勒令这八个工程师缴出公物、即日离开、不得再返回。

<div class="rebook-translation">
<span class="rebook-translation__label">ReadShift 双语翻译</span>
<p class="en-para">Assumption of the MOS portfolio —</p>
<p class="en-para">Through the late 1960s, nearly all ICs were bipolar. MOS was merely a laboratory research project. In theory, MOS offered higher density than bipolar but at lower speed, and its manufacturing technology was more unstable. The conventional wisdom of the 1960s held that MOS's density advantage did not offset its disadvantages in speed and manufacturability. So through the late 1960s, MOS was not taken seriously.</p>
<p class="en-para">Among the MOS skeptics was Jack Kilby — coinventor of the integrated circuit and the high priest of TI's semiconductor technology. In TI's semiconductor R&D, Kilby had the authority of "the final word." In the mid-to-late 1960s, Kilby's "final word" pointed to a different bipolar direction — one that ultimately failed. Kilby was among the most imaginative and creative people I have ever known. But in assessing MOS's potential, he was wrong.</p>
<p class="en-para">His underestimation of MOS meant TI had only a tiny team of eight engineers working on MOS R&D. And these eight engineers were deeply frustrated — they felt the company did not value their work. They were not part of my high-morale IC division but were marginalized in a research unit.</p>
<p class="en-para">Finally, their frustration erupted. In 1968, these eight engineers — TI's only MOS team — resigned en masse! The trigger was Shep's demand that them move to Houston. The real reason was that they felt unappreciated by the company, and more importantly — they had already secured support on the outside and were leaving to start their own company.</p>
<p class="en-para">Shep wanted badly to keep them, but when he learned they were founding a company, he flew into a rage and ordered the eight engineers to turn in their company belongings, leave that same day, and never return.</p>
</div>

### Cheat Sheet · 商业语汇

1. **Jack Kilby vs. MOS**
**中文解释**：杰克·基比（Jack Kilby，一九二三—二〇〇五），集成电路共同发明人，诺贝尔物理学奖得主；即使是基比这样的技术天才，也会因为「过度自信」而低估技术路线的潜力。这是所有技术驅動型公司必须警惕的「创始人盲区」。
**商业造句**: *Jack Kilby's MOS underestimation is a humbling reminder that even Nobel laureates can be prisoners of their own technological success.*

2. **Eight engineers → Mostek**
**中文解释**：八名工程师 → Mostek 公司，指集体离职后创立的公司；Mostek 后来成为 MOS 记忆体领域的重要竞争者，也是七〇年代德仪最头疼的对手之一。
**商业造句**: *The eight engineers who walked out of TI in 1968 founded Mostek, which would go on to pioneer the MOS memory technology that TI had dismissed.*

3. **"The final word" authority**
**中文解释**：一槌定案的权威，指技术组织中拥有最终决定权的人；在技术规范中，「final word」是必要的效率保障，但当权威者判断错误时，整个组织都会付出代价。
**商业造句**: *Granting a single technologist "the final word" authority accelerates decisions — until it doesn't.*

### 修辞赏析

<span class="rhetoric-note">
<span class="zh">「基比是我认识的人中最富有想像力和创意者之一，但是在评估 MOS 潜力上面，他错了。」——张忠谋用「但是」这个转折词，完成了一次对诺贝尔奖得主的「公正审判」。他没有因为基比是集成电路的发明人就回避他的错误——他对基比的最高评价是：他是一个富有想像力的人，但在这个关键判断上错了。这种「对事不对人」的评价风格，在东方文化中极为罕见——因为我们对权威人物的评价往往是「非颂即斥」，而非「在肯定的前提下指出错误」。</span>
<span class="en">"Kilby was among the most imaginative and creative people I have ever known. But in assessing MOS's potential, he was wrong." — Chang uses the conjunction "but" to deliver a "fair verdict" on a Nobel laureate. He does not shy away from Kilby's error because Kilby coinvented the IC. His highest praise of Kilby: a highly imaginative man who, on this particular judgment call, was wrong. This "issue-focused, not person-focused" evaluative style is rare in East Asian culture, where assessments of authority figures tend toward "either praise or condemnation" rather than "pointing out error within a context of respect."</span>
</span>

### 背景知识延伸

**计算器 IC 与 MOS 归来**：MOS 研发团队被驱逐后，德仪重建 MOS 研发，开始重视 MOS——不是因为对 MOS 技术有新的洞察，而是忽然有客户找上门来。客户要的不是旧 MOS 团队孜孜念念的记忆体，而是一个新花样：计算器 IC。七〇年代初期，计算器刚刚问世，零售价在一百美元以上——实际成本只有二三十美元。许多商人成立计算机公司，急着要买计算器用 IC。德仪新的 MOS 团队乐意应付计算器 IC 生意——因为设计制造都比记忆体简单。一九七一年，MOS 归张忠谋管辖。他接手的 MOS 团队扩充到二三十名工程师，处在得意洋洋的状态中。但张忠谋知道：严峻的挑戰即将来临，得意洋洋的笑容也即将关闭。
