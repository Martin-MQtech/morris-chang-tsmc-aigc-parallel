# Agnes 第二阶段任务：全量渲染 + 质量验收

翻译已全部完成（451 页）。现在需要你接管**渲染 + QA 验收**全管线。

## 任务概述

24 个章的 `output.html` 是旧的（翻译前渲染的），需要重新渲染以生成包含英文翻译的最终 HTML。然后做全量质量验收。

## 工作区

`/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift/下册项目工作区`

## 需要重新渲染的 24 个章

```
chap-04-德儀篇·第一章
chap-21-台積電篇一·第十七章
chap-22-台積電篇一·第十八章
chap-23-台積電篇一·第十九章
chap-24-台積電篇二·卷首
chap-25-台積電篇二·第二十章
chap-26-台積電篇二·第二十一章
chap-27-台積電篇二·第二十二章
chap-28-台積電篇二·第二十三章
chap-29-台積電篇二·第二十四章
chap-30-台積電篇二·第二十五章
chap-31-台積電篇二·第二十六章
chap-32-台積電篇二·第二十七章
chap-33-台積電篇三·卷首
chap-34-台積電篇三·第二十八章
chap-35-台積電篇三·第二十九章
chap-36-台積電篇三·第三十章
chap-37-台積電篇三·第三十一章
chap-38-台積電篇三·第三十二章
chap-39-台積電篇三·第三十三章
chap-40-台積電篇三·第三十四章
chap-41-感謝
chap-42-張忠謀大事年表
chap-44-版權頁與營運成長圖
```

## 渲染命令

```bash
cd "/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift/下册项目工作区"
node render_html_v9.js --chapter <章号> --out "/Users/martin/Documents/20260812MartinGitHub /20260812 ReadShift/下册项目工作区/chap-<章号>-<对应的英文或拼音slug>/output.html"
```

slug 对照表：
- chap-04 → chap-04-德儀篇·第一章
- chap-21 → chap-21-台積電篇一·第十七章
- chap-22 → chap-22-台積電篇一·第十八章
- chap-23 → chap-23-台積電篇一·第十九章
- chap-24 → chap-24-台積電篇二·卷首
- chap-25 → chap-25-台積電篇二·第二十章
- chap-26 → chap-26-台積電篇二·第二十一章
- chap-27 → chap-27-台積電篇二·第二十二章
- chap-28 → chap-28-台積電篇二·第二十三章
- chap-29 → chap-29-台積電篇二·第二十四章
- chap-30 → chap-30-台積電篇二·第二十五章
- chap-31 → chap-31-台積電篇二·第二十六章
- chap-32 → chap-32-台積電篇二·第二十七章
- chap-33 → chap-33-台積電篇三·卷首
- chap-34 → chap-34-台積電篇三·第二十八章
- chap-35 → chap-35-台積電篇三·第二十九章
- chap-36 → chap-36-台積電篇三·第三十条
- chap-37 → chap-37-台積電篇三·第三十一章
- chap-38 → chap-38-台積電篇三·第三十二章
- chap-39 → chap-39-台積電篇三·第三十三章
- chap-40 → chap-40-台積電篇三·第三十四章
- chap-41 → chap-41-感謝
- chap-42 → chap-42-張忠謀大事年表
- chap-44 → chap-44-版權頁與營運成長圖

## QA 验收标准（每章渲染后检查）

1. **双语配对**：output.html 中 `cn-para` 数量 > 0 且 `en-para` 数量 > 0（卷首/目录章除外）
2. **繁体→简体转换（必须执行）**：渲染后立即用 OpenCC tw2s 转换 output.html，确保最终交付物为简体中文。source/ 中的繁体保持不动（作为原始数据保留），但 output.html 必须是简体
3. **控制台零报错**：渲染过程无报错
4. **文件正常生成**：output.html 大小 > 5KB

## 繁体处理规则

- **source/page_XXX.md**：保持繁体不动（原始数据存档）
- **output.html**：必须转换为简体中文（交付物）
- 转换方法：用 Python `opencc` 库 `tw2s` 转换 output.html 后写回

## 并行策略

你有多个 Agent 可以同时跑。建议按批次：
- 第一批：chap-04, 21, 22, 23, 24, 25（6 个同时）
- 第二批：chap-26, 27, 28, 29, 30（5 个同时）
- 第三批：chap-31, 32, 33, 34, 35, 36（6 个同时）
- 第四批：chap-37, 38, 39, 40, 41, 42, 44（7 个同时）

## 异常处理

如果某章渲染失败：
- 检查 source/ 中是否仍残余 ` ```rebook-translation ` fence 格式 → 转换为 `<div class="rebook-translation">` HTML 格式
- 检查是否有未闭合的 HTML 标签
- 记录失败原因，继续处理其他章，最后回头修复

## 交付

所有 24 章渲染 + QA 完成后，汇总报告：
- 成功渲染的章节数
- 发现的问题及修复情况
- 繁体字残留情况
- 双语配对异常（如有）
