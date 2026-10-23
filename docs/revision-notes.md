# 修订说明

原稿已先备份为 `docs/submission-draft-v1-backup.md`，备份时 SHA-256 一致。修订稿仍为 `docs/submission-draft.md`。

## 调研后采用的原则

- 参考 [Humanizer 的公开编辑原则](https://github.com/blader/humanizer/blob/main/SKILL.md)：删掉空泛的强调和重复收尾，打散机械排比；保留已知事实，不为口语感添加经历。没有安装额外 skill，也没把文章交给第三方“改写服务”。
- 参考 [Digital.gov 清晰写作指南](https://digital.gov/guides/plain-language/writing/clear-short)：一个句子承载一个主要意思，长短句、段落长短适度穿插，让动作和结论更容易看懂。
- 浏览 DEV 参赛文章，例如 [RuleDelta](https://dev.to/shenjun93/the-500-side-hustle-that-turned-into-credits-why-i-built-ruledelta-3k35)，只借鉴具体问题开场、演示靠前的组织方式；没有借用他人经历，也没有把未核实的“高赞/获奖”当作判断依据。

## 实际修改

- 保留 “Four minutes, three web pages...” 开头，把后文改为大一学生讲自己为什么想少翻几页的口吻；使用 I'd、I'm、you'll 等自然缩写。
- 删除“工具不能教会整个主题”“测试不等于准确率”“格式合格不等于内容正确”在多节里的重复版本，把正确性局限集中到矩阵乘法失败案例后；失败原文依据、行列混淆和正确解释仍保留。
- 开放创新一节集中说明查询仍发给 SerpApi、本地摘要阶段可离线，以及硬件和配额成本；没有在其他节重复展开隐私/零成本免责声明。
- The Lazy Payoff 保留一次完整的计时边界说明：4 分钟含查阅、18 秒只到结果出现，未单独测阅读时间，先前接触可能影响第二次尝试。文字减少比例和真人计时仍分开写。
- 删掉多处节末升华，让流程、实验和失败自己说明问题。只保留少量贴合主题的轻松表达，没有新增上课、熬夜、同学反应等未经证实的情节。

## 保持不变

指定数字、模板栏目、第一段挑战链接、标签、两个 Prize Categories、模型与流程事实、AI 披露事实均保留。学校具体名称未加回。仍为未发布草稿；不声称改写能通过任何 AI 检测。

## 演示已就位：GIF

作者选择 GIF 后，已通过 DEV 正文图片上传流程把审核过的动图上传，并嵌入已保存的未发布草稿 Demo 区。图片地址为：

https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/lxhxrohogr3li5zpcj75.gif

本地 `docs/submission-draft.md` 已同步替换占位注释。回读上传文件确认是 1360×344、109 帧的真实 GIF；保存后页面显示 Unpublished Post、Fully Autonomous 和两个必带标签，Demo 图片加载成功。文章没有发布。

原稿备份保持原样。草稿预览链接及截图仅留在本地 notes/private，不提交公开仓库。原视频和真人计时原始记录也仍仅留本地。

## 补充真实输出及英文翻译

文章 Demo 区在 GIF 下方补入该次运行的三行中文原文，紧跟逐行英文翻译；README 的真实运行示例改为中英并排表格。中文逐字对照 `notes/demo-run-output.txt` 和 GIF 末帧，未重新调用模型生成另一份输出。两处共用相同译文，标签译为 What it is / Why it matters / An example；只翻译原文已有意思，没有补充解释、改正模型内容或增加结论。工具代码及原稿备份不变。
