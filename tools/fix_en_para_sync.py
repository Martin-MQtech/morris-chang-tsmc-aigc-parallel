#!/usr/bin/env python3
"""修复19个单期页面的英文轨时间戳问题（全站修复）：

定位到的三处缺陷：
1. switchTrack 只更新 sub-row 时间戳，不更新正文段落（bilingual-para）
   的 onclick 与 para-time-badge —— 切到英文轨后点正文段落跳到中文轨时间（错位）。
2. setActiveCue 用 getElementById('para-' + index)（0-based），但 para id 从 1 开始，
   且 id 有缺失 → 正文段落高亮永远失效。
3. 段数不匹配的4集（ep02/03/09/16）sub-row 数量与目标轨 cue 数量不一致时，
   只更新前 min 行，多余的 cue 没有字幕行 / 多余的行保留旧时间戳。

修复方式：
- 给每个 bilingual-para 注入 data-cue-idx（内容匹配 zh cue；未匹配段按时间插入点映射）
- setActiveCue 改用 [data-cue-idx] 查询高亮
- switchTrack 中：sub-row 数量不匹配时动态重建；段落 onclick/badge 随轨更新
  （经 ZH2EN 映射数组对齐中英 cue）
"""
import re
import json
import bisect
import html as html_mod
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    s = html_mod.unescape(s)
    s = s.replace("**", "").replace("__", "")
    return re.sub(r"\s+", "", s)


def build_zh2en(cues_zh, cues_en):
    """zh cue idx -> en cue idx（按 zh 文本精确匹配；未匹配 -> en 末尾）。"""
    en_by_zh = {}
    for ei, ec in enumerate(cues_en):
        if ec.get("zh"):
            en_by_zh.setdefault(norm(ec["zh"]), ei)
    zh2en = []
    for zc in cues_zh:
        z = norm(zc.get("zh", ""))
        if z and z in en_by_zh:
            zh2en.append(en_by_zh[z])
        else:
            zh2en.append(len(cues_en) - 1)  # 文末附录/预告 -> en 末 cue
    return zh2en


SUB_ROW_BLOCK = re.compile(
    r"(// Update sub-row timing \+ onclick to match active track\n"
    r"        const ac = currentTrack === 'en' \? EP_CUES_EN : EP_CUES;\n"
    r"        document\.querySelectorAll\('\.sub-row'\)\.forEach\(\(row, idx\) => \{\n"
    r"          if \(idx < ac\.length\) \{\n"
    r"            const c = ac\[idx\];\n"
    r"            row\.dataset\.start = c\.start\.toFixed\(2\);\n"
    r"            row\.dataset\.end = c\.end\.toFixed\(2\);\n"
    r"            row\.setAttribute\('onclick', 'seekAndPlay\(' \+ c\.start\.toFixed\(2\) \+ '\)'\);\n"
    r"            const timeTag = row\.querySelector\('\.sub-time-tag'\);\n"
    r"            if \(timeTag\) timeTag\.textContent = formatTime\(c\.start\);\n"
    r"          \}\n"
    r"        \}\);)"
)

NEW_SWITCH_BLOCK = """// Update sub-row timing + onclick to match active track
        const ac = currentTrack === 'en' ? EP_CUES_EN : EP_CUES;
        const existingRows = document.querySelectorAll('.sub-row');
        if (existingRows.length !== ac.length) {
          rebuildSubRows(ac);  // 段数不匹配（ep02/03/09/16）时按目标轨重建
        } else {
          existingRows.forEach((row, idx) => {
            const c = ac[idx];
            row.dataset.start = c.start.toFixed(2);
            row.dataset.end = c.end.toFixed(2);
            row.setAttribute('onclick', 'seekAndPlay(' + c.start.toFixed(2) + ')');
            const timeTag = row.querySelector('.sub-time-tag');
            if (timeTag) timeTag.textContent = formatTime(c.start);
          });
        }
        // Update bilingual-para timing + badge to match active track
        document.querySelectorAll('.bilingual-para').forEach(para => {
          const ci = parseInt(para.dataset.cueIdx, 10);
          if (isNaN(ci)) return;
          const pi = currentTrack === 'en' ? (ZH2EN[ci] !== undefined ? ZH2EN[ci] : EP_CUES_EN.length - 1) : ci;
          const c = ac[Math.min(pi, ac.length - 1)];
          if (!c) return;
          para.setAttribute('onclick', 'seekAndPlay(' + c.start.toFixed(2) + ')');
          const badge = para.querySelector('.para-time-badge');
          if (badge) badge.textContent = formatTime(c.start);
        });"""

