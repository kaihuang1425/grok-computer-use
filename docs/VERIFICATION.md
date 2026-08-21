# Verification plan

## Gate 0 — engineering correctness

- `pytest` for routing/verifier semantics.
- `grok inspect` confirms the skill and MCP server are discovered.
- `grok mcp doctor grok-computer-use` confirms stdio startup.

## Gate 1 — local deterministic task suite (20 tasks)

Create repeatable Windows tasks with final-state checks in Notepad, Calculator, Explorer, Settings, Paint and a browser.
Record:
- task success
- intermediate checkpoint pass rate
- actions per successful task
- recovery count
- raw-coordinate action share
- wall-clock time
- user-input takeover time

Compare three ablations using the same Grok model:
A. screenshot + coordinates only
B. UIA + screenshot fallback
C. UIA + fallback + verifier/recovery (this project)

Success criterion for moving on: C improves task success by >=10 percentage points over B OR cuts median actions per success by >=25% without reducing success.

## Gate 2 — WindowsWorld

Use WindowsWorld's 181 tasks / 17 apps / intermediate checkpoints. Run a frozen Grok model and fixed step budgets. Compare:
- final success
- intermediate checkpoint score
- success by 1/2/3+ applications
- steps-to-success
- verifier false-positive rate

Primary KPI: 3+ app final success. This is the field's weak point.

## Gate 3 — external baselines

Run or cite reproducible baselines where available:
- Agent S3 on OSWorld / WindowsAgentArena
- UFO² on its supported Windows task suites
- screenshot-only Grok harness

Do not compare scores from different task definitions as if they were head-to-head.

## Gate 4 — verifier quality

Adapt CUAVerifierBench methodology: label a held-out set of Grok trajectories with human outcome/process judgments, then compute accuracy/F1 and false-positive rate of our verifier. The goal is near-zero false success, because false success destroys trust.

## Trace schema

Each run should store JSONL with `observation`, `action`, `verification`, `recovery`, `checkpoint`, and `final` events, plus screenshots only when needed. This enables replay, ablation, and independent rescoring.
