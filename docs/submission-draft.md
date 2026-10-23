---
title: "Three Lines Before Class: Live Search Meets Local Gemma"
published: false
tags: devchallenge, hf26challenge
ai_disclosure_level: fully_autonomous
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)*

## What I Built

Four minutes, three web pages, and still only a rough idea of gradient descent.

That was my first encounter with the topic. I am a first-year university student, and the awkward part of meeting a new concept is often deciding where to start. A search engine gives me plenty of starting points. It does not decide which three things I should understand before class.

I built **Preclass in Three Lines** to make that first step smaller. Give it a topic, and it uses SerpApi to fetch five live search titles and snippets. Gemma 3 4B, running locally through Ollama, turns them into exactly three short Chinese lines: what it is, why it matters, and one example.

It is for the student who needs a foothold before opening the textbook. The work it automates is collecting a few starting sources and arranging them into a short introduction. Three lines cannot teach a whole topic, and I do not want the tool to pretend otherwise.

## Demo

The demo uses the same gradient-descent topic as my personal timing exercise: enter the topic in the terminal, wait for the live search and local generation, then read the three-line preview.

<!-- BEFORE PUBLICATION: upload or embed the reviewed video saved locally as notes/private/gradient-descent-demo-v2.mp4, then replace this comment with its accessible URL. The replacement passed visual review; the author waived a duration target. Do not publish with this placeholder. -->

## Code

[Source code on GitHub](https://github.com/dhuang0808/preclass-3-lines)

The Python code is MIT-licensed. The README covers setup, configuration and a real output example. The runtime uses the Python standard library, a SerpApi account and an installed local Gemma model. Search providers and model weights retain their own terms.

## How I Built It

I started with a deliberately small question: could a local model turn supplied notes into three useful lines? Once that worked, I replaced the sample notes with real search results.

The resulting path is short:

`Topic → SerpApi → five titles and snippets → local Gemma → validation → three lines`

SerpApi supplies the material at query time. The app takes the first five organic results; it reports an error if the search fails or usable snippets are missing. It does not silently substitute sample data. It also does not read full pages, so the answer must not imply that it did.

Gemma produces three structured fields. Python checks that they contain Chinese text and fit the limit of 64 characters per printed line, including the label. An invalid generation gets one retry, followed by a clear error if it still fails. Credentials come from an ignored project-local `.env` file.

Real runs showed why counting lines was insufficient. One early search exposed marketing placeholder names. Later, an answer contained editing instructions even though its JSON and line count looked valid. I added checks for those observed failures and kept the unsuccessful outputs as evidence. That is an improvement to a small tool, not a claim to have solved hallucination or prompt injection.

The core acceptance set contains **17 passing unit tests** and **five live runs across three topics**: a data-science concept, the ongoing challenge and an everyday file-organization question. The concept was repeated three times. All five final outputs met the formatting limits; the repeated concept produced two distinct phrasings. The tests do not establish a factual-accuracy percentage.

The [measurement notes](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/lazy-payoff-measurement.md) also keep failures visible. In a separate three-attempt RAG experiment, two live calls succeeded and one search connection failed. On the two successful calls, the preview appeared after **4.56 seconds and 4.99 seconds**. Those are successful-call timings, not an average that includes the failure.

I then tried four new topics closer to first-year coursework. Limits, the geometric meaning of derivatives, overfitting and matrix multiplication took 15.62, 6.12, 8.74 and 7.38 seconds respectively. All four produced valid three-line output. One was a useful warning: the matrix-multiplication explanation confused rows and columns, and its example mentioned projection without showing a multiplication. A correct basic explanation would use row-by-column dot products. I would not use that preview as a definition to memorize. The [full follow-up results](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/day3-results.md) preserve this failure rather than presenting nine formatted runs as nine correct answers.

## Why Does Open Innovation Matter?

For me, local inference makes experimentation tangible. I can inspect the prompt, change the validation and run the summarization model on my own computer. Gemma is the part that turns retrieved material into an explanation; it is central to the product.

I chose local Gemma to avoid sending the collected snippets and summarization prompt to another hosted LLM service. That choice has a boundary: **the query still goes to SerpApi**. Live search needs the internet. With the model and cached snippets already available, the summarization stage can work locally; the whole live-search application is not offline.

I incurred no hosted-model API charge for these experiments. Hardware, electricity, setup time and search quotas still have costs. A small local model also makes mistakes and requires installation. I accept those tradeoffs because an inspectable model and a small, editable pipeline help me learn how the system works.

Publishing the code and the failed examples gives another student something concrete to improve. They can change a prompt, inspect a source or reproduce a limitation instead of taking a polished demo on trust.

## My Agent Session

I used GPT/Codex as a programming partner to build, test and debug the project. Curated [test results](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/unit-tests.txt), [live-run transcripts](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/product-validation.txt) and [initial flawed outputs](https://github.com/dhuang0808/preclass-3-lines/blob/main/notes/article-measurements-initial.json) are in the repository. I have not published an unredacted agent-session transcript.

## The Lazy Payoff

My personal test was **gradient descent, a topic I was encountering for the first time**. Traditional lookup took **four minutes**, during which I opened **three web pages** and reached only a rough understanding. With the tool, the three-line preview appeared in **18 seconds**.

That is about **13 times faster to an initial preview**: 240 divided by 18 is approximately 13.3. It is one person's experience, not proof that everyone learns 13 times faster. The endpoints differ: the four minutes include searching and reading, while the 18 seconds measure waiting for the tool's output. A separate time for reading and understanding the three lines was not reported. Prior exposure to the topic can also affect the second attempt.

The earlier RAG machine experiment measured something narrower. Five titles and snippets contained 531 and 547 characters; their three-line outputs contained 143 and 158 characters, including labels. That is **about 71–73% less displayed text**. It is not a 71–73% improvement in learning or accuracy, and it should not be mixed with the personal 18-second run.

The useful payoff is having a small first explanation to question. I still need to check definitions, work through examples and learn the mathematics. The tool helps me start that work.

## Prize Categories

- **Best Use of SerpApi** — supplies the five real search titles and snippets that ground each live preview.
- **Best Use of Gemma** — local Gemma 3 4B performs the core three-line summarization.

## AI Usage Disclosure

GPT/Codex assisted with paired programming, code generation, testing, debugging and this article draft. The personal timing figures were supplied by me. This draft is marked as primarily AI-generated; approving an AI draft alone does not make it human-authored. The application does not call a GPT API: **local Gemma is its core summarization model**, and SerpApi provides live search. I remain responsible for checking the final text, evidence and claims before publication.