SET_ACTIVE_PARA_OLD = "const activePara = document.getElementById('para-' + index);"
SET_ACTIVE_PARA_NEW = ("const activePara = document.querySelector("
                       "'.bilingual-para[data-cue-idx=\"' + index + '\"]');")


def esc(s):
    return html_mod.escape(s or "", quote=True)


def rebuild_subrows_js():
    return """
    function rebuildSubRows(cues) {
      const vp = document.getElementById('subtitles-viewport');
      if (!vp) return;
      vp.innerHTML = cues.map((c, i) =>
        '<div class="sub-row" id="sub-row-' + i + '" data-index="' + i + '"' +
        ' data-start="' + c.start.toFixed(2) + '" data-end="' + c.end.toFixed(2) + '"' +
        ' onclick="seekAndPlay(' + c.start.toFixed(2) + ')">' +
        '<span class="sub-time-tag">' + formatTime(c.start) + '</span>' +
        '<div class="sub-content"><div class="sub-zh">' + (c.zh || '') + '</div>' +
        '<div class="sub-en">' + (c.en || '') + '</div></div></div>'
      ).join('\\n');
    }
"""


def patch_episode(path):
    src = open(path, encoding="utf-8").read()
    orig = src

    cues_zh = json.loads(re.search(r"const EP_CUES = (\[.*?\]);", src, re.S).group(1))
    cues_en = json.loads(re.search(r"const EP_CUES_EN = (\[.*?\]);", src, re.S).group(1))
    zh2en = build_zh2en(cues_zh, cues_en)
    starts = [c["start"] for c in cues_zh]

    # 1) 注入 data-cue-idx 到每个 bilingual-para
    def add_cue_idx(m):
        pid, onclick = int(m.group(1)), float(m.group(2))
        # 内容匹配
        body = m.group(0)
        zm = re.search(r'<p class="zh-para">(.*?)</p>', body, re.S)
        ci = None
        if zm:
            z = norm(zm.group(1))
            for i, c in enumerate(cues_zh):
                if z and z == norm(c.get("zh", "")):
                    ci = i
                    break
        if ci is None:
            ci = bisect.bisect_left(starts, onclick)
            if ci >= len(cues_zh):
                ci = len(cues_zh) - 1
        return body.replace(
            f'class="bilingual-para" id="para-{pid}"',
            f'class="bilingual-para" id="para-{pid}" data-cue-idx="{ci}"', 1)

    src, n_para = re.subn(
        r'<div class="bilingual-para" id="para-(\d+)" onclick="seekAndPlay\(([\d.]+)\)"',
        add_cue_idx, src)
    if n_para == 0:
        print(f"  ⚠️ 未找到 bilingual-para，跳过")

    # 2) setActiveCue 高亮改用 data-cue-idx
    if SET_ACTIVE_PARA_OLD in src:
        src = src.replace(SET_ACTIVE_PARA_OLD, SET_ACTIVE_PARA_NEW, 1)
    else:
        print(f"  ⚠️ setActiveCue 未匹配")

    # 3) switchTrack 的 sub-row 更新块替换为双轨完整版
    m = SUB_ROW_BLOCK.search(src)
    if not m:
        print(f"  ⚠️ switchTrack sub-row 块未匹配")
    else:
        src = src[:m.start()] + NEW_SWITCH_BLOCK + src[m.end():]

    # 4) 注入 ZH2EN 映射常量（放在 EP_CUES_EN 定义之后）
    zh2en_js = "const ZH2EN = " + json.dumps(zh2en) + ";"
    anchor = re.search(r"const EP_CUES_EN = (\[.*?\]);", src, re.S)
    if anchor and "const ZH2EN" not in src:
        src = src[:anchor.end()] + "\n    " + zh2en_js + src[anchor.end():]

    # 5) 注入 rebuildSubRows 函数（放在 switchTrack 之前）
    if "function rebuildSubRows" not in src:
        anchor2 = re.search(r"    function switchTrack\(track\) \{", src)
        if anchor2:
            src = src[:anchor2.start()] + rebuild_subrows_js() + "\n" + src[anchor2.start():]

    if src == orig:
        print(f"  ❌ 无任何修改（可能结构已变化）")
        return False
    open(path, "w", encoding="utf-8").write(src)
    return True


def main():
    ok = fail = 0
    for i in range(19):
        path = os.path.join(BASE, f"episode-{i:02d}.html")
        print(f"ep{i:02d}:")
        try:
            if patch_episode(path):
                ok += 1
            else:
                fail += 1
        except Exception as e:
            fail += 1
            print(f"  ❌ 异常: {e}")
    print(f"\n完成：成功 {ok}，失败 {fail}")


if __name__ == "__main__":
    main()
