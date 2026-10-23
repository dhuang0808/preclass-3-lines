# 投稿弹药 ②：懒人收益，先摆实测再讲故事

## 测了什么，没测什么

2026-10-22，在这台 Windows 电脑上用 `gemma3:4b` 测试“检索增强生成 RAG 是什么”。固定流程是：三次独立实时搜索与生成；对首个成功结果的五个来源逐个请求一次；再用缓存摘要做三次本地生成。脚本：[measure_article_evidence.py](../scripts/measure_article_evidence.py)，原始数据：[article-measurements.json](article-measurements.json)。

**下方是 10 月 22 日机器流程实测，不是真人阅读实验。** 10 月 23 日作者另行报告：梯度下降第一次接触，传统查阅 4 分钟、打开 3 页，仅粗略了解；工具 18 秒出三行，约 13 倍。原始计时记录按作者要求仅留本地，公开叙事数字已获授权。三行阅读时间没有单独报告，不能声称学习速度提高 13 倍。

## 实测数字

| 项目 | 实际记录 | 能说明什么 |
| --- | --- | --- |
| 完整实时流程 | 3 次尝试，2 次成功，1 次 SerpApi 连接失败或超时 | 当前网络存在失败；不能只报两次成功而隐去失败 |
| 成功两次从调用到三行出现 | 4.56 秒、4.99 秒；成功样本中位数 4.775 秒 | 是等待输出的时间，不包含真人阅读；失败那次未记录准确耗时，不能算总体平均 |
| 搜索部分 | 成功两次为 1.07 秒、1.41 秒 | 本地生成仍占其余等待时间，不是“瞬间完成” |
| 输入与输出 | 5 条标题＋摘要共 531 / 547 字符；三行含标签共 143 / 158 字符 | 这个样本展示文本量减少约 73.1% / 71.1%，不是理解效果或时间减少比例 |
| 五个来源的固定逐页请求协议 | 尝试 5 页，HTTP 成功 3 页；1 页 403，1 页连接失败；请求时间合计 16.017 秒 | 只是取网页的自动化流程；没有浏览器渲染或人的阅读，不是传统方式学习耗时 |
| 三个成功网页的粗略 HTML 文本 | 共 17,256 个非空白字符 | 包含页面杂项、缺少动态内容，不是精确正文长度；不拿它算学习提效 |
| 缓存摘要的本地生成 | 3/3 次成功；3.201、3.150、3.216 秒 | 当前 Python 客户端只允许回环连接、不带 API key 时仍能生成三行 |
| 真人体验 | 本次机器实验未测；Day 3 作者另报 4 分钟 / 3 页 / 18 秒 | 独立体验，不能并入机器实验；三行阅读耗时未单独报告 |

字符数按 Python 字符串长度统计：输入只算标题和摘要，输出包含标签、空格、标点，不含换行；不是 token 数或阅读难度指标。2 次成功结果均为 3 行、每行不超过 64 字符、一次生成通过。量化实验前模型已使用过，不是冷启动速度测试。

三次缓存生成使用相同资料并得到相同文本；两次实时生成措辞不同。稳定的是这几个样本的格式，并非任意主题的内容一致性或事实正确率。客户端回环限制的范围见 [本地 Gemma 取舍](why-local-gemma.md)，它不是整机断网证明。

## 我的实际操作链怎样变短

固定的逐页查阅对照流程会尝试五个链接；B 正常使用只需输入一个主题，拿到三行后再决定要不要打开来源。本次 B 生成前没有打开任何来源全文，只用了五条标题和摘要。

所以现在能量化的收益是**先看到多少文字、等待多久、需要做哪些操作**，不是已经证明“理解同样内容更快”。五页是实验预先设定的协议，也不是断言每个人传统查询都要翻五页。三行适合先获得方向；重要概念仍应核对来源。

## 没有藏掉的失败

首轮记录 [article-measurements-initial.json](article-measurements-initial.json) 里，旧检查器把夹杂“替换为……”的输出误判为三行合格。这个问题出现在两次实时输出和两次缓存输出里，不能拿它们作成品示例。已补回归测试、拒绝结构残片和编辑说明，并调整提示词后重新测量。初轮时长不与修复后结果混用。

这次最终记录保留了一次真实搜索失败；失败时只显示一句安全报错，不展示密钥或异常栈。后来为改进测量脚本添加了失败耗时字段；本次已发生的失败没有可靠秒数，保持未记录，不事后猜补。

## 英文文章可用表述

> In a three-attempt machine test on my laptop, two live runs produced the three-line preview in 4.56 and 4.99 seconds; one search attempt failed. The five titles and snippets contained 531 and 547 characters, while the previews contained 143 and 158 characters including labels. That reduced displayed text by about 71–73%, not measured learning time. A separate five-link retrieval protocol reached three pages and encountered two failures. This machine test did not time a person reading those pages or the preview, so it cannot establish a human time-saving percentage. The separate author-reported gradient-descent experience is described in the submission draft.

## 文章的 Prize Categories

- **Best Use of SerpApi**：真实搜索提供五条标题和摘要，绝非模拟数据。
- **Best Use of Gemma**：本地 Gemma 3 4B 是三行摘要的核心生成步骤。

仅 B 作为本周一篇投稿。A 已按令取消。
