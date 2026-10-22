# Product acceptance (2026-10-22)

- Live SerpApi integration: PASS, initial TabPFN query, five title/snippet pairs, local Gemma, three lines.
- Final acceptance: PASS, five fresh searches across three topics; repeated gradient-descent query three times, one ongoing Hacktoberfest event, one everyday file-organization question.
- All final outputs: exactly three lines, no line longer than 64 characters; all final attempts completed on the first generation.
- Three repeated concept runs returned identical output in this experiment. This is not a guarantee for arbitrary topics or later search results.
- Sixteen mocked-service unit tests cover empty/missing results, invalid/oversized output, bounded retry, one-line CLI errors, credential-bearing HTTP errors and partial HTTP bodies. Mocked tests are not live evidence.
- Real search exposed marketing placeholders; the prompt and validator now reject those identities as cases. Initial shorter-prompt runs also oversimplified gradient descent and produced a vague Nobel-prize preview.
- A stricter prompt briefly failed its runtime validation; diagnostics were kept locally, then the JSON example in the prompt was clarified. Earlier public transcripts are retained as iteration evidence.
- Final event query is explicit English Hacktoberfest wording; the earlier Nobel query's first five results were noisy and are not evidence of factual coverage of all news.
- Search uses snippets rather than full pages. Format success does not prove factual accuracy; sources still need human checking before a submission article.
- No human time-saving measurement, screenshot or demo video has been claimed.
