---
title: "Three Lines Before Class: Live Search Meets Local Gemma"
published: false
tags: devchallenge, hf26challenge
ai_disclosure_level: fully_autonomous
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)*

## What I Built

Four minutes, three web pages, and still only a rough idea of gradient descent.

I'd never studied it before. I'm a first-year university student, and I wanted a quick way into an unfamiliar topic before class. Searching gave me plenty to read. Working out where to begin was still my job.

So I built **Preclass in Three Lines**. Type a topic into the terminal, and SerpApi fetches five live search titles and snippets. Gemma 3 4B, running locally through Ollama, turns them into three short Chinese lines: what it is, why it matters, and one example.

A little less tab-hopping seemed like a reasonable goal for Slow and Steady.

## Demo

Here's the gradient-descent run: enter a topic, wait for the search and local generation, and get the three-line preview.

![Animated terminal demo: a gradient-descent query followed by three Chinese summary lines](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/lxhxrohogr3li5zpcj75.gif)

## Code

[Source code on GitHub](https://github.com/dhuang0808/preclass-3-lines)

The Python code is MIT-licensed, with setup instructions and a real output example in the README. You'll need Python, a SerpApi account and the local Gemma model. There are no third-party Python packages to install. Search providers and model weights keep their own terms.

## How I Built It

I started by giving the model some sample notes. Could it turn them into three useful lines? Once that worked, I connected real search results.

`Topic → SerpApi → five titles and snippets → local Gemma → validation → three lines`

The app uses the first five organic results returned by SerpApi. A failed search or missing snippets produces an error instead of a made-up fallback. It reads titles and snippets, not the full pages.

Gemma returns three structured fields. Python checks for Chinese text and a limit of 64 characters per printed line, including the label. If the answer fails, it gets one retry. Credentials stay in an ignored project-local `.env` file.

Getting three lines was easier than getting three useful lines. An early search brought in marketing placeholder names. Another answer included editing instructions inside valid JSON. Both problems led to checks in the code, and I kept the failed outputs.

The core acceptance set has **17 passing unit tests** and **five live runs across three topics**: a data-science concept, the ongoing challenge and a file-organization question. I repeated the concept three times. All five outputs fit the format; the repeated topic produced two different phrasings.

A separate RAG test had two successful calls and one search connection failure. The successful previews appeared in **4.56 seconds and 4.99 seconds**. The [measurement notes](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/lazy-payoff-measurement.md) keep the failure alongside those timings.

Then I tried four topics closer to my coursework. Limits, the geometric meaning of derivatives, overfitting and matrix multiplication took **15.62, 6.12, 8.74 and 7.38 seconds** respectively.

The matrix-multiplication answer was bad. It confused rows and columns, then offered a projection example without showing a multiplication. The basic explanation should have used row-by-column dot products. You can see the original answer in the [follow-up results](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/day3-results.md).

All four new answers passed the format checks, which says something about the checks' limits. This is a first explanation to question and check against a textbook. Short snippets and a small model can leave gaps or give the wrong idea; a tidy three-line answer doesn't fix that.

## Why Does Open Innovation Matter?

Running Gemma locally lets me see and change the part that writes the explanation. I can edit the prompt, adjust the checks and try again on my own computer. Having those pieces within reach matters when I'm still learning how they fit together.

It also means the snippets and summarization prompt don't need to go to another hosted LLM. **The query still goes to SerpApi**, so live search needs the internet. With the model and cached snippets already available, the summary stage can run locally.

I paid no hosted-model API charge in these experiments. I still need the hardware, electricity, setup time and search quota. Installing a small model is extra work, and its output needs checking. Those are tradeoffs I can inspect and change alongside the code.

Publishing the failed examples gives the next person a place to start, too. They can try a better prompt or check a source and see whether their change helps.

## My Agent Session

The repository has curated [test results](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/unit-tests.txt), [live-run transcripts](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/product-validation.txt) and [initial flawed outputs](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/article-measurements-initial.json) from the build. I haven't shared an unredacted agent-session transcript.

## The Lazy Payoff

For my first encounter with gradient descent, traditional lookup took **four minutes**. I opened **three web pages** and came away with only a rough understanding. The tool produced its three-line preview in **18 seconds**.

That's about **13 times faster to an initial preview**: 240 divided by 18 is approximately 13.3. It's a personal timing comparison with different endpoints. The four minutes include searching and reading; the 18 seconds stop when the output appears. I didn't report a separate reading time for the preview, and seeing the topic once could affect the second attempt. It doesn't establish how quickly I learned it.

The RAG experiment measured text volume separately. Its five titles and snippets had 531 and 547 characters; the previews had 143 and 158 characters, including labels. That's **about 71–73% less displayed text**, rather than a percentage improvement in learning or accuracy. Those figures belong to the RAG runs, not my 18-second gradient-descent experience.

I still have the maths to learn. At least now I have a shorter starting point.

## Prize Categories

- **Best Use of SerpApi** — provides the five real search titles and snippets for each live preview.
- **Best Use of Gemma** — local Gemma 3 4B writes the three-line summary at the core of the app.

## AI Usage Disclosure

GPT/Codex helped with paired programming, code generation, testing, debugging and this article draft. I supplied the personal timing figures. This draft is marked as primarily AI-generated; my approval alone doesn't make it human-authored. The app doesn't call a GPT API: **local Gemma is its core summarization model**, and SerpApi supplies live search. I'm responsible for checking the final text, evidence and claims before publication.
