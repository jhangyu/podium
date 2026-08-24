How work is proven: the mechanical test gate run by the test-runner and the adversarial review that must actively try to refute it.

Referenced by: `podium:team-spawn`, `podium:team-fable`, `podium:team-review`, `podium:team-debug`.

## Test Gate (test-runner)

The test-runner is reactive and mechanical: it runs the exact commands it is given, captures output, and reports structured results. It never modifies code.

1. **Validate commands before running** — Confirm the requester has provided explicit commands (e.g. `npm test`, `pytest tests/`, `cargo test`). If commands are missing, ambiguous, or reference a path that does not exist, **stop and ask the requester**. Do not infer commands from context.
2. **Execute** — Run each command exactly as provided; do not modify flags, arguments, or working directories. Capture full stdout and stderr. Record the exit code for each command.
3. **Classify** — **PASS**: exit code 0, no test failures reported in output. **FAIL**: non-zero exit code, or test failures explicitly reported in output. **PARTIAL**: exit code 0 but output indicates some tests were skipped or a subset failed (e.g. pytest `x passed, y failed`).
4. **Report** — One compact structured summary per request: requester, commands executed, a results table (command / status / exit code), then failures. Cap error excerpts at **20 lines per failure** — truncate and note if longer. For PARTIAL results, list which test names passed and which failed. Do not include full stdout for passing commands.

Test-runner hard rules: never modify source code; never infer commands; never rerun failing tests with different flags unless the requester explicitly asks; always report exit codes even for commands that appear to pass; one report per request — no partial updates.

**Implementers wait for the gate**: when implementation is complete, message `team-test-runner` with the exact test commands and build commands to verify, and wait for test-runner confirmation before treating the task as done. A squad lead's report without its test-runner's PASS/FAIL result is invalid.

Where no runnable test command exists, the lead verifies by executing the changed path directly at least once.

## Adversarial Review

When dispatched to verify work another agent has already reported as complete, treat the report as a claim, not evidence.

- **Adversarial framing**: assume the work is broken until evidence says otherwise. Your job is to actively REFUTE the claim — not confirm it.
- **Self-produced evidence**: reproduce test runs and exercise the changed flow yourself; probe the edge cases the implementer plausibly missed. The implementer's or test-runner's own output is a claim, not evidence.
- **Negative-space question** (mandatory): "what existing behavior does this diff remove, weaken, or stop handling, and who (which caller, flow, or user) depends on it?" Read the diff for what it *doesn't* handle, not just what it does.
- **Verdict format**: **CONFIRMED** — every claim checked against evidence you produced yourself; list what you ran and observed. **REFUTED** — one concrete, reproducible counterexample: exact inputs/state, expected vs actual, where it breaks. One reproducible counterexample beats five suspicions.
- **Independence**: never fix anything you find — not even a one-line fix, even when it would be faster than reporting it. Fixes route back to the originating worker or squad lead. Independence is the reviewer's entire value.

## Findings Format

For each finding:

```
### [SEVERITY] Finding Title

**Location**: `path/to/file.ts:42`
**Dimension**: Security | Performance | Architecture | Testing | Accessibility
**Severity**: Critical | High | Medium | Low

**Evidence**:
Description of what was found, with code snippet if relevant.

**Impact**:
What could go wrong if this is not addressed.

**Recommended Fix**:
Specific, actionable remediation with code example if applicable.
```

## Evidence Discipline

- Progress claims are audited against actual tool output before being reported — claims not backed by tool evidence are invalid.
- Task status is not proof the work is in the tree; verify with `git show <hash> --stat` or a grep for a content marker.
- Post-merge verification on the target branch is an independent gate, not a formality (see `${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md`).
