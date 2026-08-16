import os
import re
import json

WORKSPACE = "/Users/martin/Documents/20260812MartinGitHub /20260816 Morris Chang & TSMC"

print("--- Step 1: Modifying tools/build_all_episodes.py ---")
build_script_path = os.path.join(WORKSPACE, "tools/build_all_episodes.py")
with open(build_script_path, "r", encoding="utf-8") as f:
    build_code = f.read()

# 1. Update ep00 image path
build_code = build_code.replace(
    '"image_path": "./设计资产/封面/封面_上册_蓝图晶圆版.jpg",\n        "prev_link": "index.html",',
    '"image_path": "./设计资产/封面/封面_排版版.jpg",\n        "prev_link": "index.html",'
)

# 2. Check if hero split grid in build_all_episodes has special handling for ep00
# Let's inspect where hero-split-grid is defined in build_all_episodes.py
# We can inject hero_left_extra and hero_right_figure
hero_split_pattern = r'<div class="hero-split-grid">.*?</div>\s*</div>\s*</header>'

# Let's search how hero-split-grid is constructed in build_all_episodes.py
old_hero_grid = """      <div class="hero-split-grid">
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
      </div>"""

new_hero_grid = """{hero_grid_html}"""

# In the loop where ep is processed, we can construct hero_grid_html:
hero_grid_construct = """    # Hero split grid customization
    if ep_id == "00":
        hero_grid_html = f'''      <div class="hero-split-grid">
        <div class="hero-left-col">
          <div class="tagline-box" style="margin-top: 0;">
            <div class="tagline-zh">“{ep["tagline_zh"]}”</div>
            <div class="tagline-en">"{ep["tagline_en"]}"</div>
          </div>
          <div class="attribution-box" style="margin-top: 14px; padding: 14px 16px; background: rgba(245, 158, 11, 0.05); border: 1px dashed rgba(245, 158, 11, 0.3); border-radius: 10px; font-size: 12.5px; line-height: 1.6; color: #d1cdc7;">
            <div style="font-weight: 600; color: var(--amber); margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
              <span>📚 致敬经典 · 支持正版</span>
            </div>
            <p style="margin-bottom: 6px;">本项目为 AIGC 原创平行叙事二创与研读作品，故事线索与事实脉络取材自张忠谋先生权威史料与自传母本。我们强烈推荐读者购买支持张忠谋先生正版传记图书《张忠谋自传》（天下文化 / 远见出版），获取详实完整的第一手时代细节。</p>
            <p style="font-style: italic; font-size: 11.5px; color: var(--muted); font-family: var(--en);">Support Official Publication: This parallel biography is an original AIGC creative work inspired by historical records. We encourage readers to purchase the authentic authorized volumes.</p>
          </div>
        </div>

        <div class="hero-right-col">
          <figure class="lead-artwork-figure" style="background: transparent; border: none; box-shadow: none;">
            <img class="lead-artwork-img" src="{ep["image_path"]}" alt="{ep["title_zh"]} 全册封面" style="object-fit: contain; max-height: 380px; width: 100%; border-radius: 12px; box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 0 1px var(--line);" loading="eager">
          </figure>
        </div>
      </div>'''
    else:
        hero_grid_html = f'''      <div class="hero-split-grid">
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
      </div>'''"""

# Replace old hero grid in template with {hero_grid_html}
if old_hero_grid in build_code:
    build_code = build_code.replace(old_hero_grid, new_hero_grid)
    # Insert hero_grid_construct before html_template = f"""
    build_code = build_code.replace("    html_template = f\"\"\"<!DOCTYPE html>", hero_grid_construct + "\n    html_template = f\"\"\"<!DOCTYPE html>")
    print("Replaced hero grid in build_all_episodes.py successfully.")
else:
    print("Warning: old_hero_grid not matched exactly, inspecting...")

