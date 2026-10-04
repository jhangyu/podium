---
description: "Debug issues using competing hypotheses with parallel investigation, test-runner repro verification, and automatic runbook documentation"
argument-hint: "<error-description-or-file> [--hypotheses N] [--scope files|module|project] [--repro]"
---

# team-debug

Investigate a bug or error using parallel competing hypotheses, optional reproduction verification, and automatic runbook documentation.

## Phase 1: Initial Triage

Analyze the provided error description or file:
- Identify the symptom clearly (error message, stack trace, unexpected behavior)
- Determine affected scope: `--scope files` (specific files), `module` (a package/module), or `project` (whole codebase). Default: `module`.
- Gather context:
  - Recent git history for affected files
  - Relevant tests and their current pass/fail state
  - Configuration files that may be involved
  - Any environment-specific factors

Summarize the symptom in one sentence before proceeding.

## Phase 2: Hypothesis Generation

Generate N hypotheses (default: 3, override with `--hypotheses N`, max: 6).

Draw hypotheses from these categories (pick the most relevant given the symptom):
- **Logic Error** — incorrect condition, off-by-one, wrong operator
- **Data Issue** — unexpected input shape, null/undefined, encoding problem
- **State Problem** — race condition, stale cache, shared mutable state
- **Integration Failure** — API contract mismatch, version incompatibility, missing header/config
- **Resource Issue** — memory leak, file descriptor exhaustion, timeout
- **Environment** — missing env var, wrong runtime version, OS-specific behavior

Each hypothesis must include:
- Category
- Specific suspected cause (with file:line if identifiable)
- Why it would produce the observed symptom

Present hypotheses to the user and confirm before spawning agents.

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Phase 3: Investigation

Generate a team name: `debug-{timestamp}`.

Team creation: follow `${CLAUDE_PLUGIN_ROOT}/protocols/team-mode.md` (LEGACY: `TeamCreate` with `displayMode: "tmux"`; IMPLICIT: skip creation). Spawn recipe for EVERY Agent call: `name` (session-unique), `team_name` (team label), `subagent_type`, explicit `model`; the prompt includes the `ROLE: WORKER` no-spawn line and "Report via SendMessage to `team-lead`; if unreachable, send to `main`." Always include `team_name` (legacy gates require it; harmless in IMPLICIT). Then spawn agents:
- ONE `podium:team-debugger` per hypothesis (assign one hypothesis per agent)
- ONE `podium:team-doc-updater` — will document the runbook

If `--repro` flag is set: also spawn ONE `podium:team-test-runner` to attempt reproduction before full investigation begins.

## Phase 4: Repro Attempt (only if --repro)

All test-runner interaction (command validation, PASS/FAIL/PARTIAL classification, report shape) follows the verification protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/verification.md and apply it.

Signal `team-test-runner` with:
- The failing test commands, scripts, or reproduction steps derived from triage
- Instructions to capture exact failure output (exit code, stdout, stderr, stack trace)

Wait for `team-test-runner` to complete.

Pass the exact captured failure output to all `team-debugger` agents as additional context before they begin investigation.

If `team-test-runner` cannot reproduce the issue: note "Repro: NOT REPRODUCED" and flag to the user — investigation continues with original symptom description only.

## Phase 5: Evidence Collection

Use TaskList to monitor all `team-debugger` tasks.
Wait for all debuggers to complete.

Each debugger must return:
- Confidence level: High / Medium / Low
- Supporting evidence (file:line citations, log excerpts, code paths)
- Causal chain: step-by-step explanation of how the suspected cause produces the symptom
- Recommended fix (specific code change or configuration)

## Phase 6: Arbitration

Compare all findings:
1. Rank by confidence level: High > Medium > Low
2. Among equal confidence, rank by strength and completeness of causal chain
3. Identify if multiple hypotheses converge on the same root cause (strengthens that hypothesis)
4. Determine the single most likely root cause

If two hypotheses are tied and cannot be distinguished: present both to the user and ask which to prioritize for a fix attempt.

## Phase 7: Fix Verification (conditional)

This phase runs only if:
- A specific, actionable fix has been identified, AND
- `team-test-runner` is active (i.e., `--repro` flag was used)

Steps:
1. Assign a fix implementation task to `podium:team-implementer` (spawn one if not already in the team).
2. Once the implementer reports the fix is applied, signal `team-test-runner` to re-run the same commands used in Phase 4.
3. Wait for PASS or FAIL.
4. Record the result as "Fix Verified: PASS" or "Fix Verified: FAIL" in the report.

If FAIL: note which part of the fix was insufficient; do not loop — surface to the user.

## Phase 8: Documentation

Broadcast to `team-doc-updater` with:
- Root cause (winning hypothesis, confidence, causal chain)
- Evidence summary with file:line citations
- Recommended fix
- Reproduction steps (from Phase 4 if --repro, otherwise from triage)
- Fix verification result (if Phase 7 ran)

Request `team-doc-updater` to write or update a runbook entry in `DEBUGGING.md` (or an existing runbook file if found in the project).

Wait for `team-doc-updater` to confirm completion.

## Phase 9: Report and Cleanup

Present the full debug report:

```
## Debug Report: {error}

### Root Cause (Most Likely)
**Hypothesis**: {description}
**Confidence**: High/Medium/Low
**Evidence**: {summary with file:line citations}
**Causal Chain**: {step-by-step}

### Recommended Fix
{specific fix with file:line if applicable}

### Repro Verification
{PASS / FAIL / NOT REPRODUCED / N/A — include if --repro was used}

### Fix Verification
{PASS / FAIL / N/A — include if Phase 7 ran}

### Other Hypotheses
- {hypothesis 2}: {confidence} — {brief summary, why ruled out or less likely}
- {hypothesis 3}: {confidence} — {brief summary}

### Docs Updated
{file path updated by team-doc-updater, e.g. DEBUGGING.md}
```

Follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it.
