# 课前三行速通 · Preclass in Three Lines

A small Chinese CLI for the last few minutes before class: enter a topic, fetch five live Google search results with **SerpApi**, and let **Gemma 3 4B running locally through Ollama** turn their titles and snippets into three short lines:

1. What it is — 它是什么
2. Why it matters — 为什么重要
3. An illustrative example — 一个例子

Built during DEV's Hacktoberfest 2026 Week 3, “Slow and Steady”. It saves opening several tabs just to get a first orientation; it does not replace a textbook or verify every claim on the web.

## Quick start in three steps

With Python, Git and Ollama installed:

1. Get the code and the model:

   ```powershell
   git clone https://github.com/dhuang0808/preclass-3-lines.git
   Set-Location preclass-3-lines
   ollama pull gemma3:4b
   ```

2. Copy `.env.example` to `.env` on first setup, then use a text editor to fill `SERPAPI_API_KEY`. Keep your existing `.env` when updating. Leave the optional proxy empty unless needed; keep Ollama running locally.
3. Run `python preclass.py "梯度下降"` and read the three lines. No pip packages are needed. Detailed requirements follow.

## Requirements and installation

- Windows with Python (tested: 3.13.15), Git, and Ollama.
- `gemma3:4b` downloaded locally; Ollama running on localhost:11434.
- A SerpApi account with available search quota.
- No third-party Python packages. `requirements.txt` documents the standard-library-only runtime.

```powershell
git clone https://github.com/dhuang0808/preclass-3-lines.git
Set-Location preclass-3-lines
ollama pull gemma3:4b
Copy-Item .env.example .env
notepad .env
```

The copy command is for first-time setup. Keep an existing `.env` when updating.

In `.env`, fill `SERPAPI_API_KEY`. Leave `SERPAPI_PROXY` empty for a direct connection, or enter your actual local HTTP proxy address. Optional `OLLAMA_URL` and `OLLAMA_MODEL` default to `http://localhost:11434` and `gemma3:4b`. Only local HTTP model addresses are accepted. Credentials are read from this file only and never printed. `.env` is ignored by Git; `.env.example` contains variable names with empty values.

## Usage

```powershell
python preclass.py "梯度下降"
python preclass.py "大学生如何整理电脑下载文件夹"
python preclass.py "检索增强生成 RAG" --save-evidence notes/my-run.json
```

On success stdout contains exactly three Chinese lines, each at most 64 characters including its label. `--save-evidence` optionally records the public titles, snippets, source links, timestamps, timings and generated output in JSON, without the API key or credential-bearing request URL.

The Google request sets `no_cache=true`, so each run uses a search request from your quota. Results are fetched at query time; that does not guarantee that the underlying pages are new or correct. The app uses the **first five organic results**, and reports a clear error if fewer than five usable title/snippet pairs are available.

## Example output

The example below is transcribed from the author's reviewed Day 3 replacement recording; see `notes/demo-run-output.txt`. Earlier three-topic receipts remain in `notes/live-*.json`, and four new coursework topics are recorded in `notes/day3-live-evidence.json`.

<!-- LIVE_EXAMPLE_START -->
```powershell
python preclass.py "梯度下降"
```

The Chinese column preserves the exact output from the same run shown in the article's GIF. The English column is a line-by-line translation.

| Chinese original | English translation |
| --- | --- |
| 它是什么：梯度下降法是一种迭代优化算法，通过计算损失函数梯度来调整模型参数，从而降低损失函数值。 | What it is: Gradient descent is an iterative optimization algorithm that adjusts model parameters by calculating the gradient of the loss function, thereby reducing the value of the loss function. |
| 为什么重要：理解梯度下降法有助于掌握机器学习模型训练的基本原理，是后续学习更高级优化算法的基础。 | Why it matters: Understanding gradient descent helps you grasp the basic principles of training machine learning models and provides a foundation for learning more advanced optimization algorithms. |
| 一个例子：假设一个图像识别模型，通过梯度下降法不断调整参数，以减少识别错误，提高准确率。 | An example: Suppose we have an image recognition model. Gradient descent continually adjusts its parameters to reduce recognition errors and improve accuracy. |
<!-- LIVE_EXAMPLE_END -->

