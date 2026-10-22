# 课前三行速通 · Preclass in Three Lines

A small Chinese CLI for the last few minutes before class: enter a topic, fetch five live Google search results with **SerpApi**, and let **Gemma 3 4B running locally through Ollama** turn their titles and snippets into three short lines:

1. What it is — 它是什么
2. Why it matters — 为什么重要
3. A clearly hypothetical example — 一个例子

Built during DEV's Hacktoberfest 2026 Week 3, “Slow and Steady”. It saves opening several tabs just to get a first orientation; it does not replace a textbook or verify every claim on the web.

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
python preclass.py "TabPFN" --save-evidence notes/my-run.json
```

On success stdout contains exactly three Chinese lines, each at most 64 characters including its label. `--save-evidence` optionally records the public titles, snippets, source links, timestamps, timings and generated output in JSON, without the API key or credential-bearing request URL.

The Google request sets `no_cache=true`, so each run uses a search request from your quota. Results are fetched at query time; that does not guarantee that the underlying pages are new or correct. The app uses the **first five organic results**, and reports a clear error if fewer than five usable title/snippet pairs are available.

## Example output

The verified example and all three-topic live receipts are in `notes/live-*.json`; the run transcript is `notes/product-validation.txt`. The example below is copied from the final live concept run.

<!-- LIVE_EXAMPLE_START -->
```text
它是什么：通过迭代调整参数，降低模型预测误差
为什么重要：理解其原理有助于理解机器学习模型训练过程
一个例子：假设训练一个线性回归模型，梯度下降会调整权重，使预测值更接近真实值
```
<!-- LIVE_EXAMPLE_END -->

## How it works

`CLI topic → SerpApi live search → first 5 titles + snippets → local Gemma → validation → 3 lines`

- `preclass.py`: command-line entry point.
- `preclass_app/config.py`: project-local configuration and safe errors.
- `preclass_app/search.py`: live search and source extraction.
- `preclass_app/summary.py`: prompt, structured generation and output validation.
- `preclass_app/cli.py`: orchestration and optional evidence.

The model generates JSON fields; Python validates nonempty Chinese text, limits lengths, and prints the labels. Invalid generations get one retry, then a one-line error. Long answers are rejected, rather than silently cut mid-sentence. The example is requested as hypothetical, and known marketing placeholder identities are rejected. Search snippets are treated as untrusted reference data, not instructions. These controls improve reliability but do not prove factual correctness or complete prompt-injection resistance.

## Open innovation and privacy

Gemma's local inference is the core summarization step. The prompt, model choice and validation are inspectable and changeable; no hosted LLM API is used. The **query goes to SerpApi**, which retrieves Google results. The result snippets go to the model on this computer. This is not a fully offline application and should not be used for private queries you do not want sent to a search service.

This project uses Gemma and SerpApi meaningfully. The intended entry is **Best Use of SerpApi**; the final submission/category decision remains with the author. Official requirements and the one-entry-per-week constraint are recorded in `notes/official-requirements.md`.

## Errors and checks

Missing configuration, empty searches, quota errors, missing snippets, unreachable Ollama, and invalid generations produce one clear stderr message and a nonzero exit status, without a traceback. A successful run exits 0.

```powershell
python -m unittest discover -s tests -v
python scripts/validate_product.py
python scripts/check_public_files.py
```

Unit tests mock services to cover failures and leaks; they are separate from live acceptance. The live script spends five searches across three topics, including three repeated concept runs. Repeated successful formatting is not a general factual-accuracy score. `check_public_files.py` checks **staged files** before a commit; it does not audit third-party services or every past commit.

## Demo and submission status

Screenshot placeholder: `notes/screenshots/README.md` describes the planned capture. No screenshot or demo video is claimed to exist yet. A deployed link or video is still required for the DEV submission; a placeholder is not a completed demo.

The code was developed and tested with Codex assistance. A future DEV article must accurately disclose AI involvement; this README does not assert that a human wrote an AI-generated article. No DEV article has been published by this project.

## Limitations

- Five snippets are a small and sometimes noisy source set; the app does not read the full pages.
- Local small-model output can be vague or wrong. The first tuning round and its limitations are retained in `notes/iteration1-*`.
- Dates and rapidly changing topics require checking the linked sources; factual correctness is not guaranteed.
- Inference speed depends on the hardware. Search availability and quota belong to SerpApi.
- No measured human time-saving study or guaranteed percentage reduction is claimed.

## License

Project code: MIT (see `LICENSE`). Gemma weights, Ollama, search providers and any retrieved material retain their own licenses and terms; none are relicensed by this repository.
