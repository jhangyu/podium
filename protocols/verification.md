How work is proven: the mechanical test gate run by the test-runner and the adversarial review that must actively try to refute it.

Referenced by: `podium:team-spawn`, `podium:team-fable`, `podium:team-review`, `podium:team-debug`.

## Test Gate (test-runner)

The test-runner is reactive and mechanical: it runs the exact commands it is given, captures output, and reports structured results. It never modifies code.

1. **Validate commands before running** — Confirm the requester has provided explicit commands (e.g. `npm test`, `pytest tests/`, `cargo test`). If commands are missing, ambiguous, or reference a path that does not exist, **stop and ask the requester**. Do not infer commands from context.
2. **Execute** — Run each command exactly as provided; do not modify flags, arguments, or working directories. Capture full stdout and stderr. Record the exit code for each command.
3. **Classify** — **PASS**: exit code 0, no test failures reported in output. **FAIL**: non-zero exit code, or test failures explicitly reported in output. **PARTIAL**: exit code 0 but output indicates some tests were skipped or a subset failed (e.g. pytest `x passed, y failed`).
4. **Report** — One compact structured summary per request: requester, commands executed, a results table (command / status / exit code), then failures. Cap error excerpts at **20 lines per failure** — truncate and note if longer. For PARTIAL results, list which test names passed and which failed. Do not include full stdout for passing commands.

Test-runner hard rules: never modify source code; never infer commands; never rerun failing tests with different flags unless the requester explicitly asks; always report exit codes even for commands that appear to pass; one report per request — no partial updates.

**Implementers wait for the gate**: when implementation is complete, message `team-test-runner` with the exact test commands and build commands to verify, and wait for test-runner confirmation before treating the task as done. This direct implementer→test-runner message is the standing exception to the chain-of-command routing in `${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md`, which also governs how a lead's report must carry its test-runner's verdict.

Where no runnable test command exists, the lead verifies by executing the changed path directly at least once.

## Adversarial Review

When dispatched to verify work another agent has already reported as complete, treat the report as a claim, not evidence.

- **Adversarial framing**: assume the work is broken until evidence says otherwise. Your job is to actively REFUTE the claim — not confirm it.
- **Self-produced evidence**: reproduce test runs and exercise the changed flow yourself; probe the edge cases the implementer plausibly missed. The implementer's or test-runner's own output is a claim, not evidence.
- **Negative-space question** (mandatory): "what existing behavior does this diff remove, weaken, or stop handling, and who (which caller, flow, or user) depends on it?" Read the diff for what it *doesn't* handle, not just what it does — including expired flags, shims, and TODOs left behind.
- **Verdict format**: **CONFIRMED** — every claim checked against evidence you produced yourself; list what you ran and observed. **REFUTED** — one concrete, reproducible counterexample: exact inputs/state, expected vs actual, where it breaks. One reproducible counterexample beats five suspicions.
- **Independence**: never fix anything you find — not even a one-line fix, even when it would be faster than reporting it. Fixes route back to the originating worker or squad lead. Independence is the reviewer's entire value.

## Policy Gate

Five project-policy prohibitions, each a mechanical pass/fail check. Any violation = **Critical** severity finding.

1. **Third-party API fidelity**: every third-party API call matches the version actually installed per the manifest/lockfile (implementer must have verified against that version's docs via context7); the reviewer checks version/usage consistency. Third-party APIs written from training memory = violation.
2. **Verified dependency versions**: dependency versions in new or edited manifests come from registry verification (npm/PyPI/pub.dev current); dep-freshness hook reports are addressed, never ignored.
3. **No platform forks**: no per-platform forks or exceptions in implementations — unless unreachable; an unreachability claim requires proof and a user decision.
4. **No forward-compatibility baggage** (projects are pre-release): replaced modules are deleted entirely with their tests and docs, zero residue; similar functionality converges into one generic module, no parallel paths.
5. **File-operation scripts** (test/build/CI...): cross-platform Python only, one script per functional goal, runnable with zero arguments by default. No bat/shell/powershell, no splitting into multiple files, no per-run argument dependence.

## Findings Format

Reviewers emit findings in the structured template owned by the reviewer agent definition: see `${CLAUDE_PLUGIN_ROOT}/agents/team-reviewer.md` ("Output Format"). Every finding cites a specific `file:line`, an evidence-based severity, and a concrete fix.

## Evidence Discipline

- Progress claims are audited against actual tool output before being reported — claims not backed by tool evidence are invalid.
- Task status is not proof the work is in the tree; verify with `git show <hash> --stat` or a grep for a content marker.
- Post-merge verification on the target branch is an independent gate, not a formality (see `${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md`).
- Doc claims are traceable: every "mechanism exists" claim traces to an enforcer (hook/CI/code); mechanism deliverables include a one-line liveness command proving one real run.
