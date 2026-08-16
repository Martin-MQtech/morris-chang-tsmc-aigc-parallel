# 封面 · 交给 Gemini 的需求说明（生图分工）

> 分工：**我出思想与排版，Gemini 只出图。** 文字（书名/标识/说明）由我的排版合成器 `tools/make_typography.py` 烙上去，**不让生图模型画字**（避免中文乱码）。

---

## 一、最终封面长什么样（我方排版负责，仅供 Gemini 预留空间）

| 区域 | 内容 |
|---|---|
| 内嵌细框 | 暖白细线框 |
| 顶部 ~12% | 系列标识 `AIGC ORIGINAL · PARALLEL BIOGRAPHY` |
| 中部 | **主视觉**（两条平行光轨 + 芯片）——留给 Gemini |
| 底部 ~42% | 书名《台积电张忠谋》+ 副题 + 英文名 + 品牌标志 + 标语 + 出品 + 元信息 + 「AIGC 原创」徽章 |

→ 所以 Gemini 的图**中部放主视觉，顶部 12% 和底部 42% 必须暗而干净**，给文字留白。

---

## 二、给 Gemini 的提示词（整段粘贴即可）

```
You are a world-class book cover art director and photographer.

TASK: Create the COVER ART (background layer only) for a premium bilingual
biography book cover. Portrait 2:3.

SUBJECT (keep this established motif, refine it to premium book-cover quality):
Two parallel luminous threads run horizontally across an infinite dark void.
The upper thread glows warm amber gold — the path of one man's life.
The lower thread glows cool sky blue — the path of the world around him.
At the exact center, between the two threads, a single translucent circular
silicon wafer rises, etched with faint, precise circuit traces — the meeting
place where two parallel timelines resonate without ever merging.

STYLE LOCK (must follow exactly):
- Infinite dark void, extreme negative space, minimalist abstract.
- Materials: translucent silicon, luminous light threads, frosted acrylic,
  polished dark metal.
- Lighting: amber gold (#F59E0B) key light from upper left on the upper thread;
  sky blue (#38BDF8) rim light on the lower thread and the chip edges;
  studio black (#0A0A0A) background.
- Premium photographic quality, high contrast, cinematic, 8k, photorealistic.

COMPOSITION — CRITICAL (reserve space for typography to be overlaid later):
- Keep the chip + threads motif in the MIDDLE band, roughly 20%–48% of height.
- The TOP ~12% must stay dark, smooth, and uncluttered (for a series eyebrow line).
- The BOTTOM ~42% must stay dark, smooth, and nearly empty (for the title block).
- Do NOT place any bright element in the bottom 42% or the top 12%.

ABSOLUTE PROHIBITIONS:
1. ZERO text, numbers, labels, or any readable characters (text is overlaid later).
2. NO literal depictions, NO cliché tech symbols (no robotic arms, brain circuits,
   gears, rockets, shields, locks, globes, circuit boards).
3. NO AI-aesthetic (no blue-purple neon gradients, holographic figures, scattered
   particles, glowing wave lines, grid backgrounds, excessive glow).
4. NO explanatory layouts (no arrows, side-by-side, labels).

OUTPUT:
- Portrait 2:3, high resolution (at least 1536×2304, ideally 2048×3072 or higher).
- Save as PNG to: 设计资产/封面/封面_gemini.png
```

---

## 三、Gemini 回传后我做的事

1. 收到 `设计资产/封面/封面_gemini.png`；
2. 把 `tools/make_typography.py` 的封面输入指向它；
3. 跑一遍 → 自动烙上：书名中英 / 系列标识 / 品牌标志 / 标语 / 出品 / 元信息 / 框线 / 「AIGC 原创」徽章；
4. 同步重生成 电子书 + EPUB + 官网。

---

## 四、输出规格速记

| 项 | 值 |
|---|---|
| 目标文件 | `设计资产/封面/封面_gemini.png` |
| 比例 | 2:3 竖版 |
| 最小尺寸 | 1536×2304（理想 2048×3072） |
| 格式 | PNG（或最高质量 JPG） |
| 画面内文字 | 零 |
