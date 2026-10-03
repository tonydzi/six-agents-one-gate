# AI Tinkerers SF: demo application text

**Title:** Six agents, one bug, one gate

**Abstract (≤120 words):**

One real bug, the one I fixed upstream in UK AISI's inspect_ai (an LLM grader panel whose verdict depends on judge order), goes live to six coding agents in parallel: Claude Code, Codex, Grok, Gemini, GLM and Mistral. Same prompt, separate repos. Then a zero-token gate decides: it must fail on the broken code before it is trusted, it checks receipts that the tests actually ran, catches edited tests, and runs held-out spec tests. Recorded on my machine: 52 of 52 bug-report attempts said "tests pass" and were right; 3 met the rule the maintainers merged. Write the rule down: 12 of 12. Running code, no slides, works offline from a recorded run if the Wi-Fi dies.

Repo: github.com/tonydzi/six-agents-one-gate
