# EPUB 制作规范（一册 18 期 · 出版级 EPUB 3.0）

> 本规范是对《HTML 转出版级 EPUB 电子书全流程标准指南》的**查缺补漏升级版**：
> 继承其正确做法，修正其错误与盲区，并适配本项目「一册 18 期 · AIGC 原创 · 双语平行 · 暗黑金蓝签名」的实际情况。
> 生产脚本：`tools/make_epub.py`（一键生成，重跑即刷新）。

---

## 一、对原指南的裁断（Pro 复核结论）

### ✅ 保留（正确，已实测有效）

| 项 | 说明 |
|---|---|
| mimetype 第一位、无压缩 | `application/epub+zip`，否则 Apple Books 拒收 |
| nav.xhtml + toc.ncx 双目录 | EPUB3 与 EPUB2 兼容缺一不可 |
| 底色透明 | 不锁背景色，适配夜间/护眼绿/羊皮纸 |
| 防撕裂 | 卡片/图片 `page-break-inside: avoid`，标题 `page-break-after: avoid` |
| 双层目录树 | 章 → 小节（Subsection） |
| 双语差异化排版 | 中文衬线正文 + 英文罗马衬线、字号略缩 |

### ❌ 修正（原指南的错 / 不适合本项目）

1. **封面用「TSMC 核心标识」→ 弃用**。TSMC 为注册商标，本作品非官方授权传记，用其 logo 有商标侵权风险；且栏目是 AIGC 原创平行传记，不该绑官方标识。
2. **「Production Note · 学习交流用途」免责 → 不采用**。那只适用于对版权原书的二创。我们是原创，但按主理人定（2026-08-15）改用「AIGC 原创 · 仅供学习交流 · 禁止商业用途」声明。
3. **章节插图「钢笔木刻 + 暖色水彩」→ 不采用**。与主理人已拍板的「暗黑虚空 + 琥珀金主光 + 天蓝轮廓光」签名冲突。

### ➕ 补齐（原指南遗漏的关键缺口）

1. **双语 lang 标注（最大遗漏）**：中英混排必须给元素加 `lang`/`xml:lang`，否则阅读器 TTS 用错语音、词典/拼写错乱。
2. **EPUB3 元数据与校验**：`dcterms:modified` 必填；唯一 `dc:identifier`(UUID)；`properties="nav"`/`properties="cover-image"` 声明；`nav.xhtml` 含 `landmarks`；成品用 **epubcheck** 校验（Apple Books 上架关键）。
3. **字体策略**：CJK 字体嵌入动辄 10–20MB，默认**不嵌入**，依赖系统衬线（宋体/思源宋体/Georgia）；仅确需时做子集化。
4. **图片优化**：封面 1600×2400+ JPG；正文插图压缩控制体积；配 alt 文本。
5. **无障碍**：`epub:type` 语义、alt 文本、标题层级清晰。
6. **Kindle 链路**：EPUB 不直接进 Kindle，需 Kindle Previewer/Create 转 KFX/MOBI（另列一步）。
7. **打包洁净**：排除 `.DS_Store`/`__MACOSX`；用 Python `zipfile` 精确控制 mimetype 第一位 + `ZIP_STORED`。
8. **多设备实测清单**：Apple Books / 微信读书 / 多看 / Kobo / Google Play Books 逐项验收。
9. **有声同步（Media Overlays）**：EPUB3 支持 SMIL read-aloud；我们有中英双轨 mp3，预留「有声电子书」接口（非本版必需）。

---

## 二、本项目 EPUB 骨架