## How it works

SerpApi retrieves five live titles and snippets, local Gemma drafts the explanation, and Python validates and prints three short lines.

`CLI topic → SerpApi live search → first 5 titles + snippets → local Gemma → validation → 3 lines`

- `preclass.py`: command-line entry point.
- `preclass_app/config.py`: project-local configuration and safe errors.
- `preclass_app/search.py`: live search and source extraction.
- `preclass_app/summary.py`: prompt, structured generation and output validation.
- `preclass_app/cli.py`: orchestration and optional evidence.

The model generates JSON fields; Python validates nonempty Chinese text, limits lengths, and prints the labels. Invalid generations get one retry, then a one-line error. Long answers are rejected, rather than silently cut mid-sentence. The example is requested as hypothetical, and known marketing placeholder identities are rejected. Search snippets are treated as untrusted reference data, not instructions. These controls improve reliability but do not prove factual correctness or complete prompt-injection resistance.

## Open innovation and privacy

Gemma's local inference is the core summarization step. The prompt, model choice and validation are inspectable and changeable; no hosted LLM API is used. The **query goes to SerpApi**, which retrieves Google results. The result snippets go to the model on this computer. This is not a fully offline application and should not be used for private queries you do not want sent to a search service.

This is the sole planned entry. Its **Prize Categories** are **Best Use of SerpApi** and **Best Use of Gemma**, both used in the working pipeline. The backup project has been canceled. Official requirements and the one-entry-per-week constraint are recorded in `notes/official-requirements.md`.

Article evidence: [why local Gemma](notes/why-local-gemma.md), [measured payoff and its limits](notes/lazy-payoff-measurement.md), and [raw measurements](notes/article-measurements.json). These distinguish machine timing from human reading time, and local inference from fully offline search.

## Errors and checks

Missing configuration, empty searches, quota errors, missing snippets, unreachable Ollama, and invalid generations produce one clear stderr message and a nonzero exit status, without a traceback. A successful run exits 0.

```powershell
python -m unittest discover -s tests -v
python scripts/validate_product.py
python scripts/check_public_files.py
```

Unit tests mock services to cover failures and leaks; they are separate from live acceptance. The live script spends five searches across three topics, including three repeated concept runs. Repeated successful formatting is not a general factual-accuracy score. `check_public_files.py` checks **staged files** before a commit; it does not audit third-party services or every past commit.

## Demo and submission status

The reviewed recording has been converted into a cropped, original-speed GIF and uploaded through the DEV editor. It is embedded in the Demo section of the saved **unpublished** draft and in `docs/submission-draft.md`. The original video remains local in ignored `notes/private/`. See `notes/video-review.md` for the review record. The article itself has not been published.

The English draft is in `docs/submission-draft.md`, with both prize categories and an explicit AI disclosure. GPT/Codex helped with code and the draft; only local Gemma summarizes at runtime. No DEV article has been published. School details were removed with the author's approval; original personal timing records remain local and ignored. Any code changes after the submission deadline must be identified here.

## Limitations

- Five snippets are a small and sometimes noisy source set; the app does not read the full pages.
- Local small-model output can be vague or wrong. The first tuning round and its limitations are retained in `notes/iteration1-*`.
- Dates and rapidly changing topics require checking the linked sources; factual correctness is not guaranteed.
- Inference speed depends on the hardware. Search availability and quota belong to SerpApi.
- The author reported four minutes and three pages for a rough first understanding of gradient descent, versus 18 seconds until the preview. About 13x compares those two personal timings, not controlled learning time; no separate preview-reading time was reported.
- Four additional coursework topics met the format checks, but manual review found a misleading matrix-multiplication explanation. See `notes/day3-results.md`; concise output is not verified teaching material.

## License

Project code: MIT (see `LICENSE`). Gemma weights, Ollama, search providers and any retrieved material retain their own licenses and terms; none are relicensed by this repository.
