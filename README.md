# six-agents-one-gate

A live demo: the same bug goes to six AI coding agents, and a plain test script (no AI) decides which ones really fixed it.

**Who it's for:** people who let AI agents write code and want proof the fix is right, not just a green checkmark.
**What you get:** a scoreboard with one verdict per agent (`FIXED`, `GREEN≠SPEC`, `FALSE GREEN`, `DOWN` and more). In our run, all agents said "tests pass", but only 3 of 52 attempts met the maintainer's real rule.

## Quick start
1. Install Python 3.9 or newer.
2. Run: `git clone https://github.com/tonydzi/six-agents-one-gate` then `cd six-agents-one-gate`.
3. Replay a recorded run (free, no accounts needed): `python3 demo.py --replay recordings/issue-scoreboard.json`

**Done when:** you see a table with six agents and a last line like `6/6 said "tests pass" ... 1/6 meet the maintainer spec`. That looks like a failure but is the intended result: in this recorded run five agents are marked `GREEN≠SPEC` (their tests passed, the hidden maintainer rule did not) and one is `FIXED`. The replay runs in under a minute on Windows.

> Want an AI agent to do it for you? Paste this to Claude Code / Codex / Cursor:
> "Read the 'For AI agents' section of https://github.com/tonydzi/six-agents-one-gate and set it up for me."

## For AI agents

### Preconditions
- Python 3.9+ (standard library only). `run.sh` is a POSIX shell wrapper for `python3 demo.py`; on Windows call `python demo.py` directly.
- Replay mode needs nothing else: no network, no agent CLIs, no accounts.
- A live run needs the agent CLIs the human has logged in (Claude Code, Codex, Grok, Gemini or Antigravity CLI, GLM, Mistral Vibe). A missing CLI shows as `DOWN` and never stops the run.
- Ask the human: replay or live run, and which vendors (`--vendors`). A live run spends their quota.

### Reproduce
```bash
git clone https://github.com/tonydzi/six-agents-one-gate
cd six-agents-one-gate
python3 demo.py --replay recordings/issue-scoreboard.json   # recorded run, bug report as a user files it
python3 demo.py --replay recordings/spec-scoreboard.json    # recorded run, full maintainer spec
```
Live run (only with the human's go-ahead): `./run.sh`, or `./run.sh --vendors claude,codex --timeout 120`, `./run.sh --task spec`, `./run.sh --down grok`. On Windows use `python demo.py` with the same flags instead of `./run.sh`. Results land in `runs/<timestamp>/`.

### Configure
No config files. Flags (from `demo.py` and `run.sh`): `--task spec`, `--vendors a,b`, `--timeout N`, `--down <vendor>`, `--replay <path>`. Which vendors to include comes from the human.

### Verify
```bash
python3 demo.py --replay recordings/issue-scoreboard.json
```
Expected: exit code 0 and, as the last line, `6/6 said "tests pass" · 6/6 visible tests green · 1/6 meet the maintainer spec · 0 green claims not earned · gate: 0 tokens`. (Run here: matched.) The replay re-runs the local gate for real ("armed" check), so it also proves the tests are red on the broken code.
`python3 _test_demo.py` runs the gate's own tests; on a Windows machine it did not finish within 2 minutes here, so it is not confirmed there. Run it on macOS or Linux.

### Uninstall / rollback
Delete the cloned folder. A leftover `runs/.arm` folder from an interrupted run (Windows) can be deleted before retrying; `runs/` is local output only.

### Rules for the agent
- Do not run a live demo without the human's go-ahead: it launches up to six agents on their accounts.
- Do not edit `fixture/test_panel.py` or `gate/test_hidden.py`; an edited test file is scored `TAMPERED` and the held-out spec must stay hidden from agents.
- Report the verdicts as printed. Do not upgrade `GREEN≠SPEC` to a pass.
- Never put keys or tokens into the run folders.

## Details

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
2. **Receipts.** After its tests finish, `test_panel.py` appends the hash of the `panel.py` it ran against to `.test_receipts`. The gate counts only receipts for the final code, and reads them before running anything itself, so "I ran the tests" is checkable. It is evidence, not proof: an agent could forge a receipt line by hand (none tried). The demo is a gate, not a sandbox.
3. **Tamper hash.** Editing the test file is `TAMPERED`.
4. **Held-out spec.** `gate/test_hidden.py` holds the rule the maintainers merged (strict majority of all votes, a failed judge stays in the denominator). Agents work in a temp dir outside this tree and never see it; the gate runs it in a fresh dir holding only the agent's `panel.py` and pristine tests, so files the agent leaves behind cannot shadow it.

To be fair to the agents: sorting the votes or returning "no verdict" on a tie DOES fix the bug as reported. The demo measures what happens when the task is under-specified, which is how most real bug reports arrive.

Verdicts: `FIXED`, `GREEN≠SPEC` (visible tests pass, spec fails), `FALSE GREEN`, `NEVER RAN`, `TAMPERED`, `BROKEN`, `DOWN`.

## What we measured (one Mac, 2026-10-03)

| task given to the agents | attempts | said "tests pass" | visible tests green | met the maintainer spec |
|---|---|---|---|---|
| bug report only (`tasks/issue.md`) | 52 | 52 | 52 | 3 (all Gemini) |
| full spec (`tasks/spec.md`) | 12 | 12 | 12 | 12 |

No agent claimed green without green tests in 64 attempts; in the last 24, receipts confirm every agent ran the tests against its final code. Every "tests pass" was true. The gap was the spec: most fixes settled ties with "no verdict", which still lets one judge out of three decide the grade (`decide(["C", None, None]) -> "C"`); Mistral usually sorted the votes, so the alphabet decides instead of the order. Write the rule down, and all six get it right.

The point: a green test suite tells you the agent did what your tests asked. The spec has to live somewhere the agent cannot argue with.

Anton Dziatkovskii · [github.com/tonydzi](https://github.com/tonydzi)

---

<!--ecosystem-map:start-->

## 🧩 One piece of a working system

This repository is one piece lifted out of a live operation: one engineer running a fleet of
machines, built with Claude as implementation collaborator; the machines reach consensus with
each other and wake the human only for money or the irreversible. It was extracted after it
survived production, not written as a demo — and it runs on its own: nothing here phones home
to the rest.

**See how the whole thing fits together → [SYSTEM.md](https://github.com/tonydzi/tonydzi/blob/main/SYSTEM.md)**

<!--ecosystem-map:end-->

## AI contributors

This project is built by a human + AI team, and the git log says so: Claude writes most of
the code, Codex and Grok review it, Gemini feeds the research. Each is credited on a commit
**only if its output changed that commit's content** — no decorative credits. Lab-wide
policy, one source for every repo: [AI-CONTRIBUTORS.md](https://github.com/tonydzi/.github/blob/main/AI-CONTRIBUTORS.md).
