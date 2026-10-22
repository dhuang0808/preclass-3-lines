# 投稿弹药 ①：为什么坚持本地 Gemma

## 可以成立的主张

我想把“搜到什么”和“怎么解释”分开：SerpApi 负责从网上取回资料，Gemma 3 4B 在电脑上负责把标题、摘要整理成三句中文。这样不需要再把这份提示词和搜索摘要交给另一家云端大模型服务。模型、提示词和格式检查都能在本机观察和调整。

这是一条有边界的隐私优势：**查询词仍会发给 SerpApi**，搜索服务本身仍参与数据处理；“本地 Gemma”不能让含隐私的查询变安全，也不意味着整台电脑没有任何联网行为。项目没有审计第三方日志或 Ollama 服务进程的全部流量。

安装好模型、拿到资料后，摘要阶段不依赖新的云端模型请求。缓存摘要可供本地推理；首次下载模型和实时 SerpApi 搜索需要网络。因此应写“摘要可本地运行”，不要写“实时搜索版完全离线”。

本次没有调用收费的云端大模型 API，**云模型 API 账单为零**。这不等于总成本为零：电脑、显存/内存、耗电、模型下载和维护都有成本；SerpApi 免费额度也有上限。云服务同样可能提供免费层，所以不能声称本地天然比所有云端方案便宜。

## 我接受的取舍

- 小模型可能遗漏重点、误解嘈杂摘要、给出空泛解释；三行合格并不等于事实正确。项目只承诺初步认识，并保留来源供核查。
- 本地速度依赖硬件、模型是否已加载，以及是否需要重试；首次安装和模型下载是额外门槛。
- 我承担本地服务、模型版本和错误处理的维护。云端方案通常减少这些安装工作，也可能提供更强的模型。
- 三行让人更快开始提问，却删掉大量细节。涉及考试定义、日期和重要事实，仍需核对原文。

## 可复查的本地阶段实验

脚本：`python scripts/measure_article_evidence.py`。原始记录：[article-measurements.json](article-measurements.json)。

实验复用同一组已取得的公开摘要，摘要调用不带 API key。脚本对**当前 Python 客户端**的 socket.connect 加限制，只允许回环地址，并先验证一个外部测试地址被拒绝。它没有改 Wi-Fi、防火墙、代理或系统配置。

具体次数和耗时见原始记录与[量化材料](lazy-payoff-measurement.md)。这只能验证这个客户端的摘要路径不需要向外建立连接；不是整机断网实验，也不能替 Ollama 服务进程或 DNS 作流量审计。

## 英文文章可用表述

> I kept Gemma local so that summarization does not require sending the prompt and search snippets to another hosted LLM. The query still goes to SerpApi. Once the model and source snippets are available, the summarization stage can run locally; live search still needs the internet. I incurred no hosted-model API charge in this experiment, but hardware, electricity, setup time and search quotas are real costs. I accept those costs in exchange for a model and prompt I can inspect and change.

## 一手参考资料

- [Ollama FAQ：本地运行时的提示词与数据](https://docs.ollama.com/faq#does-ollama-send-my-prompts-and-answers-back-to-ollamacom)。这是供应商说明，不是本项目的独立网络审计。
- [SerpApi 免费与付费额度](https://serpapi.com/pricing)。核实时公开 Free 为每月 250 次搜索；以账户实际套餐为准，不承诺未来不变。
- [本项目实际代码路径](../preclass_app/summary.py)：默认回环 HTTP 地址、关闭客户端代理转发、模型名 gemma3:4b。
