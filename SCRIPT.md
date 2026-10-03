# Stage script, 5:00 (AI Tinkerers SF)

Setup before you walk up: terminal font 20pt+, dark theme, window ≥120 columns, `cd demos/tinkerers-5min`.
Pre-flight (backstage, 2 min before): `python3 ~/lab/bin/rails_probe.py` (all coding rails green?) and `python3 _test_demo.py` (OK).
If the venue Wi-Fi is bad: switch to phone hotspot. If still bad at 1:00, go to Plan B at once, do not wait.

| time | on screen | say (short, your own words) |
|---|---|---|
| 0:00 | terminal, nothing running | "Six coding agents. One real bug. Same prompt. Which of them fixed it? And how would you know?" |
| 0:20 | `cat panel.py` in `fixture/` | "This is an LLM grader panel: three judges vote, the panel returns one grade. I fixed this exact bug upstream in UK AISI's inspect_ai, PR 4769. When one judge fails to parse, the ORDER of the judges decides the grade." |
| 0:50 | `cat tasks/issue.md` | "This is the bug report, the way a user files it. That's all the agents get." |
| 1:00 | `./run.sh` | "Step one, before any agent runs: the gate has to be RED on the broken code. A test that has never failed proves nothing." (point at `✓ armed`) |
| 1:15 | ticker running, 6 names | "Now Claude, Codex, Grok, Gemini, GLM and Mistral, in parallel, each in its own copy. While they work: the judge is not an LLM. It's unittest. It reads a receipt the test file writes every time it runs, hashes the test file to catch edits, and runs held-out tests with the maintainer's rule: a grade needs a strict majority of ALL votes, a judge that failed still counts." |
| ~2:30 | scoreboard | "Every one says 'tests pass'. Every one is right: visible tests green, receipts show they ran them. And look at the spec column." Read ONE `↳` line aloud: `decide(["C", None, None]) -> "C"`: "one judge out of three decided the grade. That's the bug, still there, with green tests. To be fair: they fixed the bug as reported. The report was under-specified, like most are." |
| 3:15 | `./run.sh --replay recordings/spec-scoreboard.json` | "Same six agents, same bug, but I wrote the rule down in the task. Six out of six." |
| 3:40 | `cat README.md` table (or just say it) | "58 attempts on this machine today: with the bug report, 46 said 'tests pass', all 46 were green, 3 met the merged rule. With the rule written down, 12 out of 12. Nobody lied about running tests. The tests were the thing that lied, by omission." |
| 4:10 | still | "Three things to steal: arm your gate red before you trust it green. Make 'I ran the tests' a receipt, not a sentence. And keep the spec where the agent can't argue with it. The gate cost zero tokens." |
| 4:30 | `github.com/tonydzi` on screen | "Code's on GitHub, tonydzi. I run a fleet of these agents across my machines and I break them for a living. Come find me." |
| 5:00 | stop | |

## Plan B (network or vendor down)

- One or two vendors fail: do nothing. They show as `DOWN`, the table still renders. Say: "Grok's having a day. That's also a data point."
- Everything is down, or the run passes 2:50 on the clock (per-agent timeout is 110 s): Ctrl-C, then `./run.sh --replay recordings/issue-scoreboard.json` and say "here's the run from this morning, same machine". Keep going from the 2:30 line.
- Want the real-time feel without network: `script -p recordings/issue-run-1.rec` (≈75 s, plays the recorded session with original timing).
- Laptop dies: the README table and this script are enough to talk 5 minutes.

## What the result can look like live

It varies. In 7 full runs of the bug-report task, 0 or 1 of 6 met the merged rule (always Gemini, 3 times). If you get 2-3 FIXED live, the story holds: "half of them guessed the maintainer's rule, half didn't, and all of them said green." If you get 6/6 live, say "today they all guessed right, and the gate is still how I know", then show the replay.

⚠️ Do not say "the agents lied". They didn't, in 58 attempts. The claim is about green tests vs the spec.
