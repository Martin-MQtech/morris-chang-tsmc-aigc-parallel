# 给 Agnes 的收尾任务（剩余 ~70 页）

还有最后约 70 页英文翻译没做完。清单在：

```
/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift/下册项目工作区/remaining_71.txt
```

## 核心要求（务必遵守）

### 1. 格式：必须用 HTML div，不要用 fenced code block

**正确格式**（每段中文后插入）：

```html
<div class="rebook-translation">
<span class="rebook-translation__label">ReadShift 双语翻译</span>
<p class="en-para">English translation paragraph 1.</p>
<p class="en-para">English translation paragraph 2.</p>
</div>
```

**错误格式**（会导致 renderer 无法解析）：
- 不要写 ```rebook-translation（fenced code block）
- 不要用纯文本英文不加 `<p class="en-para">` 包裹

### 2. 段落 1:1 配对

每个中文正文段落 → 一个 `<p class="en-para">`，不多不少。

### 3. 不要改的内容

- Cheat Sheet · 商业语汇（已有，不要改）
- 修辞赏析（已有，不要改）
- 背景知识延伸（已有，不要改）
- 标题（# / ##）

### 4. 翻译风格（Isaacson 传记 × HBR 商业英语）

- 过去时叙事，克制优雅，让事实说话
- 动词精准：generate revenue（不说 make money）、outperform rivals（不说 beat competitors）、pivot（不说 change direction）、expand into adjacent markets（不说 go to new markets）
- 长短句交替，句号后不超过 25 词
- 专有名词原文保留：TI、TSMC、Intel、Stanford、MIT
- 禁止：感叹号、口语化、"In my opinion..." 插入语、中式英语

### 5. 参考样章（请先读取体会风格）

- `/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift/下册项目工作区/chap-18-台積電篇一·第十四章/source/page_188.md`
- `/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift/下册项目工作区/chap-30-台積電篇二·第二十五章/source/page_355.md`

## 工作流

1. 逐文件：读 page_XXX.md → 翻译中文正文 → 插入 `<div class="rebook-translation">` 块 → 写回
2. 完成所有 ~70 页后通知
3. 需要渲染时运行：`node render_html_v9.js --chapter <章号> --out "<路径>/chap-<章号>-<slug>/output.html"`
