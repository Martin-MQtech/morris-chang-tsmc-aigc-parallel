# 张忠谋自传下册 — 英译任务说明书

> 本文件可独立交给任何 LLM Agent 执行，无需额外上下文。

---

## 一、任务概述

张忠谋自传下册（1964–2018）是一套中英双语阅读产品的下部，目前 **143 个页面文件缺少英文翻译**。你的任务是：为每个页面中的中文正文撰写地道英文翻译，按指定格式嵌入源文件，运行渲染器生成最终 HTML。

- 工作区路径：`/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift/下册项目工作区`
- 待翻译页面清单：`/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift/下册项目工作区/translation_manifest.txt`
- 渲染器：`node /Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift/下册项目工作区/render_html_v9.js --chapter <章号> --out "<工作区路径>/chap-<章号>-<slug>/output.html"`
- 总工作量：143 个 page_XXX.md 文件（分布在 chap-21 至 chap-42 约 20 个章节中）

---

## 二、文件结构（务必理解）

工作区内每个章节一个文件夹：

```
chap-21-台積電篇一·第十七章/
├── output.html            ← 渲染成品（你翻译后需重新渲染）
└── source/
    ├── page_239.md        ← 中文 + 可能已有英文 + 二创卡片
    ├── page_240.md
    └── ...
```

每个 `page_XXX.md` 内部结构：

```markdown
# 章节标题（已有）

## 小节标题（已有）

<中文正文段落 1>

<中文正文段落 2>

<div class="rebook-translation">
<span class="rebook-translation__label">ReadShift 双语翻译</span>
<p class="en-para">English translation paragraph 1...</p>
<p class="en-para">English translation paragraph 2...</p>
</div>

### Cheat Sheet · 商业语汇（已有，勿改）
...

### 修辞赏析（已有，勿改）
...

### 背景知识延伸（已有，勿改）
...
```

---

## 三、翻译规则

### 3.1 什么需要翻译

- **正文中到英**：正文段落中的每个中文段落，对应一段 `<p class="en-para">` 英文翻译
- 严格 1:1 段落配对：一个中文段 → 一个英文段，不多不少

### 3.2 什么不需要翻译（已有，保持不动）

- Cheat Sheet · 商业语汇：已有英文术语 + 中文释义 + 英文造句
- 修辞赏析：已有 zh/en 双语对
- 背景知识延伸：仅中文，无需翻译
- 标题（`#` / `##`）：保持原样

### 3.3 翻译格式

英文翻译必须用以下 HTML 结构包裹：

```markdown
<div class="rebook-translation">
<span class="rebook-translation__label">ReadShift 双语翻译</span>
<p class="en-para">First English paragraph translation here.</p>
<p class="en-para">Second English paragraph translation here.</p>
</div>
```

关键格式要求：
- `div class="rebook-translation"` 必须紧接在中文段落之后、任何标题/卡片之前
- 每个英文段落用 `<p class="en-para">...</p>` 包裹
- label span 只能出现**一次**在每个 rebook-translation 块开头
- 不要在这个 div 内添加任何其他 HTML 标签或 class

### 3.4 中英文段落配对逻辑

按顺序配对：中文第一段 → 英文第一段（`<p class="en-para">`），中文第二段 → 英文第二段，依此类推。

如果中文页面有 N 个正文段落，英文必须有 N 个 `<p class="en-para">`。

---

## 四、翻译风格标准

### 4.1 核心风格：Walter Isaacson 传记 × HBR 商业语言

融合两种风格：
- **Isaacson 传记**：叙事驱动、克制优雅、有历史纵深感，把个人决策放在大时代背景下，不用形容词堆砌
- **HBR 商业语言**：动词精准、名词专业、主动语态，"market share" 不说 "customers"，"revenue" 不说 "money"

### 4.2 具体规范

**叙事语气：**
- 过去时为主（对往事的回顾）
- 内省但不煽情："Looking back, the timing proved fortuitous" 而非 "It was a tearful, unforgettable moment."
- 让事实说话，避免形容词堆砌
- 直接引语保持原文措辞

**动词精度（HBR 标准）：**

| 中文原意 | 不要写 | 应该写 |
|---|---|---|
| 增加收入 | make more money | generate incremental revenue |
| 打败对手 | beat competitors | outperform rivals on cost and quality |
| 改方向 | change direction | pivot toward / reorient |
| 快速增长 | grow fast | sustain above-market growth |
| 谈判协商 | talk about | negotiate / hash out |
| 思考考虑 | think about | evaluate / weigh / consider |
| 开拓新市场 | go to new markets | expand into adjacent markets |
| 解决问题 | solve problems | resolve / address |
| 降低成本 | spend less | reduce unit costs / improve efficiency |
| 吸引客户 | get customers | acquire customers / win market share |

