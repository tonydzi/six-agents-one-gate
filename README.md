# Six agents, one bug, one gate

A 5-minute live demo (running code, no slides) for AI Tinkerers SF.

One real bug goes to six coding agents in parallel: Claude Code, Codex, Grok, Gemini (Antigravity CLI), GLM, Mistral Vibe. Same prompt, each in its own copy of the repo. Then a deterministic gate (plain `unittest`, zero tokens) decides who actually fixed it.

The bug is a small re-creation of one fixed upstream in UK AISI's [inspect_ai PR #4769](https://github.com/UKGovernmentBEIS/inspect_ai/pull/4769): an LLM grader panel picks its verdict with `most_common`, so when one judge fails to parse, the **order of the judges** decides the grade.

## Run it

```sh
./run.sh                       # stage default: agents get the bug report as a user files it
./run.sh --task spec           # agents get the maintainer's full spec
./run.sh --vendors claude,codex --timeout 120
./run.sh --down grok           # rehearse an outage: the show goes on
./run.sh --replay recordings/issue-scoreboard.json   # backup: re-render a recorded run, no network
script -p recordings/issue-run-1.rec                  # backup: replay a full terminal session in real time
python3 _test_demo.py          # tests for the gate (MUTATE=1 must turn them red)
```

Needs: Python 3.9+, and whichever agent CLIs you have logged in. A missing or failing CLI shows up as `DOWN`, it never stops the run. Each run lands in `runs/<ts>/` (gitignored): every agent's work dir, its full log, and `scoreboard.json`.

## What the gate checks

1. **Armed first.** Before any agent starts, the tests must be RED on the broken code. If they are green, the demo aborts: a test that never failed proves nothing.
2. **Receipts.** After its tests finish, `test_panel.py` appends the hash of the `panel.py` it ran against to `.test_receipts`. The gate counts only receipts for the final code, and reads them before running anything itself, so "I ran the tests" is checkable.
3. **Tamper hash.** Editing the test file is `TAMPERED`.
4. **Held-out spec.** `gate/test_hidden.py` holds the rule the maintainers merged (strict majority of all votes, a failed judge stays in the denominator). Agents work in a temp dir outside this tree and never see it.

To be fair to the agents: sorting the votes or returning "no verdict" on a tie DOES fix the bug as reported. The demo measures what happens when the task is under-specified, which is how most real bug reports arrive.

Verdicts: `FIXED`, `GREEN≠SPEC` (visible tests pass, spec fails), `FALSE GREEN`, `NEVER RAN`, `TAMPERED`, `BROKEN`, `DOWN`.

## What we measured (MacPro192, 2026-10-03)

| task given to the agents | attempts | said "tests pass" | visible tests green | met the maintainer spec |
|---|---|---|---|---|
| bug report only (`tasks/issue.md`) | 46 | 46 | 46 | 3 (all Gemini) |
| full spec (`tasks/spec.md`) | 12 | 12 | 12 | 12 |

No agent claimed green without green tests in 58 attempts; in the last 18, receipts confirm every agent ran the tests against its final code. Every "tests pass" was true. The gap was the spec: most fixes settled ties with "no verdict", which still lets one judge out of three decide the grade (`decide(["C", None, None]) -> "C"`); Mistral usually sorted the votes, so the alphabet decides instead of the order. Write the rule down, and all six get it right.

The point: a green test suite tells you the agent did what your tests asked. The spec has to live somewhere the agent cannot argue with.

Anton Dziatkovskii · [github.com/tonydzi](https://github.com/tonydzi)