# 3. Subtitle Viewport Auto-Scroll Bug Fix in JS
old_scroll_js = """    function setActiveCue(index) {
      if (index === activeCueIndex) return;
      
      // Remove previous active classes
      if (activeCueIndex !== -1) {
        const prevRow = document.getElementById('sub-row-' + activeCueIndex);
        if (prevRow) prevRow.classList.remove('active');
        const prevPara = document.getElementById('para-' + activeCueIndex);
        if (prevPara) prevPara.classList.remove('current-reading');
      }

      activeCueIndex = index;
      const activeRow = document.getElementById('sub-row-' + index);
      if (activeRow) {
        activeRow.classList.add('active');
        if (autoScroll && subtitlesViewport) {
          const rowTop = activeRow.offsetTop;
          const rowHeight = activeRow.offsetHeight;
          const containerHeight = subtitlesViewport.clientHeight;
          subtitlesViewport.scrollTo({
            top: rowTop - (containerHeight / 2) + (rowHeight / 2),
            behavior: 'smooth'
          });
        }
      }

      const activePara = document.getElementById('para-' + index);
      if (activePara) {
        activePara.classList.add('current-reading');
      }
    }"""

new_scroll_js = """    let isUserScrolling = false;
    let userScrollTimer = null;

    if (subtitlesViewport) {
      subtitlesViewport.addEventListener('wheel', () => {
        isUserScrolling = true;
        clearTimeout(userScrollTimer);
        userScrollTimer = setTimeout(() => { isUserScrolling = false; }, 2000);
      }, { passive: true });

      subtitlesViewport.addEventListener('touchmove', () => {
        isUserScrolling = true;
        clearTimeout(userScrollTimer);
        userScrollTimer = setTimeout(() => { isUserScrolling = false; }, 2000);
      }, { passive: true });
    }

    function scrollSubtitleToCenter(container, activeElement) {
      if (!container || !activeElement || !autoScroll || isUserScrolling) return;
      
      // Calculate relative position strictly INSIDE the container viewport
      const containerRect = container.getBoundingClientRect();
      const elementRect = activeElement.getBoundingClientRect();
      
      const elementRelativeTop = elementRect.top - containerRect.top + container.scrollTop;
      const targetScrollTop = elementRelativeTop - (container.clientHeight / 2) + (elementRect.height / 2);
      
      container.scrollTo({
        top: Math.max(0, targetScrollTop),
        behavior: 'smooth'
      });
    }

    function setActiveCue(index) {
      if (index === activeCueIndex) return;
      
      // Remove previous active classes
      if (activeCueIndex !== -1) {
        const prevRow = document.getElementById('sub-row-' + activeCueIndex);
        if (prevRow) prevRow.classList.remove('active');
        const prevPara = document.getElementById('para-' + activeCueIndex);
        if (prevPara) prevPara.classList.remove('current-reading');
      }

      activeCueIndex = index;
      const activeRow = document.getElementById('sub-row-' + index);
      if (activeRow) {
        activeRow.classList.add('active');
        if (autoScroll && subtitlesViewport) {
          scrollSubtitleToCenter(subtitlesViewport, activeRow);
        }
      }

      const activePara = document.getElementById('para-' + index);
      if (activePara) {
        activePara.classList.add('current-reading');
      }
    }"""

# Notice in Python f-string template double curly braces are used
# Let's see if double curly braces are needed
old_scroll_js_doubled = old_scroll_js.replace("{", "{{").replace("}", "}}")
new_scroll_js_doubled = new_scroll_js.replace("{", "{{").replace("}", "}}")

if old_scroll_js_doubled in build_code:
    build_code = build_code.replace(old_scroll_js_doubled, new_scroll_js_doubled)
    print("Replaced subtitle scroll JS in build_all_episodes.py successfully.")
elif old_scroll_js in build_code:
    build_code = build_code.replace(old_scroll_js, new_scroll_js)
    print("Replaced subtitle scroll JS (single brace) in build_all_episodes.py successfully.")
else:
    print("Warning: old_scroll_js not matched exactly, inspecting...")

with open(build_script_path, "w", encoding="utf-8") as f:
    f.write(build_code)

print("build_all_episodes.py written.")
