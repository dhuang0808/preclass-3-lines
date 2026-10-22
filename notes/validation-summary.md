# Product acceptance (2026-10-22)

- Live SerpApi integration: PASS, initial TabPFN query, five title/snippet pairs, local Gemma, three lines.
- Final acceptance: PASS, five fresh searches across three topics; repeated gradient-descent query three times, one ongoing Hacktoberfest event, one everyday file-organization question.
- All final outputs: exactly three lines, no line longer than 64 characters; all final attempts completed on the first generation.
- After the final editing-artifact fix, three repeated concept runs produced two distinct texts. All kept the three-line format. Exact wording is not a stability guarantee.
- Seventeen mocked-service unit tests cover empty/missing results, invalid/oversized output, bounded retry, one-line CLI errors, credential-bearing HTTP errors and partial HTTP bodies. Mocked tests are not live evidence.
- Real search exposed marketing placeholders; the prompt and validator now reject those identities as cases. Initial shorter-prompt runs also oversimplified gradient descent and produced a vague Nobel-prize preview.
- A stricter prompt briefly failed its runtime validation; diagnostics were kept locally, then the JSON example in the prompt was clarified. Earlier public transcripts are retained as iteration evidence.
- Final event query is explicit English Hacktoberfest wording; the earlier Nobel query's first five results were noisy and are not evidence of factual coverage of all news.
- Search uses snippets rather than full pages. Format success does not prove factual accuracy; sources still need human checking before a submission article.
- No human time-saving measurement, screenshot or demo video has been claimed.

## Final B-only scope and extra evidence

- A and further TabPFN work were canceled by the user; B is the sole entry. Prize Categories: Best Use of SerpApi and Best Use of Gemma.
- A new RAG run exposed editing instructions inside otherwise valid JSON. The validator now rejects braces, code fences and replacement markers; a regression test retains the actual failure. Final three-topic live acceptance was repeated after the fix: all five runs passed, with two distinct texts across three concept runs.
- Article measurements: two successful live RAG runs at 4.56 and 4.99 seconds, and one search connection failure. Three cached-source local summaries passed with this Python client's non-loopback socket connections rejected. Full details and the guard's limited scope are in article-measurements.json.
- The two writing notes distinguish displayed-text reduction from human learning time, and local summarization from offline live search. Human lookup/reading timing remains unmeasured.
