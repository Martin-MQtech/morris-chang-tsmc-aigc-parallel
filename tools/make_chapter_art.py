#!/usr/bin/env python3
"""
ReadShift 章节插图批量生成（gpt-image-2 · llm-token.cn 代理）

用法:
    python3 tools/make_chapter_art.py [起始期号] [结束期号]

    默认生成第 01–18 期全部插图（3:2 横版, 1536x1024），
    每张 prompt 同步落盘到 设计资产/插图/prompts/pXX.txt 供回溯。
    可用参数只生成区间, 便于补单:  python3 tools/make_chapter_art.py 14 14

风格: 与封面同源 —— 暗黑虚空 + 琥珀金主光 + 天蓝轮廓光 + 单一焦点 + 零文字。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_images import generate  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART_DIR = os.path.join(BASE, "设计资产", "插图")
PROMPT_DIR = os.path.join(ART_DIR, "prompts")

STYLE = """You are a visual metaphor master, working like a TIME Magazine cover photographer. Convey a theme precisely with a single image containing absolutely zero text.

ABSOLUTE PROHIBITIONS:
1. ZERO TEXT — no titles, labels, numbers, or any readable characters, including gibberish.
2. NO LITERAL DEPICTIONS, NO CLICHÉ TECH SYMBOLS — no robotic arms, brain circuits, gears, rockets, shields, locks, globes.
3. NO AI-AESTHETIC — no blue-purple neon gradients, holographic figures, scattered particles, glowing wave lines, grid backgrounds, excessive glow.
4. NO EXPLANATORY LAYOUTS — no arrows, side-by-side comparisons, labels.
5. NO PHYSICAL ENVIRONMENTS — no desks, chairs, rooms, walls, horizons, machinery. Objects float in abstract space.

