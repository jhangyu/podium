How work is proven: the mechanical test gate run by the test-runner and the adversarial review that must actively try to refute it.

Referenced by:
- `podium:team-spawn`
- `podium:team-fable`
- `podium:team-review`
- `podium:team-debug`
- `podium:verification-before-completion`
- `agents/team-implementer.md`
- `agents/team-reviewer.md`
- `agents/team-test-runner.md`
- `protocols/reporting.md`
- `protocols/review.md`
- `protocols/rounds-and-review.md`
- `protocols/worktree-lifecycle.md`

## Test Gate (test-runner)

The test-runner is reactive and mechanical:
it runs the exact commands it is given, captures output, and reports structured results.
It never modifies code.
Requesters send only the checks no valid evidence record covers (Evidence Reuse below).

1. **Validate commands before running** — Confirm the requester has provided explicit commands (e.g. `npm test`, `pytest tests/`, `cargo test`).
   If commands are missing, ambiguous, or reference a path that does not exist, **stop and ask the requester**.
   Do not infer commands from context.
2. **Execute** — Run each command exactly as provided; do not modify flags, arguments, or working directories.
   Capture full stdout and stderr.
   Record the exit code for each command.
3. **Classify** —
   - **PASS**: exit code 0, no test failures reported in output.
   - **FAIL**: non-zero exit code, or test failures explicitly reported in output.
   - **PARTIAL**: exit code 0 but output reports skipped, excluded, host-excluded, or quarantined cases, or a subset failed.
     PARTIAL is never reported as PASS.
4. **Report** — One compact structured summary per request: requester, commands executed, a results table (command / status / exit code), then failures.
   Cap error excerpts at **20 lines per failure** — truncate and note if longer.
   For PARTIAL results, list which test names passed, which failed, and which did not run with the stated reason.
   Do not include full stdout for passing commands.

Test-runner hard rules:
- never modify source code
- never infer commands
- never rerun failing tests with different flags unless the requester explicitly asks
- always report exit codes even for commands that appear to pass
- one report per request — no partial updates

**Implementers wait for the gate**:
when implementation is complete, message `team-test-runner` with the exact test commands and build commands to verify,
and wait for test-runner confirmation before treating the task as done.
This direct implementer→test-runner message is the standing exception to the chain-of-command routing in `${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md`,
which also governs how a lead's report must carry its test-runner's verdict.

Where no runnable test command exists, the lead verifies by executing the changed path directly at least once.

## Adversarial Review

When dispatched to verify work another agent has already reported as complete,
treat the report as a claim, not evidence.

- **Adversarial framing**: assume the work is broken until evidence says otherwise.
  Your job is to actively REFUTE the claim — not confirm it.
- **Audit, then run the gaps**: a report without a valid evidence record (see Evidence Reuse) is a claim, not evidence — run its checks yourself.
  A valid record is audited, not re-executed; you run only the gaps and probe the edge cases the implementer plausibly missed.
- **Negative-space question** (mandatory):
  "what existing behavior does this diff remove, weaken, or stop handling,
  and who (which caller, flow, or user) depends on it?"
  Read the diff for what it *doesn't* handle, not just what it does —
  including expired flags, shims, and TODOs left behind
  (residue checks: `${CLAUDE_PLUGIN_ROOT}/protocols/review.md` H9).
  Any capability, platform, or required case that leaves the G13 manifest is a removal (`${CLAUDE_PLUGIN_ROOT}/protocols/review.md` G14).
- **Verdict format**:
  - **CONFIRMED** — every claim checked against an audited evidence record or a run you made yourself; list which records you audited and what you ran and observed.
  - **REFUTED** — one concrete, reproducible counterexample: exact inputs/state, expected vs actual, where it breaks.
  - One reproducible counterexample beats five suspicions.
- **Independence**: never fix anything you find — not even a one-line fix, even when it would be faster than reporting it.
  Fixes route back to the originating worker or squad lead.
  Independence is the reviewer's entire value.

## Evidence Discipline

- Progress claims are audited against actual tool output before being reported — claims not backed by tool evidence are invalid.
- Task status is not proof the work is in the tree;
  verify with `git show <hash> --stat` or a grep for a content marker.
- Post-merge verification on the target branch is an independent gate, not a formality (see `${CLAUDE_PLUGIN_ROOT}/protocols/worktree-lifecycle.md`): audit the existing records against the merged state and run the checks no valid record covers (Evidence Reuse).
- Doc claims are traceable:
  every "mechanism exists" claim traces to an enforcer (hook/CI/code) that the guarded action invokes — a script nothing invokes is not an enforcer;
  mechanism deliverables include a one-line liveness command proving one observed red and one observed green run.
- A red gate result is evidence against the change.
  Calling it a gate defect, flaky, or pre-existing needs the same red reproduced on the base commit; else the change is red.
- A gate verdict proves only the commit and host it ran on; a claim for another commit or platform cites that run's artifact.

## Evidence Reuse

When a prior executor left a measured-evidence record, adopt it; do not re-run the same check.

1. **Adopt, do not re-run**: the verifier or lead adopts a valid record. The verifier does not re-run the check it covers.
2. **Valid record**: per check it contains the exact command, its own exit code captured right after the command (`RC=$?`), the decisive output lines or numbers, and the code state it ran on. All four live in an artifact file the command itself wrote (output and `RC=$?` written by the command), kept until signoff; numbers that exist only in report text are a claim, not a record, and get re-run. Code state = commit hash; with uncommitted changes also record `git diff HEAD -- <paths the check covers> | shasum` at run time — the verifier recomputes it and re-runs on mismatch. A content marker alone is not a code state.
3. **Same code state, mechanically**: the record applies when `git diff <evidence commit> <state under verification> -- <paths the check covers>` is empty (or the tree hashes are equal). A different commit hash alone is not a reason to re-run.
4. **Independent verification audits the record**: confirm the command really tests the acceptance item, the RC is self-captured, and the instrument can see the change (no false green). This audit satisfies "the writer does not verify its own output". Spot-checks read the record and the code; they do not re-execute covered checks.
5. **Run only the gaps**: checks nobody ran on this code state, checks whose covered paths changed since the evidence commit, and combined-state checks a merge introduces that no record covers.
6. **Re-run is required when**: the record lacks the command, its own RC, or the code state; the covered paths changed; the audit finds the instrument blind or the result implausible (state the concrete reason); or the user asks for an independent re-run.
7. Mechanism deliveries (cron/hook/service) still need a live-run artifact; an existing live-run record that meets item 2 counts.
