#!/usr/bin/env python3
"""
下册章节切分脚本：扫描 原始素材/下册_1964-2018/章节提取/ 目录，
按 <!-- 原書第XX頁 --> 标记切分为 per-page source 文件。
输出目录结构：下册项目工作区/chap-XX-<slug>/source/page_XXX.md
"""

import os
import re

WORKSPACE = "/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift"
SOURCE_DIR = os.path.join(WORKSPACE, "原始素材", "下册_1964-2018", "章节提取")
OUTPUT_DIR = os.path.join(WORKSPACE, "下册项目工作区")


def slugify(filename):
    """从文件名提取 slug：去掉 'NN_' 前缀和 .md 后缀"""
    name = filename.replace(".md", "")
    # 去掉开头的数字编号 "00_"
    match = re.match(r"\d+_(.+)", name)
    if match:
        return match.group(1)
    return name


def split_chapter(filename):
    src_file = os.path.join(SOURCE_DIR, filename)
    slug = slugify(filename)
    chapter_id = int(re.match(r"(\d+)", filename).group(1))

    out_dir = os.path.join(OUTPUT_DIR, f"chap-{chapter_id:02d}-{slug}", "source")
    os.makedirs(out_dir, exist_ok=True)

    with open(src_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取文件标题（第一个 # 标题行）
    header_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    header_title = header_match.group(0) if header_match else ""

    # 按 <!-- 原書第XX頁 --> 切分
    pattern = r"<!--\s*原書第(\d+)頁\s*-->"
    parts = re.split(pattern, content)

    pages = []
    if len(parts) == 1:
        # 无页码标记，整章作为一个 page
        pages = [(chapter_id, parts[0].strip())]
    else:
        # parts[0] 是文件头，之后 [页码, 正文, 页码, 正文...]
        i = 1
        while i < len(parts):
            page_num = int(parts[i])
            body = parts[i + 1].strip() if i + 1 < len(parts) else ""
            pages.append((page_num, body))
            i += 2

    # 写入 per-page 文件
    saved = []
    for idx, (page_num, body) in enumerate(pages):
        fname = f"page_{page_num:03d}.md"
        # 第一页添加章节标题
        if idx == 0 and header_title:
            body = header_title + "\n\n" + body
        fpath = os.path.join(out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(body + "\n")
        saved.append(fname)

    print(f"  [{chapter_id:02d}] {slug} -> {len(pages)} pages")
    return chapter_id, slug, len(pages), out_dir


def main():
    print("=== 下册章节切分开始 ===")
    files = sorted(
        f for f in os.listdir(SOURCE_DIR)
        if re.match(r"\d{2}_.+\.md", f)
    )
    print(f"共 {len(files)} 个章节文件\n")

    results = []
    for fn in files:
        ch_id, slug, count, out_dir = split_chapter(fn)
        results.append((ch_id, slug, count, out_dir))

    print(f"\n=== 切分完成：{len(results)} 章 ===")
    total_pages = sum(r[2] for r in results)
    print(f"总页数：{total_pages}")
    return results


if __name__ == "__main__":
    main()