SPACE: Infinite dark void (studio black #0A0A0A). Extreme negative space. Objects float with no support surface.
MATERIALS: Semi-transparent glass, frosted acrylic, luminous wireframes, polished dark metal, refractive surfaces.
LIGHTING SIGNATURE: Primary amber gold (#F59E0B) warm side light (~70%), secondary sky blue (#38BDF8) rim light (~30%). Colors manifest through LIGHT and REFRACTION, never flat paint.
COMPOSITION: Single focal point, subject occupies 30-50% of frame, rest is breathing space. Landscape orientation.
OUTPUT: High contrast, single focal point, premium photographic quality, dramatic cinematic lighting, 8k resolution, photorealistic rendering.

---
"""

# (期号, 标题, 英文场景隐喻)
EPISODES = [
    (1, "逃难的孩子",
     "A single small worn leather suitcase floating in a vast dark void, its surface catching warm amber key light, "
     "cool sky blue rim light tracing its edges and one loose strap drifting weightlessly. The suitcase hangs slightly ajar, "
     "a faint warm glow seeping from the gap — a childhood packed away too early. "
     "Minimalist, single focal point, extreme negative space."),
    (2, "考不进去的南开与作家梦",
     "A towering closed door floating in the dark void, a thin sliver of warm amber light leaking through its bottom edge — "
     "the school behind it, unreachable. Before the door, a single solitary fountain pen floats, caught in cool sky blue rim light "
     "and casting a long shadow — a writer's dream born from a closed door. Minimalist, single focal point."),
    (3, "从黄浦江到查尔斯河",
     "Two abstract contour fragments of land suspended in a dark void, joined by one thin luminous thread of light. "
     "The left fragment glows warm amber gold — the homeland; the right fragment glows cool sky blue — the new world. "
     "A tiny lone boat silhouette hangs mid-crossing on the thread. Minimalist, cinematic, single focal point on the small boat."),
    (4, "四十封求职信",
     "Dozens of folded letters and envelopes drifting slowly through a dark void, most sinking into shadow. "
     "A single letter among them is illuminated by warm amber light, its edges rimmed in cool sky blue — "
     "the one reply among forty. Minimalist, dramatic, single focal point on the lit letter."),
    (5, "隔岸观火的叛乱",
     "A translucent glass wall standing in the dark void. Behind it, a distant warm amber glow flickers like a fire — "
     "the world he longs to enter. In front, a lone human silhouette in cool sky blue rim light, one hand pressed flat "
     "against the glass — watching from the other shore. Minimalist, single focal point."),
    (6, "德仪的太空竞赛岁月",
     "A single pristine silicon chip floating in the dark void, precision-engineered, its fine circuit traces glowing faintly "
     "under warm amber key light, cool sky blue rim light tracing its edges. It reads as a tiny artificial body readied for launch — "
     "silicon aimed at space. Not a planet, not cosmic, a precision-engineered object. Minimalist, single focal point."),
    (7, "半导体之巅的十年",
     "An abstract summit built from layers of stacked translucent silicon wafers, rising in the dark void. "
     "At the top stands a tiny lone human silhouette lit by warm amber key light, while the layered edges below catch "
     "cool sky blue rim light. Minimalist, dramatic, single focal point on the figure at the peak."),
    (8, "离开德州与受邀回台",
     "An empty executive chair floating in the dark void, warm amber light illuminating its now-vacant seat — "
     "the position left behind. From the distance, a thin beam of cool sky blue light reaches toward it across the darkness — "
     "the call from across the ocean. Absence metaphor, minimalist, single focal point."),
    (9, "纯代工的革命",
     "A vast empty glowing platform floating in the void, warm amber light radiating from within its surface, "
     "cool sky blue rim light tracing its edges. The platform stands empty, yet countless tiny points of light hover just "
     "above it, waiting to step on — a stage built for everyone but the builder. Minimalist, single focal point."),
    (10, "从台湾到世界",
     "A single polished brass bell floating in the dark void, its surface catching warm amber light. "
     "At the instant of being struck, concentric ripples of cool sky blue light radiate outward in all directions — "
     "the bell of New York ringing across the world. Minimalist, dramatic, single focal point."),
    (11, "记忆体的诱惑",
     "A single alluring crystal suspended in the dark void, glowing warm amber from within, its surface covered in fine "
     "granular memory-cell texture, cool sky blue rim light tracing its edges. It hangs just out of reach, beautiful and "
     "dangerous — temptation itself. Minimalist, single focal point."),
    (12, "逆周期的定力",
     "In a dark void, countless tiny points of light stream downward like falling water — those who fled. "
     "Against them, one strong column of warm amber light rises upward, its edges traced in cool sky blue — "
     "the one who invested while others retreated. Minimalist, dramatic contrast, single focal point."),
    (13, "交棒之痛",
     "A single luminous scepter floating in the dark void, its upper half bathed in warm amber light and its lower half "
     "in cool sky blue, suspended at an angle as if caught mid-exchange between two unseen hands — a baton given away "
     "and taken back. Minimalist, single focal point."),
    (14, "绚烂年代",
     "A single polished silicon chip floating in the dark void, radiating intense warm amber brilliance from its core, "
     "its faceted edges throwing precise ordered rays of cool sky blue light outward like a cut gem catching light — "
     "the brilliant era of a technological breakthrough. Minimalist, single focal point."),
    (15, "苹果来敲门",
     "A closed door floating in the dark void. Upon its surface falls a single apple-shaped patch of warm amber light, "
     "its silhouette carrying a subtle bite mark. The door's edges glow with faint cool sky blue rim light. "
     "Someone iconic is knocking. Minimalist, single focal point."),
    (16, "摩尔定律的守卫者",
     "A luminous staircase rising into the dark void, each step narrower and steeper than the last, thinning toward a single "
     "vanishing point of light at the top. The lower steps glow warm amber, the upper steps fade into cool sky blue — "
     "the lonely climb to keep a law alive. Minimalist, single focal point on the vanishing summit."),
    (17, "交棒与退休",
     "A conductor's baton laid gently to rest upon a small glowing pedestal, bathed in a spotlight of warm amber light, "
     "while soft ripples of cool sky blue light wash toward it from all sides like applause — the final bow. "
     "Minimalist, single focal point."),
    (18, "护国神山",
     "A vast, immovable mountain of translucent silicon crystal rising in the dark void, warm amber light pouring from its "
     "summit down its slopes, cool sky blue rim light tracing its edges, countless tiny points of light clustering at its base "
     "like a nation's lights — the sacred mountain that guards an island. Minimalist, monumental, single focal point."),
]


def main():
    args = sys.argv[1:]
    start = int(args[0]) if args else 1
    end = int(args[1]) if len(args) > 1 else 18

    os.makedirs(PROMPT_DIR, exist_ok=True)
    for num, title, scene in EPISODES:
        if num < start or num > end:
            continue
        prompt = STYLE + scene + "\n"
        prompt_file = os.path.join(PROMPT_DIR, f"p{num:02d}.txt")
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)
        out = os.path.join(ART_DIR, f"第{num:02d}期-{title}.png")
        print(f"[{num:02d}/18] 《{title}》", flush=True)
        generate(prompt, out, size="1536x1024", model="gpt-image-2")


if __name__ == "__main__":
    main()
