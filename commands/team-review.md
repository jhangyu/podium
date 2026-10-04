---
description: "Launch a multi-reviewer parallel code review with specialized review dimensions and automatic documentation of findings"
argument-hint: "<target> [--reviewers security,performance,architecture,testing,accessibility,techdebt] [--base-branch <branch>] [--doc]"
---

# team-review

Run a parallel code review with each reviewer specialized in one dimension.
Then consolidate findings, update the debt register, and optionally write the full report to a file.

## Phase 1: Target Resolution

Determine the review scope from the `<target>` argument:
- **File or directory path**: read the relevant files directly; no diff, so every finding is `pre-existing` (`protocols/review.md` S3)
- **Git diff**: collect the diff against `--base-branch`
- **Last commit** (`HEAD` or a commit hash): collect the diff against its parent (`<commit>~1`)
- **PR number or URL**: fetch PR diff content

`--base-branch` default: the repo's default branch from `git symbolic-ref --short refs/remotes/origin/HEAD`.
With no remote, the default is `main`; when `main` does not exist, ask the user.

Gather the full diff or file content.
Display a scope summary to the user:
- Files in scope
- Base used for the diff
- Total lines changed (if diff)
- Review dimensions that will be applied

## Language Policy

Follow the language policy in the reporting protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/reporting.md and apply it.

## Phase 2: Team Spawn

Generate a team name: `review-{timestamp}`.

Team creation: follow `${CLAUDE_PLUGIN_ROOT}/protocols/team-mode.md`.
- LEGACY: `TeamCreate` with `displayMode: "tmux"`. IMPLICIT: skip creation.
- Spawn recipe for EVERY Agent call: `name` (session-unique), `team_name` (team label), `subagent_type`, explicit `model`.
- The prompt includes the `ROLE: WORKER` no-spawn line.
- The prompt includes "Report via SendMessage to `team-lead`; if unreachable, send to `main`."
- Always include `team_name` (legacy gates require it; harmless in IMPLICIT).
- Then use TaskCreate per reviewer.

Default dimensions and agent mapping:
- Each dimension (`security`, `performance`, `architecture`, `testing`, `accessibility`, `techdebt`) → one `podium:team-reviewer`.
- Each reviewer runs only the checks `${CLAUDE_PLUGIN_ROOT}/protocols/review.md §Dimensions` assigns to its dimension.

All six dimensions are the DEFAULT set; `techdebt` runs whenever `--reviewers` is omitted.
If `--reviewers` is specified, spawn only the listed dimensions (the only way to exclude techdebt).

Always spawn ONE `podium:team-doc-updater`, with or without `--doc`.
Its writes are fixed in Phase 5.

Each reviewer prompt MUST embed the verification protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/verification.md and apply it.
It owns the adversarial framing, the self-produced-evidence rule, the negative-space question, the verdict format, and reviewer independence.

Each reviewer task must include:
- The full diff or file content, and the base used
- Their assigned dimension (checks: `${CLAUDE_PLUGIN_ROOT}/protocols/review.md §Dimensions`)
- Output: `${CLAUDE_PLUGIN_ROOT}/protocols/review.md §Finding template`

## Phase 3: Monitor and Collect

Use TaskList to track all reviewer tasks.
Wait for all reviewers, then collect their findings.

## Phase 4: Consolidation

Consolidate per `${CLAUDE_PLUGIN_ROOT}/protocols/review.md §Consolidation`.
Present introduced, non-deferred findings in severity buckets (Critical, High, Medium, Low), sorted by file path then line.
Deferred and pre-existing findings are listed and counted only in their own sections, never in a severity bucket.

For every register-bound finding (pre-existing, deferred, shortcut), per `review.md §Debt register`:
- assign the row ID `TD-<n>`
- create the ticket and fill Ticket and Owner; ask the user when no owner is known

After the row IDs are assigned, update the C3 trust tally counts for this run.

For every finding tagged `needs-user-decision` (`review.md` G14, G17), ask the user and record the answer in the finding.
Asking does not change blocking: a `pre-existing` finding still goes to the register only (S1).

## Phase 5: Documentation

Send to `team-doc-updater`:
- The full structured findings list, severity summary counts, scope metadata (target, base, timestamp)
- The register rows and the C3 tally counts

Always: `team-doc-updater` appends the register rows and updates the `## Trust tally` table in `TECH_DEBT.md` (project root).
With `--doc` only: `team-doc-updater` also writes or updates `REVIEW_FINDINGS.md` in the project root with the full report.
Without `--doc`, the full report appears inline only.

This phase runs in parallel with Phase 6; do not wait for doc completion before presenting the report.

## Phase 6: Report and Cleanup

Present the consolidated review report:

```
## Code Review: {target}
Base: {base} | Reviewers: {dimensions} | {timestamp}

### Summary
Critical: {N} | High: {N} | Medium: {N} | Low: {N} | Deferred: {N} | Pre-existing: {N}

### Critical / High / Medium / Low Findings (one section each; introduced, not deferred)
{file:line} [{dimensions}] {tags} — {rule ID}: {description}
  Suggested fix: {fix}

### Pre-existing (→ register)
{file:line} [{dimensions}] — {rule ID}: {description} | {TD-n}, {ticket}, {owner}

### Deferred
{file:line} [{dimensions}] — {rule ID}: {description} | {TD-n}, {ticket}, {owner}

### Docs Updated
TECH_DEBT.md (always); REVIEW_FINDINGS.md when --doc is set, else "full report inline only"
```

Wait for `team-doc-updater` to confirm its writes.

Follow the shutdown protocol: read ${CLAUDE_PLUGIN_ROOT}/protocols/shutdown.md and apply it.