```
台积电张忠谋-传记时间线的平行世界.epub (ZIP)
├── mimetype                      # application/epub+zip，第一位、无压缩
├── META-INF/
│   └── container.xml             # 指向 OEBPS/content.opf
└── OEBPS/
    ├── content.opf               # 元数据 + Manifest + Spine（EPUB3）
    ├── toc.ncx                   # EPUB2 双层目录树
    ├── Stylesheet.css            # 透明底 + 双语 lang 排版
    ├── Text/
    │   ├── cover.xhtml           # 独立封面页
    │   ├── title_page.xhtml      # 扉页（书名/作者/版权声明）
    │   ├── reading_guide.xhtml   # 阅读指南（双语约定 + 跨设备阅读设置）
    │   ├── nav.xhtml             # EPUB3 导航（toc + landmarks）
    │   └── chap_01..18.xhtml     # 每期一章
    └── Images/
        ├── cover.jpg             # 封面（2:3，由 设计资产/封面/封面.png 转）
        └── chapter_art_01..18.jpg  # 章首插图（3:2，由 设计资产/插图/ 转）
```

---

## 三、双语 lang 标注规范（本项目硬性）

> **主理人定（2026-08-15）**：中英「一段中文 + 一段英文」段落级交错，逐段对照——真正学英语者可即时比对。已确认现有中英稿是**逐段对齐**的（每段中文有对应英文段），故可直接交错，不需重写内容。

```html
<h3 class="subsection" id="sub-01-1">
  <span class="zh" xml:lang="zh-CN" lang="zh-CN">开场</span>
  <span class="en" xml:lang="en" lang="en">Opening</span>
</h3>
<p class="cn-para" xml:lang="zh-CN" lang="zh-CN">中文段一……</p>
<p class="en-para" xml:lang="en" lang="en">English paragraph one…</p>
<p class="cn-para" xml:lang="zh-CN" lang="zh-CN">中文段二……</p>
<p class="en-para" xml:lang="en" lang="en">English paragraph two…</p>
```

- 每段各自 `lang`/`xml:lang`（阅读器 TTS 用对语音、词典/拼写正确）。
- 视觉区分：中文正文深色宋体、英文段小一号罗马衬线 + 左浅色描边/淡底，交错一眼可辨、可跳过。
- 小节标题双语并列（中文主 + 英文斜体副题），TOC 只取中文标题作二级目录。

---

## 四、封面与插图规范（本项目）

| 资产 | 规格 | 来源 |
|---|---|---|
| 封面 | 2:3 竖版，暗黑虚空 + 琥珀金主光 + 天蓝轮廓光；**排版版**烙入书名/副题/标语/元信息（宋体+Didot，琥珀金天蓝签名） | `设计资产/封面/封面_排版版.jpg`（由 `tools/make_typography.py` 合成） |
| 章首图 | 3:2 横版 × 18，每张一个核心隐喻；**排版版**烙入期号·时间·中英标题，配中英图注 + alt | `设计资产/插图/排版版/第XX期-*.jpg` |

> 版式文字烙入图（`tools/make_typography.py`），正文仍以 HTML 文本承载（可选中/可检索/TTS 正确发音）；章节标题以 `sr-only` 保留无障碍语义。

---

## 五、打包命令（Python，避免 zip 命令的垃圾文件问题）

`tools/make_epub.py` 用 `zipfile` 精确控制：`mimetype` 首个写入且 `ZIP_STORED`（不压缩），其余 `ZIP_DEFLATED`，天然排除 `.DS_Store`/`__MACOSX`。

---

## 六、校验与验收清单

- [ ] `epubcheck` 通过（0 error；如未装，运行 `tools/make_epub.py --check` 做结构自检）
- [ ] Apple Books：封面显示、双层目录、夜间模式、字号缩放、图片不撕裂
- [ ] 微信读书 / 多看：目录层级、正文排版正常
- [ ] 中英混排：TTS 朗读语言正确（验证 lang 标注生效）
- [ ] 全书体积可控（封面+18 图压缩后 < 20MB）

---

## 七、与「AIGC 原创」的衔接

扉页版权声明写：

> 本作品为 AIGC 原创，基于公开资料和史实创作加设计 · 仅供学习交流，禁止商业用途 · github.com/Martin-MQtech/ReadShift

（主理人定 2026-08-15：虽为原创，但采用「仅供学习交流、禁止商业用途」的保守非商用定位。）