**句式节奏：**
- 长短交替：叙事段可用复合句（20-30 词），结论/转折用短句（8-12 词）
- 句号后不超过 25 词
- 避免从句嵌套超过两层

**专有名词：**
- 公司名：TI、TSMC、Intel、AMD、Qualcomm、Bosch — 原文保留
- 人名：Morris Chang、Zhang忠谋（首次出现可用 Morris Chang）、Stanford、MIT
- 书名/文章名：*"Chip War"*, *"My View of Intel"*, *Harvard Business Review*
- 术语：pure-play foundry、wafer fab、assembly and test、Semiconductor — 首次出现后可用缩写

**禁用表达：**
- ❌ 感叹号
- ❌ "In my opinion..." / "I think..." （除非在直接引语内）
- ❌ 第一人称插入语（除非是直接引语）
- ❌ 口语化："a lot of" / "big" / "really" / "stuff"
- ❌ 中式英语："no die no rest" → 应该写 "relentless / tireless"
- ❌ 冗余："past history" → "history"；"future plans" → "plans"

### 4.3 品质目标

每段英文翻译应该是：
- 母语者自然阅读无障碍
- 专业商业/传记读者不出戏
- 不逐字直译（意译优先，但语义要准确）
- 保留原文的叙事张力和节奏感

---

## 五、工作流（逐文件执行）

对每个待翻译的 `page_XXX.md` 文件：

1. **读取**文件内容
2. **识别**需要翻译的中文正文段落（在 HTML 标签 `<div>` 或 `#`/`##` 标题之外的连续中文段落）
3. **翻译**每个中文段落为英文（按第四节风格标准）
4. **插入**翻译到正确位置（中文段落后，用 `<div class="rebook-translation">` 包裹）
5. **写回**文件（保持其他所有内容不变）
6. **验证**：`<p class="en-para">` 数量 == 中文段落数量

每完成**一个章节**的所有页面后：

7. 渲染该章：`node render_html_v9.js --chapter <章号> --out "chap-<章号>-<slug>/output.html"`
8. 验证渲染成果：检查 output.html 中 `en-para` 数量与 `cn-para` 数量是否匹配
9. 繁简检测：确认 output.html 无繁体字（可用 `opencc` 或手动抽检）

---

## 六、已有正确格式的参考样本

chap-18 到 chap-30 已经有完整的英文翻译，格式正确。你翻译时应**参考这些章节的英文风格和格式**：

- ✅ 参考样章：`chap-18-台積電篇一·第十四章/source/page_188.md`
- ✅ 参考样章：`chap-25-台積電篇二·第二十章/source/page_288.md`
- ✅ 参考样章：`chap-30-台積電篇二·第二十五章/source/page_355.md`

读取这些文件，看英文段落的措辞、句式、节奏，然后按同样的标准翻译缺失的页面。

---

## 七、交付验收标准

翻译全部完成后：

- [ ] 143 个页面文件每页都有 `<div class="rebook-translation">` + `<p class="en-para">` 英文翻译
- [ ] 每个文件英文段数 == 中文段落数
- [ ] 全部 45 章（chap-00 到 chap-44）渲染成功生成 output.html
- [ ] 输出 HTML 中繁体字数量为 0（使用 OpenCC 检测）
- [ ] 导航页 `output/full/preview_book.html` 全部 45 个链接跳转正常
- [ ] 英文品质符合 Isaacson 传记 + HBR 商业语言风格

---

## 八、关键提醒

1. **只改 source/ 里的 page_XXX.md**，不要直接改 output.html
2. **保留所有已有内容**（标题、Cheat Sheet、修辞赏析、背景知识延伸），只在中到位置插入 rebook-translation 块
3. **不要修改 Cheat Sheet 中的英文术语和造句**（已经过审核）
4. **不要修改 修辞赏析 的 zh/en 内容**（已经过审核）
5. **翻译格式错误会导致 renderer 无法解析**，输出 HTML 中将丢失英文。格式请严格按第三节执行
6. 翻译完成后**必须重新渲染**，输出新的 output.html
7. 渲染命令中的路径含空格，**务必用引号包裹**
